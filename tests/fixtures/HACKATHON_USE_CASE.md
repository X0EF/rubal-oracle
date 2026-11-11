# Hackathon personal use case (fixtures)

**Goal:** Ship the Hermes plugin in `rubal-oracle` and **book + record** the &lt;90s X demo before **2026-11-11T23:00:00+01:00** (~39–42h from fixture clock).

Two commitments Oracle can track in MVP:

| # | Statement | Settler | Proof |
|---|-----------|---------|--------|
| 1 | Ship Oracle Hermes plugin (catalog-ready) | **git** | Commit on main, subject contains `plugin` |
| 2 | Block time and record demo for X | **calendar** | Event title contains `hackathon demo` in window |

**Not settled by Oracle in MVP:** posting the video on X (no settler). You still do it for the form; calendar only proves you **scheduled** recording time.

## Machine-readable sources

Full shape for adapters and manual testing: `hackathon_use_case.json`

- `meta` — repo path, remote, deadlines, human rules
- `source_catalog` — named bundles (`at_capture_*`, `at_settle_*`, `calendar_offline`)
- `cases` — eval scenarios merged into `tests.test_eval_cases`

### Git fields the engine uses (tests + future Hermes)

```json
{
  "ok": true,
  "repo": "/home/ostheperson/dev/oracle-rubal",
  "remote": "git@github.com:X0EF/rubal-oracle.git",
  "comparable": [{"id": "...", "on_time": true}],
  "commits": [{"date": "ISO8601", "subject": "feat: hermes plugin ..."}]
}
```

### Calendar fields

```json
{
  "ok": true,
  "provider": "google_workspace",
  "events": [{"summary": "...", "start": "ISO8601", "end": "ISO8601"}]
}
```

## Live checklist (your machine)

1. Connect **Google Calendar** in Hermes (not email-only).
2. Create event **“Hackathon demo screen record”** (or title containing `hackathon demo`).
3. Ship commits whose messages include **`plugin`** (e.g. `feat: hermes plugin package and register(ctx)`).
4. Screen-record Hermes + post X link separately for Typeform.

## Eval cases (ids)

- `capture-hackathon-ship-plugin` — first capture, no forecast %
- `capture-hackathon-ship-forecast` — seeded reference class + crowded calendar → 10%
- `capture-hackathon-demo-recording-slot`
- `refuse-hackathon-demo-calendar-offline`
- `settle-hackathon-ship-success` / `not-met` / `unreadable` (unresolved)
- `settle-hackathon-demo-slot-success` / `missing` (not met)
- `inject-hackathon-dual-open` — both commitments in context
- `slash-status-hackathon`
