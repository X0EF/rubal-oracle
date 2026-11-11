# Owner runbook — human-only steps

**Latest agent pass:** [AGENT_HANDOFF.md](AGENT_HANDOFF.md)

**When agents say they’re done in the repo**, they mean **M0 + code**: tests, `verify.sh`, doctor, catalog validate. **You** finish **M1–M5** here, using Hermes like a real user.

Technical gates: [PROJECT_CHECKLIST.md](PROJECT_CHECKLIST.md). Product behaviour: [SPEC.md](SPEC.md). Hackathon commitments: [HACKATHON_USE_CASE.md](../tests/fixtures/HACKATHON_USE_CASE.md).

---

## What agents cannot do for you

| Area | You only |
|------|-----------|
| Enable plugin in **Hermes Desktop** (or your CLI profile) | Toggle + restart |
| **Chat** in Hermes so tools and `pre_llm_call` run | Type / talk in Hermes |
| **Google Calendar** OAuth in Hermes | Connect GWS Calendar (not email-only) |
| Create calendar events, ship git commits for settlers | Your calendar + git |
| **Screen record** demo, **X** post, **Typeform** | M5 |
| Approve **push**, catalog **PR**, public post | Owner policy |

---

## Before you start (once)

1. **Hermes running** — Desktop (X11 if GPU crashes on Wayland) or CLI + gateway.
2. **Dev plugin path** — either:
   - **From repo:** enable development install pointing at `/home/ostheperson/dev/oracle-rubal`, or
   - **Copied:** install under `~/.hermes/plugins/` per Hermes docs.
3. **Terminal check (from repo root):**

   ```bash
   hermes plugins doctor "$(pwd)" --ci
   hermes plugins list | rg -i rubal
   ```

   **M1 done when:** doctor **OK**, `rubal-oracle` **enabled**, no `rubal-oracle` errors in `~/.hermes/logs/agent.log`.

---

## M2 — Live smoke (use Hermes like a user)

**Goal:** capture → see inject → survive restart.

### Steps

1. Open a **new Hermes chat** (Desktop or CLI).
2. Ask Hermes to call **`oracle_commit`** with your hackathon ship commitment (or paste this intent in natural language and let the agent call the tool):

   | Field | Example |
   |-------|---------|
   | `statement` | Ship Oracle Hermes plugin before hackathon deadline |
   | `deadline` | `2026-11-11T23:00:00+01:00` |
   | `success_criteria` | Commit on main whose subject contains `plugin` |
   | `settler` | `git` |
   | `repo` | `/home/ostheperson/dev/oracle-rubal` |
   | `match` | `plugin` |
   | `tag` | `feature` |

3. **Expected capture outcomes**

   | What you see | Meaning |
   |--------------|---------|
   | `ok: true`, `saved: true`, an `id` | Commitment stored |
   | Refusal / not saved | Settler missing, calendar offline when required, or rule in SPEC — read the message |
   | No percentage | **Path B** — not enough similar history (normal for first capture) |
   | A **%** + named comparables | **Path A** — enough similar past attempts |

4. Run **`/oracle status`** or ask for **`oracle_status`**.  
   **Expect:** commitment **open**, statement and deadline match what you saved.

5. Send **any normal message** (e.g. “What should I work on tonight?”).  
   **Expect:** Hermes still replies; Oracle text is **added** (inject) — open commitment, odds or Path B reasons.  
   **Must NOT happen:** your message blocked (`action: block` from Oracle).

6. **Quit Hermes completely** → start again → **`/oracle status`**.  
   **Expect:** same commitment still **open** (same `id` or same statement).

**M2 done when:** all four bullets in [PROJECT_CHECKLIST M2 gate](PROJECT_CHECKLIST.md#m2--live-smoke-plugin--backend--persistence) are true.

---

## M3 — Live settlers (git + calendar)

### One-time setup

1. Hermes → **Google Workspace** → connect **Calendar** (not email-only).
2. Create an event whose title contains **`hackathon demo`** (e.g. “Hackathon demo screen record”) in the window you care about.

### Capture calendar commitment

Ask Hermes for **`oracle_commit`** for demo recording (see `hackathon_use_case.json`).  
**If calendar offline:** capture is **refused** — connect Calendar first.

### Git proof (when ready)

```bash
git -C /home/ostheperson/dev/oracle-rubal commit -m "feat: hermes plugin …"   # subject contains `plugin`
```

(Only when **you** approve committing.)

### Settle (after deadline rules in SPEC, or your demo script)

Call **`oracle_settle`** with each commitment `id` (or ask Hermes to settle).

**M3 done when:** calendar connected; settlers return honest **met / not met / couldn’t verify** per table below.

---

## M4–M5 — Submit (owner)

| Step | Action |
|------|--------|
| M4 | Push when approved → `hermes plugins validate` at pinned SHA → open catalog PR |
| M5 | &lt;90s screen record: capture → forecast/inject → settle/mirror → post X @NousResearch → Typeform |

Recording beats: [demo-prep.md](demo-prep.md).

---

## User flows — tools and `/oracle`

| You want | How |
|----------|-----|
| Track a plan | Natural language → Hermes calls **`oracle_commit`** |
| List open / settled | **`/oracle status`** or **`oracle_status`** (`id` optional) |
| Close after deadline | **`oracle_settle`** with `commitment_id` |
| Change scope / odds path | **`oracle_revise`** |
| Push deadline | **`/oracle extend <id> <new_deadline>`** or **`oracle_extend`** |
| Prediction vs reality | **`oracle_mirror`** (after settle when SPEC allows Brier) |

Slash **`/oracle`** delegates to the same engine as the tools.

---

## All user-visible outcomes (what to expect)

### After **capture** (`oracle_commit`)

| Outcome | You see | Next |
|---------|---------|------|
| Saved | `saved: true`, `id` | Status + inject mention it |
| Refused | Error / not saved, reason | Fix settler (connect calendar, fix `repo`, etc.) |
| Path B | No %; “not enough history” + this-week context | Still tracked; settles later |
| Path A | % + comparable attempts named | Odds can shift after calendar/git signals |
| Crowded week | Lower % (if you had a %) | May still get **no nudge** if not receptive (JITAI) |

### On every **chat turn** (`pre_llm_call` inject)

| Outcome | You see |
|---------|---------|
| Normal | Extra context: open commitments, odds or Path B |
| Never | Message blocked by Oracle |

### After **deadline** — still open

| Phase | Meaning | You can |
|-------|---------|---------|
| **Deadline missed** | Date passed, not settled yet | **extend**, **revise**, or **settle** |

### After **settle** (`oracle_settle`)

| User-facing | API | Git settler | Calendar `event_exists` |
|-------------|-----|-------------|-------------------------|
| **Met** | `success` | Matching commit in window | Event found |
| **Not met** | `fail` | Repo readable, no match | Connected, no event after window |
| **Couldn’t verify** | `unresolved` | Repo unreadable / source broken | Source offline, not “punishment” |

### **Revise** / **extend**

| Action | Outcome |
|--------|---------|
| **Revise** (subtract) | Scope/deadline/criteria change; original forecast kept if there was a % |
| **Extend** | New deadline; commitment stays **open** until you settle |

### **Mirror** (`oracle_mirror`)

| Outcome | When |
|---------|------|
| Summary + optional Brier | You had a **%** and final **met** or **not met** |
| No Brier claim | **Couldn’t verify**, or &lt;3 comparable forecasts |

### Posting the X video

**Not settled by Oracle** — no settler for “posted on X”. Calendar only proves you **scheduled** recording time; you still post + Typeform for judges.

---

## Quick troubleshoot

| Symptom | Try |
|---------|-----|
| Desktop GPU crash | X11 / disable Vulkan (see your Hermes desktop config) |
| Plugin not listed | M1 doctor + enable + restart |
| Inject missing | Plugin enabled? `pre_llm_call` hook? New turn after capture? |
| Calendar refused | GWS **Calendar** connected |
| Git **not met** | Subject contains `match` string, correct `repo` path |
| Git **couldn’t verify** | Repo path wrong, permissions, Hermes can’t read git |

---

## Handoff template (for agents)

When repo work is finished, agents should point you here and list **unchecked M1–M5 rows** in [PROJECT_CHECKLIST](PROJECT_CHECKLIST.md) progress tracker only — not claim hackathon submit done.
