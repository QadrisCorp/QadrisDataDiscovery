"""Source registry — 所有資料源的單一對照表（SSOT）。

新增資料源時只需在 ``SOURCE_REGISTRY`` 加一筆（＋config.py 的 base URL 欄位），
CLI probe dispatch、market 篩選、GH Pages 產出、enrich 規則皆由此驅動。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Market = Literal["tw", "jp"]

# LLM enrich prompt 用的市場稱謂（"You are a {market} financial data expert"）
MARKET_LABELS: dict[str, str] = {"tw": "Taiwan", "jp": "Japanese"}


@dataclass(frozen=True)
class AuthSpec:
    """來源認證方式：金鑰注入位置與對應的 settings 欄位。"""

    kind: Literal["header", "query"]
    param_name: str
    settings_field: str  # DiscoverySettings 上存放金鑰的欄位名


@dataclass(frozen=True)
class SourceSpec:
    """單一資料源的靜態描述。"""

    market: Market
    display_name: str
    name_en: str
    name_local: str
    # endpoint_type -> DiscoverySettings 的 base URL 欄位名（fetch 用、env 可覆寫）
    base_url_fields: dict[str, str] = field(default_factory=dict)
    # endpoint_type -> 對外發佈用 base URL（GH Pages meta；可與 fetch base 不同）
    catalog_base_urls: dict[str, str] = field(default_factory=dict)
    # 提供 probe_discovered() 的模組（None＝discovery 內建 probe）
    probe_module: str | None = None
    auth: AuthSpec | None = None


SOURCE_REGISTRY: dict[str, SourceSpec] = {
    "twse": SourceSpec(
        market="tw",
        display_name="TWSE",
        name_en="Taiwan Stock Exchange (TWSE)",
        name_local="臺灣證券交易所",
        base_url_fields={"openapi": "twse_openapi_base", "web": "twse_web_base"},
        catalog_base_urls={
            "openapi": "https://openapi.twse.com.tw/v1",
            "web": "https://www.twse.com.tw",
        },
        probe_module="qadris_datasourcediscovery.discover_tse_web",
    ),
    "tpex": SourceSpec(
        market="tw",
        display_name="TPEx",
        name_en="Taipei Exchange (TPEx)",
        name_local="證券櫃檯買賣中心",
        base_url_fields={"openapi": "tpex_openapi_base", "web": "tpex_web_base"},
        catalog_base_urls={
            "openapi": "https://www.tpex.org.tw/openapi/v1",
            "web": "https://www.tpex.org.tw",
        },
        probe_module="qadris_datasourcediscovery.discover_otc_web",
    ),
    "mops": SourceSpec(
        market="tw",
        display_name="MOPS",
        name_en="Market Observation Post System (MOPS)",
        name_local="公開資訊觀測站",
        base_url_fields={"web": "mops_base", "xbrl": "mops_base"},
        catalog_base_urls={
            "web": "https://mopsov.twse.com.tw",
            "xbrl": "https://mops.twse.com.tw",
        },
        probe_module="qadris_datasourcediscovery.discover_mops",
    ),
    "tdcc": SourceSpec(
        market="tw",
        display_name="TDCC",
        name_en="Taiwan Depository & Clearing Corporation (TDCC)",
        name_local="臺灣集中保管結算所",
        base_url_fields={"openapi": "tdcc_openapi_base"},
        catalog_base_urls={"openapi": "https://openapi.tdcc.com.tw"},
    ),
    "jquants": SourceSpec(
        market="jp",
        display_name="J-Quants",
        name_en="J-Quants API (JPX official)",
        name_local="J-Quants API（JPX公式）",
        base_url_fields={"openapi": "jquants_base"},
        catalog_base_urls={"openapi": "https://api.jquants.com/v2"},
        probe_module="qadris_datasourcediscovery.discover_jquants",
        auth=AuthSpec(
            kind="header", param_name="x-api-key", settings_field="jquants_api_key"
        ),
    ),
    "edinet": SourceSpec(
        market="jp",
        display_name="EDINET",
        name_en="EDINET API v2 (Financial Services Agency)",
        name_local="EDINET（金融庁）",
        base_url_fields={"openapi": "edinet_base"},
        catalog_base_urls={"openapi": "https://api.edinet-fsa.go.jp/api/v2"},
        probe_module="qadris_datasourcediscovery.discover_edinet",
        auth=AuthSpec(
            kind="query",
            param_name="Subscription-Key",
            settings_field="edinet_api_key",
        ),
    ),
    "tdnet": SourceSpec(
        market="jp",
        display_name="TDnet",
        name_en="TDnet Timely Disclosure (Tokyo Stock Exchange)",
        name_local="TDnet（適時開示情報閲覧サービス）",
        base_url_fields={"web": "tdnet_base"},
        catalog_base_urls={"web": "https://www.release.tdnet.info"},
        probe_module="qadris_datasourcediscovery.discover_tdnet",
    ),
    "jpx": SourceSpec(
        market="jp",
        display_name="JPX",
        name_en="Japan Exchange Group statistics (JPX)",
        name_local="日本取引所グループ（統計情報）",
        base_url_fields={"web": "jpx_base"},
        catalog_base_urls={"web": "https://www.jpx.co.jp"},
        probe_module="qadris_datasourcediscovery.discover_jpx",
    ),
}


def get_source_spec(source: str) -> SourceSpec | None:
    """Return the SourceSpec for a source key, or None if unknown."""
    return SOURCE_REGISTRY.get(source)


def get_market(source: str) -> str:
    """Return the market code ("tw"/"jp") for a source; empty if unknown."""
    spec = SOURCE_REGISTRY.get(source)
    return spec.market if spec else ""


def sources_for_market(market: str | None = None) -> list[str]:
    """Return source keys, optionally filtered by market, in registry order."""
    if market is None:
        return list(SOURCE_REGISTRY)
    return [s for s, spec in SOURCE_REGISTRY.items() if spec.market == market]
