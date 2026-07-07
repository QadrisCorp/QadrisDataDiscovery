"""TDnet（適時開示情報閲覧サービス）discovery — 檢索面＋檔案取得模式。

`release.tdnet.info` 無官方免費 API，但 URL 規則固定（2026-07-07 實測核實）：
- 指定日一覧：``GET /inbs/I_list_{頁碼}_{YYYYMMDD}.html``（每頁 100 件，含「全N件」）
- 検索：``POST /onsf/TDJFSearch/TDJFSearch``（params: t0/t1=期間 YYYYMMDD、
  q=キーワード（コード／会社名／表題）、m=0）
- 開示資料 PDF：``/inbs/1401{YYYYMMDD}{連番}.pdf``
- 決算短信等 XBRL zip：``/inbs/0812{YYYYMMDD}{連番}.zip``
  （內容 XBRLData/Summary/*-ixbrl.htm＋Attachment）

**免費窗口僅 31 天**（超窗檔案偶存數日但不可依賴）——記入各 endpoint notes。
endpoint 粒度＝檢索面（當日一覧、按代碼、按会社名、按開示種別、期間指定）
＋檔案取得模式（PDF／XBRL zip）；path 的 ``#facet=`` 為目錄註記。
"""

from __future__ import annotations

import logging
import re
from datetime import date, timedelta
from typing import Any

from bs4 import BeautifulSoup

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.fetcher import _create_session, delay, save_sample

logger = logging.getLogger(__name__)

SEARCH_PATH = "/onsf/TDJFSearch/TDJFSearch"

# 一覧頁欄位（2026-07-07 實測）
LIST_FIELDS = ["時刻", "コード", "会社名", "表題", "XBRL", "上場取引所", "更新履歴"]

_WINDOW_NOTE = "免費窗口僅 31 天（超窗檔案偶存數日，不可依賴）"

KNOWN_ENDPOINTS: list[dict[str, Any]] = [
    {
        "path": "/inbs/I_main_00.html",
        "description": "適時開示閲覧サービス首頁（嵌入本日最新一覧）",
        "category": "開示一覧",
        "supports_history": False,
        "date_params": [],
        "granularity": "snapshot",
        "response_format": "html_table",
        "notes": f"本日一覧入口（iframe 指向 I_list_001_本日）| {_WINDOW_NOTE}",
    },
    {
        "path": "/inbs/I_list_{page}_{YYYYMMDD}.html",
        "description": "指定日開示一覧（每頁 100 件，頁碼 001 起）",
        "category": "開示一覧",
        "supports_history": True,
        "date_params": ["YYYYMMDD"],
        "granularity": "daily",
        "response_format": "html_table",
        "sample_fields": LIST_FIELDS,
        "notes": f"頁首「全N件」為當日總件數 | {_WINDOW_NOTE}",
    },
    {
        "path": f"{SEARCH_PATH}#facet=code",
        "description": "開示検索 — 按銘柄コード",
        "category": "開示検索",
        "method": "POST",
        "supports_history": True,
        "date_params": ["t0", "t1"],
        "granularity": "daily",
        "response_format": "html_table",
        "sample_fields": LIST_FIELDS,
        "notes": f"POST q=銘柄コード, t0/t1=YYYYMMDD, m=0 | {_WINDOW_NOTE}",
    },
    {
        "path": f"{SEARCH_PATH}#facet=company",
        "description": "開示検索 — 按会社名",
        "category": "開示検索",
        "method": "POST",
        "supports_history": True,
        "date_params": ["t0", "t1"],
        "granularity": "daily",
        "response_format": "html_table",
        "sample_fields": LIST_FIELDS,
        "notes": f"POST q=会社名, t0/t1=YYYYMMDD, m=0 | {_WINDOW_NOTE}",
    },
    {
        "path": f"{SEARCH_PATH}#facet=disclosure-type",
        "description": "開示検索 — 按開示種別キーワード（如「決算短信」）",
        "category": "開示検索",
        "method": "POST",
        "supports_history": True,
        "date_params": ["t0", "t1"],
        "granularity": "daily",
        "response_format": "html_table",
        "sample_fields": LIST_FIELDS,
        "notes": (
            "POST q=表題キーワード（決算短信／業績予想修正／配当…）, "
            f"t0/t1=YYYYMMDD, m=0 | {_WINDOW_NOTE}"
        ),
    },
    {
        "path": f"{SEARCH_PATH}#facet=code-window",
        "description": "開示検索 — 按銘柄コード（全 31 天窗，個股開示歷史）",
        "category": "開示検索",
        "method": "POST",
        "supports_history": True,
        "date_params": ["t0", "t1"],
        "granularity": "daily",
        "response_format": "html_table",
        "sample_fields": LIST_FIELDS,
        "notes": (
            "POST q=銘柄コード, t0=窗口起日, t1=本日, m=0（q 必填，"
            f"空 q 回「該当なし」）| {_WINDOW_NOTE}"
        ),
    },
    {
        "path": "/inbs/1401{YYYYMMDD}{seq}.pdf",
        "description": "開示資料 PDF 取得（一覧/検索結果的表題連結）",
        "category": "檔案取得",
        "supports_history": True,
        "date_params": [],
        "response_format": "pdf",
        "notes": (
            "URL 由一覧/検索頁解析取得（1401 前綴＋日期＋連番），不可自行拼湊 | "
            f"{_WINDOW_NOTE}"
        ),
    },
    {
        "path": "/inbs/0812{YYYYMMDD}{seq}.zip",
        "description": "決算短信等 XBRL zip 取得（XBRLData/Summary＋Attachment）",
        "category": "檔案取得",
        "supports_history": True,
        "date_params": [],
        "response_format": "zip",
        "sample_fields": [
            "XBRLData/Summary/tse-*-ixbrl.htm",
            "XBRLData/Summary/tse-*-def.xml",
            "XBRLData/Attachment/*-ixbrl.htm",
            "XBRLData/Attachment/qualitative.htm",
        ],
        "notes": (
            "URL 由一覧/検索頁 XBRL 連結解析（0812 前綴），僅含 XBRL 之開示有 | "
            "2024-04 四半期報告書廢止後，Q1/Q3 季頻財務唯一免費來源 | "
            f"{_WINDOW_NOTE}"
        ),
    },
]


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Build TDnet endpoint list（檢索面＋檔案取得模式，無網路）。"""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []
    for ep_def in KNOWN_ENDPOINTS:
        endpoints.append(
            EndpointInfo(
                source="tdnet",
                endpoint_type="web",
                path=ep_def["path"],
                description=ep_def["description"],
                category=ep_def["category"],
                method=ep_def.get("method", "GET"),
                supports_history=ep_def.get("supports_history", True),
                date_params=list(ep_def.get("date_params", [])),
                granularity=ep_def.get("granularity", ""),
                response_format=ep_def.get("response_format", ""),
                sample_fields=list(ep_def.get("sample_fields", []))[:15],
                id_field="コード",
                notes=ep_def.get("notes", ""),
                state="discovered",
            )
        )
    logger.info("TDnet: %d known endpoints", len(endpoints))
    return endpoints


def _recent_weekday(today: date | None = None) -> str:
    """回傳最近的平日（YYYYMMDD，今天若是平日則昨天起算）。"""
    if today is None:
        today = date.today()
    d = today - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.strftime("%Y%m%d")


_CODE_RE = re.compile(r"^[0-9][0-9A-Z]{3,4}$")


def _parse_list_page(html: str) -> dict[str, Any]:
    """解析指定日一覧頁：總件數、資料列（7 欄）、PDF/zip 連結。

    僅收「第 2 欄為銘柄コード」的列，排除 kaiji-info 等非資料列。
    """
    soup = BeautifulSoup(html, "html.parser")
    m = re.search(r"全\s*(\d+)\s*件", html)
    total = int(m.group(1)) if m else 0

    rows: list[list[str]] = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 7:
            continue
        classes = [(td.get("class") or [""])[0] for td in tds]
        if not any(c.startswith(("oddnew", "evennew")) for c in classes):
            continue
        texts = [td.get_text(strip=True) for td in tds]
        if _CODE_RE.match(texts[1]):
            rows.append(texts)

    pdf_links = re.findall(r'href="([^"]*1401\d+\.pdf)"', html)
    zip_links = re.findall(r'href="([^"]*0812\d+\.zip)"', html)
    return {
        "total": total,
        "rows": rows,
        "pdf_links": pdf_links,
        "zip_links": zip_links,
    }


def _parse_search_page(html: str) -> dict[str, Any]:
    """解析検索結果頁（markup 與一覧頁不同：tr.odd/.even＋語意 class）。"""
    soup = BeautifulSoup(html, "html.parser")
    m = re.search(r"(\d+)\s*件", html)
    total = int(m.group(1)) if m else 0

    rows: list[dict[str, str]] = []
    for tr in soup.find_all("tr", class_=["odd", "even"]):
        cells = {}
        for td in tr.find_all("td"):
            cls = (td.get("class") or [""])[0]
            if cls:
                cells[cls] = td.get_text(strip=True)
        if cells.get("code"):
            rows.append(cells)
    return {"total": total, "rows": rows}


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered TDnet endpoints（抓當日 list 解析件數與欄位）。"""
    if settings is None:
        settings = DiscoverySettings()

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="tdnet", state="discovered")

    if not discovered:
        logger.info("No discovered TDnet endpoints to probe")
        return []

    to_probe = discovered[:limit]
    base = settings.get_base_url("tdnet", "web")
    session = _create_session(settings=settings, source="tdnet")
    day = _recent_weekday()

    # --- 先抓一次當日一覧（多個 probe 共用） ---
    list_parsed: dict[str, Any] = {}
    list_http = 0
    try:
        resp = session.get(
            f"{base}/inbs/I_list_001_{day}.html", timeout=settings.request_timeout
        )
        list_http = resp.status_code
        if resp.status_code == 200:
            resp.encoding = "utf-8"
            list_parsed = _parse_list_page(resp.text)
            logger.info(
                "TDnet %s: 全%d件, %d rows on page 1",
                day,
                list_parsed["total"],
                len(list_parsed["rows"]),
            )
    except Exception as e:  # noqa: BLE001
        logger.warning("TDnet list fetch failed: %s", e)
    delay(settings.web_delay)

    first_row = (list_parsed.get("rows") or [[]])[0]
    sample_code = first_row[1] if len(first_row) > 1 else ""
    sample_company = first_row[2] if len(first_row) > 2 else ""

    def _probe_search(query: str, t0: str) -> dict[str, Any]:
        try:
            resp = session.post(
                f"{base}{SEARCH_PATH}",
                data={"t0": t0, "t1": day, "q": query, "m": "0"},
                timeout=settings.request_timeout,
            )
            if resp.status_code != 200:
                return {"status": "error", "note": f"HTTP {resp.status_code}"}
            resp.encoding = "utf-8"
            parsed = _parse_search_page(resp.text)
            n = len(parsed["rows"])
            return {
                "status": "ok" if n else "empty",
                "record_count": parsed["total"] or n,
                "note": f"q={query!r} ({t0}-{day}) → {parsed['total'] or n} 件",
            }
        except Exception as e:  # noqa: BLE001
            return {"status": "error", "note": str(e)}
        finally:
            delay(settings.web_delay)

    results: list[EndpointInfo] = []
    for ep in to_probe:
        updates: dict[str, Any] = {"state": "probed"}

        if ep.path == "/inbs/I_main_00.html":
            try:
                resp = session.get(
                    f"{base}{ep.path}", timeout=settings.request_timeout
                )
                reachable = resp.status_code == 200 and "I_list_001_" in resp.text
                updates["status"] = "ok" if reachable else "error"
                if reachable:
                    updates["record_count"] = 1
            except Exception as e:  # noqa: BLE001
                updates["status"] = "error"
                updates["notes"] = (ep.notes + f" | probe error: {e}").strip(" | ")
            delay(settings.web_delay)

        elif ep.path.startswith("/inbs/I_list_"):
            if list_parsed:
                total = list_parsed["total"]
                updates["status"] = "ok" if list_parsed["rows"] else "empty"
                updates["record_count"] = total or len(list_parsed["rows"])
                updates["notes"] = (
                    ep.notes + f" | probe {day}: 全{total}件"
                ).strip(" | ")
                if list_parsed["rows"]:
                    sample_path = (
                        settings.samples_dir / "tdnet" / f"I_list_{day}.json"
                    )
                    save_sample(
                        [dict(zip(LIST_FIELDS, r)) for r in list_parsed["rows"]],
                        sample_path,
                        max_records=settings.max_sample_records,
                    )
                    updates["sample_path"] = str(sample_path)
            else:
                updates["status"] = "error"
                updates["notes"] = (
                    ep.notes + f" | probe: HTTP {list_http}"
                ).strip(" | ")

        elif "#facet=" in ep.path:
            facet = ep.path.split("#facet=")[-1]
            window_start = (
                date.today() - timedelta(days=30)
            ).strftime("%Y%m%d")
            query, t0 = {
                "code": (sample_code, day),
                "company": (sample_company, day),
                "disclosure-type": ("決算短信", window_start),
                "code-window": (sample_code, window_start),
            }.get(facet, ("", day))
            if not query:
                updates["status"] = "error"
                updates["notes"] = (
                    ep.notes + " | probe: 當日一覧無資料，無法取樣本 query"
                ).strip(" | ")
            else:
                r = _probe_search(query, t0)
                updates["status"] = r["status"]
                if "record_count" in r:
                    updates["record_count"] = r["record_count"]
                updates["notes"] = (ep.notes + f" | probe: {r['note']}").strip(" | ")

        elif ep.path.endswith(".pdf") or ep.path.endswith(".zip"):
            links = (
                list_parsed.get("pdf_links", [])
                if ep.path.endswith(".pdf")
                else list_parsed.get("zip_links", [])
            )
            if not links:
                updates["status"] = "empty"
                updates["notes"] = (
                    ep.notes + f" | probe {day}: 一覧頁無對應連結"
                ).strip(" | ")
            else:
                url = links[0]
                if not url.startswith("http"):
                    url = f"{base}/inbs/{url.lstrip('./')}"
                try:
                    resp = session.get(url, timeout=settings.request_timeout)
                    updates["status"] = "ok" if resp.status_code == 200 else "error"
                    updates["record_count"] = len(links)
                    updates["notes"] = (
                        ep.notes
                        + f" | probe: {len(links)} links on page 1, 例 {url}"
                    ).strip(" | ")
                except Exception as e:  # noqa: BLE001
                    updates["status"] = "error"
                    updates["notes"] = (ep.notes + f" | probe error: {e}").strip(
                        " | "
                    )
                delay(settings.web_delay)

        else:
            updates["status"] = "skipped"

        results.append(ep.model_copy(update=updates))

    ok = sum(1 for r in results if r.status == "ok")
    logger.info("TDnet probe done: %d ok / %d total", ok, len(results))
    return results


def main() -> None:
    """Run TDnet discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("TDnet: %d endpoints saved to DB", len(endpoints))


if __name__ == "__main__":
    main()
