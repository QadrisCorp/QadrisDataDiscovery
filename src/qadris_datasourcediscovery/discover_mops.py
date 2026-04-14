"""MOPS discovery — hybrid strategy.

MOPS new version is a Vue SPA (mops.twse.com.tw/mops/),
backend API not directly accessible.
Old version (mopsov.twse.com.tw) still works via AJAX
returning static HTML file links.
"""

from __future__ import annotations

import logging
import re
from io import StringIO
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.fetcher import delay, save_sample

logger = logging.getLogger(__name__)

MOPS_OLD = "https://mopsov.twse.com.tw"

# Old MOPS AJAX endpoints
MOPS_ENDPOINTS: list[dict[str, Any]] = [
    {
        "path": "ajax_t21sc04_ifrs",
        "page": "t21sc04_ifrs",
        "description": "Monthly revenue summary (IFRS) - Listed",
        "category": "Revenue",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "year": "114", "month": "02", "TYPEK": "sii",
        },
        "date_params": ["year", "month"],
        "notes": "TYPEK: sii(listed)/otc(OTC)/rotc(emerging)/pub(public)",
    },
    {
        "path": "ajax_t21sc04_ifrs",
        "page": "t21sc04_ifrs",
        "description": "Monthly revenue summary (IFRS) - OTC",
        "category": "Revenue",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "year": "114", "month": "02", "TYPEK": "otc",
        },
        "date_params": ["year", "month"],
        "notes": "TYPEK=otc",
    },
    {
        "path": "ajax_t164sb04",
        "page": "t164sb04",
        "description": "Financial statements (Income statement)",
        "category": "Financial",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "year": "113", "season": "3",
        },
        "date_params": ["year", "season"],
        "notes": "By company code, year=ROC year, season=1~4",
    },
    {
        "path": "ajax_t164sb03",
        "page": "t164sb03",
        "description": "Financial statements (Balance sheet)",
        "category": "Financial",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "year": "113", "season": "3",
        },
        "date_params": ["year", "season"],
        "notes": "By company code, year=ROC year, season=1~4",
    },
    {
        "path": "ajax_t164sb05",
        "page": "t164sb05",
        "description": "Financial statements (Cash flow statement)",
        "category": "Financial",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "year": "113", "season": "3",
        },
        "date_params": ["year", "season"],
        "notes": "By company code, year=ROC year, season=1~4",
    },
    {
        "path": "ajax_t05st09_2",
        "page": "t05st09_2",
        "description": "Dividend distribution",
        "category": "Dividend",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "ESSION_str": "",
        },
        "date_params": [],
        "notes": "Historical dividend by company code",
    },
    {
        "path": "ajax_t05sr01_1",
        "page": "t05sr01_1",
        "description": "Real-time material information",
        "category": "Announcement",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1",
        },
        "date_params": [],
        "notes": "Current day real-time announcements",
    },
    {
        "path": "t05st10_ifrs",
        "page": "t05st10_ifrs",
        "description": "Profitability analysis (IFRS)",
        "category": "Financial",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "year": "113", "season": "3",
        },
        "date_params": ["year", "season"],
        "notes": "By company code",
    },
    # --- XBRL Information Platform (t203sb01~03) ---
    {
        "path": "ajax_t203sb01",
        "page": "t203sb01",
        "description": "XBRL instance document query (single company)",
        "category": "XBRL",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "co_id": "2330", "year": "113", "season": "3",
        },
        "date_params": ["year", "season"],
        "notes": (
            "By company code | Lists XBRL instance docs by year/season "
            "with view/download links via window.open()"
        ),
    },
    {
        "path": "ajax_t203sb02",
        "page": "t203sb02",
        "description": "XBRL instance document batch download",
        "category": "XBRL",
        "form_data": {
            "encodeURIComponent": "1", "step": "1", "firstin": "1",
            "off": "1", "year": "113", "season": "3", "TYPEK": "sii",
        },
        "date_params": ["year", "season"],
        "notes": (
            "TYPEK: sii(listed)/otc(OTC) | Batch ZIP download per year/season "
            "via /server-java/FileDownLoad (e.g. tifrs-2025Q3.zip)"
        ),
    },
]

# XBRL taxonomy download — static links, not AJAX
MOPS_XBRL_TAXONOMY_URLS: list[str] = [
    "/nas/taxonomy/tifrs-20200630.zip",
    "/nas/taxonomy/tifrs-20190331.zip",
    "/nas/taxonomy/tifrs-20180930.zip",
    "/nas/taxonomy/tifrs-20180331.zip",
    "/nas/taxonomy/tifrs-20170331.zip",
    "/nas/taxonomy/tifrs-20150331.zip",
    "/nas/taxonomy/tifrs-20140331.zip",
    "/nas/taxonomy/tifrs-20130331.zip",
    "/nas/taxonomy/tw-gaap-2013-06-30.zip",
    "/nas/taxonomy/tw-gaap-2012-06-30.zip",
]

SITEMAP_URL = f"{MOPS_OLD}/mops/web/t146sb08"


def _create_mops_session(*, settings: DiscoverySettings) -> requests.Session:
    """Create an HTTP session configured for MOPS requests."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": settings.user_agent,
        "Accept-Language": "zh-TW,zh;q=0.9",
    })
    return session


def _try_old_mops_ajax(
    session: requests.Session,
    page: str,
    ajax_path: str,
    form_data: dict[str, str],
    *,
    settings: DiscoverySettings,
) -> tuple[list[pd.DataFrame] | None, str]:
    """Fetch data via old MOPS AJAX.

    MOPS AJAX may return HTML tables directly, or a popup link to static HTML.
    """
    session.get(
        f"{MOPS_OLD}/mops/web/{page}", timeout=settings.request_timeout
    )
    delay(1)

    resp = session.post(
        f"{MOPS_OLD}/mops/web/{ajax_path}",
        data=form_data,
        timeout=settings.request_timeout,
    )
    resp.encoding = "utf-8"

    if "頁面無法執行" in resp.text:
        return None, "security_block"

    if "<table" in resp.text.lower():
        tables = pd.read_html(StringIO(resp.text))
        if tables:
            return tables, "direct_table"

    popup_match = re.search(r"window\.open\('(/nas/[^']+)'", resp.text)
    if popup_match:
        nas_path = popup_match.group(1)
        nas_url = f"{MOPS_OLD}{nas_path}"
        logger.info("  Found static file: %s", nas_path)
        nas_resp = session.get(nas_url, timeout=settings.request_timeout)
        nas_resp.encoding = "utf-8"
        if "<table" in nas_resp.text.lower():
            tables = pd.read_html(StringIO(nas_resp.text))
            if tables:
                return tables, f"nas_file:{nas_path}"

    return None, "no_data"


# Multiple parameter strategies to try when probing
_PROBE_STRATEGIES = [
    {"year": "113", "month": "12", "TYPEK": "sii", "co_id": "2330",
     "season": "3", "YM": "11312", "day": "15",
     "smonth": "10", "emonth": "12"},
    {"year": "113", "month": "6", "TYPEK": "sii", "co_id": "2330",
     "season": "2", "YM": "11306", "day": "10",
     "smonth": "4", "emonth": "6"},
    {"year": "114", "month": "3", "TYPEK": "all", "co_id": "2330",
     "season": "1", "YM": "11403", "day": "7",
     "smonth": "1", "emonth": "3"},
]


def _fill_form_defaults(
    form_data: dict[str, str],
    strategy: dict[str, str] | None = None,
) -> dict[str, str]:
    """Fill in smart defaults for common MOPS form parameters."""
    data = dict(form_data)
    defaults = strategy or _PROBE_STRATEGIES[0]

    for key, default_val in defaults.items():
        if key in data and not data[key]:
            data[key] = default_val

    return data


def _extract_ajax_form(
    soup: BeautifulSoup,
) -> tuple[str, dict[str, str]] | None:
    """Extract the main AJAX form action and inputs from a MOPS page."""
    for f in soup.find_all("form"):
        action = f.get("action", "")
        if "autoComplete" in action or not action.startswith("/mops/web/"):
            continue

        inputs: dict[str, str] = {}
        for inp in f.find_all("input"):
            name = inp.get("name")
            if name:
                inputs[name] = inp.get("value", "")

        # Also grab first option from select elements
        for sel in f.find_all("select"):
            name = sel.get("name")
            if name and name not in inputs:
                opts = sel.find_all("option")
                if opts:
                    inputs[name] = opts[0].get("value", "")

        return action, inputs

    return None


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered MOPS endpoints: GET page → extract form → POST ajax.

    Reads state='discovered' endpoints from DB, extracts the AJAX form from
    each page, fills in smart defaults, POSTs to get data, and returns
    updated EndpointInfo with state='probed'.
    """
    if settings is None:
        settings = DiscoverySettings()

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="mops", state="discovered")
        # Also retry previously failed endpoints
        failed = [
            ep for ep in db.get_all_endpoints()
            if ep.source == "mops" and ep.status == "error"
        ]

    to_retry = discovered + failed
    if not to_retry:
        logger.info("No MOPS endpoints to probe")
        return []

    # Deduplicate by path
    seen: set[str] = set()
    unique: list[EndpointInfo] = []
    for ep in to_retry:
        if ep.path not in seen:
            seen.add(ep.path)
            unique.append(ep)
    to_retry = unique

    # Filter out non-probeable paths
    probeable = [
        ep for ep in to_retry
        if ep.path.startswith("/mops/web/")
        and not ep.path.endswith((".doc", ".pdf", ".zip"))
        and "/server-java/" not in ep.path
        and "/nas/" not in ep.path
    ]

    to_probe = probeable[:limit]
    logger.info(
        "=== Probing %d/%d MOPS endpoints ===",
        len(to_probe), len(probeable),
    )

    session = _create_mops_session(settings=settings)
    results: list[EndpointInfo] = []

    for ep in to_probe:
        page_code = ep.path.rsplit("/", 1)[-1]
        logger.info("Probing: %s — %s", page_code, ep.description)

        try:
            # GET page to extract form
            page_url = f"{MOPS_OLD}/mops/web/{page_code}"
            resp = session.get(page_url, timeout=settings.request_timeout)
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")

            form_info = _extract_ajax_form(soup)
            if not form_info:
                logger.warning("  No AJAX form found")
                results.append(ep.model_copy(update={
                    "state": "probed",
                    "status": "error",
                    "notes": (ep.notes + " | no ajax form").strip(" | "),
                }))
                delay(settings.web_delay)
                continue

            action, form_inputs = form_info

            # Try multiple strategies
            tables = None
            result_type = "no_data"
            used_strategy = 0

            for i, strategy in enumerate(_PROBE_STRATEGIES):
                form_data = _fill_form_defaults(form_inputs, strategy)
                delay(1)

                ajax_path = action.rsplit("/", 1)[-1]
                tables, result_type = _try_old_mops_ajax(
                    session, page_code, ajax_path,
                    form_data, settings=settings,
                )

                if tables:
                    used_strategy = i
                    break

                # Check for window.open redirect to external URL
                resp2 = session.post(
                    f"{MOPS_OLD}{action}",
                    data=form_data,
                    timeout=settings.request_timeout,
                )
                resp2.encoding = "utf-8"

                ext_match = re.search(
                    r"window\.open\('(https?://[^']+)'", resp2.text
                )
                if ext_match:
                    ext_url = ext_match.group(1)
                    logger.info("  Following external URL: %s", ext_url)
                    try:
                        ext_resp = session.get(
                            ext_url, timeout=settings.request_timeout
                        )
                        ext_resp.encoding = "utf-8"
                        if "<table" in ext_resp.text.lower():
                            tables = pd.read_html(StringIO(ext_resp.text))
                            if tables:
                                result_type = f"external:{ext_url}"
                                used_strategy = i
                                break
                    except Exception:
                        pass

                # Check for step 2 form
                soup2 = BeautifulSoup(resp2.text, "html.parser")
                form2 = soup2.find("form")
                if form2 and form2.get("action", "").startswith("/mops/web/"):
                    inputs2 = {
                        inp.get("name"): inp.get("value", "")
                        for inp in form2.find_all("input")
                        if inp.get("name")
                    }
                    delay(1)
                    resp3 = session.post(
                        f"{MOPS_OLD}{form2['action']}",
                        data=inputs2,
                        timeout=settings.request_timeout,
                    )
                    resp3.encoding = "utf-8"
                    if "<table" in resp3.text.lower():
                        try:
                            tables = pd.read_html(StringIO(resp3.text))
                            if tables:
                                result_type = f"step2:{form2['action']}"
                                used_strategy = i
                                break
                        except Exception:
                            pass

            # Build update
            updates: dict[str, Any] = {
                "state": "probed",
                "method": "POST",
            }

            if tables:
                updates["status"] = "ok"
                updates["record_count"] = sum(len(t) for t in tables)
                biggest = max(tables, key=len)
                updates["sample_fields"] = [str(c) for c in biggest.columns][:10]
                updates["notes"] = (
                    f"ajax={action}, method={result_type}, "
                    f"tables={len(tables)}, strategy={used_strategy}"
                )

                sample_name = page_code
                sample_path = settings.samples_dir / "mops" / f"{sample_name}.json"
                save_sample(
                    biggest.head(settings.max_sample_records),
                    sample_path,
                    max_records=settings.max_sample_records,
                )
                logger.info(
                    "  OK: %d tables, %d rows (strategy %d)",
                    len(tables), updates["record_count"], used_strategy,
                )
            else:
                updates["status"] = "error"
                updates["notes"] = f"ajax={action}, all strategies failed"
                logger.warning("  Failed: all strategies exhausted")

            results.append(ep.model_copy(update=updates))

        except Exception as e:
            logger.error("  Exception: %s", e)
            results.append(ep.model_copy(update={
                "state": "probed",
                "status": "error",
                "notes": f"error: {e}",
            }))

        delay(settings.web_delay)

    return results


def discover_from_sitemap(
    session: requests.Session,
    *,
    settings: DiscoverySettings,
) -> list[EndpointInfo]:
    """從 MOPS 網站地圖解析所有頁面，存為 discovered 狀態。"""
    logger.info("=== MOPS Sitemap discovery (%s) ===", SITEMAP_URL)

    try:
        resp = session.get(SITEMAP_URL, timeout=settings.request_timeout)
        resp.encoding = "utf-8"
    except requests.RequestException as e:
        logger.error("Failed to fetch sitemap: %s", e)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    all_links = soup.find_all("a", href=True)

    endpoints: list[EndpointInfo] = []
    current_category = ""

    for a in all_links:
        href = a["href"]
        text = a.get_text(strip=True)

        if not text:
            continue

        # href="#" 是分類標題
        if href == "#":
            current_category = text
            continue

        # 跳過非 page_code 的連結
        if href.startswith(("http", "javascript", "/mops/")):
            continue

        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path=f"/mops/web/{href}",
            description=text,
            category=current_category,
            method="GET",
            state="discovered",
        )
        endpoints.append(ep)

    logger.info("Sitemap: found %d pages in %d categories", len(endpoints), len({ep.category for ep in endpoints}))
    return endpoints


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Discover MOPS endpoints using hybrid strategy."""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []
    session = _create_mops_session(settings=settings)

    # === Sitemap discovery（快，一次 HTTP）===
    sitemap_endpoints = discover_from_sitemap(session, settings=settings)
    endpoints.extend(sitemap_endpoints)

    # === Old MOPS AJAX discovery（慢，逐個 probe）===
    logger.info("=== Old MOPS (mopsov.twse.com.tw) AJAX discovery ===")

    for ep_def in MOPS_ENDPOINTS:
        ajax_path = ep_def["path"]
        page = ep_def["page"]
        logger.info("Probing: %s — %s", ajax_path, ep_def["description"])

        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path=f"/mops/web/{ajax_path}",
            description=ep_def["description"],
            category=ep_def["category"],
            method="POST",
            supports_history=True,
            date_params=ep_def.get("date_params", []),
            notes=ep_def.get("notes", ""),
            state="probed",
        )

        try:
            tables, result_type = _try_old_mops_ajax(
                session, page, ajax_path, ep_def["form_data"], settings=settings
            )

            if tables:
                ep.status = "ok"
                ep.record_count = sum(len(t) for t in tables)
                biggest = max(tables, key=len)
                ep.sample_fields = [str(c) for c in biggest.columns][:10]
                ep.notes += f" | method={result_type}, tables={len(tables)}"

                sample_name = ajax_path.replace("ajax_", "")
                typek = ep_def["form_data"].get("TYPEK", "")
                if typek:
                    sample_name += f"_{typek}"
                sample_path = (
                    settings.samples_dir / "mops" / f"{sample_name}.json"
                )
                save_sample(
                    biggest.head(settings.max_sample_records),
                    sample_path,
                    max_records=settings.max_sample_records,
                )

                logger.info(
                    "  OK: %d tables, %d rows, via %s",
                    len(tables),
                    ep.record_count,
                    result_type,
                )
            else:
                ep.status = "error"
                ep.notes += f" | result={result_type}"
                logger.warning("  Failed: %s", result_type)

        except Exception as e:
            ep.status = "error"
            ep.notes += f" | {e}"
            logger.error("  Exception: %s", e)

        endpoints.append(ep)
        delay(settings.web_delay)

    # === XBRL Taxonomy (static download links) ===
    logger.info("=== XBRL Taxonomy download links ===")
    taxonomy_files = ", ".join(
        url.rsplit("/", 1)[-1] for url in MOPS_XBRL_TAXONOMY_URLS[:3]
    )
    ep_taxonomy = EndpointInfo(
        source="mops",
        endpoint_type="web",
        path="/mops/web/t203sb03",
        description="XBRL taxonomy download",
        category="XBRL",
        method="GET",
        supports_history=False,
        status="ok",
        record_count=len(MOPS_XBRL_TAXONOMY_URLS),
        sample_fields=[url.rsplit("/", 1)[-1] for url in MOPS_XBRL_TAXONOMY_URLS],
        notes=(
            f"Static ZIP links on page | {len(MOPS_XBRL_TAXONOMY_URLS)} taxonomy files "
            f"(e.g. {taxonomy_files}) | IFRS + TW-GAAP versions"
        ),
        state="discovered",
    )
    endpoints.append(ep_taxonomy)
    logger.info(
        "  Recorded %d taxonomy files", len(MOPS_XBRL_TAXONOMY_URLS)
    )

    # === API architecture info ===
    ep_api = EndpointInfo(
        source="mops",
        endpoint_type="web",
        path="/mops/api/{endpoint_name}",
        description="MOPS SPA backend API architecture note",
        category="API Architecture",
        method="POST",
        state="discovered",
        notes=(
            "New API base: https://mops.interinfo.com.tw:8443/mops/api/ "
            "| Via Web Worker POST JSON "
            "| Not directly accessible, requires Selenium or browser "
            "| Old MOPS (mopsov.twse.com.tw) still works via requests + AJAX"
        ),
    )
    endpoints.append(ep_api)

    return endpoints


def main() -> None:
    """Run MOPS discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("MOPS: %d endpoints saved to DB", len(endpoints))

    ok_count = sum(1 for ep in endpoints if ep.status == "ok")
    error_count = sum(1 for ep in endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, error=%d", ok_count, error_count)


if __name__ == "__main__":
    main()
