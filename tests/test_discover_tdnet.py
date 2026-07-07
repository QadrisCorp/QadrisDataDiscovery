"""Tests for discover_tdnet — 檢索面 discovery and mocked probe."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.discover_tdnet import (
    KNOWN_ENDPOINTS,
    _parse_list_page,
    _parse_search_page,
    _recent_weekday,
    discover,
    probe_discovered,
)
from qadris_datasourcediscovery.store.database import CatalogDB

_LIST_HTML = """
<html><body>
<div>全170件（1～100件目）</div>
<table id="main-list-table">
<tr>
  <td class="header-L">時刻</td><td class="header-M">コード</td>
  <td class="header-M">会社名</td><td class="header-M">表題</td>
  <td class="header-M">XBRL</td><td class="header-M">上場取引所</td>
  <td class="header-R">更新履歴</td>
</tr>
<tr>
  <td class="oddnew-L">18:30</td><td class="oddnew-M">43310</td>
  <td class="oddnew-M">Ｔ＆Ｇニーズ</td>
  <td class="oddnew-M"><a href="140120260706588553.pdf">決算短信の訂正</a></td>
  <td class="oddnew-M"><a href="081220260706588553.zip">XBRL</a></td>
  <td class="oddnew-M">東</td><td class="oddnew-R"></td>
</tr>
<tr>
  <td class="evennew-L">17:00</td><td class="evennew-M">72030</td>
  <td class="evennew-M">トヨタ自動車</td>
  <td class="evennew-M"><a href="140120260706588578.pdf">お知らせ</a></td>
  <td class="evennew-M"></td>
  <td class="evennew-M">東</td><td class="evennew-R"></td>
</tr>
</table>
</body></html>
"""

_SEARCH_HTML = """
<html><body>
<div>15件</div>
<table>
<tr class="odd">
  <td class="time">2026/07/06 18:30</td><td class="code">43310</td>
  <td class="companyname">Ｔ＆Ｇニーズ</td>
  <td class="title"><a href="/inbs/140120260706588553.pdf">決算短信の訂正</a></td>
  <td class="xbrl"><a href="/inbs/081220260706588553.zip">XBRL</a></td>
  <td class="exchange">東</td><td class="update"></td>
</tr>
<tr class="even">
  <td class="time">2026/07/06 17:00</td><td class="code">72030</td>
  <td class="companyname">トヨタ自動車</td>
  <td class="title">お知らせ</td><td class="xbrl"></td>
  <td class="exchange">東</td><td class="update"></td>
</tr>
</table>
</body></html>
"""

_EMPTY_SEARCH_HTML = (
    "<html><body>該当する適時開示情報が見つかりませんでした。</body></html>"
)


def _settings(tmp_path: Path) -> DiscoverySettings:
    return DiscoverySettings(project_root=tmp_path, web_delay=0)


class TestDiscover:
    def test_endpoint_count(self) -> None:
        eps = discover(settings=DiscoverySettings())
        assert len(eps) == len(KNOWN_ENDPOINTS)
        assert len(eps) >= 8

    def test_31day_window_in_all_notes(self) -> None:
        eps = discover(settings=DiscoverySettings())
        assert all("31 天" in ep.notes for ep in eps)

    def test_facets_present(self) -> None:
        eps = discover(settings=DiscoverySettings())
        paths = {ep.path for ep in eps}
        assert "/inbs/I_list_{page}_{YYYYMMDD}.html" in paths
        assert any("#facet=code" in p for p in paths)
        assert any("#facet=disclosure-type" in p for p in paths)
        assert any(p.endswith(".zip") for p in paths)

    def test_xbrl_zip_is_tanshin_source(self) -> None:
        eps = discover(settings=DiscoverySettings())
        zip_ep = next(ep for ep in eps if ep.path.endswith(".zip"))
        assert zip_ep.response_format == "zip"
        assert "四半期報告書廢止" in zip_ep.notes


class TestParseListPage:
    def test_parse(self) -> None:
        parsed = _parse_list_page(_LIST_HTML)
        assert parsed["total"] == 170
        assert len(parsed["rows"]) == 2
        assert parsed["rows"][0][1] == "43310"
        assert parsed["pdf_links"] == [
            "140120260706588553.pdf",
            "140120260706588578.pdf",
        ]
        assert parsed["zip_links"] == ["081220260706588553.zip"]

    def test_parse_empty(self) -> None:
        parsed = _parse_list_page(_EMPTY_SEARCH_HTML)
        assert parsed["total"] == 0
        assert parsed["rows"] == []

    def test_parse_skips_non_data_rows(self) -> None:
        """kaiji-info 等第 2 欄非銘柄コード的列不得混入。"""
        html = _LIST_HTML.replace(
            '<td class="oddnew-L">18:30</td><td class="oddnew-M">43310</td>',
            '<td class="oddnew-L"></td>'
            '<td class="oddnew-M">2026年07月06日に開示された情報</td>',
            1,
        )
        parsed = _parse_list_page(html)
        assert len(parsed["rows"]) == 1
        assert parsed["rows"][0][1] == "72030"

    def test_parse_search_page(self) -> None:
        parsed = _parse_search_page(_SEARCH_HTML)
        assert parsed["total"] == 15
        assert len(parsed["rows"]) == 2
        assert parsed["rows"][0]["code"] == "43310"

    def test_parse_search_page_empty(self) -> None:
        parsed = _parse_search_page(_EMPTY_SEARCH_HTML)
        assert parsed["rows"] == []

    def test_recent_weekday(self) -> None:
        from datetime import date

        d = _recent_weekday(date(2026, 7, 6))  # 週一 → 上週五
        assert d == "20260703"


class TestProbe:
    def _seed(self, settings: DiscoverySettings) -> None:
        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(discover(settings=settings))

    def test_probe_all_facets(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path)
        self._seed(settings)

        def fake_get(url: str, **kw: object) -> MagicMock:
            resp = MagicMock()
            resp.status_code = 200
            if "I_list_001_" in url:
                resp.text = _LIST_HTML
            elif "I_main_00" in url:
                resp.text = '<iframe src="I_list_001_20260706.html">'
            else:  # pdf / zip
                resp.content = b"%PDF-1.4 fake"
            return resp

        def fake_post(url: str, data: dict[str, str], **kw: object) -> MagicMock:
            resp = MagicMock()
            resp.status_code = 200
            resp.text = _SEARCH_HTML if data.get("q") else _EMPTY_SEARCH_HTML
            return resp

        session = MagicMock()
        session.get.side_effect = fake_get
        session.post.side_effect = fake_post

        with (
            patch(
                "qadris_datasourcediscovery.discover_tdnet._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_tdnet.delay"),
        ):
            results = probe_discovered(settings=settings, limit=100)

        by_path = {r.path: r for r in results}
        assert all(r.state == "probed" for r in results)

        lst = by_path["/inbs/I_list_{page}_{YYYYMMDD}.html"]
        assert lst.status == "ok"
        assert lst.record_count == 170
        assert "全170件" in lst.notes

        code_search = next(
            r for r in results if r.path.endswith("#facet=code")
        )
        assert code_search.status == "ok"
        assert "q='43310'" in code_search.notes
        assert code_search.record_count == 15

        type_search = next(
            r for r in results if "#facet=disclosure-type" in r.path
        )
        assert type_search.status == "ok"

        window_search = next(
            r for r in results if "#facet=code-window" in r.path
        )
        assert window_search.status == "ok"

        pdf_ep = next(r for r in results if r.path.endswith(".pdf"))
        assert pdf_ep.status == "ok"
        assert pdf_ep.record_count == 2

        zip_ep = next(r for r in results if r.path.endswith(".zip"))
        assert zip_ep.status == "ok"
        assert zip_ep.record_count == 1

    def test_probe_list_unreachable_marks_error(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path)
        self._seed(settings)

        resp = MagicMock()
        resp.status_code = 404
        resp.text = ""
        session = MagicMock()
        session.get.return_value = resp
        session.post.return_value = resp

        with (
            patch(
                "qadris_datasourcediscovery.discover_tdnet._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_tdnet.delay"),
        ):
            results = probe_discovered(settings=settings, limit=100)

        lst = next(r for r in results if r.path.startswith("/inbs/I_list_"))
        assert lst.status == "error"
