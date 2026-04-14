"""Endpoint metadata model."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Source = Literal["twse", "tpex", "mops"]
EndpointType = Literal["openapi", "web", "xbrl"]
Status = Literal["unknown", "ok", "error", "timeout", "empty", "skipped"]
State = Literal["discovered", "probed", "enriched"]


class EndpointInfo(BaseModel):
    """Metadata for a single discovered API endpoint."""

    # --- 基礎探索欄位 ---
    source: Source
    endpoint_type: EndpointType
    path: str
    description: str = ""
    category: str = ""
    method: str = "GET"
    supports_history: bool = False
    date_params: list[str] = Field(default_factory=list)
    status: Status = "unknown"
    record_count: int = 0
    sample_fields: list[str] = Field(default_factory=list)
    notes: str = ""

    # --- Enrichment 欄位 ---
    domain_tags: list[str] = Field(default_factory=list)
    granularity: str = ""  # daily, monthly, quarterly, snapshot
    history_method: str = ""
    id_field: str = ""
    request_example: dict[str, Any] = Field(default_factory=dict)
    response_format: str = ""  # json, html_table
    coverage: str = ""  # listed_only, otc_only, all
    fields_summary: str = ""

    # --- Pipeline state ---
    state: State = "discovered"
    sample_path: str = ""
