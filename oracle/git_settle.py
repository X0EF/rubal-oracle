"""Git done-rule matching (SPEC: commit / PR / paths / test)."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def git_done_rule_satisfied(
    commitment: dict[str, Any],
    sources: dict[str, Any],
    deadline: str,
) -> bool:
    git = sources.get("git") or {}
    if not git.get("ok"):
        return False
    settler = commitment.get("settler") or {}
    rule = (settler.get("done_rule") or "commit_match").lower()
    deadline_dt = _parse_dt(deadline)
    needle = (settler.get("match") or "").lower()

    if rule in ("commit_match", "commit", ""):
        for c in git.get("commits") or []:
            subj = (c.get("subject") or "").lower()
            if needle and needle not in subj:
                continue
            when = c.get("date")
            if when and _parse_dt(when) > deadline_dt:
                continue
            return True
        return False

    if rule == "pr_merge":
        for pr in git.get("merged_prs") or []:
            title = (pr.get("title") or "").lower()
            branch = (pr.get("branch") or "").lower()
            if needle and needle not in title and needle not in branch:
                continue
            merged = pr.get("merged_at") or pr.get("date")
            if merged and _parse_dt(merged) > deadline_dt:
                continue
            return True
        return False

    if rule == "paths":
        want = [p for p in (settler.get("paths") or []) if p]
        if not want:
            return False
        for touch in git.get("path_touches") or []:
            when = touch.get("date")
            if when and _parse_dt(when) > deadline_dt:
                continue
            for p in touch.get("paths") or []:
                for w in want:
                    if p == w or p.startswith(f"{w}/") or w.startswith(f"{p}/"):
                        return True
        return False

    if rule == "test_pass":
        test_name = settler.get("test_name") or settler.get("match") or ""
        tests = git.get("tests") or {}
        if isinstance(tests, dict) and tests.get(test_name) == "pass":
            when = tests.get(f"{test_name}_at")
            if when and _parse_dt(when) > deadline_dt:
                return False
            return True
        return False

    return False
