"""Calendar events from plugin cache (ingested via post_tool_call), not Hermes credential stores."""

from __future__ import annotations

import json
from json import JSONDecoder
from typing import Any

from oracle.calendar_cache import load_cached_events, merge_events, save_cached_events

_MAX_INGEST_CHARS = 200_000


def ingest_calendar_from_text(text: str) -> list[dict[str, Any]]:
    """Parse JSON event arrays from terminal / tool output (agent ran calendar list)."""
    if not text:
        return []
    snippet = text if len(text) <= _MAX_INGEST_CHARS else text[:_MAX_INGEST_CHARS]
    events: list[dict[str, Any]] = []
    decoder = JSONDecoder()
    idx = 0
    while idx < len(snippet):
        start = snippet.find("[", idx)
        if start < 0:
            break
        try:
            data, end = decoder.raw_decode(snippet, start)
        except json.JSONDecodeError:
            idx = start + 1
            continue
        idx = end
        if not isinstance(data, list):
            continue
        for item in data:
            if isinstance(item, dict) and item.get("summary") is not None:
                events.append(
                    {
                        "summary": item.get("summary", ""),
                        "start": item.get("start", ""),
                        "end": item.get("end", ""),
                    }
                )
    return events


def resolve_calendar_events(*, force_refresh: bool = False) -> tuple[list[dict[str, Any]], str | None]:
    """Return cached events only; refresh happens when the agent runs calendar tools."""
    del force_refresh  # retained for API compatibility; no plugin-driven Google calls
    max_age = 86400 * 7
    cached = load_cached_events(max_age=max_age)
    if cached:
        return cached, None
    return (
        [],
        "no cached calendar events — ask the agent to list calendar (google-workspace skill)",
    )