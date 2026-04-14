"""CatalogDB — SQLite persistence for endpoint catalog."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from qadris_datasourcediscovery.catalog import EndpointInfo
from qadris_datasourcediscovery.exceptions import StoreError
from qadris_datasourcediscovery.store.schema import init_db

logger = logging.getLogger(__name__)

# EndpointInfo 中需要 JSON 序列化的欄位
_JSON_FIELDS = {"date_params", "sample_fields", "domain_tags", "request_example"}


class CatalogDB:
    """SQLite persistence layer for endpoint catalog."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._conn = sqlite3.connect(str(db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            init_db(self._conn)
        except sqlite3.Error as e:
            raise StoreError(f"Failed to open database: {db_path}") from e

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __enter__(self) -> CatalogDB:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def upsert_endpoints(self, endpoints: list[EndpointInfo]) -> int:
        """Insert or update endpoints by (source, path). Returns rows affected."""
        if not endpoints:
            return 0

        sql = """\
            INSERT INTO endpoints (
                source, path, endpoint_type, description, category, method,
                supports_history, date_params, status, record_count,
                sample_fields, notes, domain_tags, granularity, history_method,
                id_field, request_example, response_format, coverage,
                fields_summary, state, sample_path, updated_at
            ) VALUES (
                :source, :path, :endpoint_type, :description, :category, :method,
                :supports_history, :date_params, :status, :record_count,
                :sample_fields, :notes, :domain_tags, :granularity, :history_method,
                :id_field, :request_example, :response_format, :coverage,
                :fields_summary, :state, :sample_path, :updated_at
            )
            ON CONFLICT(source, path) DO UPDATE SET
                endpoint_type   = excluded.endpoint_type,
                description     = excluded.description,
                category        = excluded.category,
                method          = excluded.method,
                supports_history = excluded.supports_history,
                date_params     = excluded.date_params,
                status          = excluded.status,
                record_count    = excluded.record_count,
                sample_fields   = excluded.sample_fields,
                notes           = excluded.notes,
                domain_tags     = excluded.domain_tags,
                granularity     = excluded.granularity,
                history_method  = excluded.history_method,
                id_field        = excluded.id_field,
                request_example = excluded.request_example,
                response_format = excluded.response_format,
                coverage        = excluded.coverage,
                fields_summary  = excluded.fields_summary,
                state           = CASE
                    WHEN excluded.state = 'enriched' THEN 'enriched'
                    WHEN excluded.state = 'probed' AND endpoints.state != 'enriched' THEN 'probed'
                    WHEN endpoints.state = '' OR endpoints.state = 'discovered' THEN excluded.state
                    ELSE endpoints.state
                END,
                sample_path     = excluded.sample_path,
                updated_at      = excluded.updated_at
        """

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        count = 0
        for ep in endpoints:
            params = self._endpoint_to_params(ep)
            params["updated_at"] = now
            self._conn.execute(sql, params)
            count += 1

        self._conn.commit()
        return count

    def get_endpoint(self, source: str, path: str) -> EndpointInfo | None:
        """Fetch a single endpoint by its natural key."""
        row = self._conn.execute(
            "SELECT * FROM endpoints WHERE source = ? AND path = ?",
            (source, path),
        ).fetchone()
        if row is None:
            return None
        return self._row_to_endpoint(row)

    def get_all_endpoints(self) -> list[EndpointInfo]:
        """Return all endpoints."""
        rows = self._conn.execute(
            "SELECT * FROM endpoints ORDER BY source, path"
        ).fetchall()
        return [self._row_to_endpoint(r) for r in rows]

    def get_endpoints(
        self,
        *,
        source: str | None = None,
        status: str | None = None,
        state: str | None = None,
    ) -> list[EndpointInfo]:
        """Filtered query returning EndpointInfo list."""
        conditions: list[str] = []
        params: list[str] = []

        if source is not None:
            conditions.append("source = ?")
            params.append(source)
        if status is not None:
            conditions.append("status = ?")
            params.append(status)
        if state is not None:
            conditions.append("state = ?")
            params.append(state)

        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM endpoints{where} ORDER BY source, path"

        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_endpoint(r) for r in rows]

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def update_state(self, source: str, path: str, state: str) -> None:
        """Update pipeline state for a single endpoint."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._conn.execute(
            "UPDATE endpoints SET state = ?, updated_at = ? "
            "WHERE source = ? AND path = ?",
            (state, now, source, path),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def count(
        self,
        *,
        source: str | None = None,
        state: str | None = None,
    ) -> int:
        """Count endpoints matching filters."""
        conditions: list[str] = []
        params: list[str] = []

        if source is not None:
            conditions.append("source = ?")
            params.append(source)
        if state is not None:
            conditions.append("state = ?")
            params.append(state)

        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        row = self._conn.execute(
            f"SELECT COUNT(*) FROM endpoints{where}", params
        ).fetchone()
        return row[0]

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------

    def _row_to_endpoint(self, row: sqlite3.Row) -> EndpointInfo:
        """Convert a DB row to EndpointInfo, deserializing JSON fields."""
        data: dict[str, Any] = dict(row)

        # Remove DB-only columns
        data.pop("id", None)
        data.pop("discovered_at", None)
        data.pop("updated_at", None)

        # Boolean conversion
        data["supports_history"] = bool(data.get("supports_history", 0))

        # JSON deserialization
        for field in _JSON_FIELDS:
            raw = data.get(field)
            if isinstance(raw, str):
                data[field] = json.loads(raw)

        return EndpointInfo(**data)

    def _endpoint_to_params(self, ep: EndpointInfo) -> dict[str, Any]:
        """Convert EndpointInfo to a dict suitable for SQL params."""
        data = ep.model_dump()

        # Boolean to int
        data["supports_history"] = int(data["supports_history"])

        # JSON serialization
        for field in _JSON_FIELDS:
            val = data.get(field)
            if not isinstance(val, str):
                data[field] = json.dumps(val, ensure_ascii=False)

        return data
