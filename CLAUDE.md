# QadrisDataDiscovery

官方金融資料源探索工具（多市場）。自動發現、探測、標註官方 API endpoint。
現況：台灣（TWSE/TPEx/MOPS/TDCC，924 endpoints）＋日本
（J-Quants/EDINET/TDnet/JPX，230 endpoints）。

> 日本擴充實作紀錄與偏離見 `docs/JP_EXTENSION_PLAN.md`（2026-07-07 實作）。
> jquants/edinet 的 probe 需 API 金鑰（`RSR_JQUANTS_API_KEY`／`RSR_EDINET_API_KEY`，
> 人工註冊），未設定時 probe 明確報「需要金鑰」。

## 多市場架構

- **`registry.py` 的 `SOURCE_REGISTRY` 是 source 的 SSOT**：market（tw/jp）、顯示名、
  base URL 欄位、probe 模組、認證方式（header/query param）。新增來源只改
  registry＋config.py 的 base URL 欄位，CLI/GH Pages/enrich 全部自動跟上。
- `search`/`stats` 支援 `--market tw|jp`；GH Pages catalog.json 每個 endpoint 有 `market` 欄。
- DB schema 不含 market 欄——由 source 經 registry 推導。

## Pipeline

```
discovered → probed → enriched
```

- **discovered**: 從 sitemap/index 頁面解析出的 endpoint，只有名稱和分類，還沒實際打 API
- **probed**: 實際打過 API，有 status/sample_fields/record_count
- **enriched**: 跑過 rule-based + LLM 標註，有 domain_tags/fields_summary

State 只升不降 — 重跑 discovery 不會把已 probed/enriched 的 endpoint 降級（`database.py` upsert 的 CASE 邏輯）。

## 新增資料源 Sitemap 的 Checklist

### 1. 判斷頁面類型

| 類型 | 特徵 | 解析方式 |
|------|------|----------|
| 靜態 HTML | 連結直接在 HTML 裡 | BeautifulSoup（如 MOPS sitemap） |
| JS 動態載入 | 內容由 JavaScript 渲染 | Selenium + BeautifulSoup（如 TWSE report-index） |
| JSON API 目錄 | Swagger/OpenAPI spec | requests 直接解析（如 TWSE/TPEx OpenAPI） |

### 2. 實作 discover_from_xxx()

- 回傳 `list[EndpointInfo]`，所有 endpoint 設 `state="discovered"`
- 放在對應的 `discover_*.py` 模組，整合進 `discover()` 函數
- DB 的 `UNIQUE(source, path)` + upsert 自動處理重複

### 3. 實作 probe 邏輯

每個來源的 probe 方式不同，無法通用化：

**TWSE Web**:
- Selenium 載入每個頁面 → 抓 `form[data-api]` 屬性
- 拼 JSON API URL: `https://www.twse.com.tw/rwd/zh{data-api}?response=json`
- requests GET 取 sample data

**MOPS**:
- GET 頁面 → 解析 form action (`/mops/web/ajax_{page_code}`) 和 hidden inputs
- POST ajax endpoint，需要填入參數預設值
- 不同頁面需要不同參數（co_id, year/month, TYPEK 等）→ 用多組策略輪流嘗試
- 有些頁面回 `window.open` 外部 URL → 需要跟隨
- 有些頁面是多步驟 form（step 1 → step 2）→ 需要跟隨

**通用 probe CLI**: `qadris-discovery probe {source} --limit N`

### 4. Enrichment

- `qadris-discovery enrich --rules-only` — 快，推斷 granularity/coverage 等確定性欄位
- `qadris-discovery enrich` — 含 LLM，每個 endpoint 呼叫一次 Claude 推斷 domain_tags/fields_summary
- LLM enrichment 只對 `status=ok` 的跑（需要 sample_fields）
- `--force` 會跑全部 endpoint（含已有 tags 的），不加只跑 `state=probed` 的

## 已知 Gotchas

- **rule-based enrich 會升 state**: `enrich --rules-only --force` 會把 probed 升成 enriched，導致後續不加 force 的 LLM enrich 找不到目標。如果要分開跑 rules 和 LLM，用 `--force` 配 `--llm-only`
- **Python print buffering**: 背景跑長時間腳本時，output file 可能看起來是空的。加 `flush=True` 或用 `sys.stderr`
- **MOPS 安全機制**: 短時間大量 POST 可能被擋（`頁面無法執行`），需要適當 delay
- **J-Quants rate limit**: Free 方案 5 req/min → probe 間隔 ≥13s（`FREE_PLAN_PROBE_DELAY`）；方案未涵蓋的 endpoint probe 回 401/403 → 標 `skipped`（非 error），欄位資訊已由 spec 站預填
- **TDnet 免費窗口 31 天**: 超窗檔案偶存數日但不可依賴；検索 POST 空 q 回「該当なし」（q 必填）；一覧頁與検索結果頁 markup 不同（前者 oddnew/evennew class、後者 odd/even＋語意 class）
- **JPX 對雲端 client 回 403**（與 UA 無關）：discovery/probe 需在本機跑；檔案 URL 含 CMS 隨機路徑（`tXXvrt…-att`），一律重爬列表頁解析 href，絕不可寫死
- **JPX Excel 舊格式**: 統計檔多為 BIFF .xls（xlrd）；`fetch_excel_fields` 用 magic bytes sniff 引擎，header 列用「非空儲存格最多」啟發式定位
