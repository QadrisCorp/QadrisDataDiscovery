"""TWSE OpenAPI discovery — auto-discover all endpoints from swagger spec."""

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

SWAGGER_URL = "https://openapi.twse.com.tw/v1/swagger.json"


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """Discover all TWSE OpenAPI endpoints from swagger.json."""
    if settings is None:
        settings = DiscoverySettings()

    endpoints: list[EndpointInfo] = []
    session = _create_session(settings=settings)

    logger.info("Fetching TWSE OpenAPI swagger.json ...")
    try:
        swagger, status = fetch_json(SWAGGER_URL, session=session, settings=settings)
    except FetchError:
        logger.error("Failed to fetch swagger.json")
        return endpoints

    if not swagger:
        logger.error("Empty swagger.json (status=%s)", status)
        return endpoints

    paths: dict[str, Any] = swagger.get("paths", {})
    logger.info("Found %d endpoints", len(paths))

    for path, methods in paths.items():
        for method, spec in methods.items():
            method = method.upper()
            description = spec.get("summary", "") or spec.get("description", "")
            tags = spec.get("tags", [])
            category = tags[0] if tags else ""

            url = f"{settings.twse_openapi_base}{path}"
            logger.info("Probing: %s %s — %s", method, path, description)

            ep = EndpointInfo(
                source="twse",
                endpoint_type="openapi",
                path=path,
                description=description,
                category=category,
                method=method,
                supports_history=False,
                state="probed",
            )

            if method == "GET":
                try:
                    data, _resp_status = fetch_json(
                        url, session=session, settings=settings
                    )
                except FetchError:
                    ep.status = "error"
                    endpoints.append(ep)
                    delay(settings.openapi_delay)
                    continue

                if data is not None:
                    if isinstance(data, list):
                        ep.status = "ok" if data else "empty"
                        ep.record_count = len(data)
                        if data:
                            ep.sample_fields = (
                                list(data[0].keys())
                                if isinstance(data[0], dict)
                                else []
                            )
                            sample_path = (
                                settings.samples_dir
                                / "tse_openapi"
                                / f"{path.strip('/').replace('/', '_')}.json"
                            )
                            save_sample(
                                data,
                                sample_path,
                                max_records=settings.max_sample_records,
                            )
                    elif isinstance(data, dict):
                        ep.status = "ok"
                        ep.record_count = 1
                        ep.sample_fields = list(data.keys())
                        sample_path = (
                            settings.samples_dir
                            / "tse_openapi"
                            / f"{path.strip('/').replace('/', '_')}.json"
                        )
                        save_sample(
                            data,
                            sample_path,
                            max_records=settings.max_sample_records,
                        )
                    else:
                        ep.status = "ok"
                else:
                    ep.status = "error"
            else:
                ep.status = "skipped"
                ep.notes = f"Non-GET method: {method}"

            endpoints.append(ep)
            delay(settings.openapi_delay)

    return endpoints


def main() -> None:
    """Run TWSE OpenAPI discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("TWSE OpenAPI: %d endpoints saved to DB", len(endpoints))

    ok_count = sum(1 for ep in endpoints if ep.status == "ok")
    empty_count = sum(1 for ep in endpoints if ep.status == "empty")
    error_count = sum(1 for ep in endpoints if ep.status == "error")
    logger.info("Stats: ok=%d, empty=%d, error=%d", ok_count, empty_count, error_count)


if __name__ == "__main__":
    main()
