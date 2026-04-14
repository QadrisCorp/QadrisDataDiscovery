"""Tests for exception hierarchy."""

from __future__ import annotations

import pytest

from qadris_datasourcediscovery.exceptions import (
    ConfigurationError,
    DataSourceDiscoveryError,
    FetchError,
    LLMError,
    ParseError,
    StoreError,
)


class TestExceptionHierarchy:
    def test_base_exception(self) -> None:
        with pytest.raises(DataSourceDiscoveryError):
            raise DataSourceDiscoveryError("test")

    @pytest.mark.parametrize(
        "exc_class",
        [ConfigurationError, FetchError, ParseError, LLMError, StoreError],
    )
    def test_subclasses_inherit_from_base(
        self, exc_class: type[DataSourceDiscoveryError]
    ) -> None:
        assert issubclass(exc_class, DataSourceDiscoveryError)
        with pytest.raises(DataSourceDiscoveryError):
            raise exc_class("test message")

    @pytest.mark.parametrize(
        "exc_class",
        [ConfigurationError, FetchError, ParseError, LLMError, StoreError],
    )
    def test_can_catch_specifically(
        self, exc_class: type[DataSourceDiscoveryError]
    ) -> None:
        with pytest.raises(exc_class, match="specific"):
            raise exc_class("specific error message")

    def test_message_preserved(self) -> None:
        try:
            raise FetchError("connection refused")
        except FetchError as e:
            assert str(e) == "connection refused"
