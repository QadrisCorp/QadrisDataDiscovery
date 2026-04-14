"""Database schema definitions and migration logic."""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1

_CREATE_ENDPOINTS = """\
CREATE TABLE IF NOT EXISTS endpoints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source          TEXT NOT NULL,
    path            TEXT NOT NULL,
    endpoint_type   TEXT NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    category        TEXT NOT NULL DEFAULT '',
    method          TEXT NOT NULL DEFAULT 'GET',
    supports_history INTEGER NOT NULL DEFAULT 0,
    date_params     TEXT NOT NULL DEFAULT '[]',
    status          TEXT NOT NULL DEFAULT 'unknown',
    record_count    INTEGER NOT NULL DEFAULT 0,
    sample_fields   TEXT NOT NULL DEFAULT '[]',
    notes           TEXT NOT NULL DEFAULT '',
    domain_tags     TEXT NOT NULL DEFAULT '[]',
    granularity     TEXT NOT NULL DEFAULT '',
    history_method  TEXT NOT NULL DEFAULT '',
    id_field        TEXT NOT NULL DEFAULT '',
    request_example TEXT NOT NULL DEFAULT '{}',
    response_format TEXT NOT NULL DEFAULT '',
    coverage        TEXT NOT NULL DEFAULT '',
    fields_summary  TEXT NOT NULL DEFAULT '',
    state           TEXT NOT NULL DEFAULT 'discovered',
    sample_path     TEXT NOT NULL DEFAULT '',
    discovered_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    UNIQUE(source, path)
);
"""

_CREATE_SCHEMA_VERSION = """\
CREATE TABLE IF NOT EXISTS schema_version (
    version    INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
"""

_CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_endpoints_source ON endpoints(source);",
    "CREATE INDEX IF NOT EXISTS idx_endpoints_status ON endpoints(status);",
    "CREATE INDEX IF NOT EXISTS idx_endpoints_state ON endpoints(state);",
]


def get_schema_version(conn: sqlite3.Connection) -> int:
    """Return current schema version, 0 if table doesn't exist."""
    try:
        row = conn.execute(
            "SELECT MAX(version) FROM schema_version"
        ).fetchone()
        return row[0] or 0
    except sqlite3.OperationalError:
        return 0


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist and run pending migrations."""
    current = get_schema_version(conn)

    if current >= SCHEMA_VERSION:
        return

    conn.execute(_CREATE_ENDPOINTS)
    conn.execute(_CREATE_SCHEMA_VERSION)
    for idx_sql in _CREATE_INDEXES:
        conn.execute(idx_sql)

    if current < 1:
        conn.execute(
            "INSERT OR IGNORE INTO schema_version (version) VALUES (?)",
            (SCHEMA_VERSION,),
        )

    conn.commit()
    logger.info("Database initialized at schema version %d", SCHEMA_VERSION)
