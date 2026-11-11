# Oracle × Rubal — spec

This file is the source of truth for **what** the product is and **why**. If Notion, chat, or README conflict with this file, this file wins.

Repo: `git@github.com:X0EF/rubal-oracle.git`  
Hackathon: Hermes Agent Plugin Hackathon, due **Wed 11 Nov 2026, 11 PM Africa/Lagos (5 PM EST)**. Do not publish, PR, or post without the owner’s approval.

Deferred work: [nice-to-haves.md](nice-to-haves.md). **Code drift:** [SPEC_GAP.md](SPEC_GAP.md).

---

## Words we use (plain English first)

| Word | What it means here |
|---|---|
| **Commitment** | A plan you asked Oracle to track, with a deadline and a clear “what counts as done.” Not saved unless we can check the outcome from real data. |
| **Settler** | How we check if you actually did it — e.g. a matching git commit, or a calendar event that exists by Thursday. |
| **Forecast / odds** | Our honest guess whether you’ll meet the bar by the deadline, usually as a percentage. If we don’t have enough similar past attempts, we **don’t invent a number** — we say we’re not sure yet. |
| **Similar past attempts** (research: *reference class* / *outside view*) | Other weeks or tasks like this one (“ship a feature in this repo,” “put a review on the calendar”) and whether you actually followed through. |
| **Inside view** (planning fallacy) | Looking only at your plan for *this* week and feeling optimistic. Oracle is not allowed to stop there. |
| **Outside view** | What your track record on *similar* plans actually shows, then adjusting for this week. |
| **Settle** | After the deadline, run the settler. Final outcomes: **met**, **not met**, or **couldn’t verify** (no usable proof — not the same as not met). User-facing words; API may use `success` / `fail` / `unresolved`. |
| **Deadline missed** | The date passed but the commitment is still **open** — a factual phase, not a final grade. Offer extend, subtract, or settle (see [nice-to-haves.md](nice-to-haves.md)). |
| **Subtract** | Our one nudge type: suggest a smaller goal (less scope) to make follow-through more likely. This is **our product idea**, not something a study proved. |
| **Provide nothing** (JITAI: *just-in-time adaptive intervention*) | Sometimes the right move is **no message** — e.g. you’re busy, already recovering, or a ping would annoy you. A worse forecast does not mean we must interrupt. |
| **Receptive** | You’re in a state where a short suggestion might help (not midnight, not in a cooldown after dismissing us, etc.). |
| **Inject** (technical: `pre_llm_call` hook) | Before Hermes answers you, Oracle adds a short note about your open commitments and current odds. It does not block your message. |
| **Mirror** | A summary of what we predicted vs what evidence showed — not the core product, but useful for the demo. |
| **Brier score** (scoring only) | A math check of “how far off were our percentages once we knew the real outcome.” We only use it when we actually gave a number and the final outcome is **met** or **not met** (not **couldn’t verify**). With only one or two outcomes, we do **not** claim “Oracle is well calibrated.” |

---

## What it is

Oracle gives you an honest read on **whether you’re likely to do what you said** — based on similar things you’ve done before and what your calendar and git show this week — and it folds that into Hermes before it replies. If a plan is slipping and you’re open to help, Hermes might suggest **cutting scope**. Otherwise it stays quiet.

**Pitch:** Most assistants help you make plans. Oracle checks whether your behaviour supports them—and helps you change the outcome.

**Tagline:** It predicts you, then helps you beat the prediction.

## What it is not

- A todo list (those don’t require proof you can actually check).
- A day planner that only fits tasks around meetings (that’s **agenda-guardian**).
- A stopwatch for how long the *AI agent* spends on Kanban tasks (**Epoch**).
- A diary of the *agent’s* guesses before it runs a tool (**epistemic-harness**).
- A life dashboard. A small “mirror” view may exist later; it doesn’t justify the plugin by itself.
- A fancy prompt with no memory, no hooks, and no way to verify outcomes.

**The difference we want:** forecasts of **your** follow-through that **change the next Hermes reply**, checked against **git and calendar** (not your word alone).

---

## Why it exists (in plain language)

People often believe “this time I’ll finish on time” because they’re imagining a good week (**inside view**). Research on the **planning fallacy** (Buehler et al., 1994) shows that bias drops when you connect **this** plan to **similar past attempts** — not when you only remember that you’ve been late before.

Oracle plays the role of an **observer**: “Last four similar ship weeks, you finished on time once” → then “this calendar is packed” → so the odds go down.

A worse forecast is **not** permission to nag. **JITAI** (Nahum-Shani et al., 2016) is the idea that help should arrive at the right moment — and that **saying nothing** is a real option when you’re not in a good state to hear it.

**Subtract** (do less, ship a smaller slice) is something we’re trying as a product bet. Studies motivate *when* to speak, not *that* cutting scope always works.

---

## Research vs what we built (short table)

| | Research says (simply) | What Oracle does | What we must not claim |
|---|---|---|---|
| **Planning fallacy + outside view** | Don’t forecast from hope; use similar past outcomes and name them. | Odds start from comparable git/calendar history, with reasons shown. | That a few personal weeks are as solid as big public-project statistics. |
| **JITAI** | Adapt timing; allow “no help now.” | Nudge only when slipping **and** receptive; default silence. | That JITAI proves “subtract” is the best action. |
| **Brier score** | Measure forecast error when you had a % and a yes/no outcome. | Optional mirror stat when both exist. | “We’re calibrated” from one or two bets. |
| **Subtract** | — (hypothesis) | Log offer, accept/dismiss, what happened after. | That a paper validated Oracle. |

Optional flavour only (not foundations): Fogg (timing/ability), Goodhart (don’t game one metric), implementation intentions (if-then plans after subtract).

**Demo-safe one-liners** (studies did not test Oracle):

- Planning-fallacy work suggests people stay optimistic unless past misses are tied to *this* plan — so Oracle starts from named similar attempts, not your pep talk.
- JITAI-style design treats silence as valid when you’re not receptive — so a dropping forecast doesn’t always mean an interruption.

---

## Core loop

**Watch → guess → maybe nudge → check proof → reflect**

1. **Capture.** You state a plan. Oracle saves it only with a **settler** it can run. Otherwise it **refuses** and explains what would make it saveable. No settler = not a commitment, just a wish.
2. **Forecast.** Look at **similar past attempts**, then adjust for this week (e.g. a full calendar lowers the odds of shipping). Not enough history → **no fake percentage**.
3. **Update.** As git and calendar change, refresh the odds and **inject** that into Hermes before it answers.
4. **Intervene.** At chosen moments — not every message — if you’re slipping and **receptive**, Hermes may suggest **subtract**. Otherwise: **provide nothing**.
5. **Settle.** Run the settler: **met**, **not met**, or **couldn’t verify**. Git: repo readable and no matching commit/PR by the deadline → **not met**; **couldn’t verify** only when the repo/source can’t be read or the done rule can’t be checked. Calendar *event exists* with no event after the window → **not met** when the settler ran. If you accept a smaller goal, keep the original on record and add a **revision**; don’t erase history.
6. **Mirror.** What we guessed vs what proof showed. Supports honesty; not the whole product.

---

## Capture and the done rule

- The `pre_llm_call` hook spots likely commitments in conversation and **offers** to track them: “Track this? Done means X, checked by Y, by <deadline>. Tag: feature.” Nothing is saved without a yes. Explicit `/oracle` capture also works.
- Count offers made vs declined; the mirror shows both, so only logging safe bets is visible.
- **Git done rule** — exactly one check, chosen and stored at capture so settling is repeatable:
  1. a PR merged whose title or branch matches a pattern, or
  2. a commit touching given paths, or
  3. a named test passing.

## Refuse-if-unsettled

If we can’t check the outcome from data, we don’t store it as a commitment.

At capture we must record **how we’ll know** (which repo, which calendar check). If Google Calendar isn’t connected, a calendar commitment is refused until it is. If the goal is “go to the gym three times” but we have no location proof, we refuse — a calendar block only proves you **scheduled** time, not that you went.

After the deadline: if the source was readable and the done rule found no match → **not met**. If the source couldn’t be read (disconnected, repo gone, API error) → **couldn’t verify**.

---

## Data we can use (MVP)

You connect sources in **Hermes**; Oracle uses them. It does not read secret token files on its own.

| Source | “Live” means | Good for proving | Not good for pretending |
|---|---|---|---|
| **Git** | You named a real repo | A commit/merge that matches your “done” rule by the deadline | “I was working on it” with no matching commit |
| **Google Calendar** | Hermes Google Workspace **Calendar** works (email-only setup does **not** count) | An event exists in the window you named; or a protected slot stayed empty | Gym attendance, spending, “I was focused” |
| Gmail, bank, location, screen time | Not in this MVP | — | — |

Calendar can still **lower the shipping odds** when your week is crowded, even when the commitment itself is settled by git.

We don’t scan all of `~/dev` or your mail unless you pointed us at a specific repo or calendar question.

---

## Past attempts: two paths (decided 10 Nov 2026)

Connected sources are the primary path. File import / copy-paste is a fallback only, not the main flow.

**Path A — user has past data (from connections).** On first run (and periodically), Oracle reads connected sources once and builds a list of past attempts = *a planned item with a target date* matched to *evidence of when it was actually done*:

- **GitHub (strongest):** issues and milestones with due dates = past plans; linked/closing PRs and merge times = actual completion.
- **Google Calendar:** past deadline-style events (“Ship X”, “Review Y”) vs what happened; meeting load during those weeks as context.
- **Notion / Linear (if connected):** task databases with due dates and done/completed dates.
- Uncertain plan↔evidence matches are shown to the user to confirm or fix; unconfirmed ones are excluded. Items with no matching evidence are excluded from base rates (never counted as misses).
- Once ≥3 similar past attempts exist, give a percentage and name the attempts used.
- Fallback only: a manual import of a Markdown phase doc / exported task list, matched to git the same way.

**Path B — no past data.**

- Still capture, track and settle every commitment. **No percentage** — say “not enough history yet” and show this week’s evidence instead (e.g. “6 meetings, no commits since Monday”).
- No population/research-average percentage in the MVP (keeps “no fake percentage” consistent).
- Every settled commitment becomes a past attempt; percentages switch on automatically at ≥3 similar.
- Encourage short first commitments (1–3 days) so history builds fast.

Demo: connect GitHub + Calendar so Oracle finds real past attempts (Path A). If the repos lack dated issues/milestones, demo Path B honestly. Never invent past weeks.

## How we set the odds (forecast rules)

1. Find **similar past attempts**: same **task tag** and same repo (or same calendar pattern). At capture the LLM assigns one tag from a fixed list — `feature`, `bugfix`, `docs`, `meeting` (extend carefully) — and the user confirms or changes it in the same “track this?” message.
2. Count how often you actually met the bar.
3. That rate is the starting odds; then adjust for **this week’s evidence** (e.g. many meetings → odds go down).
4. Say which past attempts we used.
5. If there are fewer than **three** similar cases: **no percentage** — say “not enough history.” Still track and settle.
6. When we do give a percentage, store it with a timestamp. If you later accept a smaller goal, that original percentage stays on the record.

---

## When we speak up (intervention rules)

Inspired by JITAI, in everyday terms:

- **Goal:** you meet commitments you chose.
- **Moments we consider speaking:** after relevant git/calendar signals, or a daily check — **not** on every chat line.
- **Choices:** suggest **subtract**, or **provide nothing**.
- **Only nudge if:** the plan looks like it’s slipping **and** you’re **receptive** (quiet hours, cooldowns, and “leave me alone” count).
- **Receptive defaults (user-configurable):** quiet hours 22:00–08:00 local; no nudge for 24 h after a dismissal; at most 1 nudge per commitment per day; none while a calendar event is in progress; “leave me alone” mutes until lifted.
- Oracle never **blocks** your message to Hermes; it only adds context.

---

## How it plugs into Hermes (for builders)

Hermes **plugin**: `plugin.yaml` + Python `register(ctx)`, not a chat prompt alone.

| Piece | Role |
|---|---|
| Tools + `/oracle` | Save commitment, status, settle, revise, mirror, answer a subtract offer, backfill past attempts from connected sources |
| `pre_llm_call` hook | Inject open commitments and current odds |
| `post_tool_call` hook | Notice when git/calendar tools changed the evidence |
| `plugin_db("rubal-oracle")` | SQLite memory that survives plugin updates |

Target Hermes **≥ 0.22.7** (what’s installed now).

Hackathon catalog (when you ask): public repo, pinned commit, `hermes plugins validate` passes.

---

## Demo (90 seconds)

Two data sources, both can **settle**:

1. “Ship search this week” — checked via **git**. Odds from similar weeks, or “not enough history.”
2. “Design review Thursday” — checked via **Calendar**.
3. Busy calendar → shipping odds drop. Oracle may suggest subtract or stay silent.
4. Friday: git → **not met** if the repo was readable and no matching commit/PR; calendar → **not met** if the event never appeared (when connected).
5. Short mirror. Brier only if we gave a number and the outcome is **met** or **not met**.

Use real setup; don’t invent past weeks.

---

## Out of scope for this deadline

Wearables, bank feeds, location, screen time, digital twin, A/B tests, site blocking, betting against yourself, shared/family mode, “forecast the AI agent.”

“Nudged vs not nudged” is descriptive only — we don’t claim the nudge *caused* the result.

---

## Nearby Hermes plugins (don’t duplicate them)

- **agenda-guardian** — fits your tasks around the calendar and learns how long tasks take from what you report.
- **Epoch** — estimates how long **agent** Kanban work will take.
- **epistemic-harness** — records what the **agent** predicted before checking something.

Oracle is about **you**, your odds, proof from **git + calendar**, and what Hermes says next.

---

## Working agreements

- Git for this repo: user **X0EF**, email **ostheperson@gmail.com**, X0EF SSH key. Don’t change global git config.
- No commit, push, catalog PR, or X post unless you ask.
- Behaviour changes grounded in research also update `docs/design-rationale.md`.
- Old brainstorming: [Notion master plan](https://app.notion.com/p/40f2fd9914e08192ae0aec5d162c47bc). **This file wins** if they disagree.
