# 公開・反映結果

確認日：2026-10-28。現時点の実行検証版を公開済み。400〜500ページ相当への本文拡充は未完了。

- リポジトリ： https://github.com/k-380/business
- 新規配置： python-timeseries-cleaning/
- 書籍公開URL： https://k-380.github.io/business/python-timeseries-cleaning/index.html
- 書籍一覧： https://k-380.github.io/business/
- 教材追加コミット： https://github.com/k-380/business/commit/0a71e0c2fbac1ac67fbb529222178bce2c1252f0
- Pages Actions： https://github.com/k-380/business/actions/runs/40614906505 （success）
- もう一つの既存Pagesワークフロー： https://github.com/k-380/business/actions/runs/40614906098 （success）

## 既存コンテンツの保全

既存index.htmlのプログラミング欄へ、指定の書名、副題、紹介文と相対リンクを追加した。件数と表示番号を更新し、既存25リンクをすべて保持した。ほかの書籍ファイルは変更していない。

シェルからのgit pushは認証情報が利用できなかったため、接続済みGitHub連携のGitデータAPIで反映した。作成したリポジトリ全体のGitツリーハッシュはローカル検証済み版と一致（cc8c3e2e1cbef141a1fff27102ca483287cae475）。mainの旧SHAを照合し、force=falseで更新した。

## 公開後の検査

全24章、表紙・補講・巻末ページ、CSS、JavaScript、30図版、単一HTML、ZIPを含む68ファイルを公開URLから取得した。すべてHTTP 200かつローカル検証済みファイルとSHA-256が一致した。書籍一覧のHTMLも一致し、本書への導線を確認した。取得したZIPのCRC検査も通過した。

検査対象の一覧と取得サイズはtests/publication-results.jsonへ保存。掲載した検査記録は教材追加コミットに対する結果であり、この記録の追加後はZIPのバイト列が変わる。更新ZIPは再生成時にCRCを再検査する。

オフラインブラウザ検査の結果はtests/browser-results.jsonへ保存済み。公開サイトでのブラウザ操作の再検査は未実施だが、公開ファイルがオフライン検証版と同一であることを確認した。

## 制作上の未完了

依頼全体の完成ではない。印刷時172ページの実行検証版であり、初学者向けの段階的実習、追加の失敗例、変化点検出などの厚みを増す作業が残る。PROGRESS.mdに次の編集対象と再生成・検証手順を記録した。
