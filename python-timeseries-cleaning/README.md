# Pythonではじめる時系列データクリーニング

Excelの生データを、信頼できる解析データに変える技術。

**制作版：実行検証版 0.1（2026-10-28）。全24章を収録していますが、依頼された400〜500ページ相当の長編教科書への拡充は未完了です。完成版とは呼んでいません。進捗と残課題はPROGRESS.md、検証結果はVERIFICATION.mdを参照してください。**

## 閲覧

`index.html` をブラウザで開きます。全24章、目次、本文検索、用語集、索引、参考文献、教材一覧へ移動できます。`single-file.html` は本文・コード・図・参考文献を収録したオフライン単一ファイル版です。Python実行用教材は別途ZIPまたはこのフォルダ全体を取得してください。外部CDNは使用しません。

## 環境

検証環境はPython 3.12.14 / Linux。主な依存関係はrequirements.txtで固定し、推移的依存関係はrequirements-lock.txtに記録しています。Windows/macOSのネイティブ実行は未検証です。scikit-learnとstatsmodelsはこの版では使用しません。

Windows（PowerShell、Python 3.12をインストールした後）:

```powershell
cd python-timeseries-cleaning
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-lock.txt
.venv\Scripts\python examples/chapter01/run.py
```

macOS / Linux:

```bash
cd python-timeseries-cleaning
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python examples/chapter01/run.py
```

以降の`python`はこの仮想環境のPythonに読み替えます。インストールにはネットワークが必要ですが、インストール後の読書・教材コード実行に外部通信は不要です。Web参考資料へのリンクを開く場合は接続が必要です。

## 実行

```bash
python clean_timeseries.py --input datasets/raw/02_pressure.csv --config configs/02_pressure.yaml --output results/pressure01
python clean_timeseries.py --input datasets/raw/10_irregular_excel.xlsx --config configs/10_workbook.yaml --output results/workbook01
python -m pytest tests -q
```

初期設定は検出・分類のみ。補間を有効にするには理由と承認者を設定します。実行例は章24を参照してください。対象外・エラーの一覧はbatch_summary.json、入力ごとのレポートは出力フォルダ配下に保存されます。非空の既存出力先は拒否します。最終アプリはCSV/.xlsxのみ、ファイルごとの処理です。ファイルをまたぐ自動結合やストリーミング補間は行いません。

## 再生成

```bash
python datasets/generators/generate.py
python tools/make_examples.py
python tools/make_labs.py
python tools/verify_examples.py
python tools/build_datasets.py
python tools/refresh_sample.py
python tools/build_book.py
python tools/check_html.py
python tools/package.py
```

生成器は同梱の模擬データを再作成します。実測データをdatasets/rawへ置かず、別フォルダで管理してください。既存の教材ファイルは再生成で更新されます。

## 構成

- manuscript/：全章の編集用Markdown
- chapters/：24章のHTML
- examples/chapterXX/run.py：章ごとの完全な実行スクリプト
- examples/common.py：ファイル参照・日本語SVG出力の共通処理
- tsclean/：検出・補間・CLIの共通実装
- datasets/raw/：10題材の模擬CSVと不規則Excel、文字コード・分割例
- datasets/expected/：模擬真値、既定検出出力、期待値サマリー
- datasets/manifest.json：乱数種、生成モデル、異常位置と原因
- datasets/cleaners/：データセット別の実行入口
- exercises/：三段階の演習、解答、実行入口
- tests/：境界条件と数値結果のテスト
- references/：本文確認済み公式資料の一覧

## データとコードの扱い

すべての測定データは模擬データです。実在の製品の試験結果ではありません。latent_signalは生成器が持つ真値で、実測データから自動取得できるものではありません。演習の閾値は機器一般の規格値ではありません。

教材の原稿・独自コード・模擬データは利用者の学習と業務改変に利用できます。依存ライブラリと日本語フォントは各配布元のライセンスに従います。フォントのファイル自体は本パッケージへ再配布せず、SVGには描画に必要な字形をパスとして含めています。

## 実践補講

`labs.html`に入力形式、同期、補間法、校正、多変量検出、チャンク境界の6実験と18題の追加演習を収録。`examples/lab01`〜`lab06`は完全な実行スクリプト。補講6の処理関数は教材用であり、CLIの大容量対応を保証しない。
