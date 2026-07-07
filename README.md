# QadrisDataDiscovery

官方金融資料源探索與目錄工具（多市場：台灣＋日本）。自動發現、探測、標註官方 API endpoint，建立結構化的資料目錄。

## 涵蓋資料來源

### 台灣（market=tw）

| 來源 | 說明 | 探索方式 |
|------|------|----------|
| **TWSE OpenAPI** | 證交所開放資料 API | Swagger spec 自動解析 |
| **TWSE Web** | 證交所歷史報表（支援 `&response=json`） | Selenium 解析 report-index + 已知 endpoint |
| **TPEx OpenAPI** | 櫃買中心開放資料 API | Swagger spec 自動解析 |
| **TPEx Web** | 櫃買中心新版網站 API | Selenium 解析首頁 mega menu + 已知 endpoint |
| **MOPS** | 公開資訊觀測站（財報、營收、公告等） | Sitemap 索引 + 多策略 AJAX probe |
| **TDCC OpenAPI** | 集保中心開放資料 API（snapshot-only） | OpenAPI 3.0 spec 自動解析 |

### 日本（market=jp）

| 來源 | 說明 | 探索方式 |
|------|------|----------|
| **J-Quants** | JPX 官方 REST API（V2；需 API key） | 手工 KNOWN_ENDPOINTS（官方 spec 站逐頁核實）＋帶金鑰 probe |
| **EDINET** | 金融廳法定揭露 API v2（需 Subscription-Key，免費註冊） | 書類一覧＋書類取得；endpoint 粒度＝書類種別×取得格式 |
| **TDnet** | 適時開示情報閲覧サービス（決算短信 XBRL） | 固定 URL 規則（I_list 一覧＋検索 POST）；粒度＝檢索面 |
| **JPX 統計頁** | 投資部門別、信用残、空売り等統計（Excel/PDF） | 爬 statistics-equities 頁面樹；粒度＝頁面×檔案序列 |

各來源歸屬市場由 `registry.py` 的 `SOURCE_REGISTRY` 統一管理（新增來源只改一處）。

## Pipeline

每個 endpoint 經歷三階段處理，狀態只升不降：

```
discovered → probed → enriched
```

- **discovered** — 從 sitemap / index 頁面解析出 endpoint URL 與描述
- **probed** — 實際發送 HTTP 請求，取得 status、sample fields、record count
- **enriched** — 經 rule-based 推斷與 LLM 標註，補充 domain tags、fields summary 等語意資訊

## 安裝

```bash
# 建議使用 uv
uv pip install -e .

# 或 pip
pip install -e .
```

### 系統需求

- Python 3.12+
- Chrome / Chromium（Selenium 用於 TWSE/TPEx Web discovery）

## CLI 使用

安裝後可使用 `qadris-discovery` 指令：

### Discovery & Probe

```bash
# 執行各來源的 discovery（會自動存入 SQLite DB）
python -m qadris_datasourcediscovery.discover_tse_openapi
python -m qadris_datasourcediscovery.discover_tse_web
python -m qadris_datasourcediscovery.discover_otc_openapi
python -m qadris_datasourcediscovery.discover_otc_web
python -m qadris_datasourcediscovery.discover_mops

# 日本來源 discovery
python -m qadris_datasourcediscovery.discover_jquants
python -m qadris_datasourcediscovery.discover_edinet
python -m qadris_datasourcediscovery.discover_tdnet
python -m qadris_datasourcediscovery.discover_jpx

# Probe discovered endpoints（從 DB 讀取 state=discovered 的 endpoint）
qadris-discovery probe twse --limit 20
qadris-discovery probe tpex --limit 20
qadris-discovery probe mops --limit 50
qadris-discovery probe jquants --limit 30   # 需 RSR_JQUANTS_API_KEY
qadris-discovery probe edinet --limit 30    # 需 RSR_EDINET_API_KEY
qadris-discovery probe tdnet --limit 10
qadris-discovery probe jpx --limit 200
```

### Enrichment

```bash
# Rule-based enrichment（推斷 granularity、coverage、history_method 等）
qadris-discovery enrich --rules-only

# LLM enrichment（使用 Claude 推斷 domain_tags 和 fields_summary）
qadris-discovery enrich --model claude-haiku-4-5-20251001

# 強制重新標註所有 endpoint
qadris-discovery enrich --force

# 只跑 LLM（搭配 --force 重新標註已有 tags 的）
qadris-discovery enrich --force --llm-only

# Dry run
qadris-discovery enrich --dry-run
```

### 查詢與搜尋

```bash
# 搜尋 endpoint
qadris-discovery search --tag price --source twse
qadris-discovery search --keyword "營收" --json
qadris-discovery search --status ok --history
qadris-discovery search --market jp --tag financial_statement

# 查看單一 endpoint 詳細資訊
qadris-discovery show "twse:/exchangeReport/STOCK_DAY"

# 列出所有 domain tags
qadris-discovery tags

# 統計摘要
qadris-discovery stats
qadris-discovery stats --json
qadris-discovery stats --market jp
```

### 匯出

```bash
# 產生 Markdown 全目錄
python -m qadris_datasourcediscovery.generate_catalog

# 匯出至 Google Sheets（需設定 credentials）
python scripts/export_to_gsheet.py
```

## 專案結構

```
QadrisDataDiscovery/
├── src/qadris_datasourcediscovery/
│   ├── cli.py                  # Typer CLI（search, show, tags, stats, probe, enrich）
│   ├── catalog.py              # EndpointInfo Pydantic model
│   ├── registry.py             # SOURCE_REGISTRY（source→market/base_url/probe/auth，SSOT）
│   ├── config.py               # DiscoverySettings（pydantic-settings, RSR_ prefix）
│   ├── exceptions.py           # 例外體系
│   ├── fetcher.py              # HTTP 工具（requests, Selenium, sample 儲存）
│   ├── enrich.py               # Rule-based + LLM enrichment engine
│   ├── llm.py                  # Claude CLI wrapper（claude -p）
│   ├── generate_catalog.py     # Markdown 報表產生
│   ├── discover_tse_openapi.py # TWSE OpenAPI discovery
│   ├── discover_tse_web.py     # TWSE Web discovery + probe
│   ├── discover_otc_openapi.py # TPEx OpenAPI discovery
│   ├── discover_otc_web.py     # TPEx Web discovery + probe
│   ├── discover_mops.py        # MOPS discovery + probe
│   ├── discover_tdcc_openapi.py# TDCC OpenAPI discovery
│   ├── discover_jquants.py     # J-Quants V2 discovery + probe（API key）
│   ├── discover_edinet.py      # EDINET API v2 discovery + probe（Subscription-Key）
│   ├── discover_tdnet.py       # TDnet discovery + probe
│   ├── discover_jpx.py         # JPX 統計頁 discovery + probe（Excel/PDF）
│   └── store/
│       ├── database.py         # CatalogDB（SQLite persistence）
│       └── schema.py           # DB schema + migration
├── catalog/                    # 產出的目錄檔案（JSON, Markdown）
├── samples/                    # API sample data（.gitignore）
├── prompts/
│   └── enrich_endpoint.txt     # LLM enrichment prompt template
├── scripts/
│   └── export_to_gsheet.py    # Google Sheets 匯出腳本
└── pyproject.toml
```

## 設定

透過環境變數（`RSR_` prefix）或 `.env` 檔案設定：

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `RSR_REQUEST_TIMEOUT` | 30 | HTTP 請求逾時秒數 |
| `RSR_OPENAPI_DELAY` | 1.0 | OpenAPI 請求間隔秒數 |
| `RSR_WEB_DELAY` | 3.0 | Web 請求間隔秒數 |
| `RSR_MAX_SAMPLE_RECORDS` | 5 | 每個 endpoint 儲存的 sample 筆數 |
| `RSR_JQUANTS_API_KEY` | — | J-Quants V2 API key（`x-api-key` header） |
| `RSR_EDINET_API_KEY` | — | EDINET API Subscription-Key（query param） |

## 技術細節

### 資料儲存

- **SQLite**（`catalog/catalog.db`）：主要儲存，以 `(source, path)` 為 unique key
- Upsert 邏輯確保 state 只升不降（discovered → probed → enriched）

### 各來源 Probe 策略

- **TWSE Web**：Selenium 載入頁面 → 抓 `form[data-api]` → 拼 JSON API URL → requests GET
- **TPEx Web**：Selenium 載入頁面 → 抓 `tables.init({action:"..."})` → requests GET（多組參數策略）
- **MOPS**：GET 頁面 → 解析 form action + hidden inputs → POST AJAX（三組參數策略輪流嘗試，支援 `window.open` 跟隨與多步驟 form）
- **J-Quants**：帶 `x-api-key` GET；`pagination_key` 感知（只取首頁樣本）；**Free 方案 5 req/min → probe 間隔 ≥13s**；方案未涵蓋的 endpoint 標 `skipped`（欄位資訊已由 spec 預填）
- **EDINET**：書類一覧掃最近 5 個營業日 → 依 docTypeCode×格式 flag 標註各 endpoint → 實抓一份 type=5 CSV（UTF-16 TSV）樣本
- **TDnet**：抓當日一覧解析「全N件」與欄位；検索面以 POST 帶樣本 query 驗證；**免費窗口僅 31 天**
- **JPX**：下載代表 Excel 檔讀 header（sniff .xls/.xlsx）；PDF-only 表僅驗證可達、標 `response_format=pdf`；**對雲端 client 回 403，需本機執行**；檔案 URL 含 CMS 隨機路徑，一律重爬列表頁解析

### Enrichment

- **Rule-based**：從 endpoint metadata 推斷 granularity、history_method、id_field、request_example、response_format、coverage
- **LLM**：透過 `claude -p` 呼叫 Claude，推斷 domain_tags 和 fields_summary

## License

Private — Qadris internal use.
