"""Tests for CLI commands using Typer CliRunner."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.cli import app
from qadris_datasourcediscovery.store.database import CatalogDB

runner = CliRunner()


def _seed_db(db: CatalogDB) -> None:
    """Insert a few endpoints for CLI tests."""
    eps = [
        EndpointInfo(
            source="twse",
            endpoint_type="openapi",
            path="/opendata/test1",
            description="Test endpoint 1",
            status="ok",
            state="enriched",
            domain_tags=["price", "volume"],
            granularity="snapshot",
        ),
        EndpointInfo(
            source="tpex",
            endpoint_type="web",
            path="/zh-tw/trading/test2",
            description="Test endpoint 2",
            status="ok",
            state="probed",
            supports_history=True,
            date_params=["date"],
        ),
        EndpointInfo(
            source="mops",
            endpoint_type="web",
            path="/mops/web/test3",
            description="Test endpoint 3",
            status="error",
            state="discovered",
        ),
    ]
    db.upsert_endpoints(eps)


def _make_db(tmp_path: Path) -> CatalogDB:
    db = CatalogDB(tmp_path / "catalog" / "catalog.db")
    _seed_db(db)
    return db


class TestSearchCommand:
    def test_search_all(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["search"])
        assert result.exit_code == 0
        assert "3 endpoints" in result.stdout

    def test_search_by_source(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["search", "--source", "twse"])
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout

    def test_search_by_tag(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["search", "--tag", "price"])
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout

    def test_search_no_results(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(
                app, ["search", "--tag", "nonexistent"]
            )
        assert result.exit_code == 0
        assert "No endpoints found" in result.stdout

    def test_search_json_output(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["search", "--json"])
        assert result.exit_code == 0
        assert '"source"' in result.stdout

    def test_search_by_keyword(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(
                app, ["search", "--keyword", "endpoint 2"]
            )
        assert result.exit_code == 0
        assert "1 endpoints" in result.stdout


class TestShowCommand:
    def test_show_existing(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(
                app, ["show", "twse:/opendata/test1"]
            )
        assert result.exit_code == 0
        assert "Test endpoint 1" in result.stdout

    def test_show_nonexistent(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(
                app, ["show", "twse:/nonexistent"]
            )
        assert result.exit_code == 1

    def test_show_bad_format(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["show", "nocolon"])
        assert result.exit_code == 1

    def test_show_json_output(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(
                app, ["show", "twse:/opendata/test1", "--json"]
            )
        assert result.exit_code == 0
        assert '"source": "twse"' in result.stdout


class TestTagsCommand:
    def test_tags(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["tags"])
        assert result.exit_code == 0
        assert "price" in result.stdout

    def test_tags_json(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["tags", "--json"])
        assert result.exit_code == 0
        assert '"price"' in result.stdout

    def test_tags_empty(self, tmp_path: Path) -> None:
        db = CatalogDB(tmp_path / "catalog" / "empty.db")
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["tags"])
        assert result.exit_code == 0
        assert "No domain tags" in result.stdout
        db.close()


class TestStatsCommand:
    def test_stats(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["stats"])
        assert result.exit_code == 0
        assert "3 endpoints" in result.stdout

    def test_stats_json(self, tmp_path: Path) -> None:
        db = _make_db(tmp_path)
        with patch(
            "qadris_datasourcediscovery.cli._get_db", return_value=db
        ):
            result = runner.invoke(app, ["stats", "--json"])
        assert result.exit_code == 0
        assert '"total": 3' in result.stdout
