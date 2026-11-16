# Hermes catalog compliance (rubal-oracle)

For reviewers on [hermes-agent catalog PRs](https://github.com/NousResearch/hermes-agent).

## Credentials and third-party access

- Oracle **does not** read Hermes `auth.json`, token files, or other credential stores.
- Oracle **does not** spawn Hermes google-workspace `google_api.py` or call Google APIs from plugin code.
- **Calendar evidence:** events are **ingested** from agent terminal/shell tool output in `post_tool_call` (`ingest_calendar_from_text`) and stored under `plugin_data_dir("rubal-oracle")`. Settlers read that cache only.
- **Git evidence:** local `git log` in a user-supplied repo path (no network).
- Other settlers (`github`, `notion`, …) use `sources.*` payloads Hermes/tests supply; this plugin does not implement those API clients.

## Hermes home / profiles

- Prefer `hermes_constants.get_hermes_home()` when a path under Hermes is needed (see `oracle/hermes_home.py`).
- Plugin state uses `plugins.plugin_storage.plugin_db` / `plugin_data_dir`, not `~/.hermes` hardcoding.

## User-facing calendar setup

1. User connects Google in Hermes (google-workspace skill).
2. Agent runs a calendar list command in chat.
3. `post_tool_call` caches JSON events → calendar settlers can verify `event_exists` / `slot_empty`.

Without step 2–3, calendar settlers correctly report **couldn’t verify** / calendar `ok: false`.

## Reviewer checklist (Hermes catalog #154037)

| Ask | Where addressed | Tests |
|-----|-----------------|-------|
| No `auth.json` / token reads for `calendar_connected` | `oracle/sources.py` → cache-only | `tests/test_calendar_sources.py` |
| No `google_api.py` subprocess / plugin Google calls | `oracle/calendar_fetch.py` → cache-only resolve | same |
| `get_hermes_home` / profile-aware paths | `oracle/hermes_home.py` | `tests/test_hermes_home.py` |
| JSON ingest cap + `raw_decode` (recommended) | `ingest_calendar_from_text` in `calendar_fetch.py` | `test_ingest_*` in `test_calendar_sources.py` |

Verification: `./scripts/verify.sh` (unittest + `hermes plugins doctor` when CLI is present).