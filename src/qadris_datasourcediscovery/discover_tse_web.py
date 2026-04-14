"""TWSE web endpoint discovery — report-index + known endpoint probing."""

from __future__ import annotations

import logging
import re
from typing import Any

from bs4 import BeautifulSoup

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    delay,
    fetch_json,
    fetch_with_selenium,
    get_selenium_driver,
    save_sample,
)

logger = logging.getLogger(__name__)

REPORT_INDEX_URL = "https://www.twse.com.tw/zh/report-index.html"

# URL path category mapping
_CATEGORY_MAP = {
    "trading": "交易資訊",
    "indices": "指數資訊",
    "announcement": "公告資訊",
    "products": "上市證券",
    "listed": "上市公司",
    "focus": "市場焦點",
}

# TWSE known web endpoints (support &response=json)
# Date format: YYYYMMDD
KNOWN_ENDPOINTS: list[dict[str, Any]] = [
    {
        "path": "/exchangeReport/STOCK_DAY",
        "description": "Individual stock daily trading",
        "category": "Market",
        "params": {"date": "20250407", "stockNo": "2330", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/MI_INDEX",
        "description": "Daily market summary (indices)",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/fund/T86",
        "description": "Three institutional investors daily trades",
        "category": "Institutional",
        "params": {"date": "20250407", "selectType": "ALL", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/MI_MARGN",
        "description": "Margin trading balance",
        "category": "Margin",
        "params": {"date": "20250407", "selectType": "ALL", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWTASU",
        "description": "Credit trading statistics",
        "category": "Margin",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/FMTQIK",
        "description": "Daily trading volume/value",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/MI_INDEX20",
        "description": "Top 20 traded securities",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/fund/MI_QFIIS",
        "description": "Foreign/mainland investors holdings",
        "category": "Institutional",
        "params": {
            "date": "20250407",
            "selectType": "ALLBUT0999",
            "response": "json",
        },
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWT93U",
        "description": "Securities lending details",
        "category": "Lending",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/indicesReport/MI_5MINS_HIST",
        "description": "TAIEX historical index data",
        "category": "Index",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/STOCK_DAY_AVG",
        "description": "Individual stock monthly average price",
        "category": "Market",
        "params": {"date": "20250407", "stockNo": "2330", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/FMSRFK",
        "description": "Individual stock monthly trading info",
        "category": "Market",
        "params": {"date": "20250407", "stockNo": "2330", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/BWIBBU",
        "description": "PE ratio, dividend yield, PB ratio",
        "category": "Fundamental",
        "params": {"date": "20250407", "stockNo": "2330", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/fund/TWT38U",
        "description": "Three institutional investors trade summary",
        "category": "Institutional",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWT84U",
        "description": "Stock price change range",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWT53U",
        "description": "Odd-lot trading",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/BFT41U",
        "description": "After-hours fixed-price trading",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWTB4U",
        "description": "Day trading targets and statistics",
        "category": "Market",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/BFI84U",
        "description": "Margin/short-sale suspension notice",
        "category": "Margin",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/exchangeReport/TWT48U",
        "description": "Ex-dividend/ex-rights schedule",
        "category": "Fundamental",
        "params": {"date": "20250407", "response": "json"},
        "date_params": ["date"],
        "supports_history": True,
    },
]


def discover_from_report_index(
    *,
    settings: DiscoverySettings,
) -> list[EndpointInfo]:
    """從 TWSE report-index.html 解析所有報表頁面（Selenium 渲染）。"""
    logger.info("=== TWSE Report Index discovery (%s) ===", REPORT_INDEX_URL)

    try:
        driver = get_selenium_driver(settings=settings)
        html = fetch_with_selenium(
            REPORT_INDEX_URL,
            settings=settings,
            driver=driver,
            wait_seconds=8,
        )
        driver.quit()
    except Exception as e:
        logger.error("Failed to fetch report-index: %s", e)
        return []

    soup = BeautifulSoup(html, "html.parser")
    from bs4 import Tag

    table = soup.find("table")
    if not table or not isinstance(table, Tag):
        logger.error("No table found in report-index page")
        return []

    rows = table.find_all("tr")[1:]  # skip header
    endpoints: list[EndpointInfo] = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 5:
            continue

        name = cells[0].get_text(strip=True)
        fields_text = cells[1].get_text(strip=True)
        start_date = cells[2].get_text(strip=True)
        update_freq = cells[3].get_text(strip=True)

        # Extract link URL
        link = cells[4].find("a")
        if not link or not link.get("href"):
            continue

        href = str(link["href"])

        # Extract path from full URL: https://www.twse.com.tw/zh/trading/historical/mi-index.html
        m = re.search(r"twse\.com\.tw(/zh/[^?#]+)", href)
        if not m:
            continue

        page_path = m.group(1)

        # Infer category from URL path segment
        parts = page_path.split("/")
        category = _CATEGORY_MAP.get(parts[2], parts[2]) if len(parts) >= 4 else ""

        # Parse field names from fields_text (truncate for sample_fields)
        field_names = [
            f.strip()
            for f in re.split(r"[、,]", fields_text)
            if f.strip() and not f.strip().startswith("[")
        ]

        notes_parts = []
        if start_date:
            notes_parts.append(f"起始: {start_date}")
        if update_freq:
            notes_parts.append(f"更新: {update_freq}")

        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path=page_path,
            description=name,
            category=category,
            method="GET",
            supports_history=bool(start_date),
            sample_fields=field_names[:15],
            notes=" | ".join(notes_parts),
            state="discovered",
        )
        endpoints.append(ep)

    logger.info(
        "Report Index: found %d reports in %d categories",
        len(endpoints),
        len({ep.category for ep in endpoints}),
    )
    return endpoints


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered TWSE web endpoints.

    Extract data-api via Selenium, then fetch JSON.

    Reads state='discovered' endpoints from DB, finds their JSON API path,
    hits the API for sample data, and returns updated EndpointInfo with state='probed'.
    """
    if settings is None:
        settings = DiscoverySettings()

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="twse", state="discovered")

    if not discovered:
        logger.info("No discovered TWSE endpoints to probe")
        return []

    to_probe = discovered[:limit]
    logger.info(
        "=== Probing %d/%d discovered TWSE endpoints ===",
        len(to_probe),
        len(discovered),
    )

    # Phase 1: Selenium — extract data-api from each page
    from selenium.webdriver.common.by import By

    driver = get_selenium_driver(settings=settings)
    api_map: dict[str, str] = {}  # page_path -> data-api

    try:
        for ep in to_probe:
            page_url = f"{settings.twse_web_base}{ep.path}"
            logger.info("Extracting API: %s — %s", ep.path, ep.description)
            try:
                driver.get(page_url)
                import time

                time.sleep(3)
                forms = driver.find_elements(By.CSS_SELECTOR, "form[data-api]")
                if forms:
                    api_map[ep.path] = forms[0].get_attribute("data-api")
                    logger.info("  data-api: %s", api_map[ep.path])
                else:
                    logger.warning("  No data-api form found")
            except Exception as e:
                logger.error("  Selenium error: %s", e)
    finally:
        driver.quit()

    # Phase 2: requests — hit JSON API for each endpoint
    session = _create_session(settings=settings)
    results: list[EndpointInfo] = []

    for ep in to_probe:
        api_path = api_map.get(ep.path)
        if not api_path:
            results.append(
                ep.model_copy(
                    update={
                        "state": "probed",
                        "status": "error",
                        "notes": (ep.notes + " | No data-api found").strip(" | "),
                    }
                )
            )
            continue

        api_url = f"{settings.twse_web_base}/rwd/zh{api_path}"
        logger.info("Probing API: %s", api_url)

        try:
            data, status_code = fetch_json(
                api_url,
                session=session,
                settings=settings,
                params={"response": "json"},
            )
        except FetchError as e:
            results.append(
                ep.model_copy(
                    update={
                        "state": "probed",
                        "status": "error",
                        "notes": (ep.notes + f" | API error: {e}").strip(" | "),
                    }
                )
            )
            delay(settings.web_delay)
            continue

        updates: dict[str, Any] = {
            "state": "probed",
            "notes": (ep.notes + f" | api={api_path}").strip(" | "),
        }

        if data is not None:
            stat = data.get("stat", "") if isinstance(data, dict) else ""
            if re.match(r"(?i)^ok$", stat):
                # Extract fields and record count
                record_count = 0
                if "tables" in data and isinstance(data["tables"], list):
                    all_fields: list[str] = []
                    for t in data["tables"]:
                        if isinstance(t, dict):
                            rows = t.get("data", [])
                            record_count += len(rows)
                            fields = t.get("fields", [])
                            if fields and not all_fields:
                                all_fields = [str(f) for f in fields[:15]]
                    updates["record_count"] = record_count
                    if all_fields:
                        updates["sample_fields"] = all_fields
                elif "data" in data and isinstance(data["data"], list):
                    record_count = len(data["data"])
                    updates["record_count"] = record_count
                    if "fields" in data and isinstance(data["fields"], list):
                        updates["sample_fields"] = [str(f) for f in data["fields"][:15]]

                updates["status"] = "ok" if record_count > 0 else "empty"

                # Save sample
                sample_name = api_path.strip("/").replace("/", "_")
                sample_path = settings.samples_dir / "tse_web" / f"{sample_name}.json"
                save_sample(data, sample_path, max_records=settings.max_sample_records)
            else:
                updates["status"] = "error"
                updates["notes"] = (
                    ep.notes + f" | api={api_path} | stat={stat}"
                ).strip(" | ")
        else:
            updates["status"] = "error"
            updates["notes"] = (
                ep.notes + f" | api={api_path} | HTTP {status_code}"
            ).strip(" | ")

        results.append(ep.model_copy(update=updates))
        delay(settings.web_delay)

    return results


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Discover TWSE web historical data endpoints."""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []

    # === Report Index discovery（Selenium，一次載入）===
    report_index_endpoints = discover_from_report_index(settings=settings)
    endpoints.extend(report_index_endpoints)

    # === Known endpoint probing（逐個打 API）===
    session = _create_session(settings=settings)

    for ep_def in KNOWN_ENDPOINTS:
        path = ep_def["path"]
        params = ep_def["params"]
        url = f"{settings.twse_web_base}{path}"

        logger.info("Probing: %s — %s", path, ep_def["description"])

        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path=path,
            description=ep_def["description"],
            category=ep_def["category"],
            method="GET",
            supports_history=ep_def.get("supports_history", True),
            date_params=ep_def.get("date_params", []),
            state="probed",
        )

        try:
            data, status = fetch_json(
                url, session=session, settings=settings, params=params
            )
        except FetchError as e:
            ep.status = "error"
            ep.notes = str(e)
            endpoints.append(ep)
            delay(settings.web_delay)
            continue

        if data is not None:
            stat = data.get("stat", "") if isinstance(data, dict) else ""
            if stat == "OK" or isinstance(data, list):
                if isinstance(data, dict):
                    if "tables" in data and isinstance(data["tables"], list):
                        for t in data["tables"]:
                            if isinstance(t, dict):
                                rows = t.get("data", [])
                                ep.record_count += len(rows)
                                fields = t.get("fields", [])
                                if fields and not ep.sample_fields:
                                    ep.sample_fields = [str(f) for f in fields[:10]]
                    elif "data" in data and isinstance(data["data"], list):
                        ep.record_count = len(data["data"])
                    elif "aaData" in data and isinstance(data["aaData"], list):
                        ep.record_count = len(data["aaData"])

                    if not ep.sample_fields:
                        if "fields" in data and isinstance(data["fields"], list):
                            ep.sample_fields = data["fields"][:10]
                        elif "fields9" in data and isinstance(data["fields9"], list):
                            ep.sample_fields = data["fields9"][:10]
                elif isinstance(data, list):
                    ep.record_count = len(data)
                ep.status = "ok" if ep.record_count > 0 else "empty"

                sample_path = (
                    settings.samples_dir
                    / "tse_web"
                    / f"{path.strip('/').replace('/', '_')}.json"
                )
                save_sample(data, sample_path, max_records=settings.max_sample_records)
            else:
                ep.status = "error"
                ep.notes = f"stat={stat}"
        else:
            ep.status = "error"
            ep.notes = f"HTTP {status}"

        endpoints.append(ep)
        delay(settings.web_delay)

    return endpoints


def main() -> None:
    """Run TWSE web discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("TWSE Web: %d endpoints saved to DB", len(endpoints))

    ok_count = sum(1 for ep in endpoints if ep.status == "ok")
    error_count = sum(1 for ep in endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, error=%d", ok_count, error_count)


if __name__ == "__main__":
    main()
