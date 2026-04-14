"""Configuration for qadris-datasourcediscovery using pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings

from qadris_datasourcediscovery.exceptions import ConfigurationError


class DiscoverySettings(BaseSettings):
    """Data source discovery settings.

    All fields are read from environment variables with the ``RSR_`` prefix.
    """

    # Base URLs
    twse_openapi_base: str = "https://openapi.twse.com.tw/v1"
    twse_web_base: str = "https://www.twse.com.tw"
    tpex_openapi_base: str = "https://www.tpex.org.tw/openapi/v1"
    tpex_web_base: str = "https://www.tpex.org.tw"
    mops_base: str = "https://mops.twse.com.tw"

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
        mapping: dict[tuple[str, str], str] = {
            ("twse", "openapi"): self.twse_openapi_base,
            ("twse", "web"): self.twse_web_base,
            ("tpex", "openapi"): self.tpex_openapi_base,
            ("tpex", "web"): self.tpex_web_base,
            ("mops", "web"): self.mops_base,
            ("mops", "xbrl"): self.mops_base,
        }
        return mapping.get((source, endpoint_type), "")

    def validate_settings(self) -> None:
        """Validate that required settings are configured.

        Raises:
            ConfigurationError: If required directories cannot be created.
        """
        if not self.project_root.exists():
            raise ConfigurationError(
                f"Project root does not exist: {self.project_root}"
            )
