"""J-Quants API V2 discovery — 手工 KNOWN_ENDPOINTS 清單＋API key probe。

J-Quants 無公開 swagger/OpenAPI spec，endpoint 清單由官方 spec 站
（https://jpx-jquants.com/en/spec/*，2026-07-07 逐頁核實）手工整理；
sample_fields 直接取自 spec 文件的 response 欄位表，
故 **方案未涵蓋（probe 被擋）的 endpoint 仍有欄位資訊可供 enrich**。

認證：V2 以 ``x-api-key`` header 認證（``RSR_JQUANTS_API_KEY``）。
Rate limit：Free 方案 5 req/min → probe 間隔至少 13 秒。
分頁：回應含 ``pagination_key`` 時代表還有下頁；probe 只取首頁樣本。
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.fetcher import _create_session, delay, save_sample

logger = logging.getLogger(__name__)

# Free 方案 5 req/min → 間隔 ≥13s（其他方案更寬，取保守值）
FREE_PLAN_PROBE_DELAY = 13.0

# spec 站逐頁核實的 V2 endpoint 清單（2026-07-07）。
# plan：該 endpoint 最低可用方案（Free ⊂ Light ⊂ Standard ⊂ Premium；Add-on 另計）。
# probe_params：probe 時帶的參數；"{date}" 由 probe 換成近期營業日。
# probe_params=None 表示無法獨立 probe（需前置請求取得 id）。
KNOWN_ENDPOINTS: list[dict[str, Any]] = [
    # --- Equities ---
    {
        "path": "/equities/master",
        "description": "Listed Issue Master（上場銘柄一覧，point-in-time）",
        "category": "Equities",
        "plan": "Free",
        "since": "2008-05-07",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "Code", "CoName", "CoNameEn", "S17", "S17Nm", "S33",
            "S33Nm", "ScaleCat", "Mkt", "MktNm", "Mrgn", "MrgnNm", "ProdCat",
        ],
        "notes": "params: code, date",
    },
    {
        "path": "/equities/bars/daily",
        "description": "Stock Prices OHLC（株価四本値，含調整價與 AdjFactor）",
        "category": "Equities",
        "plan": "Free",
        "since": "2008-05-07",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "Code", "O", "H", "L", "C", "UL", "LL", "Vo", "Va",
            "AdjFactor", "AdjO", "AdjH", "AdjL", "AdjC", "AdjVo",
        ],
        "notes": (
            "params: code, date, from, to, pagination_key | "
            "AdjFactor 僅涵蓋分割/併合/rights issue，不含配息"
        ),
    },
    {
        "path": "/equities/bars/daily/am",
        "description": "Morning Session Stock Prices（前場四本値）",
        "category": "Equities",
        "plan": "Premium",
        "since": "recent only",
        "date_params": [],
        "probe_params": {"code": "72030"},
        "sample_fields": ["Date", "Code", "MO", "MH", "ML", "MC", "MVo", "MVa"],
        "notes": "params: code, pagination_key | 僅當日前場",
    },
    {
        "path": "/equities/bars/minute",
        "description": "Minute Stock Prices OHLC（分足）",
        "category": "Equities",
        "plan": "Add-on (Stock Prices minute/Tick)",
        "since": "2 years rolling",
        "date_params": ["date", "from", "to"],
        "probe_params": {"code": "72030", "date": "{date}"},
        "sample_fields": ["Date", "Time", "Code", "O", "H", "L", "C", "Vo", "Va"],
        "notes": (
            "params: code, date, from, to, pagination_key | "
            "add-on rate limit 60/min"
        ),
    },
    {
        "path": "/equities/trades",
        "description": "Stock Prices Tick（ティックデータ）",
        "category": "Equities",
        "plan": "Add-on (Stock Prices minute/Tick)",
        "since": "2 years rolling",
        "date_params": [],
        "probe_params": None,
        "sample_fields": [],
        "notes": "CSV bulk download only（經 /bulk 取得），無 REST GET",
    },
    {
        "path": "/equities/investor-types",
        "description": "Trading by Type of Investors（投資部門別売買状況，週次）",
        "category": "Equities",
        "plan": "Light",
        "since": "2008-01-16",
        "date_params": ["from", "to"],
        "granularity": "weekly",
        "probe_params": {"section": "TSEPrime"},
        "sample_fields": [
            "PubDate", "StDate", "EnDate", "Section", "PropSell", "PropBuy",
            "PropTot", "PropBal", "BrkSell", "BrkBuy", "TotSell", "TotBuy",
        ],
        "notes": "params: section, from, to, pagination_key | 市場層級（無個股粒度）",
    },
    {
        "path": "/equities/earnings-calendar",
        "description": "Earnings Calendar（決算発表予定日）",
        "category": "Equities",
        "plan": "Free",
        "since": "recent only",
        "date_params": [],
        "granularity": "snapshot",
        "supports_history": False,
        "probe_params": {},
        "sample_fields": ["Date", "Code", "CoName", "FY", "SectorNm", "FQ", "Section"],
        "notes": "params: pagination_key",
    },
    # --- Financials ---
    {
        "path": "/fins/summary",
        "description": "Financial Data Summary（決算短信サマリ財務情報）",
        "category": "Financials",
        "plan": "Free",
        "since": "2008-07-07",
        "date_params": ["date"],
        "granularity": "quarterly",
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "DiscDate", "DiscTime", "Code", "DiscNo", "DocType", "CurPerType",
            "CurPerSt", "CurPerEn", "Sales", "OP", "OdP", "NP", "EPS", "DEPS",
        ],
        "notes": (
            "params: code, date, cursor, pagination_key | "
            "endpoint 專屬 rate limit 60/min"
        ),
    },
    {
        "path": "/fins/details",
        "description": "Financial Statement Data BS/PL/CF（財務諸表明細）",
        "category": "Financials",
        "plan": "Premium",
        "since": "2009-01-13",
        "date_params": ["date"],
        "granularity": "quarterly",
        "probe_params": {"date": "{date}"},
        "sample_fields": ["DiscDate", "DiscTime", "Code", "DiscNo", "DocType", "FS"],
        "notes": (
            "params: code, date, cursor, pagination_key | "
            "endpoint 專屬 rate limit 60/min"
        ),
    },
    {
        "path": "/fins/dividend",
        "description": "Cash Dividend Data（配当金明細）",
        "category": "Financials",
        "plan": "Premium",
        "since": "2013-02-20",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "PubDate", "PubTime", "Code", "RefNo", "StatCode", "BoardDate",
            "IFCode", "FRCode", "IFTerm", "DivRate", "RecDate", "ExDate",
            "ActRecDate", "PayDate", "DistAmt",
        ],
        "notes": "params: code, from, to, date, pagination_key",
    },
    # --- Markets ---
    {
        "path": "/markets/breakdown",
        "description": "Breakdown Trading Data(売買内訳データ)",
        "category": "Markets",
        "plan": "Premium",
        "since": "2015-04-01",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "Code", "LongSellVa", "ShrtNoMrgnVa", "MrgnSellNewVa",
            "MrgnSellCloseVa", "LongBuyVa", "MrgnBuyNewVa", "MrgnBuyCloseVa",
            "LongSellVo", "ShrtNoMrgnVo", "LongBuyVo",
        ],
        "notes": "params: code, from, to, date, pagination_key",
    },
    {
        "path": "/markets/calendar",
        "description": "Trading Calendar（取引カレンダー）",
        "category": "Markets",
        "plan": "Free",
        "since": "2008-01-01",
        "date_params": ["from", "to"],
        "probe_params": {},
        "sample_fields": ["Date", "HolDiv"],
        "notes": "params: hol_div, from, to",
    },
    {
        "path": "/markets/margin-alert",
        "description": (
            "Margin Trading Outstanding — daily publication（日々公表信用取引残高）"
        ),
        "category": "Markets",
        "plan": "Standard",
        "since": "2008-05-08",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "PubDate", "Code", "AppDate", "PubReason", "ShrtOut", "ShrtOutChg",
            "ShrtOutRatio", "LongOut", "LongOutChg", "LongOutRatio", "SLRatio",
        ],
        "notes": "params: code, from, to, date, pagination_key | 僅規制/注意喚起銘柄",
    },
    {
        "path": "/markets/margin-interest",
        "description": "Margin Trading Outstandings（信用取引週末残高）",
        "category": "Markets",
        "plan": "Standard",
        "since": "2012-02-10",
        "date_params": ["date", "from", "to"],
        "granularity": "weekly",
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "Code", "ShrtVol", "LongVol", "ShrtNegVol", "LongNegVol",
            "ShrtStdVol", "LongStdVol", "IssType",
        ],
        "notes": "params: code, from, to, date, pagination_key | 週末残高（週次）",
    },
    {
        "path": "/markets/short-ratio",
        "description": "Short Sale Value and Ratio by Sector（業種別空売り比率）",
        "category": "Markets",
        "plan": "Standard",
        "since": "2008-11-05",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "S33", "SellExShortVa", "ShrtWithResVa", "ShrtNoResVa",
        ],
        "notes": "params: from, to, date, pagination_key | 業種層級",
    },
    {
        "path": "/markets/short-sale-report",
        "description": (
            "Outstanding Short Selling Positions（空売り残高報告，≥0.5% 部位）"
        ),
        "category": "Markets",
        "plan": "Standard",
        "since": "2013-11-07",
        "date_params": ["disc_date", "disc_date_from", "disc_date_to", "calc_date"],
        "probe_params": {"disc_date": "{date}"},
        "sample_fields": [
            "DiscDate", "CalcDate", "Code", "SSName", "SSAddr", "DICName",
            "FundName", "ShrtPosToSO", "ShrtPosShares", "ShrtPosUnits",
        ],
        "notes": (
            "params: code, disc_date, disc_date_from, disc_date_to, "
            "calc_date, pagination_key"
        ),
    },
    # --- Indices ---
    {
        "path": "/indices/bars/daily",
        "description": "Indices OHLC（指数四本値）",
        "category": "Indices",
        "plan": "Standard",
        "since": "2008-05-07",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": ["Date", "Code", "O", "H", "L", "C"],
        "notes": "params: code, date, from, to, pagination_key",
    },
    {
        "path": "/indices/bars/daily/topix",
        "description": "TOPIX Prices OHLC（TOPIX指数四本値）",
        "category": "Indices",
        "plan": "Light",
        "since": "2008-05-07",
        "date_params": ["from", "to"],
        "probe_params": {},
        "sample_fields": ["Date", "O", "H", "L", "C"],
        "notes": "params: from, to, pagination_key",
    },
    # --- Derivatives ---
    {
        "path": "/derivatives/bars/daily/futures",
        "description": "Futures OHLC（先物四本値）",
        "category": "Derivatives",
        "plan": "Premium",
        "since": "2008-05-07",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Code", "ProdCat", "Date", "O", "H", "L", "C", "MO", "MH", "ML",
            "MC", "EO", "EH", "EL", "EC",
        ],
        "notes": "params: category, date, contract_flag, pagination_key",
    },
    {
        "path": "/derivatives/bars/daily/options",
        "description": "Options OHLC（オプション四本値）",
        "category": "Derivatives",
        "plan": "Premium",
        "since": "2008-05-07",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Code", "ProdCat", "UndSSO", "Date", "O", "H", "L", "C", "MO",
            "MH", "ML", "MC",
        ],
        "notes": "params: category, code, date, contract_flag, pagination_key",
    },
    {
        "path": "/derivatives/bars/daily/options/225",
        "description": "Nikkei 225 Index Option OHLC（日経225オプション四本値）",
        "category": "Derivatives",
        "plan": "Standard",
        "since": "2008-05-07",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "Date", "Code", "O", "H", "L", "C", "EO", "EH", "EL", "EC", "Vo",
            "OI", "Va", "CM",
        ],
        "notes": "params: date, pagination_key",
    },
    # --- TDnet add-on ---
    {
        "path": "/td/list",
        "description": (
            "TDnet/Company Disclosure Index List（適時開示インデックス一覧）"
        ),
        "category": "TDnet",
        "plan": "Add-on (TDnet/Company Disclosure)",
        "since": "5 years rolling",
        "date_params": ["date", "from", "to"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "DiscNo", "Code", "Name", "DiscDate", "DiscTime", "Title",
            "DiscStatus", "RevNo", "DiscItems", "Docs",
        ],
        "notes": (
            "params: date, code, from, to, discItems, cursor, pagination_key | "
            "add-on rate limit 100/min"
        ),
    },
    {
        "path": "/td/files",
        "description": "TDnet/Company Disclosure Files（開示資料ファイル取得）",
        "category": "TDnet",
        "plan": "Add-on (TDnet/Company Disclosure)",
        "since": "5 years rolling",
        "date_params": [],
        "supports_history": False,
        "probe_params": None,
        "sample_fields": [
            "discNo", "files", "files.pdf", "files.summaryPdf", "files.xbrl",
        ],
        "notes": "params: discNo, docs | 需先由 /td/list 取得 discNo，無法獨立 probe",
    },
    {
        "path": "/td/bulk",
        "description": (
            "TDnet/Company Disclosure Index CSV Download（インデックス一括DL）"
        ),
        "category": "TDnet",
        "plan": "Add-on (TDnet/Company Disclosure)",
        "since": "5 years rolling",
        "date_params": [],
        "supports_history": False,
        "probe_params": {},
        "sample_fields": ["lastUpdated", "url"],
        "notes": "回傳 CSV 下載 URL",
    },
    # --- Bulk ---
    {
        "path": "/bulk/list",
        "description": "List of Downloadable Files（CSV 一括DL可能ファイル一覧）",
        "category": "Bulk",
        "plan": "Light",
        "since": "-",
        "date_params": ["date", "from", "to"],
        "supports_history": False,
        "probe_params": {"endpoint": "/equities/master"},
        "sample_fields": ["Key", "LastModified", "Size"],
        "notes": "params: endpoint, date, from, to | 付費方案限定（Free 無 CSV DL）",
    },
    {
        "path": "/bulk/get",
        "description": "Get File Download URL（CSV ファイル取得 URL）",
        "category": "Bulk",
        "plan": "Light",
        "since": "-",
        "date_params": [],
        "supports_history": False,
        "probe_params": None,
        "sample_fields": ["url"],
        "notes": (
            "params: key, endpoint, date | 需先由 /bulk/list 取得 key，"
            "無法獨立 probe"
        ),
    },
    # --- EDINET-derived ---
    {
        "path": "/edinet/major-shareholders",
        "description": "Major Shareholders from EDINET（大株主状況，有報由来）",
        "category": "EDINET",
        "plan": "Standard",
        "since": "2016-06-01",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "DocId", "Code", "EdinetCode", "FilerName", "FilerNameEn",
            "DocTypeCode", "SubDate", "SubTime", "PerSt", "PerEn", "Hldrs",
        ],
        "notes": "params: edinet_code, code, date, pagination_key",
    },
    {
        "path": "/edinet/cross-shareholdings",
        "description": "Cross-Shareholdings from EDINET（政策保有株式，有報由来）",
        "category": "EDINET",
        "plan": "Standard",
        "since": "2020-03-31",
        "date_params": ["date"],
        "probe_params": {"date": "{date}"},
        "sample_fields": [
            "DocId", "Code", "EdinetCode", "FilerName", "FilerNameEn",
            "DocTypeCode", "SubDate",
        ],
        "notes": "params: edinet_code, code, date, pagination_key",
    },
]


def _probe_date(today: date | None = None) -> str:
    """回傳約 13 週前的最近平日（YYYY-MM-DD）。

    Free 方案資料延遲 12 週，往前多留一週 buffer；
    若落在週末則往前調到週五（遇日本假日時 API 回 empty，由呼叫端重試）。
    """
    if today is None:
        today = date.today()
    d = today - timedelta(weeks=13)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.isoformat()


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Build J-Quants endpoint list from the hand-curated spec catalog（無網路）。"""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []
    for ep_def in KNOWN_ENDPOINTS:
        notes_parts = [f"plan={ep_def['plan']}", f"since={ep_def['since']}"]
        if ep_def.get("notes"):
            notes_parts.append(ep_def["notes"])

        ep = EndpointInfo(
            source="jquants",
            endpoint_type="openapi",
            path=ep_def["path"],
            description=ep_def["description"],
            category=ep_def["category"],
            method="GET",
            supports_history=ep_def.get("supports_history", True),
            date_params=list(ep_def.get("date_params", [])),
            sample_fields=list(ep_def.get("sample_fields", []))[:15],
            granularity=ep_def.get("granularity", ""),
            notes=" | ".join(notes_parts),
            state="discovered",
        )
        endpoints.append(ep)

    logger.info("J-Quants: %d known endpoints from spec catalog", len(endpoints))
    return endpoints


def _classify_response(
    ep: EndpointInfo, status_code: int, payload: Any
) -> dict[str, Any]:
    """依 HTTP 狀態與 payload 決定 probe 結果欄位更新。"""
    updates: dict[str, Any] = {"state": "probed"}

    if status_code in (401, 403):
        updates["status"] = "skipped"
        updates["notes"] = (
            ep.notes + " | probe: 401/403（方案未涵蓋或金鑰無效，見 plan=）"
        ).strip(" | ")
        return updates
    if status_code == 429:
        updates["status"] = "error"
        updates["notes"] = (ep.notes + " | probe: 429 rate limited").strip(" | ")
        return updates
    if status_code != 200 or not isinstance(payload, dict):
        updates["status"] = "error"
        updates["notes"] = (ep.notes + f" | probe: HTTP {status_code}").strip(" | ")
        return updates

    data = payload.get("data")
    if isinstance(data, list):
        updates["record_count"] = len(data)
        updates["status"] = "ok" if data else "empty"
        if data and isinstance(data[0], dict):
            updates["sample_fields"] = [str(k) for k in data[0].keys()][:15]
        if payload.get("pagination_key"):
            updates["notes"] = (
                ep.notes + " | paginated (first page sampled)"
            ).strip(" | ")
    elif "url" in payload or "lastUpdated" in payload:
        # /td/bulk、/bulk/get 類：回傳下載 URL 物件
        updates["record_count"] = 1
        updates["status"] = "ok"
        updates["sample_fields"] = [str(k) for k in payload.keys()][:15]
    else:
        updates["status"] = "empty"
    return updates


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered J-Quants endpoints with the configured API key.

    Raises:
        ConfigurationError: 未設定 RSR_JQUANTS_API_KEY（明確報錯，不靜默失敗）。
    """
    if settings is None:
        settings = DiscoverySettings()

    settings.require_api_key("jquants")

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="jquants", state="discovered")

    if not discovered:
        logger.info("No discovered J-Quants endpoints to probe")
        return []

    to_probe = discovered[:limit]
    probe_defs = {d["path"]: d for d in KNOWN_ENDPOINTS}
    probe_date = _probe_date()
    base = settings.get_base_url("jquants", "openapi")
    session = _create_session(settings=settings, source="jquants")
    probe_delay = max(settings.openapi_delay, FREE_PLAN_PROBE_DELAY)

    logger.info(
        "=== Probing %d/%d J-Quants endpoints (date=%s, delay=%.0fs) ===",
        len(to_probe),
        len(discovered),
        probe_date,
        probe_delay,
    )

    results: list[EndpointInfo] = []
    for ep in to_probe:
        ep_def = probe_defs.get(ep.path, {})
        params_template = ep_def.get("probe_params")

        if params_template is None:
            results.append(
                ep.model_copy(
                    update={
                        "state": "probed",
                        "status": "skipped",
                        "notes": (
                            ep.notes + " | probe: 需前置請求取得 id，未獨立 probe"
                        ).strip(" | "),
                    }
                )
            )
            continue

        params = {
            k: (probe_date if v == "{date}" else v)
            for k, v in params_template.items()
        }
        url = f"{base}{ep.path}"
        logger.info("Probing: %s params=%s", ep.path, params)

        try:
            resp = session.get(url, params=params, timeout=settings.request_timeout)
            try:
                payload = resp.json()
            except ValueError:
                payload = None
            updates = _classify_response(ep, resp.status_code, payload)
        except Exception as e:  # noqa: BLE001 — probe 全部失敗不中斷其他 endpoint
            updates = {
                "state": "probed",
                "status": "error",
                "notes": (ep.notes + f" | probe error: {e}").strip(" | "),
            }

        if updates.get("status") == "ok" and isinstance(payload, dict):
            sample_path = (
                settings.samples_dir
                / "jquants"
                / f"{ep.path.strip('/').replace('/', '_')}.json"
            )
            data = payload.get("data", payload)
            save_sample(data, sample_path, max_records=settings.max_sample_records)
            updates["sample_path"] = str(sample_path)

        results.append(ep.model_copy(update=updates))
        delay(probe_delay)

    ok = sum(1 for r in results if r.status == "ok")
    skipped = sum(1 for r in results if r.status == "skipped")
    logger.info(
        "J-Quants probe done: %d ok, %d skipped (plan-gated/id-required), %d total",
        ok,
        skipped,
        len(results),
    )
    return results


def main() -> None:
    """Run J-Quants discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("J-Quants: %d endpoints saved to DB", len(endpoints))


if __name__ == "__main__":
    main()
