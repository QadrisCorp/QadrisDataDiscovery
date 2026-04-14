"""Tests for CatalogDB persistence layer."""

from __future__ import annotations

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.store.database import CatalogDB


class TestCatalogDBCRUD:
    def test_upsert_and_get(self, tmp_db: CatalogDB, sample_ep: EndpointInfo) -> None:
        tmp_db.upsert_endpoints([sample_ep])
        result = tmp_db.get_endpoint("twse", "/opendata/test")
        assert result is not None
        assert result.source == "twse"
        assert result.path == "/opendata/test"

    def test_upsert_empty_list(self, tmp_db: CatalogDB) -> None:
        assert tmp_db.upsert_endpoints([]) == 0

    def test_upsert_returns_count(
        self, tmp_db: CatalogDB, sample_ep: EndpointInfo
    ) -> None:
        count = tmp_db.upsert_endpoints([sample_ep])
        assert count == 1

    def test_get_nonexistent(self, tmp_db: CatalogDB) -> None:
        result = tmp_db.get_endpoint("twse", "/nonexistent")
        assert result is None

    def test_get_all_endpoints(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(source="twse", endpoint_type="openapi", path="/a"),
            EndpointInfo(source="tpex", endpoint_type="web", path="/b"),
        ]
        tmp_db.upsert_endpoints(eps)
        results = tmp_db.get_all_endpoints()
        assert len(results) == 2

    def test_get_endpoints_filter_by_source(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(source="twse", endpoint_type="openapi", path="/a"),
            EndpointInfo(source="tpex", endpoint_type="web", path="/b"),
        ]
        tmp_db.upsert_endpoints(eps)
        twse = tmp_db.get_endpoints(source="twse")
        assert len(twse) == 1
        assert twse[0].source == "twse"

    def test_get_endpoints_filter_by_state(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(
                source="twse", endpoint_type="web", path="/a", state="probed"
            ),
            EndpointInfo(
                source="twse", endpoint_type="web", path="/b", state="discovered"
            ),
        ]
        tmp_db.upsert_endpoints(eps)
        probed = tmp_db.get_endpoints(state="probed")
        assert len(probed) == 1
        assert probed[0].path == "/a"

    def test_get_endpoints_filter_by_status(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(
                source="twse", endpoint_type="web", path="/a", status="ok"
            ),
            EndpointInfo(
                source="twse", endpoint_type="web", path="/b", status="error"
            ),
        ]
        tmp_db.upsert_endpoints(eps)
        ok_eps = tmp_db.get_endpoints(status="ok")
        assert len(ok_eps) == 1


class TestUpsertStateMonotonicity:
    def test_upsert_probed_over_discovered(self, tmp_db: CatalogDB) -> None:
        ep1 = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="discovered"
        )
        tmp_db.upsert_endpoints([ep1])

        ep2 = ep1.model_copy(update={"state": "probed", "status": "ok"})
        tmp_db.upsert_endpoints([ep2])

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "probed"

    def test_upsert_discovered_over_probed_keeps_probed(
        self, tmp_db: CatalogDB
    ) -> None:
        ep1 = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="probed"
        )
        tmp_db.upsert_endpoints([ep1])

        ep2 = ep1.model_copy(update={"state": "discovered"})
        tmp_db.upsert_endpoints([ep2])

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "probed"

    def test_upsert_enriched_over_probed(self, tmp_db: CatalogDB) -> None:
        ep1 = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="probed"
        )
        tmp_db.upsert_endpoints([ep1])

        ep2 = ep1.model_copy(update={"state": "enriched"})
        tmp_db.upsert_endpoints([ep2])

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "enriched"

    def test_upsert_probed_over_enriched_keeps_enriched(
        self, tmp_db: CatalogDB
    ) -> None:
        ep1 = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="enriched"
        )
        tmp_db.upsert_endpoints([ep1])

        ep2 = ep1.model_copy(update={"state": "probed"})
        tmp_db.upsert_endpoints([ep2])

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "enriched"


class TestUpdateStateMonotonicity:
    def test_update_discovered_to_probed(self, tmp_db: CatalogDB) -> None:
        ep = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="discovered"
        )
        tmp_db.upsert_endpoints([ep])
        tmp_db.update_state("twse", "/x", "probed")

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "probed"

    def test_cannot_downgrade_enriched_to_discovered(
        self, tmp_db: CatalogDB
    ) -> None:
        ep = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="enriched"
        )
        tmp_db.upsert_endpoints([ep])
        tmp_db.update_state("twse", "/x", "discovered")

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "enriched"

    def test_cannot_downgrade_probed_to_discovered(
        self, tmp_db: CatalogDB
    ) -> None:
        ep = EndpointInfo(
            source="twse", endpoint_type="web", path="/x", state="probed"
        )
        tmp_db.upsert_endpoints([ep])
        tmp_db.update_state("twse", "/x", "discovered")

        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.state == "probed"


class TestCatalogDBCount:
    def test_count_all(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(source="twse", endpoint_type="openapi", path="/a"),
            EndpointInfo(source="tpex", endpoint_type="web", path="/b"),
        ]
        tmp_db.upsert_endpoints(eps)
        assert tmp_db.count() == 2

    def test_count_by_source(self, tmp_db: CatalogDB) -> None:
        eps = [
            EndpointInfo(source="twse", endpoint_type="openapi", path="/a"),
            EndpointInfo(source="twse", endpoint_type="web", path="/b"),
            EndpointInfo(source="tpex", endpoint_type="web", path="/c"),
        ]
        tmp_db.upsert_endpoints(eps)
        assert tmp_db.count(source="twse") == 2
        assert tmp_db.count(source="tpex") == 1

    def test_count_empty_db(self, tmp_db: CatalogDB) -> None:
        assert tmp_db.count() == 0


class TestCatalogDBContextManager:
    def test_context_manager(self, tmp_path: "Path") -> None:
        from pathlib import Path

        db_path = Path(tmp_path) / "ctx.db"
        with CatalogDB(db_path) as db:
            ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
            db.upsert_endpoints([ep])
            assert db.count() == 1


class TestCatalogDBJsonSerialization:
    def test_list_fields_roundtrip(self, tmp_db: CatalogDB) -> None:
        ep = EndpointInfo(
            source="twse",
            endpoint_type="web",
            path="/x",
            date_params=["date", "month"],
            sample_fields=["收盤價", "成交量"],
            domain_tags=["price", "volume"],
            request_example={"url": "https://test.com", "method": "GET"},
        )
        tmp_db.upsert_endpoints([ep])
        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.date_params == ["date", "month"]
        assert result.sample_fields == ["收盤價", "成交量"]
        assert result.domain_tags == ["price", "volume"]
        assert result.request_example == {
            "url": "https://test.com",
            "method": "GET",
        }

    def test_empty_list_roundtrip(self, tmp_db: CatalogDB) -> None:
        ep = EndpointInfo(source="twse", endpoint_type="web", path="/x")
        tmp_db.upsert_endpoints([ep])
        result = tmp_db.get_endpoint("twse", "/x")
        assert result is not None
        assert result.date_params == []
        assert result.domain_tags == []
