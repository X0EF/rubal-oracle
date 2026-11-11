"""Fetch Google Calendar events via Hermes google-workspace skill script."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from oracle.calendar_cache import load_cached_events, merge_events, save_cached_events


def _hermes_home() -> Path:
    import os

    return Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))


def google_api_script() -> Path | None:
    candidates = [
        _hermes_home() / "hermes-agent/skills/productivity/google-workspace/scripts/google_api.py",
        Path.home() / ".hermes/hermes-agent/skills/productivity/google-workspace/scripts/google_api.py",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def _default_window() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=14)
    return now.isoformat(), end.isoformat()


def fetch_calendar_events(
    *, start: str | None = None, end: str | None = None
) -> tuple[list[dict[str, Any]], str | None]:
    script = google_api_script()
    if not script:
        return [], "google_workspace skill script not found"
    t0, t1 = _default_window()
    start = start or t0
    end = end or t1
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "calendar",
                "list",
                "--start",
                start,
                "--end",
                end,
                "--max",
                "50",
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], str(exc)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "calendar list failed").strip()[:500]
        return [], err
    try:
        raw = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], "calendar list returned non-JSON"
    if not isinstance(raw, list):
        return [], "unexpected calendar payload"
    events = [
        {"summary": e.get("summary", ""), "start": e.get("start", ""), "end": e.get("end", "")}
        for e in raw
        if isinstance(e, dict)
    ]
    return events, None


def ingest_calendar_from_text(text: str) -> list[dict[str, Any]]:
    """Parse JSON event arrays from terminal / tool output (agent ran calendar list)."""
    if not text:
        return []
    events: list[dict[str, Any]] = []
    for chunk in re.findall(r"\[[\s\S]*?\]", text):
        try:
            data = json.loads(chunk)
        except json.JSONDecodeError:
            continue
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
    if not force_refresh:
        cached = load_cached_events()
        if cached:
            return cached, None
    events, err = fetch_calendar_events()
    if events:
        merged = merge_events(load_cached_events(max_age=86400 * 7), events)
        save_cached_events(merged)
        return merged, None
    cached = load_cached_events(max_age=86400)
    if cached:
        return cached, err
    return [], err
