"""Export endpoints table to Google Sheets."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

from qadris_datasourcediscovery.config import DiscoverySettings
from qadris_datasourcediscovery.store import CatalogDB

CREDENTIALS_PATH = Path(__file__).resolve().parent.parent / "credentials" / "client_secret_chubear.json"
SHEET_ID = "1dmCA3H9dSte3a2t9D8NjebQIkgGjmyhygaHOtYwGoEw"
WORKSHEET_NAME = "endpoints"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

HEADERS = [
    "source",
    "endpoint_type",
    "path",
    "description",
    "category",
    "method",
    "status",
    "state",
    "supports_history",
    "record_count",
    "sample_fields",
    "date_params",
    "domain_tags",
    "granularity",
    "history_method",
    "id_field",
    "response_format",
    "coverage",
    "fields_summary",
    "notes",
]


def main() -> None:
    settings = DiscoverySettings()

    # Load endpoints
    with CatalogDB(settings.db_path) as db:
        endpoints = db.get_all_endpoints()

    print(f"Loaded {len(endpoints)} endpoints from DB")

    # Build rows
    rows: list[list[str]] = [HEADERS]
    for ep in endpoints:
        rows.append([
            ep.source,
            ep.endpoint_type,
            ep.path,
            ep.description,
            ep.category,
            ep.method,
            ep.status,
            ep.state,
            "Y" if ep.supports_history else "N",
            str(ep.record_count),
            ", ".join(ep.sample_fields) if ep.sample_fields else "",
            ", ".join(ep.date_params) if ep.date_params else "",
            ", ".join(ep.domain_tags) if ep.domain_tags else "",
            ep.granularity,
            ep.history_method,
            ep.id_field,
            ep.response_format,
            ep.coverage,
            ep.fields_summary,
            ep.notes,
        ])

    # Auth & upload
    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=SCOPES)
    gc = gspread.authorize(creds)

    sh = gc.open_by_key(SHEET_ID)

    # Get or create worksheet
    try:
        ws = sh.worksheet(WORKSHEET_NAME)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=WORKSHEET_NAME, rows=len(rows), cols=len(HEADERS))

    ws.update(range_name="A1", values=rows)

    print(f"Exported {len(rows) - 1} endpoints to Google Sheets")
    print(f"  Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    main()
