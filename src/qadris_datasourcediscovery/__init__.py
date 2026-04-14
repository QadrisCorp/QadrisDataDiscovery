"""qadris-datasourcediscovery: Taiwan official financial data source discovery tool."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("qadris-datasourcediscovery")
except PackageNotFoundError:
    __version__ = "0.1.0"

from qadris_datasourcediscovery.catalog import (
    EndpointInfo,
    EndpointType,
    Source,
    State,
    Status,
)
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.enrich import enrich_all
from qadris_datasourcediscovery.exceptions import (
    ConfigurationError,
    DataSourceDiscoveryError,
    FetchError,
    LLMError,
    ParseError,
    StoreError,
)
from qadris_datasourcediscovery.store import CatalogDB

__all__ = [
    "CatalogDB",
    "ConfigurationError",
    "DataSourceDiscoveryError",
    "DiscoverySettings",
    "EndpointInfo",
    "EndpointType",
    "FetchError",
    "LLMError",
    "ParseError",
    "Source",
    "State",
    "Status",
    "StoreError",
    "enrich_all",
]
