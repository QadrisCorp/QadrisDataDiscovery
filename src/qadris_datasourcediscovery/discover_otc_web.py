"""TPEx web endpoint discovery — homepage mega menu + known endpoint probing."""

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

TPEX_HOME_URL = "https://www.tpex.org.tw/zh-tw/index.html"

# Only discover pages under these path prefixes (量化投資相關)
_ALLOWED_PREFIXES = (
    "/zh-tw/mainboard/trading/",
    "/zh-tw/mainboard/listed/",
    "/zh-tw/indices/",
    "/zh-tw/esb/trading/",
    "/zh-tw/announce/market/",
)

# Category mapping from URL path
_CATEGORY_MAP = {
    "trading": "交易資訊",
    "listed": "上櫃公司",
    "indices": "指數資訊",
    "esb": "興櫃交易",
    "announce": "公告資訊",
}

# TPEx new website endpoints (direct JSON responses)
# Date format: YYYYMMDD (Western calendar)
KNOWN_ENDPOINTS: list[dict[str, Any]] = [
    {
        "path": "/www/zh-tw/afterTrading/dailyQuotes",
        "description": "OTC daily closing quotes",
        "category": "Market",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/dailyTradingInfo",
        "description": "Daily market trading info",
        "category": "Market",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/peRatio",
        "description": "PE ratio, dividend yield, PB ratio",
        "category": "Fundamental",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/insti/dailyTrade",
        "description": "Three institutional investors trade details",
        "category": "Institutional",
        "params": {"date": "20250407", "type": "D"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/insti/summary",
        "description": "Three institutional investors trade summary",
        "category": "Institutional",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/insti/qfiiTrade",
        "description": "Foreign/mainland investors trade details",
        "category": "Institutional",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/marginTrading/balance",
        "description": "Margin trading balance",
        "category": "Margin",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/marginTrading/marginSbl",
        "description": "Short-sale and securities lending balance",
        "category": "Margin",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/monthlyTrade",
        "description": "Individual stock monthly trading info",
        "category": "Market",
        "params": {"date": "20250407", "stkNo": "6510"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/indexInfo/minuteIndex",
        "description": "OTC index historical data",
        "category": "Index",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/exRight/dailyQuote",
        "description": "Ex-dividend/ex-rights schedule",
        "category": "Fundamental",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/brokerTrading",
        "description": "Broker trading volume/value",
        "category": "Market",
        "params": {"date": "20250407", "stkNo": "6510"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/oddLot",
        "description": "Odd-lot trading",
        "category": "Market",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/blockTrading",
        "description": "Block trading",
        "category": "Market",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
    {
        "path": "/www/zh-tw/afterTrading/dayTrading",
        "description": "Day trading statistics",
        "category": "Market",
        "params": {"date": "20250407"},
        "date_params": ["date"],
        "supports_history": True,
    },
]


def discover_from_homepage(
    *, settings: DiscoverySettings,
) -> list[EndpointInfo]:
    """從 TPEx 首頁 mega menu 解析所有報表頁面（Selenium 渲染）。"""
    logger.info("=== TPEx Homepage discovery (%s) ===", TPEX_HOME_URL)

    try:
        driver = get_selenium_driver(settings=settings)
        html = fetch_with_selenium(
            TPEX_HOME_URL,
            settings=settings,
            driver=driver,
            wait_seconds=8,
        )
        driver.quit()
    except Exception as e:
        logger.error("Failed to fetch TPEx homepage: %s", e)
        return []

    soup = BeautifulSoup(html, "html.parser")
    endpoints: list[EndpointInfo] = []
    seen: set[str] = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if not text or not href.startswith("/zh-tw/") or not href.endswith(".html"):
            continue

        # Filter by allowed prefixes
        if not any(href.startswith(p) for p in _ALLOWED_PREFIXES):
            continue

        if href in seen:
            continue
        seen.add(href)

        # Infer category from URL
        parts = href.split("/")
        # /zh-tw/mainboard/trading/... → trading
        # /zh-tw/indices/... → indices
        # /zh-tw/esb/trading/... → esb
        cat_key = ""
        if "mainboard" in parts:
            idx = parts.index("mainboard")
            if idx + 1 < len(parts):
                cat_key = parts[idx + 1]
        elif "esb" in parts:
            cat_key = "esb"
        elif "indices" in parts:
            cat_key = "indices"
        elif "announce" in parts:
            cat_key = "announce"

        category = _CATEGORY_MAP.get(cat_key, cat_key)

        ep = EndpointInfo(
            source="tpex",
            endpoint_type="web",
            path=href,
            description=text,
            category=category,
            method="GET",
            state="discovered",
        )
        endpoints.append(ep)

    logger.info(
        "Homepage: found %d pages in %d categories",
        len(endpoints),
        len({ep.category for ep in endpoints}),
    )
    return endpoints


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered TPEx web endpoints: extract API action via Selenium, then fetch JSON.

    TPEx API pattern: https://www.tpex.org.tw/www/zh-tw/{action}
    Action is found in: tables.init({action:"..."}) on each page.
    """
    if settings is None:
        settings = DiscoverySettings()

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="tpex", state="discovered")
        # Also retry previously failed endpoints with stat errors
        failed = [
            ep for ep in db.get_all_endpoints()
            if ep.source == "tpex" and ep.status == "error"
            and "stat=" in ep.notes
        ]

    to_retry = discovered + failed
    if not to_retry:
        logger.info("No TPEx endpoints to probe")
        return []

    # Deduplicate by path
    seen: set[str] = set()
    unique: list[EndpointInfo] = []
    for ep in to_retry:
        if ep.path not in seen:
            seen.add(ep.path)
            unique.append(ep)

    to_probe = unique[:limit]
    logger.info(
        "=== Probing %d/%d discovered TPEx endpoints ===",
        len(to_probe), len(discovered),
    )

    # Phase 1: Selenium — extract tables.init action from each page
    from selenium.webdriver.common.by import By

    driver = get_selenium_driver(settings=settings)
    action_map: dict[str, str] = {}  # page_path -> action

    try:
        for ep in to_probe:
            page_url = f"{settings.tpex_web_base}{ep.path}"
            logger.info("Extracting API: %s — %s", ep.path, ep.description)
            try:
                driver.get(page_url)
                import time
                time.sleep(3)

                # Extract action from tables.init({action:"..."})
                action = driver.execute_script("""
                    var scripts = document.querySelectorAll('script');
                    for (var s of scripts) {
                        var m = s.textContent.match(/action:"([^"]+)"/);
                        if (m) return m[1];
                    }
                    return null;
                """)

                if action:
                    action_map[ep.path] = action
                    logger.info("  action: %s", action)
                else:
                    logger.warning("  No tables.init action found")
            except Exception as e:
                logger.error("  Selenium error: %s", e)
    finally:
        driver.quit()

    # Phase 2: requests — hit JSON API with multiple param strategies
    session = _create_session(settings=settings)
    results: list[EndpointInfo] = []

    # TPEx accepts both YYYYMMDD and YYYY/MM/DD depending on endpoint
    param_strategies = [
        {"date": "20250407"},
        {"date": "2025/04/07"},
        {"date": "2025/04/07", "code": "6510"},
        {"date": "2025/03/01", "type": "2"},
        {"date": "2025", "startDate": "2025/01/01", "endDate": "2025/03/31"},
        {"date": "20250407", "stkNo": "6510"},
    ]

    for ep in to_probe:
        action = action_map.get(ep.path)
        if not action:
            results.append(ep.model_copy(update={
                "state": "probed",
                "status": "error",
                "notes": "No tables.init action found (static page?)",
            }))
            continue

        api_url = f"{settings.tpex_web_base}/www/zh-tw/{action}"
        logger.info("Probing API: %s", api_url)

        # Try multiple param strategies
        best_data = None
        best_strategy = 0

        for i, params in enumerate(param_strategies):
            try:
                data, _sc = fetch_json(
                    api_url,
                    session=session,
                    settings=settings,
                    params=params,
                )
            except FetchError:
                continue

            if data and isinstance(data, dict):
                stat = str(data.get("stat", ""))
                if re.match(r"(?i)^ok$", stat):
                    best_data = data
                    best_strategy = i
                    break

            delay(1)

        updates: dict[str, Any] = {
            "state": "probed",
            "method": "GET",
        }

        if best_data is not None:
            updates["supports_history"] = True
            updates["date_params"] = ["date"]

            record_count = 0
            if "tables" in best_data and isinstance(best_data["tables"], list):
                all_fields: list[str] = []
                for t in best_data["tables"]:
                    if isinstance(t, dict):
                        rows = t.get("data", [])
                        record_count += len(rows)
                        fields = t.get("fields", [])
                        if fields and not all_fields:
                            all_fields = [str(f) for f in fields[:15]]
                updates["record_count"] = record_count
                if all_fields:
                    updates["sample_fields"] = all_fields
            elif "data" in best_data and isinstance(best_data["data"], list):
                record_count = len(best_data["data"])
                updates["record_count"] = record_count
                if "fields" in best_data:
                    updates["sample_fields"] = [
                        str(f) for f in best_data["fields"][:15]
                    ]

            updates["status"] = "ok" if record_count > 0 else "empty"
            updates["notes"] = f"api={action}, strategy={best_strategy}"

            sample_name = action.replace("/", "_")
            sample_path = (
                settings.samples_dir / "otc_web" / f"{sample_name}.json"
            )
            save_sample(best_data, sample_path, max_records=settings.max_sample_records)
        else:
            updates["status"] = "error"
            updates["notes"] = f"api={action} | all strategies failed"

        results.append(ep.model_copy(update=updates))
        delay(settings.web_delay)

    return results


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Discover TPEx new website API endpoints."""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []

    # === Homepage mega menu discovery（Selenium，一次載入）===
    homepage_endpoints = discover_from_homepage(settings=settings)
    endpoints.extend(homepage_endpoints)

    # === Known endpoint probing（逐個打 API）===
    session = _create_session(settings=settings)

    for ep_def in KNOWN_ENDPOINTS:
        path = ep_def["path"]
        params = ep_def.get("params", {})
        url = f"{settings.tpex_web_base}{path}"

        logger.info("Probing: %s — %s", path, ep_def["description"])

        ep = EndpointInfo(
            source="tpex",
            endpoint_type="web",
            path=path,
            description=ep_def["description"],
            category=ep_def["category"],
            method="GET",
            supports_history=ep_def.get("supports_history", True),
            date_params=ep_def.get("date_params", []),
            notes="New website API, date format: YYYYMMDD",
            state="probed",
        )

        try:
            data, status = fetch_json(
                url, session=session, settings=settings, params=params
            )
        except FetchError as e:
            ep.status = "error"
            ep.notes += f" | {e}"
            endpoints.append(ep)
            delay(settings.web_delay)
            continue

        if data is not None:
            if isinstance(data, dict):
                if "tables" in data and isinstance(data["tables"], list):
                    for table in data["tables"]:
                        if isinstance(table, dict):
                            if "data" in table and isinstance(table["data"], list):
                                ep.record_count += len(table["data"])
                            if "fields" in table and isinstance(
                                table["fields"], list
                            ):
                                ep.sample_fields = table["fields"][:10]
                            if "title" in table:
                                ep.notes += f" | {table['title']}"
                elif "data" in data and isinstance(data["data"], list):
                    ep.record_count = len(data["data"])
                elif "date" in data:
                    ep.record_count = 1

            ep.status = "ok" if ep.record_count > 0 else "empty"

            sample_name = path.strip("/").replace("/", "_")
            sample_path = (
                settings.samples_dir / "otc_web" / f"{sample_name}.json"
            )
            save_sample(data, sample_path, max_records=settings.max_sample_records)
        else:
            ep.status = "error"
            ep.notes += f" | HTTP {status}"

        endpoints.append(ep)
        delay(settings.web_delay)

    return endpoints


def main() -> None:
    """Run TPEx web discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("TPEx Web: %d endpoints saved to DB", len(endpoints))

    ok_count = sum(1 for ep in endpoints if ep.status == "ok")
    error_count = sum(1 for ep in endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, error=%d", ok_count, error_count)


if __name__ == "__main__":
    main()
