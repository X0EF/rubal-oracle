---
name: oracle-build
description: Build or change rubal-oracle. Read SPEC, run verify.sh, match fixtures.
---

# Oracle build skill

**Orchestration (owner):** Subagents / `Task` and ECC roles are **allowed** for this repo — parallel planner, tdd-guide, code-reviewer, etc. when useful. Hermes live gates (M1–M5) still human per `docs/OWNER_RUNBOOK.md`.

1. **Source of truth:** `docs/SPEC.md`; backlog `docs/nice-to-haves.md`; phases `docs/PHASES.md`; done `docs/DONE.md`.
2. **Before claiming done:** `scripts/verify.sh` (39+ unit tests + doctor + catalog validate).
3. **Engine contract:** `tests/fixtures/cases.json` + `hackathon_use_case.json` — behavior must match, not just pass unrelated tests.
4. **Plugin:** root `plugin.yaml` + `__init__.py` `register(ctx)` → `oracle.engine`; no `pre_llm_call` block.
5. **No push / catalog PR / X** unless the owner asks.
6. **Before claiming “done” for the hackathon:** list unchecked **M1–M5** items and point the owner to `docs/OWNER_RUNBOOK.md` (agents do not pass Hermes live gates).
