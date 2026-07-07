"""Tests for discover_edinet — 書類種別×取得格式 discovery and mocked probe."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.discover_edinet import (
    DOC_TYPES,
    FORMATS,
    _extract_csv_fields,
    _recent_business_days,
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
        assert len(eps) == 1 + len(DOC_TYPES) * len(FORMATS)
        assert len(eps) >= 15

    def test_granularity_by_doc_type(self) -> None:
        eps = discover(settings=DiscoverySettings())
        yuho_csv = next(
            ep for ep in eps if "docTypeCode=120" in ep.path and "type=5" in ep.path
        )
        assert yuho_csv.granularity == "yearly"
        assert yuho_csv.category == "有価証券報告書"
        assert yuho_csv.response_format == "csv"
        assert yuho_csv.id_field == "docID"
        assert yuho_csv.date_params == ["date"]

    def test_list_endpoint(self) -> None:
        eps = discover(settings=DiscoverySettings())
        lst = next(ep for ep in eps if ep.path == "/documents.json")
        assert "docID" in lst.sample_fields
        assert "edinetCode" in lst.sample_fields
        assert lst.response_format == "json"

    def test_large_holding_present(self) -> None:
        """大量保有報告書（5% 規則）必須在目錄內。"""
        eps = discover(settings=DiscoverySettings())
        assert any(ep.category == "大量保有報告書" for ep in eps)

    def test_quarterly_abolished_note(self) -> None:
        eps = discover(settings=DiscoverySettings())
        q = next(ep for ep in eps if ep.category == "四半期報告書")
        assert "廢止" in q.notes


class TestHelpers:
    def test_recent_business_days_weekdays_only(self) -> None:
        from datetime import date

        days = _recent_business_days(5, today=date(2026, 7, 7))
        assert len(days) == 5
        for d in days:
            assert date.fromisoformat(d).weekday() < 5

    def test_extract_csv_fields_utf16_tsv(self) -> None:
        buf = io.BytesIO()
        csv_content = "要素ID\t項目名\tコンテキストID\t値\n".encode("utf-16")
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("XBRL_TO_CSV/jpcrp030000-asr-001.csv", csv_content)
        fields = _extract_csv_fields(buf.getvalue())
        assert fields == ["要素ID", "項目名", "コンテキストID", "値"]

    def test_extract_csv_fields_no_csv(self) -> None:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("readme.txt", "x")
        assert _extract_csv_fields(buf.getvalue()) == []


def _list_payload() -> dict[str, object]:
    return {
        "metadata": {"resultset": {"count": 2}},
        "results": [
            {
                "docID": "S100XXX1",
                "edinetCode": "E12345",
                "secCode": "72030",
                "filerName": "トヨタ自動車株式会社",
                "docTypeCode": "120",
                "submitDateTime": "2026-06-24 09:00",
                "xbrlFlag": "1",
                "pdfFlag": "1",
                "csvFlag": "1",
            },
            {
                "docID": "S100XXX2",
                "edinetCode": "E67890",
                "secCode": "67580",
                "filerName": "ソニーグループ株式会社",
                "docTypeCode": "350",
                "submitDateTime": "2026-06-24 10:00",
                "xbrlFlag": "1",
                "pdfFlag": "1",
                "csvFlag": "1",
            },
        ],
    }


def _csv_zip_bytes() -> bytes:
    buf = io.BytesIO()
    content = "要素ID\t項目名\t値\n".encode("utf-16")
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("XBRL_TO_CSV/report.csv", content)
    return buf.getvalue()


class TestProbe:
    def test_missing_key_raises(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, edinet_api_key="")
        with pytest.raises(ConfigurationError, match="RSR_EDINET_API_KEY"):
            probe_discovered(settings=settings, limit=5)

    def _seed(self, settings: DiscoverySettings) -> None:
        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(discover(settings=settings))

    def test_probe_marks_doc_types_from_list(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, edinet_api_key="key")
        self._seed(settings)

        def fake_get(url: str, params: dict[str, str] | None = None, **kw: object):
            resp = MagicMock()
            resp.status_code = 200
            if url.endswith("/documents.json"):
                resp.json.return_value = _list_payload()
            else:
                resp.content = _csv_zip_bytes()
                resp.raise_for_status.return_value = None
            return resp

        session = MagicMock()
        session.get.side_effect = fake_get

        with (
            patch(
                "qadris_datasourcediscovery.discover_edinet._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_edinet.delay"),
        ):
            results = probe_discovered(settings=settings, limit=100)

        by_path = {r.path: r for r in results}

        lst = by_path["/documents.json"]
        assert lst.status == "ok"
        assert lst.record_count > 0
        assert "docID" in lst.sample_fields

        yuho_csv = next(
            r
            for r in results
            if "docTypeCode=120" in r.path and "type=5" in r.path
        )
        assert yuho_csv.status == "ok"
        assert "要素ID" in yuho_csv.sample_fields  # CSV 樣本欄位回填

        holding_xbrl = next(
            r
            for r in results
            if "docTypeCode=350" in r.path and "type=1" in r.path
        )
        assert holding_xbrl.status == "ok"

        # 掃描日內沒出現的種別 → empty（非 error）
        hanki = next(
            r
            for r in results
            if "docTypeCode=160" in r.path and "type=5" in r.path
        )
        assert hanki.status == "empty"

    def test_probe_auth_failure_marks_error(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path, edinet_api_key="bad")
        self._seed(settings)

        resp = MagicMock()
        resp.status_code = 401
        session = MagicMock()
        session.get.return_value = resp

        with (
            patch(
                "qadris_datasourcediscovery.discover_edinet._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_edinet.delay"),
        ):
            results = probe_discovered(settings=settings, limit=100)

        assert all(r.status == "error" for r in results)
        assert all("金鑰無效" in r.notes for r in results)
