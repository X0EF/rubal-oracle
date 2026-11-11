# Project checklist — end-to-end with milestone gates

One path from zero → hackathon submit. **Do not tick a phase complete until its milestone gate passes.**  
Spec: [SPEC.md](SPEC.md) · drift: [SPEC_GAP.md](SPEC_GAP.md) · phases map: [PHASES.md](PHASES.md).

**Current phase (update by hand):** **Repo ready (M0 + catalog validate) → you: M1–M5 in Hermes** ([OWNER_RUNBOOK.md](OWNER_RUNBOOK.md))

---

## How to read this doc

| Column | Meaning |
|--------|---------|
| **Tasks** | Checkboxes — do the work |
| **Milestone gate** | **All** bullets must pass before you call the phase **done** |
| **Verify** | Commands / observations — copy-paste where possible |

---

## M0 — Foundation (intent + contracts)

**Goal:** Behavior is written down and enforced by tests before Hermes wiring.

### Tasks

- [x] [SPEC.md](SPEC.md) + [HACKATHON_USE_CASE.md](../tests/fixtures/HACKATHON_USE_CASE.md)
- [x] Fixtures: `cases.json` + `hackathon_use_case.json`
- [x] `oracle/engine.py` implements fixture contract
- [x] Root `plugin.yaml` + `__init__.py` `register(ctx)` (may fail doctor until paths fixed — fixed in M0 verify)

### Milestone gate — M0 is **done** when:

1. `./scripts/verify.sh` exits **0**
2. Output includes **`Ran 39 tests`** (or higher) and **`OK`**
3. Output includes **`hermes plugins doctor`** → **`registrations: 8 tool(s), 2 hook(s)`**

### Verify

```bash
cd /home/ostheperson/dev/oracle-rubal
./scripts/verify.sh
```

---

## M1 — Plugin package (Hermes can load it)

**Goal:** Hermes discovers the plugin from this repo; no chat yet required.

### Tasks

- [x] Six tools + `/oracle` + hooks declared in `plugin.yaml`
- [ ] Plugin **enabled** in your Hermes profile (dev install — see verify)
- [ ] Hermes restarted after enable (Desktop or CLI)

### Milestone gate — M1 is **done** when:

1. `hermes plugins doctor /home/ostheperson/dev/oracle-rubal --ci` → **OK**
2. `hermes plugins list` (or Desktop → Plugins) shows **`rubal-oracle`** **enabled**
3. No import/registration error in `~/.hermes/logs/agent.log` on startup (grep `rubal-oracle`)

### Verify

```bash
# Option A — develop from repo (typical)
hermes plugins doctor "$(pwd)" --ci   # run from repo root

# Option B — after install into ~/.hermes/plugins/rubal-oracle
hermes plugins doctor rubal-oracle --ci
hermes plugins list | rg -i rubal
```

---

## M2 — Live smoke (plugin + backend + persistence)

**Goal:** One real capture → inject → survive restart. Uses **your** Hermes session, not only unit tests.

### Tasks

- [ ] Capture hackathon **ship** commitment (git settler, `match: plugin`) via tool or `/oracle`
- [ ] `/oracle status` shows it **open**
- [ ] New chat turn: Oracle context appears (open commitment / odds / Path B text)
- [ ] Quit Hermes fully → reopen → **same** commitment still **open**
- [ ] Optional: `oracle_settle` on a test id in a scratch repo — outcome matches SPEC

### Milestone gate — M2 is **done** when:

1. **Capture:** `oracle_commit` returns `"ok": true`, `"saved": true`, commitment `id` present
2. **Inject:** Next model turn’s context (or tool trace) mentions the **statement** you saved
3. **Persist:** After Hermes restart, `/oracle status` still lists that commitment (same `id` or same statement + still open)
4. **No block:** Never `action: block` from Oracle on `pre_llm_call`

### Verify (example tool args — adjust paths)

Ask the agent in Hermes to call **`oracle_commit`** with:

- `statement`: Ship Oracle Hermes plugin before hackathon deadline  
- `deadline`: `2026-11-11T23:00:00+01:00`  
- `success_criteria`: commit on main whose subject contains `plugin`  
- `settler`: `git`  
- `repo`: `/home/ostheperson/dev/oracle-rubal`  
- `match`: `plugin`  
- `tag`: `feature`

Then:

```text
/oracle status
```

Restart Hermes → `/oracle status` again (must still show open).

---

## M3 — Live settlers (git + calendar for **your** hackathon case)

**Goal:** Real data feeds forecasts/settle; demo story is honest.

### Tasks

- [ ] Google Calendar connected (Hermes GWS — **not** email-only)
- [ ] Calendar event title contains **`hackathon demo`**
- [ ] Capture **demo recording** calendar commitment ([HACKATHON_USE_CASE.md](../tests/fixtures/HACKATHON_USE_CASE.md))
- [ ] Git commit with **`plugin`** in subject when codebase is catalog-ready
- [ ] `oracle_settle` on both commitments after deadline (or dry-run before with test clock)

### Milestone gate — M3 is **done** when:

1. **Calendar live:** `calendar_connected()` true — event visible to Oracle (capture calendar commitment **not refused**)
2. **Git live:** Ship commitment settles **success** after matching commit, or **fail** if readable repo + no match (not stuck **unresolved** when repo OK)
3. **Calendar settle:** Event exists → **success**; no event after window → **fail** (`not met`)
4. **Forecast:** Either a **%** with named comparables **or** “not enough history” + Path B reasons (no invented %)

### Verify

```bash
# Calendar skill (if installed) — should return JSON events, not auth error
python3 ~/.hermes/hermes-agent/skills/productivity/google-workspace/scripts/google_api.py \
  calendar list --start 2026-11-10T00:00:00+01:00 --end 2026-11-12T00:00:00+01:00 | head

git -C /home/ostheperson/dev/oracle-rubal log -1 --oneline
```

In Hermes: `oracle_settle` with each commitment `id` after deadline rules in SPEC.

---

## M4 — Catalog-ready (hackathon admission)

**Goal:** Upstream Hermes catalog CI accepts the plugin at a pinned SHA.

### Tasks

- [ ] Repo pushed; default branch has plugin + docs
- [ ] `hermes plugins validate` on **pinned commit** (catalog rules)
- [ ] Catalog entry PR prepared ([Hermes catalog guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission))
- [ ] `docs/design-rationale.md` if catalog copy cites research (working agreement)

### Milestone gate — M4 is **done** when:

1. **`scripts/catalog_validate.sh`** (or `hermes plugins validate` on installed id) exits **0** at the **same commit** you pin in the PR
2. PR contains: `plugin.yaml`, `register`, repo URL, **pinned SHA**, author metadata
3. Fresh clone + doctor on that SHA → **OK** (optional but strong)

### Verify

```bash
git rev-parse HEAD    # pin this in catalog PR
scripts/catalog_validate.sh   # rsync w/o .cursor/.git/caches → hermes plugins validate
# or installed id after upstream layout:
hermes plugins validate rubal-oracle
```

---

## M5 — Submitted (owner actions)

**Goal:** Judges have PR + video + form entry.

### Tasks

- [ ] Catalog **PR open** (link saved)
- [ ] **&lt;90s** screen demo: commit → forecast → inject → settle/mirror (git + calendar beats)
- [ ] Video posted on **X**, tag **@NousResearch**
- [ ] [Typeform](https://form.typeform.com/to/FwJLvOln): PR URL + video URL
- [ ] Before **2026-11-11 23:00 Africa/Lagos**

### Milestone gate — M5 is **done** when:

1. PR URL loads and points at pinned commit with plugin sources
2. Video **&lt; 90s**, shows **tools or hooks** (not prompt-only)
3. Typeform submitted; you have confirmation/screenshot

### Verify

Manual — no automated gate. Checklist only.

---

## M6 — SPEC stretch (after M5 or if time)

**Not required for hackathon MVP.** Track in [SPEC_GAP.md](SPEC_GAP.md).

- [ ] Offer-to-track in `pre_llm_call` (yes before save)
- [ ] Git done rules: PR / paths / test
- [ ] `oracle_backfill`, Path A past attempts
- [ ] Receptive defaults + mirror offer/decline counts

**Milestone gate:** each item has at least one fixture or manual script in PROJECT_CHECKLIST appendix (add when built).

---

## Progress tracker

| Milestone | Status | Date verified |
|-----------|--------|----------------|
| M0 Foundation | Done (repo) | |
| M1 Plugin load | | |
| M2 Live smoke | | |
| M3 Live settlers | | |
| M4 Catalog | | |
| M5 Submit | | |
| M6 SPEC stretch | Deferred | |

---

## Related docs

| Doc | Use |
|-----|-----|
| **This file** | End-to-end + **milestone gates** |
| [DONE.md](DONE.md) | Quick gate before commit / agent claims “done” |
| [PHASES.md](PHASES.md) | Short phase names (maps to M0–M5) |
| [demo-prep.md](demo-prep.md) | Recording notes |
| [OWNER_RUNBOOK.md](OWNER_RUNBOOK.md) | **Human-only** Hermes steps + all user outcomes (agent handoff) |
