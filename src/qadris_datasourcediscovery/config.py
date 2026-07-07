"""Configuration for qadris-datasourcediscovery using pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings

from qadris_datasourcediscovery.exceptions import ConfigurationError
from qadris_datasourcediscovery.registry import SOURCE_REGISTRY


class DiscoverySettings(BaseSettings):
    """Data source discovery settings.

    All fields are read from environment variables with the ``RSR_`` prefix.
    """

    # Base URLs — Taiwan
    twse_openapi_base: str = "https://openapi.twse.com.tw/v1"
    twse_web_base: str = "https://www.twse.com.tw"
    tpex_openapi_base: str = "https://www.tpex.org.tw/openapi/v1"
    tpex_web_base: str = "https://www.tpex.org.tw"
    mops_base: str = "https://mops.twse.com.tw"
    tdcc_openapi_base: str = "https://openapi.tdcc.com.tw"

    # Base URLs — Japan
    jquants_base: str = "https://api.jquants.com/v2"
    edinet_base: str = "https://api.edinet-fsa.go.jp/api/v2"
    tdnet_base: str = "https://www.release.tdnet.info"
    jpx_base: str = "https://www.jpx.co.jp"

    # API keys（RSR_JQUANTS_API_KEY / RSR_EDINET_API_KEY）
    jquants_api_key: str = ""
    edinet_api_key: str = ""

    # Output paths — default to cwd, overridable via RSR_PROJECT_ROOT
    project_root: Path = Path.cwd()
    samples_dir: Path = Path("")
    catalog_dir: Path = Path("")
    db_path: Path = Path("")

    # Request settings
    request_timeout: int = 30
    openapi_delay: float = 1.0
    web_delay: float = 3.0
    max_sample_records: int = 5

    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )

    model_config = {"env_prefix": "RSR_"}

    def model_post_init(self, __context: object) -> None:
        """Derive paths from project_root after init."""
        if self.samples_dir == Path(""):
            self.samples_dir = self.project_root / "samples"
        if self.catalog_dir == Path(""):
            self.catalog_dir = self.project_root / "catalog"
        if self.db_path == Path(""):
            self.db_path = self.project_root / "catalog" / "catalog.db"

    def get_base_url(self, source: str, endpoint_type: str) -> str:
        """Return base URL for a given source and endpoint type."""
        spec = SOURCE_REGISTRY.get(source)
        if spec is None:
            return ""
        attr = spec.base_url_fields.get(endpoint_type, "")
        if not attr:
            return ""
        value: str = getattr(self, attr, "")
        return value

    def get_api_key(self, source: str) -> str:
        """Return the configured API key for a source ("" if none/not needed)."""
        spec = SOURCE_REGISTRY.get(source)
        if spec is None or spec.auth is None:
            return ""
        value: str = getattr(self, spec.auth.settings_field, "")
        return value

    def require_api_key(self, source: str) -> str:
        """Return the API key for a source, raising if missing.

        Raises:
            ConfigurationError: 該源需要金鑰但未設定（明確報錯，不靜默失敗）。
        """
        spec = SOURCE_REGISTRY.get(source)
        if spec is None or spec.auth is None:
            return ""
        key = self.get_api_key(source)
        if not key:
            env_name = f"RSR_{spec.auth.settings_field.upper()}"
            raise ConfigurationError(
                f"{spec.display_name} 需要 API 金鑰：請在 .env 設定 {env_name}"
            )
        return key

    def validate_settings(self) -> None:
        """Validate that required settings are configured.

        Raises:
            ConfigurationError: If required directories cannot be created.
        """
        if not self.project_root.exists():
            raise ConfigurationError(
                f"Project root does not exist: {self.project_root}"
            )
