"""Tests for rule-based enrichment functions."""

from __future__ import annotations

from unittest.mock import MagicMock

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.enrich import (
    enrich_all,
    enrich_endpoint,
    enrich_rule_based,
    infer_coverage,
    infer_granularity,
    infer_history_method,
    infer_id_field,
    infer_request_example,
    infer_response_format,
)


# =====================================================================
# infer_granularity
# =====================================================================


class TestInferGranularity:
    def test_openapi_is_snapshot(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="openapi", path="/x")
        assert infer_granularity(ep) == "snapshot"

    def test_season_param_is_quarterly(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year", "season"],
        )
        assert infer_granularity(ep) == "quarterly"

    def test_quarter_param_is_quarterly(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year", "quarter"],
        )
        assert infer_granularity(ep) == "quarterly"

    def test_year_month_is_monthly(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year", "month"],
        )
        assert infer_granularity(ep) == "monthly"

    def test_date_param_is_daily(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            date_params=["date"],
        )
        assert infer_granularity(ep) == "daily"

    def test_year_only_is_yearly(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year"],
        )
        assert infer_granularity(ep) == "yearly"

    def test_supports_history_no_params_is_daily(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            supports_history=True,
        )
        assert infer_granularity(ep) == "daily"

    def test_no_params_no_history_is_snapshot(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert infer_granularity(ep) == "snapshot"


# =====================================================================
# infer_history_method
# =====================================================================


class TestInferHistoryMethod:
    def test_no_history_no_params(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert infer_history_method(ep) == "snapshot_only"

    def test_twse_web_with_date(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            date_params=["date"],
        )
        result = infer_history_method(ep)
        assert "date=YYYYMMDD" in result
        assert "response=json" in result

    def test_tpex_web_with_date(self) -> None:
        ep = EndpointInfo(
            source="tpex",
            endpoint_type="web",
            path="/x",
            date_params=["date"],
        )
        result = infer_history_method(ep)
        assert "date=YYYYMMDD" in result

    def test_mops_year_season(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year", "season"],
        )
        result = infer_history_method(ep)
        assert "ROC_YEAR" in result
        assert "season" in result

    def test_mops_year_month(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            date_params=["year", "month"],
        )
        result = infer_history_method(ep)
        assert "ROC_YEAR" in result
        assert "month" in result

    def test_mops_supports_history_no_date_params(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/x",
            supports_history=True,
        )
        result = infer_history_method(ep)
        assert "see notes" in result


# =====================================================================
# infer_id_field
# =====================================================================


class TestInferIdField:
    def test_exact_match(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            sample_fields=["日期", "證券代號", "成交股數"],
        )
        assert infer_id_field(ep) == "證券代號"

    def test_fuzzy_match_chinese(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            sample_fields=["日期", "個股代號", "收盤價"],
        )
        assert infer_id_field(ep) == "個股代號"

    def test_no_match(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            sample_fields=["日期", "開盤價", "收盤價"],
        )
        assert infer_id_field(ep) == ""

    def test_empty_fields(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert infer_id_field(ep) == ""


# =====================================================================
# infer_request_example
# =====================================================================


class TestInferRequestExample:
    def test_openapi(self) -> None:
        ep = EndpointInfo(
            source="twse", endpoint_type="openapi", path="/exchangeReport/MI"
        )
        result = infer_request_example(ep)
        assert result["method"] == "GET"
        assert "/exchangeReport/MI" in result["url"]

    def test_twse_web_with_date(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/zh/trading/test",
            date_params=["date"],
        )
        result = infer_request_example(ep)
        assert result["params"]["date"] == "20250401"
        assert result["params"]["response"] == "json"

    def test_mops_year_season(self) -> None:
        ep = EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/mops/web/test",
            date_params=["year", "season"],
            method="POST",
        )
        result = infer_request_example(ep)
        assert result["method"] == "POST"
        assert result["params"]["year"] == "114"
        assert result["params"]["season"] == "1"


# =====================================================================
# infer_response_format
# =====================================================================


class TestInferResponseFormat:
    def test_openapi_is_json(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="openapi", path="/x")
        assert infer_response_format(ep) == "json"

    def test_mops_is_html_table(self) -> None:
        ep = EndpointInfo(source="mops", endpoint_type="web", path="/x")
        assert infer_response_format(ep) == "html_table"

    def test_twse_web_is_json(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert infer_response_format(ep) == "json"


# =====================================================================
# infer_coverage
# =====================================================================


class TestInferCoverage:
    def test_twse(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert infer_coverage(ep) == "listed_only"

    def test_tpex(self) -> None:
        ep = EndpointInfo(source="tpex", endpoint_type="web", path="/x")
        assert infer_coverage(ep) == "otc_only"

    def test_mops(self) -> None:
        ep = EndpointInfo(source="mops", endpoint_type="web", path="/x")
        assert infer_coverage(ep) == "all"


# =====================================================================
# enrich_rule_based
# =====================================================================


class TestEnrichRuleBased:
    def test_fills_empty_fields(self, probed_ep: EndpointInfo) -> None:
        updates = enrich_rule_based(probed_ep)
        assert "granularity" in updates
        assert "history_method" in updates
        assert "response_format" in updates
        assert "coverage" in updates
        assert "id_field" in updates

    def test_does_not_override_existing(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            granularity="monthly",
            coverage="all",
        )
        updates = enrich_rule_based(ep)
        assert "granularity" not in updates
        assert "coverage" not in updates


# =====================================================================
# enrich_endpoint
# =====================================================================


class TestEnrichEndpoint:
    def test_rules_only(self, probed_ep: EndpointInfo) -> None:
        result = enrich_endpoint(probed_ep, rules_only=True)
        assert result.granularity != ""
        assert result.coverage != ""

    def test_llm_only_skips_rules(self, probed_ep: EndpointInfo) -> None:
        result = enrich_endpoint(probed_ep, llm_only=True)
        # LLM is None, so no LLM enrichment either
        assert result == probed_ep

    def test_no_changes_returns_same_object(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="openapi",
            path="/x",
            granularity="snapshot",
            history_method="snapshot_only",
            response_format="json",
            coverage="listed_only",
            request_example={"url": "https://test", "method": "GET"},
        )
        result = enrich_endpoint(ep, rules_only=True)
        assert result is ep


# =====================================================================
# enrich_all
# =====================================================================


class TestEnrichAll:
    def test_enriches_probed_endpoints(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            state="probed",
            status="ok",
            date_params=["date"],
            sample_fields=["證券代號", "收盤價"],
        )
        mock_db = MagicMock()
        mock_db.get_endpoints.return_value = [ep]

        count = enrich_all(db=mock_db, rules_only=True)
        assert count == 1
        mock_db.upsert_endpoints.assert_called_once()

    def test_dry_run_does_not_write(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            state="probed",
            date_params=["date"],
        )
        mock_db = MagicMock()
        mock_db.get_endpoints.return_value = [ep]

        count = enrich_all(db=mock_db, rules_only=True, dry_run=True)
        assert count == 1
        mock_db.upsert_endpoints.assert_not_called()

    def test_limit(self) -> None:
        eps = [
            EndpointInfo(
                source="twse",
                endpoint_type="web",
                path=f"/x{i}",
                state="probed",
                date_params=["date"],
            )
            for i in range(5)
        ]
        mock_db = MagicMock()
        mock_db.get_endpoints.return_value = eps

        count = enrich_all(db=mock_db, rules_only=True, limit=2)
        assert count == 2

    def test_force_uses_get_all(self) -> None:
        mock_db = MagicMock()
        mock_db.get_all_endpoints.return_value = []

        enrich_all(db=mock_db, rules_only=True, force=True)
        mock_db.get_all_endpoints.assert_called_once()
        mock_db.get_endpoints.assert_not_called()
