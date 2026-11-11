# Eval cases — inputs the system actually takes

Oracle is a **Hermes plugin**. The user talks in chat; the model (or `/oracle`) calls us. We do not parse free text as the primary API.

Clock in all fixtures: `2026-11-10T05:00:00+01:00`.

## Surfaces

| Surface | When | Payload |
|---|---|---|
| **Tool** | Model calls `oracle_*` | `args: dict` → JSON string `{"ok": ...}` |
| **Slash** | User types `/oracle ...` | `raw_args: str` → text |
| **`pre_llm_call`** | Every turn, before the model | `user_message`, `conversation_history`, `is_first_turn`, `session_id`, `platform` → `{"context": "..."}` or `None`. Never `{"action":"block"}`. |
| **`post_tool_call`** | After any tool | `tool_name`, `args`, `result` — observer; may refresh evidence |

Internal (same cases, faked in tests): **git log** of a named repo, **Calendar `events.list`** via the Hermes Google skill. Not email. Not `google_token.json`.

## Tools (agent-facing)

| Tool | Args | Typical ok | Typical fail |
|---|---|---|---|
| `oracle_commit` | `statement`, `deadline`, `success_criteria`, `settler` (`git`\|`calendar`), settler fields (`repo`, `match` / `event_match`, `window`) | commitment + forecast | `refused: true`, no row |
| `oracle_settle` | `id` | `success` / `fail` / `unresolved` | unknown id |
| `oracle_revise` | `id`, `new_criteria` | original preserved, revision open | — |
| `oracle_respond` | `id`, `accept`\|`dismiss` | subtract logged | no pending offer |
| `oracle_status` | optional `id` | open commitments + forecasts | — |
| `oracle_mirror` | none | resolved rows, Brier only if numeric+resolved | n too small → no calibration claim |

Slash `/oracle` is a thin wrapper over the same actions (`commit`, `settle`, `status`, `mirror`, `accept`, `dismiss`).

Machine-readable copies: `cases.json` + `hackathon_use_case.json` (personal ship + demo). Tests merge both.

Hackathon use case (sources + ids): [HACKATHON_USE_CASE.md](HACKATHON_USE_CASE.md).

**Settle outcomes in fixtures:** git readable, no matching commit → `fail`; git unreadable → `unresolved`; calendar `event_exists` with no event → `fail`.
