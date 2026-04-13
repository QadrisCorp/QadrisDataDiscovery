"""Endpoint metadata models and catalog export utilities."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EndpointInfo(BaseModel):
    """Metadata for a single discovered API endpoint."""

    # --- Step 1: 基礎探索欄位 ---
    source: str  # twse, tpex, mops
    endpoint_type: str  # openapi, web, xbrl
    path: str
    description: str = ""
    category: str = ""
    method: str = "GET"
    supports_history: bool = False
    date_params: list[str] = Field(default_factory=list)
    status: str = "unknown"  # ok, error, timeout, empty
    record_count: int = 0
    sample_fields: list[str] = Field(default_factory=list)
    notes: str = ""

    # --- Step 2: Enrichment 欄位 ---
    domain_tags: list[str] = Field(default_factory=list)
    granularity: str = ""  # daily, monthly, quarterly, snapshot
    history_method: str = ""  # 含日期格式的取得方式描述
    id_field: str = ""  # 個股識別欄位名
    request_example: dict[str, Any] = Field(default_factory=dict)
    response_format: str = ""  # json, html_table
    coverage: str = ""  # listed_only, otc_only, all
    fields_summary: str = ""  # 一句話描述


class Catalog:
    """Collection of discovered endpoints with export capabilities."""

    def __init__(self) -> None:
        self.endpoints: list[EndpointInfo] = []

    def add(self, endpoint: EndpointInfo) -> None:
        """Add an endpoint to the catalog."""
        self.endpoints.append(endpoint)

    def to_json(self, path: Path) -> None:
        """Export catalog as JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [ep.model_dump() for ep in self.endpoints]
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def to_markdown(self) -> str:
        """Generate markdown table grouped by category."""
        lines: list[str] = []
        by_category: dict[str, list[EndpointInfo]] = {}
        for ep in self.endpoints:
            by_category.setdefault(ep.category or "Other", []).append(ep)

        for cat, eps in sorted(by_category.items()):
            lines.append(f"### {cat}\n")
            lines.append("| Path | Description | Status | History | Count | Fields |")
            lines.append("|------|-------------|--------|---------|-------|--------|")
            for ep in eps:
                fields = ", ".join(ep.sample_fields[:5])
                hist = "Y" if ep.supports_history else "N"
                lines.append(
                    f"| `{ep.path}` | {ep.description} | {ep.status} "
                    f"| {hist} | {ep.record_count} | {fields} |"
                )
            lines.append("")
        return "\n".join(lines)


def load_catalog(path: Path) -> list[dict[str, Any]]:
    """Load catalog from a JSON file."""
    if not path.exists():
        return []
    result: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    return result


def load_all_endpoints(*, catalog_dir: Path) -> list[EndpointInfo]:
    """Load all catalog JSON files and return as EndpointInfo list."""
    endpoints: list[EndpointInfo] = []

    for catalog_file in sorted(catalog_dir.glob("*_catalog.json")):
        data = load_catalog(catalog_file)
        for item in data:
            endpoints.append(EndpointInfo(**item))
        logger.info("Loaded %s: %d endpoints", catalog_file.name, len(data))

    return endpoints
