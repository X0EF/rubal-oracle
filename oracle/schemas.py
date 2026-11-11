from __future__ import annotations

from typing import Any


def _str(description: str) -> dict[str, Any]:
    return {"type": "string", "description": description}


def _schema(
    name: str, description: str, properties: dict[str, Any], required: list[str] | None = None
) -> dict[str, Any]:
    params: dict[str, Any] = {"type": "object", "properties": properties, "additionalProperties": False}
    if required:
        params["required"] = required
    return {"name": name, "description": description, "parameters": params}


ORACLE_COMMIT = _schema(
    "oracle_commit",
    "Save a commitment with a proof-based settler (git or calendar). Refuses if unsettled.",
    {
        "statement": _str("What you plan to do."),
        "deadline": _str("ISO8601 deadline."),
        "success_criteria": _str("Plain-language bar for success."),
        "settler": {"type": "string", "enum": ["git", "calendar"]},
        "repo": _str("Git repo path (git settler)."),
        "match": _str("Substring that must appear in commit subject (git)."),
        "event_match": _str("Substring for calendar event title."),
        "window_start": _str("Calendar window start (ISO8601)."),
        "window_end": _str("Calendar window end (ISO8601)."),
        "mode": _str("Calendar mode, default event_exists."),
        "tag": {
            "type": "string",
            "enum": ["feature", "bugfix", "docs", "meeting"],
            "description": "Task tag for similar past attempts (SPEC).",
        },
        "done_rule": {
            "type": "string",
            "enum": ["commit_match", "pr_merge", "paths", "test_pass"],
            "description": "Git proof rule at capture.",
        },
        "paths": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Paths touched (paths rule).",
        },
        "test_name": _str("Test id for test_pass rule."),
    },
    required=["statement", "deadline", "success_criteria", "settler"],
)

ORACLE_SETTLE = _schema(
    "oracle_settle",
    "Run settler after deadline: success, fail, or unresolved.",
    {"id": _str("Commitment id from oracle_commit.")},
    required=["id"],
)

ORACLE_REVISE = _schema(
    "oracle_revise",
    "Subtract: new success criteria while preserving original record.",
    {
        "id": _str("Commitment id."),
        "new_criteria": _str("Revised success criteria."),
        "match": _str("Optional new git match substring."),
    },
    required=["id", "new_criteria"],
)

ORACLE_STATUS = _schema(
    "oracle_status",
    "Open commitments and forecasts.",
    {"id": _str("Optional single commitment id.")},
)

ORACLE_MIRROR = _schema(
    "oracle_mirror",
    "Predicted vs settled outcomes; Brier only when numeric and resolved.",
    {},
)

ORACLE_EXTEND = _schema(
    "oracle_extend",
    "Move deadline on an open commitment (deadline missed phase).",
    {
        "id": _str("Commitment id."),
        "new_deadline": _str("ISO8601 new deadline."),
    },
    required=["id", "new_deadline"],
)

ORACLE_RESPOND_TRACK = _schema(
    "oracle_respond_track",
    "Accept or decline a pre_llm_call track offer (nothing saved until accept + settler).",
    {
        "offer_id": _str("Offer id from inject context."),
        "accept": {"type": "boolean"},
        "statement": _str("Required on accept."),
        "deadline": _str("Required on accept."),
        "success_criteria": _str("Required on accept."),
        "settler": {"type": "string", "enum": ["git", "calendar"]},
        "repo": _str("Git repo path."),
        "match": _str("Git match / PR pattern / test name."),
        "event_match": _str("Calendar title match."),
        "window_start": _str("Calendar window start."),
        "window_end": _str("Calendar window end."),
        "done_rule": {"type": "string"},
        "paths": {"type": "array", "items": {"type": "string"}},
        "test_name": _str("Named test for test_pass rule."),
        "tag": {"type": "string"},
    },
    required=["offer_id", "accept"],
)

ORACLE_BACKFILL = _schema(
    "oracle_backfill",
    "Propose Path A comparables from git history; confirm_ids to count in forecasts.",
    {
        "repo": _str("Git repo to scan."),
        "match": _str("Subject substring for similar attempts."),
        "tag": _str("Optional task tag."),
        "confirm_ids": {"type": "array", "items": {"type": "string"}},
    },
    required=["match"],
)
