"""Endpoint enrichment engine — rule-based + LLM."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Protocol

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import LLMError
from qadris_datasourcediscovery.llm import ClaudeCLI, load_prompt_template
from qadris_datasourcediscovery.registry import MARKET_LABELS, get_market

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
    # 日本源
    "LocalCode",
    "銘柄コード",
    "証券コード",
    "edinetCode",
    "docID",
]

# --- Default settings for base URL resolution ---
_default_settings = DiscoverySettings()

# --- Prompt template 路徑 ---
# 優先使用套件內的 prompts/，fallback 到 project_root/prompts/
_PACKAGE_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
_REPO_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


def _get_prompts_dir() -> Path:
    """Return the prompts directory, preferring package-local."""
    if _PACKAGE_PROMPTS_DIR.is_dir():
        return _PACKAGE_PROMPTS_DIR
    return _REPO_PROMPTS_DIR


class CatalogStore(Protocol):
    """Protocol for catalog DB access (avoids circular import)."""

    def get_all_endpoints(self) -> list[EndpointInfo]: ...
    def get_endpoints(
        self,
        *,
        source: str | None = None,
        status: str | None = None,
        state: str | None = None,
    ) -> list[EndpointInfo]: ...
    def upsert_endpoints(self, endpoints: list[EndpointInfo]) -> int: ...


# ====================================================================
# 層次一：Rule-based 推斷
# ====================================================================


def infer_granularity(ep: EndpointInfo) -> str:
    """從 endpoint_type 和 date_params 推斷資料粒度。"""
    # 台灣三源的 OpenAPI 皆為當期 snapshot；日本 REST API（J-Quants/EDINET）
    # 帶 date 參數支援歷史查詢，走下方 date_params 推斷
    if ep.endpoint_type == "openapi" and get_market(ep.source) == "tw":
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
    elif ep.source == "jquants":
        if "date" in params or "from" in params:
            return f"{method} date=YYYY-MM-DD or from/to range (pagination_key)"
    elif ep.source == "edinet":
        if "date" in params:
            return f"{method} date=YYYY-MM-DD (提出日, JST)"
    elif ep.source == "tdnet":
        if ep.supports_history:
            return f"{method} I_list_{{page}}_YYYYMMDD.html (free window: last 31 days)"
    elif ep.source == "jpx":
        if ep.supports_history:
            return f"{method} archive pages per year/month (see notes)"

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
        if "代號" in field or "代碼" in field or "コード" in field:
            return field
        if lower in ("code", "stockcode", "stockno"):
            return field
    return ""


def infer_request_example(ep: EndpointInfo) -> dict[str, Any]:
    """建構完整請求範例。"""
    base = _default_settings.get_base_url(ep.source, ep.endpoint_type)
    if not base:
        return {}

    # 台灣三源 OpenAPI 無參數即可打；日本 REST API 需帶認證/日期，走下方分支
    if ep.endpoint_type == "openapi" and get_market(ep.source) == "tw":
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
    elif ep.source == "jquants":
        if "date" in ep.date_params:
            params["date"] = "2026-06-30"
        if "code" in ep.date_params:
            params["code"] = "7203"
    elif ep.source == "edinet":
        if "date" in ep.date_params:
            params["date"] = "2026-06-30"
        params["Subscription-Key"] = "<YOUR_API_KEY>"

    example: dict[str, Any] = {"url": url, "method": ep.method}
    if ep.source == "jquants":
        example["headers"] = {"x-api-key": "<YOUR_API_KEY>"}
    if params:
        example["params"] = params
    return example


def infer_response_format(ep: EndpointInfo) -> str:
    """推斷回傳格式。"""
    if ep.endpoint_type == "openapi":
        return "json"
    if ep.source == "mops":
        return "html_table"
    if ep.source == "tdnet":
        return "html_table"
    if ep.source == "jpx":
        # JPX 統計頁產物多為 Excel；PDF-only 表在 discovery/probe 時明確標 pdf
        return "excel"
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
        return "all"
    if get_market(ep.source) == "jp":
        # 日本源預設涵蓋東證全市場（Prime/Standard/Growth）；
        # 分段限定表（如 Prime-only 統計）在 discovery 時明確覆寫
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
        req_example = infer_request_example(ep)
        if req_example:
            updates["request_example"] = req_example
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
    template_path = _get_prompts_dir() / "enrich_endpoint.txt"

    fields_str = ", ".join(ep.sample_fields[:15]) if ep.sample_fields else "(none)"
    market_label = MARKET_LABELS.get(get_market(ep.source), "Taiwan")
    prompt_text = load_prompt_template(
        template_path,
        market=market_label,
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


def enrich_endpoint(
    ep: EndpointInfo,
    *,
    llm: ClaudeCLI | None = None,
    rules_only: bool = False,
    llm_only: bool = False,
    force: bool = False,
) -> EndpointInfo:
    """組合 rule-based + LLM 豐富單一 endpoint。"""
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

    if updates:
        return ep.model_copy(update=updates)
    return ep


def enrich_all(
    *,
    db: CatalogStore,
    llm: ClaudeCLI | None = None,
    rules_only: bool = False,
    llm_only: bool = False,
    force: bool = False,
    limit: int = 0,
    dry_run: bool = False,
) -> int:
    """豐富 endpoints，從 DB 讀取並寫回。"""
    if force:
        endpoints = db.get_all_endpoints()
    else:
        endpoints = db.get_endpoints(state="probed")

    enriched_count = 0

    for ep in endpoints:
        if limit and enriched_count >= limit:
            break

        updated = enrich_endpoint(
            ep,
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
            else:
                updated = updated.model_copy(update={"state": "enriched"})
                db.upsert_endpoints([updated])

    return enriched_count
