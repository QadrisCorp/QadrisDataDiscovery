#!/bin/bash
# Export endpoints to Google Sheets
set -e

cd "$(dirname "$0")/.."

# Install deps if needed
uv run --python 3.12 pip install gspread google-auth --quiet 2>/dev/null

uv run --python 3.12 python scripts/export_to_gsheet.py
