"""Shared fixtures for QadrisDataDiscovery tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.store.database import CatalogDB


@pytest.fixture()
def tmp_db(tmp_path: Path) -> CatalogDB:
    """Create a temporary CatalogDB for testing."""
    db = CatalogDB(tmp_path / "test.db")
    yield db  # type: ignore[misc]
    db.close()


@pytest.fixture()
def sample_ep() -> EndpointInfo:
    """A minimal EndpointInfo for reuse."""
    return EndpointInfo(
        source="twse",
        endpoint_type="openapi",
        path="/opendata/test",
    )


@pytest.fixture()
def probed_ep() -> EndpointInfo:
    """An EndpointInfo in probed state with sample data."""
    return EndpointInfo(
        source="twse",
        endpoint_type="web",
        path="/zh/trading/test",
        description="Test trading data",
        category="trading",
        method="GET",
        supports_history=True,
        date_params=["date"],
        status="ok",
        record_count=100,
        sample_fields=["日期", "證券代號", "成交股數", "收盤價"],
        state="probed",
    )


@pytest.fixture()
def mops_ep() -> EndpointInfo:
    """A MOPS EndpointInfo for enrichment tests."""
    return EndpointInfo(
        source="mops",
        endpoint_type="web",
        path="/mops/web/t05st09_2",
        description="Monthly revenue",
        category="revenue",
        method="POST",
        supports_history=True,
        date_params=["year", "month"],
        status="ok",
        record_count=50,
        sample_fields=["公司代號", "公司名稱", "當月營收", "去年當月營收"],
        state="probed",
    )
