# SPEC vs implementation

Tracks [SPEC.md](SPEC.md) decisions not yet fully in code. Update when closing gaps.

## Aligned in this pass (10 Nov 2026)

- Git settle: repo **readable**, no matching done rule → API `fail` (**not met**); unreadable repo → `unresolved` (**couldn’t verify**)
- Task **tag** on commit (`feature` | `bugfix` | `docs` | `meeting`); comparable history filters by tag when set
- Path B hint: when no %, forecast `reasons` may list this week’s calendar/commit evidence

## Aligned (11 Nov 2026 — agent pass)

- User-facing **outcome_label** / **status_label** on settle + status (`met` / `not met` / `couldn’t verify`)
- **Catalog validate:** `scripts/catalog_validate.sh` (excludes local `.cursor`/ECC from security scan)
- **design-rationale.md** for catalog research copy

## Aligned (11 Nov 2026 — kyuubi pass)

| SPEC | Status |
|------|--------|
| Git done rules | **commit_match**, **pr_merge**, **paths**, **test_pass** (`oracle/git_settle.py`) |
| `pre_llm_call` track **offer** + **oracle_respond_track** (yes before save) | Heuristic offer + decline/save via tool |
| **oracle_backfill** tool | Propose from git log; `confirm_ids` → store comparables |
| Path A unconfirmed excluded | `confirmed: false` backfill rows omitted from forecast base rate |
| Receptive defaults | `oracle/receptive.py` — quiet 22–08, 24h after dismiss, event in progress, leave-me-alone |
| Mirror offer counts | `track_offers_*`, `subtract_*` on `oracle_mirror` |
| Hermes tools | **8** tools registered (was 6) |

## Still thin / later

- Live GitHub issues/milestones backfill (today: git log heuristic + fixtures `merged_prs` / `path_touches` / `tests`)
- User confirm UI for uncertain plan↔evidence matches (use `confirm_ids` on backfill)
- Full `@/leave-me-alone` command wiring (store field exists)
- Git **test_pass** live: run pytest in plugin (fixtures only today)

When in doubt, **fixtures + SPEC** win; extend `cases.json` before changing settle semantics again.
