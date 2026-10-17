# Pythonで学ぶ探索アルゴリズム

<p class="subtitle">全探索から再帰・動的計画法・最適化まで</p>
<p class="deck">数独、麻雀、迷路、ナップサック問題、人生の壺で学ぶ全12回講義</p>
<p class="edition">初版 · 2026年10月17日 · Python 3.11以降 · 標準ライブラリで実習</p>

## はじめに――答えを探す方法を選ぶ

プログラムに計算させるとき、難しいのは計算式を一つ書くことだけではない。どの候補を調べ、どこで諦め、どの計算結果を再利用するかを決める必要がある。本書は、その判断を探索という共通の視点から学ぶ教科書である。

たとえば麻雀の手牌を面子に分ける問題は、牌の組を取り出して残りを調べる再帰で表せる。数独も、数字を置いて残りを調べるという同型の構造を持つ。しかし同じ再帰でも、全解を列挙するか、一つ見つけて終えるかでreturnと復元処理が変わる。コードを似た形へ写すだけではなく、この契約の違いを言葉にすることが重要になる。

本書はPythonの変数・条件分岐・ループ・リスト・辞書・関数を一通り知っている読者を想定する。再帰、型ヒント、タプル、キャッシュなどは使用する場所で説明する。型ヒントは読み手と開発支援ツールのための情報であり、それだけで実行時の入力検査が行われるわけではない。

### 学習の依存関係

| 段階 | 講義 | ここで作る土台 | 再登場する題材 |
|---|---|---|---|
| 入力と候補を定める | 1〜2 | 計算量、不変条件、境界 | 測定値・数当て |
| 選択を積み重ねる | 3〜4 | 再帰、スタック、キュー | 組合せ・迷路 |
| 矛盾した枝を戻る | 5〜6 | 復元、制約、全解列挙 | 数独・麻雀 |
| 計算を共有する | 7〜8 | 状態の正規化、メモ化、DP | 麻雀・改善テーマ |
| 保証を保って優先する | 9〜10 | 距離・界・緩和 | 迷路・ナップサック |
| モデルと答えを評価する | 11〜12 | 統計的推定、順序制約 | 麻雀・活動計画 |

第3〜8回は順に読むことを推奨する。第9回は第4回のグラフ、第10回は第8回のナップサック、第11回は第6〜8回の状態設計を使う。第12回は全体の総合演習である。

### 90分授業と独学での使い方

各回は15節の共通形式を持つ。90分授業では復習5分、導入と原理15分、図と手計算15分、基本実装20分、実習20分、問題10分、振り返り5分を基本とする。本文を一字ずつ読み上げる構成ではない。長い完成コードは配布し、授業中は中心部分の実装と追跡へ時間を使う。特に第11回は厳密評価器の内部を事後課題に回せるよう、モデルの理解とサンプリングを授業の中心にする。

独学では、まずコードを隠して手計算を行い、次に完成コードの結果を予想してから実行し、最後に入力や条件を一つ変える。一回を90分で終える必要はない。第3・5・7・8回でつまずいたときは、先へ急ぐより「子から戻った直後の行」を声に出して追う方が効果的だ。

### 実行方法とファイル構成

実習ZIPを展開し、lessonファイルのあるフォルダで次を実行する。追加インストールは不要である。Windowsでpythonが見つからない場合は、環境に応じて`py -3`を使う。

```text
python lesson01_linear_search.py
python lesson05_sudoku.py
python -m unittest -v
python maze_comparison.py
python experiments.py
```

第7回以降には過去のlessonファイルをimportするものがある。すべてを同じフォルダに置けば実行できる。各回のコードは本書内に完全掲載しており、ZIPなしでも同名のファイルへ保存して再構成できる。プログラム出力は制作時の実行から自動挿入した。時間の実測値は環境依存なので本文の確定的な出力とは分ける。

### 学習記録の付け方

各回について「解いた問題」「状態」「終了条件」「保証」「検証例」の五つを自分の言葉で記録する。演習の基礎B・標準S・発展Aと理解度確認Qの全問に巻末解答を用意した。発展問題は授業後の課題にしてよい。

本書のコードは説明可能性を優先している。実務へ転用する場合は、入力規模、許される処理時間、例外処理、現実の制約をあらためて定める。教材内での正しさは、書かれた入力契約の下での正しさである。

## 全体目次

1. [第1回　探索とは何か――線形探索と計算量](#lesson01)
2. [第2回　二分探索――調べる範囲を半分にする](#lesson02)
3. [第3回　再帰関数――探索木を自動生成する](#lesson03)
4. [第4回　深さ優先探索と幅優先探索](#lesson04)
5. [第5回　バックトラック――失敗したら戻る](#lesson05)
6. [第6回　制約充足問題――麻雀の面子分解](#lesson06)
7. [第7回　メモ化探索――同じ問題を二度解かない](#lesson07)
8. [第8回　動的計画法――ナップサック問題](#lesson08)
9. [第9回　グラフ探索――最短経路を求める](#lesson09)
10. [第10回　貪欲法と分枝限定法――最適解を探す](#lesson10)
11. [第11回　確率的探索とモンテカルロ法](#lesson11)
12. [第12回　総合演習――人生の壺をアルゴリズムで解く](#lesson12)

[巻末解答](#answers) · [同じ迷路の比較](#maze-extra) · [実測記録](#benchmarks) · [手法の選択表](#selection) · [参考資料](#references)


<a id="lesson01"></a>

## 第1回　探索とは何か――線形探索と計算量

### 1. 講義タイトルと到達点

探索とは、候補の中から条件を満たすものを見つけることだ。本講義では、探索する前に「何を候補とし、何が分かれば終えてよいか」を言葉にする。最初の道具は線形探索である。地味な方法だが、後の高度な方法を検証する基準にもなる。

### 2. この回で学ぶこと

読み終えたら、存在判定・一つの解の取得・全解列挙・最適解探索の違いを説明できるようにしよう。また、要素数をNと置いて、最悪の場合に何回比較するかを数えられるようにする。「Pythonだから速い」「二重ループだから遅い」という印象ではなく、入力の大きさと作業回数を結びつける。

### 3. 前回までの復習に代わる準備

リストの添字は0から始まる。`return`は関数の呼び出し元へ値を返し、その関数の今回の実行を終了する。`None`は「結果がない」を表すために使える。ここでは見つからないときに-1を返さない。Pythonでは`values[-1]`が末尾を指すため、結果確認を忘れたときに誤った要素を取り出してしまうからだ。

### 4. 身近な問題からの導入

測定値が `[18, 25, 12, 25, 31]` と並んでいる。25という値が最初に現れる位置はどこか。人間なら左から見て、18は違う、次の25が一致した、と判断する。答えは添字1だ。

一方、25以上の測定値をすべて確認したいなら、添字1を発見して終えるわけにはいかない。後ろの25と31も必要である。同じデータと似た条件でも、求める出力が変われば終了条件が変わる。実務の要求文で「異常を検出する」と書くだけでは、最初の異常で警報を出すのか、全異常の記録を作るのかが決まらない。

### 5. アルゴリズムの原理

状態は「現在の添字と、そこまでに調べた結果」、候補は各要素、条件は値が目標と等しいこと、解は条件を満たす添字である。線形探索は各候補を順に評価する。最初の一致を返すなら、一致を確認した瞬間に終了してよい。そこまでの全要素が不一致だったので、それより前に解がないと分かっているからだ。

全探索は、有限な候補集合を漏れなく調べる方針を指す。線形探索はその最も単純な姿だが、候補は数値だけとは限らない。改善テーマ10件を採用するかどうかの組合せなら、候補は10個のビットからなる選択案になる。表の行を探すことと、まだ存在しない選択案を生成することの両方が探索である。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 210" role="img" aria-labelledby="fig01-title"><title id="fig01-title">図1　線形探索は左から比較する</title><rect width="720" height="210" fill="#fff"/><g font-family="sans-serif"><rect x="65" y="50" width="100" height="65" rx="9" fill="#f5f6f7" stroke="#147d86" stroke-width="1.5"/><text x="115.0" y="88.5" font-size="18" fill="#142c40" text-anchor="middle">18</text><text x="115" y="140" font-size="16" fill="#142c40" text-anchor="middle">添字 0</text><rect x="185" y="50" width="100" height="65" rx="9" fill="#e2f0ed" stroke="#147d86" stroke-width="1.5"/><text x="235.0" y="88.5" font-size="18" fill="#142c40" text-anchor="middle">25</text><text x="235" y="140" font-size="16" fill="#142c40" text-anchor="middle">添字 1</text><rect x="305" y="50" width="100" height="65" rx="9" fill="#f5f6f7" stroke="#147d86" stroke-width="1.5"/><text x="355.0" y="88.5" font-size="18" fill="#142c40" text-anchor="middle">12</text><text x="355" y="140" font-size="16" fill="#142c40" text-anchor="middle">添字 2</text><rect x="425" y="50" width="100" height="65" rx="9" fill="#f5f6f7" stroke="#147d86" stroke-width="1.5"/><text x="475.0" y="88.5" font-size="18" fill="#142c40" text-anchor="middle">25</text><text x="475" y="140" font-size="16" fill="#142c40" text-anchor="middle">添字 3</text><rect x="545" y="50" width="100" height="65" rx="9" fill="#f5f6f7" stroke="#147d86" stroke-width="1.5"/><text x="595.0" y="88.5" font-size="18" fill="#142c40" text-anchor="middle">31</text><text x="595" y="140" font-size="16" fill="#142c40" text-anchor="middle">添字 4</text><text x="360" y="185" font-size="21" fill="#142c40" text-anchor="middle">18 ≠ 25 → 25 = 25：添字1で終了</text></g></svg></div><figcaption>図1：線形探索の比較位置</figcaption></figure>

図は左から調べた範囲が増える様子を示す。最初の探索では添字1で終了する。全件取得では添字4まで進む。紙に同じ配列を書き、見終えた要素に線を引いてみよう。探索中に保たれる「ここより左には見落とした候補がない」という性質が、正しさの説明になる。

| 比較順 | 添字 | 値 | 25と等しいか | 次の動作 |
|---|---:|---:|---|---|
| 1 | 0 | 18 | いいえ | 次へ |
| 2 | 1 | 25 | はい | 1を返す |

### 7. Pythonによる基本実装

`enumerate`は添字と値を一緒に取り出す。以下は完成プログラムであり、末尾の`assert`も実行される。`assert 条件`は、条件が偽なら例外を発生させる簡単なテストである。通常実行で使い、`python -O`で無効にしないこと。

**完成プログラム：lesson01_linear_search.py**

```python
"""第1回: 最初の位置と、すべての候補。"""
def linear_search(values: list[int], target: int) -> int | None:
    for index, value in enumerate(values):
        if value == target:
            return index
    return None


def matching_indices(values: list[int], lower: int) -> list[int]:
    result = []
    for index, value in enumerate(values):
        if value >= lower:
            result.append(index)
    return result


if __name__ == '__main__':
    values = [18, 25, 12, 25, 31]
    assert linear_search([], 1) is None
    assert linear_search(values, 25) == 1
    assert linear_search(values, 99) is None
    assert matching_indices(values, 25) == [1, 3, 4]
    print('first:', linear_search(values, 25))
    print('all >= 25:', matching_indices(values, 25))
```

### 8. コードの実行過程

`linear_search(values, 25)`が呼ばれると、最初は`index=0, value=18`となる。ifの条件が偽なのでreturnへ入らず、forの次の反復へ進む。次は`index=1, value=25`で条件が真になり、`return index`が1を返す。残りの反復も、末尾の`return None`も実行されない。

空のリストではforの本体が一度も実行されず、末尾のreturnに達する。値が見つからなかった場合も同じ経路だ。こうして「空」「先頭にある」「途中にある」「ない」を一つの構造で扱える。

**実行結果**

```text
first: 1
all >= 25: [1, 3, 4]
```

### 9. 改良版アルゴリズム

`matching_indices`は一致するたびに添字を保存し、最後まで走査する。存在判定だけなら最初の一致で返す方が無駄がない。全件取得では、その早期終了が誤りになる。まず改善すべきなのはコードの短さではなく、要求に合った仕事だけをすることだ。

大量の検索を同じデータに繰り返すなら、辞書による索引やソートを検討できる。ただし、索引を作る時間とメモリが必要で、データの追加・変更にも対応しなければならない。1回だけの検索なら、準備せずに1回走査する方が合理的な場合がある。

### 10. 計算量と適用条件

最初の一致の探索は最良O(1)、最悪O(N)、補助領域O(1)である。全件取得は常にN要素を調べるので時間O(N)、出力がK件なら出力領域O(K)を使う。出力領域と、出力以外の作業領域は区別して記載する。

Big-Oは成長の上からの評価であり、厳密な秒数ではない。T(N)=3N+8ならO(N)と書く。Nが2倍になると主要な仕事もほぼ2倍になることを表す。厳密に同じ増加オーダーを述べたいときはΘ(N)を使う。O(N)には定数倍や小さな項が隠れており、小規模入力の実測でO(N²)がO(N log N)に勝っても矛盾ではない。

本書では整数比較や足し算を原則O(1)とみなす。ただし巨大整数や長い文字列では、その長さに応じた費用がある。何を一回の操作とみなしたかも計算量の一部である。

### 11. Python実習

測定値のリストを変更し、目標値が先頭・末尾・存在しない場合を実行する。次に関数内へ比較回数の変数を追加し、比較する直前に1増やす。N=10,100,1000で不在の値を探し、比較回数がNになることを確認しよう。時計による測定はまだ不要だ。Nに比例するという予測を、操作回数で検証する。

90分授業では、復習5分、要求の分解15分、手計算15分、実装20分、実習20分、問題10分、振り返り5分を目安とする。以降も同じ配分を基本とし、完成コードを写す時間より、値を変えて結果を予測する時間を優先する。

### 12. 練習問題

- **1-B 基礎**：`[4, 1, 4, 7]`から4を探すと何を返すか。7なら何回比較するか。
- **1-S 標準**：最後に一致する添字を返す関数の方針を二つ示し、それぞれの最悪計算量を述べよ。
- **1-A 発展**：N件から異なる2件を選ぶ全探索の候補数を求めよ。順序を区別する場合との違いも説明せよ。

### 13. 理解度確認問題

**1-Q1**：最初の一致の探索で、見つけた後も走査すると正しさはどうなるか。効率はどうなるか。**1-Q2**：O(N)の処理が、必ずO(N²)の処理より速いと言えるか。

### 14. まとめ

探索を始める前に、候補・条件・出力・終了条件を定める。線形探索は候補を一つずつ確認し、最悪でN回の比較が必要になる。単純な全探索は、後で作る高速な方法の答え合わせにも使える。

### 15. 次回への接続

もし測定値が小さい順に並んでいたら、真ん中の値を一つ見るだけで、多数の候補をまとめて捨てられる。第2回では、追加の前提条件が探索量をどう変えるかを見る。


<a id="lesson02"></a>

## 第2回　二分探索――調べる範囲を半分にする

### 1. 講義タイトルと到達点

二分探索を「真ん中を見る方法」で終わらせず、探索範囲を更新する理由まで説明する。今回の目標は、同じ値が複数ある場合や、目標値がない場合にも壊れない境界値探索を実装することだ。

### 2. この回で学ぶこと

半開区間、ループ不変条件、単調な判定条件、境界の更新を扱う。`lower_bound`は目標値以上の最初の位置を返す。その位置の値が目標と等しければ発見、等しくないか末尾なら不在と判断できる。探索と存在判定を分けると、応用範囲が広がる。

### 3. 前回までの復習

第1回では、未確認の各要素が解である可能性を捨てられなかった。だから一つずつ比較した。二分探索ではソート済みという条件を使う。前提条件が追加される代わりに、大きな範囲を一度に除外できる。

### 4. 身近な問題からの導入

0から100までの整数を一つ思い浮かべてもらう。「50以上か」と尋ね、はいなら50より下を、いいえなら50以上を除外する。これを繰り返せば、値を一つずつ尋ねるより少ない質問で特定できる。

ただし、相手が途中で数を変えるなら成立しない。データ探索でも同じで、探索中に並び順が変わったり、判定条件が偽→真→偽と揺れたりすれば、半分を捨てる根拠が消える。高速化の理由は、中央を見る動作自体ではなく、答えの配置に規則性があることだ。

### 5. アルゴリズムの原理

`predicate(i)`が、ある境界より前では偽、境界から後では真になるとする。境界は0からNまでのN+1通りで、全部偽ならNを返す。`left=0, right=N`から始める。

ループ中に保つ性質は、①`0 <= left <= right <= N`、②left未満はすべて偽、③right以上N未満はすべて真、の三つである。境界の候補は閉区間[left,right]に残るが、実際に調べる配列要素の区間は半開区間[left,right)である。この二つを混同しない。

中央が真なら境界は中央以前なので`right=middle`とする。中央が偽ならそこは答えではなく、境界はさらに右なので`left=middle+1`とする。`left=middle`ではない。要素が一つだけ残ったとき、middleはleftと同じになり、更新しても進まなくなるからだ。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 310" role="img" aria-labelledby="fig02-title"><title id="fig02-title">図2　二分探索で区間が縮む</title><rect width="720" height="310" fill="#fff"/><g font-family="sans-serif"><text x="85" y="60" font-size="20" fill="#142c40" text-anchor="middle">[0, 5)</text><rect x="160" y="35" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#a7b7bf" stroke-width="1.5"/><text x="200.0" y="63.0" font-size="18" fill="#142c40" text-anchor="middle">2</text><rect x="260" y="35" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#a7b7bf" stroke-width="1.5"/><text x="300.0" y="63.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="360" y="35" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#c76e36" stroke-width="1.5"/><text x="400.0" y="63.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="460" y="35" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#a7b7bf" stroke-width="1.5"/><text x="500.0" y="63.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><rect x="560" y="35" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#a7b7bf" stroke-width="1.5"/><text x="600.0" y="63.0" font-size="18" fill="#142c40" text-anchor="middle">9</text><text x="85" y="125" font-size="20" fill="#142c40" text-anchor="middle">[0, 2)</text><rect x="160" y="100" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#a7b7bf" stroke-width="1.5"/><text x="200.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">2</text><rect x="260" y="100" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#c76e36" stroke-width="1.5"/><text x="300.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="360" y="100" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="400.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="460" y="100" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="500.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><rect x="560" y="100" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="600.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">9</text><text x="85" y="190" font-size="20" fill="#142c40" text-anchor="middle">[0, 1)</text><rect x="160" y="165" width="80" height="44" rx="9" fill="#d9eeeb" stroke="#c76e36" stroke-width="1.5"/><text x="200.0" y="193.0" font-size="18" fill="#142c40" text-anchor="middle">2</text><rect x="260" y="165" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="300.0" y="193.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="360" y="165" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="400.0" y="193.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="460" y="165" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="500.0" y="193.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><rect x="560" y="165" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="600.0" y="193.0" font-size="18" fill="#142c40" text-anchor="middle">9</text><text x="85" y="255" font-size="20" fill="#142c40" text-anchor="middle">[1, 1)</text><rect x="160" y="230" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="200.0" y="258.0" font-size="18" fill="#142c40" text-anchor="middle">2</text><rect x="260" y="230" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="300.0" y="258.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="360" y="230" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="400.0" y="258.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="460" y="230" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="500.0" y="258.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><rect x="560" y="230" width="80" height="44" rx="9" fill="#f5f6f7" stroke="#a7b7bf" stroke-width="1.5"/><text x="600.0" y="258.0" font-size="18" fill="#142c40" text-anchor="middle">9</text><text x="360" y="300" font-size="17" fill="#142c40" text-anchor="middle">middleは橙色の枠／最後はleft=right=1</text></g></svg></div><figcaption>図2：二分探索の探索区間</figcaption></figure>

`[2,4,4,7,9]`で4以上の最初を探す。中央の4を見つけても終了しない。それより左にも4があるかもしれないからだ。

| 反復開始 | left | right | middle | 中央の値 | 更新 |
|---|---:|---:|---:|---:|---|
| 1 | 0 | 5 | 2 | 4 | right=2 |
| 2 | 0 | 2 | 1 | 4 | right=1 |
| 3 | 0 | 1 | 0 | 2 | left=1 |
| 終了 | 1 | 1 | — | — | 1を返す |

right=Nは配列の外だが、その位置を読むわけではない。ループ中はleft<rightなのでmiddle<right<=N、したがってmiddleは必ず有効な添字になる。

### 7. Pythonによる基本実装

`first_true`は判定関数を受け取る。`lambda index: values[index] >= target`は、indexを受け取って比較結果を返す短い関数である。慣れなければ同じ処理をdefで書いてよい。

**完成プログラム：lesson02_binary_search.py**

```python
"""第2回: 半開区間によるlower_bound。入力は昇順。"""
from collections.abc import Callable


def first_true(stop: int, predicate: Callable[[int], bool]) -> int:
    """[0, stop) の単調な偽→真の境界。真がなければstop。"""
    if stop < 0:
        raise ValueError('stop must be nonnegative')
    left, right = 0, stop
    while left < right:
        middle = (left + right) // 2
        if predicate(middle):
            right = middle
        else:
            left = middle + 1
    return left


def lower_bound(values: list[int], target: int) -> int:
    return first_true(len(values), lambda index: values[index] >= target)


if __name__ == '__main__':
    values = [2, 4, 4, 7, 9]
    assert lower_bound([], 3) == 0
    assert lower_bound(values, 4) == 1
    assert lower_bound(values, 10) == 5
    assert first_true(101, lambda number: number >= 73) == 73
    print('lower_bound(4):', lower_bound(values, 4))
    print('first x with x*x >= 30:', first_true(11, lambda x: x*x >= 30))
```

### 8. コードの実行過程

`lower_bound`は自分でwhileを持たず、判定条件を`first_true`に渡している。探索手順と「何を真とするか」を分離した設計だ。実行時にはwhileの各反復でpredicateが一度呼ばれ、TrueまたはFalseによって境界を更新する。

返された添字を読み出すときは、まず`index < len(values)`を確認する。その後に`values[index] == target`を確認すればよい。Pythonの`and`は左が偽なら右を評価しないので、この順序で範囲外アクセスを防げる。

**実行結果**

```text
lower_bound(4): 1
first x with x*x >= 30: 6
```

### 9. 改良版アルゴリズム

値そのものが並んだ配列がなくても、単調な判定が作れれば使える。例の`x*x >= 30`は非負整数xについて偽から真へ一度だけ変化する。答え6は、平方が30以上になる最小整数である。

製造業の条件探索でも「設定値を上げるほど必ず条件が満たされる」と証明・確認できるなら境界探索を考えられる。ただし実験値にノイズや非単調性がある場合、単に二分探索を適用しても保証はない。判定を繰り返す設計や統計モデルは別に必要だ。

### 10. 計算量と適用条件

区間長は各反復でおおむね半分になる。k回後の長さはN/2ᵏ程度なので、1以下にするにはkがlog₂N程度あればよい。時間O(log N)、補助領域O(1)である。N=0を含めて書くならO(log(N+1))と考える。

predicate一回がO(C)なら全体はO(C log N)であり、判定費用を忘れてはいけない。また、未整列データを一度検索するためだけにソートすると、一般的な比較ソートのO(N log N)が加わる。検索だけをO(log N)と称して全処理が速くなったと結論してはいけない。

正しさは不変条件の維持、終了はright-leftが必ず減ることで説明できる。終了時にはleft=rightで境界の候補が一つとなり、その値が答えである。

### 11. Python実習

N個の位置について、境界を0,1,…,Nのすべてに変えて`first_true`を試す。predicateを`i >= boundary`とすれば正解が既知になる。最後に空配列、全要素同じ配列、最大値より大きいtargetで試す。これは偶然の入力を数件試すより、境界の全位置を検査する強いテストになる。

### 12. 練習問題

- **2-B 基礎**：`[1,3,3,8]`に対しtarget=3とtarget=9の反復を手で追え。
- **2-S 標準**：targetを「超える」最初の位置を求めるにはpredicateをどう変えるか。二つの境界からtargetの個数を求めよ。
- **2-A 発展**：N=1、predicateが常に偽のとき、`left=middle`に変更したプログラムが停止しない理由を説明せよ。

### 13. 理解度確認問題

**2-Q1**：ソートされていない配列でも、たまたま正解することはあるか。それは適用条件を満たす証拠か。**2-Q2**：rightをNに初期化しても範囲外アクセスしない理由は何か。

### 14. まとめ

二分探索は、答えの場所に単調な構造があるとき、領域を安全に捨てる方法である。不変条件と必ず減る量をセットで考えれば、境界のバグを発見しやすくなる。

### 15. 次回への接続

候補が配列に並んでいない場合は、自分で候補を生成する必要がある。第3回では、選択の数に応じて深さが変わるループを、再帰関数で表現する。


<a id="lesson03"></a>

## 第3回　再帰関数――探索木を自動生成する

### 1. 講義タイトルと到達点

再帰は、関数が自分自身を呼び出す記述方法である。「同じところへ飛ぶ」だけではない。呼び出し元の仕事を途中で保留し、別の関数呼び出しを実行し、それが終わると保留した場所へ戻る。この往復を具体的に追うことが本講義の中心となる。

### 2. この回で学ぶこと

終了条件であるベースケース、呼び出しごとの変数を保つコールスタック、呼び出し前後の処理、返り値を使った成功・失敗の伝達を学ぶ。二進文字列の全列挙と、和を満たす部分集合の一解探索を対比する。再帰は探索そのものではなく、探索や分割統治などを実装する手段の一つである。

### 3. 前回までの復習

第2回ではright-leftが減ることから停止を説明した。再帰にも減少する量が必要だ。今回は「残りの文字数」や「未処理の要素数」が減る。単にifが書いてあるだけでは終了の保証にならない。すべての再帰経路がそのifへ近づくかを確認する。

### 4. 身近な問題からの導入

0と1からなる長さ2の文字列をすべて書くなら、最初に0を選び、その後に0と1を付ける。次に最初を1にして、同じ作業をする。結果は00,01,10,11だ。長さ3ならforを三重にすればよい。しかし実行時に長さが決まる場合、ソースコードに何重のforを書くかを事前には決められない。

人間の説明はもっと簡潔で、「一文字選んでから、残りについて同じことをする」で済む。この繰り返される説明を関数にしたものが再帰である。最初に完成品全体を考える代わりに、今の一段と残りの仕事を分ける。

### 5. アルゴリズムの原理

`path`を現在までに選んだ文字の列とする。長さが目標に達したら解として保存し、それ以上は進まない。達していなければ0を追加して残りを探索し、終わったら0を取り除く。次に1を追加して同様に探索する。

重要なのは、子の呼び出しが終わった後にも親の処理が残っていることだ。`visit()`から戻った親は、次の`path.pop()`を実行し、その後でforの次の候補へ進む。子がreturnしても親の関数全体が自動的に終了するわけではない。

`path`は内側の関数から共有される可変リストである。一方、各呼び出しのforが現在どの候補まで進んだかという実行状態は、呼び出しごとに保留される。共有されるものと、呼び出しごとに保持されるものを分けて考えると混乱が減る。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 315" role="img" aria-labelledby="fig03-title"><title id="fig03-title">図3　二進文字列の再帰木</title><rect width="720" height="315" fill="#fff"/><g font-family="sans-serif"><path d="M360,68 L190,135" stroke="#526574" stroke-width="2" fill="none" /><path d="M360,68 L530,135" stroke="#526574" stroke-width="2" fill="none" /><path d="M190,180 L100,240" stroke="#526574" stroke-width="2" fill="none" /><path d="M190,180 L280,240" stroke="#526574" stroke-width="2" fill="none" /><path d="M530,180 L440,240" stroke="#526574" stroke-width="2" fill="none" /><path d="M530,180 L620,240" stroke="#526574" stroke-width="2" fill="none" /><rect x="300" y="20" width="120" height="48" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="360.0" y="50.0" font-size="18" fill="#142c40" text-anchor="middle">空文字列</text><rect x="140" y="135" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="190.0" y="163.5" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="480" y="135" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="530.0" y="163.5" font-size="18" fill="#142c40" text-anchor="middle">1</text><rect x="50" y="240" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="100.0" y="268.5" font-size="18" fill="#142c40" text-anchor="middle">00</text><rect x="230" y="240" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="280.0" y="268.5" font-size="18" fill="#142c40" text-anchor="middle">01</text><rect x="390" y="240" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="440.0" y="268.5" font-size="18" fill="#142c40" text-anchor="middle">10</text><rect x="570" y="240" width="100" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="620.0" y="268.5" font-size="18" fill="#142c40" text-anchor="middle">11</text></g></svg></div><figcaption>図3：再帰の呼び出し木</figcaption></figure>

根は空文字列、辺は一文字の選択、葉は完成した文字列を示す。図を作るために全ノードを先にメモリへ保存する必要はない。再帰呼び出しは、その時点で必要な枝だけを進み、戻って次の枝を生成する。

| 時点 | 実行中の深さ | 処理 | path |
|---|---:|---|---|
| 1 | 0 | 0をappend | 0 |
| 2 | 1 | 0をappend | 00 |
| 3 | 2 | 解を保存してreturn | 00 |
| 4 | 1 | 子から戻りpop | 0 |
| 5 | 1 | 次の1をappend | 01 |
| 6 | 2 | 解を保存してreturn | 01 |
| 7 | 1 | pop、for終了、呼び出し元へ戻る | 0 |
| 8 | 0 | pop、次の1をappend | 1 |

深さ1の呼び出しが終わっても、深さ0のforはまだ途中である。表の8の後には10と11の探索が続く。returnは「今の呼び出しを終える」という意味であり、プログラム全体を終える命令ではない。

### 7. Pythonによる基本実装

前半は全列挙、後半は部分集合和の一解探索である。二つの関数で成功時の状態の扱いが違うことに注目する。

**完成プログラム：lesson03_recursion.py**

```python
"""第3回: 呼び出し前後を追う。"""
def binary_words(length: int) -> list[str]:
    if length < 0:
        raise ValueError('length must be nonnegative')
    answers: list[str] = []
    path: list[str] = []

    def visit() -> None:
        if len(path) == length:
            answers.append(''.join(path))
            return
        for digit in '01':
            path.append(digit)  # 選ぶ
            visit()             # その先をすべて調べる
            path.pop()          # 呼び出し元の状態へ戻す

    visit()
    return answers


def find_sum(values: list[int], target: int) -> list[int] | None:
    """部分集合の和。負数も許すため和の大きさでは枝刈りしない。"""
    path: list[int] = []
    def visit(index: int, total: int) -> bool:
        if index == len(values):
            return total == target
        path.append(values[index])
        if visit(index + 1, total + values[index]):
            return True  # 成功経路をpathに残すという契約
        path.pop()
        if visit(index + 1, total):
            return True
        return False
    return path.copy() if visit(0, 0) else None


if __name__ == '__main__':
    assert binary_words(0) == ['']
    assert len(binary_words(3)) == 8
    assert find_sum([2, 5], 3) is None
    assert find_sum([], 0) == []
    print('words:', binary_words(2))
    print('sum 7:', find_sum([2, 4, 5], 7))
```

### 8. コードの実行過程

`binary_words(2)`では、葉で`''.join(path)`が新しい文字列を作る。この文字列をanswersへ保存するので、その後pathを変更しても保存済みの解は変わらない。もし`answers.append(path)`と書けば、同じリストへの参照を保存してしまう。複数の解を記録する場面では、値のコピーか不変な表現が必要だ。

`find_sum([2,4,5],7)`は、まず2を採用し、4も採用し、5も採用する。合計11で葉へ到達しFalseを返す。呼び出し元は5をpopし、不採用の枝を調べるが合計6なのでこれも失敗する。さらに一段戻って4をpopし、4を不採用として5を選ぶと7になる。この葉はTrueを返す。

Trueは呼び出し元の`if visit(...):`を成立させ、その親が`return True`を実行する。その親の返り値もさらに上のifを成立させる。成功は一段ずつ伝播する。今回の契約では成功経路をpathに残したいので、この場合だけpopを飛ばす。常に復元する全列挙とは目的が異なる。

`visit`が値を返さなければ、暗黙にNoneを返す。Noneはifで偽として扱われる。そのため、葉で答えを見つけても親へ成功が伝わらず、成功経路を取り消してしまう。「途中まで動いて最後だけ壊れる」原因になるので、関数が何を返す契約なのかを最初に決めよう。

**実行結果**

```text
words: ['00', '01', '10', '11']
sum 7: [2, 5]
```

### 9. 改良版アルゴリズム

全解を保存せず、一つずつ処理すれば出力保存用のメモリを減らせる。発展的にはgeneratorとyieldで実現できるが、まずは葉で表示するだけでも違いを確認できる。ただし出力件数そのものは減らない。長さNの二進文字列は2ᴺ個あり、すべて書き出す要求には少なくともその件数分の仕事が必要だ。

部分集合和では「現在の和がtargetを超えたら終了」という枝刈りを思いつく。しかし残りに負数があれば、後から和が小さくなる可能性がある。本実装は負数を許すため、その枝刈りを入れていない。高速化するなら、入力条件と安全性の根拠を一緒に追加する。

### 10. 計算量と適用条件

二進文字列の木のノード数は1+2+…+2ᴺ=2ᴺ⁺¹−1。各葉で長さNの文字列を作るため、出力込みの時間はO(N2ᴺ)、出力領域もO(N2ᴺ)、探索中のpathとスタックはO(N)である。

部分集合和の実装は、最悪で二分木全体をたどりO(2ᴺ)時間、作業領域O(N)を使う。Pythonの再帰には深さの上限があり、大きなNで無制限に呼び出せるわけではない。上限を安易に増やす前に、明示的なスタックや別のアルゴリズムを考える。再帰で書くこと自体に高速化の保証はない。

### 11. Python実習

visitの入口と出口に、深さ分の空白とpathを表示する文を加える。N=2で上の表と照合し、N=3では紙に予測してから動かす。次に一時的にpopを削除して何が壊れるかを観察し、元へ戻す。最後に`find_sum`の葉のreturnをNoneへ変える実験を行い、失敗の理由を説明する。変更は実習用コピーで行うこと。

### 12. 練習問題

- **3-B 基礎**：`binary_words(0)`が`['']`を返す理由を説明せよ。`[]`との意味の違いは何か。
- **3-S 標準**：0,1,2からなる長さNの文字列を列挙するよう変更し、葉の数と計算量を求めよ。
- **3-A 発展**：`find_sum`を全解列挙へ変更する方針を示せ。値が重複する入力で「位置が違う選択」と「同じ値の組合せ」を区別せよ。

### 13. 理解度確認問題

**3-Q1**：子のreturnの後、親はどの行から再開するか。**3-Q2**：return Trueとprint(True)は同じか。**3-Q3**：再帰を使えば探索木全体を保存する必要があるか。

### 14. まとめ

再帰は、現在の仕事を保留して小さな同型の仕事を呼ぶ仕組みである。入口・終了条件・呼び出し・呼び出し後の処理を分けて追おう。成功を返すのか、全解を保存するのかによって、復元とreturnの置き方が決まる。

### 15. 次回への接続

同じ探索木でも、奥へ進む順序と、近いところを先に見る順序がある。第4回では再帰が自然に作る深さ優先探索と、キューを使う幅優先探索を比べる。


<a id="lesson04"></a>

## 第4回　深さ優先探索と幅優先探索

### 1. 講義タイトルと到達点

迷路を題材に、探索する順序を変えるだけで得られる保証が変わることを学ぶ。DFSで到達可能性を調べ、BFSで最短手数の経路を復元する。どちらも万能な最短経路法ではない。

### 2. この回で学ぶこと

深さ優先探索（DFS）、幅優先探索（BFS）、スタック、キュー、訪問済み集合、親ポインタを扱う。迷路の一つの通路マスを頂点、上下左右の移動を辺とみなす。こうした対象の表現方法をモデル化と呼ぶ。

### 3. 前回までの復習

二進文字列の再帰は、0で始まる枝の葉まで進んでから1の枝へ移った。これは深さ優先の順序である。ただし文字列の木と迷路には違いがある。迷路では右へ行って左へ戻ると同じマスになる。訪問済み管理がなければ、再帰は同じ場所を何度も往復してしまう。

### 4. 身近な問題からの導入

建物の出口を探す場面を考えよう。分岐で一つを選び、行き止まりまで進んで戻る方法は自然だ。しかし出口が入口の別の分岐のすぐ近くにあっても、最初に長い通路を調べてしまうことがある。

最短の移動回数が欲しいなら、入口から1歩の場所を全部調べ、次に2歩の場所を全部調べる方がよい。BFSはこの「距離の層」を順に広げる。DFSは探索の深さを優先し、BFSは到達までの辺数を優先する。

### 5. アルゴリズムの原理

DFSは頂点に到達したら訪問済みにし、未訪問の隣接頂点へ再帰する。処理を保留した呼び出しがスタックに積まれるため、最後に入った仕事から処理される。再帰を使わず、リストをスタックとしても実装できる。

BFSは開始点をキューへ入れ、先頭から取り出した頂点の未発見の隣接頂点を末尾へ入れる。キューは先入れ先出しである。開始点を距離0とすれば、距離dの頂点から新しく発見する頂点の距離はd+1になる。距離dの頂点がキューの前方にあるため、d+1より先にd+2が処理されることはない。

訪問済みの登録は、キューから出した時点でなく、入れる時点で行う。二つの頂点から同じ頂点へ辺がある場合、登録を遅らせると同じ頂点を何度もキューへ入れてしまう。親を記録する辞書を発見済み集合の代わりにも使えば、管理を一元化できる。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 310" role="img" aria-labelledby="fig04-title"><title id="fig04-title">図4　DFSとBFSの訪問順</title><rect width="720" height="310" fill="#fff"/><g font-family="sans-serif"><path d="M360,45 L210,125" stroke="#526574" stroke-width="2" fill="none" /><path d="M360,45 L510,125" stroke="#526574" stroke-width="2" fill="none" /><path d="M210,125 L110,205" stroke="#526574" stroke-width="2" fill="none" /><path d="M210,125 L300,205" stroke="#526574" stroke-width="2" fill="none" /><path d="M510,125 L550,205" stroke="#526574" stroke-width="2" fill="none" /><rect x="325" y="25" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="360.0" y="51.0" font-size="18" fill="#142c40" text-anchor="middle">S</text><rect x="175" y="105" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="210.0" y="131.0" font-size="18" fill="#142c40" text-anchor="middle">A</text><rect x="475" y="105" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="510.0" y="131.0" font-size="18" fill="#142c40" text-anchor="middle">B</text><rect x="75" y="185" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="110.0" y="211.0" font-size="18" fill="#142c40" text-anchor="middle">C</text><rect x="265" y="185" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="300.0" y="211.0" font-size="18" fill="#142c40" text-anchor="middle">D</text><rect x="515" y="185" width="70" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="550.0" y="211.0" font-size="18" fill="#142c40" text-anchor="middle">E</text><text x="360" y="270" font-size="20" fill="#142c40" text-anchor="middle">DFS：S, A, C, D, B, E</text><text x="360" y="300" font-size="20" fill="#142c40" text-anchor="middle">BFS：S, A, B, C, D, E</text></g></svg></div><figcaption>図4：DFSとBFSの順序</figcaption></figure>

図の分岐例ではDFSは一方の枝を深くたどり、BFSは同じ深さの頂点を先に扱う。完成プログラムの迷路では、右・下・左・上の順に隣接マスを登録する。同じ最短距離の経路が複数あれば、この順序がどの経路を返すかに影響する。

| 操作 | キューの内容（左が次） | 新しい親の記録 |
|---|---|---|
| 初期化 | S | parent[S]=None |
| Sを展開 | A, B | A←S, B←S |
| Aを展開 | B, C, D | C←A, D←A |
| Bを展開 | C, D, E | E←B |

この表は順序の仕組みを見るための小さなグラフ例であり、座標付き迷路の出力とは別である。

### 7. Pythonによる基本実装

`#`を壁、それ以外を通路とする。座標をタプルにすると辞書のキーにできる。`deque.popleft()`は先頭から効率よく取り出す操作である。リストの`pop(0)`では後続要素の移動が発生する。

**完成プログラム：lesson04_dfs_bfs.py**

```python
"""第4回: 無重みの迷路。座標は(row, column)。"""
from collections import deque
Cell = tuple[int, int]


def maze_graph(rows: list[str]) -> dict[Cell, list[Cell]]:
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('rectangular nonempty maze required')
    graph: dict[Cell, list[Cell]] = {}
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char == '#':
                continue
            graph[r, c] = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(rows) and 0 <= nc < len(row) and rows[nr][nc] != '#':
                    graph[r, c].append((nr, nc))
    return graph


def dfs(graph: dict, start: Cell) -> list[Cell]:
    if start not in graph:
        raise ValueError('unknown start')
    seen: set[Cell] = set()
    order: list[Cell] = []
    def visit(cell: Cell) -> None:
        seen.add(cell)
        order.append(cell)
        for neighbor in graph[cell]:
            if neighbor not in seen:
                visit(neighbor)
    visit(start)
    return order


def bfs_path(graph: dict, start: Cell, goal: Cell) -> list[Cell] | None:
    if start not in graph or goal not in graph:
        raise ValueError('unknown endpoint')
    queue = deque([start])
    parent = {start: None}  # 発見と同時に登録する
    while queue:
        cell = queue.popleft()
        if cell == goal:
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return path[::-1]
        for neighbor in graph[cell]:
            if neighbor not in parent:
                parent[neighbor] = cell
                queue.append(neighbor)
    return None


MAZE = ['...#.', '.#...', '...#.']
if __name__ == '__main__':
    graph = maze_graph(MAZE)
    path = bfs_path(graph, (0, 0), (2, 4))
    assert path is not None and len(path) - 1 == 6
    assert bfs_path(graph, (0, 0), (0, 0)) == [(0, 0)]
    assert len(dfs(graph, (0, 0))) == len(graph)
    print('DFS:', dfs(graph, (0, 0)))
    print('BFS path:', path)
    print('steps:', len(path) - 1)
```

### 8. コードの実行過程

DFSでは`seen.add(cell)`を再帰より前に行う。隣から同じ場所へ戻る辺があっても、すでにseenにあるため再帰しない。visitが終わると、その頂点を呼んだ親のforへ戻り、まだ調べていない隣接頂点へ進む。

BFSでは、ゴールを取り出したらparentを逆向きにたどる。ゴールから一つ前、その一つ前、とたどると最後に開始点へ着く。作られたリストは逆順なので`[::-1]`で反転する。開始点とゴールが同じ場合にも、要素一つの経路が返り、移動回数は0になる。

**実行結果**

```text
DFS: [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (0, 4), (2, 2), (2, 1), (2, 0), (1, 0)]
BFS path: [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4)]
steps: 6
```

### 9. 改良版アルゴリズム

大きな迷路では、再帰版DFSが深さ制限に達する可能性がある。明示的なスタックに未処理頂点を積む反復版へ変更すれば、Pythonの関数呼び出し深さから独立できる。ただし、同じ訪問順序を再現したいなら、隣接頂点を積む順序と訪問済みにする時点を慎重に決める必要がある。

経路を求めず距離だけが必要なら、BFSで距離辞書を持てばよい。全頂点への距離が必要ならゴール発見時に終了せず、キューが空になるまで続ける。要求する出力に合わせて、保存する情報と終了条件を変える。

### 10. 計算量と適用条件

隣接リストを用いれば、DFSもBFSも各頂点と各辺を定数回確認し、時間O(V+E)、補助領域O(V)である。迷路を隣接リストへ変換する費用と保存領域もO(V+E)かかる。

BFSは辺の本数が最小の経路を保証する。全辺の費用が同一の非負定数なら、費用最小とも一致する。坂道・料金・移動時間などの重みが異なる場合、辺数が少ない経路が最安とは限らない。DFSが返す到達順も、最短距離を表さない。

### 11. Python実習

完成プログラムの迷路を紙に描き、BFS経路をなぞる。次に壁を一つ追加してゴールへ到達できなくし、Noneが返ることを確認する。別の実験として、通路の各辺に異なる移動時間を手で付け、最短手数と最短時間が違う例を作る。この段階では重み付きの正しいプログラムはまだ書かなくてよい。

### 12. 練習問題

- **4-B 基礎**：開始点と終点が同じ場合、経路の要素数と移動回数はいくつか。
- **4-S 標準**：三角形のグラフで訪問済みを使わない再帰DFSが止まらない理由を説明せよ。
- **4-A 発展**：S→Gの費用10、S→Aの費用1、A→Gの費用1というグラフで、BFSの答えと最小費用を比べよ。

### 13. 理解度確認問題

**4-Q1**：BFSのキューをスタックへ置き換えても、最短手数の保証は残るか。**4-Q2**：到達不能なゴールに対して空リストとNoneのどちらを返す契約にしたか。

### 14. まとめ

探索順序は、次に処理する候補の保管方法で決まる。DFSはスタック、BFSはキューを使う。循環のあるグラフでは訪問済み管理が必要で、BFSの最短性は辺数または一様な費用に対する保証である。

### 15. 次回への接続

迷路では固定されたマスを訪れた。数独では、自分で数字を置くたびに状態そのものが変わる。第5回は、変えた状態を戻すバックトラックへ進む。


<a id="lesson05"></a>

## 第5回　バックトラック――失敗したら戻る

### 1. 講義タイトルと到達点

数独の空欄に数字を仮置きし、矛盾したら取り消すソルバーを作る。完成した数字だけを見るのではなく、失敗がどの呼び出しへ戻り、どのマスが空欄に戻るかを理解する。

### 2. この回で学ぶこと

制約による枝刈り、状態の復元、最少候補優先（MRV）、成功を伝えるboolを扱う。単純版とMRV版を同じコードのスイッチで比較し、答えを変えずに探索順序だけを変更する効果を確かめる。

### 3. 前回までの復習

DFSは探索順序を表す。バックトラックは、部分解を伸ばし、続けられなければ取り消して別の選択を試す方法である。バックトラックはDFSで実装されることが多いが同義ではない。固定グラフを巡回するDFSには、仮置きした数字を復元する仕事はなかった。

### 4. 身近な問題からの導入

数独では、各行・各列・各3×3ブロックに1〜9を一度ずつ置く。人間なら、空欄の行・列・ブロックを見て置けない数を除外する。すぐには決まらなければ候補の一つを仮定して進む。途中でどの数字も入らないマスができれば、その仮定の下では完成できない。

空欄がE個あると、制約を無視して9種類を全部入れる候補は9ᴱ通りになる。完成してから矛盾を調べるのは無駄が多い。部分的な盤面の段階で既に破っている制約は、先へ進んでも直らない。この枝を早めに捨てるのが枝刈りである。

### 5. アルゴリズムの原理

searchは、現在の盤面を完成できるならTrue、できなければFalseを返す。空欄を一つ選び、そのマスで許される数を列挙する。候補を一つ置いてsearchを呼ぶ。子がTrueなら完成盤面を保ったままTrueを返す。Falseならその数を0へ戻し、次の候補を試す。

空欄が一つもなければTrueを返す。これが安全なのは、初期配置を検証し、その後も許される数だけを置くからだ。もし初期の重複を調べなければ、数字で埋まった不正盤面を「空欄なしだから成功」としてしまう。

MRVは、候補が最も少ない空欄を次に選ぶ。選択肢の少ない制約を早く確定させ、矛盾があるなら浅い段階で見つける狙いがある。候補0のマスを選べば、forが一度も実行されず即座にFalseとなる。MRVは探索順序の工夫であり、どれかの候補を勝手に除外する方法ではない。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" role="img" aria-labelledby="fig13-title"><title id="fig13-title">図5a　数独の初期盤面と中央マスの候補</title><rect width="720" height="380" fill="#fff"/><g font-family="sans-serif"><text x="44" y="51" font-size="20" fill="#142c40" text-anchor="middle">5</text><text x="76" y="51" font-size="20" fill="#142c40" text-anchor="middle">3</text><text x="172" y="51" font-size="20" fill="#142c40" text-anchor="middle">7</text><text x="44" y="83" font-size="20" fill="#142c40" text-anchor="middle">6</text><text x="140" y="83" font-size="20" fill="#142c40" text-anchor="middle">1</text><text x="172" y="83" font-size="20" fill="#142c40" text-anchor="middle">9</text><text x="204" y="83" font-size="20" fill="#142c40" text-anchor="middle">5</text><text x="76" y="115" font-size="20" fill="#142c40" text-anchor="middle">9</text><text x="108" y="115" font-size="20" fill="#142c40" text-anchor="middle">8</text><text x="268" y="115" font-size="20" fill="#142c40" text-anchor="middle">6</text><text x="44" y="147" font-size="20" fill="#142c40" text-anchor="middle">8</text><text x="172" y="147" font-size="20" fill="#142c40" text-anchor="middle">6</text><text x="300" y="147" font-size="20" fill="#142c40" text-anchor="middle">3</text><text x="44" y="179" font-size="20" fill="#142c40" text-anchor="middle">4</text><text x="140" y="179" font-size="20" fill="#142c40" text-anchor="middle">8</text><rect x="156" y="156" width="32" height="32" fill="#d0eee6"/><text x="172" y="179" font-size="20" fill="#147d86" text-anchor="middle">?</text><text x="204" y="179" font-size="20" fill="#142c40" text-anchor="middle">3</text><text x="300" y="179" font-size="20" fill="#142c40" text-anchor="middle">1</text><text x="44" y="211" font-size="20" fill="#142c40" text-anchor="middle">7</text><text x="172" y="211" font-size="20" fill="#142c40" text-anchor="middle">2</text><text x="300" y="211" font-size="20" fill="#142c40" text-anchor="middle">6</text><text x="76" y="243" font-size="20" fill="#142c40" text-anchor="middle">6</text><text x="236" y="243" font-size="20" fill="#142c40" text-anchor="middle">2</text><text x="268" y="243" font-size="20" fill="#142c40" text-anchor="middle">8</text><text x="140" y="275" font-size="20" fill="#142c40" text-anchor="middle">4</text><text x="172" y="275" font-size="20" fill="#142c40" text-anchor="middle">1</text><text x="204" y="275" font-size="20" fill="#142c40" text-anchor="middle">9</text><text x="300" y="275" font-size="20" fill="#142c40" text-anchor="middle">5</text><text x="172" y="307" font-size="20" fill="#142c40" text-anchor="middle">8</text><text x="268" y="307" font-size="20" fill="#142c40" text-anchor="middle">7</text><text x="300" y="307" font-size="20" fill="#142c40" text-anchor="middle">9</text><path d="M28,28 V316 M28,28 H316" stroke="#244453" stroke-width="2" fill="none"/><path d="M60,28 V316 M28,60 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M92,28 V316 M28,92 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M124,28 V316 M28,124 H316" stroke="#244453" stroke-width="2" fill="none"/><path d="M156,28 V316 M28,156 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M188,28 V316 M28,188 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M220,28 V316 M28,220 H316" stroke="#244453" stroke-width="2" fill="none"/><path d="M252,28 V316 M28,252 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M284,28 V316 M28,284 H316" stroke="#244453" stroke-width="0.6" fill="none"/><path d="M316,28 V316 M28,316 H316" stroke="#244453" stroke-width="2" fill="none"/><text x="350" y="65" font-size="17" fill="#142c40" text-anchor="start">中央マス (row=4, col=4)</text><text x="350" y="110" font-size="17" fill="#142c40" text-anchor="start">行の候補：2, 5, 6, 7, 9</text><text x="350" y="150" font-size="17" fill="#142c40" text-anchor="start">列の候補：3, 4, 5</text><text x="350" y="190" font-size="17" fill="#142c40" text-anchor="start">区画の候補：1, 4, 5, 7, 9</text><text x="350" y="245" font-size="17" fill="#142c40" text-anchor="start">共通候補は 5 のみ</text><text x="350" y="285" font-size="17" fill="#142c40" text-anchor="start">MRVはこのマスから進む</text><text x="360" y="355" font-size="19" fill="#142c40" text-anchor="middle">空欄は未定。行・列・区画の三つの制約を同時に満たす。</text></g></svg></div><figcaption>図5a：実際の数独盤面とMRVの最初の選択</figcaption></figure>

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 330" role="img" aria-labelledby="fig05-title"><title id="fig05-title">図5　仮置きと取り消し</title><rect width="720" height="330" fill="#fff"/><g font-family="sans-serif"><rect x="250" y="20" width="220" height="45" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="360.0" y="48.5" font-size="18" fill="#142c40" text-anchor="middle">X：候補 2, 7</text><path d="M320,65 L170,120" stroke="#526574" stroke-width="2" fill="none" /><path d="M400,65 L550,120" stroke="#526574" stroke-width="2" fill="none" /><rect x="70" y="120" width="200" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="170.0" y="151.0" font-size="18" fill="#142c40" text-anchor="middle">X = 2</text><rect x="450" y="120" width="200" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="550.0" y="151.0" font-size="18" fill="#142c40" text-anchor="middle">X = 7</text><path d="M170,170 L170,220" stroke="#526574" stroke-width="2" fill="none" /><rect x="55" y="220" width="230" height="50" rx="9" fill="#fff0e7" stroke="#c76e36" stroke-width="1.5"/><text x="170.0" y="251.0" font-size="18" fill="#142c40" text-anchor="middle">Y：候補なし → False</text><path d="M550,170 L550,220" stroke="#526574" stroke-width="2" fill="none" /><rect x="450" y="220" width="200" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="550.0" y="251.0" font-size="18" fill="#142c40" text-anchor="middle">次のマスへ</text><text x="360" y="310" font-size="19" fill="#142c40" text-anchor="middle">Falseで親へ戻る → Xを0に復元 → 次の候補7</text></g></svg></div><figcaption>図5：バックトラックの復元</figcaption></figure>

上の盤面では中央マスの候補が5に絞られる。下のXとYの図は復元の仕組みを示す別の概念例であり、この初期盤面の具体的な枝を表したものではない。

一つの呼び出しが選んだマスをX、その次の呼び出しのマスをYとしよう。X=2の下でYの全候補が失敗したなら、Yを選んだ呼び出しはFalseを返す。親はXを0に戻してXの次の候補を試す。Y以降のマスは、各子が戻るまでに自分で取り消している。

| 実行位置 | 盤面の変更 | 意味 |
|---|---|---|
| 親のfor | Xに2を代入 | 仮定を作る |
| 子のsearch | Y以降を探索 | 仮定の帰結を調べる |
| 子がFalseを返す | 子の仮置きは復元済み | X=2では完成不能 |
| 親の次の行 | Xを0へ戻す | 呼び出し前の部分解に戻す |
| 親のforの次 | Xに次の候補 | 別の枝を調べる |

この復元責任を「自分が変更したものは、失敗して戻る前に自分で戻す」と決めると、深い再帰でも局所的に考えられる。

### 7. Pythonによる基本実装

入力盤面はコピーし、呼び出し側のリストを変更しない。戻り値は解と統計の組で、解なしなら先頭はNoneである。複数解がある場合も一つだけ返し、一意性の証明は行わない。

**完成プログラム：lesson05_sudoku.py**

```python
"""第5回: 一解を返す。入力を変更せず、解なしはNone。"""
Board = list[list[int]]


def candidates(board: Board, row: int, column: int) -> list[int]:
    used = set(board[row])
    used.update(board[r][column] for r in range(9))
    br, bc = row // 3 * 3, column // 3 * 3
    used.update(board[r][c] for r in range(br, br+3) for c in range(bc, bc+3))
    return [n for n in range(1, 10) if n not in used]


def validate(board: Board) -> None:
    if len(board) != 9 or any(len(row) != 9 for row in board):
        raise ValueError('9 x 9 required')
    if any(type(n) is not int or not 0 <= n <= 9 for row in board for n in row):
        raise ValueError('integer 0..9 required')
    for r in range(9):
        for c in range(9):
            n = board[r][c]
            if n:
                copied = [row.copy() for row in board]
                copied[r][c] = 0
                if n not in candidates(copied, r, c):
                    raise ValueError('conflicting givens')


def solve(puzzle: Board, use_mrv: bool = True) -> tuple[Board | None, dict[str, int]]:
    validate(puzzle)
    board = [row.copy() for row in puzzle]
    stats = {'calls': 0, 'undo': 0}
    def search() -> bool:
        stats['calls'] += 1
        chosen = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    options = candidates(board, r, c)
                    if chosen is None or len(options) < len(chosen[2]):
                        chosen = (r, c, options)
                    if not use_mrv:
                        break
            if chosen is not None and not use_mrv:
                break
        if chosen is None:
            return True
        r, c, options = chosen
        for n in options:
            board[r][c] = n
            if search():
                return True
            board[r][c] = 0
            stats['undo'] += 1
        return False
    success = search()
    return (board if success else None), stats


PUZZLE = [[int(n) for n in row] for row in [
    '530070000', '600195000', '098000060',
    '800060003', '400803001', '700020006',
    '060000280', '000419005', '000080079']]
if __name__ == '__main__':
    for use_mrv in (False, True):
        solution, stats = solve(PUZZLE, use_mrv)
        assert solution is not None
        validate(solution)
        assert all(0 not in row for row in solution)
        print('MRV:', use_mrv, 'stats:', stats)
    for row in solution:
        print(''.join(map(str, row)))
```

### 8. コードの実行過程

`chosen`は `(行,列,候補リスト)` を保持する。単純版は最初の空欄を見つけた時点で二重ループから抜ける。MRV版は全空欄を見て最小候補数を探す。候補数が同じなら先に見つかったマスを保持し、数字は小さい順に試すので実行は決定的になる。

盤面へ数字を入れた後の`if search():`は、今の数字だけが正しいかを調べるifではない。「この数字を置いた先のすべての空欄を埋められたか」を受け取るifだ。Falseが返ったとき、直後の`board[r][c]=0`が実行される。この行を削ると、次の探索が前の枝の数字を含んだ盤面から始まり、探索漏れを起こす。

標準問題では単純版は4209回呼ばれ、4157回の取り消しを行った。MRV版は52回で、取り消しは0回だった。空欄51個を一つずつ埋め、完成を判定する最後の呼び出しを含めて52回である。この問題ではMRVが非常に効いたが、どんな数独でも取り消しが不要になるという意味ではない。テストに収録した別の盤面では、MRV版でも218回の呼び出しと159回の取り消しが必要だった。

**実行結果**

```text
MRV: False stats: {'calls': 4209, 'undo': 4157}
MRV: True stats: {'calls': 52, 'undo': 0}
534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
```

### 9. 改良版アルゴリズム

各行・列・ブロックに使われた数字を集合として保持すれば、候補を求めるたびに盤面を読み直す仕事を減らせる。ただし、仮置き時の追加と取り消し時の削除を三つの集合で正しくそろえる必要がある。高速化によって管理する状態が増えるので、まず単純版を正解基準として残すとよい。

全解を数える場合には成功でreturnせず、完成盤面をコピーして保存した後も探索を続ける。この場合、成功した枝でも必ず盤面を復元する。一意性だけ知りたければ2解見つけた時点で停止できるが、1解しか見つからない場合は残りの探索も必要になる。

### 10. 計算量と適用条件

空欄E個の候補割当ての最悪上界はO(9ᴱ)で、MRVも最悪の指数性を消さない。9×9固定盤面では一状態の候補計算を定数としてこのように表す。一般化した盤面ではマス選択・候補計算の費用も乗じる必要がある。

探索の深さはE以下、スタック領域はO(E)である。盤面は固定サイズだが、呼び出しごとの候補リストも保持される。MRVは一状態で全空欄を比較するため、ノード数が少なくても必ずしも同じ比率で実時間が短くなるとは限らない。

### 11. Python実習

まず完成出力を検証し、与えられた数字が保存されていることを確認する。次に`use_mrv`を切り替え、callsとundoを比較する。0だらけの盤面に変える実験では一解だけ見つけても「数独問題として一意」とは言えないことに注意する。

MRVでも巻き戻しが起きる盤面は、行を文字列で表すと`100007090 / 030020008 / 009600500 / 005300900 / 010080002 / 600004000 / 300000010 / 040000007 / 007000300`である。0が空欄を表す。`test_05_mrv_backtracks`に同じ入力を収録している。候補の順序を変えると呼び出し回数も変わることを確かめよう。

最後に、最初の行を`0,1,2,3,4,5,6,7,8`、2行目の先頭を9、それ以外を0にする。この盤面は与え数字の直接重複はないが、左上には何も置けない。入力不正と、合法な部分配置だが完成不能であることを区別してテストしよう。

### 12. 練習問題

- **5-B 基礎**：空欄なし、候補なし、候補が一つ、の各場合にsearchはどう動くか。
- **5-S 標準**：全解列挙へ変えるなら、Trueを返す行と復元処理をどう変更するか。
- **5-A 発展**：初期盤面を変更しないという契約をテストするには、実行前後の何を比較するか。浅いコピーだけでは不十分な理由も述べよ。

### 13. 理解度確認問題

**5-Q1**：MRVは最適解を近似しているか。**5-Q2**：子が失敗したとき、親が全盤面を初期状態へ戻す必要はあるか。**5-Q3**：空欄数が少ない数独は必ず計算時間が短いか。

### 14. まとめ

バックトラックの正しさには、候補の網羅と状態の復元の両方が必要である。MRVは解集合を変えずに調べる順番を変える。呼び出し回数と実行時間は、異なる尺度として観察しよう。

### 15. 次回への接続

数独では空欄を埋めた。麻雀では、手牌から使える面子を取り除いて残りを調べる。増やす探索と減らす探索は、再帰の同じ骨格で書ける。


<a id="lesson06"></a>

## 第6回　制約充足問題――麻雀の面子分解

### 1. 講義タイトルと到達点

14枚の手牌を4面子1雀頭へ分解できるかを判定する。さらに、複数の異なる分解をすべて列挙する。「和了できるか」と「どのように分けられるか」を区別し、後の点数計算へつながるデータを作る。

### 2. この回で学ぶこと

制約充足問題（CSP）は、変数に値を割り当て、制約を同時に満たす解を求める枠組みである。麻雀の面子選択も、牌の総数を守りながら、許された組を割り当てる問題として表現できる。ここでは34種類の枚数表現、最小の残り牌を基準にした分岐、復元、正規化による重複排除を学ぶ。

### 3. 前回までの復習

数独では一つのマスの値を変更し、失敗時に0へ戻した。今回は複数種類の枚数を減らし、探索後に同じ枚数を足す。一つの操作が複数要素にまたがるため、何を変更したかを面子のタプルとして保存し、そのまま復元に使う。

### 4. 身近な問題からの導入

同じ色の`11122233344455`は、`111 / 222 / 333 / 444 / 55`と分けられる。一方で`123 / 123 / 123 / 444 / 55`も可能だ。「111があるから刻子にする」と一つに決め打ちすると、別の分解を見落とす。

麻雀の基本用語を確認する。刻子は同じ牌3枚、順子は同じ色で連続する数牌3枚、雀頭は同じ牌2枚である。字牌には順子がない。数牌の8,9,次の色の1を順子にしてはいけない。ここでは副露・槓なし、34種類各4枚まで、門前14枚の形だけを扱い、役・フリテン・点数・実戦での和了可否は扱わない。

### 5. アルゴリズムの原理

最初に雀頭の種類を選び、その2枚を除く。残り12枚が面子だけに分かれるかを調べる。残っている最小の牌番号iに注目すると、その牌を含む面子は、iの刻子か、iから始まる順子に限られる。

なぜiを順子の中央や末尾として使う必要がないのか。iより小さい牌はもう残っていないからである。完成分解の中でiが中央ならi−1、末尾ならi−2が必要だが、それは存在しない。したがって二種類の分岐を調べれば漏れがない。これは単なる経験則ではなく、探索候補を削減できる証明だ。

空になったら成功である。最初に14枚から雀頭2枚を取り、面子ごとに3枚減らすため、空になった時点で面子は必ず4個となる。`sum(counts)==14`の入力検査を省くと、この保証も失われる。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 320" role="img" aria-labelledby="fig06-title"><title id="fig06-title">図6　麻雀の面子分解：雀頭55を除いた枝</title><rect width="720" height="320" fill="#fff"/><g font-family="sans-serif"><rect x="200" y="20" width="320" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="360.0" y="51.0" font-size="18" fill="#142c40" text-anchor="middle">111222333444</text><path d="M290,70 L175,130" stroke="#526574" stroke-width="2" fill="none" /><path d="M430,70 L545,130" stroke="#526574" stroke-width="2" fill="none" /><rect x="45" y="130" width="260" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="175.0" y="161.0" font-size="18" fill="#142c40" text-anchor="middle">111を除く：222333444</text><rect x="415" y="130" width="260" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="545.0" y="161.0" font-size="18" fill="#142c40" text-anchor="middle">123を除く：112233444</text><path d="M175,180 L175,240" stroke="#526574" stroke-width="2" fill="none" /><path d="M545,180 L545,240" stroke="#526574" stroke-width="2" fill="none" /><rect x="35" y="240" width="280" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="175.0" y="271.0" font-size="18" fill="#142c40" text-anchor="middle">222 / 333 / 444</text><rect x="405" y="240" width="280" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="545.0" y="271.0" font-size="18" fill="#142c40" text-anchor="middle">123 / 123 / 444</text></g></svg></div><figcaption>図6：麻雀の分解枝</figcaption></figure>

図は雀頭55を外した後の一部分を示す。最小牌1に対して111を取る枝と123を取る枝がある。刻子を先に取るコード順でも、順子の枝を後で試すため、分解は漏れない。

| 牌種 | 番号 |
|---|---|
| 萬子1〜9 | 0〜8 |
| 筒子1〜9 | 9〜17 |
| 索子1〜9 | 18〜26 |
| 東・南・西・北・白・發・中 | 27〜33 |

たとえば1萬は番号0であり、表示される`(0,1,2)`は123萬を意味する。入力表記と内部の0始まりの番号を混同しないこと。

### 7. Pythonによる基本実装

`tiles`が文字列から34要素の枚数タプルを作る。全分解を返す関数は、雀頭番号と面子タプルの組を返す。最終出力をsortedにすることで、集合の内部順序に左右されない結果を表示する。

**完成プログラム：lesson06_mahjong.py**

```python
"""第6回: 34種の牌で、門前14枚の通常形を全分解。役・点数は対象外。"""
Counts = tuple[int, ...]
Meld = tuple[int, int, int]


def tiles(man: str = '', pin: str = '', sou: str = '', honors: str = '') -> Counts:
    counts = [0] * 34
    for digits, offset, limit in [(man, 0, 9), (pin, 9, 9), (sou, 18, 9), (honors, 27, 7)]:
        for char in digits:
            if char not in '123456789'[:limit]:
                raise ValueError('invalid tile')
            counts[offset + int(char) - 1] += 1
    validate_counts(tuple(counts))
    return tuple(counts)


def validate_counts(counts: Counts) -> None:
    if len(counts) != 34 or any(type(n) is not int or not 0 <= n <= 4 for n in counts):
        raise ValueError('34 counts, each integer 0..4 required')


def decompositions(counts: Counts) -> list[tuple[int, tuple[Meld, ...]]]:
    validate_counts(counts)
    if sum(counts) != 14:
        raise ValueError('closed 14-tile hand required')
    remaining = list(counts)
    results: set[tuple[int, tuple[Meld, ...]]] = set()
    path: list[Meld] = []
    def remove_melds(pair: int) -> None:
        index = next((i for i, n in enumerate(remaining) if n), -1)
        if index == -1:
            results.add((pair, tuple(sorted(path))))
            return
        choices: list[Meld] = []
        if remaining[index] >= 3:
            choices.append((index, index, index))
        if index < 27 and index % 9 <= 6 and remaining[index+1] and remaining[index+2]:
            choices.append((index, index+1, index+2))
        for meld in choices:
            for tile in meld:
                remaining[tile] -= 1
            path.append(meld)
            remove_melds(pair)
            path.pop()
            for tile in meld:
                remaining[tile] += 1
    for pair in range(34):
        if remaining[pair] >= 2:
            remaining[pair] -= 2
            remove_melds(pair)
            remaining[pair] += 2
    return sorted(results)


def is_agari(counts: Counts) -> bool:
    return bool(decompositions(counts))


if __name__ == '__main__':
    hand = tiles(man='11122233344455')
    answers = decompositions(hand)
    assert len(answers) == 4
    assert not is_agari(tiles(man='19', pin='19', sou='19', honors='11234567'))
    print('normal decompositions:', len(answers))
    for pair, melds in answers:
        print('pair:', pair, 'melds:', melds)
```

### 8. コードの実行過程

雀頭候補を一つ選ぶと、外側で2枚を減らす。内側のremove_meldsは、最小の残り牌を探し、取り出せる面子をchoicesへ入れる。面子を選ぶたびに枚数を減らしてpathへ記録し、子を呼ぶ。子がreturnした後はpathをpopし、減らした牌をすべて足し戻す。

この関数は全分解を集めるため、成功しても上の呼び出しをまとめて終了しない。空の状態で結果を保存したら、その呼び出しだけが戻り、親が別の面子を試す。第3回の一解探索とreturnの意味は同じだが、親が成功を受けて終了する仕組みを使っていない。

面子の順序が違うだけなら同じ分解として扱う。`tuple(sorted(path))`で面子の並びを正規化し、setへ入れることで重複を除く。牌番号の順番と、面子の列挙順序は別物である。正規化してよいのは、この問題で順序に意味がないからだ。

**実行結果**

```text
normal decompositions: 4
pair: 1 melds: ((0, 0, 0), (1, 2, 3), (2, 3, 4), (2, 3, 4))
pair: 4 melds: ((0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3))
pair: 4 melds: ((0, 0, 0), (1, 2, 3), (1, 2, 3), (1, 2, 3))
pair: 4 melds: ((0, 1, 2), (0, 1, 2), (0, 1, 2), (3, 3, 3))
```

4分解のうち一つは雀頭が22であり、`111 / 234 / 345 / 345 / 22`になる。雀頭55だけを試して終えると、この分解を見落とす。雀頭の探索と面子の探索を分ける理由がここに現れる。

### 9. 改良版アルゴリズム

和了しているかだけ知りたいなら、最初の成功でTrueを返せばよい。ただし全分解を求める第6回の関数とは出力の契約が変わる。第7回ではこの判定版をメモ化する。

七対子は異なる7種類の対子、国士無双は13種類の么九牌とそのうち一種類の対子という別形である。本回の通常形判定がFalseでも、特殊形では和了していることがある。通常形と特殊形を別関数にし、必要に応じて論理和を取る構成が分かりやすい。

### 10. 計算量と適用条件

牌種数T、取り出す面子数Mとすると、雀頭候補をT通り、各段で最大2分岐、最小牌を探す費用をO(T)として、粗い時間上界はO(T²2ᴹ)に出力正規化・保存費用を加えたものになる。実際にはT=34、M=4と固定なので小さい。一般のN枚の探索の指数性と、固定14枚の実行コストを混同しない。

探索中の枚数表とスタックはO(T+M)。全分解がR件ならO(RM)の出力領域も使う。牌を4枚までに制限し、色の境界を確認することは、計算効率より先に必要な正しさの条件である。

### 11. Python実習

通常形の完成例と、国士無双の完成例を入力し、前者だけTrueになることを確認する。次に各分解をもう一度34要素の枚数へ戻し、入力と完全一致するか確かめる。これは見た目がもっともらしいだけの誤分解を検出する。

入力の牌の並びを変えても枚数タプルは同じになる。`tiles(man='123123')`と`tiles(man='112233')`を比べ、順序を捨てる状態表現が探索へ与える意味を説明しよう。

### 12. 練習問題

- **6-B 基礎**：`index < 27`と`index % 9 <= 6`は、それぞれ何を防ぐか。
- **6-S 標準**：14枚の七対子判定を追加する方針を書け。同じ牌4枚を2対子として認めるかを明記せよ。
- **6-A 発展**：最小の残り牌を使わず、取り出せるすべての面子を順不同で試した場合、どのような重複が生じるか。

### 13. 理解度確認問題

**6-Q1**：通常形判定がTrueなら、実戦で必ず和了を宣言できるか。**6-Q2**：setへ入れるだけで、探索中の重複計算もなくなるか。**6-Q3**：成功した枝でも枚数を戻すのはなぜか。

### 14. まとめ

状態を牌の枚数として表し、最小の残り牌を基準にすると、網羅性を維持しながら分岐を減らせる。全列挙では成功後も復元して探索を続ける。正規化は出力の重複を除くが、計算の再利用とは別の工夫である。

### 15. 次回への接続

違う面子の取り方を経て、同じ残り牌へ到達することがある。その先の答えを何度も計算する必要はない。次回は状態と答えを対応づけて保存する。


<a id="lesson07"></a>

## 第7回　メモ化探索――同じ問題を二度解かない

### 1. 講義タイトルと到達点

再帰の呼び出しが同じ部分問題へ何度も戻るとき、答えを保存して再利用する。キャッシュを付ければ何でも速くなるという理解を避け、何を状態として保存すれば正しいかを説明できるようにする。

### 2. この回で学ぶこと

フィボナッチ数列、重複部分問題、辞書によるメモ化、`functools.cache`、状態の正規化、キャッシュのヒットとミスを扱う。麻雀の通常形判定を再登場させ、全分解の出力とboolの判定では再利用する値が違うことを確認する。

### 3. 前回までの復習

第6回は、面子を取り除いた残り牌を再帰へ渡した。もし二つの経路が同じ残り牌になれば、そこから面子だけへ分けられるかという答えは同じである。これまでの履歴が違っても、未来の可能性が同じなら一つの部分問題として扱える。

### 4. 身近な問題からの導入

F(0)=0、F(1)=1、F(n)=F(n−1)+F(n−2)という数列を考える。F(5)を計算するにはF(4)とF(3)が必要であり、F(4)を計算する途中でもF(3)が現れる。紙で計算するなら、F(3)=2と一度書いたらその値を再利用するはずだ。

素朴な再帰は、そのメモを持たない。F(3)の呼び出しは前にも計算したことを知らず、再びF(2)とF(1)を呼ぶ。式そのものは簡潔でも、実行される仕事には大きな重複がある。メモ化は人間の計算メモを関数の仕組みにする方法だ。

### 5. アルゴリズムの原理

辞書のキーをn、値をF(n)と考える。関数の入口でnが辞書にあればその値を返す。なければ通常どおり計算し、辞書へ保存して返す。Pythonの`@cache`はこの処理を関数の周囲に付ける。デコレータの詳しい構文を知らなくても、引数から戻り値へのメモ帳が付くと理解すれば本回の実習はできる。

ただし、同じ引数なら同じ答えという条件が必要だ。外部の可変盤面を読んでいるのに引数がない関数へcacheを付けると、盤面が変わっても同じキーとして扱われ、誤答を返す。残り牌なら、その全枚数をキーに含める。ナップサックなら残り容量だけでなく、どの品物まで判断したかも必要になる。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 330" role="img" aria-labelledby="fig07-title"><title id="fig07-title">図7　メモ化で同じ部分問題を共有する</title><rect width="720" height="330" fill="#fff"/><g font-family="sans-serif"><text x="170" y="25" font-size="20" fill="#142c40" text-anchor="middle">呼び出し木</text><text x="550" y="25" font-size="20" fill="#142c40" text-anchor="middle">状態を共有</text><path d="M170,75 L90,150" stroke="#526574" stroke-width="2" fill="none" /><path d="M170,75 L260,150" stroke="#526574" stroke-width="2" fill="none" /><path d="M90,150 L150,235" stroke="#526574" stroke-width="2" fill="none" /><rect x="122" y="55" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="170.0" y="81.0" font-size="18" fill="#142c40" text-anchor="middle">F(5)</text><rect x="42" y="130" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="90.0" y="156.0" font-size="18" fill="#142c40" text-anchor="middle">F(4)</text><rect x="212" y="130" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="260.0" y="156.0" font-size="18" fill="#142c40" text-anchor="middle">F(3)</text><rect x="102" y="215" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="150.0" y="241.0" font-size="18" fill="#142c40" text-anchor="middle">F(3)</text><path d="M550,75 L470,150" stroke="#526574" stroke-width="2" fill="none" /><path d="M550,75 L600,235" stroke="#526574" stroke-width="2" fill="none" /><path d="M470,150 L600,235" stroke="#526574" stroke-width="2" fill="none" /><rect x="502" y="55" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="550.0" y="81.0" font-size="18" fill="#142c40" text-anchor="middle">F(5)</text><rect x="422" y="130" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="470.0" y="156.0" font-size="18" fill="#142c40" text-anchor="middle">F(4)</text><rect x="552" y="215" width="96" height="40" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="600.0" y="241.0" font-size="18" fill="#142c40" text-anchor="middle">F(3)</text><text x="360" y="310" font-size="18" fill="#142c40" text-anchor="middle">同じnの本体は一度だけ計算。再訪は保存済みの値を返す。</text></g></svg></div><figcaption>図7：メモ化による状態共有</figcaption></figure>

左はF(3)が複数回現れる呼び出し木、右は同じnを一つの状態として共有する関係を表す。実際にPythonのコールスタックが図のグラフそのものへ変わるわけではない。関数呼び出しは行われるが、計算済みならその先の再帰展開が省略される。

| F(4)の計算中 | 状態 | 動作 |
|---|---|---|
| F(2)初回 | 未保存 | F(1),F(0)から1を作り保存 |
| F(3)完成 | F(2)等を利用 | 2を保存 |
| F(4)右側のF(2) | 保存済み | 1をすぐ返す |
| F(4)完成 | 子の値がそろう | 3を保存 |

キャッシュには「再帰から戻って計算が完成した値」を入れる。循環のある依存関係では、まだ完成していない同じ状態を呼び直す可能性がある。cacheだけではその無限再帰を解決できない。

### 7. Pythonによる基本実装

本回の麻雀関数は第6回の入力変換と検証をimportする。ZIPを展開し、全lessonファイルを同じフォルダに置いて実行する。書籍内には参照先のコードも省略せず掲載している。

**完成プログラム：lesson07_memoization.py**

```python
"""第7回: 戻り値をキャッシュする。"""
from functools import cache
from lesson06_mahjong import Counts, tiles, validate_counts


def fibonacci_plain(n: int) -> int:
    if n < 0:
        raise ValueError('n >= 0 required')
    if n < 2:
        return n
    return fibonacci_plain(n-1) + fibonacci_plain(n-2)


@cache
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError('n >= 0 required')
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def is_agari_memo(counts: Counts) -> tuple[bool, object]:
    validate_counts(counts)
    if sum(counts) != 14:
        raise ValueError('14 tiles required')
    @cache
    def meldable(state: Counts) -> bool:
        index = next((i for i, n in enumerate(state) if n), -1)
        if index == -1:
            return True
        choices = []
        if state[index] >= 3:
            choices.append((index, index, index))
        if index < 27 and index % 9 <= 6 and state[index+1] and state[index+2]:
            choices.append((index, index+1, index+2))
        for meld in choices:
            remaining = list(state)
            for tile in meld:
                remaining[tile] -= 1
            if meldable(tuple(remaining)):
                return True
        return False
    for pair in range(34):
        if counts[pair] >= 2:
            remaining = list(counts)
            remaining[pair] -= 2
            if meldable(tuple(remaining)):
                return True, meldable.cache_info()
    return False, meldable.cache_info()


if __name__ == '__main__':
    fibonacci.cache_clear()
    assert fibonacci(20) == fibonacci_plain(20) == 6765
    print('fib(20):', fibonacci(20))
    print('cache:', fibonacci.cache_info())
    answer, info = is_agari_memo(tiles(man='11122233344455'))
    assert answer
    print('normal agari:', answer)
    print('hand cache:', info)
```

### 8. コードの実行過程

`fibonacci(20)`の初回計算では、0〜20の21状態が実計算される。もう一度20を呼べば、入口で保存済みの6765を返す。出力のhitsにはこの再呼び出しも含まれるので、理論の「異なる状態数」と表示される総ヒット回数は別の指標である。

麻雀の`meldable`では、受け取ったタプルを変更できないため、子を作るときだけリストへ変換し、取り出した面子の枚数を減らして再びタプルにする。親のタプルは変わらないので、子から戻った後の足し戻しは不要だ。第6回の共有リストを変更・復元する方式と、状態のコピーを渡す方式は、同じ探索を異なる管理方法で表している。

雀頭は外側で除去済みなので、meldableの答えは残り牌だけで決まる。どの雀頭を選んだかをキーへ入れる必要はない。一方、全分解を列挙したい場合にboolだけを保存しても、どんな面子が作れたかは復元できない。目的に応じて、分解の集合や次の選択などを保存する必要がある。

**実行結果**

```text
fib(20): 6765
cache: CacheInfo(hits=19, misses=21, maxsize=None, currsize=21)
normal agari: True
hand cache: CacheInfo(hits=0, misses=9, maxsize=None, currsize=9)
```

この手牌の判定ではhitsが0である。成功が早く見つかったので同一状態の再訪がなかった。メモ化の実装が正しいことと、その入力で速くなることは別であり、キャッシュ費用の分だけ不利になる可能性もある。

### 9. 改良版アルゴリズム

F(n)の値だけが欲しければ、前の二つの値を変数で持ってループを回せる。この場合、全キャッシュや再帰スタックを保持せずに済む。これは次回のボトムアップDPへの橋渡しになる。

キャッシュを長時間生存させる場合はメモリを消費し続ける。`lru_cache(maxsize=...)`で件数を制限する方法があるが、追い出された状態は再計算するため、無制限メモ化の「各状態を一度だけ実計算」という計算量の説明はそのまま適用できない。

### 10. 計算量と適用条件

素朴なフィボナッチ再帰はT(n)=T(n−1)+T(n−2)+O(1)で、O(2ⁿ)という粗い上界を持つ。より鋭くは黄金比φを使ってΘ(φⁿ)回程度である。メモ化後はn+1状態なので、整数演算を定数時間とみなせばO(n)時間、O(n)領域になる。F(n)の桁数も増えるため、巨大なnのビット計算量では加算費用を追加する必要がある。

麻雀では訪れた異なる状態数をSとすれば、おおむねO(ST)に雀頭の生成費用が加わる。ここでT=34で、タプルの作成・ハッシュ化・最小牌の走査にはO(T)を見込む。状態の総数自体が大きければ、メモ化しても多項式時間になるとは限らない。

### 11. Python実習

キャッシュをclearした初回、clearしない再実行、素朴な再帰の三つを比較する。速度比較では計算済み状態を使った「温かいキャッシュ」と、最初から作る「冷たいキャッシュ」を分けて記録する。麻雀では全分解版と判定版の時間を単純に比較せず、返している情報量の違いを先に記す。

### 12. 練習問題

- **7-B 基礎**：F(6)までを計算した後にF(5)を呼ぶと、F(4)へ再帰するか。
- **7-S 標準**：数独の関数`search()`にそのまま@cacheを付けてはいけない理由を、キーの観点から説明せよ。
- **7-A 発展**：牌を並び順のあるリストとしてキーにする場合と、34種の枚数としてキーにする場合を比べよ。

### 13. 理解度確認問題

**7-Q1**：メモ化すれば探索の最悪計算量は必ず多項式になるか。**7-Q2**：副作用を持つ関数の戻り値だけを再利用すると何が変わるか。**7-Q3**：キャッシュのヒットが0でも、プログラムが誤っているとは限らない理由は何か。

### 14. まとめ

メモ化の中心は、未来の計算結果を決定する状態を見つけることだ。引数を正規化し、同じ部分問題だけを共有する。再帰木は重複状態を共有する見方へ変わるが、状態数と保存費用は残る。

### 15. 次回への接続

部分問題が分かれば、必要になる順番に表を埋めることもできる。第8回では、同じ漸化式をメモ化再帰と表計算の両方で実装する。


<a id="lesson08"></a>

## 第8回　動的計画法――ナップサック問題

### 1. 講義タイトルと到達点

限られた予算の中で改善テーマを選び、効果の合計を最大にする。全探索・メモ化再帰・二次元DP・一次元DPを同じデータへ適用し、値が一致することを確認する。DPの式を暗記せず、状態の意味から導くことが目標だ。

### 2. この回で学ぶこと

最適部分構造、部分問題の重複、トップダウンとボトムアップ、遷移式、表からの選択復元、一次元圧縮の逆順ループを扱う。Excelで表を作る経験がある読者は、DPのセルを「意味の決まった部分問題の答え」として読むとよい。

### 3. 前回までの復習

メモ化再帰は必要な状態を呼び出して答えを保存するトップダウン型DPの一つである。DPは表をforで埋める手法だけを指すわけではない。依存関係に沿って部分問題の答えを再利用する考え方が共通している。

### 4. 身近な問題からの導入

改善テーマAは予算2で効果3、Bは予算3で効果4、Cは予算4で効果5とする。総予算は5。一つずつしか採用できない。効果最大のCだけを選ぶと5だが、AとBなら7になる。効果が最大のテーマから順に選べばよいとは限らない。

人間なら、最後のテーマCを採るか採らないかに分けて考えられる。採らないならA,Bだけで予算5の問題になる。採るなら残り予算1でA,Bを選ぶ問題になり、Cの効果5を足す。このように、選択一つを確定すると残りが同型の小さな問題になる。

### 5. アルゴリズムの原理

dp[i][c]を「先頭i件だけを使い、容量c以下で得られる最大価値」と定める。容量をちょうど使い切る問題ではないので、空集合は常に価値0の候補である。品物iの重さをwᵢ、価値をvᵢとすると、次の式になる。

<div class="equation">dp[i,c] = max(dp[i−1,c], dp[i−1,c−wᵢ] + vᵢ)　（wᵢ ≤ c）</div>

入らない場合はdp[i−1,c]をそのまま使う。初期行dp[0,c]はすべて0。ここで「採用した後の残り部分が最適である」と言えることが大切だ。もし残り部分をもっと高価値の選択へ交換できるなら、全体の価値も上げられ、元が最適であることに反する。

この最適部分構造は、価値が加算でき、使った予算以外の履歴が将来を左右しないモデルで成立する。テーマAとBを一緒に行うと相乗効果が出る、あるテーマが別テーマの前提になる、といった条件を勝手に無視して同じDPを使ってはいけない。必要なら状態や遷移を増やす。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 320" role="img" aria-labelledby="fig08-title"><title id="fig08-title">図8　DPテーブルと前の行からの遷移</title><rect width="720" height="320" fill="#fff"/><g font-family="sans-serif"><text x="210" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=0</text><text x="290" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=1</text><text x="370" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=2</text><text x="450" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=3</text><text x="530" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=4</text><text x="610" y="27" font-size="17" fill="#142c40" text-anchor="middle">c=5</text><text x="90" y="75" font-size="18" fill="#142c40" text-anchor="middle">なし</text><rect x="175" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="210.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="255" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="290.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="335" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="370.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="415" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="450.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="495" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="530.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="575" y="45" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="610.0" y="73.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><text x="90" y="130" font-size="18" fill="#142c40" text-anchor="middle">Aまで</text><rect x="175" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="210.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="255" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="290.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="335" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="370.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><rect x="415" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="450.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><rect x="495" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="530.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><rect x="575" y="100" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="610.0" y="128.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><text x="90" y="185" font-size="18" fill="#142c40" text-anchor="middle">Bまで</text><rect x="175" y="155" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="210.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="255" y="155" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="290.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="335" y="155" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="370.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><rect x="415" y="155" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="450.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="495" y="155" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="530.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="575" y="155" width="70" height="44" rx="9" fill="#ffeadb" stroke="#147d86" stroke-width="1.5"/><text x="610.0" y="183.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><text x="90" y="240" font-size="18" fill="#142c40" text-anchor="middle">Cまで</text><rect x="175" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="210.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="255" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="290.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">0</text><rect x="335" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="370.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">3</text><rect x="415" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="450.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">4</text><rect x="495" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="530.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">5</text><rect x="575" y="210" width="70" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="610.0" y="238.0" font-size="18" fill="#142c40" text-anchor="middle">7</text><text x="360" y="300" font-size="21" fill="#142c40" text-anchor="middle">Bまで・容量5：max(3, 3+4) = 7</text></g></svg></div><figcaption>図8：DPテーブル</figcaption></figure>

| 使用できる品物＼容量 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| なし | 0 | 0 | 0 | 0 | 0 | 0 |
| Aまで | 0 | 0 | 3 | 3 | 3 | 3 |
| Bまで | 0 | 0 | 3 | 4 | 4 | 7 |
| Cまで | 0 | 0 | 3 | 4 | 5 | 7 |

Bまでの容量5のセルは、Bを採らない価値3と、採って残り容量2の価値3へBの価値4を足した7を比較する。左隣のセルだけでなく、必ず一つ前の行を参照する。これが同じ品物の二重使用を防いでいる。

### 7. Pythonによる基本実装

本実装は重さを正整数、価値を非負整数、容量を非負整数に限定する。0-1は各品物を採るか採らないかを意味し、価値が0か1という意味ではない。重さ0を扱えないわけではないが、第10回の価値密度と共通の入力契約にするため除外する。

**完成プログラム：lesson08_knapsack.py**

```python
"""第8回: 0-1ナップサック。重さは正整数、価値は非負整数。"""
from functools import cache
from itertools import product
Item = tuple[int, int]  # weight, value


def validate(items: list[Item], capacity: int) -> None:
    if type(capacity) is not int or capacity < 0:
        raise ValueError('nonnegative integer capacity required')
    if any(type(w) is not int or w <= 0 or type(v) is not int or v < 0 for w, v in items):
        raise ValueError('positive integer weight and nonnegative integer value required')


def brute_force(items: list[Item], capacity: int) -> int:
    validate(items, capacity)
    best = 0
    for chosen in product((0, 1), repeat=len(items)):
        weight = sum(w*b for (w, v), b in zip(items, chosen))
        value = sum(v*b for (w, v), b in zip(items, chosen))
        if weight <= capacity:
            best = max(best, value)
    return best


def top_down(items: list[Item], capacity: int) -> int:
    validate(items, capacity)
    @cache
    def best(index: int, rest: int) -> int:
        if index == len(items):
            return 0
        weight, value = items[index]
        answer = best(index+1, rest)
        if weight <= rest:
            answer = max(answer, value + best(index+1, rest-weight))
        return answer
    return best(0, capacity)


def table_dp(items: list[Item], capacity: int) -> tuple[int, list[int], list[list[int]]]:
    validate(items, capacity)
    dp = [[0] * (capacity+1) for _ in range(len(items)+1)]
    for i, (weight, value) in enumerate(items, 1):
        for room in range(capacity+1):
            dp[i][room] = dp[i-1][room]
            if weight <= room:
                dp[i][room] = max(dp[i][room], dp[i-1][room-weight] + value)
    chosen = []
    room = capacity
    for i in range(len(items), 0, -1):
        if dp[i][room] != dp[i-1][room]:
            chosen.append(i-1)
            room -= items[i-1][0]
    return dp[-1][-1], chosen[::-1], dp


def compressed_dp(items: list[Item], capacity: int) -> int:
    validate(items, capacity)
    dp = [0] * (capacity+1)
    for weight, value in items:
        for room in range(capacity, weight-1, -1):
            dp[room] = max(dp[room], dp[room-weight] + value)
    return dp[capacity]


ITEMS = [(2, 3), (3, 4), (4, 5)]
if __name__ == '__main__':
    answer, chosen, dp = table_dp(ITEMS, 5)
    assert answer == brute_force(ITEMS, 5) == top_down(ITEMS, 5) == compressed_dp(ITEMS, 5) == 7
    assert compressed_dp([(2, 3)], 4) == 3
    print('best:', answer, 'chosen:', chosen)
    print('DP rows:')
    for row in dp:
        print(row)
```

### 8. コードの実行過程

`brute_force`は各品物の採否を0/1で全列挙する。これは正解基準であり、効率のよい本命ではない。`top_down`はindexとrestをキーとし、同じ残り品物・同じ残り容量を一度だけ実計算する。table_dpは同じ依存関係を下から表として埋める。

選択の復元では最終行から戻る。dp[i][room]がdp[i−1][room]と異なるなら、品物iを使わなければその値に達せないので採用する。等しい場合は、不採用でも同じ価値に達するため不採用を選ぶ。この規則は一つの最適解を返すだけで、同価値の全最適解を列挙するわけではない。

一次元DPでは、古い行の値と新しい行の値を同じ配列へ置く。容量を大きい方から更新すれば、参照する`dp[room-weight]`はまだその品物を反映していない値である。小さい方から更新すると、同じ品物で更新済みの値を再利用してしまう。

具体的に品物(重さ2,価値3)一つ、容量4を考える。昇順ではdp[2]=3の後、dp[4]=dp[2]+3=6となり、同じ品物を2回採った値が出る。降順ならdp[4]を計算するときdp[2]はまだ0なので、正しい値3を得る。

**実行結果**

```text
best: 7 chosen: [0, 1]
DP rows:
[0, 0, 0, 0, 0, 0]
[0, 0, 3, 3, 3, 3]
[0, 0, 3, 4, 4, 7]
[0, 0, 3, 4, 5, 7]
```

### 9. 改良版アルゴリズム

値だけ必要なら一次元圧縮で領域をO(W)にできる。選択内容も必要な場合、二次元表を保存する方法が初学者には追いやすい。一次元表に単純な親ポインタを付けると、後の更新によって過去の選択履歴が変わる問題があるので、安易に復元できると考えない。

容量が巨大で価値の合計が小さいなら、「価値を達成するための最小重さ」を状態にする逆のDPを考えられる。どの量を表の軸にするかは、入力の上限で判断する。DPは万能な高速化ではなく、状態空間を扱える大きさに設計する技術である。

### 10. 計算量と適用条件

N件、容量Wに対し、全探索実装は各候補でN件を合計するためO(N2ᴺ)。二次元DPはO(NW)時間・O(NW)領域、一次元DPはO(NW)時間・O(W)領域である。トップダウンは到達した状態だけを計算し、最悪O(NW)時間・領域と深さO(N)のスタックを使う。

O(NW)は擬多項式時間と呼ばれる。Wを二進数で書く入力長は約log₂Wなので、W=10⁹を表の幅にすると、入力文字数は短くても表が巨大になる。重量が実数なら、そのまま整数添字の表にはできない。単位を粗くして丸めると別の問題へ変わるため、誤差を明示する。

### 11. Python実習

3件の例を手計算し、出力の全行と照合する。次に容量0、品物なし、すべて容量超過、同じ品物データが複数件ある場合を試す。同じデータが2件ある場合は別の品物なので両方採用できることと、一つの品物を2回使うことは違う。

実務風の課題として、5件の改善テーマへ工数と効果を割り当て、予算を変えながら選択がどう切り替わるか調べる。効果の数値は教材用の仮定であり、現実の評価が客観的に測れたことを意味しない。

### 12. 練習問題

- **8-B 基礎**：A=(2,3)、B=(3,4)、容量4の最適価値と選択を求めよ。
- **8-S 標準**：一次元DPを昇順にしたとき、どの問題を解く更新式になるか。重さが正である条件にも触れよ。
- **8-A 発展**：予算を「以下」でなく「ちょうど使い切る」に変更すると、初期値はどう変える必要があるか。

### 13. 理解度確認問題

**8-Q1**：DPのキーに残り容量だけを使うと、なぜ不十分か。**8-Q2**：O(NW)だから、どんな容量でも現実的に計算できるか。**8-Q3**：メモ化再帰はDPと無関係か。

### 14. まとめ

DPでは、各状態の意味を先に固定し、最後の選択から遷移を導く。一次元圧縮は式を短くするだけではなく、依存する古い値が上書きされない順序を守る変更である。

### 15. 次回への接続

迷路にも、ある地点までの最小費用という部分問題がある。ただし、費用順に処理する仕組みが必要だ。次回は優先度付きキューを使う最短経路探索へ戻る。


<a id="lesson09"></a>

## 第9回　グラフ探索――最短経路を求める

### 1. 講義タイトルと到達点

道路ごとの移動時間が異なるグラフで、最小費用の経路を求める。ダイクストラ法とA*を同じ実装へまとめ、ヒューリスティックを0にするとダイクストラ法になる関係を見る。

### 2. この回で学ぶこと

辺の重み、距離の緩和、優先度付きキュー、古いキュー項目の除外、許容的・整合的ヒューリスティックを扱う。A*が必ず速いわけではなく、最適性を保証するための条件があることを明確にする。

### 3. 前回までの復習

BFSは到達までの辺数が少ない頂点から展開した。重みが異なる場合、同じ辺数でも費用は異なる。DPでは部分問題の答えを更新したが、グラフには循環もあり、単純な番号順に一度ずつ計算するだけでは正しくない場合がある。

### 4. 身近な問題からの導入

SからAへ2分、SからBへ5分、AからBへ1分、AからGへ7分、BからGへ2分かかるとする。S→B→Gは7分、S→A→Gは9分、S→A→B→Gは5分だ。辺数が多くても最短時間になる場合がある。

人間なら、到達済みの場所に「今までに分かった最短時間」を書き込み、別ルートで短縮できるたびに書き直す。ただし、どこから次に調べるかを無計画に決めると、書き直しが増える。ダイクストラ法は暫定距離が最小の頂点を先に扱う。

### 5. アルゴリズムの原理

距離g(u)が分かっている頂点uから、費用wの辺でvへ行く候補はg(u)+wである。これが現在のg(v)より小さければ更新する。この操作が緩和である。未到達の距離は無限大とみなす。

非負重みなら、最小の暫定距離で取り出した頂点へ、未確定の頂点を経由してさらに短く到達することはない。途中までの費用がすでにそれ以上で、その先に負の費用がないからだ。これがダイクストラ法の確定の根拠である。

A*は、ここまでの実費gにゴールまでの推定費用hを加えたf=g+hの小さい順に展開する。hが真の残り費用を超えないことを許容性と呼ぶ。さらに各辺でh(u)≤w(u,v)+h(v)が成立するなら整合的という。本実装は改善された頂点を再度キューへ入れて再展開できるため、有限グラフ・非負重み・許容的なh、h(goal)=0の下で最適解を返す。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 300" role="img" aria-labelledby="fig09-title"><title id="fig09-title">図9　非負重みの道路グラフ</title><rect width="720" height="300" fill="#fff"/><g font-family="sans-serif"><path d="M118.67699537200556,132.27757952613123 L274.4520604406608,73.42922161130593" stroke="#147d86" stroke-width="2" fill="none" /><polygon points="274.4520604406608,73.42922161130593 266.8643423475854,81.6405877668258 263.33033666039967,72.2858668301576" fill="#147d86"/><text x="190" y="85" font-size="22" fill="#142c40" text-anchor="middle">2</text><path d="M118.67699537200556,157.72242047386877 L274.4520604406608,216.57077838869407" stroke="#abb5bb" stroke-width="2" fill="none" /><polygon points="274.4520604406608,216.57077838869407 263.33033666039967,217.7141331698424 266.8643423475854,208.35941223317417" fill="#abb5bb"/><text x="190" y="225" font-size="22" fill="#142c40" text-anchor="middle">5</text><path d="M310.0,96.0 L310.0,192.0" stroke="#147d86" stroke-width="2" fill="none" /><polygon points="310.0,192.0 305.0,182.0 315.0,182.0" fill="#147d86"/><text x="330" y="150" font-size="22" fill="#142c40" text-anchor="middle">1</text><path d="M344.756834958421,69.37882848084375 L588.3122297661112,135.10012549244271" stroke="#abb5bb" stroke-width="2" fill="none" /><polygon points="588.3122297661112,135.10012549244271 577.3549383219882,137.32223354754458 579.9601684555558,127.66755717020541" fill="#abb5bb"/><text x="470" y="82" font-size="22" fill="#142c40" text-anchor="middle">7</text><path d="M344.756834958421,220.62117151915623 L588.3122297661112,154.89987450755729" stroke="#147d86" stroke-width="2" fill="none" /><polygon points="588.3122297661112,154.89987450755729 579.9601684555558,162.3324428297946 577.3549383219882,152.67776645245542" fill="#147d86"/><text x="470" y="225" font-size="22" fill="#142c40" text-anchor="middle">2</text><rect x="55" y="123" width="60" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="85.0" y="151.0" font-size="18" fill="#142c40" text-anchor="middle">S</text><rect x="280" y="38" width="60" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="310.0" y="66.0" font-size="18" fill="#142c40" text-anchor="middle">A</text><rect x="280" y="208" width="60" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="310.0" y="236.0" font-size="18" fill="#142c40" text-anchor="middle">B</text><rect x="595" y="123" width="60" height="44" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="625.0" y="151.0" font-size="18" fill="#142c40" text-anchor="middle">G</text><text x="360" y="290" font-size="17" fill="#142c40" text-anchor="middle">辺のラベルは移動費用／最短 S→A→B→G = 5</text></g></svg></div><figcaption>図9：距離の更新と最短経路</figcaption></figure>

| 取り出す頂点 | 主な緩和 | 暫定距離A,B,G |
|---|---|---|
| S（0） | A=2、B=5 | 2,5,∞ |
| A（2） | Bを3へ、G=9 | 2,3,9 |
| B（3） | Gを5へ | 2,3,5 |
| G（5） | ゴール到達 | 2,3,5 |

B=5として登録した古い項目もキューに残る。取り出した値と現在のdistanceを比較し、不一致なら無視する。優先度をキュー内で直接書き換える機構を使わずに済む実装だ。

### 7. Pythonによる基本実装

頂点名は比較可能な文字列へ統一する。同じ優先度の場合、heapqはタプルの次の要素、さらに頂点名を比較する。任意のオブジェクトを頂点にしたい場合には、比較用の通し番号を追加する設計が必要になる。

**完成プログラム：lesson09_shortest_path.py**

```python
"""第9回: 非負重み、再オープン可能なA*。h=0ならダイクストラ。"""
from collections.abc import Callable
from heapq import heappush, heappop
from math import inf, isfinite
Graph = dict[str, list[tuple[str, float]]]


def shortest_path(graph: Graph, start: str, goal: str,
                  heuristic: Callable[[str], float] = lambda vertex: 0) -> tuple[float, list[str], int]:
    if start not in graph or goal not in graph:
        raise ValueError('unknown endpoint')
    for edges in graph.values():
        for neighbor, weight in edges:
            if neighbor not in graph or not isfinite(weight) or weight < 0:
                raise ValueError('known vertices and finite nonnegative weights required')
    h = {vertex: heuristic(vertex) for vertex in graph}
    if any(not isfinite(value) or value < 0 for value in h.values()) or h[goal] != 0:
        raise ValueError('finite nonnegative h; h(goal)=0 required')
    distance = {start: 0.0}
    parent: dict[str, str] = {}
    queue = [(h[start], 0.0, start)]
    expanded = 0
    while queue:
        _, cost, vertex = heappop(queue)
        if cost != distance.get(vertex, inf):
            continue  # 古い距離で登録された項目
        expanded += 1
        if vertex == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return cost, path[::-1], expanded
        for neighbor, weight in graph[vertex]:
            candidate = cost + weight
            if candidate < distance.get(neighbor, inf):
                distance[neighbor] = candidate
                parent[neighbor] = vertex
                heappush(queue, (candidate + h[neighbor], candidate, neighbor))
    return inf, [], expanded


ROAD = {'S': [('A', 2), ('B', 5)], 'A': [('B', 1), ('G', 7)],
        'B': [('G', 2)], 'G': []}
if __name__ == '__main__':
    estimates = {'S': 4, 'A': 3, 'B': 2, 'G': 0}
    dijkstra = shortest_path(ROAD, 'S', 'G')
    astar = shortest_path(ROAD, 'S', 'G', estimates.__getitem__)
    assert dijkstra[0] == astar[0] == 5
    assert shortest_path(ROAD, 'G', 'S')[0] == inf
    print('Dijkstra:', dijkstra)
    print('A*:', astar)
```

### 8. コードの実行過程

キューの要素は`(f, g, 頂点)`である。最初の値は取り出し優先度、二番目はその登録時点の実費だ。gを別に保存することで、hが変わらない同じ頂点について古い距離の登録を判別できる。

ゴールへ辺を発見した時点では終了しない。初めてGへ到達する候補は9だが、その後B経由で5へ更新される。適切な優先度でゴールをキューから取り出したときに終了する。`parent[neighbor]=vertex`も距離が改善された時点で書き直すため、最後の親をたどれば最小費用の経路が得られる。

**実行結果**

```text
Dijkstra: (5.0, ['S', 'A', 'B', 'G'], 4)
A*: (5.0, ['S', 'A', 'B', 'G'], 4)
```

この小さなグラフではA*も4頂点を展開し、ダイクストラ法と同じ回数である。ヒューリスティックを付けたというだけで、展開回数が必ず減るわけではない。

### 9. 改良版アルゴリズム

上下左右に一歩費用1で動く格子なら、マンハッタン距離`|r−rg|+|c−cg|`は障害物を無視した下界となり、許容的かつ整合的である。斜め移動やワープを加えると条件が変わり、この下界が使えるとは限らなくなる。

道路の直線距離を時間へ換算するなら、距離を許される最大速度で割った値が候補になる。ただし、データの単位・移動規則が合うことが必要だ。「それらしい推定」は過大評価しているかもしれず、最適性の証明の代わりにならない。

### 10. 計算量と適用条件

この重複登録式ダイクストラ実装では、各辺の緩和と高々O(E)個のキュー項目を考え、時間O((V+E) log(V+E))、入力以外の領域O(V+E)が安全な評価となる。単純グラフではよくO((V+E) log V)と表す。

A*が整合的なら各頂点の確定を同様に考えられる。一方、許容的でも非整合なhでは再展開が起こり、同じ計算量を無条件には主張できない。本実装は負辺を拒否する。負辺を含む一般の問題ではベルマン–フォード法など別の方法を検討する。

理論上の比較は正確な数値演算を仮定する。浮動小数点の移動時間では丸め誤差や極端な値の桁あふれに注意し、必要なら単位を定めた整数費用へモデル化する。本実装は開始距離を浮動小数点0.0で持つ教材実装であり、巨大整数の厳密経路計算を保証するものではない。

hが許容的かどうかを関数は自動検証しない。有限・非負・ゴールで0という必要な入力検査だけを行う。許容性はモデル側で根拠を用意する契約である。

### 11. Python実習

完成コードの道路グラフを手計算し、Bの距離が5から3へ変わることを確認する。次にhをすべて0としてA*とダイクストラが一致することを確かめる。第4回の迷路を重み1のグラフに変換すれば、BFSの移動回数とも一致する。異なる手法の一致は有用な検証になる。

### 12. 練習問題

- **9-B 基礎**：Gを発見した瞬間に終了した場合、この例ではいくつを答えてしまうか。
- **9-S 標準**：h=0が許容的かつ整合的になる条件を述べよ。
- **9-A 発展**：S→A=3、S→B=1、B→A=1、A→G=2、h(A)=0、h(B)=3、h(S)=4のとき、Aの再展開が必要になる順序を追え。

### 13. 理解度確認問題

**9-Q1**：負の辺が一つでもあれば、この実装の入力契約を満たすか。**9-Q2**：A*のhを大きくすれば、最適性を保ったまま必ず高速になるか。**9-Q3**：古いキュー項目を無視するのは、訪問済みの全頂点を二度と見ないことと同じか。

### 14. まとめ

重み付き探索では、発見と最短距離の確定を分けて考える。ダイクストラ法は非負重みを使い、A*は安全な残り費用の下界を使う。保証を支える条件を、実装と一緒に管理する。

### 15. 次回への接続

最短経路では残り費用の下界が役立った。価値最大化では、これ以上よくはならないという上界が探索を減らす。次回はナップサックへ戻り、最適化の枝刈りを学ぶ。


<a id="lesson10"></a>

## 第10回　貪欲法と分枝限定法――最適解を探す

### 1. 講義タイトルと到達点

すぐに良さそうな選択を確定する貪欲法と、最適性を守りながら不要な枝を切る分枝限定法を比較する。速く答えを出すことと、最適だと保証することを分けて判断する。

### 2. この回で学ぶこと

局所最適と大域最適、交換による正しさの説明、緩和問題、最大化における上界・下界、暫定最良解、分数ナップサック上界を学ぶ。第8回の全探索・DPを答え合わせに再利用する。

### 3. 前回までの復習

A*では、残り費用を過大評価しない下界を使った。今回は価値最大化なので向きが逆になる。ある枝から達成し得る価値を過小評価しない上界を作り、その上界でも既知の解に勝てない枝を捨てる。

### 4. 身近な問題からの導入

予算50で、A=(10,60)、B=(20,100)、C=(30,120)を選ぶ。重さあたりの価値は6,5,4なので、密度順の貪欲法はAとBを選び、価値160となる。しかしBとCなら予算50ちょうどで価値220だ。安い単位効果の品物を先に取っても、容量の残り方によって全体では損をする。

一方、品物を小分けにできるなら、AとBを取り、残り20だけCを取れば価値240となる。切り分けられるかどうかという条件が、同じ選択規則の正しさを変える。

### 5. アルゴリズムの原理

貪欲法は局所的な規則で選び、原則として選び直さない。最適性を示すには、その局所選択を含む最適解が必ず存在するなどの証明が必要である。分数ナップサックでは、低密度の品物を使っている部分を未使用の高密度の品物へ置き換えると、同じ重さで価値が下がらない。この交換を繰り返せば密度順の選択へ変形できる。

0-1ナップサックでは分数選択が禁止されるため、この交換はそのまま使えない。ただし、禁止を取り払った分数版の最適値は元問題の最適値以上になる。元の実行可能解はすべて緩和後でも許されるからだ。この値を上界として使う。

分枝限定法は、品物を採る枝と採らない枝へ分け、各部分問題の上界を計算する。すでに実現した価値をincumbentとして保持し、上界≤incumbentならその枝ではよりよい解を作れないので切る。最初に貪欲解を入れておくと、最初からある程度よい下界を使える。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 340" role="img" aria-labelledby="fig10-title"><title id="fig10-title">図10　分枝限定法の安全な枝刈り</title><rect width="720" height="340" fill="#fff"/><g font-family="sans-serif"><rect x="220" y="20" width="280" height="55" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="360.0" y="53.5" font-size="18" fill="#142c40" text-anchor="middle">根：下界160／上界240</text><path d="M300,75 L180,140" stroke="#526574" stroke-width="2" fill="none" /><path d="M420,75 L540,140" stroke="#526574" stroke-width="2" fill="none" /><rect x="35" y="140" width="290" height="55" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="180.0" y="173.5" font-size="18" fill="#142c40" text-anchor="middle">A採用：上界240</text><rect x="395" y="140" width="290" height="55" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="540.0" y="173.5" font-size="18" fill="#142c40" text-anchor="middle">A不採用：上界220</text><path d="M180,195 L180,255" stroke="#526574" stroke-width="2" fill="none" /><path d="M540,195 L540,255" stroke="#526574" stroke-width="2" fill="none" /><rect x="35" y="255" width="290" height="55" rx="9" fill="#fff0e7" stroke="#c76e36" stroke-width="1.5"/><text x="180.0" y="288.5" font-size="18" fill="#142c40" text-anchor="middle">B不採用：上界180 → 枝刈り</text><rect x="395" y="255" width="290" height="55" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="540.0" y="288.5" font-size="18" fill="#142c40" text-anchor="middle">B+C：価値220を発見</text></g></svg></div><figcaption>図10：上界による枝刈り</figcaption></figure>

図は、価値220の解を得た後ならA採用・B不採用の上界180を切れることを示している。実装の訪問順序そのものとは区別しよう。根の上界は240、初期の実行可能解は160。上界240が得られたからといって、価値240の0-1解があるわけではない。Aを採らない枝を調べるとB+C=220が見つかり、incumbentが更新される。その後は上界220以下の枝を調べなくてよい。

| 用語（最大化） | 意味 | 本例 |
|---|---|---:|
| 下界 | 実現可能解が保証する、最適値の下側 | 初期160、改善後220 |
| 上界 | 制約を緩めた問題などから得る上側 | 根で240 |
| 最適値 | すべての許された解の最大 | 220 |

最小化問題では上下の役割が逆になるため、「上界なら切る」とだけ暗記しない。何を最大・最小にしているかを先に確認する。

### 7. Pythonによる基本実装

価値密度と上界は`Fraction`で厳密な有理数として扱う。浮動小数点の丸めで上界をわずかに小さく見積もり、本当の最適解を切る危険を避けるためである。

**完成プログラム：lesson10_branch_bound.py**

```python
"""第10回: 分数ナップサック上界。丸め誤差を避けるFraction。"""
from fractions import Fraction
from lesson08_knapsack import Item, validate, brute_force, compressed_dp


def greedy(items: list[Item], capacity: int) -> int:
    validate(items, capacity)
    rest, value = capacity, 0
    for weight, gain in sorted(items, key=lambda item: Fraction(item[1], item[0]), reverse=True):
        if weight <= rest:
            rest -= weight
            value += gain
    return value


def branch_bound(items: list[Item], capacity: int) -> tuple[int, dict[str, int]]:
    validate(items, capacity)
    ordered = sorted(items, key=lambda item: Fraction(item[1], item[0]), reverse=True)
    incumbent = greedy(items, capacity)
    stats = {'nodes': 0, 'pruned': 0}
    def upper_bound(index: int, rest: int, value: int) -> Fraction:
        bound = Fraction(value)
        for weight, gain in ordered[index:]:
            if weight <= rest:
                rest -= weight
                bound += gain
            else:
                bound += Fraction(gain * rest, weight)
                break
        return bound
    def search(index: int, rest: int, value: int) -> None:
        nonlocal incumbent
        stats['nodes'] += 1
        incumbent = max(incumbent, value)
        if index == len(ordered):
            return
        if upper_bound(index, rest, value) <= incumbent:
            stats['pruned'] += 1
            return
        weight, gain = ordered[index]
        if weight <= rest:
            search(index+1, rest-weight, value+gain)
        search(index+1, rest, value)
    search(0, capacity, 0)
    return incumbent, stats


if __name__ == '__main__':
    items = [(10, 60), (20, 100), (30, 120)]
    result, stats = branch_bound(items, 50)
    assert result == brute_force(items, 50) == compressed_dp(items, 50) == 220
    assert greedy(items, 50) == 160
    print('greedy:', greedy(items, 50))
    print('optimal:', result, 'stats:', stats)
```

### 8. コードの実行過程

orderedは密度の高い順の品物列である。searchのindexより前の採否は確定済みで、restが残り容量、valueが採用済みの価値を表す。まずvalueでincumbentを更新する。すべての品物を処理済みならそれ以上の枝はない。

upper_boundは残りの品物を密度順に詰め、入らない最初の品物だけを分数で使って終了する。採る枝ではrestが減りvalueが増える。不採用の枝ではrestとvalueを保ったままindexだけ増える。ここでは状態を整数引数として渡すので、共有リストのpopのような復元は不要だ。

**実行結果**

```text
greedy: 160
optimal: 220 stats: {'nodes': 12, 'pruned': 1}
```

この例では枝刈りが1回起きる。小さい入力では上界計算の費用が削減できる探索量を上回ることもある。分枝限定法という名前だけから高速だと判断しない。

### 9. 改良版アルゴリズム

上界の大きい部分問題を優先度付きキューへ入れ、期待の高い枝から調べる方法もある。よい暫定解を早く得られれば、その後の枝刈りが増える可能性がある。一方、未処理の多数の部分問題を保存するためメモリ消費は増える。

貪欲法にも最適性が保証される問題はある。たとえば区間ごとの価値が同じで、重ならない区間を最大件数選ぶ問題では、終了時刻の早い区間から選ぶ規則に交換論法を適用できる。区間に異なる価値を付ければ別問題になり、同じ保証は失われる。

### 10. 計算量と適用条件

密度順の貪欲法はソート込みO(N log N)時間、ソート済み列の保存にO(N)領域。0-1版での最適性や一定の近似比を、この単純な実装には一般に保証しない。実行可能な解を速く得る発見的手法として使っている。

分枝限定法も最悪では指数時間である。本実装は各ノードで残り品物を走査して上界を計算するため、粗い上界はO(N2ᴺ)。スタックとorderedはO(N)だが、Fractionの算術費用は数値の桁数に依存する。

最適性の保証には、安全な上界、網羅的な分岐、正確な実行可能性判定、探索を必要なところまで完了することが必要だ。途中で時間切れにしたら、暫定最良解は得られても最適とは限らない。全最適解を列挙したい場合は、同値の枝を切る`<=`も見直す必要がある。

### 11. Python実習

第8回の4手法と今回の2手法へ同じ小規模入力を渡す。厳密解を返す手法は一致し、貪欲解はその値以下になることを確認する。次に上界を誤って小さくする変更を実習用コピーで行い、最適解を失う反例を作る。枝刈りは速さだけでなく正しさの一部だと実感しよう。

### 12. 練習問題

- **10-B 基礎**：本文の例で貪欲解160と分数上界240の選択内容を説明せよ。
- **10-S 標準**：最大化で上界180、現在の暫定解190なら、その枝を調べる必要があるか。上界200ならどうか。
- **10-A 発展**：全最適解を列挙する場合に`bound <= incumbent`を使えない理由を説明せよ。

### 13. 理解度確認問題

**10-Q1**：分枝限定法は必ずDPより速いか。**10-Q2**：よい貪欲解を初期値に使うと、正しさを損なうか。**10-Q3**：最適性を証明していない貪欲法を、近似比保証付きアルゴリズムと呼べるか。

### 14. まとめ

局所的な規則には、その問題固有の証明が必要である。分枝限定法は、実現した解と安全な上界を比較して探索を減らす。最悪の指数性は残るが、入力の構造が合えば多くの枝を省ける。

### 15. 次回への接続

次回は「最良の一つを探す」から「多数のランダムな状態の平均を知る」へ問いを変える。同じ計算予算でも、求める答えが推定値なら別の道具がある。


<a id="lesson11"></a>

## 第11回　確率的探索とモンテカルロ法

### 1. 講義タイトルと到達点

麻雀のランダム配牌について平均シャンテン数を推定する。各手牌のシャンテン数は厳密に計算し、配牌全体の平均はサンプリングで推定する。この二つの精度を明確に分ける。

### 2. この回で学ぶこと

一様サンプリング、非復元抽出、乱数シード、標本平均、標準誤差、近似的信頼区間を扱う。再帰・メモ化・DPを組み合わせた厳密な評価器を、確率的な実験の内側へ入れる。最適化のランダム探索と平均値のモンテカルロ推定も区別する。

### 3. 前回までの復習

第6回は通常形の完成判定、第7回は状態の再利用、第8回は部分問題の合成を学んだ。今回はすべてを使う。単に乱数を生成するだけでは、測る対象の定義や評価器の誤りは解決しない。

### 4. 身近な問題からの導入

「配牌は平均何シャンテンか」と尋ねられても、34種類の牌がどれも同じ確率で独立に13回出ると考えてはいけない。同じ牌は4枚しかなく、1枚引けば残り枚数が変わる。また、異なる牌種の組合せを一様に選ぶことも、136枚の物理牌から一様に選ぶことと違う。

本書の実験は、四人麻雀の136枚、各種4枚、門前13枚、槓・副露・抜きドラなし、配牌後の打牌前というモデルである。赤牌は通常の5と同じ種類として扱う。親の14枚配牌の平均ではない。三麻では牌集合が変わるため、この平均をそのまま使えない。

### 5. アルゴリズムの原理

136枚に0〜135の異なる番号を付け、一様に13枚を重複なしで取り出す。番号を4で整数除算すると34種類へ変換できる。各配牌内は非復元抽出だが、次の試行では136枚に戻して独立な配牌を生成するモデルである。

シャンテン数は、和了形が完成していれば−1、聴牌なら0、あと一段進める必要があれば1と数える。本書では、他家の手牌や河による牌の枯れは考えず、各種類最大4枚という牌集合の制約を含む構造的な距離を使う。通常形・七対子・国士無双のうち最小の値を全形のシャンテン数とする。

通常形について、現在の枚数をhᵢ、合法な完成形の枚数をtᵢとし、不足枚数をΣ max(0,tᵢ−hᵢ)と定める。その最小値から1を引く。13枚の聴牌なら不足1枚なので0、完成14枚なら不足0枚なので−1となる。14枚の未完成手では余分な牌を捨てながら不足を補う距離になる。外部に見えている牌による利用可能性や役の条件は含まない。

完成形を全部直接列挙すると多いので、萬子・筒子・索子・字牌ごとに「m面子とp雀頭を作る最小不足枚数」を計算し、最後に4面子1雀頭となる組合せをDPで合成する。第8回の容量の代わりに、面子数と雀頭数を状態の軸にする。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg role="img" aria-label="標本数と平均シャンテン数および近似95パーセント区間" xmlns:xlink="http://www.w3.org/1999/xlink" width="604.8pt" height="252pt" viewBox="0 0 604.8 252" xmlns="http://www.w3.org/2000/svg" version="1.1">
 
 <defs>
  <style type="text/css">*{stroke-linejoin: round; stroke-linecap: butt}</style>
 </defs>
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 252 
L 604.8 252 
L 604.8 0 
L 0 0 
z
" style="fill: #ffffff"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 52.33274 214.77226 
L 601.79976 214.77226 
L 601.79976 19.94199 
L 52.33274 19.94199 
z
" style="fill: #ffffff"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <path d="M 77.308514 214.77226 
L 77.308514 19.94199 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_2">
      <defs>
       <path id="mc1589c1fcc" d="M 0 0 
L 0 3.5 
" style="stroke: #000000; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#mc1589c1fcc" x="77.308514" y="214.77226" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="77.308514" y="230.890385" transform="rotate(-0 77.308514 230.890385)">200</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_3">
      <path d="M 282.81322 214.77226 
L 282.81322 19.94199 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_4">
      <g>
       <use xlink:href="#mc1589c1fcc" x="282.81322" y="214.77226" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="282.81322" y="230.890385" transform="rotate(-0 282.81322 230.890385)">1000</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_5">
      <path d="M 488.317927 214.77226 
L 488.317927 19.94199 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_6">
      <g>
       <use xlink:href="#mc1589c1fcc" x="488.317927" y="214.77226" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="488.317927" y="230.890385" transform="rotate(-0 488.317927 230.890385)">5000</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_7">
      <path d="M 576.823986 214.77226 
L 576.823986 19.94199 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_8">
      <g>
       <use xlink:href="#mc1589c1fcc" x="576.823986" y="214.77226" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="576.823986" y="230.890385" transform="rotate(-0 576.823986 230.890385)">10000</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_9">
      <defs>
       <path id="mdca7c640d3" d="M 0 0 
L 0 2 
" style="stroke: #000000; stroke-width: 0.6"/>
      </defs>
      <g>
       <use xlink:href="#mdca7c640d3" x="129.08124" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#mdca7c640d3" x="165.814573" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#mdca7c640d3" x="194.30716" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#mdca7c640d3" x="217.587299" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_13">
      <g>
       <use xlink:href="#mdca7c640d3" x="237.270376" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_14">
      <g>
       <use xlink:href="#mdca7c640d3" x="254.320633" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_15">
      <g>
       <use xlink:href="#mdca7c640d3" x="269.360025" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_16">
      <g>
       <use xlink:href="#mdca7c640d3" x="371.31928" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_13">
     <g id="line2d_17">
      <g>
       <use xlink:href="#mdca7c640d3" x="423.092006" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_18">
      <g>
       <use xlink:href="#mdca7c640d3" x="459.82534" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_15">
     <g id="line2d_19">
      <g>
       <use xlink:href="#mdca7c640d3" x="511.598066" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_16">
     <g id="line2d_20">
      <g>
       <use xlink:href="#mdca7c640d3" x="531.281142" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_17">
     <g id="line2d_21">
      <g>
       <use xlink:href="#mdca7c640d3" x="548.331399" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_18">
     <g id="line2d_22">
      <g>
       <use xlink:href="#mdca7c640d3" x="563.370792" y="214.77226" style="stroke: #000000; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="text_5">
     <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="327.06625" y="246.504135" transform="rotate(-0 327.06625 246.504135)">Number of samples (log scale)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_23">
      <path d="M 52.33274 210.446778 
L 601.79976 210.446778 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_24">
      <defs>
       <path id="mc366812d3f" d="M 0 0 
L -3.5 0 
" style="stroke: #000000; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#mc366812d3f" x="52.33274" y="210.446778" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: end" x="45.33274" y="215.00584" transform="rotate(-0 45.33274 215.00584)">3.45</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_25">
      <path d="M 52.33274 171.659422 
L 601.79976 171.659422 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_26">
      <g>
       <use xlink:href="#mc366812d3f" x="52.33274" y="171.659422" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: end" x="45.33274" y="176.218485" transform="rotate(-0 45.33274 176.218485)">3.50</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_27">
      <path d="M 52.33274 132.872067 
L 601.79976 132.872067 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_28">
      <g>
       <use xlink:href="#mc366812d3f" x="52.33274" y="132.872067" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: end" x="45.33274" y="137.43113" transform="rotate(-0 45.33274 137.43113)">3.55</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_29">
      <path d="M 52.33274 94.084712 
L 601.79976 94.084712 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_30">
      <g>
       <use xlink:href="#mc366812d3f" x="52.33274" y="94.084712" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: end" x="45.33274" y="98.643774" transform="rotate(-0 45.33274 98.643774)">3.60</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_31">
      <path d="M 52.33274 55.297356 
L 601.79976 55.297356 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #b0b0b0; stroke-opacity: 0.2; stroke-width: 0.8; stroke-linecap: square"/>
     </g>
     <g id="line2d_32">
      <g>
       <use xlink:href="#mc366812d3f" x="52.33274" y="55.297356" style="stroke: #000000; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: end" x="45.33274" y="59.856419" transform="rotate(-0 45.33274 59.856419)">3.65</text>
     </g>
    </g>
    <g id="text_11">
     <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: middle" x="12.118365" y="117.357125" transform="rotate(-90 12.118365 117.357125)">Shanten: all three forms</text>
    </g>
   </g>
   <g id="LineCollection_1">
    <path d="M 77.308514 205.916339 
L 77.308514 28.797911 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #147d86; stroke-width: 1.5"/>
    <path d="M 282.81322 148.741105 
L 282.81322 65.803721 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #147d86; stroke-width: 1.5"/>
    <path d="M 488.317927 115.298956 
L 488.317927 76.904353 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #147d86; stroke-width: 1.5"/>
    <path d="M 576.823986 108.377733 
L 576.823986 81.188036 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #147d86; stroke-width: 1.5"/>
   </g>
   <g id="line2d_33">
    <defs>
     <path id="mcf805b39fb" d="M 7 0 
L -7 -0 
" style="stroke: #147d86"/>
    </defs>
    <g clip-path="url(#pfde0755ada)">
     <use xlink:href="#mcf805b39fb" x="77.308514" y="205.916339" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="282.81322" y="148.741105" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="488.317927" y="115.298956" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="576.823986" y="108.377733" style="fill: #147d86; stroke: #147d86"/>
    </g>
   </g>
   <g id="line2d_34">
    <g clip-path="url(#pfde0755ada)">
     <use xlink:href="#mcf805b39fb" x="77.308514" y="28.797911" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="282.81322" y="65.803721" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="488.317927" y="76.904353" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#mcf805b39fb" x="576.823986" y="81.188036" style="fill: #147d86; stroke: #147d86"/>
    </g>
   </g>
   <g id="line2d_35">
    <path d="M 77.308514 117.357125 
L 282.81322 107.272413 
L 488.317927 96.101654 
L 576.823986 94.782884 
" clip-path="url(#pfde0755ada)" style="fill: none; stroke: #147d86; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m8fd75ee901" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #147d86"/>
    </defs>
    <g clip-path="url(#pfde0755ada)">
     <use xlink:href="#m8fd75ee901" x="77.308514" y="117.357125" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#m8fd75ee901" x="282.81322" y="107.272413" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#m8fd75ee901" x="488.317927" y="96.101654" style="fill: #147d86; stroke: #147d86"/>
     <use xlink:href="#m8fd75ee901" x="576.823986" y="94.782884" style="fill: #147d86; stroke: #147d86"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 52.33274 214.77226 
L 52.33274 19.94199 
" style="fill: none; stroke: #000000; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 601.79976 214.77226 
L 601.79976 19.94199 
" style="fill: none; stroke: #000000; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 52.33274 214.77226 
L 601.79976 214.77226 
" style="fill: none; stroke: #000000; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 52.33274 19.94199 
L 601.79976 19.94199 
" style="fill: none; stroke: #000000; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_12">
    <text style="font-weight: 700; font-size: 14.4px; font-family: 'DejaVu Sans'; text-anchor: start" x="52.33274" y="13.94199" transform="rotate(-0 52.33274 13.94199)">Four-player / 13 tiles / seed = 2026</text>
   </g>
   <g id="legend_1">
    <g id="LineCollection_2">
     <path d="M 433.677885 203.276635 
L 433.677885 191.276635 
" style="fill: none; stroke: #147d86; stroke-width: 1.5"/>
    </g>
    <g id="line2d_36">
     <g>
      <use xlink:href="#mcf805b39fb" x="433.677885" y="203.276635" style="fill: #147d86; stroke: #147d86"/>
     </g>
    </g>
    <g id="line2d_37">
     <g>
      <use xlink:href="#mcf805b39fb" x="433.677885" y="191.276635" style="fill: #147d86; stroke: #147d86"/>
     </g>
    </g>
    <g id="line2d_38">
     <path d="M 421.677885 197.276635 
L 445.677885 197.276635 
" style="fill: none; stroke: #147d86; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="line2d_39">
     <g>
      <use xlink:href="#m8fd75ee901" x="433.677885" y="197.276635" style="fill: #147d86; stroke: #147d86"/>
     </g>
    </g>
    <g id="text_13">
     <text style="font-size: 12px; font-family: 'DejaVu Sans'; text-anchor: start" x="455.277885" y="201.476635" transform="rotate(-0 455.277885 201.476635)">Mean / approx. 95% CI</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pfde0755ada">
   <rect x="52.33274" y="19.94199" width="549.46702" height="194.83027"/>
  </clipPath>
 </defs>
</svg>
</div><figcaption>図11：標本平均と近似95%区間（同一seedの累積標本）</figcaption></figure>

図は実測した標本平均の変化を示す。標本数を増やしても、推定値が真値へ毎回単調に近づくわけではない。揺れの典型的な幅が小さくなる、というのが収束の意味である。

通常形の色別計算も手で追おう。順子123を数えると、1で順子を始めた時点で2と3に一枚ずつ必要となる。needの`carry`は現在の番号に既に必要な枚数、`next_carry`は次の番号に既に必要な枚数だ。新しくs個の順子を始めると、現在にもs枚、次にもs枚、その次にもs枚が追加される。

| 現在の番号 | 既存carry | 新しく始める順子 | 現在の目標枚数 | 次の(carry,next_carry) |
|---|---:|---:|---:|---|
| 1 | 0 | 1 | 1 | (1,1) |
| 2 | 1 | 0 | 1 | (1,0) |
| 3 | 1 | 0 | 1 | (0,0) |

刻子なら同じ番号へ3枚、雀頭なら2枚を追加する。目標枚数が4を超える分岐は除く。8や9から順子を始める分岐、字牌で順子を作る分岐も禁止する。この仕組みにより、たとえば東4枚を「東の刻子と東の雀頭まであと1枚」と評価して、存在しない5枚目を要求する誤りを避ける。

### 7. Pythonによる基本実装

やや長いが、新しい中心概念は乱数と誤差であり、評価器は既習の状態設計・再帰・DPの合成である。90分授業では、dealとestimateを必修実装、色別評価器の詳細な再実装を事前・事後課題とする。独学ではcarry表を追ってからコードへ進むとよい。

**完成プログラム：lesson11_monte_carlo.py**

```python
"""第11回: 四人麻雀、門前13/14枚。完成形への不足枚数から厳密に計算。"""
from functools import cache, lru_cache
from random import Random
from statistics import mean, stdev
from math import sqrt
from lesson06_mahjong import Counts, tiles, validate_counts
INF = 99
ORPHANS = (0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33)


@lru_cache(maxsize=20000)
def group_costs(hand: tuple[int, ...], suited: bool) -> tuple[int, ...]:
    """cost[2*m+p]: この色にm面子p雀頭を置く完成形までの最小不足枚数。"""
    @cache
    def need(rank: int, carry: int, next_carry: int, melds: int, pair: int) -> int:
        if rank == len(hand):
            return 0 if (carry, next_carry, melds, pair) == (0, 0, 0, 0) else INF
        answer = INF
        max_sequences = melds if suited and rank <= len(hand)-3 else 0
        for sequences in range(max_sequences+1):
            for triplet in range(min(1, melds-sequences)+1):
                for head in range(pair+1):
                    target = carry + sequences + 3*triplet + 2*head
                    if target > 4:
                        continue  # 存在しない5枚目を要求する完成形を除外
                    missing = max(0, target-hand[rank])
                    suffix = need(rank+1, next_carry+sequences, sequences,
                                  melds-sequences-triplet, pair-head)
                    answer = min(answer, missing+suffix)
        return answer
    return tuple(need(0, 0, 0, melds, pair) for melds in range(5) for pair in range(2))


def normal_shanten(counts: Counts) -> int:
    validate_hand(counts)
    groups = [(counts[0:9], True), (counts[9:18], True),
              (counts[18:27], True), (counts[27:34], False)]
    dp = {(0, 0): 0}
    for hand, suited in groups:
        costs = group_costs(hand, suited)
        new_dp: dict[tuple[int, int], int] = {}
        for (used_melds, used_pair), cost in dp.items():
            for melds in range(5-used_melds):
                for pair in range(2-used_pair):
                    state = (used_melds+melds, used_pair+pair)
                    candidate = cost + costs[2*melds+pair]
                    new_dp[state] = min(new_dp.get(state, INF), candidate)
        dp = new_dp
    return dp[4, 1] - 1


def validate_hand(counts: Counts) -> None:
    validate_counts(counts)
    if sum(counts) not in (13, 14):
        raise ValueError('closed 13 or 14 tiles required')


def special_shanten(counts: Counts) -> tuple[int, int]:
    validate_hand(counts)
    pairs = sum(n >= 2 for n in counts)
    kinds = sum(n > 0 for n in counts)
    chiitoitsu = 6 - pairs + max(0, 7-kinds)
    unique_orphans = sum(counts[i] > 0 for i in ORPHANS)
    orphan_pair = any(counts[i] >= 2 for i in ORPHANS)
    kokushi = 13 - unique_orphans - int(orphan_pair)
    return chiitoitsu, kokushi


def shanten(counts: Counts, all_forms: bool = True) -> int:
    normal = normal_shanten(counts)
    return min(normal, *special_shanten(counts)) if all_forms else normal


def deal(rng: Random, size: int = 13) -> Counts:
    if size not in (13, 14):
        raise ValueError('13 or 14 required')
    physical_tiles = rng.sample(range(136), size)
    counts = [0] * 34
    for physical in physical_tiles:
        counts[physical // 4] += 1
    return tuple(counts)


def estimate(samples: int, seed: int = 2026) -> dict[str, float | int]:
    if samples < 2:
        raise ValueError('at least 2 samples required')
    rng = Random(seed)
    normal_values, all_values = [], []
    for _ in range(samples):
        hand = deal(rng)
        normal = normal_shanten(hand)
        normal_values.append(normal)
        all_values.append(min(normal, *special_shanten(hand)))
    standard_error = stdev(all_values) / sqrt(samples)
    return {'n': samples, 'normal_mean': mean(normal_values),
            'all_mean': mean(all_values), 'se': standard_error,
            'low95': mean(all_values)-1.96*standard_error,
            'high95': mean(all_values)+1.96*standard_error}


if __name__ == '__main__':
    assert shanten(tiles(man='123456789', pin='123', honors='11')) == -1
    assert shanten(tiles(man='123456789', pin='123', honors='1')) == 0
    assert special_shanten(tiles(man='1122', pin='3344', sou='5566', honors='1'))[0] == 0
    assert special_shanten(tiles(man='19', pin='19', sou='19', honors='1234567'))[1] == 0
    result = estimate(200)
    print('four-player, closed 13 tiles, seed=2026')
    for key, value in result.items():
        print(f'{key}: {value:.6f}' if isinstance(value, float) else f'{key}: {value}')
```

### 8. コードの実行過程

`group_costs`の内側のneedは、番号rankを一つずつ増やしながら、残りの面子数と雀頭数を減らす。最後の番号を越えたとき、carryも残りの面子・雀頭もすべて0なら成功で、不足枚数0を返す。不成立の終端は大きな値INFを返し、最小化の候補から事実上除外する。合法な完成形の不足は最大14なので99で十分だ。

`target`はその牌種を完成形で何枚使うか、`missing`は手持ちから不足する分だけである。余っている牌に負の費用は付けない。余分を持っていることが、別の牌の不足を打ち消してしまうのを防ぐためだ。次の状態へ持ち越すのは順子の要求枚数だけで、刻子と雀頭はその番号で完結する。

色別の結果は10個の値である。面子数0〜4の5通りと雀頭数0〜1の2通りを、添字`2*melds+pair`へ平らに格納する。normal_shantenのdpは、処理済みの色について使った面子数・雀頭数ごとの最小不足を保持し、新しい色の表を足し合わせる。最後にdp[4,1]だけを読む。

七対子は`6−対子種類数+max(0,7−牌種数)`、国士無双は`13−么九牌種類数−対子の有無`で求める。同じ牌4枚は七対子の2対子にはしない。通常形と特殊形の最小値を使うため、全形平均は通常形だけの平均以下になる。

**実行結果**

```text
four-player, closed 13 tiles, seed=2026
n: 200
normal_mean: 3.780000
all_mean: 3.570000
se: 0.058245
low95: 3.455840
high95: 3.684160
```

これは200標本の実行例であり、母平均の確定値ではない。より大きい標本の実測値は本章末の実験記録表に示す。乱数生成の実装が変わる場合には、同じseedだけで異なるPython版との完全一致を保証しない。

### 9. 改良版アルゴリズム

内側の厳密評価を速くすれば、同じ時間に多くの標本を評価できる。色別の手牌タプルが同じなら結果も同じなので、group_costsを上限付きでキャッシュする。各手牌の評価を近似へ変えるより、既知の正しさを保持したまま試行回数を増やせる。

ランダム探索による最適化なら、無作為に活動の選択や順番を作り、実行可能なもののうち最もよい値を保存する。これは平均の推定とは違う。最良値は標本を増やすと悪化しないが、何回試せば大域最適に到達するかは別途議論が必要で、平均値の信頼区間を最良値にそのまま付けられない。

### 10. 計算量と適用条件

標本数をn、一手の厳密評価費用をCとすれば時間O(nC)。平均・分散は逐次更新すればO(1)領域で計算できるが、本実装は学習のため全標本値を保存しO(n)領域を使う。色別の有限状態DPでは、訪れた状態数S、各状態の候補数Bに対してO(SB)となる。牌種数34、面子数4が固定なので、この実験に対してCは有限の定数だが、実測コストとしては支配的である。

独立同分布の標本で標準偏差をsとすると、平均の標準誤差はs/√nと推定する。約95%の区間として平均±1.96s/√nを表示する。これは中心極限定理に基づく大標本近似であり、有限標本で厳密な95%を保証する区間ではない。毎回この手順で区間を作ると、長期的に約95%が真の平均を覆うという意味である。

誤差の典型幅を半分にするには標本数を約4倍にする必要がある。評価器の系統誤差や偏った抽出方法は、標本数を増やしても消えない。ランダムに取ったつもりという感覚より、何を一様に取ったかを検証することが重要だ。

### 11. Python実習

まず完成形・聴牌・七対子・国士・同種4枚のテストを通す。次にn=200,1000,5000,10000へ増やし、平均と標準誤差を記録する。標本数だけでなく、13枚か14枚か、通常形だけか全形か、seedはいくつかも必ず記載する。

| 標本数 | 通常形平均 | 全形平均 | 全形の標準誤差 | 全形平均の近似95%区間 |
|---:|---:|---:|---:|---|
| 200 | 3.7800 | 3.5700 | 0.05824 | 3.4558〜3.6842 |
| 1,000 | 3.7700 | 3.5830 | 0.02727 | 3.5295〜3.6365 |
| 5,000 | 3.7904 | 3.5974 | 0.01263 | 3.5727〜3.6221 |
| 10,000 | 3.7970 | 3.5991 | 0.00894 | 3.5816〜3.6166 |


掲載値は同じseedで先頭から増やした標本列なので、行どうしは独立ではない。複数の独立な実験を比較したければseedを変えて繰り返す。今回の評価器は別方式の一色完成形列挙と照合し、さらに外部のmahjong 1.4.0とランダム13枚1000手・14枚1000手で照合した。全手牌を尽くした検証ではない。

### 12. 練習問題

- **11-B 基礎**：標本数を2500から10000へ増やすと、標準誤差はおおむね何倍になるか。
- **11-S 標準**：`randrange(34)`を13回呼ぶ方法で配牌を作ると、どの制約を破るか。牌種別枚数ベクトルを一様に選ぶ方法も不適切な理由を述べよ。
- **11-A 発展**：三麻へ拡張するとき、配牌生成と通常形の完成候補生成の両方で何を変えるか。抜きドラや配牌枚数もモデルとして決めよ。

### 13. 理解度確認問題

**11-Q1**：各手牌のシャンテン数が厳密なら、200手の平均も母平均と厳密に一致するか。**11-Q2**：信頼区間は「個々の配牌の95%が入る範囲」か。**11-Q3**：モンテカルロ法は常に最適解探索を意味するか。

### 14. まとめ

何をランダムに選び、何を測定するかを固定して初めて平均が意味を持つ。厳密な内側の評価と確率的な外側の推定は両立する。誤差は数字として示し、モデル誤差とサンプリング誤差を分ける。

### 15. 次回への接続

最後は、活動の選択と実行順序を同時に扱う。正しいモデル、厳密解、速い発見的解、計算量、検証を一つのプロジェクトへまとめる。


<a id="lesson12"></a>

## 第12回　総合演習――人生の壺をアルゴリズムで解く

### 1. 講義タイトルと到達点

限られた一日の時間へ、学習・応募・運動・趣味を配置する。活動を選ぶだけでなく、期限と先行関係を守って順序を決める。これまでの探索手法を、モデルの条件に応じて選ぶ総合演習である。

### 2. この回で学ぶこと

選択と順序の違い、時間窓、先行関係、一資源スケジューリング、バックトラック、分枝限定法、貪欲法の比較を行う。最適解の価値だけでなく、いつ何を行うかという実行可能な予定表を出力する。

### 3. 前回までの復習

ナップサックでは重さと価値の和だけを考え、並べる順序は無関係だった。今回も全活動を好きな時刻に行えて、段取り時間もなければ、時間を容量とするナップサックに戻る。期限・開始可能時刻・先行関係などを追加したことで、順序の探索が必要になる。

### 4. 身近な問題からの導入

「壺に大きな石、小石、砂をどう入れるか」という寓話を、人生の時間配分へ読み替える。ただし実際の三次元充填では、物体の形、姿勢、空隙、投入経路、摩擦などが重要になる。本章のプログラムは三次元の壺を詰めるものではない。一本の時間軸上へ、途中で分割しない活動を配置するモデルである。

業界を選ぶ、住みたい地域を決める、会社へ応募する、必要なスキルを身につけるという計画も、単に項目を選ぶだけでは完了しない。応募前に学習が必要なら順序に制約がある。ただし実際の人生では価値や機会も変化する。本モデルの目的は人生の正解を算出することではなく、どの仮定が結論を左右するかを見えるようにすることだ。

### 5. アルゴリズムの原理

一人が同時に一つの活動を行う。活動ごとに所要時間・価値・開始可能時刻release・完了期限deadlineを与える。必要な先行活動がすべて終了していれば実行候補になる。活動は一度だけ、途中で中断せずに実行する。任意の活動を省略してよいが、選んだ活動の前提は省略できない。

探索状態は、選択済み活動の集合、現在時刻、直前の活動、累積価値である。未選択で前提を満たす活動を一つ選び、開始可能時刻まで必要なら待ち、完了が期限と全体の時間枠内なら再帰する。各状態で「ここで終える」ことも可能なので、累積価値を毎回最良値と比較する。

段取り時間は直前と次の活動の組に依存する非負整数とする。本モデルでは、直前活動が終わったら段取りを行え、次の活動のrelease前に段取りだけ済ませてよい。この仮定の下で開始は`max(現在時刻+段取り時間, release)`となる。段取り自体もrelease以後にしかできないモデルなら式を変更する必要がある。

### 6. 図解・手計算による説明

<figure class="diagram"><div class="figure-scroll"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 310" role="img" aria-labelledby="fig12-title"><title id="fig12-title">図12　期限と前提を守る時間配置</title><rect width="720" height="310" fill="#fff"/><g font-family="sans-serif"><path d="M140,80 L140,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="140" y="65" font-size="18" fill="#142c40" text-anchor="middle">0</text><path d="M220,80 L220,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="220" y="65" font-size="18" fill="#142c40" text-anchor="middle">1</text><path d="M300,80 L300,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="300" y="65" font-size="18" fill="#142c40" text-anchor="middle">2</text><path d="M380,80 L380,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="380" y="65" font-size="18" fill="#142c40" text-anchor="middle">3</text><path d="M460,80 L460,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="460" y="65" font-size="18" fill="#142c40" text-anchor="middle">4</text><path d="M540,80 L540,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="540" y="65" font-size="18" fill="#142c40" text-anchor="middle">5</text><path d="M620,80 L620,265" stroke="#d9e1e6" stroke-width="2" fill="none" /><text x="620" y="65" font-size="18" fill="#142c40" text-anchor="middle">6</text><text x="70" y="135" font-size="20" fill="#142c40" text-anchor="middle">最適</text><text x="70" y="220" font-size="20" fill="#142c40" text-anchor="middle">貪欲</text><rect x="140" y="100" width="160" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="220.0" y="131.0" font-size="18" fill="#142c40" text-anchor="middle">C：価値5</text><rect x="300" y="100" width="160" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="380.0" y="131.0" font-size="18" fill="#142c40" text-anchor="middle">A：価値2</text><rect x="460" y="100" width="80" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="500.0" y="131.0" font-size="18" fill="#142c40" text-anchor="middle">B：8</text><rect x="140" y="190" width="160" height="50" rx="9" fill="#edf6f5" stroke="#147d86" stroke-width="1.5"/><text x="220.0" y="221.0" font-size="18" fill="#142c40" text-anchor="middle">C：価値5</text><rect x="300" y="190" width="240" height="50" rx="9" fill="#fff0e7" stroke="#c76e36" stroke-width="1.5"/><text x="420.0" y="221.0" font-size="18" fill="#142c40" text-anchor="middle">D：価値4</text><text x="360" y="295" font-size="20" fill="#142c40" text-anchor="middle">最適：C→A→B = 15 ／ 貪欲：C→D = 9</text></g></svg></div><figcaption>図12：活動の順序と期限</figcaption></figure>

| 活動 | 時間 | 価値 | 時間窓 | 前提 |
|---|---:|---:|---|---|
| A-study 学習 | 2 | 2 | 0〜6 | なし |
| B-apply 応募 | 1 | 8 | 0〜6 | A終了 |
| C-exercise 運動 | 2 | 5 | 0〜2 | なし |
| D-hobby 趣味 | 3 | 4 | 0〜6 | なし |

容量は6。密度順の貪欲法は、実行可能な中でCを選び、次にDを選ぶので価値9となる。Aの価値密度は低いが、Aを行うことで高価値のBが可能になる。C→A→Bなら時間5、価値15である。価値を単体で評価した選択規則が、前提を解放する効果を見落としている。

### 7. Pythonによる基本実装

`Activity`は活動のデータをひとまとめにするクラスであり、dataclassが初期化処理を作る。`frozen=True`により活動の属性を探索途中で書き換えない。探索によって変わる状態はpathとchosen、引数のtime,last,valueに分離する。

**完成プログラム：lesson12_final_project.py**

```python
"""第12回: 一資源・非中断活動。時間窓、先行関係、順序依存の段取り。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Activity:
    name: str
    duration: int
    value: int
    release: int
    deadline: int
    prerequisites: tuple[str, ...] = ()


def validate(activities: list[Activity], horizon: int, setup: dict[tuple[str, str], int]) -> None:
    names = {a.name for a in activities}
    if len(names) != len(activities) or type(horizon) is not int or horizon < 0:
        raise ValueError('unique names and nonnegative horizon required')
    for a in activities:
        if (any(type(x) is not int for x in (a.duration, a.value, a.release, a.deadline))
            or a.duration <= 0 or a.value < 0 or a.release < 0 or a.deadline < a.release
            or any(p not in names for p in a.prerequisites)):
            raise ValueError('invalid activity')
    if any(type(v) is not int or v < 0 or a not in names or b not in names
           for (a, b), v in setup.items()):
        raise ValueError('invalid setup')
    # 先行関係の循環を検出
    done: set[str] = set()
    while len(done) < len(names):
        ready = {a.name for a in activities if a.name not in done and set(a.prerequisites) <= done}
        if not ready:
            raise ValueError('cyclic prerequisites')
        done.update(ready)


def optimize(activities: list[Activity], horizon: int,
             setup: dict[tuple[str, str], int] | None = None,
             use_bound: bool = True) -> tuple[int, list[tuple[str, int, int]], dict[str, int]]:
    setup = {} if setup is None else setup
    validate(activities, horizon, setup)
    best_value, best_path = 0, []
    stats = {'nodes': 0, 'pruned': 0}
    path: list[tuple[str, int, int]] = []
    chosen: set[str] = set()
    def visit(time: int, last: str, value: int) -> None:
        nonlocal best_value, best_path
        stats['nodes'] += 1
        if value > best_value:
            best_value, best_path = value, path.copy()
        if use_bound:
            # 時間窓・先行関係・段取りを緩和した安全な上界。
            remaining = [a for a in activities if a.name not in chosen]
            room = horizon-time
            # 残り時間を各活動へ分数配分する分数ナップサック上界
            from fractions import Fraction
            bound = Fraction(value)
            for a in sorted(remaining, key=lambda a: Fraction(a.value, a.duration), reverse=True):
                take = min(room, a.duration)
                bound += Fraction(a.value*take, a.duration)
                room -= take
                if room == 0:
                    break
            if bound <= best_value:
                stats['pruned'] += 1
                return
        for a in activities:
            if a.name in chosen or not set(a.prerequisites) <= chosen:
                continue
            # 段取りは直前活動終了後に行い、release前に済ませてよいモデル
            start = max(time + setup.get((last, a.name), 0), a.release)
            finish = start + a.duration
            if finish > min(horizon, a.deadline):
                continue
            chosen.add(a.name)
            path.append((a.name, start, finish))
            visit(finish, a.name, value+a.value)
            path.pop()
            chosen.remove(a.name)
    visit(0, '', 0)
    return best_value, best_path, stats


def greedy_schedule(activities: list[Activity], horizon: int) -> tuple[int, list[str]]:
    """段取りなしの比較用。入れられる中で価値/時間が最大のものを次に置く。"""
    from fractions import Fraction
    validate(activities, horizon, {})
    chosen: set[str] = set()
    time, value, order = 0, 0, []
    while True:
        available = [a for a in activities if a.name not in chosen
                     and set(a.prerequisites) <= chosen
                     and max(time, a.release)+a.duration <= min(horizon, a.deadline)]
        if not available:
            return value, order
        activity = max(available, key=lambda a: Fraction(a.value, a.duration))
        time = max(time, activity.release)+activity.duration
        value += activity.value
        chosen.add(activity.name)
        order.append(activity.name)


ACTIVITIES = [Activity('A-study', 2, 2, 0, 6),
              Activity('B-apply', 1, 8, 0, 6, ('A-study',)),
              Activity('C-exercise', 2, 5, 0, 2),
              Activity('D-hobby', 3, 4, 0, 6)]
if __name__ == '__main__':
    exact = optimize(ACTIVITIES, 6, use_bound=False)
    bounded = optimize(ACTIVITIES, 6)
    assert exact[0] == bounded[0] == 15
    print('greedy:', greedy_schedule(ACTIVITIES, 6))
    print('backtrack:', exact)
    print('branch-bound:', bounded)
```

### 8. コードの実行過程

最初はchosenが空なのでBは候補にならない。Aから始める枝ではCの期限に間に合わなくなるが、探索はその枝だけで終了せず、Aをchosenから外してCから始める枝も調べる。Cの終了時刻2からAを実行し、時刻4でBが候補になる。Bを終える時刻5で価値15を記録する。

`best_path=path.copy()`が必要なのは、pathがこの後もpopされるからだ。最良経路をpathそのものへの参照として保存すると、最後には探索途中の状態または空のリストになってしまう。第3回の全列挙で学んだ可変オブジェクトの保存と同じ問題である。

先行関係の循環は入力検査で拒否する。Aの前にB、Bの前にAという指定では実行開始できない。本教材は先行関係全体をDAGに限定する契約であり、循環に含まれる任意活動だけを捨てる前処理は実装していない。

**実行結果**

```text
greedy: (9, ['C-exercise', 'D-hobby'])
backtrack: (15, [('C-exercise', 0, 2), ('A-study', 2, 4), ('B-apply', 4, 5)], {'nodes': 13, 'pruned': 0})
branch-bound: (15, [('C-exercise', 0, 2), ('A-study', 2, 4), ('B-apply', 4, 5)], {'nodes': 11, 'pruned': 3})
```

### 9. 改良版アルゴリズム

分枝限定版では、未選択活動の時間窓・先行関係・段取りをすべて無視し、活動を分割して採れると仮定した分数ナップサックの上界を作る。元より自由な問題なので、その最適値は元のどの継続案以上になる。これでも現在の最良値を超えないなら、枝を安全に切れる。

同じ順序に対し、より遅く開始する予定を列挙しないのはなぜか。本モデルでは価値は時刻によらず、段取りは直前の活動だけで決まり、制約は開始下限と完了上限である。同じ順序なら各活動を最も早く実行しても後続を不利にしない。したがって早い配置が遅い配置を支配し、順序だけを列挙すれば十分になる。夜に行うと価値が増えるなどの条件を加えた場合、この省略は成立しない。

### 10. 計算量と適用条件

N活動の部分順列はΣₖ₌₀ᴺ N!/(N−k)!通りで、O(N!)の規模になる。各ノードで候補を走査し、分枝限定版では上界用のソートも行うので、この実装の粗い時間上界はO(N log N・N!)。先行関係や期限は実際の分岐を減らすが、最悪の階乗的増加を消すわけではない。

探索スタックとpathはO(N)。実装は各再帰で未選択活動のリストを保持するため、上界計算中のリストを含むピーク作業領域は粗くO(N²)と評価できる。反復順やデータ構造を改善する余地はある。

時刻を離散化し、活動集合をビットマスクにすれば、subset DPやメモ化を検討できる。ただし選択集合だけでは、現在時刻や直前活動に依存する残りの可能性を区別できない。正規化によって消してよい情報か、未来に影響する情報かをまず確認する。

### 11. Python実習

最初は段取りなしで、貪欲法・バックトラック・分枝限定法を実行し、厳密法の価値が一致することを確認する。次にC→Aの段取りを1にし、同じ順序が時刻6までに終わることを確認する。2にすればC→A→Bは時間枠を超え、最適選択が変わる。

次に自分の活動を5件だけモデル化する。価値を一つの数へ置くことに違和感があれば、その違和感も仕様として書く。「運動は必須」「学習は最低2時間」のような制約へ変える方が適切な場合がある。ただし必須制約は完成コードに含まれないので、終端の実行可能性判定を追加する必要がある。

最後に、返された順序を独立に検算する。重なりなし、release以上、deadline以下、前提完了、時間枠内、同一活動の重複なし、価値合計の一致を調べる。アルゴリズムの出力を、別の簡単な検証器で検査する設計を習慣にしよう。

### 12. 練習問題

- **12-B 基礎**：C→A→Bの開始・完了時刻と価値を求めよ。
- **12-S 標準**：release・deadline・前提・段取りがすべてない場合、どの既習問題へ戻るか。
- **12-A 発展**：選択済み集合だけをキーにしたメモ化が誤る例を、順序依存の段取りを使って作れ。

### 13. 理解度確認問題

**12-Q1**：このプログラムは本物の石の三次元充填を解いているか。**12-Q2**：時間窓を無視した上界が、実際には不可能な予定の価値を含んでいてもよいか。**12-Q3**：最適解という言葉は、現実の人生でも最良であることを保証するか。

### 14. まとめ

モデルが変われば、必要な状態と保証も変わる。容量だけの選択ならナップサック、順序と期限があればスケジューリングになる。小規模の厳密解を基準に、発見的な方法と計算量を比較することができる。

### 15. 次の学習への接続

今後は、制約プログラミング、整数計画、局所探索、確率モデル、ゲーム木探索へ進める。道具を増やす前に、今回の問いを繰り返そう。候補は何か、何を保証したいか、未来を決める状態は何か、正しい答えをどう確かめるか。この四つが、未知の問題へ探索を持ち込む出発点になる。


<a id="answers"></a>

## 巻末解答と詳しい解説

答えを読む前に、結果の予想とその根拠を書こう。プログラムが出した値だけでなく、「どの条件ならその答えが保証されるか」まで述べられれば、この講義の目標へ近づいている。

### 第1回の解答

**1-B**：4の最初の添字は0。7は末尾なので4回比較する。同じ4が後ろにあっても、最初の一致を返す契約では関係しない。

**1-S**：左から最後まで走査し、一致するたびに答えの添字を上書きする方法と、右から走査して最初の一致を返す方法がある。どちらも最悪O(N)、補助領域O(1)。右からの走査は末尾付近に一致があれば早く終了する。左からの走査は全要素を確認するが、同時に件数などの集計を行いやすい。いずれも不在時の値をNoneとして初期化・返却する。

**1-A**：順序を区別せず異なる2件を選ぶ数はN(N−1)/2。順序を区別すればN(N−1)である。いずれもΘ(N²)だが、実際の候補数は2倍違う。Big-Oで同じだから同じ作業量というわけではない。

**1-Q1**：最初の答えを保持するなら正しさは変わらないが、早期終了できる利点を失う。一致ごとに上書きすると「最後の位置」を返す別の関数になる。**1-Q2**：言えない。定数倍、入力サイズ、実装・機器・データ分布で実時間は変わる。漸近的な増え方と個別実行の秒数は別である。

### 第2回の解答

**2-B**：target=3では(左,右)が(0,4)→(0,2)→(0,1)→(1,1)となり答え1。target=9では(0,4)→(3,4)→(4,4)となり答え4。後者は「末尾の8が答え」ではなく、配列の範囲内に9以上がないことを表す。

**2-S**：`values[index] > target`を判定にする。これをupper_boundと呼ぶと、targetの個数はupper_bound−lower_boundである。値が存在しなければ二つの位置が等しく、差は0。全要素同じ場合にも、左端0と右端Nとの差を正しく求められる。

**2-A**：left=0,right=1ではmiddle=0。偽のときleft=middleとしても0のままで、区間が縮まらない。middle+1ならleft=1となって終了する。「中央が偽なので中央を候補から除く」という意味を、更新式へ正しく反映する必要がある。

**2-Q1**：たまたま正しい結果はあり得るが、どの半分にも答えがないという根拠がないので保証できない。テストの成功は前提の証明の代わりにならない。**2-Q2**：要素を読むのはleft<rightの反復だけであり、middleは必ずright未満になる。rightそのものを配列添字として読まない。

### 第3回の解答

**3-B**：長さ0の文字列は空文字列という一つの解である。`['']`は解が一件、`[]`は解が一件もないことを表す。この区別は再帰のベースケースや組合せ数の初期値に繰り返し現れる。

**3-S**：forの候補を`'012'`に変える。各桁で3通りなので葉は3ᴺ個。各葉で長さNの文字列を作るため時間O(N3ᴺ)、出力領域O(N3ᴺ)、探索中の領域O(N)。再帰の深さは候補の数ではなく桁数Nである。

**3-A**：成功時にTrueで上へ抜けず、indexが末尾でtotalがtargetならpath.copy()を結果へ追加する。採用枝から戻ったら成功・失敗に関係なくpopし、不採用枝も調べる。入力[2,2]で和2なら、最初の位置を採る解と後の位置を採る解がある。位置を区別するなら添字を保存し、値の組合せを同一視するならソート済みタプル等で結果を正規化する。ただし集合で重複を除くことは、重複探索自体の削減ではない。

**3-Q1**：呼び出し式を評価し終え、その式を含む文の残りまたは次の文へ進む。`if visit():`なら、まず返り値でifの分岐を決める。**3-Q2**：違う。printは画面へ表示するだけで、関数の成功を呼び出し元へ返さない。**3-Q3**：不要。探索中の一経路と保留された呼び出しだけを保持する実装が可能である。

### 第4回の解答

**4-B**：経路は開始点一つ、移動回数は0。経路の頂点数から1を引いて辺数を得る。到達不能を表すNoneと混同しない。

**4-S**：A→B→C→Aという循環をたどると、前に来たAでも再び再帰する。探索を打ち切る条件がなく、Pythonではやがて再帰深さの例外になる。発見時に訪問済みへ登録すれば、同じ頂点への再帰を防げる。

**4-A**：BFSは1辺のS→Gを選ぶが費用10。最小費用は2辺のS→A→Gで2。BFSが誤った最短手数を答えたのではなく、求めたい最短費用とBFSの保証する尺度が一致していない。

**4-Q1**：残らない。スタックでは一方の枝を深く進み、別の浅い経路を後回しにし得る。**4-Q2**：None。開始点＝ゴールの正常な経路は要素一つであり、到達不能と明確に分かれる。

### 第5回の解答

**5-B**：空欄なしはchosenがNoneのままなのでTrue。候補なしは空リストのforが一度も回らずFalse。候補一つは一度仮置きして子を呼び、成功なら残し、失敗なら0へ戻してFalseとなる。

**5-S**：完成時に盤面を行ごとコピーして結果へ追加する。成功を返して上の探索を終える処理をなくし、各候補の子探索が終わるたびに必ず0へ戻す。2解まで欲しいなどの打ち切り条件を入れるなら、終了してよい理由を別途伝播させる必要がある。

**5-A**：各行をcopyした実行前の盤面を保存し、呼び出し後の入力盤面がそれと等しいかを確認する。`board.copy()`だけだと外側のリストしか複製されず、内側の行は共有される。そのため一方のboard[r][c]を書き換えると比較用の行も変わり、変更を検出できなくなる。

**5-Q1**：近似していない。候補を選ぶ順序を変えるだけで、各候補は失敗しない限り必要な範囲を探索する。**5-Q2**：不要。子は子が置いた分を復元し、親は自分が置いた一マスを戻す。初期状態へ全部戻すと、さらに上の仮定まで壊れる。**5-Q3**：必ずしもそうではない。候補数、矛盾の出る深さ、探索順序などが影響する。

### 第6回の解答

**6-B**：index<27は字牌を順子にしない条件。index%9<=6は各色の1〜7だけを順子の開始牌にする条件であり、8,9や色の境界をまたぐ偽の順子を防ぐ。

**6-S**：34種類中、枚数が2の種類がちょうど7種類あり、それ以外は0であれば完成七対子である。入力14枚・各4枚までの検査を先に行う。同じ牌4枚を2対子に数えない。枚数が2以上の種類を数えるシャンテン式と、完成形の判定条件を混同しないこと。

**6-A**：111を先に取ってから222を取る経路と、その逆の経路が同じ残り牌になる。4個の異なる面子では、その選択順だけでも最大4!通りの重複があり得る。最小の残り牌を使う方式は、この順序の重複を大幅に避ける。なお、牌の共有の仕方による本当の別分解まで消してはいけない。

**6-Q1**：できない。役、フリテン、誰の番かなどの条件は別である。**6-Q2**：なくならない。setは保存された結果の重複を除くが、その結果へ至る計算が実行済みかどうかは管理していない。**6-Q3**：兄弟の分岐や別の雀頭候補を、同じ入力状態から試す必要があるからである。

### 第7回の解答

**7-B**：キャッシュが残っていれば保存済みのF(5)を返し、その本体は再実行しない。clearした場合や上限付きキャッシュから追い出された場合は別である。

**7-S**：引数なしのsearchでは全呼び出しが同じ空のキーになる。しかし共有boardは毎回違い、答えも違う。盤面全体など未来を決める情報を不変なキーへ含めなければいけない。さらに「成功時に盤面を変更して解を残す」という副作用は、boolのキャッシュだけでは再現できない。

**7-A**：牌を並びで表すと123123と112233は異なるキーになるが、面子判定では同じ問題である。枚数表現にすれば同じタプルに正規化され、共有できる。一方、牌の取得順が問題の条件に影響する別のモデルなら、その情報を消すと誤る。

**7-Q1**：必ずしも多項式にならない。部分集合を状態にすれば、異なる状態だけで2ᴺ個ある。**7-Q2**：関数本体が再実行されないので、表示や外部状態の更新などが繰り返されなくなる。**7-Q3**：一解が早く見つかったり、同じ状態へ到達する枝がなかったりすればヒットは発生しない。

### 第8回の解答

**8-B**：A+Bは重さ5で入らない。B単体の価値4が最適。Cはこの設問の品物に含まれていないので、本文の3件例と混同しない。

**8-S**：同じ品物を何度でも採れる無制限ナップサックの更新になる。小さい容量を今回の品物で更新した値を再利用するので、複数回の採用が表現される。重さが正なら参照する容量が小さくなり、順序が成立する。重さ0・価値正を無制限に採れる問題は価値が無限大であり、この表だけで通常の有限最適値として扱えない。

**8-A**：容量0だけを価値0、正の容量は到達不能を表す−∞などに初期化する。遷移で到達不能から価値を足して有効な状態にしないよう注意する。すべて0にすると、容量を使っていない状態まで「ちょうど使えた」と誤認する。

**8-Q1**：同じ容量でも、使える品物が違えば最適値が違うからである。**8-Q2**：Wが巨大なら状態数も巨大で、擬多項式時間の限界がある。**8-Q3**：メモ化再帰はトップダウン型DPの代表的な実装であり、同じ部分問題の再利用という考え方を共有する。

### 第9回の解答

**9-B**：AからGを初めて発見したときの費用9。まだB経由の5を調べていないので、発見だけで終了してはいけない。

**9-S**：辺重みが非負なら、0は真の残り費用以下であり、0≤w+0も成立する。ゴールのhも0なので条件を満たす。負辺や負閉路を許す問題へ、そのままこの説明を拡張しない。

**9-A**：SからAへg=3,f=3、Bへg=1,f=4を登録する。Aを先に展開しGへ5を登録する。次にBを展開するとAへ2で到達できるため、Aを再登録する。再展開されたAからGは4へ改善される。最初のAの展開後に永久に閉じてしまうと、改善を後続へ伝えられず5を答えてしまう。このhは許容的だが、B→Aに対して3≤1+0が成立せず非整合である。

**9-Q1**：満たさない。関数はValueErrorを返す。**9-Q2**：言えない。過大評価すると最適解の保証を失う。許容的でも推定の計算費用や同順位処理により実時間は変わる。**9-Q3**：違う。古い登録だけを捨て、新しい安い距離での再登録は処理する。

### 第10回の解答

**10-B**：貪欲法はA,Bを丸ごと採って重さ30・価値160、残り20にはCを丸ごと入れられない。分数版はCの2/3を入れ、価値80を追加して240となる。この240は元の0-1問題では実行不能である。

**10-S**：上界180なら最良でも190に届かないので切れる。200なら改善の可能性が残り、上界だけでは切れない。上界が200でも、本当に200を達成できるとは限らない。

**10-A**：同じ最適値に到達する別の解が、上界とincumbentの等しい枝に残っている可能性がある。一解だけなら同値の枝を切ってよいが、全解が必要なら同値を残して探索し、重複を管理する。

**10-Q1**：必ずしも速くない。入力の容量、上界の強さ、解の見つかる順序に依存する。**10-Q2**：実行可能な解の価値だけを初期値にすれば、正しさを損なわない。架空の高い値を入れると誤って枝を切る。**10-Q3**：呼べない。近似比保証には、最適値との比について全入力に対する証明が必要である。

### 第11回の解答

**11-B**：標本数が4倍なので約1/2。費用もおおむね4倍になるため、精度を上げるコストは小さくない。

**11-S**：同じ牌を5枚以上生成する可能性があり、4枚という制約を破る。また13回の独立抽出は、山から取る非復元抽出と確率分布が違う。枚数ベクトルhの出現確率は、物理牌の選び方の数∏ᵢ C(4,hᵢ)に比例する。したがって合法な枚数ベクトルを一様に選んでも、物理牌からの配牌と同じ分布にはならない。

**11-A**：一般的な三麻の例なら萬子2〜8を牌集合から除外する。ただしローカルルールを先に確定する。生成から除くだけでなく、完成候補にも存在しない萬子2〜8を含めてはいけない。現コードのsuited=Trueの萬子評価はその候補を含むので、そのまま使えない。北の抜きによる手牌・山の扱いや13枚時点を測るかも指定する必要がある。平均値だけ流用しない。

**11-Q1**：一致しない。評価器の厳密さと母集団を全部見たかは別である。**11-Q2**：違う。母平均の推定手順に対する区間であり、各配牌の散らばりを覆う予測区間ではない。**11-Q3**：意味しない。平均、確率、積分などの推定にも使う。

### 第12回の解答

**12-B**：Cが0〜2、Aが2〜4、Bが4〜5。価値は5+2+8=15。BはA終了後なので先行関係を守り、Cも期限2で完了する。

**12-S**：時間を重さ、価値をそのまま使う0-1ナップサックになる。総所要時間が容量以下なら、選ばれた活動のどの順序も実行可能である。活動の中断や繰返しを許せば、さらに別の問題になる。

**12-A**：A,Bを選択済みでも、順序がA→Bなら直前はB、B→Aなら直前はAである。次のCへの段取りをB→C=10、A→C=0とすれば、同じ選択集合でもCを実行できるかが変わる。さらに以前の段取りによって現在時刻が違う場合もある。キーは未来を左右する時刻・直前活動を区別するか、同一集合・直前に対する最早時刻などの支配関係を正しく扱う必要がある。

**12-Q1**：解いていない。一次元の時間配置である。**12-Q2**：よい。上界は楽観的でよく、実際の継続で得られる価値を下回らなければ安全。ただし暫定解として採用してはいけない。**12-Q3**：保証しない。入力した価値、制約、予測のモデル内での最適性であり、現実の価値判断まで自動的に正しくなるわけではない。

<a id="maze-extra"></a>

## 補講A　同じ迷路を四つの方法で解く

第4回の無重みグラフを、全辺の重みが1である道路グラフへ変換する。変換後は第9回の関数をそのまま使える。行と列から頂点名を作り、逆引き辞書で座標へ戻せるようにする。上下左右移動なのでマンハッタン距離をA*へ渡す。

```python
"""同一迷路にDFS/BFS/Dijkstra/A*を適用する追加実習。"""
from lesson04_dfs_bfs import MAZE, maze_graph, dfs, bfs_path
from lesson09_shortest_path import shortest_path


def compare() -> dict:
    graph = maze_graph(MAZE)
    names = {cell: f'{cell[0]},{cell[1]}' for cell in graph}
    reverse = {name: cell for cell, name in names.items()}
    weighted = {names[cell]: [(names[n], 1) for n in neighbors] for cell, neighbors in graph.items()}
    start, goal = (0, 0), (2, 4)
    def manhattan(name: str) -> float:
        r, c = reverse[name]
        return abs(r-goal[0])+abs(c-goal[1])
    bfs = bfs_path(graph, start, goal)
    dijkstra = shortest_path(weighted, names[start], names[goal])
    astar = shortest_path(weighted, names[start], names[goal], manhattan)
    assert bfs is not None
    assert len(bfs)-1 == dijkstra[0] == astar[0] == 6
    return {'DFS_visit_order': dfs(graph, start), 'BFS_steps': len(bfs)-1,
            'Dijkstra': dijkstra, 'A*': astar}


if __name__ == '__main__':
    for name, result in compare().items():
        print(name, result)
```

```text
DFS_visit_order [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (0, 4), (2, 2), (2, 1), (2, 0), (1, 0)]
BFS_steps 6
Dijkstra (6.0, ['0,0', '0,1', '0,2', '1,2', '1,3', '1,4', '2,4'], 12)
A* (6.0, ['0,0', '0,1', '0,2', '1,2', '1,3', '1,4', '2,4'], 11)
```

DFSの出力は訪問順であり、隣り合う出力要素が必ず辺でつながる経路とは限らない。再帰で戻った後に別の枝へ入るためだ。BFS・ダイクストラ・A*は同じ距離6を返す。これは重みがすべて1であるという条件を、コードを通して確認した例になる。

<a id="benchmarks"></a>

## 補講B　実測とランダム探索

以下は実際に実行した比較である。測定は同じプロセスで5回繰り返した中央値であり、入力生成や印刷は測定区間に含めない。フィボナッチのメモ化は各回cache_clearしている。数値は本環境の記録であり、読者のPCで同じ秒数になる保証はない。

測定環境：Python 3.12.14／Linux-6.18.55-x86_64-with-glibc2.39。値は5回の中央値。

| 問題 | N | 方法 | 結果 | 時間（ms） |
|---|---:|---|---:|---:|
| fibonacci | 20 | plain | 6765 | 0.8137 |
| fibonacci | 20 | memo-cold | 6765 | 0.0027 |
| fibonacci | 25 | plain | 75025 | 8.8117 |
| fibonacci | 25 | memo-cold | 75025 | 0.0034 |
| fibonacci | 30 | plain | 832040 | 98.6483 |
| fibonacci | 30 | memo-cold | 832040 | 0.0041 |
| knapsack | 16 | brute | 168 | 134.2692 |
| knapsack | 16 | topdown | 168 | 0.1574 |
| knapsack | 16 | dp1d | 168 | 0.0522 |
| knapsack | 16 | branch-bound | 168 | 0.1468 |
| knapsack | 16 | greedy | 168 | 0.0172 |
| knapsack | 16 | random-1000 | 157 | 5.6076 |


ランダム探索は、無作為な採否を1000回作り、容量を守るもののうち最高価値を保存した。ここで求めるのは平均ではない。乱数seedを変えれば最良値も変わり、実行可能な解であることは確かめられても最適性は保証されない。実験の全入力とコードは次に示す。

```python
"""追加実験。python experiments.py > experiments.json で再実行可能。"""
import json
import platform
import time
from statistics import median
from random import Random
import lesson07_memoization as l7
import lesson08_knapsack as l8
import lesson10_branch_bound as l10
import lesson11_monte_carlo as l11
import lesson12_final_project as l12


def timed(function, repetitions: int = 5) -> tuple[object, float]:
    seconds = []
    answer = None
    for _ in range(repetitions):
        begin = time.perf_counter()
        answer = function()
        seconds.append(time.perf_counter()-begin)
    return answer, median(seconds)


def random_knapsack(items: list[l8.Item], capacity: int, samples: int, seed: int) -> int:
    """無作為な採否案の中の最良実行可能値。最適性の保証はない。"""
    l8.validate(items, capacity)
    if samples < 0:
        raise ValueError('samples >= 0 required')
    rng = Random(seed)
    best = 0
    for _ in range(samples):
        bits = [rng.randrange(2) for _ in items]
        weight = sum(w*b for (w, v), b in zip(items, bits))
        value = sum(v*b for (w, v), b in zip(items, bits))
        if weight <= capacity:
            best = max(best, value)
    return best


def run() -> dict:
    result = {'python': platform.python_version(), 'platform': platform.platform(),
              'timing': 'median of 5 runs; perf_counter; environment dependent', 'benchmarks': []}
    for n in (20, 25, 30):
        def cold():
            l7.fibonacci.cache_clear()
            return l7.fibonacci(n)
        for name, function in [('plain', lambda: l7.fibonacci_plain(n)), ('memo-cold', cold)]:
            answer, seconds = timed(function)
            result['benchmarks'].append({'problem': 'fibonacci', 'n': n, 'method': name,
                                         'answer': answer, 'seconds': seconds})
    rng = Random(808)
    items = [(rng.randint(1, 12), rng.randint(1, 30)) for _ in range(16)]
    capacity = 45
    result['knapsack_input'] = {'items': items, 'capacity': capacity}
    expected = l8.brute_force(items, capacity)
    methods = [('brute', lambda: l8.brute_force(items, capacity)),
               ('topdown', lambda: l8.top_down(items, capacity)),
               ('dp1d', lambda: l8.compressed_dp(items, capacity)),
               ('branch-bound', lambda: l10.branch_bound(items, capacity)[0]),
               ('greedy', lambda: l10.greedy(items, capacity)),
               ('random-1000', lambda: random_knapsack(items, capacity, 1000, 10))]
    for name, function in methods:
        answer, seconds = timed(function)
        if name not in ('greedy', 'random-1000'):
            assert answer == expected
        else:
            assert answer <= expected
        result['benchmarks'].append({'problem':'knapsack', 'n':16, 'method':name,
                                     'answer':answer, 'seconds':seconds})
    result['monte_carlo'] = [l11.estimate(n, 2026) for n in (200, 1000, 5000, 10000)]
    result['scheduling'] = {str(use_bound): l12.optimize(l12.ACTIVITIES, 6, use_bound=use_bound)
                            for use_bound in (False, True)}
    return result


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
```

`experiments.py`の実行結果はJSONで出力される。ZIPの`recorded_results/experiments.json`には制作時の結果を収録した。速度だけで判断せず、返す値、最適性の条件、メモリ、入力の大きさをそろえて比較すること。

<a id="selection"></a>

## 補講C　未知の問題に向き合うための選択表

| 観察した構造 | 最初に試す方法 | 確認すべき条件 |
|---|---|---|
| 候補が少ない | 全探索 | 候補を漏れなく生成できるか |
| 判定が偽から真へ一度だけ変わる | 二分探索 | 単調性、境界、不変条件 |
| 選択を積み重ね、途中で矛盾が分かる | バックトラック | 取り消し、網羅性、安全な枝刈り |
| 同じ残り問題に何度も到達する | メモ化 | 未来を決める完全な状態キー |
| 小さい状態の組合せで答えを作れる | DP | 状態数、遷移、依存関係、最適部分構造 |
| 無重みグラフの最短手数 | BFS | 発見時の登録、キュー |
| 非負重みの最短経路 | ダイクストラ | 負辺なし、古い項目の除外 |
| ゴールまでの下界が作れる | A* | 許容性、整合性または再展開 |
| 局所選択を最適解へ組み込める証明がある | 貪欲法 | 問題固有の交換・支配の証明 |
| 最適性が必要で上界が作れる | 分枝限定法 | 安全な界、実行可能な暫定解 |
| 大きな母集団の平均や確率が欲しい | モンテカルロ推定 | 抽出分布、独立性、誤差表示 |
| 良い解が早く欲しく最適性は必須でない | ランダム探索など | 解の検証、停止条件、再現性 |

**厳密解**は定義された問題の正しい解、最適化なら最適性が保証された解を指す。**近似解**は最適値に近いことを狙う解であり、用語だけで誤差保証が付くわけではない。理論上の**近似アルゴリズム**と呼ぶ場合は近似比などの保証を明示する。**発見的手法**は、実用上よい結果を期待して使うが一般の最適性保証を持たない規則である。**統計的推定値**は未知の平均などを標本から推定した値であり、最適解の近似とは目的が異なる。

最適部分構造だけで高速なDPが完成するわけでもない。十分な状態表現、計算できる遷移、依存関係を処理する順序、扱える状態数が必要である。また、すべてのDPが最適化を扱うわけではなく、数え上げや到達可能性も同じ枠組みで扱える。

<a id="references"></a>

## 補講D　参考資料と確認範囲

以下は仕様・保証条件の照合と、次の学習のための一次資料である。本書の説明・図・Pythonコードは教材用に構成したもので、外部資料の長文転載ではない。参照確認日：2026年10月17日。

- **Python公式ドキュメント：functools（第7回・第11回）** — キャッシュ可能な引数、cache_info、cache_clear、上限付きキャッシュの仕様。[Python 3.11 functools](https://docs.python.org/3.11/library/functools.html)
- **Python公式ドキュメント：heapq（第9回）** — ヒープの優先度付きキューとタプル比較の注意。[Python 3.11 heapq](https://docs.python.org/3.11/library/heapq.html)
- **MIT OpenCourseWare 6.006：Dijkstra（第9回）** — 非負重みと緩和・確定の考え方。[Lecture 16 PDF](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/6277a1f06100c26a7ff21031af6757b5_MIT6_006F11_lec16.pdf)
- **MIT OpenCourseWare 6.006：Knapsack（第8回）** — 状態設計と擬多項式時間。[Recitation 21](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/recitation-21-dynamic-programming-knapsack-problem/)
- **UC Berkeley CS188：Informed Search（第9回）** — 安い経路が後から見つかったときの再展開と整合性。[Spring 2023 Lecture 4 PDF](https://inst.eecs.berkeley.edu/~cs188/sp23/assets/lectures/cs188-sp23-lec04.pdf)
- **MahjongRepository/mahjong（第11回の外部照合）** — シャンテン計算の公開実装。本制作の実行照合にはPyPI版1.4.0を使用。現在のmasterの仕様と固定版は区別する。[プロジェクト](https://github.com/MahjongRepository/mahjong) / [shanten.py](https://github.com/MahjongRepository/mahjong/blob/master/mahjong/shanten.py)

公開実装との有限個の一致は数学的な正しさの完全証明ではない。本書では、通常形の合法な完成候補への距離という定義、色別の分解と合成の網羅性、独立した小規模全探索、既知の境界ケースを組み合わせて検証した。性能も、この教材と掲載入力に対する結果であり、競技・商用ソルバーの最速実装を主張しない。
