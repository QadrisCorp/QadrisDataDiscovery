"""Tests for discover_jquants — spec catalog discovery and mocked probe."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.discover_jquants import (
    KNOWN_ENDPOINTS,
    _probe_date,
    discover,
    probe_discovered,
)
from qadris_datasourcediscovery.exceptions import ConfigurationError
from qadris_datasourcediscovery.store.database import CatalogDB


def _settings(tmp_path: Path, **kwargs: str) -> DiscoverySettings:
    return DiscoverySettings(project_root=tmp_path, **kwargs)


class TestDiscover:
    def test_endpoint_count(self) -> None:
        eps = discover(settings=DiscoverySettings())
        assert len(eps) == len(KNOWN_ENDPOINTS)
        assert len(eps) >= 25

    def test_all_discovered_state(self) -> None:
        eps = discover(settings=DiscoverySettings())
        assert all(ep.state == "discovered" for ep in eps)
        assert all(ep.source == "jquants" for ep in eps)
        assert all(ep.endpoint_type == "openapi" for ep in eps)

    def test_plan_recorded_in_notes(self) -> None:
        eps = discover(settings=DiscoverySettings())
        assert all("plan=" in ep.notes for ep in eps)
        by_path = {ep.path: ep for ep in eps}
        assert "plan=Free" in by_path["/equities/bars/daily"].notes
        assert "plan=Premium" in by_path["/fins/dividend"].notes
        assert "plan=Standard" in by_path["/edinet/major-shareholders"].notes

    def test_sample_fields_prefilled_from_spec(self) -> None:
        eps = discover(settings=DiscoverySettings())
        by_path = {ep.path: ep for ep in eps}
        assert "AdjFactor" in by_path["/equities/bars/daily"].sample_fields
        assert "EPS" in by_path["/fins/summary"].sample_fields

    def test_key_domains_present(self) -> None:
        """Phase 1 datalake 三域（財報/股價/股利）的 endpoint 必須在清單內。"""
        paths = {ep["path"] for ep in KNOWN_ENDPOINTS}
        assert "/equities/bars/daily" in paths
        assert "/fins/summary" in paths
        assert "/fins/details" in paths
        assert "/fins/dividend" in paths


class TestProbeDate:
    def test_weekday(self) -> None:
        d = _probe_date(date(2026, 7, 7))
        assert date.fromisoformat(d).weekday() < 5

    def test_about_13_weeks_back(self) -> None:
        d = date.fromisoformat(_probe_date(date(2026, 7, 7)))
        assert (date(2026, 7, 7) - d).days >= 90


def _mock_response(status_code: int, payload: object) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = payload
    return resp


class TestProbe:
    def test_missing_key_raises(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, jquants_api_key="")
        with pytest.raises(ConfigurationError, match="RSR_JQUANTS_API_KEY"):
            probe_discovered(settings=settings, limit=5)

    def _seed(
        self, settings: DiscoverySettings, paths: list[str] | None = None
    ) -> None:
        eps = discover(settings=settings)
        if paths is not None:
            eps = [ep for ep in eps if ep.path in paths]
        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(eps)

    def test_probe_ok(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, jquants_api_key="k")
        self._seed(
            settings, paths=["/equities/bars/daily", "/equities/master"]
        )

        payload = {
            "data": [{"Date": "2026-04-06", "Code": "72030", "C": 3000.0}],
            "pagination_key": "abc",
        }
        session = MagicMock()
        session.get.return_value = _mock_response(200, payload)

        with (
            patch(
                "qadris_datasourcediscovery.discover_jquants._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_jquants.delay"),
        ):
            results = probe_discovered(settings=settings, limit=2)

        assert len(results) == 2
        ok = [r for r in results if r.status == "ok"]
        assert ok
        assert ok[0].state == "probed"
        assert ok[0].record_count == 1
        assert "Code" in ok[0].sample_fields
        assert "paginated" in ok[0].notes

    def test_probe_plan_gated_is_skipped_not_error(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, jquants_api_key="k")
        self._seed(
            settings,
            paths=["/fins/dividend", "/fins/details", "/markets/breakdown"],
        )

        session = MagicMock()
        session.get.return_value = _mock_response(403, {"message": "forbidden"})

        with (
            patch(
                "qadris_datasourcediscovery.discover_jquants._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_jquants.delay"),
        ):
            results = probe_discovered(settings=settings, limit=3)

        assert all(r.status == "skipped" for r in results)
        assert all(r.state == "probed" for r in results)
        assert all("401/403" in r.notes for r in results)

    def test_probe_id_required_endpoint_skipped_without_request(
        self, tmp_path: Path
    ) -> None:
        settings = _settings(tmp_path, jquants_api_key="k")
        eps = [ep for ep in discover(settings=settings) if ep.path == "/td/files"]
        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(eps)

        session = MagicMock()
        with (
            patch(
                "qadris_datasourcediscovery.discover_jquants._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_jquants.delay"),
        ):
            results = probe_discovered(settings=settings, limit=5)

        assert len(results) == 1
        assert results[0].status == "skipped"
        session.get.assert_not_called()

    def test_probe_state_upgrade_persists(self, tmp_path: Path) -> None:
        """probe 結果 upsert 後 state 升為 probed（只升不降）。"""
        settings = _settings(tmp_path, jquants_api_key="k")
        self._seed(settings, paths=["/equities/bars/daily"])

        session = MagicMock()
        session.get.return_value = _mock_response(200, {"data": []})

        with (
            patch(
                "qadris_datasourcediscovery.discover_jquants._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_jquants.delay"),
        ):
            results = probe_discovered(settings=settings, limit=1)

        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(results)
            ep = db.get_endpoint("jquants", results[0].path)

        assert ep is not None
        assert ep.state == "probed"
        assert ep.status == "empty"
