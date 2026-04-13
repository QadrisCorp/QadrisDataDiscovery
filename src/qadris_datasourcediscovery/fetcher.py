"""HTTP fetch utilities and sample data storage."""

from __future__ import annotations

import json
import logging
import time
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import FetchError

logger = logging.getLogger(__name__)


def _create_session(*, settings: DiscoverySettings) -> requests.Session:
    """Create a new HTTP session with configured headers."""
    session = requests.Session()
    session.headers.update({"User-Agent": settings.user_agent})
    return session


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
