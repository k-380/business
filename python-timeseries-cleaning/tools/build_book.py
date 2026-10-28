from pathlib import Path
import html,json,re,sys
import markdown
ROOT=Path(__file__).resolve().parents[1]
PARTS=['生データを理解する','時間軸を修復する','欠損値と異常値を扱う','センサーデータ特有の問題','複数データの統合と品質管理','実務の自動化']
ROMAN=['I','II','III','IV','V','VI']
chapters=[]
for i in range(1,25):
    text=(ROOT/f'manuscript/chapter{i:02d}.md').read_text(encoding='utf-8')
    chapters.append({'n':i,'title':text.splitlines()[0][2:],'text':text,'path':f'chapters/chapter{i:02d}.html'})

def md(text):return markdown.markdown(text,extensions=['tables','fenced_code','toc'])
def code(text,lang='python'):return '<pre><code class="language-'+lang+'">'+html.escape(text)+'</code></pre>'
def sidebar(base,current=None,single=False):
    s='<nav aria-label="全章目次"><a href="'+('#top' if single else base+'index.html')+'">表紙・全体目次</a>'
    for p in range(6):
        s+=f'<p class="part">第{ROMAN[p]}部 {PARTS[p]}</p>'
        for c in chapters[p*4:p*4+4]:
            s+=f'<a class="{"current" if current==c["n"] else ""}" href="'+(f'#c{c["n"]:02d}' if single else base+c['path'])+f'">{c["n"]:02d}　{c["title"]}</a>'
    for label,path,anchor in [('はじめに・環境構築','getting-started.html','intro'),('実践補講6題','labs.html','labs'),('教材ダウンロード','downloads.html','downloads'),('用語集・索引','glossary.html','glossary'),('参考文献','references/bibliography.html','bibliography'),('検証と未完了項目','verification.html','verification')]:
        s+=f'<a href="{("#"+anchor) if single else base+path}">{label}</a>'
    return s+'</nav>'

def page(title,body,path='index.html',current=None,single=False):
    seen={}
    def unique_id(m):
        ident=m.group(1);seen[ident]=seen.get(ident,0)+1
        return 'id="'+ident+('' if seen[ident]==1 else '--'+str(seen[ident]))+'"'
    body=re.sub(r'\bid="([^"]+)"',unique_id,body)
    base='../' if '/' in path else ''
    css=(ROOT/'assets/css/book.css').read_text()
    js=(ROOT/'assets/js/book.js').read_text()
    search=(ROOT/'assets/js/search-index.js').read_text() if (ROOT/'assets/js/search-index.js').exists() else ''
    head=f'<style>{css}</style>' if single else f'<link rel="stylesheet" href="{base}assets/css/book.css">'
    scripts=f'<script>{search}</script><script>{js}</script>' if single else f'<script src="{base}assets/js/search-index.js"></script><script src="{base}assets/js/book.js"></script>'
    s=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="測定値の意味を保全する時系列データクリーニング。全24章の実行検証版。"><title>{html.escape(title)} | Pythonではじめる時系列データクリーニング</title>{head}</head><body data-base="{base}" data-single="{str(single).lower()}"><a class="skip" href="#main">本文へ</a><header><a class="brand" href="{'#top' if single else base+'index.html'}">Pythonではじめる<br>時系列データクリーニング</a><div class="tools"><button id="menu-toggle" aria-expanded="false" type="button">目次</button><button id="search-toggle" type="button">全文検索</button><button id="theme-toggle" type="button">明暗切替</button></div></header><section id="search-panel" class="search-panel" aria-label="全文検索"><div><label for="search-input">全24章・補講を検索（複数語はスペースで区切る）</label><input id="search-input" type="search" placeholder="例：補間 欠損"><div id="search-results" class="search-results" aria-live="polite"></div></div></section><div class="layout"><aside>{sidebar(base,current,single)}</aside><main id="main">{body}<footer>Pythonではじめる時系列データクリーニング · 実行検証版0.1 · 2026-10-28<br>測定データはすべて模擬。閾値は演習設定。長編教科書への拡充は継続中。</footer></main></div>{scripts}</body></html>'''
    (ROOT/path).write_text(s,encoding='utf-8')
    return s

INTRO='''# はじめに・環境構築

データクリーニングとは、異常な値を都合よく削除することではない。測定値の意味を保全しながら、解析可能な状態へ変換する技術である。本書はExcelを使う技術者が、測定の意味を確かめながらPythonを学ぶための教材として制作した。

## この版の到達点

全24章の本文、実行可能な例、実行結果、図、72題の三段階演習、10題材のデータ、CLIと自動テストを収録した実行検証版である。依頼された400〜500ページ相当の長編版には達しておらず、完成版とは表記していない。未完了項目は検証ページに明示する。

## 最初の30分

1. 教材ダウンロードページでZIPを取得し、展開する。ZIPの中から直接実行しない。
2. index.htmlをブラウザで開き、第1章を読む。
3. Python 3.12の環境を用意し、下記の仮想環境へ依存関係を入れる。
4. examples/chapter01/run.pyを実行し、原本を残したまま候補が付くことを確認する。
5. 数字と図が掲載結果に一致したら第2章へ進む。

## Pythonを実行する場所

ブラウザの教科書はPythonを実行するアプリではない。読書、検索、コードコピーはブラウザで行い、計算は自分のPCのPythonで行う。コードを貼る場所は、WindowsのPowerShellやmacOSのターミナルである。`python ...`というコマンドをPythonの対話画面の`>>>`へ入力しない。

Pythonは公式配布元から3.12系を用意する。検証には3.12.14を使用した。OSの管理ポリシーがある業務PCでは、それに従ってインストールする。まず `python --version` またはWindowsの `py -3.12 --version` で対象を確認する。

## Windows PowerShell

以下は、展開したフォルダの一つ上から始める。仮想環境を有効化する操作を省き、実行するPythonの場所を毎回明示するので、実行ポリシーの変更は不要である。

```powershell
cd python-timeseries-cleaning
py -3.12 -m venv .venv
.venv\\Scripts\\python -m pip install -r requirements-lock.txt
.venv\\Scripts\\python examples/chapter01/run.py
```

## macOS / Linux

```bash
cd python-timeseries-cleaning
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python examples/chapter01/run.py
```

仮想環境は、この教材で使うライブラリを他の仕事から分離するためのフォルダである。インストール時にはネットワーク接続が必要だが、教材を取得し依存関係を入れた後は、サンプル実行に外部通信は不要である。[Python公式資料](references/bibliography.html#r10)も参照してほしい。

## フォルダとパス

`datasets/raw/02_pressure.csv` は、現在の作業フォルダから見た相対パスである。コマンドを実行する場所が違うと見つからない。サンプルプログラムは自身の場所から教材のルートを求めるため、データ参照は安定する。CLIの引数は利用者が指定するため、現在位置からのパスまたは絶対パスを書く。空白を含むパスは引用符で囲む。

## 読み進めるためのPython最小知識

|表記|意味|測定データでの用途|
|---|---|---|
|x = 3|名前xへ値を割り当てる|周期や閾値の設定|
|df['温度']|表から列を取り出す|温度だけを検査|
|df.iloc[10]|位置で11行目を取り出す|問題箇所の確認|
|df.loc[mask]|条件がTrueの行を取り出す|候補一覧の作成|
|a & b|真偽の列の両方を満たす|同一モードかつ欠損|
|x[2:5]|2以上5未満の位置を取り出す|区間抽出|
|def name(...):|再利用する処理を定義する|検出関数を作る|
|assert condition|条件が偽なら止める|計算結果の確認|

Pythonの位置は0から数え、スライスの終端は含まない。本文の異常位置も、明示がなければ0始まりである。Excelの行番号は1始まりなのでsource_rowで別に保存する。インデントは処理のまとまりを表すため、先頭の空白を勝手に消さない。列に対する条件式では `(x>0) & (x<10)` のように括弧を付ける。

## エラーが出たとき

最後の行だけでなく、どのファイルの何行目で止まったかを読む。ModuleNotFoundErrorなら実行環境とpipの対象が一致しているか、FileNotFoundErrorなら作業フォルダとファイル名、KeyErrorなら列名と見出し行を確認する。ValueErrorはデータの前提違反を意図的に通知している場合がある。コードの検査を削除して先へ進まない。

各章の掲載コードは `examples/chapterXX/run.py` の全体で、共通処理は `examples/common.py` と `tsclean/core.py` にある。コードコピーだけで別フォルダへ移すと、この構成が失われる。最初はフォルダ全体を取得して実行する。共通処理の全ソースは実装資料で読める。

## 学習順と判断の原則

まず第I部で読み込みと意味の確認、第II部で時間軸、第III部で欠損と候補判定、第IV部でセンサーと信号、第V部で統合と記録、第VI部で自動化へ進む。各章は単独実行できるが、第24章の出力を正しく評価するには前の原則が必要である。

すべてのデータは模擬である。正解情報は処理結果の検証に使い、実データの未知の真値を自動で知る手段と考えない。本書の最終的な問いは、「このデータを、この目的に使ってよい根拠は何か」である。
'''

REFS=[
('pandas.read_excel — pandas 2.2.3','https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.read_excel.html','見出し、シート、型、欠損解釈のAPI仕様。第2章。'),
('Working with missing data — pandas 2.2.3','https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/missing_data.html','欠損表現と補間limitの挙動。第9・10章。'),
('filtfilt / sosfiltfilt — SciPy documentation','https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html','往復フィルタ、合成次数、端点処理。第16章。併せてsosfiltfiltの本文も確認。'),
('resample_poly — SciPy 1.17.0','https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.signal.resample_poly.html','低域通過処理を伴うレート変換と境界条件。第7章。'),
('median_abs_deviation — SciPy documentation','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_abs_deviation.html','MADの定義とnormal尺度。第11章。'),
('Dates and Times — openpyxl','https://openpyxl.readthedocs.io/en/stable/datetime.html','Excel日付システム、架空日付、タイムゾーン。第3章。'),
('NIST/SEMATECH e-Handbook, Detection of Outliers','https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm','候補のラベル付けと原因特定の区別、分布の前提。第1・11章。'),
('numpy.fft.rfftfreq — NumPy documentation','https://numpy.org/doc/stable/reference/generated/numpy.fft.rfftfreq.html','FFT周波数軸とサンプル間隔の単位。第16章。'),
('pandas.merge_asof — pandas documentation','https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html','結合キーの整列、direction、tolerance。第17章。'),
('仮想環境とパッケージ — Python 3.12','https://docs.python.org/ja/3.12/tutorial/venv.html','仮想環境とバージョン指定インストール。はじめに。'),
('PchipInterpolator — SciPy documentation','https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html','形状保持区分三次補間と単調性。補講3。'),
('CubicSpline — SciPy documentation','https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html','三次スプラインの境界条件。補講3。'),
('numpy.linalg.lstsq — NumPy 2.3','https://numpy.org/doc/2.3/reference/generated/numpy.linalg.lstsq.html','最小二乗問題の解、残差、ランク。補講2・4。')]

GLOSS=[('ADC','アナログ信号をデジタル値へ変換する装置。レンジと分解能を区別する。',[1,14]),('エイリアシング','サンプリングにより異なる周波数が同じ観測へ重なること。後から元成分を一意に分離できない。',[6,7]),('オフセット','値または時刻の原点のずれ。感度・時計の速さのずれと区別する。',[8,13]),('完全性','必要な測定情報がどの程度存在するか。分母は予定数か受領数かを明示する。',[4]),('候補フラグ','確認対象の印。測定不具合が確定したことを意味しない。',[1,11,20]),('校正','基準との比較によって測定系の関係を確認すること。トレンド除去とは異なる。',[13]),('ジッター','サンプル時刻などの短期的な揺れ。時計の長期ドリフトと区別する。',[6]),('セグメント','同じ連続状態として扱う区間。A→B→Aの二つのAは別区間。',[10,18]),('ゼロ位相','往復処理などで位相ずれを相殺した性質。非因果性と振幅変化は残る。',[16]),('タイムゾーン','ローカル時刻とUTCの関係を定める地域の時刻規則。',[3]),('チャンク','大きなファイルを分割して処理する単位。窓処理には境界状態が必要。',[21]),('ドリフト','オフセット、感度、時計などが時間や条件とともに変化すること。',[8,13]),('ナイキスト周波数','等間隔サンプリングの周波数の半分。実際の通過帯域設計には余裕が必要。',[6,7]),('フリーズ','値が更新されず固定される現象。同一値だけでは通信異常と確定しない。',[15]),('補間','既知の点の内側に値を推定すること。実測値と区別する。',[7,10]),('飽和','測定系の上限・下限などで入力への応答が頭打ちになること。',[14]),('量子化','連続的な値を離散的な段階へ表すこと。',[14]),('リネージ','入力から結果に至る変換と由来の連鎖。',[20]),('Hampel','局所中央値と局所MADで逸脱候補を探す方式。実装の窓定義を確認する。',[11,12]),('IQR','第3四分位数と第1四分位数の差。',[11]),('MAD','中央値からの絶対偏差の中央値。正規尺度補正は約1.4826。',[11]),('MAR / MCAR / MNAR','欠損が観測情報や未観測値にどう依存するかのモデル。欠損パターンだけで原因は決まらない。',[9]),('NaN / NaT','数値・日時の欠損表現。ゼロとは異なる。',[3,9]),('RMS','二乗平均平方根。直流成分がある場合、標準偏差とは異なる。',[19]),('SHA-256','ファイル内容の同一性確認に使うハッシュ。電子署名や測定の正しさの保証ではない。',[20]),('UTC','時刻比較の共通基準。元の地域時刻とその意味も保存する。',[3,8]),('Zスコア','平均からの差を標準偏差で割った指標。確率解釈には分布の前提が必要。',[11]),('merge_asof','順序キーの距離による結合。許容差、方向、対応時刻を明示する。',[17]),('原本保全','受領したファイルを変更せず残すこと。raw列の保存だけでは原ファイルの代わりにならない。',[1,20,24]),('有効桁数','測定と表現で意味を持つ桁。計算機の桁数が測定精度を保証するわけではない。',[3,14])]

CASE_NOTES=[
('温度の長時間測定','短い欠損と長い欠損、後半のドリフトを分ける。','33点の欠損を検出する。ドリフトは既定ルールでは自動診断できない。基準なしにトレンドを引かない。', [3,4,9,10,13]),
('圧力の時系列','二つの測定スパイクと35秒付近の実パルスを区別する。','範囲外候補2点。実パルスを保存する。修正する場合は第12章の承認済み2点だけ。',[1,11,12]),
('振動加速度','40/130 Hzの実成分と370 Hzの干渉を分ける。','既定検査は値を変更しない。250 Hzへ間引く場合130 Hzは保存できない。第7・16章の目的別出力を比較する。',[6,7,16]),
('電流波形','起動ピークの飽和と周期性を確認する。','飽和候補35点、記録の最大絶対値12 A。真値ピーク約17.21 Aは原観測だけから復元できない。',[14,16,19]),
('複数センサー同時計測','時計のオフセットと200 ppmのドリフトを検証する。','時計モデルtB=1.0002tA+0.7。第8章で符号と補正を検証する。基準チャンネルは出題の補助情報。',[8,17]),
('製品耐久試験','製品劣化とセンサー長期ドリフトを区別する。','真の劣化傾き0.0006 mm/s/hを保存する。基準との差を校正に使い、終端の外挿を確認する。',[13,19]),
('運転停止を含む試験','停止中の無測定と運転中の短い欠損を区別する。','欠損92点。承認設定では運転中2点のみ補間、停止中90点を保持する。',[9,10,18,24]),
('データロガー再起動','取得順序を残して時刻の重複とリセットを見つける。','逆転1箇所。重複はリセットにより広範囲にも発生する。自動ソート・補間はしない。',[5,6,15]),
('複数試作品比較','固定値、異周期、分割ファイルの重複と追加列を調べる。','固定値候補21点。許容差0.4秒の対応付けではB未対応200点。分割ファイルを黙って重複削除しない。',[15,17,21]),
('不規則なExcel帳票','結合セル、単位行、混合型、空白行、Excelシリアル値を調べる。','CSV版40行、Excel測定表41行。故障は変換不能、空白・---は欠損として分類。原Excel行番号を保存する。',[2,3,24])]

def chapter_body(c):
    n=c['n'];text=c['text']
    pre,rest=text.split('<!-- EXEC -->')
    b=md(pre)
    b+='<p class="note">関連する詳細実験は<a href="../labs.html">実践補講</a>に掲載。入力形式・同期・補間・校正・多変量・チャンク境界を扱う。</p>'
    script=(ROOT/f'examples/chapter{n:02d}/run.py').read_text()
    output=(ROOT/f'examples/chapter{n:02d}/output.txt').read_text()
    b+=f'<h2 id="code{n:02d}">実行するコードと結果</h2><p class="source-link"><a href="../examples/chapter{n:02d}/run.py" download>run.py</a> · <a href="../implementation.html">共通処理の全ソース</a><br>教材フォルダで <code>python examples/chapter{n:02d}/run.py</code> を実行。以下は省略のないスクリプト。共通モジュールは教材一式に含む。</p>'+code(script)
    b+='<details><summary>検証環境での実行結果を開く</summary>'+code(output,'text')+'</details>'
    b+=f'<figure id="fig{n:02d}"><img src="../assets/images/chapter{n:02d}.svg" alt="図{n}-1 {c["title"]}の検証グラフ"><figcaption>図{n}-1　{c["title"]}。掲載スクリプトから生成。軸と単位は図中に記載し、線種・マーカーを併用。すべて模擬データ。</figcaption></figure>'
    before,answer=rest.split('## 解答・解説')
    answer,summary=answer.split('## 章末まとめ')
    b+=md(before)+'<details class="answers"><summary>演習解答・解説を表示する</summary>'+md(answer)+'</details>'+md('## 章末まとめ'+summary)
    problems=rest.split('## 演習')[1].split('## 解答・解説')[0]
    (ROOT/f'exercises/problems/chapter{n:02d}.md').write_text(f'# 第{n}章 {c["title"]}\n'+problems,encoding='utf-8')
    (ROOT/f'exercises/solutions/chapter{n:02d}.md').write_text(f'# 第{n}章 解答\n'+answer,encoding='utf-8')
    runner=f'''"""Run the complete chapter example as the foundation exercise."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[2]/'examples/chapter{n:02d}/run.py'),run_name='__main__')
'''
    (ROOT/f'exercises/solutions/chapter{n:02d}.py').write_text(runner,encoding='utf-8')
    # Table of contents is built from actual heading anchors.
    headings=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',b)
    toc='<details id="page-toc"><summary>この章の節</summary><ul>'+''.join(f'<li><a href="#{a}">{t}</a></li>' for a,t in headings)+'</ul></details>'
    return f'<p class="eyebrow">第{ROMAN[(n-1)//4]}部　{PARTS[(n-1)//4]} / 第{n:02d}章</p>'+toc+b

def main():
    search=[]
    for c in chapters:
        text=re.sub(r'<[^>]+>|[#*`|]',' ',c['text']);text=re.sub(r'\s+',' ',text)
        search.append({'n':c['n'],'title':c['title'],'text':text,'path':c['path']})
    labtext=(ROOT/'manuscript/labs.md').read_text()
    search.append({'n':0,'title':'実践補講：入力形式・同期・補間・校正・多変量・チャンク処理','text':re.sub(r'\s+',' ',labtext),'path':'labs.html','anchor':'labs'})
    (ROOT/'assets/js/search-index.js').write_text('window.BOOK_SEARCH='+json.dumps(search,ensure_ascii=False).replace('</','<\\/')+';',encoding='utf-8')
    labs=md(labtext)
    for n in range(1,7):
        script=(ROOT/f'examples/lab{n:02d}/run.py').read_text()
        output=(ROOT/f'examples/lab{n:02d}/output.txt').read_text()
        block=f'<p><a href="examples/lab{n:02d}/run.py" download>補講{n}の完全な実行スクリプト</a>：教材フォルダで <code>python examples/lab{n:02d}/run.py</code></p>'+code(script)
        block+='<details><summary>実行結果</summary>'+code(output,'text')+'</details>'
        block+=f'<figure id="labfig{n}"><img src="assets/images/chapter{n+24:02d}.svg" alt="補講{n}の検証グラフ"><figcaption>補講{n} 図1　掲載コードから生成した模擬データの検証結果。</figcaption></figure>'
        labs=labs.replace(f'<!-- LAB{n} -->',block)
    page('実践補講',labs,'labs.html')
    intro=md(INTRO)
    page('はじめに・環境構築',intro,'getting-started.html')
    bibliography='<h1>参考文献・技術資料</h1><p>下記は2026-10-28に本文を確認した資料。引用は要点の参照に限り、教材のコードと説明は独自に構成した。stable/currentの資料には検証環境より新しい版が含まれる。実際のコード互換性は固定環境で確認した。存在を確認できない文献や有料規格本文は引用していない。</p>'
    for i,(title,url,note) in enumerate(REFS,1):bibliography+=f'<section id="r{i}"><h2>R{i}　{title}</h2><p><a href="{url}">{url}</a></p><p>{note} 確認状態：本文確認済み。</p></section>'
    bibliography+='<p>補助確認：<a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html">SciPy sosfiltfilt</a>（本文確認済み）。資料のURL先はオンラインだが、本書の閲覧に接続は不要。</p>'
    page('参考文献',bibliography,'references/bibliography.html')
    glossary='<h1>用語集・索引</h1><p>用語の定義と、説明している章への索引。全文検索も利用できる。</p><dl class="glossary">'
    for term,definition,ns in GLOSS:
        links='、'.join(f'<a href="chapters/chapter{n:02d}.html">第{n}章</a>' for n in ns)
        glossary+=f'<dt>{term}</dt><dd>{definition} {links}</dd>'
    glossary+='</dl>';page('用語集・索引',glossary,'glossary.html')
    datasets='<h1>教材データと正解情報</h1><p>10題材すべて模擬データ。seed=20261028。異常位置は0始まり、start以上stop未満。正解のlatent_signalは測定ノイズを除く模擬真値で、クリーニング後に一致すべき値とは限らない。</p><p><a href="datasets/manifest.json">生成条件と異常位置の全記録</a> · <a href="datasets/generators/generate.py">生成器</a></p><p>expectedのinspection/flagsは既定設定の期待出力スナップショット。独立の小さな正解テストも併用する。単に同じ実装の出力を正解とした検証ではない。</p>'
    manifests=json.loads((ROOT/'datasets/manifest.json').read_text())['datasets']
    for i,(d,notes) in enumerate(zip(manifests,CASE_NOTES),1):
        title,problem,answer,ns=notes;name=d['id']
        datasets+=f'<section id="data{i:02d}"><h2>{i:02d}　{title}</h2><p>{problem}</p><p>モデル：{html.escape(d["model"])}。{d["n"]}行、単位：{d["unit"]}。</p><p><a href="datasets/raw/{name}.csv" download>生CSV</a> · <a href="datasets/expected/{name}_truth.csv" download>模擬真値</a> · <a href="datasets/expected/{name}_inspection.csv" download>期待する検査後データ</a> · <a href="datasets/expected/{name}_flags.csv" download>期待フラグ</a> · <a href="datasets/cleaners/{name}.py" download>専用実行入口</a> · <a href="configs/{name}.yaml" download>設定</a></p>'
        datasets+='<h3>問題がある位置</h3>'+code(json.dumps(d['events'],ensure_ascii=False,indent=2),'json')
        datasets+=f'<h3>基礎・応用・実務課題</h3><ol><li>専用実行入口で検出し、期待フラグと比較する。</li>対応章の窓・時間幅・閾値を変更し、候補数と実現象の保持を調べる。</li>{problem} 実務で真値がなければ、追加でどの証拠が必要かを記述する。</li></ol><details class="answers"><summary>期待結果と解説</summary><p>{answer}</p><p>「真値へ無条件で置換する」は不適切。処理対象外の観測値と原本が保持されることを確かめる。</p></details><p>対応章：'+', '.join(f'<a href="chapters/chapter{n:02d}.html">{n}章</a>' for n in ns)+'</p></section>'
    datasets+='<h2>追加の入力形式</h2><p><a href="datasets/raw/10_irregular_excel.xlsx" download>不規則Excel</a> · <a href="configs/10_workbook.yaml">Excel用設定</a> · <a href="datasets/raw/locale_cp932.csv">CP932・セミコロンCSV</a> · <a href="datasets/raw/prototype_part1.csv">分割1</a> · <a href="datasets/raw/prototype_part2.csv">分割2</a> · <a href="configs/07_modes_interpolate.yaml">承認補間設定</a></p>'
    page('教材データ',datasets,'datasets.html')
    implementation='<h1>API・実装の読み方</h1><p>共通関数の全ソース。各章の実行例はこれらを読み込む。原本を上書きするAPIは設けていない。</p>'
    for path in ['tsclean/core.py','tsclean/app.py','tsclean/streaming.py','examples/common.py','clean_timeseries.py']:
        implementation+=f'<h2>{path}</h2><p><a href="{path}" download>ファイルを取得</a></p>'+code((ROOT/path).read_text())
    page('共通処理の全ソース',implementation,'implementation.html')
    downloads='''<h1>教材ダウンロード</h1><p>フォルダ構成を保って展開してください。HTMLはローカルで開けます。計算にはPython環境が必要です。</p><p><a class="download" href="python-timeseries-cleaning.zip" download>教科書・教材一式 ZIP</a><a class="download" href="single-file.html" download>本文単一ファイル版 HTML</a></p><ul><li><a href="README.md">README</a></li><li><a href="requirements.txt">主要依存関係</a> / <a href="requirements-lock.txt">依存関係の固定ファイル</a></li><li><a href="datasets.html">10題材の生データ・正解・処理プログラム</a></li><li><a href="implementation.html">共通コード全体</a></li><li><a href="tests/test_core.py">自動テスト</a></li><li><a href="PROGRESS.md">制作状況・再開手順</a></li></ul><p>ZIPはZIP自身を含みません。単一HTMLの本文・図・コード・数式はオフラインで読めますが、Pythonの実行にはZIP内の共通モジュールとデータが必要です。</p>'''
    page('教材ダウンロード',downloads,'downloads.html')
    verify_path=ROOT/'VERIFICATION.md'
    verification=md(verify_path.read_text()) if verify_path.exists() else '<h1>検証状況</h1><p>検証ログの集約作業中。完成判定はまだ行っていません。</p>'
    verification+=md((ROOT/'PROGRESS.md').read_text())
    page('検証と未完了項目',verification,'verification.html')
    toc='<div class="toc-grid">'
    for p in range(6):
        toc+=f'<section class="toc-card"><h2>第{ROMAN[p]}部<br>{PARTS[p]}</h2><ol start="{p*4+1}">'+''.join(f'<li><a href="{c["path"]}">{c["title"]}</a></li>' for c in chapters[p*4:p*4+4])+'</ol></section>'
    toc+='</div>'
    cover='''<section class="cover" id="top"><p class="eyebrow">ENGINEERING DATA / PYTHON</p><h1>Pythonではじめる<br>時系列データクリーニング</h1><p class="subtitle">Excelの生データを、信頼できる解析データに変える技術</p><p>測定値を残す。時間軸を確かめる。<br>処理の根拠と影響を、自分の言葉で説明する。</p><p class="badge">全6部24章 · 10題材 · 実行コード・SVG・72題の章末演習＋補講6本</p><div class="note status"><strong>実行検証版 0.1</strong><br>全24章と教材を収録。400〜500ページ相当の長編版への拡充は未完了です。<a href="verification.html">検証結果と残課題</a>を公開しています。</div><p><a class="download" href="getting-started.html">はじめに・環境構築</a><a class="download" href="chapters/chapter01.html">第1章から読む</a><a href="downloads.html">教材をダウンロード</a></p></section><h2>この教科書の原則</h2><blockquote>データクリーニングとは、異常な値を都合よく削除することではない。測定値の意味を保全しながら、解析可能な状態へ変換する技術である。</blockquote><p>元の値、解析用の値、品質フラグ、処理履歴を分けます。異常候補は自動削除せず、補間値は実測値と区別します。例は温度・圧力・振動・電流・耐久試験。すべて再生成可能な模擬データです。</p><h2>全体目次</h2>'''+toc+'<h2>巻末資料</h2><p><a href="labs.html">実践補講6題</a> · <a href="datasets.html">教材一覧</a> · <a href="glossary.html">用語集・索引</a> · <a href="references/bibliography.html">参考文献</a> · <a href="single-file.html">一冊を続けて読む</a></p>'
    page('表紙・目次',cover)
    single_parts=[]
    for c in chapters:
        body=chapter_body(c);n=c['n']
        prev=f'<a href="chapter{n-1:02d}.html">← 第{n-1}章</a>' if n>1 else '<a href="../getting-started.html">← はじめに</a>'
        next=f'<a href="chapter{n+1:02d}.html">第{n+1}章 →</a>' if n<24 else '<a href="../glossary.html">用語集 →</a>'
        page(f'第{n}章 {c["title"]}',body+f'<nav class="chapter-nav" aria-label="章間移動">{prev}{next}</nav>',c['path'],n)
        # Inline SVG and scope IDs so all figures/headings can coexist in one document.
        svg=(ROOT/f'assets/images/chapter{n:02d}.svg').read_text();svg=svg[svg.index('<svg'):]
        body=re.sub(r'<img[^>]+>',lambda m:svg,body,count=1)
        ids=re.findall(r'\bid="([^"]+)"',body)
        for ident in sorted(set(ids),key=len,reverse=True):
            body=body.replace(f'id="{ident}"',f'id="c{n:02d}-{ident}"').replace(f'href="#{ident}"',f'href="#c{n:02d}-{ident}"').replace(f'url(#{ident})',f'url(#c{n:02d}-{ident})')
        body=body.replace('../references/bibliography.html#','#').replace('../implementation.html','#implementation').replace('../','')
        single_parts.append(f'<article id="c{n:02d}" class="single-chapter">'+body+'</article>')
    single_cover=re.sub(r'href="chapters/chapter(\d\d).html"',r'href="#c\1"',cover)
    full=single_cover+'<section id="intro" class="single-chapter">'+intro+'</section>'+''.join(single_parts)
    single_labs=labs
    for n in range(1,7):
        svg=(ROOT/f'assets/images/chapter{n+24:02d}.svg').read_text();svg=svg[svg.index('<svg'):]
        for ident in sorted(set(re.findall(r'\bid="([^"]+)"',svg)),key=len,reverse=True):
            svg=svg.replace(f'id="{ident}"',f'id="lab{n}-{ident}"').replace(f'href="#{ident}"',f'href="#lab{n}-{ident}"').replace(f'url(#{ident})',f'url(#lab{n}-{ident})')
        single_labs=re.sub(r'<img[^>]+chapter'+f'{n+24:02d}'+r'\.svg"[^>]*>',lambda m:svg,single_labs)
    for ident,content in [('labs',single_labs),('downloads',downloads),('glossary',glossary),('bibliography',bibliography),('implementation',implementation),('verification',verification)]:
        content=re.sub(r'href="chapters/chapter(\d\d).html"',r'href="#c\1"',content)
        full+=f'<section id="{ident}" class="single-chapter">'+content+'</section>'
    full=full.replace('href="references/bibliography.html#','href="#').replace('href="getting-started.html"','href="#intro"').replace('href="verification.html"','href="#verification"').replace('href="downloads.html"','href="#downloads"').replace('href="glossary.html"','href="#glossary"').replace('href="references/bibliography.html"','href="#bibliography"')
    full=full.replace('href="labs.html"','href="#labs"')
    page('単一ファイル版',full,'single-file.html',single=True)
    print('Built 24 chapters and supplementary pages.')

if __name__=='__main__':main()
