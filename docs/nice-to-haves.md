# Nice to haves

Backlog and product choices that are **not required** for the hackathon MVP. [SPEC.md](SPEC.md) wins on scope; implement in the order below when you have time.

---

## Locked product choices (implement when you pick them up)

These were decided in design chat; they belong in code/fixtures when ready, not left ambiguous.

### Settlement labels (user-facing vs API)

| API / internal | User-facing | When |
|----------------|-------------|------|
| `success` | **Met** | Settler ran; bar satisfied by the deadline rule. |
| `fail` | **Not met** | Settler ran; objective rule not satisfied (especially calendar *event exists*). |
| `unresolved` | **Couldn’t verify** | Missing proof, settler offline, or git silent — not a punishment. |

- **Git (SPEC 10 Nov):** repo readable, no match → **not met** (`fail`); unreadable source → **couldn’t verify** (`unresolved`).
- **Calendar (`event_exists`):** window ended, calendar connected, no matching event → **not met**.
- **Brier / mirror:** only when you gave a % and final outcome is **met** or **not met** (not **couldn’t verify**).

### Deadline missed (phase, not a fourth tombstone)

- **`deadline_missed`**: open commitment, `now > deadline`, not settled yet — factual, supportive tone.
- **Then offer:** extend deadline, revise (subtract), or settle now (met / not met / couldn’t verify).
- **Git after deadline, no commit:** stay in **deadline missed** until user extends or closes → usually **couldn’t verify**.
- **Calendar, window over, no event:** **not met** (or one optional extend before **not met** — pick one and document in SPEC).

Suggested Hermes copy patterns live in SPEC once deadline-missed ships; see implementation items below.

---

## Priority order (hackathon → later)

| P | Item | Status | Notes |
|---|------|--------|--------|
| 1 | Fixture: `settle-calendar-missing-event` → **not met** | Done | In `cases.json`; API `fail` = user **not met**. |
| 2 | SPEC + engine strings for met / not met / couldn’t verify | Partial | Glossary in SPEC; user strings in inject/status TBD. |
| 3 | **Deadline missed** + **extend deadline** (tool or revise field) + inject | Done | `extend_deadline`, `pre_llm_call` + `/oracle extend`; no eval case yet. |
| 4 | Settle after **revise** (subtract accepted) | Defer unless demo shows it | `revise-preserves-original` already tests storage. |
| 5 | Calendar **reference class** → % at capture | Skip for MVP | Git odds + crowded calendar carry forecast demo. |
| 6 | Git explicit **not met** (late/wrong commit) | Skip for MVP | Avoid shame without a clear rule. |
| 7 | Mirror fixture **n = 2** + still `claims_calibration: false` | Skip | One Brier row is enough for judges. |

---

## Fixture gaps (detail)

### Calendar settle — no event

- **Setup:** `capture-calendar-event` (already exists).
- **Settle:** `now` after window; `events: []` or no title match.
- **Expect:** `outcome: fail` (API), user copy **not met**.

### Git settle — not met (deferred)

Only add if you define e.g. “commit after deadline counts as not met” or “explicit revert of promised work.” Until then, empty git → **couldn’t verify** only.

### Wrong calendar title

- Event exists but doesn’t match `event_match` → **not met** vs **couldn’t verify** depending on strict matching; decide when you add P1 fixture.

---

## Implementation checklist (deadline missed + extend)

- [ ] Derive `phase: deadline_missed` on open commitments when `now > deadline`.
- [ ] `oracle_extend` `{ id, new_deadline }` or extend via `oracle_revise`; log history, refresh forecast optional.
- [ ] `pre_llm_call`: mention overdue commitments + one supportive line; subtract only if slipping **and** receptive.
- [ ] Slash/tool: `extend`, `settle` after overdue.
- [ ] Eval cases: overdue git → couldn’t verify path; overdue calendar → not met.

---

## Integration / demo (not unit tests)

- Small **demo repo** with seeded commits for “similar past attempts” in live Hermes runs.
- **Google Calendar** connected in Hermes for real settle (unit tests keep faked `sources`).
- `docs/design-rationale.md` when behaviour ties to research (SPEC working agreement).

---

## Explicitly out of this list

Already in MVP scope or out of scope per SPEC: wearables, bank, location, ActivityWatch, agent self-forecast (Epoch / epistemic-harness territory), calibration marketing from n &lt; 3.
