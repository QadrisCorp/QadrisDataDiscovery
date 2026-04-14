"""Tests for DiscoverySettings."""

from __future__ import annotations

from pathlib import Path

import pytest

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.exceptions import ConfigurationError


class TestDiscoverySettingsDefaults:
    def test_default_values(self) -> None:
        s = DiscoverySettings()
        assert s.request_timeout == 30
        assert s.openapi_delay == 1.0
        assert s.web_delay == 3.0
        assert s.max_sample_records == 5

    def test_default_urls(self) -> None:
        s = DiscoverySettings()
        assert "openapi.twse.com.tw" in s.twse_openapi_base
        assert "twse.com.tw" in s.twse_web_base
        assert "tpex.org.tw" in s.tpex_openapi_base
        assert "tpex.org.tw" in s.tpex_web_base
        assert "mops.twse.com.tw" in s.mops_base


class TestModelPostInit:
    def test_paths_derived_from_project_root(self, tmp_path: Path) -> None:
        s = DiscoverySettings(project_root=tmp_path)
        assert s.samples_dir == tmp_path / "samples"
        assert s.catalog_dir == tmp_path / "catalog"
        assert s.db_path == tmp_path / "catalog" / "catalog.db"

    def test_explicit_paths_not_overridden(self, tmp_path: Path) -> None:
        custom = tmp_path / "custom_samples"
        s = DiscoverySettings(project_root=tmp_path, samples_dir=custom)
        assert s.samples_dir == custom
        # Others still derived
        assert s.catalog_dir == tmp_path / "catalog"


class TestGetBaseUrl:
    def test_twse_openapi(self) -> None:
        s = DiscoverySettings()
        url = s.get_base_url("twse", "openapi")
        assert url == s.twse_openapi_base

    def test_twse_web(self) -> None:
        s = DiscoverySettings()
        url = s.get_base_url("twse", "web")
        assert url == s.twse_web_base

    def test_tpex_openapi(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("tpex", "openapi") == s.tpex_openapi_base

    def test_mops_web(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("mops", "web") == s.mops_base

    def test_mops_xbrl(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("mops", "xbrl") == s.mops_base

    def test_unknown_returns_empty(self) -> None:
        s = DiscoverySettings()
        assert s.get_base_url("unknown", "api") == ""


class TestValidateSettings:
    def test_valid_project_root(self, tmp_path: Path) -> None:
        s = DiscoverySettings(project_root=tmp_path)
        s.validate_settings()  # Should not raise

    def test_nonexistent_project_root(self, tmp_path: Path) -> None:
        s = DiscoverySettings(project_root=tmp_path / "nonexistent")
        with pytest.raises(ConfigurationError, match="does not exist"):
            s.validate_settings()


class TestEnvPrefix:
    def test_env_prefix(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("RSR_REQUEST_TIMEOUT", "60")
        s = DiscoverySettings()
        assert s.request_timeout == 60
