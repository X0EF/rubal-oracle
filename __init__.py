"""rubal-oracle Hermes plugin — register(ctx) entry."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from oracle import engine, schemas
from oracle.persist import PersistedStore, load_store, save_store
from oracle.calendar_cache import merge_events, save_cached_events, load_cached_events
from oracle.calendar_fetch import ingest_calendar_from_text
from oracle.sources import build_sources, now_iso

_DEFAULT_REPO = str(Path(__file__).resolve().parent)

log = logging.getLogger(__name__)

_CTX: Any = None
_STORE: PersistedStore | None = None


def _store() -> PersistedStore:
    global _STORE
    if _STORE is None:
        _STORE = load_store()
    return _STORE


def _persist() -> None:
    save_store(_store())


def _sources_for_args(args: dict[str, Any], *, refresh_calendar: bool = False) -> dict[str, Any]:
    history = [c for c in _store().commitments if c.get("status") in ("success", "fail", "unresolved")]
    repo = args.get("repo") or _DEFAULT_REPO
    return build_sources(
        repo=repo,
        match=args.get("match"),
        settled_history=history,
        refresh_calendar=refresh_calendar,
        tag=args.get("tag"),
    )


def _json(result: Any) -> str:
    return json.dumps(result, indent=2)


def handle_commit(args: dict[str, Any], **_: Any) -> str:
    sources = _sources_for_args(args)
    result = engine.commit(args, sources=sources, store=_store(), now=now_iso())
    _persist()
    return _json(result)


def handle_settle(args: dict[str, Any], **_: Any) -> str:
    c = engine._find_commitment(_store(), args.get("id")) if args.get("id") else None
    repo = (c or {}).get("settler", {}).get("repo")
    match = (c or {}).get("settler", {}).get("match")
    sources = build_sources(
        repo=repo or _DEFAULT_REPO,
        match=match,
        settled_history=_store().commitments,
        refresh_calendar=True,
    )
    result = engine.settle(args, sources=sources, store=_store(), now=now_iso())
    _persist()
    return _json(result)


def handle_revise(args: dict[str, Any], **_: Any) -> str:
    result = engine.revise(args, store=_store(), now=now_iso())
    _persist()
    return _json(result)


def handle_mirror(_args: dict[str, Any], **_: Any) -> str:
    return _json(engine.mirror(_store()))


def handle_status(args: dict[str, Any], **_: Any) -> str:
    return _json(engine.oracle_status(_store(), now=now_iso(), commitment_id=args.get("id")))


def handle_extend(args: dict[str, Any], **_: Any) -> str:
    result = engine.extend_deadline(args, store=_store(), now=now_iso())
    _persist()
    return _json(result)


def handle_respond_track(args: dict[str, Any], **_: Any) -> str:
    sources = _sources_for_args(args)
    result = engine.respond_track(args, sources=sources, store=_store(), now=now_iso())
    _persist()
    return _json(result)


def handle_backfill(args: dict[str, Any], **_: Any) -> str:
    repo = args.get("repo") or _DEFAULT_REPO
    sources = build_sources(
        repo=repo,
        match=args.get("match"),
        settled_history=_store().commitments,
        refresh_calendar=False,
        tag=args.get("tag"),
    )
    result = engine.oracle_backfill(args, sources=sources, store=_store())
    _persist()
    return _json(result)


def _on_pre_llm_call(**kwargs: Any) -> dict[str, Any] | None:
    payload = {
        "user_message": kwargs.get("user_message", ""),
        "conversation_history": kwargs.get("conversation_history") or [],
        "is_first_turn": bool(kwargs.get("is_first_turn")),
        "session_id": kwargs.get("session_id", ""),
        "platform": kwargs.get("platform", "cli"),
    }
    return engine.pre_llm_call(payload, store=_store(), now=now_iso())


def _result_text(result: Any) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ("output", "stdout", "result", "content", "text"):
            val = result.get(key)
            if isinstance(val, str):
                return val
        return json.dumps(result)
    return str(result)


def _on_post_tool_call(tool_name: str, args: Any, result: Any, **kwargs: Any) -> None:
    if tool_name not in ("terminal", "shell_exec", "run_terminal"):
        return
    blob = _result_text(result)
    if "calendar" not in blob.lower() and not blob.strip().startswith("["):
        return
    ingested = ingest_calendar_from_text(blob)
    if not ingested:
        return
    merged = merge_events(load_cached_events(max_age=86400 * 7), ingested)
    save_cached_events(merged)
    log.debug("rubal-oracle: cached %d calendar events from tool output", len(merged))


def _slash_oracle(raw_args: str) -> str:
    sources = build_sources(repo=_DEFAULT_REPO, settled_history=_store().commitments)
    return engine.slash(raw_args or "status", store=_store(), sources=sources, now=now_iso())


def register(ctx) -> None:
    global _CTX, _STORE
    _CTX = ctx
    _STORE = load_store()

    tools = (
        ("oracle_commit", schemas.ORACLE_COMMIT, handle_commit),
        ("oracle_settle", schemas.ORACLE_SETTLE, handle_settle),
        ("oracle_revise", schemas.ORACLE_REVISE, handle_revise),
        ("oracle_status", schemas.ORACLE_STATUS, handle_status),
        ("oracle_mirror", schemas.ORACLE_MIRROR, handle_mirror),
        ("oracle_extend", schemas.ORACLE_EXTEND, handle_extend),
        ("oracle_respond_track", schemas.ORACLE_RESPOND_TRACK, handle_respond_track),
        ("oracle_backfill", schemas.ORACLE_BACKFILL, handle_backfill),
    )
    for name, schema, handler in tools:
        ctx.register_tool(
            name=name,
            toolset="rubal-oracle",
            schema=schema,
            handler=handler,
        )

    ctx.register_command(
        "oracle",
        _slash_oracle,
        description="Oracle commitments: status, extend, settle (see docs/SPEC.md)",
    )
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    log.info("rubal-oracle: registered %d tools", len(tools))
