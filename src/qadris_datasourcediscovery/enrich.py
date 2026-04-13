"""Endpoint enrichment engine — rule-based + LLM."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo, load_catalog
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import LLMError
from qadris_datasourcediscovery.llm import ClaudeCLI, load_prompt_template

logger = logging.getLogger(__name__)

# --- 已知的個股識別欄位名 ---
_KNOWN_ID_FIELDS = [
    "公司代號",
    "證券代號",
    "股票代號",
    "Code",
    "SecuritiesCompanyCode",
    "stockNo",
    "StockCode",
    "SecuritiesCode",
    "公司代碼",
]

# --- Base URL mapping ---
_BASE_URLS: dict[tuple[str, str], str] = {
    ("twse", "openapi"): "https://openapi.twse.com.tw/v1",
    ("twse", "web"): "https://www.twse.com.tw",
    ("tpex", "openapi"): "https://www.tpex.org.tw/openapi/v1",
    ("tpex", "web"): "https://www.tpex.org.tw",
    ("mops", "web"): "https://mopsov.twse.com.tw",
    ("mops", "xbrl"): "https://mops.twse.com.tw",
}

# --- Prompt template 路徑 ---
_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


# ====================================================================
# 層次一：Rule-based 推斷
# ====================================================================


def infer_granularity(ep: EndpointInfo) -> str:
    """從 endpoint_type 和 date_params 推斷資料粒度。"""
    if ep.endpoint_type == "openapi":
        return "snapshot"

    params = ep.date_params
    if "season" in params or "quarter" in params:
        return "quarterly"
    if "month" in params and "year" in params and len(params) == 2:
        return "monthly"
    if "date" in params:
        return "daily"
    if "year" in params and len(params) == 1:
        return "yearly"

    # MOPS web endpoints 沒帶 date_params 但有 supports_history
    if ep.supports_history:
        return "daily"
    return "snapshot"


def infer_history_method(ep: EndpointInfo) -> str:
    """推斷歷史資料取得方式。"""
    if not ep.supports_history and not ep.date_params:
        return "snapshot_only"

    method = ep.method
    params = ep.date_params

    if ep.source == "twse" and ep.endpoint_type == "web":
        if "date" in params:
            return f"{method} date=YYYYMMDD&response=json"
    elif ep.source == "tpex" and ep.endpoint_type == "web":
        if "date" in params:
            return f"{method} date=YYYYMMDD (new API, JSON response)"
    elif ep.source == "mops":
        if "year" in params and "season" in params:
            return f"{method} year=ROC_YEAR&season=1-4"
        if "year" in params and "month" in params:
            return f"{method} year=ROC_YEAR&month=1-12"
        if ep.supports_history:
            return f"{method} (see notes for params)"

    if params:
        param_str = "&".join(f"{p}=?" for p in params)
        return f"{method} {param_str}"

    return "snapshot_only"


def infer_id_field(ep: EndpointInfo) -> str:
    """從 sample_fields 找個股識別欄位。"""
    for field in ep.sample_fields:
        if field in _KNOWN_ID_FIELDS:
            return field
    # 模糊比對
    for field in ep.sample_fields:
        lower = field.lower()
        if "代號" in field or "代碼" in field:
            return field
        if lower in ("code", "stockcode", "stockno"):
            return field
    return ""


def infer_request_example(ep: EndpointInfo) -> dict[str, Any]:
    """建構完整請求範例。"""
    base = _BASE_URLS.get((ep.source, ep.endpoint_type), "")
    if not base:
        return {}

    if ep.endpoint_type == "openapi":
        return {"url": f"{base}{ep.path}", "method": "GET"}

    url = f"{base}{ep.path}"
    params: dict[str, str] = {}

    if ep.source == "twse" and ep.endpoint_type == "web":
        if "date" in ep.date_params:
            params["date"] = "20250401"
            params["response"] = "json"
    elif ep.source == "tpex" and ep.endpoint_type == "web":
        if "date" in ep.date_params:
            params["date"] = "20250401"
    elif ep.source == "mops":
        if "year" in ep.date_params:
            params["year"] = "114"  # ROC year
        if "season" in ep.date_params:
            params["season"] = "1"
        if "month" in ep.date_params:
            params["month"] = "3"

    example: dict[str, Any] = {"url": url, "method": ep.method}
    if params:
        example["params"] = params
    return example


def infer_response_format(ep: EndpointInfo) -> str:
    """推斷回傳格式。"""
    if ep.endpoint_type == "openapi":
        return "json"
    if ep.source == "mops":
        return "html_table"
    # TWSE/TPEx web endpoints
    return "json"


def infer_coverage(ep: EndpointInfo) -> str:
    """推斷資料涵蓋範圍。"""
    if ep.source == "twse":
        return "listed_only"
    if ep.source == "tpex":
        return "otc_only"
    if ep.source == "mops":
        # MOPS 的 TYPEK 參數決定涵蓋範圍
        if "TYPEK" in ep.notes:
            return "all"  # 支援 sii/otc/rotc/pub
        return "all"
    return ""


def enrich_rule_based(ep: EndpointInfo) -> dict[str, Any]:
    """Rule-based 推斷所有確定性欄位，回傳更新 dict。"""
    updates: dict[str, Any] = {}

    if not ep.granularity:
        updates["granularity"] = infer_granularity(ep)
    if not ep.history_method:
        updates["history_method"] = infer_history_method(ep)
    if not ep.id_field:
        val = infer_id_field(ep)
        if val:
            updates["id_field"] = val
    if not ep.request_example:
        val = infer_request_example(ep)
        if val:
            updates["request_example"] = val
    if not ep.response_format:
        updates["response_format"] = infer_response_format(ep)
    if not ep.coverage:
        val = infer_coverage(ep)
        if val:
            updates["coverage"] = val

    return updates


# ====================================================================
# 層次二：LLM enrichment
# ====================================================================


def enrich_llm(ep: EndpointInfo, llm: ClaudeCLI) -> dict[str, Any]:
    """用 claude -p 推斷語意欄位（domain_tags, fields_summary）。"""
    template_path = _PROMPTS_DIR / "enrich_endpoint.txt"

    fields_str = ", ".join(ep.sample_fields[:15]) if ep.sample_fields else "(none)"
    prompt_text = load_prompt_template(
        template_path,
        source=ep.source,
        endpoint_type=ep.endpoint_type,
        path=ep.path,
        description=ep.description,
        category=ep.category,
        sample_fields=fields_str,
    )

    try:
        result = llm.prompt_json(prompt_text)
    except LLMError as e:
        logger.warning("LLM enrichment failed for %s:%s — %s", ep.source, ep.path, e)
        return {}

    updates: dict[str, Any] = {}

    tags = result.get("domain_tags")
    if isinstance(tags, list) and tags:
        updates["domain_tags"] = tags

    summary = result.get("fields_summary")
    if isinstance(summary, str) and summary:
        updates["fields_summary"] = summary

    return updates


# ====================================================================
# Orchestration
# ====================================================================


def load_overrides(catalog_dir: Path) -> dict[str, dict[str, Any]]:
    """載入手動 override 檔。"""
    override_path = catalog_dir / "enrichment_overrides.json"
    if not override_path.exists():
        return {}
    data: dict[str, dict[str, Any]] = json.loads(
        override_path.read_text(encoding="utf-8")
    )
    return data


def enrich_endpoint(
    ep: EndpointInfo,
    *,
    overrides: dict[str, dict[str, Any]],
    llm: ClaudeCLI | None = None,
    rules_only: bool = False,
    llm_only: bool = False,
    force: bool = False,
) -> EndpointInfo:
    """組合 rule-based + LLM + override 豐富單一 endpoint。"""
    updates: dict[str, Any] = {}

    # Rule-based
    if not llm_only:
        updates.update(enrich_rule_based(ep))

    # LLM
    if not rules_only and llm is not None:
        needs_llm = force or not ep.domain_tags
        if needs_llm:
            llm_updates = enrich_llm(ep, llm)
            updates.update(llm_updates)

    # Override（最高優先）
    key = f"{ep.source}:{ep.path}"
    if key in overrides:
        updates.update(overrides[key])

    if updates:
        return ep.model_copy(update=updates)
    return ep


def enrich_catalog_file(
    path: Path,
    *,
    overrides: dict[str, dict[str, Any]],
    llm: ClaudeCLI | None = None,
    rules_only: bool = False,
    llm_only: bool = False,
    force: bool = False,
    limit: int = 0,
    dry_run: bool = False,
) -> int:
    """豐富單一 catalog JSON 檔案，回傳更新數量。"""
    data = load_catalog(path)
    if not data:
        return 0

    endpoints = [EndpointInfo(**item) for item in data]
    enriched_count = 0
    results: list[dict[str, Any]] = []

    for ep in endpoints:
        if limit and enriched_count >= limit:
            results.append(ep.model_dump())
            continue

        updated = enrich_endpoint(
            ep,
            overrides=overrides,
            llm=llm,
            rules_only=rules_only,
            llm_only=llm_only,
            force=force,
        )

        if updated != ep:
            enriched_count += 1
            if dry_run:
                logger.info(
                    "[DRY RUN] Would enrich %s:%s — tags=%s",
                    updated.source,
                    updated.path,
                    updated.domain_tags,
                )

        results.append(updated.model_dump())

    if not dry_run and enriched_count > 0:
        path.write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return enriched_count


def enrich_all(
    *,
    catalog_dir: Path,
    llm: ClaudeCLI | None = None,
    rules_only: bool = False,
    llm_only: bool = False,
    force: bool = False,
    limit: int = 0,
    dry_run: bool = False,
) -> int:
    """豐富所有 catalog JSON 檔案。"""
    overrides = load_overrides(catalog_dir)
    total = 0

    for catalog_file in sorted(catalog_dir.glob("*_catalog.json")):
        count = enrich_catalog_file(
            catalog_file,
            overrides=overrides,
            llm=llm,
            rules_only=rules_only,
            llm_only=llm_only,
            force=force,
            limit=limit,
            dry_run=dry_run,
        )
        logger.info("Enriched %s: %d endpoints", catalog_file.name, count)
        total += count

    return total
