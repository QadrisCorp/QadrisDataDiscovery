"""Generate consolidated catalog report from all discovery results."""

from __future__ import annotations

import logging

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.store import CatalogDB

logger = logging.getLogger(__name__)


def _generate_markdown(endpoints: list[EndpointInfo]) -> str:
    """Generate markdown report."""
    lines: list[str] = []
    lines.append("# Taiwan Official Financial Data Source Catalog")
    lines.append("")
    lines.append(f"**Total: {len(endpoints)} endpoints**")
    lines.append("")

    # Statistics
    by_source: dict[str, list[EndpointInfo]] = {}
    for ep in endpoints:
        by_source.setdefault(ep.source, []).append(ep)

    lines.append("## Summary Statistics")
    lines.append("")
    lines.append("| Source | Type | Total | OK | Empty | Error | History |")
    lines.append("|--------|------|-------|----|-------|-------|---------|")

    for source in ["twse", "tpex", "mops", "tdcc"]:
        eps = by_source.get(source, [])
        by_type: dict[str, list[EndpointInfo]] = {}
        for ep in eps:
            by_type.setdefault(ep.endpoint_type, []).append(ep)

        for etype, type_eps in sorted(by_type.items()):
            ok = sum(1 for e in type_eps if e.status == "ok")
            empty = sum(1 for e in type_eps if e.status == "empty")
            error = sum(1 for e in type_eps if e.status == "error")
            hist = sum(1 for e in type_eps if e.supports_history)
            source_name = {"twse": "TWSE", "tpex": "TPEx", "mops": "MOPS"}[source]
            lines.append(
                f"| {source_name} | {etype} | {len(type_eps)} "
                f"| {ok} | {empty} | {error} | {hist} |"
            )

    lines.append("")

    # Detail per source
    source_names = {
        "twse": "TWSE (Taiwan Stock Exchange)",
        "tpex": "TPEx (Taipei Exchange)",
        "mops": "MOPS (Market Observation Post System)",
    }

    for source in ["twse", "tpex", "mops", "tdcc"]:
        eps = by_source.get(source, [])
        if not eps:
            continue

        lines.append(f"## {source_names[source]}")
        lines.append("")

        source_by_type: dict[str, list[EndpointInfo]] = {}
        for ep in eps:
            source_by_type.setdefault(ep.endpoint_type, []).append(ep)

        for etype, type_eps in sorted(source_by_type.items()):
            type_names = {"openapi": "OpenAPI", "web": "Web", "xbrl": "XBRL"}
            lines.append(
                f"### {type_names.get(etype, etype)} ({len(type_eps)} endpoints)"
            )
            lines.append("")

            by_cat: dict[str, list[EndpointInfo]] = {}
            for ep in type_eps:
                by_cat.setdefault(ep.category or "Other", []).append(ep)

            for cat, cat_eps in sorted(by_cat.items()):
                lines.append(f"#### {cat}")
                lines.append("")
                lines.append(
                    "| Path | Description | Status | History | Count | Fields |"
                )
                lines.append(
                    "|------|-------------|--------|---------|-------|--------|"
                )

                for ep in cat_eps:
                    fields_str = (
                        ", ".join(ep.sample_fields[:5]) if ep.sample_fields else ""
                    )
                    if len(fields_str) > 50:
                        fields_str = fields_str[:47] + "..."
                    hist_flag = "Y" if ep.supports_history else "N"
                    path_short = (
                        ep.path if len(ep.path) <= 50 else "..." + ep.path[-47:]
                    )
                    lines.append(
                        f"| `{path_short}` | {ep.description} "
                        f"| {ep.status} | {hist_flag} "
                        f"| {ep.record_count} | {fields_str} |"
                    )

                lines.append("")

    # Technical notes
    lines.append("## Technical Notes")
    lines.append("")
    lines.append("### TWSE")
    lines.append(
        "- **OpenAPI**: `https://openapi.twse.com.tw/v1` — real-time, current day only"
    )
    lines.append(
        "- **Web**: `https://www.twse.com.tw`"
        " — historical, add `&response=json` for JSON"
    )
    lines.append("- Date format: `YYYYMMDD`")
    lines.append("- Rate limit: OpenAPI 1s, Web 3s")
    lines.append("")
    lines.append("### TPEx")
    lines.append(
        "- **OpenAPI**: `https://www.tpex.org.tw/openapi/v1`"
        " — real-time, current day only"
    )
    lines.append(
        "- **Web**: `https://www.tpex.org.tw/www/zh-tw/` — new API, partial JSON"
    )
    lines.append("- Date format: OpenAPI `YYYYMMDD`, old web ROC year `YYY/MM/DD`")
    lines.append("")
    lines.append("### MOPS")
    lines.append(
        "- **New SPA**: `https://mops.twse.com.tw/mops/` — Vue SPA, requires Selenium"
    )
    lines.append(
        "- **Old**: `https://mopsov.twse.com.tw` — still works via requests + AJAX"
    )
    lines.append(
        "- **API**: `https://mops.interinfo.com.tw:8443` — browser Worker only"
    )
    lines.append("- Monthly revenue via `/nas/t21/{type}/` static HTML")
    lines.append("- Financial statements return HTML tables directly")
    lines.append("- Date format: ROC calendar year")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Load all catalogs and generate consolidated report."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = DiscoverySettings()
    with CatalogDB(settings.db_path) as db:
        endpoints = db.get_all_endpoints()
    logger.info("Total loaded: %d endpoints", len(endpoints))

    md_content = _generate_markdown(endpoints)
    output = settings.catalog_dir / "full_catalog.md"
    output.write_text(md_content, encoding="utf-8")
    logger.info("Full catalog saved: %s", output)


if __name__ == "__main__":
    main()
