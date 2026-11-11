# rubal-oracle

A [Hermes](https://github.com/NousResearch/hermes-agent) plugin. You name a goal and a deadline in chat. After the deadline, Oracle checks **proof** — not your word — and marks it **met**, **not met**, or **couldn’t verify**.

Most assistants help you make plans. This one checks whether you did it.

**Rubal** is the forecast: if there are enough similar past attempts, you get a percentage (named, and nudged if this week’s calendar is packed). If there aren’t enough, it says so. If you’re slipping it may suggest a smaller goal. It can also stay quiet.

**Tagline:** *It predicts you, then helps you beat the prediction.*

---

## Install

Needs Hermes `>= 0.22.7`. After install, **restart the gateway** (or quit Desktop fully) so the tools load.

```bash
hermes plugins install github:X0EF/rubal-oracle
hermes plugins enable rubal-oracle
hermes gateway restart   # or fully quit Hermes Desktop
```

From a local clone:

```bash
hermes plugins install "file://$(pwd)"
hermes plugins enable rubal-oracle
hermes gateway restart
```

Check:

```bash
hermes plugins doctor "$(pwd)" --ci
hermes plugins list | grep -i rubal
```

In chat: `/oracle help` or just ask how it works. `/oracle status` lists what is open. You do not need a slash command to save a goal — talk; Hermes will call `oracle_commit`.

---

## What you can track

Oracle only saves a commitment when it knows **how to check**. Git is a **repo path**, not a plugin. Everything else needs the matching Hermes plugin (or MCP) connected; if that source is offline, capture is refused and settle returns **couldn’t verify**.

| Commitment | Proof | You need |
|---|---|---|
| Ship a feature | Commit subject contains a word | Local **git** repo |
| Merge a PR | Merged PR title / branch | Local git `merged_prs` (or GitHub) |
| Land files in a folder | Paths touched | Local git |
| Named test green | Named test passed | Local git |
| Meeting / demo is on the calendar | Event title in a window | Hermes **Calendar** / Google Workspace Calendar (not email-only) |
| Keep a focus slot empty | No matching event in that window | Same Calendar plugin (`mode: slot_empty`) |
| Close a GitHub issue | Issue `closed` by the deadline | Hermes GitHub / `gh` |
| Finish a Notion task | Status done / complete / completed | **Notion** MCP |
| Finish a Linear issue | State done / complete / completed | Hermes **Linear** |
| Send a specific email | Sent mail, subject match | Hermes **Gmail** |
| Hermes kanban card done | Card status done | Hermes **kanban** |

Sample JSON for the non-git sources lives in [`tests/fixtures/sources/`](tests/fixtures/sources/). That is the contract a linked plugin should return (`ok` plus the rows). Full map: [`docs/COMMITMENT_SOURCES.md`](docs/COMMITMENT_SOURCES.md).

---

## How a turn works

1. **Capture** — statement, deadline, success criteria, settler (`git`, `calendar`, `github`, `notion`, `linear`, `gmail`, `kanban`).
2. **While it’s open** — Hermes replies as usual. Oracle may inject a short note (odds or “not enough history”). It does not block your message.
3. **Settle** — after the deadline: **met** / **not met** / **couldn’t verify**.

Tools: `oracle_commit`, `oracle_settle`, `oracle_status`, `oracle_revise`, `oracle_extend`, `oracle_mirror`, `oracle_respond_track`, `oracle_backfill`. Slash: `/oracle help`, `/oracle status`, `/oracle extend <id> <iso>`.

---

## Develop

```bash
scripts/verify.sh
# or
PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py' -q
hermes plugins doctor "$(pwd)" --ci
```

After a code change, reinstall from this repo and restart the gateway before judging live chat. `scripts/hermes_plugin_loop.sh` does that plus two `hermes chat -q --oneshot` runs.

Spec: [`docs/SPEC.md`](docs/SPEC.md). Hermes-as-a-user checks: [`docs/OWNER_RUNBOOK.md`](docs/OWNER_RUNBOOK.md).

MIT — see [LICENSE](LICENSE).
