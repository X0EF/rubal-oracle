"""Path A backfill: proposed comparables from git history (confirm to count)."""

from __future__ import annotations

from typing import Any


def merge_backfill_comparables(
    git: dict[str, Any],
    stored: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge fixture/live backfill rows with settled history; unconfirmed excluded from rate."""
    base = list(git.get("comparable") or [])
    seen = {row.get("id") for row in base if row.get("id")}
    for row in stored:
        if not row.get("confirmed", True):
            continue
        rid = row.get("id")
        if rid and rid in seen:
            continue
        base.append(row)
        if rid:
            seen.add(rid)
    for row in git.get("backfill_comparables") or []:
        if not row.get("confirmed", False):
            continue
        rid = row.get("id")
        if rid and rid in seen:
            continue
        base.append(row)
        if rid:
            seen.add(rid)
    return base


def backfill_from_git(git: dict[str, Any], *, match: str, tag: str | None = None) -> dict[str, Any]:
    """Propose comparables from commit subjects (live heuristic; user confirms in store)."""
    if not git.get("ok"):
        return {"ok": False, "code": "git_unavailable", "proposed": []}
    needle = match.lower()
    proposed: list[dict[str, Any]] = []
    n = 0
    for c in git.get("commits") or []:
        subj = (c.get("subject") or "").lower()
        if needle and needle not in subj:
            continue
        n += 1
        proposed.append(
            {
                "id": f"bf-{n}",
                "on_time": True,
                "confirmed": False,
                "source": "git_log_heuristic",
                "tag": tag,
            }
        )
    return {"ok": True, "proposed": proposed, "count": len(proposed)}
