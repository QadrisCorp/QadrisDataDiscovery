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

    # Output paths
    project_root: Path = Path(__file__).resolve().parent.parent.parent
    samples_dir: Path = project_root / "samples"
    catalog_dir: Path = project_root / "catalog"
    db_path: Path = project_root / "catalog" / "catalog.db"

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

    def validate_settings(self) -> None:
        """Validate that required settings are configured.

        Raises:
            ConfigurationError: If required directories cannot be created.
        """
        if not self.project_root.exists():
            raise ConfigurationError(
                f"Project root does not exist: {self.project_root}"
            )
