# rubal-oracle — current product (v1)

Hermes plugin. You name a goal, a deadline, and **how we check**. After the deadline Oracle reads proof — not your word — and marks it **met**, **not met**, or **couldn’t verify**.

Most assistants help you make plans. This one checks whether you did it.

**Rubal** is the forecast: ≥3 similar past attempts → a percentage (named), minus 0.15 if this week’s calendar has ≥4 events, clamped to `[0.05, 0.95]`. Fewer than 3 → no percentage (`insufficient_reference_class`), this week’s evidence only.

**Tagline:** It predicts you, then helps you beat the prediction.

Install: Hermes `>= 0.22.7`. `plugin.yaml` + `__init__.py` `register(ctx)`. Talk in chat; Hermes calls `oracle_commit`. `/oracle help`, `/oracle status`, `/oracle extend <id> <iso>`.

---

## Loop

1. **Offer** — `pre_llm_call` may offer to track a plan-shaped message. Nothing is saved until yes.
2. **Capture** — `oracle_commit`. Refused if the settler source is offline (`ok: false`) or the settler kind is `location` / `bank`.
3. **Inject** — each later turn gets open commitments and odds (if any). Never blocks the user message.
4. **Revise / extend** — smaller success criteria (`oracle_revise`, original kept as `superseded`); new deadline (`oracle_extend`). **Revise does not recalculate odds.**
5. **Settle** — `oracle_settle`. Source offline → **couldn’t verify**. Source readable, rule missed → **not met**. Rule hit by deadline → **met**.
6. **Mirror** — guessed % vs met/not met. Brier only when a % was stored and the outcome is met or not met. Never claims calibration.

Open + `now > deadline` is a **deadline missed** phase (still open), not a fourth grade. Inject offers extend, smaller goal, or settle.

---

## Commitments and plugins

Oracle only saves a goal when it knows how to check. **Git is a repo path, not a plugin.** Everything else needs that Hermes plugin or MCP connected. If `ok` is false at capture → not saved. If it dies at settle → **couldn’t verify**.

Payload shapes: `tests/fixtures/sources/`.

| You said you’d… | Settler | Met when | Source / plugin |
|---|---|---|---|
| Ship a feature | `git` `commit_match` | Commit subject contains `match` by the deadline | Local git repo |
| Merge a PR | `git` `pr_merge` | Merged PR title/branch matches | Local git `merged_prs` |
| Land files | `git` `paths` | Named paths touched | Local git |
| Named test green | `git` `test_pass` | Named test passed | Local git |
| Meeting exists | `calendar` `event_exists` | Event title in the window | **Cached** events after the agent runs **google-workspace** calendar list (`post_tool_call`); no plugin OAuth or `auth.json` reads |
| Keep a slot empty | `calendar` `slot_empty` | No matching event in the window | Same cache |
| Close a GitHub issue | `github` | Issue title matches, `state=closed` by deadline | Hermes GitHub plugin or GitHub CLI data already on the machine |
| Finish a Notion task | `notion` | Title matches, status done/complete/completed | **Notion** MCP |
| Finish a Linear issue | `linear` | Title matches, state done/complete/completed | Hermes **Linear** |
| Send a specific email | `gmail` | Sent mail, subject match, `sent_at` by deadline | Hermes **Gmail** |
| Kanban card done | `kanban` | Title matches, status done | Hermes **kanban** |
| Workout / run / gym | `strava` | Activity name or sport matches, `start_at` by deadline | **Strava** MCP |
| Workout from Health | `health` | Workout title or sport matches, `started_at` by deadline | **Apple Health** MCP or **athletedata** |

This plugin does **not** call vendor APIs itself. It reads `sources.<name>` that Hermes (or tests) already supplied, plus **calendar JSON cached from agent tool output** (see [CATALOG_COMPLIANCE.md](CATALOG_COMPLIANCE.md)).

---

## Tools and hooks

| Surface | Role |
|---|---|
| `oracle_commit` | Save commitment + forecast |
| `oracle_settle` | Grade from proof |
| `oracle_revise` | Smaller criteria; keep original |
| `oracle_extend` | New deadline |
| `oracle_status` | Open + settled summary |
| `oracle_mirror` | % vs outcome |
| `oracle_respond_track` | Accept/decline a track offer |
| `oracle_backfill` | Propose git-history comparables; only **confirmed** ids count |
| `/oracle` | `help`, `status`, `extend`, `settle` |
| `pre_llm_call` | Inject; track offer; never `action: block` |
| `post_tool_call` | May cache Calendar events from tool output |
| `plugin_db("rubal-oracle")` | SQLite; survives plugin updates |

Forecast comparables today come from `sources.git.comparable` plus **confirmed** backfill rows. Minimum class size: **3**.

Subtract (“smaller scope”) is injected only when the hook is told `slipping` and `decision_point` and the user is **receptive**. The live hook does not compute slipping itself; the skill may still tell Hermes to suggest it. Receptive defaults: not 22:00–08:00, not within 24h of a track-offer dismiss, not during a calendar event; `leave_me_alone_until` is stored but has no user command yet.

---

## What v1 is not

A todo list, a day planner, a life dashboard, or a claim that Oracle is calibrated. Unbuilt work: [docs/nice-to-haves.md](docs/nice-to-haves.md).
