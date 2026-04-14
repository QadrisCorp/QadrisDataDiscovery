"""TPEx web endpoint discovery — new website API (/www/zh-tw/ paths)."""

from __future__ import annotations

import logging
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    delay,
    fetch_json,
    save_sample,
)

logger = logging.getLogger(__name__)

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


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Discover TPEx new website API endpoints."""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []
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
            ep.status = "ok"

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
