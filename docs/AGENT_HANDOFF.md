# Agent handoff — repo done, you finish in Hermes

**Date:** 2026-11-11 (automated build pass)

## Repo status (agents)

| Check | Result |
|-------|--------|
| `./scripts/verify.sh` | 32 tests OK + doctor + **catalog validate** |
| `hermes plugins validate` (via catalog sync) | **Passed** (`.cursor`/ECC excluded — not in git) |
| Product code | `oracle/`, `plugin.yaml`, `__init__.py`, persistence, git+calendar sources |

**Not done by agents:** M1–M5 live Hermes, push, catalog PR, demo, Typeform.

## Your list only (≈30–60 min + record)

Follow **[OWNER_RUNBOOK.md](OWNER_RUNBOOK.md)** in order:

1. **M1** — Enable `rubal-oracle`, restart Hermes, doctor OK in UI/logs  
2. **M2** — `oracle_commit` ship goal → chat inject → restart → `/oracle status`  
3. **M3** — Calendar connect, `hackathon demo` event, calendar commitment, settle both  
4. **M4** — `git push` (when ready) → open catalog PR at pinned `git rev-parse HEAD`  
5. **M5** — &lt;90s screen record → X @NousResearch → Typeform  

**Catalog validate before push:** `./scripts/catalog_validate.sh` (already in `verify.sh`).

## If something fails

| Symptom | Doc |
|---------|-----|
| Desktop GPU quit | OWNER_RUNBOOK → troubleshoot |
| Local `hermes plugins validate` on full tree fails | ECC in `.cursor/` — use `catalog_validate.sh`, not raw validate on repo root |
| Outcome wording | settle returns `outcome` + `outcome_label` |

## Code added (kyuubi pass)

8 tools (`oracle_respond_track`, `oracle_backfill`), git done rules (PR/paths/test), track offers in inject, mirror stats. **39** fixture tests.

## Still thin (SPEC_GAP)

Live GitHub issue backfill, live pytest settler, leave-me-alone slash — see [SPEC_GAP.md](SPEC_GAP.md).
