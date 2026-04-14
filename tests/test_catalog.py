"""Tests for EndpointInfo model."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from qadris_datasourcediscovery.catalog import EndpointInfo


class TestEndpointInfoConstruction:
    def test_minimal(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="openapi", path="/test")
        assert ep.source == "twse"
        assert ep.endpoint_type == "openapi"
        assert ep.path == "/test"
        assert ep.status == "unknown"
        assert ep.state == "discovered"
        assert ep.method == "GET"

    def test_all_sources(self) -> None:
        for src in ("twse", "tpex", "mops"):
            ep = EndpointInfo(source=src, endpoint_type="web", path="/x")
            assert ep.source == src

    def test_all_endpoint_types(self) -> None:
        for t in ("openapi", "web", "xbrl"):
            ep = EndpointInfo(source="twse", endpoint_type=t, path="/x")
            assert ep.endpoint_type == t

    def test_all_statuses(self) -> None:
        for s in ("unknown", "ok", "error", "timeout", "empty", "skipped"):
            ep = EndpointInfo(
                source="twse", endpoint_type="web", path="/x", status=s
            )
            assert ep.status == s

    def test_all_states(self) -> None:
        for s in ("discovered", "probed", "enriched"):
            ep = EndpointInfo(
                source="twse", endpoint_type="web", path="/x", state=s
            )
            assert ep.state == s

    def test_defaults(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        assert ep.description == ""
        assert ep.category == ""
        assert ep.supports_history is False
        assert ep.date_params == []
        assert ep.record_count == 0
        assert ep.sample_fields == []
        assert ep.domain_tags == []
        assert ep.request_example == {}
        assert ep.sample_path == ""


class TestEndpointInfoValidation:
    def test_invalid_source(self) -> None:
        with pytest.raises(ValidationError):
            EndpointInfo(source="invalid", endpoint_type="web", path="/x")

    def test_invalid_endpoint_type(self) -> None:
        with pytest.raises(ValidationError):
            EndpointInfo(source="twse", endpoint_type="invalid", path="/x")

    def test_invalid_status(self) -> None:
        with pytest.raises(ValidationError):
            EndpointInfo(
                source="twse", endpoint_type="web", path="/x", status="bad"
            )

    def test_invalid_state(self) -> None:
        with pytest.raises(ValidationError):
            EndpointInfo(
                source="twse", endpoint_type="web", path="/x", state="bad"
            )


class TestEndpointInfoSerialization:
    def test_model_dump(self) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="openapi",
            path="/test",
            domain_tags=["price"],
        )
        d = ep.model_dump()
        assert d["source"] == "twse"
        assert d["domain_tags"] == ["price"]
        assert isinstance(d, dict)

    def test_model_dump_json(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        json_str = ep.model_dump_json()
        assert '"source":"twse"' in json_str or '"source": "twse"' in json_str

    def test_model_copy(self) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        ep2 = ep.model_copy(update={"status": "ok", "state": "probed"})
        assert ep2.status == "ok"
        assert ep2.state == "probed"
        # Original unchanged
        assert ep.status == "unknown"
        assert ep.state == "discovered"

    def test_list_fields_are_independent(self) -> None:
        ep1 = EndpointInfo(source="twse", endpoint_type="web", path="/a")
        ep2 = EndpointInfo(source="twse", endpoint_type="web", path="/b")
        ep1.domain_tags.append("price")
        assert ep2.domain_tags == []
