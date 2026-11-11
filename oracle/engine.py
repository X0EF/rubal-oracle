"""Domain API the fixtures exercise."""

from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Any

from oracle.backfill import backfill_from_git, merge_backfill_comparables
from oracle.git_settle import git_done_rule_satisfied
from oracle.receptive import is_receptive
from oracle.user_copy import (
    EMPTY_STORE_STATUS,
    FIRST_TURN_ONBOARDING,
    HELP_INJECT,
    TRACK_OFFER_USER,
    USER_HELP,
)

_TRACK_OFFER_RE = re.compile(
    r"\b(i will|i'll|this week|by (monday|tuesday|wednesday|thursday|friday|saturday|sunday)|ship .+ (by|before))\b",
    re.IGNORECASE,
)


class MemoryStore:
    def __init__(self) -> None:
        self.commitments: list[dict[str, Any]] = []
        self.forecasts: list[dict[str, Any]] = []
        self.backfill_comparables: list[dict[str, Any]] = []
        self.stats: dict[str, int] = {
            "track_offers_made": 0,
            "track_offers_declined": 0,
            "subtract_offers": 0,
            "subtract_declined": 0,
        }
        self.leave_me_alone_until: str | None = None
        self.last_track_dismiss_at: str | None = None
        self.onboarding_sessions: list[str] = []
        self.last_id: str | None = None
        self._seq = 0

    def new_id(self) -> str:
        self._seq += 1
        cid = f"c{self._seq}"
        self.last_id = cid
        return cid


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _find_commitment(store: MemoryStore, cid: str) -> dict[str, Any] | None:
    for c in store.commitments:
        if c["id"] == cid:
            return c
    return None


_SETTLED_STATUSES = frozenset({"success", "fail", "unresolved"})
_OUTCOME_LABELS: dict[str, str] = {
    "success": "met",
    "fail": "not met",
    "unresolved": "couldn't verify",
}


def _outcome_label(status: str) -> str | None:
    return _OUTCOME_LABELS.get(status)


def _commitment_with_status_label(c: dict[str, Any]) -> dict[str, Any]:
    row = dict(c)
    label = _outcome_label(c.get("status", ""))
    if label is not None:
        row["status_label"] = label
    return row


def _forecast(
    args: dict[str, Any],
    sources: dict[str, Any],
    store: MemoryStore | None = None,
    *,
    min_class_n: int = 3,
) -> dict[str, Any]:
    git = dict(sources.get("git") or {})
    comparable = merge_backfill_comparables(
        git, (store.backfill_comparables if store else [])
    )
    n = len(comparable)
    if n < min_class_n:
        return {
            "probability": None,
            "uncertainty": "insufficient_reference_class",
            "comparisons": comparable,
            "reasons": [],
        }
    successes = sum(1 for row in comparable if row.get("on_time"))
    p = successes / n
    reasons = [f"{successes} of {n} similar past attempts on time"]
    events = (sources.get("calendar") or {}).get("events") or []
    if len(events) >= 4:
        p -= 0.15
        reasons.append("calendar crowded this week")
    p = max(0.05, min(0.95, p))
    return {
        "probability": round(p, 2) if p != int(p) or True else p,
        "uncertainty": "ok",
        "comparisons": comparable,
        "reasons": reasons,
    }


def _path_b_evidence(sources: dict[str, Any]) -> list[str]:
    """Path B (SPEC): no % yet — describe this week's evidence."""
    hints: list[str] = []
    events = (sources.get("calendar") or {}).get("events") or []
    if events:
        hints.append(f"{len(events)} calendar events this window")
    git = sources.get("git") or {}
    commits = git.get("commits") or []
    if git.get("ok") and not commits:
        hints.append("no commits on this repo since tracking started")
    elif git.get("ok") and commits:
        hints.append(f"{len(commits)} recent commits in repo")
    if hints:
        hints.insert(0, "not enough history yet")
    return hints


def _refuse(code: str, *, how: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {
        "ok": False,
        "refused": True,
        "code": code,
        "saved": False,
    }
    if how:
        out["how_to_make_saveable"] = how
    return out


def commit(
    args: dict[str, Any],
    *,
    sources: dict[str, Any],
    store: MemoryStore,
    now: str,
) -> dict[str, Any]:
    settler = args.get("settler")
    if settler in ("location", "bank"):
        how = (
            "Oracle MVP settles from git or Google Calendar. "
            "Try a git-ship goal or a calendar event you can verify."
        )
        if settler == "location":
            how += " A calendar block alone does not prove gym visits."
        return _refuse("no_settler", how=how)

    if settler == "calendar":
        cal = sources.get("calendar") or {}
        if not cal.get("ok"):
            reason = cal.get("reason") or "calendar not connected"
            return _refuse(
                "settler_offline",
                how=f"Connect Hermes Google Workspace Calendar. ({reason})",
            )

    if settler == "git":
        git = sources.get("git") or {}
        if not git.get("ok"):
            return _refuse(
                "settler_offline",
                how="Point Oracle at a reachable git repo for this commitment.",
            )

    cid = store.new_id()
    tag = args.get("tag")
    if tag and tag not in ("feature", "bugfix", "docs", "meeting"):
        tag = None
    row = {
        "id": cid,
        "statement": args.get("statement", ""),
        "deadline": args.get("deadline", ""),
        "success_criteria": args.get("success_criteria", ""),
        "status": "open",
        "settler": _settler_payload(args),
        "tag": tag,
        "created_at": now,
    }
    store.commitments.append(row)

    fc = _forecast(args, sources, store)
    if fc.get("uncertainty") == "insufficient_reference_class":
        week = _path_b_evidence(sources)
        if week:
            fc["reasons"] = week
    fc["commitment_id"] = cid
    fc["at"] = now
    store.forecasts.append(fc)

    return {"ok": True, "refused": False, "commitment": row, "forecast": fc}


def _settler_payload(args: dict[str, Any]) -> dict[str, Any]:
    kind = args.get("settler")
    base: dict[str, Any] = {"kind": kind}
    if kind == "git":
        base["repo"] = args.get("repo")
        base["match"] = args.get("match")
        base["done_rule"] = (args.get("done_rule") or "commit_match").lower()
        if args.get("paths"):
            base["paths"] = list(args["paths"])
        if args.get("test_name"):
            base["test_name"] = args["test_name"]
    if kind == "calendar":
        base["event_match"] = args.get("event_match")
        base["window_start"] = args.get("window_start")
        base["window_end"] = args.get("window_end")
        base["mode"] = args.get("mode", "event_exists")
    return base


def _calendar_matches(commitment: dict[str, Any], sources: dict[str, Any]) -> bool:
    cal = sources.get("calendar") or {}
    if not cal.get("ok"):
        return False
    settler = commitment.get("settler") or {}
    needle = (settler.get("event_match") or "").lower()
    win_start = settler.get("window_start")
    win_end = settler.get("window_end")
    if not needle:
        return False
    for ev in cal.get("events") or []:
        title = (ev.get("summary") or "").lower()
        if needle not in title:
            continue
        if win_start and win_end:
            start = ev.get("start") or ""
            if start:
                t = _parse_dt(start)
                if t < _parse_dt(win_start) or t > _parse_dt(win_end):
                    continue
        return True
    return False


def settle(
    args: dict[str, Any],
    *,
    sources: dict[str, Any],
    store: MemoryStore,
    now: str,
) -> dict[str, Any]:
    cid = args.get("id")
    c = _find_commitment(store, cid) if cid else None
    if not c:
        return {"ok": False, "code": "unknown_id"}

    kind = (c.get("settler") or {}).get("kind")
    outcome: str

    if kind == "git":
        git = sources.get("git") or {}
        if not git.get("ok"):
            outcome = "unresolved"
        elif git_done_rule_satisfied(c, sources, c["deadline"]):
            outcome = "success"
        else:
            outcome = "fail"

    elif kind == "calendar":
        cal = sources.get("calendar") or {}
        if not cal.get("ok"):
            outcome = "unresolved"
        elif _calendar_matches(c, sources):
            outcome = "success"
        else:
            mode = (c.get("settler") or {}).get("mode", "event_exists")
            if mode == "event_exists":
                outcome = "fail"
            else:
                outcome = "unresolved"
    else:
        outcome = "unresolved"

    c["status"] = outcome
    c["settled_at"] = now
    return {
        "ok": True,
        "outcome": outcome,
        "outcome_label": _outcome_label(outcome),
        "commitment": _commitment_with_status_label(c),
    }


def revise(
    args: dict[str, Any],
    *,
    store: MemoryStore,
    now: str,
) -> dict[str, Any]:
    cid = args.get("id")
    original = _find_commitment(store, cid) if cid else None
    if not original:
        return {"ok": False, "code": "unknown_id"}

    original["status"] = "superseded"

    new_id = store.new_id()
    revision = {
        "id": new_id,
        "original_id": cid,
        "statement": original.get("statement", ""),
        "deadline": original.get("deadline", ""),
        "success_criteria": args.get("new_criteria", original.get("success_criteria")),
        "status": "open",
        "settler": dict(original.get("settler") or {}),
        "created_at": now,
    }
    if args.get("match"):
        revision["settler"]["match"] = args["match"]
    store.commitments.append(revision)
    return {"ok": True, "original": original, "revision": revision}


def _open_commitments(store: MemoryStore, now: str) -> list[dict[str, Any]]:
    now_dt = _parse_dt(now)
    open_rows = [c for c in store.commitments if c.get("status") == "open"]
    for c in open_rows:
        if c.get("deadline") and _parse_dt(c["deadline"]) < now_dt:
            c["_phase"] = "deadline_missed"
        else:
            c["_phase"] = "active"
    return open_rows


def extend_deadline(
    args: dict[str, Any],
    *,
    store: MemoryStore,
    now: str,
) -> dict[str, Any]:
    cid = args.get("id")
    c = _find_commitment(store, cid) if cid else None
    if not c or c.get("status") != "open":
        return {"ok": False, "code": "unknown_id"}
    new_dl = args.get("new_deadline")
    if not new_dl:
        return {"ok": False, "code": "missing_deadline"}
    c["deadline"] = new_dl
    c["extended_at"] = now
    c.pop("_phase", None)
    return {"ok": True, "commitment": c}


def _latest_forecast(store: MemoryStore, commitment_id: str) -> dict[str, Any] | None:
    for fc in reversed(store.forecasts):
        if fc.get("commitment_id") == commitment_id:
            return fc
    return None


def mirror(store: MemoryStore) -> dict[str, Any]:
    pairs: list[tuple[float, float]] = []
    for c in store.commitments:
        if c.get("status") not in ("success", "fail"):
            continue
        fc = _latest_forecast(store, c["id"])
        p = fc.get("probability") if fc else None
        if p is None:
            continue
        outcome_val = 1.0 if c["status"] == "success" else 0.0
        pairs.append((float(p), outcome_val))

    n = len(pairs)
    brier = None
    if n:
        brier = sum((p - o) ** 2 for p, o in pairs) / n

    stats = getattr(store, "stats", {}) or {}
    return {
        "ok": True,
        "n_resolved_numeric": n,
        "brier": brier,
        "claims_calibration": False if n < 3 else False,
        "track_offers_made": int(stats.get("track_offers_made", 0)),
        "track_offers_declined": int(stats.get("track_offers_declined", 0)),
        "subtract_offers": int(stats.get("subtract_offers", 0)),
        "subtract_declined": int(stats.get("subtract_declined", 0)),
    }


def status_text(store: MemoryStore, *, now: str) -> str:
    lines: list[str] = []
    for c in _open_commitments(store, now):
        fc = _latest_forecast(store, c["id"])
        prob = fc.get("probability") if fc else None
        unc = (fc or {}).get("uncertainty", "")
        phase = c.get("_phase", "active")
        stmt = c.get("statement", "")
        st = c.get("status", "open")
        if prob is not None:
            lines.append(f"{stmt}: {st}, forecast {prob:.0%}")
        elif unc == "insufficient_reference_class":
            lines.append(f"{stmt}: {st}, insufficient reference class")
        else:
            lines.append(f"{stmt}: {st}")
        if phase == "deadline_missed":
            lines.append(
                f"  The deadline passed for \"{stmt}\". You can extend, revise, or settle."
            )
    settled = [
        c for c in store.commitments if c.get("status") in _SETTLED_STATUSES
    ]
    for c in settled:
        stmt = c.get("statement", "")
        label = _outcome_label(c["status"])
        lines.append(f"{stmt}: {label}")
    if not lines:
        return EMPTY_STORE_STATUS
    return "\n".join(lines)


def oracle_status(store: MemoryStore, *, now: str, commitment_id: str | None = None) -> dict[str, Any]:
    text = status_text(store, now=now)
    open_rows = _open_commitments(store, now)
    settled_rows = [
        _commitment_with_status_label(c)
        for c in store.commitments
        if c.get("status") in _SETTLED_STATUSES
    ]
    if commitment_id:
        open_rows = [c for c in open_rows if c.get("id") == commitment_id]
        settled_rows = [c for c in settled_rows if c.get("id") == commitment_id]
    return {"ok": True, "summary": text, "open": open_rows, "settled": settled_rows}


def user_help() -> str:
    return USER_HELP


def _first_turn_onboarding(payload: dict[str, Any], store: MemoryStore) -> str | None:
    if not payload.get("is_first_turn"):
        return None
    if store.commitments:
        return None
    sid = str(payload.get("session_id") or "")
    if sid and sid in store.onboarding_sessions:
        return None
    if sid:
        store.onboarding_sessions.append(sid)
    return FIRST_TURN_ONBOARDING


def _slash_tokens(raw_args: str) -> list[str]:
    tokens = [t.lstrip("/").lower() for t in raw_args.strip().split() if t]
    if tokens and tokens[0] == "oracle":
        tokens = tokens[1:]
    return tokens


def _help_request(message: str) -> bool:
    text = (message or "").strip().lower()
    if not text:
        return False
    if "/oracle help" in text or text in ("help", "/help", "?", "oracle help"):
        return True
    return bool(re.search(r"\bhow (do i|does|to) (use |does )?oracle\b", text))


def slash(raw_args: str, *, store: MemoryStore, sources: dict[str, Any], now: str) -> str:
    parts = _slash_tokens(raw_args)
    cmd = parts[0] if parts else "status"
    if cmd in ("help", "?", "h") or "help" in parts:
        return user_help()
    if cmd == "status":
        return status_text(store, now=now)
    if cmd == "extend" and len(parts) >= 3:
        cid = parts[1]
        new_dl = parts[2]
        res = extend_deadline({"id": cid, "new_deadline": new_dl}, store=store, now=now)
        return json_ok(res) if res.get("ok") else f"Could not extend: {res.get('code')}"
    if cmd == "settle" and len(parts) >= 2:
        res = settle({"id": parts[1]}, sources=sources, store=store, now=now)
        return json_ok(res)
    return status_text(store, now=now)


def json_ok(obj: dict[str, Any]) -> str:
    import json

    return json.dumps(obj, indent=2)


def _track_offer_context(message: str, store: MemoryStore) -> str | None:
    text = (message or "").strip()
    if len(text) < 24 or not _TRACK_OFFER_RE.search(text):
        return None
    store.stats["track_offers_made"] = int(store.stats.get("track_offers_made", 0)) + 1
    offer_id = f"off-{uuid.uuid4().hex[:8]}"
    return (
        f"[Oracle track offer {offer_id}] {TRACK_OFFER_USER} "
        "If they agree, gather what/how/deadline then oracle_commit. "
        f'If they decline: oracle_respond_track offer_id="{offer_id}" accept false.'
    )


def respond_track(
    args: dict[str, Any],
    *,
    sources: dict[str, Any],
    store: MemoryStore,
    now: str,
) -> dict[str, Any]:
    if not args.get("accept", False):
        store.stats["track_offers_declined"] = int(
            store.stats.get("track_offers_declined", 0)
        ) + 1
        store.last_track_dismiss_at = now
        return {"ok": True, "saved": False, "declined": True}
    commit_args = {k: v for k, v in args.items() if k not in ("offer_id", "accept")}
    commit_args.setdefault("settler", args.get("settler"))
    if not commit_args.get("settler"):
        return {
            "ok": False,
            "code": "missing_settler",
            "saved": False,
            "how_to_make_saveable": "accept requires settler + proof fields like oracle_commit.",
        }
    return commit(commit_args, sources=sources, store=store, now=now)


def oracle_backfill(
    args: dict[str, Any],
    *,
    sources: dict[str, Any],
    store: MemoryStore,
) -> dict[str, Any]:
    git = sources.get("git") or {}
    match = args.get("match") or ""
    result = backfill_from_git(git, match=match, tag=args.get("tag"))
    if not result.get("ok"):
        return result
    proposed = result.get("proposed") or []
    if args.get("confirm_ids"):
        confirmed = set(args["confirm_ids"])
        added = 0
        for row in proposed:
            if row.get("id") in confirmed:
                store.backfill_comparables.append({**row, "confirmed": True})
                added += 1
        return {"ok": True, "confirmed_count": added, "proposed": proposed}
    return {"ok": True, "proposed": proposed, "count": len(proposed)}


def pre_llm_call(
    payload: dict[str, Any],
    *,
    store: MemoryStore,
    now: str,
    slipping: bool = False,
    decision_point: bool = False,
    receptive: bool | None = True,
) -> dict[str, Any] | None:
    chunks: list[str] = []
    user_message = payload.get("user_message") or ""
    if _help_request(user_message):
        chunks.append(HELP_INJECT)
    hint = _first_turn_onboarding(payload, store)
    if hint:
        chunks.append(hint)
    offer = _track_offer_context(user_message, store)
    if offer:
        chunks.append(offer)

    open_rows = _open_commitments(store, now)
    if open_rows:
        chunks.append("[Oracle commitments]")
        for c in open_rows:
            fc = _latest_forecast(store, c["id"])
            stmt = c.get("statement", "")
            if fc and fc.get("probability") is not None:
                p = fc["probability"]
                chunks.append(f"- {stmt}: open, ~{p} ({p:.0%}) chance by deadline")
            else:
                chunks.append(f"- {stmt}: open")
            if c.get("_phase") == "deadline_missed":
                chunks.append(
                    f'  Deadline passed for "{stmt}" — offer extend, smaller goal, or settle.'
                )

    events = ((payload.get("sources") or {}).get("calendar") or {}).get("events")
    if events is None:
        events = []
    rec = is_receptive(now=now, store=store, calendar_events=events, explicit=receptive)
    if slipping and decision_point and rec:
        store.stats["subtract_offers"] = int(store.stats.get("subtract_offers", 0)) + 1
        chunks.append(
            "User may be slipping; if helpful, suggest subtract (smaller scope)."
        )
    elif slipping and decision_point and not rec:
        store.stats["subtract_declined"] = int(store.stats.get("subtract_declined", 0)) + 1

    if not chunks:
        return {"context": None}

    return {"context": "\n".join(chunks)}
