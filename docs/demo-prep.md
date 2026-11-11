# Demo prep (live walkthrough)

Your tracked commitments and source shapes: [../tests/fixtures/HACKATHON_USE_CASE.md](../tests/fixtures/HACKATHON_USE_CASE.md) and `hackathon_use_case.json`.

Unit tests use faked `sources` in `cases.json` + hackathon fixtures. For a live Hermes demo:

1. **Git** — use a real repo (e.g. this one or a scratch repo). Seed a few past weeks with commits whose subjects match your demo `match` string if you want live odds, or accept “not enough history.”
2. **Calendar** — connect Hermes Google Workspace **Calendar** (not email-only). Create or confirm a “design review” event for the demo window.
3. **Walkthrough** — align with [SPEC.md](SPEC.md) demo beats: ship + review, crowded week lowers odds, Friday settle (git **couldn’t verify** / calendar **not met** if empty), mirror + Brier only when a % was given and outcome is met or not met.
4. **`/oracle`** — `status`, `extend <id> <new_deadline>` after a missed deadline if you show that beat.
