"""TWSE web endpoint discovery — manually curated historical data pages."""

from __future__ import annotations

import logging
from typing import Any

from qadris_datasourcediscovery.catalog import Catalog, EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    delay,
    fetch_json,
    save_sample,
)

logger = logging.getLogger(__name__)

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


def discover(*, settings: DiscoverySettings | None = None) -> Catalog:
    """Discover TWSE web historical data endpoints."""
    if settings is None:
        settings = DiscoverySettings()

    catalog = Catalog()
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
        )

        try:
            data, status = fetch_json(
                url, session=session, settings=settings, params=params
            )
        except FetchError as e:
            ep.status = "error"
            ep.notes = str(e)
            catalog.add(ep)
            delay(settings.web_delay)
            continue

        if data is not None:
            stat = data.get("stat", "") if isinstance(data, dict) else ""
            if stat == "OK" or isinstance(data, list):
                ep.status = "ok"
                if isinstance(data, dict):
                    for key in ("data", "tables", "aaData"):
                        if key in data and isinstance(data[key], list):
                            ep.record_count = len(data[key])
                            break
                    if "fields" in data and isinstance(data["fields"], list):
                        ep.sample_fields = data["fields"][:10]
                    elif "fields9" in data:
                        ep.sample_fields = (
                            data["fields9"][:10]
                            if isinstance(data["fields9"], list)
                            else []
                        )
                elif isinstance(data, list):
                    ep.record_count = len(data)

                sample_path = (
                    settings.samples_dir
                    / "tse_web"
                    / f"{path.strip('/').replace('/', '_')}.json"
                )
                save_sample(
                    data, sample_path, max_records=settings.max_sample_records
                )
            else:
                ep.status = "error"
                ep.notes = f"stat={stat}"
        else:
            ep.status = "error"
            ep.notes = f"HTTP {status}"

        catalog.add(ep)
        delay(settings.web_delay)

    return catalog


def main() -> None:
    """Run TWSE web discovery and save catalog."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    catalog = discover(settings=settings)
    output = settings.catalog_dir / "tse_web_catalog.json"
    catalog.to_json(output)
    logger.info(
        "TWSE Web catalog saved: %s (%d endpoints)", output, len(catalog.endpoints)
    )

    ok_count = sum(1 for ep in catalog.endpoints if ep.status == "ok")
    error_count = sum(1 for ep in catalog.endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, error=%d", ok_count, error_count)


if __name__ == "__main__":
    main()
