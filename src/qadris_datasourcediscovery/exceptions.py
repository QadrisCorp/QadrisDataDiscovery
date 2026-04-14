"""Exceptions for qadris-datasourcediscovery."""


class DataSourceDiscoveryError(Exception):
    """Base exception for all qadris-datasourcediscovery errors."""


class ConfigurationError(DataSourceDiscoveryError):
    """Raised when required configuration is missing or invalid."""


class FetchError(DataSourceDiscoveryError):
    """Raised when an HTTP request fails."""


class ParseError(DataSourceDiscoveryError):
    """Raised when response parsing fails."""


class LLMError(DataSourceDiscoveryError):
    """Raised when LLM CLI call fails."""


class StoreError(DataSourceDiscoveryError):
    """Raised when database operations fail."""
