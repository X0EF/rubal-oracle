"""Persist calendar events between tool calls (Desktop optional)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

CACHE_FILE = "calendar_events_cache.json"
TTL_SECONDS = 900


def _cache_path() -> Path | None:
    try:
        from plugins.plugin_storage import plugin_data_dir

        return plugin_data_dir("rubal-oracle") / CACHE_FILE
    except Exception:
        return None


def load_cached_events(*, max_age: int = TTL_SECONDS) -> list[dict[str, Any]]:
    path = _cache_path()
    if not path or not path.exists():
        return []
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if time.time() - float(blob.get("fetched_at", 0)) > max_age:
        return []
    events = blob.get("events")
    return list(events) if isinstance(events, list) else []


def save_cached_events(events: list[dict[str, Any]]) -> None:
    path = _cache_path()
    if not path:
        return
    payload = {"fetched_at": time.time(), "events": events}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError:
        pass


def merge_events(
    existing: list[dict[str, Any]], incoming: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    for ev in existing + incoming:
        if not isinstance(ev, dict):
            continue
        key = str(ev.get("id") or f"{ev.get('summary','')}@{ev.get('start','')}")
        by_key[key] = {
            "summary": ev.get("summary", ""),
            "start": ev.get("start", ""),
            "end": ev.get("end", ""),
        }
    return sorted(by_key.values(), key=lambda e: e.get("start") or "")
