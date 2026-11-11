"""JITAI-style receptive checks (SPEC defaults)."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_receptive(
    *,
    now: str,
    store: Any,
    calendar_events: list[dict[str, Any]] | None = None,
    explicit: bool | None = None,
) -> bool:
    """Return whether a nudge may be shown. Tests may pass explicit=True/False."""
    if explicit is not None:
        return explicit

    leave_until = getattr(store, "leave_me_alone_until", None)
    if leave_until:
        try:
            if _parse_dt(now) < _parse_dt(leave_until):
                return False
        except ValueError:
            pass

    dismiss = getattr(store, "last_track_dismiss_at", None)
    if dismiss:
        try:
            delta = _parse_dt(now) - _parse_dt(dismiss)
            if delta.total_seconds() < 86400:
                return False
        except ValueError:
            pass

    try:
        t = _parse_dt(now)
        hour = t.hour
        if hour >= 22 or hour < 8:
            return False
    except ValueError:
        pass

    if calendar_events:
        for ev in calendar_events:
            start = ev.get("start")
            end = ev.get("end")
            if not start or not end:
                continue
            try:
                s, e = _parse_dt(start), _parse_dt(end)
                n = _parse_dt(now)
                if s <= n <= e:
                    return False
            except ValueError:
                continue

    return True
