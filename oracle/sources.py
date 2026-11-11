"""Build `sources` dicts for oracle.engine from live git / Hermes calendar availability."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from oracle.calendar_fetch import resolve_calendar_events


def _hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))


def calendar_connected() -> bool:
    """Heuristic: Google workspace token present (do not read secrets)."""
    for name in ("google_token.json", "gws_token.json", "google_workspace_token.json"):
        if (_hermes_home() / name).exists():
            return True
    auth = _hermes_home() / "auth.json"
    if auth.exists():
        try:
            data = json.loads(auth.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("google"):
                return True
        except (OSError, json.JSONDecodeError):
            pass
    return False


def git_log_commits(repo: str, *, limit: int = 50) -> list[dict[str, Any]]:
    repo_path = Path(repo).expanduser()
    if not repo_path.is_dir():
        return []
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(repo_path),
                "log",
                f"-{limit}",
                "--format=%aI\t%s",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    commits: list[dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        if "\t" not in line:
            continue
        date_s, subject = line.split("\t", 1)
        commits.append({"date": date_s, "subject": subject})
    return commits


def comparable_from_history(
    settled_rows: list[dict[str, Any]],
    *,
    match: str,
    settler_kind: str,
    tag: str | None = None,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    needle = match.lower()
    for row in settled_rows:
        st = row.get("settler") or {}
        if st.get("kind") != settler_kind:
            continue
        if tag and row.get("tag") != tag:
            continue
        if needle and needle not in (st.get("match") or "").lower():
            continue
        out.append(
            {
                "id": row.get("id"),
                "on_time": row.get("status") == "success",
            }
        )
    return out[-12:]


def build_sources(
    *,
    repo: str | None = None,
    match: str | None = None,
    settled_history: list[dict[str, Any]] | None = None,
    calendar_events: list[dict[str, Any]] | None = None,
    refresh_calendar: bool = False,
    tag: str | None = None,
) -> dict[str, Any]:
    git: dict[str, Any] = {"ok": False}
    if repo:
        repo_path = Path(repo).expanduser()
        git["repo"] = str(repo_path)
        git["ok"] = repo_path.is_dir() and (repo_path / ".git").exists()
        if git["ok"]:
            git["commits"] = git_log_commits(str(repo_path))
            hist = settled_history or []
            if match:
                git["comparable"] = comparable_from_history(
                    hist, match=match, settler_kind="git", tag=tag
                )

    cal_ok = calendar_connected()
    events = list(calendar_events) if calendar_events is not None else []
    fetch_err: str | None = None
    if cal_ok and calendar_events is None:
        fetched, fetch_err = resolve_calendar_events(force_refresh=refresh_calendar)
        if fetched:
            events = fetched
    calendar: dict[str, Any] = {"ok": cal_ok, "events": events}
    if not cal_ok:
        calendar["reason"] = "google calendar not connected"
    elif fetch_err and not events:
        calendar["fetch_error"] = fetch_err

    return {"git": git, "calendar": calendar}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()
