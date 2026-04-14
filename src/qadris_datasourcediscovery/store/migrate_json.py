"""One-time migration: import existing JSON catalogs into SQLite."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.store.database import CatalogDB

logger = logging.getLogger(__name__)


def _infer_state(ep: EndpointInfo) -> str:
    """Determine initial state from existing data.

    - Has domain_tags → enriched (LLM/rule enrichment done)
    - Has sample_fields or status is ok/error/empty → probed (actually hit the API)
    - Otherwise → discovered (only indexed, not yet probed)
    """
    if ep.domain_tags:
        return "enriched"
    if ep.sample_fields or ep.status in ("ok", "error", "empty", "timeout"):
        return "probed"
    return "discovered"


def _infer_sample_path(ep: EndpointInfo, samples_dir: Path) -> str:
    """Try to locate existing sample file on disk, return relative path or ''."""
    source_type = f"{ep.source}_{ep.endpoint_type}"
    # Sanitize path for filename: /opendata/t187ap45_L → opendata_t187ap45_L
    sanitized = ep.path.strip("/").replace("/", "_")
    candidate = samples_dir / source_type / f"{sanitized}.json"
    if candidate.exists():
        return str(candidate.relative_to(samples_dir))
    return ""


def migrate_json_to_sqlite(
    catalog_dir: Path,
    db_path: Path,
    *,
    samples_dir: Path | None = None,
    dry_run: bool = False,
) -> int:
    """Import all *_catalog.json files into SQLite. Returns endpoint count."""
    if samples_dir is None:
        samples_dir = catalog_dir.parent / "samples"

    json_files = sorted(catalog_dir.glob("*_catalog.json"))
    if not json_files:
        logger.warning("No *_catalog.json files found in %s", catalog_dir)
        return 0

    all_endpoints: list[EndpointInfo] = []

    for json_file in json_files:
        raw: list[dict[str, Any]] = json.loads(
            json_file.read_text(encoding="utf-8")
        )
        for item in raw:
            ep = EndpointInfo(**item)
            ep = ep.model_copy(
                update={
                    "state": _infer_state(ep),
                    "sample_path": _infer_sample_path(ep, samples_dir),
                }
            )
            all_endpoints.append(ep)
        logger.info("Loaded %s: %d endpoints", json_file.name, len(raw))

    if dry_run:
        logger.info(
            "[DRY RUN] Would import %d endpoints from %d files",
            len(all_endpoints),
            len(json_files),
        )
        return len(all_endpoints)

    with CatalogDB(db_path) as db:
        count = db.upsert_endpoints(all_endpoints)
        logger.info("Imported %d endpoints into %s", count, db_path)

    return count
