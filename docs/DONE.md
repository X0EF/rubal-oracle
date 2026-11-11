# Done checklist

**Full ship list:** [PROJECT_CHECKLIST.md](PROJECT_CHECKLIST.md).

Agents and humans: **tests ≠ shipped**. Use this after code changes and before catalog/demo.

## Automated

- [ ] `scripts/verify.sh` exits 0 (unit tests + `hermes plugins doctor --ci` on this repo)

## Intent (SPEC + fixtures)

- [ ] Refuse capture when settler missing or calendar offline ([SPEC](SPEC.md) refuse-if-unsettled)
- [ ] Forecast: no fake % below 3 comparable attempts; crowded calendar lowers odds
- [ ] `pre_llm_call` injects context, never `action: block`
- [ ] Settle: git readable + no match → `fail` (not met); git unreadable → `unresolved`; calendar empty → `fail`
- [ ] Hackathon use case ids in `hackathon_use_case.json` still pass

## Hermes plugin (phase 1+)

- [ ] `oracle_commit`, `oracle_settle`, `oracle_revise`, `oracle_status`, `oracle_mirror`, `oracle_extend` registered
- [ ] `/oracle` slash delegates to same engine
- [ ] State survives restart via `plugin_db` (phase 3)

## Hackathon submit (phase 5 — owner only)

- [ ] Commit on `rubal-oracle` with **`plugin`** in subject (git settler)
- [ ] Calendar event title contains **`hackathon demo`**
- [ ] Catalog PR open; validate/doctor clean at pinned commit
- [ ] &lt;90s screen demo on X, tag @NousResearch; Typeform with PR + video links

## Out of scope (do not claim)

- Brier “calibration” with n &lt; 3; gym/location/bank settlers; blocking user messages
