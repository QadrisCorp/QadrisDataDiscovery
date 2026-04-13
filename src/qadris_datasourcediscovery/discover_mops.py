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

from qadris_datasourcediscovery.catalog import Catalog, EndpointInfo
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

# New MOPS SPA known routes (for reference)
MOPS_SPA_ROUTES: list[dict[str, str]] = [
    {"hash": "#/web/t05sr01_1", "description": "Real-time material information"},
    {"hash": "#/web/t05st02", "description": "Today's material information"},
    {"hash": "#/web/t05st01", "description": "Historical material information"},
    {"hash": "#/web/t146sb10", "description": "Announcement query"},
    {"hash": "#/web/t146sb05", "description": "Company overview"},
    {"hash": "#/web/t05st03", "description": "Company basic info"},
    {"hash": "#/web/t164sb00", "description": "Consolidated/individual reports (XBRL)"},
    {"hash": "#/web/t163sb01", "description": "Financial report announcements"},
    {"hash": "#/web/t57sb01_q1", "description": "Financial reports"},
    {"hash": "#/web/t05st10_ifrs", "description": "Monthly revenue"},
    {"hash": "#/web/t05st15", "description": "Mainland investment info"},
    {"hash": "#/web/t108sb19", "description": "Ex-dividend announcements"},
    {"hash": "#/web/t108sb16_q1", "description": "Shareholder meetings"},
    {"hash": "#/web/t05st09_2", "description": "Dividend distribution"},
    {"hash": "#/web/stapap1", "description": "Director/supervisor holdings"},
    {"hash": "#/web/query6_1", "description": "Insider holding changes"},
    {"hash": "#/web/t100sb03_1", "description": "Functional committees"},
    {"hash": "#/web/t51sb10", "description": "Latest announcements"},
]


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


def discover(*, settings: DiscoverySettings | None = None) -> Catalog:
    """Discover MOPS endpoints using hybrid strategy."""
    if settings is None:
        settings = DiscoverySettings()

    catalog = Catalog()
    session = _create_mops_session(settings=settings)

    # === Old MOPS AJAX discovery ===
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

        catalog.add(ep)
        delay(settings.web_delay)

    # === Record new MOPS SPA routes ===
    logger.info("=== New MOPS SPA route recording ===")
    for route in MOPS_SPA_ROUTES:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path=route["hash"],
            description=route["description"],
            category="SPA Page",
            method="GET",
            supports_history=True,
            status="ok",
            notes="New MOPS SPA route, requires Selenium",
        )
        catalog.add(ep)

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
    )
    catalog.add(ep_taxonomy)
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
        status="ok",
        notes=(
            "New API base: https://mops.interinfo.com.tw:8443/mops/api/ "
            "| Via Web Worker POST JSON "
            "| Not directly accessible, requires Selenium or browser "
            "| Old MOPS (mopsov.twse.com.tw) still works via requests + AJAX"
        ),
    )
    catalog.add(ep_api)

    return catalog


def main() -> None:
    """Run MOPS discovery and save catalog."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    catalog = discover(settings=settings)
    output = settings.catalog_dir / "mops_catalog.json"
    catalog.to_json(output)
    logger.info(
        "MOPS catalog saved: %s (%d endpoints)", output, len(catalog.endpoints)
    )

    ok_count = sum(1 for ep in catalog.endpoints if ep.status == "ok")
    error_count = sum(1 for ep in catalog.endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, error=%d", ok_count, error_count)


if __name__ == "__main__":
    main()
