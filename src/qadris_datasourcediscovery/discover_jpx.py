"""JPX 統計頁 discovery — 爬 markets/statistics-equities/ 頁面樹＋Excel probe。

站點特性（2026-07-07 實測核實）：
- 統計頁為靜態 HTML；檔案（.xls/.xlsx/.pdf/.csv）URL 含 **CMS 隨機路徑**
  （如 ``t13vrt000001iqby-att``）——**必須先爬列表頁解析 href，不可寫死檔案 URL**。
- 同一資料表以「檔案序列」發佈（如 ``stock_vol_1_260604.xls`` 週更）；
  endpoint 粒度＝「頁面×檔案序列」（序列鍵＝檔名中 ≥4 位數字換成 ``*``）。
- 部分表僅提供 PDF（如實標 ``response_format=pdf``，不解析內容）。
- **JPX 對雲端抓取 client 回 403**（與 UA 無關）；本機 requests 可抓。
- 禮貌抓取：沿用 ``web_delay``（預設 3s）。
"""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urljoin

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError
from qadris_datasourcediscovery.fetcher import (
    _create_session,
    delay,
    fetch_excel_fields,
)

logger = logging.getLogger(__name__)

STATS_ROOT = "/markets/statistics-equities/"

# 每個 section 最多爬的子頁數（防站點改版時失控）
MAX_SUBPAGES_PER_SECTION = 20

_FILE_EXT_RE = re.compile(r'href="([^"]+\.(?:xlsx|xls|csv|pdf))"', re.IGNORECASE)
_SECTION_RE = re.compile(r"/markets/statistics-equities/([a-z0-9-]+)/")

_FORMAT_BY_EXT = {"xlsx": "excel", "xls": "excel", "csv": "csv", "pdf": "pdf"}

_403_NOTE = "JPX 對雲端抓取 client 回 403（與 UA 無關），需本機執行"


def _series_key(filename: str) -> str:
    """檔名 → 序列鍵：≥4 位連續數字（日期戳）換成 ``*``。

    例：``stock_vol_1_260604.xls`` → ``stock_vol_1_*.xls``；
    ``data_j.xls``（無日期戳）→ 原樣。
    """
    return re.sub(r"\d{4,}", "*", filename)


def _page_title_parts(html: str) -> tuple[str, str]:
    """回傳 (頁名, 分類)——取自 <title>「頁名 | 分類 | 日本取引所グループ」。"""
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return "", ""
    parts = [p.strip() for p in m.group(1).split("|")]
    parts = [p for p in parts if p and "日本取引所" not in p]
    if not parts:
        return "", ""
    page_name = parts[0]
    category = parts[1] if len(parts) > 1 else ""
    return page_name, category


def _collect_subpages(index_html: str, section: str) -> list[str]:
    """從 section index 頁收集同 section 的子頁路徑（排除 archives）。"""
    pattern = re.compile(
        rf'href="(/markets/statistics-equities/{re.escape(section)}/'
        rf'[0-9a-z_-]+\.html)"'
    )
    pages: list[str] = []
    for m in pattern.finditer(index_html):
        path = m.group(1)
        if "archives" in path or path.endswith("/index.html"):
            continue
        if path not in pages:
            pages.append(path)
    return pages[:MAX_SUBPAGES_PER_SECTION]


def _endpoints_from_page(
    page_path: str,
    html: str,
    *,
    base: str,
    section: str,
) -> list[EndpointInfo]:
    """把一個統計頁解析成「頁面×檔案序列」endpoints。"""
    page_name, category = _page_title_parts(html)
    if not category:
        # index 頁 title 只有「頁名 | 日本取引所グループ」→ 頁名即分類
        category = page_name or section

    series: dict[str, list[str]] = {}
    for m in _FILE_EXT_RE.finditer(html):
        href = m.group(1)
        filename = href.rsplit("/", 1)[-1]
        key = _series_key(filename)
        series.setdefault(key, []).append(href)

    endpoints: list[EndpointInfo] = []
    for key, hrefs in series.items():
        ext = key.rsplit(".", 1)[-1].lower()
        representative = urljoin(f"{base}{page_path}", sorted(hrefs)[-1])
        has_history = len(hrefs) > 1 or "*" in key

        notes_parts = [
            "檔案 URL 含 CMS 隨機路徑（-att），必須重爬本頁解析 href，不可寫死",
            f"本頁 {len(hrefs)} 檔",
            _403_NOTE,
        ]
        if ext == "pdf":
            notes_parts.append("PDF-only 資料（不解析內容）")

        endpoints.append(
            EndpointInfo(
                source="jpx",
                endpoint_type="web",
                path=f"{page_path}#{key}",
                description=f"{page_name} — {key}" if page_name else key,
                category=category,
                method="GET",
                supports_history=has_history,
                response_format=_FORMAT_BY_EXT.get(ext, ""),
                request_example={"url": representative, "method": "GET"},
                history_method=(
                    "爬本頁（及各年 archives 頁）解析檔案連結"
                    if has_history
                    else ""
                ),
                notes=" | ".join(notes_parts),
                state="discovered",
            )
        )
    return endpoints


def discover(*, settings: DiscoverySettings | None = None) -> list[EndpointInfo]:
    """爬 JPX 統計頁樹，回傳「頁面×檔案序列」endpoints。"""
    if settings is None:
        settings = DiscoverySettings()

    base = settings.get_base_url("jpx", "web")
    session = _create_session(settings=settings, source="jpx")

    def _get(path: str) -> str | None:
        try:
            resp = session.get(f"{base}{path}", timeout=settings.request_timeout)
            if resp.status_code == 403:
                raise FetchError(f"HTTP 403 for {path}（{_403_NOTE}）")
            if resp.status_code != 200:
                logger.warning("JPX %s -> HTTP %d", path, resp.status_code)
                return None
            resp.encoding = "utf-8"
            return resp.text
        except FetchError:
            raise
        except Exception as e:  # noqa: BLE001
            logger.warning("JPX fetch failed %s: %s", path, e)
            return None
        finally:
            delay(settings.web_delay)

    root_path = f"{STATS_ROOT}index.html"
    root_html = _get(root_path)
    if root_html is None:
        logger.error("JPX statistics root unreachable")
        return []

    sections: list[str] = []
    for m in _SECTION_RE.finditer(root_html):
        s = m.group(1)
        if s not in sections:
            sections.append(s)
    logger.info("JPX sections: %s", sections)

    endpoints: list[EndpointInfo] = []
    seen_pages: set[str] = set()

    for section in sections:
        index_path = f"{STATS_ROOT}{section}/index.html"
        index_html = _get(index_path)
        if index_html is None:
            continue

        page_paths = [index_path] + _collect_subpages(index_html, section)
        for page_path in page_paths:
            if page_path in seen_pages:
                continue
            seen_pages.add(page_path)

            html = index_html if page_path == index_path else _get(page_path)
            if html is None:
                continue
            eps = _endpoints_from_page(
                page_path, html, base=base, section=section
            )
            if eps:
                logger.info("  %s: %d series", page_path, len(eps))
            endpoints.extend(eps)

    logger.info(
        "JPX: %d endpoints from %d pages", len(endpoints), len(seen_pages)
    )
    return endpoints


def probe_discovered(
    *,
    settings: DiscoverySettings | None = None,
    limit: int = 10,
) -> list[EndpointInfo]:
    """Probe discovered JPX endpoints — Excel 下載讀 header；PDF 驗證可達。"""
    if settings is None:
        settings = DiscoverySettings()

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        discovered = db.get_endpoints(source="jpx", state="discovered")

    if not discovered:
        logger.info("No discovered JPX endpoints to probe")
        return []

    to_probe = discovered[:limit]
    session = _create_session(settings=settings, source="jpx")
    logger.info("=== Probing %d/%d JPX endpoints ===", len(to_probe), len(discovered))

    results: list[EndpointInfo] = []
    for ep in to_probe:
        updates: dict[str, Any] = {"state": "probed"}
        url = str(ep.request_example.get("url", ""))

        if not url:
            updates["status"] = "error"
            updates["notes"] = (ep.notes + " | probe: 無代表檔 URL").strip(" | ")
            results.append(ep.model_copy(update=updates))
            continue

        logger.info("Probing: %s (%s)", ep.path, ep.response_format)

        if ep.response_format == "excel":
            try:
                fields, count, _status = fetch_excel_fields(
                    url, session=session, settings=settings
                )
                updates["status"] = "ok" if fields else "empty"
                updates["sample_fields"] = fields[:15]
                updates["record_count"] = count
            except FetchError as e:
                if "403" in str(e):
                    updates["status"] = "error"
                    updates["notes"] = (
                        ep.notes + f" | probe: HTTP 403（{_403_NOTE}）"
                    ).strip(" | ")
                else:
                    updates["status"] = "error"
                    updates["notes"] = (ep.notes + f" | probe: {e}").strip(" | ")
        else:
            # pdf / csv / 其他：驗證可達性；PDF 不解析內容
            try:
                resp = session.get(url, timeout=settings.request_timeout)
                if resp.status_code == 200:
                    updates["status"] = "ok"
                    updates["record_count"] = 1
                elif resp.status_code == 403:
                    updates["status"] = "error"
                    updates["notes"] = (
                        ep.notes + f" | probe: HTTP 403（{_403_NOTE}）"
                    ).strip(" | ")
                else:
                    updates["status"] = "error"
                    updates["notes"] = (
                        ep.notes + f" | probe: HTTP {resp.status_code}"
                    ).strip(" | ")
            except Exception as e:  # noqa: BLE001
                updates["status"] = "error"
                updates["notes"] = (ep.notes + f" | probe: {e}").strip(" | ")

        results.append(ep.model_copy(update=updates))
        delay(settings.web_delay)

    ok = sum(1 for r in results if r.status == "ok")
    logger.info("JPX probe done: %d ok / %d total", ok, len(results))
    return results


def main() -> None:
    """Run JPX discovery and save to database."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    endpoints = discover(settings=settings)

    from qadris_datasourcediscovery.store import CatalogDB

    with CatalogDB(settings.db_path) as db:
        db.upsert_endpoints(endpoints)

    logger.info("JPX: %d endpoints saved to DB", len(endpoints))


if __name__ == "__main__":
    main()
