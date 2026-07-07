# QadrisDataDiscovery

官方金融資料源探索工具。自動發現、探測、標註官方 API endpoint。
現況：台灣（TWSE/TPEx/MOPS/TDCC，DB 924 endpoints）；**日本擴充建置中**。

> **進行中：日本市場擴充**——實作 SSOT 見 `docs/JP_EXTENSION_PLAN.md`
> （框架泛化＋jquants/edinet/tdnet/jpx 四源，2026-07-07 定案，不走 steward、Bear 直接開 agent 實作）。
> 開工前先讀該檔；完成一節就在該檔勾銷並補記偏離。

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
