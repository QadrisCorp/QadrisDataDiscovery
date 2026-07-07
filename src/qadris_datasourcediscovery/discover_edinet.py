"""EDINET API v2 discovery — 書類一覧＋書類取得，粒度＝「書類種別×取得格式」。

正規 REST（金融廳）：
- 書類一覧 API：``GET /documents.json?date=YYYY-MM-DD&type=2``
- 書類取得 API：``GET /documents/{docID}?type=N``
  （type：1=提出本文書及び監査報告書(XBRL)、2=PDF、3=代替書面・添付文書、
  4=英文ファイル、5=CSV；官方 API 仕様書 Version 2（2026-06）核實）

目錄語意：每個「書類種別×取得格式」是一個 endpoint（如「有価証券報告書 CSV」），
category=書類種別、date_params=提出日、id_field=docID。
書類取得 path 中的 ``#docTypeCode=`` 為目錄註記——docID 需先打書類一覧
（以 docTypeCode 篩選）取得，去掉 fragment 即為真實 URL 樣板。

認證：``Subscription-Key`` query param（``RSR_EDINET_API_KEY``，免費註冊）。
"""

from __future__ import annotations

import csv
import io
import logging
import zipfile
from datetime import date, timedelta
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    auth_query_params,
    delay,
    save_sample,
)

logger = logging.getLogger(__name__)

# probe 時掃描的提出日數（往前找最近的營業日）
PROBE_DAYS = 5

# 書類一覧 API 的 results 欄位（官方仕様書核實）
LIST_FIELDS = [
    "docID",
    "edinetCode",
    "secCode",
    "JCN",
    "filerName",
    "fundCode",
    "ordinanceCode",
    "formCode",
    "docTypeCode",
    "periodStart",
    "periodEnd",
    "submitDateTime",
    "docDescription",
    "xbrlFlag",
    "pdfFlag",
]

# 書類種別（docTypeCode → 官方名稱／granularity）；挑股票研究相關者
DOC_TYPES: list[dict[str, str]] = [
    {"code": "120", "name": "有価証券報告書", "granularity": "yearly"},
    {"code": "130", "name": "訂正有価証券報告書", "granularity": "yearly"},
    {"code": "140", "name": "四半期報告書", "granularity": "quarterly"},
    {"code": "150", "name": "訂正四半期報告書", "granularity": "quarterly"},
    {"code": "160", "name": "半期報告書", "granularity": "semiannual"},
    {"code": "170", "name": "訂正半期報告書", "granularity": "semiannual"},
    {"code": "180", "name": "臨時報告書", "granularity": ""},
    {"code": "350", "name": "大量保有報告書", "granularity": ""},
    {"code": "360", "name": "訂正大量保有報告書", "granularity": ""},
]

# 取得格式（type 參數值／可用性 flag 欄位／response_format）
FORMATS: list[dict[str, str]] = [
    {"key": "csv", "type": "5", "flag": "csvFlag", "response_format": "csv"},
    {"key": "xbrl", "type": "1", "flag": "xbrlFlag", "response_format": "zip"},
    {"key": "pdf", "type": "2", "flag": "pdfFlag", "response_format": "pdf"},
]

_QUARTERLY_ABOLISHED_NOTE = (
    "四半期報告書制度 2024-04 廢止（金商法改正），僅歷史資料；"
    "Q1/Q3 季頻財務之後唯一來源為 TDnet 決算短信"
)


def _fetch_doc_path(doc_type_code: str, type_num: str) -> str:
    """組合書類取得 endpoint 的目錄 path（fragment 為註記）。"""
    return f"/documents/{{docID}}?type={type_num}#docTypeCode={doc_type_code}"


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Build EDINET endpoint list（書類一覧＋書類種別×格式，無網路）。"""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []

    endpoints.append(
        EndpointInfo(
            source="edinet",
            endpoint_type="openapi",
            path="/documents.json",
            description="書類一覧 API（提出書類一覧及びメタデータ）",
            category="書類一覧",
            method="GET",
            supports_history=True,
            date_params=["date"],
            sample_fields=LIST_FIELDS[:15],
            id_field="docID",
            response_format="json",
            notes=(
                "params: date=YYYY-MM-DD（提出日）, type=1|2（1=メタデータのみ, "
                "2=提出書類一覧含む）, Subscription-Key | 回溯上限約 10 年"
            ),
            state="discovered",
        )
    )

    for dt in DOC_TYPES:
        for fmt in FORMATS:
            notes_parts = [
                f"docTypeCode={dt['code']}",
                (
                    "docID 先由 /documents.json?date=…（篩 docTypeCode）取得；"
                    f"僅 {fmt['flag']}=1 的書類可用此格式"
                ),
            ]
            if dt["code"] in ("140", "150"):
                notes_parts.append(_QUARTERLY_ABOLISHED_NOTE)

            endpoints.append(
                EndpointInfo(
                    source="edinet",
                    endpoint_type="openapi",
                    path=_fetch_doc_path(dt["code"], fmt["type"]),
                    description=f"{dt['name']} — {fmt['key'].upper()} 取得",
                    category=dt["name"],
                    method="GET",
                    supports_history=True,
                    date_params=["date"],
                    granularity=dt["granularity"],
                    id_field="docID",
                    response_format=fmt["response_format"],
                    notes=" | ".join(notes_parts),
                    state="discovered",
                )
            )

    logger.info(
        "EDINET: %d endpoints (1 list + %d 種別×格式)",
        len(endpoints),
        len(endpoints) - 1,
    )
    return endpoints


def _recent_business_days(n: int, today: date | None = None) -> list[str]:
    """回傳從昨天往回的 n 個平日（YYYY-MM-DD）。"""
    if today is None:
        today = date.today()
    days: list[str] = []
    d = today - timedelta(days=1)
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d.isoformat())
        d -= timedelta(days=1)
    return days


def _extract_csv_fields(zip_bytes: bytes) -> list[str]:
    """從書類取得 API（type=5）回傳的 zip 取第一個 CSV 的欄位名。

    EDINET CSV 為 UTF-16 編碼、tab 分隔。
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            return []
        with zf.open(csv_names[0]) as f:
            text = f.read().decode("utf-16")
        reader = csv.reader(io.StringIO(text), delimiter="\t")
        header = next(reader, [])
        return [h.strip() for h in header if h.strip()]


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered EDINET endpoints.

    打書類一覧 API（掃最近 PROBE_DAYS 個營業日），據以標註各
    書類種別×格式 endpoint 的 status；並實際抓一份 type=5 CSV 樣本。

    Raises:
        ConfigurationError: 未設定 RSR_EDINET_API_KEY（明確報錯，不靜默失敗）。
    """
    if settings is None:
        settings = DiscoverySettings()

    settings.require_api_key("edinet")

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="edinet", state="discovered")

    if not discovered:
        logger.info("No discovered EDINET endpoints to probe")
        return []

    to_probe = discovered[:limit]
    base = settings.get_base_url("edinet", "openapi")
    session = _create_session(settings=settings, source="edinet")
    auth = auth_query_params("edinet", settings=settings)

    # --- 掃書類一覧（多個營業日彙總） ---
    all_results: list[dict[str, Any]] = []
    list_status = "error"
    list_error_note = ""
    for day in _recent_business_days(PROBE_DAYS):
        try:
            resp = session.get(
                f"{base}/documents.json",
                params={"date": day, "type": "2", **auth},
                timeout=settings.request_timeout,
            )
            if resp.status_code in (401, 403):
                list_status = "error"
                list_error_note = f"HTTP {resp.status_code}（金鑰無效或未訂閱）"
                break
            payload = resp.json()
        except Exception as e:  # noqa: BLE001 — 單日失敗不中斷掃描
            logger.warning("EDINET list fetch failed for %s: %s", day, e)
            continue
        results = payload.get("results") or []
        logger.info("EDINET %s: %d documents", day, len(results))
        if results:
            list_status = "ok"
            all_results.extend(results)
        elif list_status != "ok":
            list_status = "empty"
        delay(settings.openapi_delay)

    by_doc_type: dict[str, list[dict[str, Any]]] = {}
    for r in all_results:
        by_doc_type.setdefault(str(r.get("docTypeCode", "")), []).append(r)

    # --- 抓一份 type=5 CSV 樣本（優先有報 120） ---
    csv_fields: list[str] = []
    csv_doc_id = ""
    csv_candidates = [
        r
        for code in ("120", "160", "140", "350", "180")
        for r in by_doc_type.get(code, [])
        if str(r.get("csvFlag", "")) == "1"
    ]
    if csv_candidates:
        csv_doc_id = str(csv_candidates[0].get("docID", ""))
        try:
            resp = session.get(
                f"{base}/documents/{csv_doc_id}",
                params={"type": "5", **auth},
                timeout=settings.request_timeout,
            )
            resp.raise_for_status()
            csv_fields = _extract_csv_fields(resp.content)
            logger.info("CSV sample from %s: fields=%s", csv_doc_id, csv_fields)
        except Exception as e:  # noqa: BLE001
            logger.warning("EDINET CSV sample fetch failed (%s): %s", csv_doc_id, e)

    # --- 標註各 endpoint ---
    results_out: list[EndpointInfo] = []
    for ep in to_probe:
        updates: dict[str, Any] = {"state": "probed"}

        if ep.path == "/documents.json":
            updates["status"] = list_status
            updates["record_count"] = len(all_results)
            if all_results:
                updates["sample_fields"] = [
                    str(k) for k in all_results[0].keys()
                ][:15]
                sample_path = settings.samples_dir / "edinet" / "documents_list.json"
                save_sample(
                    all_results,
                    sample_path,
                    max_records=settings.max_sample_records,
                )
                updates["sample_path"] = str(sample_path)
            if list_error_note:
                updates["notes"] = (ep.notes + f" | probe: {list_error_note}").strip(
                    " | "
                )
        else:
            # 書類種別×格式：由一覧掃描結果標註
            code = ep.path.split("#docTypeCode=")[-1]
            fmt_flag = {
                "type=5": "csvFlag",
                "type=1": "xbrlFlag",
                "type=2": "pdfFlag",
            }
            flag_field = next(
                (v for k, v in fmt_flag.items() if k in ep.path), ""
            )
            docs = by_doc_type.get(code, [])
            matched = [
                d for d in docs if not flag_field or str(d.get(flag_field, "")) == "1"
            ]
            if list_error_note:
                updates["status"] = "error"
                updates["notes"] = (ep.notes + f" | probe: {list_error_note}").strip(
                    " | "
                )
            else:
                updates["record_count"] = len(matched)
                updates["status"] = "ok" if matched else "empty"
                if matched:
                    example = str(matched[0].get("docID", ""))
                    updates["notes"] = (
                        ep.notes
                        + f" | probe: 近{PROBE_DAYS}營業日 {len(matched)} 件"
                        + (f"，例 docID={example}" if example else "")
                    ).strip(" | ")
                else:
                    updates["notes"] = (
                        ep.notes + f" | probe: 近{PROBE_DAYS}營業日 0 件"
                    ).strip(" | ")
            # CSV 樣本欄位回填給對應種別的 CSV endpoint
            if csv_fields and "type=5" in ep.path and csv_doc_id:
                sample_doc_type = next(
                    (
                        str(r.get("docTypeCode", ""))
                        for r in csv_candidates
                        if str(r.get("docID", "")) == csv_doc_id
                    ),
                    "",
                )
                if code == sample_doc_type:
                    updates["sample_fields"] = csv_fields[:15]

        results_out.append(ep.model_copy(update=updates))

    ok = sum(1 for r in results_out if r.status == "ok")
    logger.info("EDINET probe done: %d ok / %d total", ok, len(results_out))
    return results_out


def main() -> None:
    """Run EDINET discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("EDINET: %d endpoints saved to DB", len(endpoints))


if __name__ == "__main__":
    main()
