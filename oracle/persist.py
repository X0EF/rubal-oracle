from __future__ import annotations

import json
import sqlite3
from typing import Any

from oracle.engine import MemoryStore

PLUGIN_ID = "rubal-oracle"
_STATE_KEY = "memory"


class PersistedStore(MemoryStore):
    def to_blob(self) -> dict[str, Any]:
        return {
            "commitments": self.commitments,
            "forecasts": self.forecasts,
            "backfill_comparables": list(self.backfill_comparables),
            "stats": dict(self.stats),
            "leave_me_alone_until": self.leave_me_alone_until,
            "last_track_dismiss_at": self.last_track_dismiss_at,
            "last_id": self.last_id,
            "seq": self._seq,
        }

    @classmethod
    def from_blob(cls, blob: dict[str, Any] | None) -> PersistedStore:
        store = cls()
        if not blob:
            return store
        store.commitments = list(blob.get("commitments") or [])
        store.forecasts = list(blob.get("forecasts") or [])
        store.backfill_comparables = list(blob.get("backfill_comparables") or [])
        store.stats = dict(blob.get("stats") or store.stats)
        store.leave_me_alone_until = blob.get("leave_me_alone_until")
        store.last_track_dismiss_at = blob.get("last_track_dismiss_at")
        store.last_id = blob.get("last_id")
        store._seq = int(blob.get("seq") or len(store.commitments))
        return store


def _conn():
    from plugins.plugin_storage import plugin_db

    return plugin_db(PLUGIN_ID)


def load_store() -> PersistedStore:
    try:
        conn = _conn()
    except Exception:
        return PersistedStore()
    try:
        row = conn.execute(
            "SELECT value FROM plugin_state WHERE key = ?", (_STATE_KEY,)
        ).fetchone()
    except sqlite3.OperationalError:
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS plugin_state (key TEXT PRIMARY KEY, value TEXT)"
            )
            conn.commit()
            row = None
        except Exception:
            return PersistedStore()
    if not row:
        return PersistedStore()
    try:
        blob = json.loads(row[0])
    except (TypeError, json.JSONDecodeError):
        return PersistedStore()
    return PersistedStore.from_blob(blob)


def save_store(store: PersistedStore) -> None:
    try:
        conn = _conn()
    except Exception:
        return
    payload = json.dumps(store.to_blob())
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS plugin_state (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute(
            "INSERT INTO plugin_state(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (_STATE_KEY, payload),
        )
        conn.commit()
    except Exception:
        pass
