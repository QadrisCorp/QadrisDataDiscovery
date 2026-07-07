"""Generate GitHub Pages static files from the endpoint catalog database.

Produces:
  docs/catalog.json  — structured endpoint catalog for AI agents
  docs/openapi.yaml  — OpenAPI 3.1 spec describing the catalog API
  docs/llms.txt      — AI agent discovery protocol
  docs/index.html    — human-browsable search UI
"""

from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.registry import SOURCE_REGISTRY, get_market

from qadris_datasourcediscovery.store import CatalogDB

logger = logging.getLogger(__name__)

GITHUB_PAGES_BASE = "https://qadriscorp.github.io/QadrisDataDiscovery"

# source metadata 由 registry 生成（name_zh 對日本源放當地語言名稱）
SOURCE_META: dict[str, dict[str, Any]] = {
    key: {
        "name": spec.name_en,
        "name_zh": spec.name_local,
        "market": spec.market,
        "base_urls": dict(spec.catalog_base_urls),
    }
    for key, spec in SOURCE_REGISTRY.items()
}


def _build_full_url(ep: EndpointInfo, settings: DiscoverySettings) -> str:
    """Build full URL for an endpoint."""
    base = settings.get_base_url(ep.source, ep.endpoint_type)
    if not base:
        return ep.path
    return f"{base}{ep.path}"


def _endpoint_to_dict(ep: EndpointInfo, settings: DiscoverySettings) -> dict[str, Any]:
    """Convert EndpointInfo to catalog JSON entry."""
    entry: dict[str, Any] = {
        "id": f"{ep.source}:{ep.endpoint_type}:{ep.path}",
        "source": ep.source,
        "market": get_market(ep.source),
        "endpoint_type": ep.endpoint_type,
        "url": _build_full_url(ep, settings),
        "path": ep.path,
        "method": ep.method,
        "description": ep.description,
        "category": ep.category,
        "domain_tags": ep.domain_tags,
        "granularity": ep.granularity or None,
        "coverage": ep.coverage or None,
        "fields_summary": ep.fields_summary,
        "sample_fields": ep.sample_fields,
        "supports_history": ep.supports_history,
        "response_format": ep.response_format or None,
    }
    if ep.history_method:
        entry["history_method"] = ep.history_method
    if ep.id_field:
        entry["id_field"] = ep.id_field
    if ep.request_example:
        entry["request_example"] = ep.request_example
    if ep.date_params:
        entry["date_params"] = ep.date_params
    return entry


def generate_catalog_json(
    endpoints: list[EndpointInfo], settings: DiscoverySettings
) -> dict[str, Any]:
    """Build the catalog.json structure."""
    tag_counter: Counter[str] = Counter()
    for ep in endpoints:
        tag_counter.update(ep.domain_tags)

    return {
        "meta": {
            "title": "Official Financial Data Catalog (Taiwan & Japan)",
            "description": (
                "Machine-readable catalog of official financial data API endpoints: "
                "Taiwan (TWSE, TPEx, MOPS, TDCC) and Japan (J-Quants, EDINET, TDnet, JPX). "
                "Designed for AI agents to discover official financial data sources."
            ),
            "version": "2.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_endpoints": len(endpoints),
            "sources": SOURCE_META,
        },
        "tags": dict(tag_counter.most_common()),
        "endpoints": [_endpoint_to_dict(ep, settings) for ep in endpoints],
    }


def generate_openapi_yaml(endpoint_count: int) -> str:
    """Generate OpenAPI 3.1 spec for the catalog API."""
    return f"""\
openapi: "3.1.0"
info:
  title: Official Financial Data Catalog API (Taiwan & Japan)
  description: |
    Static catalog of official financial data API endpoints:
    Taiwan (TWSE, TPEx, MOPS, TDCC) and Japan (J-Quants, EDINET, TDnet, JPX).
    AI agents can fetch /catalog.json to discover available data sources,
    then call the actual endpoints directly.
  version: "2.0.0"
  contact:
    name: QadrisCorp
    url: https://github.com/QadrisCorp/QadrisDataDiscovery

servers:
  - url: {GITHUB_PAGES_BASE}
    description: GitHub Pages

paths:
  /catalog.json:
    get:
      operationId: getCatalog
      summary: Get the full endpoint catalog
      description: |
        Returns a JSON object containing metadata about {endpoint_count} official
        financial data API endpoints from Taiwan (TWSE, TPEx, MOPS, TDCC) and
        Japan (J-Quants, EDINET, TDnet, JPX).
        Each endpoint includes URL, method, description, domain tags,
        field summaries, and request examples.
      responses:
        "200":
          description: Full catalog of financial data endpoints
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Catalog"
        "404":
          description: Not found. GitHub Pages returns an HTML error page, not JSON.

  /llms.txt:
    get:
      operationId: getLlmsTxt
      summary: AI agent discovery file
      description: Human/AI-readable summary of what this catalog provides.
      responses:
        "200":
          description: Plain text discovery file
          content:
            text/plain:
              schema:
                type: string
        "404":
          description: Not found. GitHub Pages returns an HTML error page, not JSON.

components:
  schemas:
    Catalog:
      type: object
      required: [meta, tags, endpoints]
      properties:
        meta:
          $ref: "#/components/schemas/CatalogMeta"
        tags:
          type: object
          description: Map of domain tag to endpoint count
          additionalProperties:
            type: integer
        endpoints:
          type: array
          items:
            $ref: "#/components/schemas/Endpoint"

    CatalogMeta:
      type: object
      required: [title, version, generated_at, total_endpoints, sources]
      properties:
        title:
          type: string
        description:
          type: string
        version:
          type: string
        generated_at:
          type: string
          format: date-time
        total_endpoints:
          type: integer
        sources:
          type: object
          description: "Map of source key (twse/tpex/mops/tdcc/jquants/edinet/tdnet/jpx) to metadata"
          additionalProperties:
            type: object
            properties:
              name:
                type: string
                description: English name of the data source
              name_zh:
                type: string
                description: Local-language name of the data source
              market:
                type: string
                enum: [tw, jp]
                description: Market the source belongs to
              base_urls:
                type: object
                description: "Map of endpoint_type to base URL"
                additionalProperties:
                  type: string
                  format: uri

    Endpoint:
      type: object
      required: [id, source, endpoint_type, url, method, description]
      properties:
        id:
          type: string
          description: "Unique ID: {{source}}:{{endpoint_type}}:{{path}}"
          example: "twse:openapi:/exchangeReport/STOCK_DAY_ALL"
        source:
          type: string
          enum: [twse, tpex, mops, tdcc, jquants, edinet, tdnet, jpx]
        market:
          type: string
          enum: [tw, jp]
          description: Market the source belongs to
        endpoint_type:
          type: string
          enum: [openapi, web, xbrl]
        url:
          type: string
          format: uri
          description: Full URL to call the endpoint
        path:
          type: string
          description: Path portion of the endpoint URL
        method:
          type: string
          enum: [GET, POST]
        description:
          type: string
          description: Human-readable description (often in Chinese)
        category:
          type: string
          description: Category or domain classification
        domain_tags:
          type: array
          items:
            type: string
          description: Semantic tags (e.g. price, volume, financial, revenue)
        granularity:
          type: [string, "null"]
          enum: [daily, monthly, quarterly, yearly, snapshot, null]
        coverage:
          type: [string, "null"]
          enum: [listed_only, otc_only, all, null]
          description: "For jp sources 'all' = all TSE segments (Prime/Standard/Growth)"
        fields_summary:
          type: string
          description: LLM-generated summary of response fields
        sample_fields:
          type: array
          items:
            type: string
          description: Field names from sample API response
        supports_history:
          type: boolean
          description: Whether historical data can be fetched
        history_method:
          type: string
          description: How to fetch historical data
        id_field:
          type: string
          description: Stock/company identifier field name
        request_example:
          type: object
          description: Complete request example with URL, method, params
        response_format:
          type: [string, "null"]
          enum: [json, html_table, excel, pdf, csv, zip, null]
        date_params:
          type: array
          items:
            type: string
          description: Date parameter names for historical queries
"""


_SOURCE_NOTES: dict[str, list[str]] = {
    "twse": [
        "OpenAPI: https://openapi.twse.com.tw/v1 (real-time, current day)",
        "Web: https://www.twse.com.tw (historical, add &response=json)",
    ],
    "tpex": [
        "OpenAPI: https://www.tpex.org.tw/openapi/v1 (real-time, current day)",
        "Web: https://www.tpex.org.tw (historical)",
    ],
    "mops": [
        "Web: https://mopsov.twse.com.tw (financial statements, revenue, governance)",
    ],
    "tdcc": [
        "OpenAPI: https://openapi.tdcc.com.tw (snapshot only; no history)",
    ],
    "jquants": [
        "API: https://api.jquants.com/v2 (JPX official; API key in x-api-key header)",
        "Rate limit: Free plan 5 req/min; endpoint plan tier noted in notes",
    ],
    "edinet": [
        "API v2: https://api.edinet-fsa.go.jp/api/v2 "
        "(Subscription-Key query param; free registration)",
        "Statutory filings: annual/semi-annual reports XBRL+CSV, "
        "large shareholding reports",
    ],
    "tdnet": [
        "Web: https://www.release.tdnet.info (timely disclosure; "
        "free window = last 31 days only)",
    ],
    "jpx": [
        "Web: https://www.jpx.co.jp statistics pages (Excel downloads; some PDF-only)",
        "Cloud-hosted clients get HTTP 403 — fetch from a local machine",
    ],
}


def generate_llms_txt(endpoints: list[EndpointInfo]) -> str:
    """Generate llms.txt discovery file."""
    tag_counter: Counter[str] = Counter()
    source_counter: Counter[str] = Counter()
    for ep in endpoints:
        tag_counter.update(ep.domain_tags)
        source_counter[ep.source] += 1

    top_tags = ", ".join(tag for tag, _ in tag_counter.most_common(20))

    source_lines: list[str] = []
    for key, spec in SOURCE_REGISTRY.items():
        source_lines.append(
            f"- **{spec.display_name}** ({spec.name_en} / {spec.name_local}) "
            f"[market: {spec.market}]: {source_counter[key]} endpoints"
        )
        for note in _SOURCE_NOTES.get(key, []):
            source_lines.append(f"  - {note}")
    sources_block = "\n".join(source_lines)

    return f"""\
# Official Financial Data Catalog (Taiwan & Japan)

> Machine-readable catalog of {len(endpoints)} official API endpoints from
> Taiwan (TWSE, TPEx, MOPS, TDCC) and Japan (J-Quants, EDINET, TDnet, JPX).
> Designed for AI agents to discover available financial data sources.

## How to use

1. Fetch the full catalog: GET {GITHUB_PAGES_BASE}/catalog.json
2. Search endpoints by domain_tags, description, category, or market (tw/jp)
3. Use the endpoint's url, method, and request_example to call the actual API

## OpenAPI spec

GET {GITHUB_PAGES_BASE}/openapi.yaml

## Sources

{sources_block}

## Available domain tags

{top_tags}

## Endpoint fields

Each endpoint in catalog.json includes:
- id, source, market (tw/jp), endpoint_type, url, path, method
- description (often in Chinese), category
- domain_tags — semantic classification
- granularity — daily, monthly, quarterly, yearly, snapshot
- coverage — listed_only, otc_only, all
- fields_summary — natural language description of response fields
- sample_fields — actual field names from API response
- supports_history, history_method, date_params
- request_example — complete request with URL, method, params
- response_format — json or html_table
- id_field — stock/company identifier field name

## Tips for AI agents

- Use domain_tags to filter endpoints by topic (e.g. "price", "revenue", "financial")
- Check supports_history and history_method for time-series data
- request_example has ready-to-use request parameters
- MOPS endpoints use POST method and ROC calendar dates
- TWSE/TPEx OpenAPI endpoints are real-time snapshots (no history)
- TWSE/TPEx Web endpoints support historical queries with date parameters
- J-Quants requires an API key (x-api-key header); Free plan is 5 req/min
- EDINET requires a Subscription-Key query param (free registration)
- TDnet free web pages only keep the last 31 days
- JPX statistics file URLs contain random CMS paths — re-crawl, do not hardcode
"""


def generate_index_html(endpoint_count: int) -> str:
    """Generate a simple search UI page."""
    return f"""\
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Official Financial Data Catalog (TW/JP)</title>
<style>
  :root {{
    --bg: #0a0a0a; --surface: #141414; --border: #2a2a2a;
    --text: #e0e0e0; --text-muted: #888; --accent: #4fc3f7;
    --tag-bg: #1a2a3a; --tag-text: #7fdbff;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    background: var(--bg); color: var(--text); line-height: 1.6;
    padding: 2rem; max-width: 1200px; margin: 0 auto;
  }}
  h1 {{ color: var(--accent); font-size: 1.5rem; margin-bottom: 0.5rem; }}
  .subtitle {{ color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.9rem; }}
  .controls {{
    display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap;
  }}
  input, select {{
    background: var(--surface); border: 1px solid var(--border);
    color: var(--text); padding: 0.5rem 0.75rem; border-radius: 4px;
    font-size: 0.875rem;
  }}
  input {{ flex: 1; min-width: 200px; }}
  input:focus, select:focus {{ outline: none; border-color: var(--accent); }}
  .stats {{
    color: var(--text-muted); font-size: 0.8rem; margin-bottom: 1rem;
  }}
  .endpoint {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 6px; padding: 1rem; margin-bottom: 0.75rem;
    cursor: pointer; transition: border-color 0.2s;
  }}
  .endpoint:hover {{ border-color: var(--accent); }}
  .endpoint-header {{
    display: flex; justify-content: space-between; align-items: flex-start;
    gap: 1rem; margin-bottom: 0.5rem;
  }}
  .endpoint-title {{
    font-size: 0.9rem; font-weight: 600; word-break: break-all;
  }}
  .endpoint-source {{
    font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 3px;
    background: var(--tag-bg); color: var(--tag-text); white-space: nowrap;
    flex-shrink: 0;
  }}
  .endpoint-desc {{
    color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;
  }}
  .endpoint-tags {{ display: flex; gap: 0.4rem; flex-wrap: wrap; }}
  .tag {{
    font-size: 0.7rem; padding: 0.1rem 0.4rem; border-radius: 3px;
    background: var(--tag-bg); color: var(--tag-text);
  }}
  .endpoint-detail {{
    display: none; margin-top: 0.75rem; padding-top: 0.75rem;
    border-top: 1px solid var(--border); font-size: 0.8rem;
  }}
  .endpoint.expanded .endpoint-detail {{ display: block; }}
  .detail-row {{
    display: flex; gap: 0.5rem; margin-bottom: 0.3rem;
  }}
  .detail-label {{
    color: var(--text-muted); min-width: 120px; flex-shrink: 0;
  }}
  .detail-value {{ word-break: break-all; }}
  pre {{
    background: var(--bg); border: 1px solid var(--border);
    padding: 0.5rem; border-radius: 4px; overflow-x: auto;
    font-size: 0.75rem; margin-top: 0.3rem;
  }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .agent-links {{
    margin-bottom: 1.5rem; font-size: 0.85rem;
    display: flex; gap: 1.5rem;
  }}
  .agent-links a {{
    padding: 0.3rem 0.6rem; border: 1px solid var(--border);
    border-radius: 4px;
  }}
</style>
</head>
<body>

<h1>Official Financial Data Catalog (TW/JP)</h1>
<p class="subtitle">{endpoint_count} official API endpoints —
Taiwan (TWSE, TPEx, MOPS, TDCC) &amp; Japan (J-Quants, EDINET, TDnet, JPX)</p>

<div class="agent-links">
  <a href="catalog.json">catalog.json</a>
  <a href="openapi.yaml">openapi.yaml</a>
  <a href="llms.txt">llms.txt</a>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="Search description, tags, fields...">
  <select id="market-filter">
    <option value="">All Markets</option>
    <option value="tw">Taiwan</option>
    <option value="jp">Japan</option>
  </select>
  <select id="source-filter">
    <option value="">All Sources</option>
    <option value="twse">TWSE</option>
    <option value="tpex">TPEx</option>
    <option value="mops">MOPS</option>
    <option value="tdcc">TDCC</option>
    <option value="jquants">J-Quants</option>
    <option value="edinet">EDINET</option>
    <option value="tdnet">TDnet</option>
    <option value="jpx">JPX</option>
  </select>
  <select id="tag-filter">
    <option value="">All Tags</option>
  </select>
  <select id="granularity-filter">
    <option value="">All Granularity</option>
  </select>
</div>

<div class="stats" id="stats"></div>
<div id="endpoints"></div>

<script>
let catalog = null;

async function init() {{
  const res = await fetch("catalog.json");
  catalog = await res.json();

  // Populate tag filter
  const tagSelect = document.getElementById("tag-filter");
  Object.entries(catalog.tags)
    .sort((a, b) => b[1] - a[1])
    .forEach(([tag, count]) => {{
      const opt = document.createElement("option");
      opt.value = tag;
      opt.textContent = `${{tag}} (${{count}})`;
      tagSelect.appendChild(opt);
    }});

  // Populate granularity filter
  const granSet = new Set(catalog.endpoints.map(e => e.granularity).filter(Boolean));
  const granSelect = document.getElementById("granularity-filter");
  [...granSet].sort().forEach(g => {{
    const opt = document.createElement("option");
    opt.value = g;
    opt.textContent = g;
    granSelect.appendChild(opt);
  }});

  render();
}}

function render() {{
  const query = document.getElementById("search").value.toLowerCase();
  const market = document.getElementById("market-filter").value;
  const source = document.getElementById("source-filter").value;
  const tag = document.getElementById("tag-filter").value;
  const gran = document.getElementById("granularity-filter").value;

  const filtered = catalog.endpoints.filter(ep => {{
    if (market && ep.market !== market) return false;
    if (source && ep.source !== source) return false;
    if (tag && !ep.domain_tags.includes(tag)) return false;
    if (gran && ep.granularity !== gran) return false;
    if (query) {{
      const haystack = [
        ep.description, ep.fields_summary, ep.category, ep.path,
        ...ep.domain_tags, ...ep.sample_fields
      ].join(" ").toLowerCase();
      return haystack.includes(query);
    }}
    return true;
  }});

  document.getElementById("stats").textContent =
    `Showing ${{filtered.length}} of ${{catalog.endpoints.length}} endpoints`;

  const container = document.getElementById("endpoints");
  container.innerHTML = filtered.slice(0, 200).map(ep => `
    <div class="endpoint" onclick="this.classList.toggle('expanded')">
      <div class="endpoint-header">
        <span class="endpoint-title">${{ep.description || ep.path}}</span>
        <span class="endpoint-source">${{ep.source.toUpperCase()}} / ${{ep.endpoint_type}}</span>
      </div>
      <div class="endpoint-desc">${{ep.path}}</div>
      <div class="endpoint-tags">
        ${{ep.domain_tags.map(t => `<span class="tag">${{t}}</span>`).join("")}}
        ${{ep.granularity ? `<span class="tag">${{ep.granularity}}</span>` : ""}}
        ${{ep.supports_history ? '<span class="tag">history</span>' : ""}}
      </div>
      <div class="endpoint-detail">
        <div class="detail-row"><span class="detail-label">URL</span><span class="detail-value"><a href="${{ep.url}}" target="_blank">${{ep.url}}</a></span></div>
        <div class="detail-row"><span class="detail-label">Method</span><span class="detail-value">${{ep.method}}</span></div>
        ${{ep.fields_summary ? `<div class="detail-row"><span class="detail-label">Fields Summary</span><span class="detail-value">${{ep.fields_summary}}</span></div>` : ""}}
        ${{ep.sample_fields.length ? `<div class="detail-row"><span class="detail-label">Sample Fields</span><span class="detail-value">${{ep.sample_fields.join(", ")}}</span></div>` : ""}}
        ${{ep.coverage ? `<div class="detail-row"><span class="detail-label">Coverage</span><span class="detail-value">${{ep.coverage}}</span></div>` : ""}}
        ${{ep.id_field ? `<div class="detail-row"><span class="detail-label">ID Field</span><span class="detail-value">${{ep.id_field}}</span></div>` : ""}}
        ${{ep.history_method ? `<div class="detail-row"><span class="detail-label">History Method</span><span class="detail-value">${{ep.history_method}}</span></div>` : ""}}
        ${{ep.request_example ? `<div class="detail-row"><span class="detail-label">Request Example</span></div><pre>${{JSON.stringify(ep.request_example, null, 2)}}</pre>` : ""}}
      </div>
    </div>
  `).join("");
}}

document.getElementById("search").addEventListener("input", render);
document.getElementById("market-filter").addEventListener("change", render);
document.getElementById("source-filter").addEventListener("change", render);
document.getElementById("tag-filter").addEventListener("change", render);
document.getElementById("granularity-filter").addEventListener("change", render);

init();
</script>
</body>
</html>
"""


def main() -> None:
    """Generate all GitHub Pages files."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    settings = DiscoverySettings()
    docs_dir = settings.project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    with CatalogDB(settings.db_path) as db:
        all_eps = db.get_all_endpoints()

    # Filter: only OK + enriched
    endpoints = [
        ep for ep in all_eps if ep.status == "ok" and ep.state == "enriched"
    ]
    logger.info("Selected %d endpoints (OK + enriched) out of %d total", len(endpoints), len(all_eps))

    # Sort by source, then category, then path
    endpoints.sort(key=lambda e: (e.source, e.category, e.path))

    # Generate catalog.json
    catalog = generate_catalog_json(endpoints, settings)
    catalog_path = docs_dir / "catalog.json"
    catalog_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    logger.info("Generated %s (%d endpoints)", catalog_path, len(endpoints))

    # Generate openapi.yaml
    openapi_path = docs_dir / "openapi.yaml"
    openapi_path.write_text(generate_openapi_yaml(len(endpoints)), encoding="utf-8")
    logger.info("Generated %s", openapi_path)

    # Generate llms.txt
    llms_path = docs_dir / "llms.txt"
    llms_path.write_text(generate_llms_txt(endpoints), encoding="utf-8")
    logger.info("Generated %s", llms_path)

    # Generate index.html
    index_path = docs_dir / "index.html"
    index_path.write_text(generate_index_html(len(endpoints)), encoding="utf-8")
    logger.info("Generated %s", index_path)

    logger.info("Done! All files in %s", docs_dir)


if __name__ == "__main__":
    main()
