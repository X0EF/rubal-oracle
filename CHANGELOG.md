# Changelog

## Unreleased

### Fixed (catalog review)

- Calendar connection and fetch use **plugin cache only** (from `post_tool_call` ingest); no Hermes credential reads.
- Removed google-workspace `google_api.py` subprocess from plugin code.
- Hermes home via `hermes_constants.get_hermes_home()` with env fallback (`oracle/hermes_home.py`).
- Safer calendar JSON ingest (`JSONDecoder.raw_decode`, input size cap).