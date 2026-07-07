# 日本市場擴充實作計畫 v1.0

> 制定：OmniQadris＋Bear，2026-07-07。
> 目標：把本 repo 從台灣單市場擴成**多市場**，新增日本四個官方資料源
> （J-Quants／EDINET／TDnet／JPX 官網統計），產出日本版來源目錄（第一版目標 200–400 endpoints），
> 供 `~/QadrisDatalakeJP`（日股 datalake，Phase 1＝財報/股價/股利）的來源調查使用。
> 執行方式：**不走 steward**，Bear 直接在本 repo 開 agent session 實作。
> 背景依據：`~/QadrisCorp/docs/Qadris_JP_Datalake_Feasibility_2026-07-07.md`（資料源事實均經查證，勿憑記憶改寫）。

## 0. 設計原則

- **框架不 fork**：多市場共用本 repo 與同一顆 `catalog/catalog.db`（`UNIQUE(source, path)` 天然支援多源並存；state 只升不降的 upsert 邏輯不動）。
- **台股 924 endpoints 零回歸**：所有改動不得降級/覆寫既有資料；現有 134 個測試須全綠。
- 日本源特性與台灣的差異：EDINET/J-Quants 是正規 REST（比 MOPS 逆向工程簡單），無民國年/Big5 問題；**新增複雜度是認證**（J-Quants API key、EDINET Subscription-Key）與 **Excel/PDF 下載型 probe**（JPX）。

## 1. 框架泛化（先做，估 0.5–1.5 天）

1. **Source registry 抽單一對照表**：現在 source 資訊散落 `catalog.py:Source` Literal、`config.py:get_base_url`、`cli.py` probe dispatch／stats 顯示名、`generate_catalog.py`、`scripts/generate_gh_pages.py`——抽成一張 `SOURCE_REGISTRY`（source → market／顯示名／base_url／probe 模組），加新源只改一處。`Source` Literal 擴充 `jquants/edinet/tdnet/jpx`。
2. **market 維度**：不動 DB schema——由 `SOURCE_REGISTRY` 的 source→market（`tw`/`jp`）推導即可；`search`/`stats` CLI 加 `--market` 篩選；GH Pages `catalog.json`/`index.html` 加 market 欄與篩選器。
3. **認證 hook（框架唯一新缺口）**：`fetcher.py` 加可選 auth 注入（per-source：header `x-api-key`（J-Quants V2）／query param `Subscription-Key`（EDINET））；金鑰走 `config.py`（`RSR_JQUANTS_API_KEY`、`RSR_EDINET_API_KEY`），`.env.example` 更新。無金鑰時 probe 該源要**明確報「需要金鑰」而非靜默失敗**。
4. **Excel probe 路徑**：probe 對 `.xls/.xlsx` 連結新增「下載→pandas/openpyxl 讀 header→存 sample_fields」路徑（JPX 統計頁產物多為 Excel）；PDF 連結標記 `response_format=pdf` 不解析內容。
5. **Enrich 泛化**：prompt 第一行參數化（`You are a {market} financial data expert`）；`_KNOWN_ID_FIELDS` 增補日文/日股欄位名（`Code`、`LocalCode`、`銘柄コード`、`証券コード`、`edinetCode`、`docID`）＋模糊比對加「コード」；rule 函數（`infer_history_method`/`infer_request_example`/`infer_coverage`/`infer_response_format`）各加四個日本源分支（日期西元制，比民國年單純；coverage 對應 prime/standard/growth）。domain tag 清單沿用（市場中立），可選加 `timely_disclosure`。

## 2. 四個來源模組（估 4–8 天）

| 模組 | 做法 | 參考範本 | 估工 |
|------|------|---------|------|
| `discover_jquants.py` | 無公開 swagger → **手工 `KNOWN_ENDPOINTS` 清單**（V2 spec 站 `jpx-jquants.com/en/spec/*` 約 30–40 個 endpoint：listed info、daily bars、fins summary/details、dividend、indices、margin、short selling、trades by investor type…），probe 帶 API key GET＋`pagination_key` 感知（只取首頁樣本）。**rate limit：Free 5 req/min → probe 間隔 ≥13s**；記錄各 endpoint 所屬方案（Free/Light/Standard/Premium）進 `notes` | `discover_tse_web.py` 的 KNOWN_ENDPOINTS 模式 | 200–300 行＋auth |
| `discover_edinet.py` | 正規 REST：書類一覧 `documents.json?date=`＋書類取得 `documents/{docID}?type=`。**目錄語意決策：endpoint 粒度＝「書類種別×取得格式」**（如「有價證券報告書 CSV」「大量保有報告書 XBRL」），category=書類種別、date_params=提出日、id_field=docID/edinetCode；probe 打一覧 API＋抓一份 type=5 CSV 樣本 | `discover_tdcc_openapi.py`（乾淨 REST） | 200–350 行 |
| `discover_tdnet.py` | 爬 `release.tdnet.info` 的 `I_list_{頁碼}_{YYYYMMDD}.html` 固定規則；endpoint 粒度＝檢索面（當日一覧、按代碼、按開示種別）＋短信 XBRL zip 取得模式；**免費窗口 31 天**記入 `notes`；probe 抓當日 list 解析件數與欄位 | `discover_mops.py` 簡化版（無民國年/Big5/多步 form） | 300–450 行 |
| `discover_jpx.py` | BeautifulSoup 爬 `jpx.co.jp/markets/statistics-equities/` 頁面樹（investor-type／margin／short-selling／examination／misc…）；**檔案 URL 含 CMS 隨機路徑（`tXXvrt…-att`），必須先爬列表頁解析 href、不可寫死**；probe 走 Excel 下載路徑；PDF-only 表（銘柄別信用週殘、空賣比率）如實標記。**注意：JPX 對雲端抓取 client 回 403，本機 requests/curl 可抓（與 UA 無關）**；`web_delay` 沿用 3s | `discover_mops.py` 的 sitemap 連結樹＋`discover_tse_web.py` 的 report-index 模式 | 300–500 行 |

前置帳號（人工，Bear 或 agent 引導 Bear 做）：J-Quants Free 註冊（驗 schema 夠用；一年後自動解約要留意）＋EDINET API key（免費、含多要素認證）。

## 3. Enrich 與發佈（估 1–2 天）

- 四源 probe 完跑 `enrich --rules-only` → LLM enrich（prompt 已泛化；日文欄位名 Claude 可直接處理）。
- `generate_gh_pages.py`：市場篩選＋Technical Notes 補日本源段落（帳號需求、rate limit、31 天窗、JPX 403 特性）。
- `catalog/full_catalog.md` 重生。

## 4. 驗收條件

1. **零回歸**：既有 134 tests 全綠；台股 924 endpoints state/資料無任何降級（跑 `stats` 前後對照）。
2. 四源皆達 discovered→probed→enriched，最低 endpoint 數：jquants ≥30、edinet ≥15、tdnet ≥8、jpx ≥80；`status=ok` 比例 ≥70%（JPX PDF-only 者標 pdf 不算 error）。
3. `qadris-discovery search --market jp --tag financial_statement` 能找到 EDINET/TDnet/J-Quants 的財報 endpoints（Phase 1 datalake 的三個域——財報/股價/股利——都查得到對應 endpoint）。
4. GH Pages 目錄含 market 篩選、正常發佈。
5. 新來源模組有單元測試（HTTP mock，照既有慣例）；`.env.example`、README、CLAUDE.md 更新（多市場說明＋新 gotchas：J-Quants rate limit、JPX 403、TDnet 31 天）。

## 5. 順序與交付

本擴充是 **QadrisDatalakeJP 的 Phase 0**：目錄出第一版後，datalake 那邊的 dataset 來源調查
（`docs/datasets/` 六段骨架的「來源調查」段）直接引用本目錄。建議實作順序：
框架泛化 → jquants＋edinet（正規 API，快）→ tdnet → jpx（最花時間）→ enrich＋發佈。
合計粗估 **6–11 個工作天**。
