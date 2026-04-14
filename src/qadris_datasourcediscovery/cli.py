"""CLI for qadris-datasourcediscovery — search, show, enrich catalog."""

from __future__ import annotations

import json
import logging
from collections import Counter
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.enrich import enrich_all
from qadris_datasourcediscovery.llm import ClaudeCLI
from qadris_datasourcediscovery.store import CatalogDB

app = typer.Typer(help="Taiwan financial data source catalog tool.")
console = Console()


def _get_settings() -> DiscoverySettings:
    return DiscoverySettings()


def _get_db() -> CatalogDB:
    settings = _get_settings()
    return CatalogDB(settings.db_path)


def _load_endpoints(
    *,
    source: str | None = None,
    status: str | None = None,
    state: str | None = None,
) -> list[EndpointInfo]:
    with _get_db() as db:
        return db.get_endpoints(source=source, status=status, state=state)


def _match_endpoint(
    ep: EndpointInfo,
    *,
    tag: list[str] | None = None,
    keyword: str | None = None,
    history: bool | None = None,
) -> bool:
    """Check if endpoint matches in-memory filters (tag, keyword, history)."""
    if history is not None and ep.supports_history != history:
        return False
    if tag:
        if not any(t in ep.domain_tags for t in tag):
            return False
    if keyword:
        kw = keyword.lower()
        searchable = " ".join(
            [
                ep.path,
                ep.description,
                ep.category,
                ep.fields_summary,
                ep.notes,
                " ".join(ep.sample_fields),
                " ".join(ep.domain_tags),
            ]
        ).lower()
        if kw not in searchable:
            return False
    return True


@app.command()
def search(
    tag: Annotated[
        Optional[list[str]], typer.Option("--tag", "-t", help="Filter by domain tag")
    ] = None,
    keyword: Annotated[
        Optional[str], typer.Option("--keyword", "-k", help="Full-text keyword search")
    ] = None,
    source: Annotated[
        Optional[str], typer.Option("--source", "-s", help="Filter by source (twse/tpex/mops)")
    ] = None,
    status: Annotated[
        Optional[str], typer.Option("--status", help="Filter by status (ok/empty/error)")
    ] = None,
    state: Annotated[
        Optional[str], typer.Option("--state", help="Filter by state (discovered/probed/enriched)")
    ] = None,
    history: Annotated[
        Optional[bool], typer.Option("--history/--no-history", help="Filter by history support")
    ] = None,
    output_json: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Search endpoints by tag, keyword, source, status, or state."""
    endpoints = _load_endpoints(source=source, status=status, state=state)
    matches = [
        ep
        for ep in endpoints
        if _match_endpoint(ep, tag=tag, keyword=keyword, history=history)
    ]

    if output_json:
        typer.echo(json.dumps([ep.model_dump() for ep in matches], ensure_ascii=False, indent=2))
        return

    if not matches:
        console.print("[yellow]No endpoints found matching your criteria.[/yellow]")
        return

    table = Table(title=f"Found {len(matches)} endpoints")
    table.add_column("Source", style="cyan", width=6)
    table.add_column("Type", width=7)
    table.add_column("Path", style="green", max_width=40)
    table.add_column("Description", max_width=30)
    table.add_column("Tags", style="magenta", max_width=25)
    table.add_column("State", width=10)
    table.add_column("Status", width=6)

    for ep in matches:
        tags_str = ", ".join(ep.domain_tags) if ep.domain_tags else "-"
        table.add_row(
            ep.source,
            ep.endpoint_type,
            ep.path,
            ep.description[:30],
            tags_str,
            ep.state,
            ep.status,
        )

    console.print(table)


@app.command()
def show(
    identifier: Annotated[str, typer.Argument(help="Endpoint ID: source:path (e.g. twse:/opendata/t187ap45_L)")],
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Show detailed info for a single endpoint."""
    if ":" not in identifier:
        console.print("[red]Format: source:path (e.g. twse:/opendata/t187ap45_L)[/red]")
        raise typer.Exit(1)

    src, path = identifier.split(":", 1)

    with _get_db() as db:
        match = db.get_endpoint(src, path)

    if not match:
        # Fuzzy: try path contains
        all_eps = _load_endpoints(source=src)
        candidates = [ep for ep in all_eps if path in ep.path]
        if len(candidates) == 1:
            match = candidates[0]
        elif candidates:
            console.print(f"[yellow]Multiple matches for '{identifier}':[/yellow]")
            for c in candidates:
                console.print(f"  {c.source}:{c.path} — {c.description}")
            raise typer.Exit(1)
        else:
            console.print(f"[red]Endpoint not found: {identifier}[/red]")
            raise typer.Exit(1)

    if output_json:
        typer.echo(json.dumps(match.model_dump(), ensure_ascii=False, indent=2))
        return

    console.print(f"\n[bold cyan]{match.source}:{match.path}[/bold cyan]")
    console.print(f"[bold]{match.description}[/bold]\n")

    info = [
        ("Source", match.source),
        ("Type", match.endpoint_type),
        ("Category", match.category),
        ("Method", match.method),
        ("Status", match.status),
        ("State", match.state),
        ("Record Count", str(match.record_count)),
        ("History", "Yes" if match.supports_history else "No"),
        ("Date Params", ", ".join(match.date_params) if match.date_params else "-"),
        ("Domain Tags", ", ".join(match.domain_tags) if match.domain_tags else "-"),
        ("Granularity", match.granularity or "-"),
        ("History Method", match.history_method or "-"),
        ("ID Field", match.id_field or "-"),
        ("Response Format", match.response_format or "-"),
        ("Coverage", match.coverage or "-"),
        ("Fields Summary", match.fields_summary or "-"),
    ]

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    for label, value in info:
        table.add_row(label, value)
    console.print(table)

    if match.request_example:
        console.print("\n[bold]Request Example:[/bold]")
        console.print(json.dumps(match.request_example, indent=2))

    if match.sample_fields:
        console.print(f"\n[bold]Sample Fields ({len(match.sample_fields)}):[/bold]")
        for f in match.sample_fields:
            console.print(f"  - {f}")

    if match.notes:
        console.print(f"\n[bold]Notes:[/bold] {match.notes}")
    console.print()


@app.command()
def tags(
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """List all domain tags with endpoint counts."""
    endpoints = _load_endpoints()

    tag_counter: Counter[str] = Counter()
    tag_sources: dict[str, set[str]] = {}
    for ep in endpoints:
        for t in ep.domain_tags:
            tag_counter[t] += 1
            tag_sources.setdefault(t, set()).add(ep.source)

    if output_json:
        result = {
            t: {"count": c, "sources": sorted(tag_sources.get(t, set()))}
            for t, c in tag_counter.most_common()
        }
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not tag_counter:
        console.print("[yellow]No domain tags found. Run 'enrich' first.[/yellow]")
        return

    table = Table(title="Domain Tags")
    table.add_column("Tag", style="magenta")
    table.add_column("Count", justify="right")
    table.add_column("Sources")

    for t, count in tag_counter.most_common():
        sources = ", ".join(sorted(tag_sources.get(t, set())))
        table.add_row(t, str(count), sources)

    console.print(table)

    # Summary
    enriched = sum(1 for ep in endpoints if ep.domain_tags)
    console.print(
        f"\n[dim]{enriched}/{len(endpoints)} endpoints have domain tags[/dim]"
    )


@app.command()
def stats(
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Show catalog summary statistics."""
    endpoints = _load_endpoints()

    by_source: dict[str, list[EndpointInfo]] = {}
    for ep in endpoints:
        by_source.setdefault(ep.source, []).append(ep)

    enriched_count = sum(1 for ep in endpoints if ep.domain_tags)

    if output_json:
        result: dict[str, object] = {
            "total": len(endpoints),
            "enriched": enriched_count,
            "by_source": {},
        }
        for src, eps in sorted(by_source.items()):
            result_by_source = result["by_source"]
            assert isinstance(result_by_source, dict)
            result_by_source[src] = {
                "total": len(eps),
                "ok": sum(1 for e in eps if e.status == "ok"),
                "empty": sum(1 for e in eps if e.status == "empty"),
                "error": sum(1 for e in eps if e.status == "error"),
                "enriched": sum(1 for e in eps if e.domain_tags),
            }
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    console.print(f"\n[bold]Total: {len(endpoints)} endpoints[/bold]")
    console.print(f"Enriched: {enriched_count}/{len(endpoints)}\n")

    table = Table(title="By Source")
    table.add_column("Source", style="cyan")
    table.add_column("Type")
    table.add_column("Total", justify="right")
    table.add_column("OK", justify="right", style="green")
    table.add_column("Empty", justify="right", style="yellow")
    table.add_column("Error", justify="right", style="red")
    table.add_column("Enriched", justify="right", style="magenta")

    source_names = {"twse": "TWSE", "tpex": "TPEx", "mops": "MOPS"}
    for src in ["twse", "tpex", "mops"]:
        eps = by_source.get(src, [])
        by_type: dict[str, list[EndpointInfo]] = {}
        for ep in eps:
            by_type.setdefault(ep.endpoint_type, []).append(ep)

        for etype, type_eps in sorted(by_type.items()):
            ok = sum(1 for e in type_eps if e.status == "ok")
            empty = sum(1 for e in type_eps if e.status == "empty")
            error = sum(1 for e in type_eps if e.status == "error")
            enriched = sum(1 for e in type_eps if e.domain_tags)
            table.add_row(
                source_names.get(src, src),
                etype,
                str(len(type_eps)),
                str(ok),
                str(empty),
                str(error),
                str(enriched),
            )

    console.print(table)
    console.print()


@app.command()
def probe(
    source: Annotated[
        str, typer.Argument(help="Source to probe (twse)")
    ] = "twse",
    limit: Annotated[
        int, typer.Option("--limit", "-n", help="Max endpoints to probe")
    ] = 10,
) -> None:
    """Probe discovered endpoints to extract API data and sample fields."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    settings = _get_settings()

    if source == "twse":
        from qadris_datasourcediscovery.discover_tse_web import probe_discovered
        results = probe_discovered(settings=settings, limit=limit)
    elif source == "tpex":
        from qadris_datasourcediscovery.discover_otc_web import probe_discovered
        results = probe_discovered(settings=settings, limit=limit)
    elif source == "mops":
        from qadris_datasourcediscovery.discover_mops import probe_discovered
        results = probe_discovered(settings=settings, limit=limit)
    else:
        console.print(f"[red]Probe not implemented for source: {source}[/red]")
        raise typer.Exit(1)

    with _get_db() as db:
        db.upsert_endpoints(results)

    ok = sum(1 for ep in results if ep.status == "ok")
    err = sum(1 for ep in results if ep.status == "error")
    console.print(
        f"\n[bold]Probed {len(results)} endpoints: "
        f"[green]{ok} ok[/green], [red]{err} error[/red][/bold]"
    )


@app.command()
def enrich(
    rules_only: Annotated[
        bool, typer.Option("--rules-only", help="Only run rule-based enrichment")
    ] = False,
    llm_only: Annotated[
        bool, typer.Option("--llm-only", help="Only run LLM enrichment")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Re-enrich even if already enriched")
    ] = False,
    limit: Annotated[
        int, typer.Option("--limit", "-n", help="Max endpoints to LLM-enrich")
    ] = 0,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Show what would change without writing")
    ] = False,
    model: Annotated[
        str, typer.Option("--model", help="LLM model for enrichment")
    ] = "claude-haiku-4-5-20251001",
) -> None:
    """Run enrichment on catalog (rule-based and/or LLM)."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    llm: ClaudeCLI | None = None
    if not rules_only:
        llm = ClaudeCLI(model=model)

    with _get_db() as db:
        count = enrich_all(
            db=db,
            llm=llm,
            rules_only=rules_only,
            llm_only=llm_only,
            force=force,
            limit=limit,
            dry_run=dry_run,
        )

    action = "Would enrich" if dry_run else "Enriched"
    console.print(f"\n[bold]{action} {count} endpoints[/bold]")


if __name__ == "__main__":
    app()
