---
name: oracle
description: >-
  Help users track follow-through on plans provable from git or Google Calendar.
  Load when the user wants to commit to a deadline, asks to be held accountable,
  mentions shipping by a date, or uses /oracle.
---

# Oracle (rubal-oracle)

Oracle tracks **commitments the user chooses**, checks outcomes from **git** or **Calendar** — not the user's word alone.

## When to use tools

| User intent | Tool |
|-------------|------|
| "Track … by Friday", "hold me to it", ships a feature by deadline | `oracle_commit` |
| "What's open?", list commitments | `oracle_status` or `/oracle status` |
| After deadline, close it out | `oracle_settle` with commitment `id` |
| Smaller scope | `oracle_revise` |
| Push deadline | `oracle_extend` or `/oracle extend <id> <iso>` |
| Prediction vs reality | `oracle_mirror` |
| User declined a track offer in inject | `oracle_respond_track` accept false |
| User said yes to a track offer | `oracle_respond_track` accept true + same fields as commit |

Load this skill at the start of a session about goals, deadlines, or accountability (`skill_view("rubal-oracle:oracle")`).

## Capture (git)

Ask for or infer: statement, deadline (ISO8601), success_criteria, `settler: git`, `repo` path, `match` substring in commit subject, optional `tag` (feature|bugfix|docs|meeting).

Example: *Ship search this week* → repo, match `search`, deadline Friday 18:00 local as ISO.

Refuses location/bank goals — explain: use git or Calendar proof only.

## Capture (calendar)

Needs Hermes **Google Calendar** connected. `settler: calendar`, `event_match`, `window_start`, `window_end`, `mode: event_exists`.

## Conversation-first

Users should not need a slash command. They talk; you call `oracle_commit`. Explain proof in one line:

- **Git** — local repo path; no extra plugin. Done = commit subject match, merged PR, paths, or named test.
- **Calendar** — Hermes **Google Calendar** plugin (Workspace Calendar). Email-only Google setup is not enough. Done = matching event exists in the window.

Never offer gym, bank, Gmail, or location. Inject may show open commitments and odds; never block the user's message. `/oracle help` is optional if they ask how it works.

## Outcomes (tell the user plainly)

- **Met** (success) — proof matched
- **Not met** (fail) — settler ran, bar not met
- **Couldn't verify** (unresolved) — source offline, not punishment

## Refusals

If commit refuses, read `how_to_make_saveable` and tell the user what to fix (connect Calendar, fix repo path).
