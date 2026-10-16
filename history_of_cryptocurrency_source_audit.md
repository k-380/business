# 出典照合表 — 仮想通貨の歴史

対象：`history_of_cryptocurrency.html`（全章収録・短縮稿）  
歴史叙述の調査基準日：2026年10月15日  
最終制作・動作検証日：2026年10月16日  
書誌項目：74件（史料・技術文書・データ等73件、原構想1件）

## 照合の意味と限界

Web検索の後、資料本文、公開コード、価格CSV、または明記した公式要旨を確認した。本文確認は記した箇所についての確認であり、各文献の全ページ精読や独立した第三者監査を意味しない。会社の発表は会社がその内容を公表した証拠、訴状についての発表はその時点での訴えの内容の証拠として扱った。後の有罪判断とは区別している。

確認範囲が限定された資料を、全文確認済みとは表示しない。以下の照合表とHTMLの参考文献には同じ資料番号を使用した。本文中の番号、章末注、参考文献の相互リンクで、資料を使用した位置をたどれる。2026年10月15日より後の出来事は歴史本文に追加していない。2030年等の数字は、基準日以前に発表された予測として明示した。

## 主要事実と根拠の照合

| ID | 確認した主要事実・採用上の限定 | 本書での位置 | 資料・日付・参照箇所 | 確認範囲 |
|---|---|---|---|---|
| S01 | 支払いと本人情報の結合を弱める盲署名。会議年と出版年を区別。 | 第1章、全体年表 | [David Chaum：Blind Signatures for Untraceable Payments](https://chaum.com/wp-content/uploads/2022/01/Chaum-blind-signatures.pdf) ／ CRYPTO 1982／論文集1983 ／ pp.199–203、冒頭画像確認 | 本文確認（PDF冒頭） |
| S02 | 選択的に情報を開示するプライバシー観。 | 第1章、全体年表 | [Eric Hughes：A Cypherpunk’s Manifesto](https://www.activism.net/cypherpunk/manifesto.html) ／ 1993-03-09 ／ 本文 | 本文確認 |
| S03 | 1997年提案、2002年論文化。計算コストを課す迷惑行為対策。 | 第1章、全体年表 | [Adam Back：Hashcash — A Denial of Service Counter-Measure](https://cdn.nakamotoinstitute.org/docs/hashcash.pdf) ／ 2002-08-01 ／ §1–3 | 本文確認 |
| S04 | 分散した残高管理構想。第1案の同期・妨害不能通信という強い前提。 | 第1章、全体年表 | [Wei Dai：b-money](https://nakamotoinstitute.org/library/b-money/) ／ 1998-11 ／ 2方式の提案と導入 | 本文確認（原文転載） |
| S05 | PoW・時刻証明・所有記録の組合せ。1998年構想と公開本文の年を区別。 | 第1章、全体年表 | [Nick Szabo：Bit Gold](https://nakamotoinstitute.org/library/bit-gold/) ／ 2005-12-29 ／ 手順1–7 | 本文確認（原文転載） |
| S06 | 署名だけでは二重支払いを防げない。PoWによる履歴選択。 | 第1章、第13章、第2章、第3章、第4章、序章 | [Satoshi Nakamoto：Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) ／ 2008 ／ §1–6、§11 | 本文確認 |
| S07 | ホワイトペーパー公開告知。 | 第2章、全体年表 | [Satoshi Nakamoto：Bitcoin P2P e-cash paper](https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html) ／ 2008-10-31 ／ メール本文 | 本文確認 |
| S08 | 初期ネットワークとテスト送金。後年の本人回想として扱う。 | 第2章、第5章 | [Hal Finney：Bitcoin and Me](https://nakamotoinstitute.org/library/bitcoin-and-me/) ／ 2013-03-19 ／ 初期ソフト・10BTC受領の回想 | 本文確認（原文転載） |
| S09 | 2枚のピザと10,000BTC。世界最初のあらゆる価値交換とは断定しない。 | 第2章、全体年表 | [laszloほか：Pizza for bitcoins?](https://bitcointalk.org/index.php?topic=137.0) ／ 2010-05-18〜22 ／ 依頼投稿と成立報告 | 本文確認 |
| S10 | 独立検証、累積仕事量、難易度、報酬。 | 第11章、第12章、第2章、第5章 | [Bitcoin Developer Guide：Block Chain](https://developer.bitcoin.org/devguide/block_chain.html) ／ 日付表示なし ／ Introduction、Proof of Work、Consensus | 本文確認 |
| S11 | UTXO、入力、出力、署名。 | 第2章、序章 | [Bitcoin Developer Guide：Transactions](https://developer.bitcoin.org/devguide/transactions.html) ／ 日付表示なし ／ Introduction、P2PKH | 本文確認 |
| S12 | プールは報酬変動を平準化。ASICはブロックヘッダーをハッシュ。 | 第13章、第2章、第5章、補論Ⅱ | [Bitcoin Developer Guide：Mining](https://developer.bitcoin.org/devguide/mining.html) ／ 日付表示なし ／ Solo Mining、Pool Mining | 本文確認 |
| S13 | 本文・図表は日次USD終値系列。全体図は2011〜2025年末。取得ファイル末尾は2026-05-24、最後の非欠損価格は05-23。 | 第10章、第11章、第3章、第6章、第7章、第8章、第9章、はじめに、長期価格図 | [Coin Metrics：Community Data CSV archive: btc.csv](https://github.com/coinmetrics/data/blob/master/csv/btc.csv) ／ 取得2026-10-15 ／ time、PriceUSD列 | CSV実データ確認 |
| S14 | PriceUSDはUTC日末。単一取引所価格でなくCM Reference Rates系列。 | 第10章、第11章、第3章、第7章、はじめに、長期価格図 | [Coin Metrics：USD Denominated Closing Price](https://github.com/coinmetrics/docs-website/blob/master/asset-metrics/market/priceusd.md) ／ 日付表示なし ／ Definition、Details | 本文確認 |
| S15 | 金融・決済機関の取扱制限。個人の自己責任取引を一律禁止した文書ではない。 | 第3章、第6章、全体年表 | [中国人民銀行ほか／工業情報化部掲載：关于防范比特币风险的通知](https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2013/art_d7241872221f43708e47fd30ac30eac0.html) ／ 2013-12（掲載12-06） ／ 本文・添付通知 | 本文確認 |
| S16 | 利用者と管理者・交換業者を区分した規制解釈。 | 第3章、全体年表 | [FinCEN：FIN-2013-G001](https://www.fincen.gov/system/files/shared/FIN-2013-G001.pdf) ／ 2013-03-18 ／ pp.1–3 | 本文確認 |
| S17 | 分散型DNS、マージマイニング。 | 第4章 | [Namecoin project：Namecoin](https://www.namecoin.org/) ／ 日付表示なし ／ 導入・用途 | 本文確認 |
| S18 | 2011-10-13 03:00 GMT起動、2.5分目標。コード公開日と運転開始を混同しない。 | 第4章、全体年表 | [Charlie Lee（coblee）：Litecoin — a lite version of Bitcoin. Launched!](https://bitcointalk.org/index.php?topic=47417.0) ／ 2011-10 ／ 冒頭および#2、#4 | 本文確認 |
| S19 | Billy Markus、Jackson Palmer、2013-12-06公開。 | 第4章、全体年表 | [Dogecoin project：The History of Dogecoin](https://dogecoin.com/dogepedia/articles/history-of-dogecoin/) ／ 日付表示なし ／ 本文 | 本文確認 |
| S20 | 汎用的な状態遷移とスマートコントラクト。 | 第4章 | [Vitalik Buterin：Ethereum Whitepaper](https://ethereum.org/whitepaper/) ／ 2013構想、公開本文2014 ／ Ethereum、Applications | 本文確認 |
| S21 | 2015-07-30 Frontier、2016-07-20 DAO fork、2022-09-15 Merge。 | 第4章、第6章、全体年表 | [ethereum.org：Timeline of all Ethereum forks](https://ethereum.org/ethereum-forks/) ／ 更新2026-06-26 ／ Frontier、DAO fork、Paris | 本文確認 |
| S22 | 利用者約75万BTC・自社約10万BTC消失という当時の会社発表。原因説明は確定認定ではない。 | 第6章、第8章、全体年表 | [MtGox Co., Ltd.：Announcement regarding application for civil rehabilitation](https://www.mtgox.com/img/pdf/20140228-announcement_eng.pdf) ／ 2014-02-28 ／ pp.1–2 | 本文確認 |
| S23 | 3月7日に旧ウォレット約20万BTC確認。85万BTC全量永久消失とは書かない。 | 第6章、全体年表 | [MtGox Co., Ltd.：保有ビットコイン残高に関するお知らせ](https://www.mtgox.com/img/pdf/20140320-btc-announce.pdf) ／ 2014-03-20 ／ 日本語p.1／英訳p.2 | 本文確認 |
| S24 | 交換業登録制。2020-05-01法令用語を暗号資産へ変更。 | 第7章、全体年表、はじめに | [金融庁：暗号資産に関連する事業を行うみなさまへ](https://www.fsa.go.jp/policy/virtual_currency/index_2.html) ／ 制度開始2017-04-01 ／ 冒頭・法令改正状況 | 本文確認 |
| S25 | The DAOトークンへの証券法適用判断。全トークン一律判断ではない。 | 第7章、全体年表 | [SEC：SEC Issues Investigative Report Concluding DAO Tokens, a Digital Asset, Were Securities](https://www.sec.gov/newsroom/press-releases/2017-131) ／ 2017-07-25 ／ 本文 | 本文確認 |
| S26 | 署名データの分離とブロック重量。発動日を提案日と分ける。 | 第7章 | [Eric Lombrozo、Johnson Lau、Pieter Wuille：BIP 141: Segregated Witness (Consensus layer)](https://bitcoin.org/bip/141/) ／ 2015-12-21提案 ／ Abstract、Motivation、Specification | 本文確認 |
| S27 | 2017-12-18取引日、現金決済、参照価格を使う先物。 | 第7章、全体年表 | [CME Group：CME Group Self-Certifies Bitcoin Futures to Launch Dec. 18](https://www.cmegroup.com/media-room/press-releases/2017/12/01/cme_group_self-certifiesbitcoinfuturestolaunchdec18.html) ／ 2017-12-01 ／ 本文 | 本文確認 |
| S28 | 流出数量526,300,010XEM。初報の概数と区別。 | 第8章、全体年表 | [コインチェック：暗号資産NEMの不正送金に関する質問](https://coincheck.com/ja/info/faq_nem) ／ 2018-10-16更新 ／ 事案概要、原因、補償 | 本文確認 |
| S29 | みなし業者の位置づけ、検査と審査の強化。 | 第7章、第8章 | [金融庁：仮想通貨交換業者の登録審査について](https://www.fsa.go.jp/news/30/virtual_currency/20181024-2.html) ／ 2018-10-24 ／ 本文 | 本文確認 |
| S30 | 2018-11-02メインネット公開という開発者の記録。 | 第8章、全体年表 | [Hayden Adams：A Short History of Uniswap](https://blog.uniswap.org/uniswap-history) ／ 2019-02-11 ／ 冒頭 | 本文確認 |
| S31 | 政策金利誘導目標0〜0.25%。BTC上昇の単独原因とはしない。 | 第9章、全体年表 | [Federal Reserve：Federal Reserve issues FOMC statement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20200315a.htm) ／ 2020-03-15 ／ 本文 | 本文確認 |
| S32 | パンデミック前後の株式と暗号資産の連動増加に関する分析。 | 第9章 | [Tobias Adrian、Tara Iyer、Mahvash S. Qureshi／IMF：Crypto Prices Move More in Sync With Stocks, Posing New Risks](https://www.imf.org/en/Blogs/Articles/2022/01/11/crypto-prices-move-more-in-sync-with-stocks-posing-new-risks) ／ 2022-01-11 ／ 本文 | 本文確認 |
| S33 | 2020-04-20の5月限清算値−37.63USD/バレル。暫定報告であり単一原因の確定ではない。 | 全体年表、補論Ⅰ | [CFTC staff：Interim Staff Report on Trading in NYMEX WTI Crude Oil Futures Contract Leading up to, on, and around April 20, 2020](https://www.cftc.gov/media/5296/InterimStaffReportNYMEX_WTICrudeOil/download) ／ 2020-11-23 ／ Executive Summary、契約の説明 | 本文確認 |
| S34 | 21,454BTC、手数料等込み2.5億USD購入。 | 第10章、全体年表 | [MicroStrategy：Form 8-K / MicroStrategy Adopts Bitcoin as Primary Treasury Reserve Asset](https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/bltdc574e252ebabae5/6762eaf6fce5e8b4194e463f/form-8-k_08-11-2020.pdf) ／ 2020-08-11 ／ Exhibit 99.1 p.5 | 本文確認 |
| S35 | 新規採掘案件禁止と既存案件退出。公表日と制発日の相違に注意。 | 第10章、全体年表 | [中国国家発展改革委員会ほか：关于整治虚拟货币“挖矿”活动的通知](https://zfxxgk.ndrc.gov.cn/web/iteminfo.jsp?id=18271) ／ 制発2021-09-03 ／ 本文 | 本文確認 |
| S36 | 交換等を非法金融活動と位置づけ、海外交換業者の国内向けサービスも対象。 | 第10章 | [中国人民銀行ほか：关于进一步防范和处置虚拟货币交易炒作风险的通知](https://www.pbc.gov.cn/tiaofasi/144941/3581332/4348658/index.html) ／ 公表2021-09-24 ／ 第1項 | 本文確認 |
| S37 | 受取り任意化と納税USD限定の法改正。法定通貨という語だけで政策を判断しない。 | 第10章、全体年表 | [IMF：IMF Executive Board Approves New 40-month US$1.4 billion Extended Fund Facility Arrangement for El Salvador](https://www.imf.org/en/news/articles/2025/02/26/pr25043-el-salvador-imf-approves-new-40-month-us1-bn-eff-arr) ／ 2025-02-26 ／ Bitcoin関連事前措置 | 本文確認 |
| S38 | 2022年5月UST崩壊、2024年民事陪審判断と和解。市場価値消失と回収額を区別。 | 第11章、全体年表 | [SEC：Terraform and Kwon to Pay $4.5 Billion Following Fraud Verdict](https://www.sec.gov/newsroom/press-releases/2024-73) ／ 2024-06-13 ／ 本文 | 本文確認 |
| S39 | 2022-06-12出金停止、07-13破産申立。訴状の主張として表示。 | 第11章、全体年表 | [CFTC：CFTC Charges Alexander Mashinsky and Celsius Network, LLC with Fraud and Material Misrepresentations](https://www.cftc.gov/PressRoom/PressReleases/8749-23) ／ 2023-07-13 ／ Case Background | 本文確認 |
| S40 | 登録ファンド運用者に対する処分。個々の貸借・損失額の全容はこの資料から確定しない。 | 第11章 | [Monetary Authority of Singapore：MAS Reprimands Three Arrows Capital for Providing False Information and Exceeding Assets Under Management Threshold](https://www.mas.gov.sg/regulation/enforcement/enforcement-actions/2022/mas-reprimands-three-arrows-capital-for-providing-false-information-and-exceeding-assets-under-management-threshold) ／ 2022-06-30 ／ 本文 | 本文確認 |
| S41 | 25年の量刑、顧客資金流用。起訴と有罪判断を区別。 | 第11章、全体年表 | [US Department of Justice, SDNY：Samuel Bankman-Fried Sentenced To 25 Years In Prison](https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison) ／ 2024-03-28 ／ 本文 | 本文確認 |
| S42 | 危機時の大小投資家行動と損失推計。全利用者の実現損益の実測ではない。 | 第11章 | [Giulio Cornelli、Sebastian Doerr、Jon Frost、Leonardo Gambacorta／BIS：Crypto shocks and retail losses, BIS Bulletin 69](https://www.bis.org/publications/bulletin-69-crypto-shocks-and-retail-losses) ／ 2023-02-20 ／ Key takeaways | 公式要旨確認／PDF全文未確認 |
| S43 | PoWからPoSへの移行。ガス代低下と同一ではない。 | 第11章、第4章、全体年表、補論Ⅱ | [ethereum.org：The Merge](https://ethereum.org/roadmap/merge/) ／ 移行2022-09-15 ／ What was The Merge?、Misconceptions | 本文確認 |
| S44 | ETP上場・取引承認。BTCの推薦・承認ではない。Grayscale司法判断の影響。 | 第12章、全体年表 | [Gary Gensler／SEC：Statement on the Approval of Spot Bitcoin Exchange-Traded Products](https://www.sec.gov/newsroom/speeches-statements/gensler-statement-spot-bitcoin-011023) ／ 2024-01-10 ／ 本文 | 本文確認 |
| S45 | 2024-12-30全面適用に向けた実施文書。 | 第12章、全体年表 | [ESMA：ESMA releases last policy documents to get ready for MiCA](https://www.esma.europa.eu/press-news/esma-news/esma-releases-last-policy-documents-get-ready-mica) ／ 2024-12-17 ／ 本文 | 本文確認 |
| S46 | 没収等で政府帰属したBTCを基礎とする備蓄。発表を市場買付実績と混同しない。 | 第12章、全体年表 | [President of the United States：Establishment of the Strategic Bitcoin Reserve and United States Digital Asset Stockpile](https://www.whitehouse.gov/presidential-actions/2025/03/establishment-of-the-strategic-bitcoin-reserve-and-united-states-digital-asset-stockpile/) ／ 2025-03-06 ／ §3 | 本文確認 |
| S47 | ステーブルコイン法署名。政権の期待効果は実証結果ではない。 | 第11章、第12章、全体年表 | [The White House：Fact Sheet: President Donald J. Trump Signs GENIUS Act into Law](https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-signs-genius-act-into-law/) ／ 2025-07-18 ／ 本文 | 本文確認 |
| S48 | 2026-04-10提出、07-15成立と掲載。施行済みとは断定しない。 | 第12章、全体年表 | [金融庁：国会提出法案等](https://www.fsa.go.jp/common/diet/index.html) ／ 2026年成立欄 ／ 第221回国会・当該法律 | 本文確認 |
| S49 | 暗号資産規制の金商法移管等の制度設計。審議用説明資料であることを明示。 | 第12章 | [金融庁：金融商品取引法及び資金決済に関する法律の一部を改正する法律案 説明資料](https://www.fsa.go.jp/common/diet/221/02/03.pdf) ／ 2026-04 ／ pp.1–3 | 本文確認 |
| S50 | 年間138TWh推計、回答事業者は世界活動48%相当。75.4%米国は回答標本内。 | 第5章 | [Cambridge Judge Business School／CCAF：Cambridge study: sustainable energy rising in Bitcoin mining](https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/) ／ 2025-04-28 ／ 調査結果本文 | 大学公式要約確認／報告PDF取得失敗 |
| S51 | FY2018 Q2/Q3開示と暗号採掘需要、550万USD制裁金。会計年度は暦年と異なる。 | 第13章、第5章、補論Ⅱ | [SEC：In the Matter of NVIDIA Corporation, Release No.33-11060](https://www.sec.gov/files/litigation/admin/2022/33-11060.pdf) ／ 2022-05-06 ／ §II、§III、処分 | 本文確認 |
| S52 | 公開日と人間のフィードバックを使う調整。誤情報生成という限界。 | 第13章、全体年表 | [OpenAI：Introducing ChatGPT](https://openai.com/index/chatgpt/) ／ 2022-11-30 ／ Methods、Limitations | 本文確認 |
| S53 | Transformer、attention、行列演算。暗号資産の直接の派生技術ではない。 | 第13章 | [Ashish Vaswaniほか：Attention Is All You Need](https://arxiv.org/html/1706.03762v7) ／ 2017（確認版v7:2023） ／ §1、§3 | 本文確認 |
| S54 | GPT-3と大規模言語モデル。詳細学習コストは採用しない。 | 第13章 | [Tom B. Brownほか：Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) ／ 2020 ／ Abstract | 要旨確認 |
| S55 | モデル規模・データ量・計算予算の配分問題。 | 第13章 | [Jordan Hoffmannほか：Training Compute-Optimal Large Language Models](https://arxiv.org/pdf/2203.15556) ／ 2022 ／ Abstract、§1 | 本文確認 |
| S56 | 2030年945TWhは当時の予測。2026年改訂と区別。 | 第13章 | [IEA：Energy and AI — Executive summary](https://www.iea.org/reports/energy-and-ai/executive-summary) ／ 2025-04-10 ／ データセンター電力需要 | 本文確認 |
| S57 | 2025年485TWh、2030年950TWh予測。全データセンターでありAI単独ではない。 | 第13章 | [IEA：Key Questions on Energy and AI — Executive summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) ／ 2026-04 ／ 電力需要見通し | 本文確認 |
| S58 | 金融引締めとリスク選好経路の研究。因果推定にはモデル前提がある。 | 第9章 | [IMF：The Crypto Cycle and US Monetary Policy](https://www.imf.org/en/publications/wp/issues/2023/08/04/the-crypto-cycle-and-us-monetary-policy-534834) ／ 2023-08-04 ／ 公式掲載要旨 | 公式要旨確認 |
| S59 | トークンの識別と所有者管理。画像の著作権を自動移転する規格ではない。 | 第10章 | [William Entriken、Dieter Shirley、Jacob Evans、Nastassia Sachs：ERC-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721) ／ 2018-01-24 ／ Abstract、Specification、Metadata | 本文確認 |
| S60 | 定積型AMMと価格情報。説明用例では手数料を省略。 | 第8章 | [Hayden Adams、Noah Zinsmeister、Dan Robinson：Uniswap v2 Core](https://app.uniswap.org/whitepaper.pdf) ／ 2020-03 ／ §1–2 | 本文確認 |
| S61 | 2026-07-01に向けた移行期間終了対応。 | 第12章、全体年表 | [ESMA：Statement on the end of transitional periods under MiCA](https://www.esma.europa.eu/sites/default/files/2026-04/ESMA75-113276571-1679_Statement_on_the_end_of_transitional_periods_under_MiCA.pdf) ／ 2026-04-17 ／ pp.1–2 | 本文確認 |
| S62 | 初期BTC市場・Mt.Gox・2011年の価格変動。当時の評価を現在の評価と混同しない。 | 第3章、全体年表 | [European Central Bank：Virtual Currency Schemes](https://www.ecb.europa.eu/pub/pdf/other/virtualcurrencyschemes201210en.pdf) ／ 2012-10 ／ Bitcoinのケーススタディ | 本文確認 |
| S63 | 価格・検索・中国市場の関係は単純でない。キプロス危機の年に本文上の不整合があり当該年代記述は不採用。 | 第3章 | [Ladislav Kristoufek：What Are the Main Drivers of the Bitcoin Price? Evidence from Wavelet Coherence Analysis](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0123923) ／ 2015-04-15 ／ Interest、Safe haven、Influence of China | 本文確認 |
| S64 | 利用普及と金融包摂への慎重な評価。原典全文の調査時点は再確認課題。 | 第10章 | [IMF：El Salvador: Selected Issues](https://www.imf.org/en/publications/cr/issues/2025/03/19/el-salvador-selected-issues-565394) ／ 2025-03-19掲載 ／ 公式掲載要旨 | 公式要旨確認 |
| S65 | SegWitの有効化はブロック481,824。 | 第7章 | [Bitcoin BIPs contributors：BIP 9 deployments](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0009/assignments.mediawiki) ／ 随時更新 ／ segwit行 | 本文確認 |
| S66 | 2017-08-01にBTCと分岐。それ以前の取引履歴を共有。 | 第7章、全体年表 | [Bitcoin Cash Node developers：What is Bitcoin Cash?](https://docs.bitcoincashnode.org/) ／ 随時更新 ／ What is Bitcoin Cash? | 本文確認 |
| S67 | BVI裁判所による清算開始2022-06-27。MAS処分とは区別。 | 第11章、全体年表 | [Russell Crumpler／Teneo：Three Arrows Capital, Ltd. — Notice of Appointment](https://3acliquidation.com/wp-content/uploads/2022/07/Notice-of-Appointment-1-2.pdf) ／ 2022-06-30 ／ p.1 | 本文確認 |
| S68 | 00:09:27 UTCのヘッダー時刻。自前ノード由来とされるブロック記録。現在の確認数等は歴史本文に不使用。 | 第12章、全体年表 | [The Bitcoin Time Machine：Block 840,000](https://www.thebitcointm.com/block/840000) ／ ブロック日時2024-04-20 ／ Time／ブロックハッシュ | 記録本文確認 |
| S69 | ジェネシスの新聞見出し、時刻1231006505、半減間隔210,000、SegWit高481,824。2024年コードによる過去の規則の確認。 | 第2章、全体年表 | [Bitcoin Core contributors：Bitcoin Core v27.0 — chainparams.cpp](https://raw.githubusercontent.com/bitcoin/bitcoin/v27.0/src/kernel/chainparams.cpp) ／ 2024年版 ／ CreateGenesisBlock／CMainParams | コード取得・該当箇所確認 |
| S70 | データベースの実装差による分岐、採掘プールの旧版への切替で収束。 | 第3章、全体年表 | [Gavin Andresen：BIP 50: March 2013 Chain Fork Post-Mortem](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0050.mediawiki) ／ 2013-03-20 ／ What went wrong／Root cause | 本文確認 |
| S71 | 募集期間2016-04-30〜05-28、約1,200万ETH、募集終了時評価約1.5億USD。6月17日から約360万ETH移転。 | 第4章、全体年表 | [SEC：Report of Investigation: The DAO, Release No.81207](https://www.sec.gov/files/litigation/investreport/34-81207.pdf) ／ 2017-07-25 ／ pp.2–3、9–10 | 本文確認 |
| S72 | 2015年6月最終規則、9月22日Circleの初承認。州の枠組みと連邦制度を混同しない。 | 第6章、全体年表 | [New York State Department of Financial Services：NYDFS Announces Approval of First Bitlicense Application From a Virtual Currency Firm](https://www.dfs.ny.gov/reports_and_publications/press_releases/pr1509221) ／ 2015-09-22 ／ 本文・制度年表 | 本文確認 |
| S73 | 2013-10-01逮捕、同月サイト閉鎖。運営内容はこの資料では起訴側の主張として扱う。 | 第3章、全体年表 | [U.S. Department of Justice／SDNY：Manhattan U.S. Attorney Announces the Indictment of Ross Ulbricht](https://www.justice.gov/usao-sdny/pr/manhattan-us-attorney-announces-indictment-ross-ulbricht-creator-and-owner-silk-road) ／ 2014-02-04 ／ 本文・起訴内容・末尾の無罪推定説明 | 本文確認 |
| S74 | 原構想として照合。技術・価格・因果の史実根拠には用いない。 | はじめに | [冷やし茶漬　量産開発者　製造業：仮想通貨の歴史　目次](https://note.com/hiyashi_chazuke/n/n576f09c451f1) ／ 2026-01-11 11:40 ／ 第1章〜エピローグの構想全文 | 本文確認／構想の参照のみ |

## 価格数値の再現条件

系列はCoin Metrics Community Dataの`btc.csv`の`time`、`PriceUSD`列。単位は1BTC当たり米ドル（USD/BTC）、UTC日末。単一取引所の約定価格ではなくCoin Metricsの参照価格系列である。円換算値は作成していない。初期価格も当時の各取引所の「最高値」を混ぜず、この系列内の値として記述した。

将来、供給元が過去の値や算出方法を更新する可能性がある。本書の数値は取得版に固定しており、当時の時点で閲覧可能だったデータだけを使う検証（point-in-time検証）ではない。個々の年の構成取引所・価格算出方法の全履歴までは確認していない。

- 取得日：2026-10-15。
- 取得ファイル：2,482,497 bytes。
- SHA-256：`06495ff8e643432e6948b7b4686ce44fc106217287dabdc1b38351d9ddec46c3`。
- データURL： https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv
- 書誌と定義：[S13](https://github.com/coinmetrics/data/blob/master/csv/btc.csv)、[S14](https://github.com/coinmetrics/docs-website/blob/master/asset-metrics/market/priceusd.md)。
- ファイルの最終行：2026-05-24。PriceUSDの最後の非欠損値：2026-05-23。
- 長期図の範囲：2011-01-01〜2025-12-31、5,479日・5,479値。対象範囲の欠損日なし。
- 年別図：2017年・2021年・2022年それぞれ1月1日〜12月31日、365値。
- 点を描き、欠損補間や架空の日中値は作っていない。長期図は対数軸、各年図は線形軸。
- 表示は小数点以下2桁に丸めた。増減率は丸め前の値で計算し、小数点以下1桁に丸めた。

### 本文の代表価格

| UTC日付 | USD/BTC | 使用目的 | 根拠 |
|---|---:|---|---|
| 2011-06-08 | 29.03 | 2011年の日末値ピーク | S13・S14 |
| 2013-01-01 | 13.33 | 2013年年初 | S13・S14 |
| 2013-12-04 | 1,134.93 | 2013年の日末値ピーク | S13・S14 |
| 2015-01-14 | 175.64 | 2013年高値からの下落比較 | S13・S14 |
| 2017-01-01 | 997.26 | 2017年年初 | S13・S14 |
| 2017-12-16 | 19,640.51 | 2017年の日末値ピーク | S13・S14 |
| 2018-01-06 | 17,103.59 | 2018年内の日末値最大 | S13・S14 |
| 2018-12-15 | 3,185.07 | 2018年内の日末値最小 | S13・S14 |
| 2020-03-11 | 7,939.34 | 2020年3月急落の比較元 | S13・S14 |
| 2020-03-12 | 4,959.31 | 2020年3月急落の比較先 | S13・S14 |
| 2021-11-08 | 67,541.76 | 2021年内の日末値最大 | S13・S14 |
| 2021-12-31 | 46,355.12 | 2021年末 | S13・S14 |
| 2022-01-01 | 47,560.01 | 2022年内の日末値最大 | S13・S14 |
| 2022-11-09 | 15,758.29 | 2022年内の日末値最小 | S13・S14 |
| 2022-12-31 | 16,524.22 | 2022年末 | S13・S14 |
| 2025-12-31 | 87,516.98 | 長期図の終点 | S13・S14 |

### 比較率の計算

| 比較 | 計算式（丸め前の系列値で計算） | 変化率 | 注意 |
|---|---|---:|---|
| 2013-12-04 → 2015-01-14 | (175.63764056 ÷ 1134.93223089 − 1) × 100 | -84.5% | 選んだ2日の日末値比較。全期間の日中最大ドローダウンではない。 |
| 2018-01-06 → 2018-12-15 | (3185.07404383 ÷ 17103.58927966 − 1) × 100 | -81.4% | 2018年内の日末値の最大から最小への変化。 |
| 2020-03-11 → 2020-03-12 | (4959.31341438 ÷ 7939.34133477 − 1) × 100 | -37.5% | UTC日末同士の1日変化。国内日付や日中値とは異なる。 |

## 価格以外の主要数値

| 対象 | 数値と基準 | 根拠 | 本書での限定 |
|---|---|---|---|
| Hal Finneyのテスト受領 | 10BTC、初期ネットワークを2013年に回想 | [S08](https://nakamotoinstitute.org/library/bitcoin-and-me/) | 同時代の送金記録を直接解析した記述ではなく、本人の回想。 |
| ピザ交換 | ピザ2枚・10,000BTC、2010-05-22成立報告 | [S09](https://bitcointalk.org/index.php?topic=137.0) | 店舗の直接BTC決済、世界最初の全種類の交換とは断定しない。 |
| Litecoin | 2.5分のブロック生成目標 | [S18](https://bitcointalk.org/index.php?topic=47417.0) | 確定に必ず2.5分しか要らない、という意味ではない。 |
| Mt. Gox初期発表 | 顧客約75万BTC、自社約10万BTC、2014-02-28 | [S22](https://www.mtgox.com/img/pdf/20140228-announcement_eng.pdf) | 当時の会社の把握・発表。恒久的な最終損失額ではない。 |
| Mt. Gox追加確認 | 旧ウォレット約20万BTC、2014-03-07確認／03-20公表 | [S23](https://www.mtgox.com/img/pdf/20140320-btc-announce.pdf) | 85万BTCがすべて永久に消えたとの叙述を避ける。 |
| The DAO募集 | 約1,200万ETH、募集終了時約1.5億USD、2016-04-30〜05-28 | [S71](https://www.sec.gov/files/litigation/investreport/34-81207.pdf) | ドル額はSEC報告書の当時評価。現在価値に換算しない。 |
| The DAO資金移転 | 約360万ETH、2016-06-17から | [S71](https://www.sec.gov/files/litigation/investreport/34-81207.pdf) | 報告書の概数。1,200万の厳密な3分の1と再計算しない。 |
| Coincheck不正送金 | 526,300,010XEM、2018年1月事案、会社FAQ更新2018-10-16 | [S28](https://coincheck.com/ja/info/faq_nem) | 初報の概数や円換算額を混ぜない。 |
| FRB政策金利目標 | 0〜0.25%、2020-03-15発表 | [S31](https://www.federalreserve.gov/newsevents/pressreleases/monetary20200315a.htm) | BTCのその後の上昇を単独で説明する因果係数ではない。 |
| WTI先物 | −37.63USD/バレル、2020-04-20、2020年5月限 | [S33](https://www.cftc.gov/media/5296/InterimStaffReportNYMEX_WTICrudeOil/download) | 特定契約の清算値。原油全般・現物小売価格ではない。 |
| MicroStrategy購入 | 21,454BTC・2.5億USD、手数料等込み、2020-08-11発表 | [S34](https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/bltdc574e252ebabae5/6762eaf6fce5e8b4194e463f/form-8-k_08-11-2020.pdf) | 企業の当時の購入発表であり、以後の保有残高ではない。 |
| Terraform等の解決 | 約45億USDを含む支払い、2024-06-13公表 | [S38](https://www.sec.gov/newsroom/press-releases/2024-73) | 市場価値消失額・被害者の実回収額と区別。 |
| SBF量刑 | 禁錮25年、2024-03-28 | [S41](https://www.justice.gov/usao-sdny/pr/samuel-bankman-fried-sentenced-25-years-prison) | 量刑時の判決事実。以後の訴訟手続全体の更新ではない。 |
| 2024年半減期 | ブロック840,000、6.25→3.125BTC、2024-04-20 UTC | [S68](https://www.thebitcointm.com/block/840000) | 新規発行分。手数料を含む採掘収入全額ではない。発行規則はS10・S69も参照。 |
| NVIDIA制裁金 | 550万USD、2022-05-06処分 | [S51](https://www.sec.gov/files/litigation/admin/2022/33-11060.pdf) | FY2018の開示対象期間を暦年2018と同一視しない。 |
| Bitcoin採掘電力 | 年間138TWh規模の推計、2025-04-28公表 | [S50](https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/) | 公式要約確認。報告全体の対象期間・方法は未確認。総実測値とはしない。 |
| 採掘電源構成 | 持続可能52.4%＝再生可能42.6%＋原子力9.8%、同上 | [S50](https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/) | 持続可能を再生可能と読み替えない。 |
| 採掘調査の範囲 | 報告活動は世界の約48%相当、米国75.4%は標本内、同上 | [S50](https://www.jbs.cam.ac.uk/2025/cambridge-study-sustainable-energy-rising-in-bitcoin-mining/) | 75.4%を世界全体の米国シェアとしない。 |
| データセンター需要・2025報告 | 2030年945TWh、2025-04-10報告 | [S56](https://www.iea.org/reports/energy-and-ai/executive-summary) | 将来予測。AI単独の実績ではない。 |
| データセンター需要・2026報告 | 2025年485TWh、2030年950TWh予測、2026年4月報告 | [S57](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) | 全データセンター。AI学習だけの需要でも、電力設備容量GWでもない。 |

## 説明用の仮想数値

UTXOの0.8BTC→0.3BTC＋0.499BTC（差額0.001BTC）、自己資金20・借入80・資産100→90、AMMの10×1,000＝10,000とBの100追加は、仕組みを説明するための架空例である。実勢価格・実際の口座・推奨取引額・推奨手数料として扱っていない。

## 不採用・未解決の主要論点

| 論点 | 判定・残る課題 |
|---|---|
| キプロス危機がBTC高騰を起こした | 同時期の出来事を単独の因果にしない。S63の研究本文にはキプロスの年の不整合もあり、その年代記述を採用していない。資金移動を直接追跡していない。 |
| 2015年の中国ショックが最初の冬の原因 | 原構想の断定を不採用。2011年にも大きな下落があり、2013年規制と2014年Mt. Goxを別の出来事として扱う。 |
| 最初の取引 | テスト送金、法定通貨との交換、商品購入を区分。ピザ事例の「全世界のあらゆる交換の初例」は証明していない。 |
| Bit Goldの1998年と2005年 | 構想の起源と確認できる公開本文の日付を分離。1998年に通貨が稼働したとはしない。 |
| 採掘の機器と地理 | 発展の方向を示したが、機種別初出・出荷台数・市場占有率・国別時系列の網羅的復元は未実施。 |
| ICOや草コインの消滅率 | 母集団と「死んだ」の定義が定まらないため、「大半」や架空の割合を採用しない。 |
| NVIDIAが最大の勝者 | 採掘者・製造受託・設備・GPU企業の利益を同じ範囲で比較していないため不採用。 |
| BIS個人損失 | S42は公式要旨のみ。全利用者の実現損益や破産人数を調べた統計とはしない。 |
| El Salvadorの利用効果 | S64は公式要旨のみ。原典の調査時点・利用率の詳細は未確認。2025年修正はS37本文で確認。 |
| 日本の2026年改正 | 提出・成立はS48、設計意図はS49。施行政令・個別規定の実施日・下位規則の全確認は未実施。成立＝全面施行としない。 |
| 米国の備蓄 | S46は制度設置と条件の文書。基準日までの市場買付総量を立証する資料としては使わない。 |
| 2030年の電力需要 | 予測の発表時点は基準日以前。2030年の実績として本文に混入させない。 |
| 原構想 | S74を全文確認したが、史実の根拠にはしない。原構想と本書の変更対応は編集報告に記載。 |

## 再確認の優先順位

長編版へ拡充する場合は、①Cambridge・BIS・IMFの未取得原典、②採掘企業の機種・出荷・決算資料、③破産事件の債権・回収計画と基準日までの司法記録、④2025〜2026年の規制施行と制度運用、⑤原データの当時版・取引所別履歴を優先する。現在の短縮稿の空白を、一般論や未確認の数字で埋めたことにしてはならない。
