"""Tests for discover_jpx — 頁面樹爬取、序列鍵、Excel/PDF probe（HTTP mock）。"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.discover_jpx import (
    _collect_subpages,
    _endpoints_from_page,
    _page_title_parts,
    _series_key,
    discover,
    probe_discovered,
)
from qadris_datasourcediscovery.store.database import CatalogDB

_ROOT_HTML = """
<html><body>
<a href="/markets/statistics-equities/investor-type/index.html">投資部門別</a>
<a href="/markets/statistics-equities/misc/index.html">その他</a>
</body></html>
"""

_IT = "/markets/statistics-equities/investor-type"

_INVESTOR_INDEX_HTML = f"""
<html><head>
<title>投資部門別売買状況 | 日本取引所グループ</title></head><body>
<a href="{_IT}/02.html">ETF</a>
<a href="{_IT}/00-archives-00.html">過去</a>
<a href="{_IT}/t13vrt000001iqby-att/stock_vol_1_260604.xls">x</a>
<a href="{_IT}/t13vrt000001iqby-att/stock_vol_1_260604.pdf">p</a>
<a href="{_IT}/t13vrt000001i8z5-att/stock_vol_1_260603.xls">x</a>
</body></html>
"""

_INVESTOR_02_HTML = f"""
<html><head>
<title>ETF | 投資部門別売買状況 | 日本取引所グループ</title></head><body>
<a href="{_IT}/t13vrt000000krlu-att/etf_m2601.xls">x</a>
<a href="{_IT}/t13vrt000000oxnw-att/etf_m2602.xls">x</a>
</body></html>
"""

_MISC_INDEX_HTML = """
<html><head>
<title>その他統計資料 | 日本取引所グループ</title></head><body>
<a href="/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls">一覧</a>
</body></html>
"""


def _settings(tmp_path: Path) -> DiscoverySettings:
    return DiscoverySettings(project_root=tmp_path, web_delay=0)


class TestHelpers:
    def test_series_key_date_stamp(self) -> None:
        assert _series_key("stock_vol_1_260604.xls") == "stock_vol_1_*.xls"
        assert _series_key("etf_m2601.xls") == "etf_m*.xls"
        assert _series_key("2601.pdf") == "*.pdf"

    def test_series_key_no_stamp(self) -> None:
        assert _series_key("data_j.xls") == "data_j.xls"
        assert _series_key("Premium_Charges.xlsx") == "Premium_Charges.xlsx"

    def test_page_title_parts(self) -> None:
        assert _page_title_parts(
            "<title>品貸料 | 信用取引残高等 | 日本取引所グループ</title>"
        ) == ("品貸料", "信用取引残高等")
        assert _page_title_parts(
            "<title>東証上場銘柄一覧 | 日本取引所グループ</title>"
        ) == ("東証上場銘柄一覧", "")

    def test_collect_subpages_excludes_archives(self) -> None:
        pages = _collect_subpages(_INVESTOR_INDEX_HTML, "investor-type")
        assert "/markets/statistics-equities/investor-type/02.html" in pages
        assert not any("archives" in p for p in pages)


class TestEndpointsFromPage:
    def test_series_grouping(self) -> None:
        eps = _endpoints_from_page(
            "/markets/statistics-equities/investor-type/index.html",
            _INVESTOR_INDEX_HTML,
            base="https://www.jpx.co.jp",
            section="investor-type",
        )
        by_key = {ep.path.split("#")[-1]: ep for ep in eps}
        assert set(by_key) == {"stock_vol_1_*.xls", "stock_vol_1_*.pdf"}

        xls = by_key["stock_vol_1_*.xls"]
        assert xls.response_format == "excel"
        assert xls.supports_history  # 2 檔
        assert xls.category == "投資部門別売買状況"
        # 代表檔＝最新（排序最大）
        assert xls.request_example["url"].endswith("stock_vol_1_260604.xls")
        assert "不可寫死" in xls.notes

        pdf = by_key["stock_vol_1_*.pdf"]
        assert pdf.response_format == "pdf"
        assert "PDF-only" in pdf.notes

    def test_static_file_no_history(self) -> None:
        eps = _endpoints_from_page(
            "/markets/statistics-equities/misc/index.html",
            _MISC_INDEX_HTML,
            base="https://www.jpx.co.jp",
            section="misc",
        )
        assert len(eps) == 1
        assert eps[0].path.endswith("#data_j.xls")
        assert not eps[0].supports_history


def _fake_site_session() -> MagicMock:
    def fake_get(url: str, **kw: object) -> MagicMock:
        resp = MagicMock()
        resp.status_code = 200
        if url.endswith("/markets/statistics-equities/index.html"):
            resp.text = _ROOT_HTML
        elif url.endswith("/investor-type/index.html"):
            resp.text = _INVESTOR_INDEX_HTML
        elif url.endswith("/investor-type/02.html"):
            resp.text = _INVESTOR_02_HTML
        elif url.endswith("/misc/index.html"):
            resp.text = _MISC_INDEX_HTML
        elif url.endswith(".xls"):
            buf = BytesIO()
            df = pd.DataFrame(
                [["銘柄コード", "銘柄名", "売買高"], ["1301", "極洋", 100]]
            )
            df.to_excel(buf, index=False, header=False)
            content = bytearray(buf.getvalue())
            resp.content = bytes(content)
        elif url.endswith(".pdf"):
            resp.content = b"%PDF-1.4"
        else:
            resp.status_code = 404
            resp.text = ""
        return resp

    session = MagicMock()
    session.get.side_effect = fake_get
    return session


class TestDiscover:
    def test_crawl_tree(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path)
        with (
            patch(
                "qadris_datasourcediscovery.discover_jpx._create_session",
                return_value=_fake_site_session(),
            ),
            patch("qadris_datasourcediscovery.discover_jpx.delay"),
        ):
            eps = discover(settings=settings)

        paths = {ep.path for ep in eps}
        assert (
            "/markets/statistics-equities/investor-type/index.html"
            "#stock_vol_1_*.xls" in paths
        )
        assert (
            "/markets/statistics-equities/investor-type/02.html#etf_m*.xls"
            in paths
        )
        assert "/markets/statistics-equities/misc/index.html#data_j.xls" in paths
        assert all(ep.state == "discovered" for ep in eps)
        assert all(ep.source == "jpx" for ep in eps)


class TestProbe:
    def test_probe_excel_and_pdf(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path)
        with (
            patch(
                "qadris_datasourcediscovery.discover_jpx._create_session",
                return_value=_fake_site_session(),
            ),
            patch("qadris_datasourcediscovery.discover_jpx.delay"),
        ):
            eps = discover(settings=settings)
            with CatalogDB(settings.db_path) as db:
                db.upsert_endpoints(eps)
            results = probe_discovered(settings=settings, limit=100)

        assert all(r.state == "probed" for r in results)

        xls = next(r for r in results if r.path.endswith("stock_vol_1_*.xls"))
        assert xls.status == "ok"
        assert "銘柄コード" in xls.sample_fields
        assert xls.record_count == 1

        pdf = next(r for r in results if r.path.endswith("stock_vol_1_*.pdf"))
        assert pdf.status == "ok"  # PDF 可達 → ok，不算 error
        assert pdf.response_format == "pdf"

    def test_probe_403_notes_cloud_block(self, tmp_path: Path) -> None:
        settings = _settings(tmp_path)
        with (
            patch(
                "qadris_datasourcediscovery.discover_jpx._create_session",
                return_value=_fake_site_session(),
            ),
            patch("qadris_datasourcediscovery.discover_jpx.delay"),
        ):
            eps = discover(settings=settings)
        with CatalogDB(settings.db_path) as db:
            db.upsert_endpoints(eps)

        resp403 = MagicMock()
        resp403.status_code = 403
        resp403.content = b""
        session = MagicMock()
        session.get.return_value = resp403

        with (
            patch(
                "qadris_datasourcediscovery.discover_jpx._create_session",
                return_value=session,
            ),
            patch("qadris_datasourcediscovery.discover_jpx.delay"),
        ):
            results = probe_discovered(settings=settings, limit=100)

        assert all(r.status == "error" for r in results)
        assert all("403" in r.notes for r in results)
