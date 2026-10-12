"""カレーづくりの工程モデル。
食品の安全性や実際の加熱時間は判定しません。

Python 3.12以上の基本構文・標準ライブラリのみを使用。
new_job / prepare / heat / plate は新しい状態を返します。
呼び出し元の在庫・レシピ・状態は変更しません。
"""


def positive_int(value, label):
    """boolを除く正のintを要求する。
    型違いはTypeError、範囲外はValueError。
    """
    if type(value) is not int:
        raise TypeError(f"{label}は整数で指定してください")
    if value <= 0:
        raise ValueError(f"{label}は1以上にしてください")


def make_recipe(kind="standard"):
    """呼び出しごとに独立したレシピを作る。分量は教育用の仮定。"""
    amounts = {
        "肉_g": 100, "玉ねぎ_g": 75, "じゃがいも_g": 75,
        "にんじん_g": 40, "ルー_g": 25, "水_ml": 250,
        "炊飯済みご飯_g": 180,
    }
    if kind == "standard":
        return {
            "name": "基本カレー",
            "per_person": amounts,
            "heat_steps": 6,
        }
    if kind == "seafood":
        del amounts["肉_g"]
        amounts["シーフード_g"] = 100
        return {
            "name": "シーフードカレー",
            "per_person": amounts,
            "heat_steps": 4,
        }
    raise ValueError("レシピはstandardまたはseafoodです")


def validate_recipe(recipe):
    if not isinstance(recipe, dict):
        raise TypeError("レシピは辞書で指定してください")
    name = recipe.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("レシピ名が必要です")
    amounts = recipe.get("per_person")
    if not isinstance(amounts, dict) or not amounts:
        raise ValueError("1人分の材料辞書が必要です")
    for name, amount in amounts.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("材料名は空でない文字列にしてください")
        positive_int(amount, name)
    positive_int(recipe.get("heat_steps"), "加熱ステップ数")


def requirements(recipe, servings):
    """必要量の辞書を返す。servingsは1〜20人。入力を変更しない。"""
    validate_recipe(recipe)
    positive_int(servings, "人数")
    if servings > 20:
        raise ValueError("人数は20以下にしてください")
    needed = {}
    for name, amount in recipe["per_person"].items():
        needed[name] = amount * servings
    return needed


def validate_stock(stock):
    if not isinstance(stock, dict):
        raise TypeError("在庫は辞書で指定してください")
    for name, amount in stock.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("在庫の材料名が不正です")
        if type(amount) is not int:
            raise TypeError(f"{name}の在庫は整数にしてください")
        if amount < 0:
            raise ValueError(f"{name}の在庫は0以上にしてください")


def shortages(stock, needed):
    """不足量だけを返す。未登録の材料は在庫0とみなす。"""
    validate_stock(stock)
    missing = {}
    for name, amount in needed.items():
        positive_int(amount, name)
        gap = amount - stock.get(name, 0)
        if gap > 0:
            missing[name] = gap
    return missing


def reserve(stock, needed):
    """全材料が揃うときだけ差し引いた新在庫を返す。
    不足時はValueError。
    """
    missing = shortages(stock, needed)
    if missing:
        raise ValueError(f"材料不足: {missing}")
    remaining = stock.copy()
    for name, amount in needed.items():
        remaining[name] -= amount
    return remaining


def new_job(recipe, servings):
    """計画状態を作る。
    レシピから必要な値だけを取り込み、共有を避ける。
    """
    needed = requirements(recipe, servings)
    return {
        "recipe_name": recipe["name"], "servings": servings,
        "needed": needed, "heat_target": recipe["heat_steps"],
        "heat_done": 0, "stage": "planned", "history": ["計画済み"],
    }


def move(job, stage, event):
    """内部補助。新しい辞書と履歴リストを作る。"""
    updated = job.copy()
    updated["needed"] = job["needed"].copy()
    updated["history"] = job["history"] + [event]
    updated["stage"] = stage
    return updated


def prepare(job):
    """確保済み状態を下ごしらえ済みにする。順序違反はRuntimeError。"""
    if job["stage"] != "reserved":
        raise RuntimeError("材料確保後に下ごしらえしてください")
    return move(job, "prepared", "下ごしらえ完了")


def heat(job, stove_ok=True):
    """仮想加熱を1ステップ進める。故障時・順序違反時はRuntimeError。"""
    if type(stove_ok) is not bool:
        raise TypeError("コンロ状態はboolで指定してください")
    if job["stage"] not in ("prepared", "heating"):
        raise RuntimeError("下ごしらえ後、加熱完了前に実行してください")
    if not stove_ok:
        raise RuntimeError("コンロ故障: 加熱を中断しました")
    count = job["heat_done"] + 1
    stage = "cooked" if count == job["heat_target"] else "heating"
    updated = move(job, stage, f"加熱 {count}/{job['heat_target']}")
    updated["heat_done"] = count
    return updated


def plate(job):
    """加熱完了状態のみを盛り付ける。"""
    if job["stage"] != "cooked":
        raise RuntimeError("加熱が完了していません")
    return move(job, "done", "盛り付け完了")


def is_complete(job):
    """本モジュールの関数で作った状態について、完成条件を確認する。"""
    return (
        job["stage"] == "done"
        and job["heat_done"] == job["heat_target"]
        and "材料確保" in job["history"]
        and "下ごしらえ完了" in job["history"]
        and job["history"][-1] == "盛り付け完了"
    )


def run_simulation(recipe, servings, stock, stove_ok=True):
    """工程を実行して結果辞書を返す。
    画面表示も入力データの変更もしない。

    不正な入力はTypeError/ValueError。
    材料不足・機器故障はok=Falseの結果。
    確保後の失敗では、確保分を返却しない在庫方針を採用する。
    """
    job = new_job(recipe, servings)
    validate_stock(stock)
    if type(stove_ok) is not bool:
        raise TypeError("コンロ状態はboolで指定してください")
    remaining = stock.copy()
    error = None
    missing = shortages(stock, job["needed"])
    if missing:
        error = f"材料不足: {missing}"
    else:
        remaining = reserve(stock, job["needed"])
        job = move(job, "reserved", "材料確保")
        try:
            job = prepare(job)
            while job["stage"] != "cooked":
                job = heat(job, stove_ok)
            job = plate(job)
        except RuntimeError as exc:
            error = str(exc)
    return {
        "ok": error is None and is_complete(job),
        "job": job, "remaining": remaining, "error": error,
    }


def main():
    """対話入力と表示を担当する、副作用のある外側の処理。"""
    print("カレー工程シミュレーター（仮想工程・実際の安全判定なし）")
    try:
        servings = int(input("人数（1〜20）: "))
        kind = input("レシピ standard / seafood [standard]: ")
        kind = kind.strip() or "standard"
        recipe = make_recipe(kind)
        needed = requirements(recipe, servings)
        stock = {}
        for name, amount in needed.items():
            raw = input(f"{name}の在庫 [必要量{amount}]: ").strip()
            stock[name] = amount if raw == "" else int(raw)
        answer = input("コンロは正常ですか y/n [y]: ")
        answer = answer.strip().lower() or "y"
        if answer not in ("y", "n"):
            raise ValueError("コンロ状態はyまたはnで入力してください")
        result = run_simulation(
            recipe, servings, stock, stove_ok=(answer == "y")
        )
    except (TypeError, ValueError) as exc:
        print(f"入力エラー: {exc}")
        return
    except (EOFError, KeyboardInterrupt):
        print("\n入力を中断しました")
        return
    for event in result["job"]["history"]:
        print(event)
    print("完成" if result["ok"] else f"未完成: {result['error']}")
    print("残り在庫:", result["remaining"])


if __name__ == "__main__":
    main()