"""Tests for the source registry, auth hook, and multi-market framework."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from typer.testing import CliRunner

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.cli import app
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.enrich import (
    infer_coverage,
    infer_granularity,
    infer_history_method,
    infer_id_field,
    infer_request_example,
    infer_response_format,
)
from qadris_datasourcediscovery.exceptions import ConfigurationError, FetchError
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    auth_query_params,
    fetch_excel_fields,
)
from qadris_datasourcediscovery.registry import (
    SOURCE_REGISTRY,
    get_market,
    sources_for_market,
)
from qadris_datasourcediscovery.store.database import CatalogDB

runner = CliRunner()


class TestRegistry:
    def test_all_sources_present(self) -> None:
        assert set(SOURCE_REGISTRY) == {
            "twse",
            "tpex",
            "mops",
            "tdcc",
            "jquants",
            "edinet",
            "tdnet",
            "jpx",
        }

    def test_markets(self) -> None:
        assert get_market("twse") == "tw"
        assert get_market("jquants") == "jp"
        assert get_market("unknown") == ""
        assert sources_for_market("jp") == ["jquants", "edinet", "tdnet", "jpx"]
        assert len(sources_for_market()) == 8

    def test_auth_specs(self) -> None:
        jq = SOURCE_REGISTRY["jquants"].auth
        assert jq is not None
        assert jq.kind == "header"
        assert jq.param_name == "x-api-key"

        ed = SOURCE_REGISTRY["edinet"].auth
        assert ed is not None
        assert ed.kind == "query"
        assert ed.param_name == "Subscription-Key"

        assert SOURCE_REGISTRY["twse"].auth is None

    def test_probe_modules_exist(self) -> None:
        """registry 指到的 probe module 名稱必須符合套件命名。"""
        for spec in SOURCE_REGISTRY.values():
            if spec.probe_module:
                assert spec.probe_module.startswith("qadris_datasourcediscovery.")


class TestConfigBaseUrls:
    def test_tw_base_urls_unchanged(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("twse", "openapi") == "https://openapi.twse.com.tw/v1"
        assert s.get_base_url("twse", "web") == "https://www.twse.com.tw"
        assert s.get_base_url("mops", "web") == "https://mops.twse.com.tw"
        assert s.get_base_url("mops", "xbrl") == "https://mops.twse.com.tw"
        assert s.get_base_url("tdcc", "openapi") == "https://openapi.tdcc.com.tw"

    def test_jp_base_urls(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("jquants", "openapi") == "https://api.jquants.com/v2"
        assert (
            s.get_base_url("edinet", "openapi")
            == "https://api.edinet-fsa.go.jp/api/v2"
        )
        assert s.get_base_url("tdnet", "web") == "https://www.release.tdnet.info"
        assert s.get_base_url("jpx", "web") == "https://www.jpx.co.jp"

    def test_unknown_returns_empty(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("nosuch", "openapi") == ""
        assert s.get_base_url("jquants", "web") == ""


class TestApiKeys:
    def test_require_api_key_missing_raises(self) -> None:
        s = DiscoverySettings(jquants_api_key="")
        with pytest.raises(ConfigurationError, match="RSR_JQUANTS_API_KEY"):
            s.require_api_key("jquants")

    def test_require_api_key_present(self) -> None:
        s = DiscoverySettings(jquants_api_key="k123")
        assert s.require_api_key("jquants") == "k123"

    def test_require_api_key_no_auth_source(self) -> None:
        s = DiscoverySettings()
        assert s.require_api_key("twse") == ""

    def test_get_api_key(self) -> None:
        # _env_file=None：隔離開發機本地 .env 的金鑰
        s = DiscoverySettings(_env_file=None, edinet_api_key="e456")
        assert s.get_api_key("edinet") == "e456"
        assert s.get_api_key("jquants") == ""


class TestAuthInjection:
    def test_header_auth_injected(self) -> None:
        s = DiscoverySettings(jquants_api_key="k123")
        session = _create_session(settings=s, source="jquants")
        assert session.headers["x-api-key"] == "k123"

    def test_header_auth_absent_without_key(self) -> None:
        s = DiscoverySettings(jquants_api_key="")
        session = _create_session(settings=s, source="jquants")
        assert "x-api-key" not in session.headers

    def test_no_auth_for_tw_sources(self) -> None:
        s = DiscoverySettings()
        session = _create_session(settings=s, source="twse")
        assert "x-api-key" not in session.headers

    def test_query_auth_params(self) -> None:
        s = DiscoverySettings(_env_file=None, edinet_api_key="e456")
        assert auth_query_params("edinet", settings=s) == {"Subscription-Key": "e456"}
        no_key = DiscoverySettings(_env_file=None)
        assert auth_query_params("edinet", settings=no_key) == {}
        assert auth_query_params("twse", settings=s) == {}


def _mock_excel_session(content: bytes) -> MagicMock:
    session = MagicMock()
    resp = MagicMock()
    resp.content = content
    resp.status_code = 200
    resp.raise_for_status.return_value = None
    session.get.return_value = resp
    return session


class TestFetchExcelFields:
    def test_xlsx_with_title_rows(self) -> None:
        """JPX 型 Excel：標題列在前、真正 header 在第 3 列。"""
        buf = BytesIO()
        df = pd.DataFrame(
            [
                ["投資部門別売買状況", None, None],
                [None, None, None],
                ["銘柄コード", "銘柄名", "売買代金"],
                ["1301", "極洋", 1000],
                ["1332", "ニッスイ", 2000],
            ]
        )
        df.to_excel(buf, index=False, header=False)
        session = _mock_excel_session(buf.getvalue())

        fields, count, status = fetch_excel_fields(
            "https://example.com/x.xlsx",
            session=session,
            settings=DiscoverySettings(),
        )
        assert fields == ["銘柄コード", "銘柄名", "売買代金"]
        assert count == 2
        assert status == 200

    def test_non_excel_raises(self) -> None:
        session = _mock_excel_session(b"<html>not excel</html>")
        with pytest.raises(FetchError, match="Not an Excel file"):
            fetch_excel_fields(
                "https://example.com/x.xls",
                session=session,
                settings=DiscoverySettings(),
            )


class TestEnrichJapanRules:
    def test_granularity_tw_openapi_still_snapshot(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="openapi", path="/x")
        assert infer_granularity(ep) == "snapshot"

    def test_granularity_jquants_daily(self) -> None:
        ep = EndpointInfo(
            source="jquants",
            endpoint_type="openapi",
            path="/equities/bars/daily",
            date_params=["date"],
            supports_history=True,
        )
        assert infer_granularity(ep) == "daily"

    def test_history_method_edinet(self) -> None:
        ep = EndpointInfo(
            source="edinet",
            endpoint_type="openapi",
            path="/documents.json",
            date_params=["date"],
            supports_history=True,
        )
        assert "YYYY-MM-DD" in infer_history_method(ep)

    def test_history_method_tdnet_mentions_31_days(self) -> None:
        ep = EndpointInfo(
            source="tdnet",
            endpoint_type="web",
            path="/inbs/I_list_001_YYYYMMDD.html",
            supports_history=True,
        )
        assert "31 days" in infer_history_method(ep)

    def test_id_field_japanese_known(self) -> None:
        ep = EndpointInfo(
            source="jquants",
            endpoint_type="openapi",
            path="/x",
            sample_fields=["Date", "LocalCode", "Close"],
        )
        assert infer_id_field(ep) == "LocalCode"

    def test_id_field_japanese_fuzzy(self) -> None:
        ep = EndpointInfo(
            source="jpx",
            endpoint_type="web",
            path="/x",
            sample_fields=["日付", "発行者コード", "残高"],
        )
        assert infer_id_field(ep) == "発行者コード"

    def test_request_example_jquants_has_auth_header(self) -> None:
        ep = EndpointInfo(
            source="jquants",
            endpoint_type="openapi",
            path="/equities/bars/daily",
            date_params=["date"],
        )
        example = infer_request_example(ep)
        assert example["url"] == "https://api.jquants.com/v2/equities/bars/daily"
        assert example["headers"] == {"x-api-key": "<YOUR_API_KEY>"}
        assert example["params"]["date"] == "2026-06-30"

    def test_request_example_edinet_has_subscription_key(self) -> None:
        ep = EndpointInfo(
            source="edinet",
            endpoint_type="openapi",
            path="/documents.json",
            date_params=["date"],
        )
        example = infer_request_example(ep)
        assert example["params"]["Subscription-Key"] == "<YOUR_API_KEY>"

    def test_response_format_jp(self) -> None:
        assert (
            infer_response_format(
                EndpointInfo(source="jquants", endpoint_type="openapi", path="/x")
            )
            == "json"
        )
        assert (
            infer_response_format(
                EndpointInfo(source="tdnet", endpoint_type="web", path="/x")
            )
            == "html_table"
        )
        assert (
            infer_response_format(
                EndpointInfo(source="jpx", endpoint_type="web", path="/x")
            )
            == "excel"
        )

    def test_coverage_jp_default_all(self) -> None:
        for src in ("jquants", "edinet", "tdnet", "jpx"):
            ep = EndpointInfo(source=src, endpoint_type="web", path="/x")  # type: ignore[arg-type]
            assert infer_coverage(ep) == "all"

    def test_coverage_tw_unchanged(self) -> None:
        assert (
            infer_coverage(
                EndpointInfo(source="twse", endpoint_type="openapi", path="/x")
            )
            == "listed_only"
        )


def _seed_multimarket_db(tmp_path: Path) -> CatalogDB:
    db = CatalogDB(tmp_path / "catalog" / "catalog.db")
    db.upsert_endpoints(
        [
            EndpointInfo(
                source="twse",
                endpoint_type="openapi",
                path="/opendata/t1",
                description="TW endpoint",
                status="ok",
                state="enriched",
                domain_tags=["price"],
            ),
            EndpointInfo(
                source="jquants",
                endpoint_type="openapi",
                path="/equities/bars/daily",
                description="JP daily bars",
                status="ok",
                state="enriched",
                domain_tags=["price"],
            ),
        ]
    )
    return db


class TestMarketFilterCLI:
    def test_search_market_jp(self, tmp_path: Path) -> None:
        db = _seed_multimarket_db(tmp_path)
        with patch("qadris_datasourcediscovery.cli._get_db", return_value=db):
            result = runner.invoke(app, ["search", "--market", "jp"])
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout

    def test_search_market_tw(self, tmp_path: Path) -> None:
        db = _seed_multimarket_db(tmp_path)
        with patch("qadris_datasourcediscovery.cli._get_db", return_value=db):
            result = runner.invoke(app, ["search", "--market", "tw"])
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout

    def test_stats_market_filter(self, tmp_path: Path) -> None:
        db = _seed_multimarket_db(tmp_path)
        with patch("qadris_datasourcediscovery.cli._get_db", return_value=db):
            result = runner.invoke(app, ["stats", "--market", "jp"])
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout
