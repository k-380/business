"""本書の短い実行例を選択して動かします。
python curry_python_examples.py --list
python curry_python_examples.py 09-04
python curry_python_examples.py
16-02のみpytestを必要とします。省略時はその例を飛ばします。
"""
import sys

EXAMPLES = {
'05-01': r'''
print("材料を確認する")
print("下ごしらえをする")
print("加熱する")
print("盛り付ける")
'''.strip(),

'05-02': r'''
# これは手順の表示だけで、実際の加熱ではありません。
print("加熱工程を案内する")  # 行の途中からもコメントを書けます。
'''.strip(),

'06-01': r'''
servings = 2
meat_per_person_g = 100
meat_g = servings * meat_per_person_g
print(meat_g)
print("必要な肉:", meat_g, "g")
'''.strip(),

'06-02': r'''
potatoes_count = 3
water_l = 0.5
ingredient_name = "玉ねぎ"
prepared = False
print(type(potatoes_count).__name__)
print(type(water_l).__name__)
print(type(ingredient_name).__name__)
print(type(prepared).__name__)
'''.strip(),

'06-03': r'''
meat_g = 200
reserved_g = meat_g
meat_g = meat_g - 50
print(meat_g)
print(reserved_g)
'''.strip(),

'06-a': r'''
servings = 3
meat_per_person_g = 100
print(servings * meat_per_person_g)
'''.strip(),

'07-01': r'''
def 下ごしらえ():
    print("肉を切る")
    print("野菜を切る")

print("調理開始")
下ごしらえ()
print("次の工程へ")
'''.strip(),

'07-02': r'''
def 肉を切る():
    print("肉を切る")

def 野菜を切る():
    print("野菜を切る")

def 下ごしらえ():
    肉を切る()
    野菜を切る()

def カレーを作る():
    print("開始")
    下ごしらえ()
    print("加熱の準備へ")

カレーを作る()
'''.strip(),

'08-01': r'''
def 下ごしらえ(肉, 野菜):
    print("肉:", 肉)
    print("野菜:", 野菜)

下ごしらえ("豚肉", "玉ねぎ")
下ごしらえ("鶏肉", "にんじん")
'''.strip(),

'08-02': r'''
def 必要な肉_g(人数, 一人分_g):
    print(人数 * 一人分_g)

必要な肉_g(2, 100)
必要な肉_g(人数=3, 一人分_g=100)
'''.strip(),

'08-03': r'''
def 切り方を案内する(材料, 大きさ_mm=20):
    print(材料, 大きさ_mm, "mmに切る想定")

切り方を案内する("玉ねぎ")
切り方を案内する("にんじん", 10)
'''.strip(),

'08-04': r'''
def 名前を付け直す(材料):
    材料 = "カット済み玉ねぎ"
    print("関数内:", 材料)

元の材料 = "玉ねぎ"
名前を付け直す(元の材料)
print("呼び出し元:", 元の材料)
'''.strip(),

'09-01': r'''
def 下ごしらえ(肉, 野菜):
    具材 = "カット済み:" + 肉 + "・" + 野菜
    return 具材

結果 = 下ごしらえ("豚肉", "玉ねぎ")
print(結果)
'''.strip(),

'09-02': r'''
def 具材を分けて返す(肉, 野菜):
    return "カット済み:" + 肉, "カット済み:" + 野菜

肉の結果, 野菜の結果 = 具材を分けて返す("豚肉", "玉ねぎ")
print(肉の結果)
print(野菜の結果)
'''.strip(),

'09-03': r'''
def 下ごしらえ(肉, 野菜):
    return "カット済み(" + 肉 + "・" + 野菜 + ")"

def 加熱(具材):
    return "調理済み(" + 具材 + ")"

def 盛り付け(カレー):
    return "一皿(" + カレー + ")"

def カレーを作る(肉, 野菜):
    具材 = 下ごしらえ(肉, 野菜)
    カレー = 加熱(具材)
    一皿 = 盛り付け(カレー)
    return 一皿

print(カレーを作る("豚肉", "玉ねぎ"))
'''.strip(),

'09-04': r'''
def 表示する(人数):
    print(人数 * 100)

def 返す(人数):
    return 人数 * 100

a = 表示する(2)
b = 返す(2)
print("a =", a)
print("b =", b)
'''.strip(),

'09-a': r'''
def necessary_meat_g(servings):
    return servings * 100

amount_g = necessary_meat_g(3)
print("必要量:", amount_g, "g")
'''.strip(),

'10-01': r'''
heat_done = 4
heat_target = 6

if heat_done >= heat_target:
    print("仮想加熱完了")
else:
    print("仮想加熱を続ける必要があります")
'''.strip(),

'10-02': r'''
stove_ok = False
heat_done = 6
heat_target = 6

if not stove_ok:
    print("故障のため中断")
elif heat_done < heat_target:
    print("加熱途中")
else:
    print("次工程へ")
'''.strip(),

'10-03': r'''
stock_g = 200
needed_g = 200
stove_ok = True
can_start = stock_g >= needed_g and stove_ok
print(can_start)

if can_start:
    print("この二条件について開始可能")
'''.strip(),

'11-01': r'''
for number in range(1, 4):
    print("じゃがいも", number, "を切る")
print("全個処理しました")
'''.strip(),

'11-02': r'''
heat_done = 0
heat_target = 3

while heat_done < heat_target:
    heat_done = heat_done + 1
    print("仮想加熱", heat_done)

print("規定ステップに到達")
'''.strip(),

'11-03': r'''
for number in range(1, 5):
    if number == 2:
        continue
    if number == 4:
        break
    print("処理対象", number)
print("繰り返しの外")
'''.strip(),

'11-04': r'''
def cut_label(number):
    return "カット済みじゃがいも" + str(number)

for number in range(1, 4):
    result = cut_label(number)
    print(result)
'''.strip(),

'12-01': r'''
shopping = ["肉", "玉ねぎ", "ルー"]
print(shopping[0])
shopping.append("にんじん")
shopping.remove("ルー")
for name in shopping:
    print(name)
'''.strip(),

'12-02': r'''
stock = {"肉_g": 300, "玉ねぎ_g": 200}
print(stock["肉_g"])
print(stock.get("ルー_g", 0))
print("肉_g" in stock)
'''.strip(),

'12-03': r'''
stock = {"肉_g": 300}
stock["ルー_g"] = 100
stock["肉_g"] = stock["肉_g"] - 200
del stock["ルー_g"]
print(stock)
'''.strip(),

'12-04': r'''
stock = {"肉_g": 150, "玉ねぎ_g": 200}
needed = {"肉_g": 200, "玉ねぎ_g": 150, "ルー_g": 50}
missing = {}

for name, amount in needed.items():
    gap = amount - stock.get(name, 0)
    if gap > 0:
        missing[name] = gap

print(missing)
'''.strip(),

'12-05': r'''
def calculate_needed(per_person, servings):
    needed = {}
    for name, amount in per_person.items():
        needed[name] = amount * servings
    return needed

recipe = {"肉_g": 100, "玉ねぎ_g": 75, "ルー_g": 25}
print(calculate_needed(recipe, 2))
print(recipe)
'''.strip(),

'12-06': r'''
def subtract_stock(stock, needed):
    for name, amount in needed.items():
        if stock.get(name, 0) < amount:
            return None
    remaining = stock.copy()
    for name, amount in needed.items():
        remaining[name] = remaining[name] - amount
    return remaining

stock = {"肉_g": 300, "ルー_g": 100}
remaining = subtract_stock(stock, {"肉_g": 200, "ルー_g": 50})
print(remaining)
print(stock)
'''.strip(),

'13-01': r'''
def use_meat(stock, amount_g):
    stock["肉_g"] = stock["肉_g"] - amount_g
    return "材料を確保しました"

fridge = {"肉_g": 300}
message = use_meat(fridge, 100)
print(message)
print(fridge)
'''.strip(),

'13-02': r'''
def replace_name(stock):
    stock = {"肉_g": 0}
    return stock

fridge = {"肉_g": 300}
other = replace_name(fridge)
print(fridge)
print(other)
'''.strip(),

'13-03': r'''
meat_g = 300

def local_change():
    meat_g = 100
    print("内側:", meat_g)

def global_change():
    global meat_g
    meat_g = meat_g - 50

local_change()
print("外側:", meat_g)
global_change()
print("変更後:", meat_g)
'''.strip(),

'13-04': r'''
def add_ingredient(name, basket=[]):
    basket.append(name)
    return basket

print(add_ingredient("肉"))
print(add_ingredient("玉ねぎ"))
'''.strip(),

'13-05': r'''
def add_ingredient(name, basket=None):
    if basket is None:
        basket = []
    basket.append(name)
    return basket

print(add_ingredient("肉"))
print(add_ingredient("玉ねぎ"))
'''.strip(),

'13-06': r'''
original = {"材料": ["肉", "玉ねぎ"]}
shallow = original.copy()
shallow["材料"].append("にんじん")
print(original)
print(shallow)
print(original is shallow)
print(original["材料"] is shallow["材料"])
'''.strip(),

'13-07': r'''
def remaining_stock(stock, used_g):
    new_stock = stock.copy()
    new_stock["肉_g"] = stock["肉_g"] - used_g
    return new_stock

stock = {"肉_g": 300}
next_stock = remaining_stock(stock, 100)
print("前:", stock)
print("後:", next_stock)
stock = next_stock
print("採用した在庫:", stock)
'''.strip(),

'13-a': r'''
def added_ingredient(name, basket=None):
    result = [] if basket is None else basket.copy()
    result.append(name)
    return result

original = ["肉"]
print(added_ingredient("玉ねぎ", original))
print(original)
'''.strip(),

'14-01': r'''
def cut_with_knife(name):
    return "カット済み:" + name

def cut_with_processor(name):
    return "カット済み:" + name

def prepare_names(names, cutter):
    results = []
    for name in names:
        results.append(cutter(name))
    return results

names = ["玉ねぎ", "にんじん"]
print(prepare_names(names, cut_with_knife))
print(prepare_names(names, cut_with_processor))
'''.strip(),

'15-01': r'''
def heat_once(stove_ok):
    if not stove_ok:
        raise RuntimeError("コンロが動きません")
    return "仮想加熱を1ステップ実行"

try:
    result = heat_once(False)
    print(result)
except RuntimeError as exc:
    print("中断:", exc)
print("状況を確認してください")
'''.strip(),

'15-02': r'''
def check_servings(servings):
    if type(servings) is not int:
        raise TypeError("人数は整数にしてください")
    if not 1 <= servings <= 20:
        raise ValueError("人数は1〜20にしてください")
    return servings

for value in (2, 0, "2", True):
    try:
        print("受付:", check_servings(value))
    except (TypeError, ValueError) as exc:
        print("不正:", exc)
'''.strip(),

'15-03': r'''
def heat_once(stove_ok):
    if not stove_ok:
        raise RuntimeError("コンロ故障")
    return "加熱実行"

history = ["材料確保", "下ごしらえ完了"]
try:
    history.append(heat_once(False))
except RuntimeError as exc:
    history.append("中断理由: " + str(exc))

for event in history:
    print(event)
'''.strip(),

'15-04': r'''
stock = {"肉_g": 300}
try:
    stock["肉_g"] -= 100
    raise RuntimeError("確保後の故障")
except RuntimeError:
    print("処理を中断")
finally:
    print("終了確認を実行")
print(stock)
'''.strip(),

'16-01': r'''
def necessary_meat_g(servings):
    return servings * 100

assert necessary_meat_g(1) == 100
assert necessary_meat_g(3) == 300
print("必要量の確認に合格")
'''.strip(),

'16-02': r'''
def necessary_meat_g(servings):
    if type(servings) is not int:
        raise TypeError("整数を指定してください")
    if not 1 <= servings <= 20:
        raise ValueError("人数が範囲外です")
    return servings * 100

def test_three_servings():
    assert necessary_meat_g(3) == 300

def test_invalid_servings():
    import pytest
    with pytest.raises(ValueError):
        necessary_meat_g(0)
'''.strip(),

'17-01': r'''
from curry_python_simulator import make_recipe, requirements

recipe = make_recipe()
needed = requirements(recipe, 2)
print(recipe["name"])
print(needed["肉_g"])
print(needed["水_ml"])
'''.strip(),

'18-01': r'''
from curry_python_simulator import make_recipe, requirements

recipe = make_recipe()
needed = requirements(recipe, 2)
for name, amount in needed.items():
    print(name, amount)
'''.strip(),

'18-02': r'''
from curry_python_simulator import make_recipe, requirements, run_simulation

recipe = make_recipe()
stock = requirements(recipe, 2)
stock["肉_g"] = 199
result = run_simulation(recipe, 2, stock)
print(result["ok"])
print(result["error"])
print(result["job"]["history"])
print(result["remaining"] == stock)
'''.strip(),

'18-03': r'''
from curry_python_simulator import make_recipe, requirements, run_simulation

recipe = make_recipe()
stock = requirements(recipe, 2)
result = run_simulation(recipe, 2, stock)
for event in result["job"]["history"]:
    print(event)
print("完成判定:", result["ok"])
'''.strip(),

'18-04': r'''
from curry_python_simulator import make_recipe, requirements, run_simulation

recipe = make_recipe()
stock = requirements(recipe, 2)
result = run_simulation(recipe, 2, stock, stove_ok=False)
print(result["ok"])
print(result["job"]["stage"])
print(result["job"]["heat_done"])
print(result["remaining"]["肉_g"])
print(stock["肉_g"])
'''.strip(),

'18-05': r'''
from curry_python_simulator import make_recipe, requirements, run_simulation

recipe = make_recipe()
stock = requirements(recipe, 2)
first = run_simulation(recipe, 2, stock)
stock = first["remaining"]
second = run_simulation(recipe, 2, stock)
print("1回目:", first["ok"])
print("2回目:", second["ok"])
'''.strip(),

'18-06': r'''
from curry_python_simulator import make_recipe, requirements, run_simulation

recipe = make_recipe("seafood")
recipe["per_person"]["玉ねぎ_g"] = 90
stock = requirements(recipe, 3)
result = run_simulation(recipe, 3, stock)
print(recipe["name"])
print(stock["玉ねぎ_g"])
print(stock["シーフード_g"])
print("肉_g" in stock)
print(result["job"]["heat_done"])
print(result["ok"])
'''.strip(),

'D-01': r'''
def shopping_shortage(stock, needed):
    result = {}
    for name, amount in needed.items():
        gap = amount - stock.get(name, 0)
        if gap > 0:
            result[name] = gap
    return result

stock = {"肉_g": 250, "ルー_g": 100}
needed = {"肉_g": 300, "ルー_g": 75}
result = shopping_shortage(stock, needed)
assert result == {"肉_g": 50}
assert stock == {"肉_g": 250, "ルー_g": 100}
print(result)
'''.strip(),

'D-02': r'''
def possible_servings(stock, per_person):
    limits = []
    for name, amount in per_person.items():
        limits.append(stock.get(name, 0) // amount)
    return min(limits)

recipe = {"肉_g": 100, "ルー_g": 25}
stock = {"肉_g": 350, "ルー_g": 100}
print(possible_servings(stock, recipe))
print(possible_servings({"肉_g": 350}, recipe))
'''.strip(),

'D-03': r'''
def recorded(state, event):
    result = state.copy()
    result["history"] = state["history"] + [event]
    return result

before = {"stage": "prepared", "history": ["下ごしらえ"]}
after = recorded(before, "加熱開始")
print(before["history"])
print(after["history"])
assert before["history"] is not after["history"]
'''.strip(),

'F-01': r'''
def count_tasks(task):
    if isinstance(task, str):
        return 1
    total = 0
    for child in task:
        total += count_tasks(child)
    return total

recipe_tasks = [
    ["肉を切る", "野菜を切る"],
    ["炒める", "煮込む", "ルーを加える"],
    "盛り付ける",
]
print(count_tasks(recipe_tasks))
print(count_tasks([]))
'''.strip(),

'F-02': r'''
class Pantry:
    def __init__(self, stock):
        self.stock = stock.copy()

    def remaining(self, name):
        return self.stock.get(name, 0)

    def use(self, name, amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("使用量は正の整数にしてください")
        if self.remaining(name) < amount:
            raise ValueError("在庫不足です")
        self.stock[name] -= amount

pantry = Pantry({"肉_g": 300})
pantry.use("肉_g", 100)
print(pantry.remaining("肉_g"))
'''.strip(),

}


def run_example(name):
    namespace = {"__name__": "__example__"}
    print("\n--- 例 " + name + " ---")
    exec(compile(EXAMPLES[name], "example_" + name, "exec"), namespace)
    if name == "16-02":
        namespace["test_three_servings"]()
        namespace["test_invalid_servings"]()
        print("2件のテストに合格")


def main():
    args = sys.argv[1:]
    if args == ["--list"]:
        print("\n".join(EXAMPLES))
        return
    selected = args or [name for name in EXAMPLES if name != "16-02"]
    for name in selected:
        if name not in EXAMPLES:
            raise SystemExit("例番号がありません: " + name)
        run_example(name)
    if not args:
        print("\n16-02はpytest使用例のため省略しました。個別に選択できます。")


if __name__ == "__main__":
    main()