"""HTTP fetch utilities and sample data storage."""

from __future__ import annotations

import json
import logging
import time
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import requests

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError
from qadris_datasourcediscovery.registry import SOURCE_REGISTRY

logger = logging.getLogger(__name__)


def _create_session(
    *, settings: DiscoverySettings, source: str | None = None
) -> requests.Session:
    """Create a new HTTP session with configured headers.

    若 ``source`` 有 header 式認證（如 J-Quants x-api-key）且金鑰已設定，
    自動注入認證 header。金鑰缺漏檢查由各 probe 呼叫
    ``settings.require_api_key()`` 明確處理，這裡不拋錯。
    """
    session = requests.Session()
    session.headers.update({"User-Agent": settings.user_agent})
    if source:
        spec = SOURCE_REGISTRY.get(source)
        if spec and spec.auth and spec.auth.kind == "header":
            key = settings.get_api_key(source)
            if key:
                session.headers[spec.auth.param_name] = key
    return session


def auth_query_params(
    source: str, *, settings: DiscoverySettings
) -> dict[str, str]:
    """Return query-param auth for a source（如 EDINET Subscription-Key）。

    無 query 式認證或金鑰未設定時回傳空 dict。
    """
    spec = SOURCE_REGISTRY.get(source)
    if spec and spec.auth and spec.auth.kind == "query":
        key = settings.get_api_key(source)
        if key:
            return {spec.auth.param_name: key}
    return {}


def fetch_json(
    url: str,
    *,
    session: requests.Session,
    settings: DiscoverySettings,
    params: dict[str, str] | None = None,
) -> tuple[Any, int]:
    """GET JSON and return (data, status_code).

    Raises:
        FetchError: When the request fails entirely.
    """
    try:
        resp = session.get(url, params=params, timeout=settings.request_timeout)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.exceptions.JSONDecodeError:
        logger.warning("Non-JSON response: %s", url)
        return None, resp.status_code
    except requests.RequestException as e:
        raise FetchError(f"Request failed {url}: {e}") from e


def fetch_csv(
    url: str,
    *,
    session: requests.Session,
    settings: DiscoverySettings,
    params: dict[str, str] | None = None,
) -> tuple[pd.DataFrame | None, int]:
    """GET CSV and return (DataFrame, status_code).

    Raises:
        FetchError: When the request or CSV parsing fails.
    """
    try:
        resp = session.get(url, params=params, timeout=settings.request_timeout)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        df = pd.read_csv(StringIO(resp.text))
        return df, resp.status_code
    except requests.RequestException as e:
        raise FetchError(f"CSV fetch failed {url}: {e}") from e
    except Exception as e:
        raise FetchError(f"CSV parse failed {url}: {e}") from e


def fetch_post_html(
    url: str,
    form_data: dict[str, str],
    *,
    session: requests.Session,
    settings: DiscoverySettings,
) -> tuple[list[pd.DataFrame] | None, int]:
    """POST form data and parse HTML tables with pandas.

    Raises:
        FetchError: When the request or HTML parsing fails.
    """
    try:
        resp = session.post(url, data=form_data, timeout=settings.request_timeout)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        tables = pd.read_html(StringIO(resp.text))
        return tables, resp.status_code
    except requests.RequestException as e:
        raise FetchError(f"POST HTML fetch failed {url}: {e}") from e
    except Exception as e:
        raise FetchError(f"POST HTML parse failed {url}: {e}") from e


def fetch_post_json(
    url: str,
    form_data: dict[str, str],
    *,
    session: requests.Session,
    settings: DiscoverySettings,
) -> tuple[Any, int]:
    """POST form data and return JSON response.

    Raises:
        FetchError: When the request fails entirely.
    """
    try:
        resp = session.post(url, data=form_data, timeout=settings.request_timeout)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.exceptions.JSONDecodeError:
        logger.warning("Non-JSON response: %s", url)
        return None, resp.status_code
    except requests.RequestException as e:
        raise FetchError(f"POST JSON request failed {url}: {e}") from e


def _find_header_row(df: pd.DataFrame, scan_rows: int = 15) -> int:
    """在前 N 列中找最像 header 的一列（非空儲存格最多者，取最先）。

    JPX 統計 Excel 常有標題列/註記列在真正欄位列之前。
    """
    best_idx = 0
    best_count = -1
    for i in range(min(scan_rows, len(df))):
        count = int(df.iloc[i].notna().sum())
        if count > best_count:
            best_count = count
            best_idx = i
    return best_idx


def fetch_excel_fields(
    url: str,
    *,
    session: requests.Session,
    settings: DiscoverySettings,
) -> tuple[list[str], int, int]:
    """下載 Excel（.xls/.xlsx）並擷取欄位名與資料列數。

    Returns:
        (fields, record_count, status_code)

    Raises:
        FetchError: 下載或解析失敗。
    """
    try:
        resp = session.get(url, timeout=settings.request_timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise FetchError(f"Excel fetch failed {url}: {e}") from e

    content = resp.content
    # 內容 sniff：xlsx 是 zip（PK），舊式 .xls 是 OLE2（D0 CF）
    engine: Literal["openpyxl", "xlrd"]
    if content[:2] == b"PK":
        engine = "openpyxl"
    elif content[:2] == b"\xd0\xcf":
        engine = "xlrd"
    else:
        raise FetchError(f"Not an Excel file (magic={content[:4]!r}): {url}")

    try:
        df = pd.read_excel(BytesIO(content), header=None, engine=engine)
    except Exception as e:
        raise FetchError(f"Excel parse failed {url}: {e}") from e

    if df.empty:
        return [], 0, resp.status_code

    header_idx = _find_header_row(df)
    fields = [
        str(v).strip().replace("\n", " ")
        for v in df.iloc[header_idx].tolist()
        if pd.notna(v) and str(v).strip()
    ]
    record_count = max(0, len(df) - header_idx - 1)
    return fields, record_count, resp.status_code


def save_sample(
    data: Any,
    path: Path,
    *,
    max_records: int = 5,
) -> None:
    """Save first N records as a sample file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, pd.DataFrame):
        data.head(max_records).to_json(
            path, orient="records", force_ascii=False, indent=2
        )
    elif isinstance(data, list):
        sample = data[:max_records]
        path.write_text(
            json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    elif isinstance(data, dict):
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        path.write_text(str(data), encoding="utf-8")
    logger.info("Sample saved: %s", path)


def get_selenium_driver(*, settings: DiscoverySettings) -> Any:
    """Create a headless Chrome driver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={settings.user_agent}")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def fetch_with_selenium(
    url: str,
    *,
    settings: DiscoverySettings,
    driver: Any = None,
    wait_seconds: int = 5,
) -> str:
    """Fetch page HTML using Selenium as a fallback for JS-heavy pages."""
    if driver is None:
        driver = get_selenium_driver(settings=settings)
    driver.get(url)
    time.sleep(wait_seconds)
    page_source: str = driver.page_source
    return page_source


def delay(seconds: float) -> None:
    """Rate-limiting delay between requests."""
    time.sleep(seconds)
