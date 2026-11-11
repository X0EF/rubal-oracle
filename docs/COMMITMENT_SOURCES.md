# Commitment sources — what we support vs catalog

**Product name:** rubal-oracle. Rubal = forecast (odds from similar past attempts + this week’s calendar) and optional “do less”; Oracle = capture + settle from proof.

Oracle only **settles** from data we can check. A Hermes plugin on the machine is not enough until we have a sample payload + a settler that reads it. Git is a **repo path**, not a plugin.

Tonight we cannot OAuth-test 20 plugins. This table is the support list. Each row has a fixture shape so a real linked plugin can drop the same JSON later.

## Table (20 common commitments)

| # | Commitment people actually make | Proof | Hermes surface | Status |
|---|---|---|---|---|
| 1 | Ship a feature | commit subject contains a word | **local git** (no plugin) | **shipped** |
| 2 | Merge a PR | merged PR title/branch | local git `merged_prs` / GitHub | **shipped** (fixture) |
| 3 | Land files in a folder | paths touched | local git | **shipped** |
| 4 | Named test green | `test_pass` | local git / CI JSON | **shipped** |
| 5 | Meeting / demo block exists | event title in a window | **google-workspace** Calendar, **booking-bridge**, **calendar-agenda** | **shipped** if Calendar `ok` |
| 6 | Keep a focus slot empty | no event in window | same Calendar | **shipped-via-fixture** — `mode: slot_empty` |
| 7 | Close a GitHub issue | issue state closed by deadline | `gh` / GitHub in Workspace-ish tools, **diaktoros** (PRs) | **shipped-via-fixture** — `github.issues`; no live OAuth |
| 8 | Finish a Notion task | status Done + date | Notion MCP (already in some Hermes profiles) | **shipped-via-fixture** — `notion.tasks`; no live OAuth |
| 9 | Finish a Linear issue | issue done | **linear-digest** | **shipped-via-fixture** — `linear.issues`; no live OAuth |
| 10 | Send a specific email | Gmail sent, subject match | **google-workspace**, **gmail** desktop | **shipped-via-fixture** — `gmail.sent`; no live OAuth |
| 11 | File exists / shared in Drive | file id/name | **google-workspace** Drive | skip unless we need a 11th |
| 12 | Doc updated | Docs revision after t | **google-workspace** Docs | skip (overlaps git) |
| 13 | Sheet row added | Sheets | **google-workspace** Sheets | skip niche |
| 14 | Invoice chased / paid | CSV paid flag | **cash-desk** | skip (finance niche) |
| 15 | Hermes kanban card done | task status | built-in kanban / **kanban-*** plugins | **shipped-via-fixture** — `kanban.tasks`; no live OAuth |
| 16 | Consult booked | event created | **booking-bridge** | same as #5 if we see the event |
| 17 | Agenda item marked done | private outcome=done | **calendar-agenda** | **todo** — still not “went to gym” |
| 18 | X post went out | tweet exists | not **hermes-x-bookmarks** (bookmarks only) | skip until a post plugin |
| 19 | Gym / location / bank / screen time | none we can read | — | **refuse** (honest) |
| 20 | “I was focused” / vibes | none | — | **refuse** |

**Hard-hitting, common, keep on the todo (after git+calendar):** GitHub issue closed, Notion task done, Linear done, Gmail sent, kanban done, calendar empty slot. That is six more settlers, not twenty plugins.

Most catalog plugins (advisor, agora, babysit, chrome-tabs, …) do **not** prove a human commitment. Do not wire them.

## Loop to get one source working

For each **todo** row:

1. Capture one **sample JSON** (from the plugin tool, MCP, or docs). Save under `tests/fixtures/sources/<name>.json`.
2. Add `sources.<name>.ok` + the rows the settler needs. Unit test: capture → settle success / fail / unreadble.
3. `oracle_commit` `settler` enum += that name. Refuse if `ok` is false (`how_to_make_saveable` = connect that plugin).
4. Skill + short help line: “this goal uses X, not git.”
5. `scripts/hermes_plugin_loop.sh` after commit: doctor, reinstall, **gateway restart**, `hermes chat -q` with a sentence that should save or refuse.
6. Do **not** claim live OAuth works until that chat run on a profile that actually has the plugin linked.

Git #1–4 and Calendar #5 already follow this with faked `sources` in `cases.json`.

## Demo tonight (timeboxed)

Show **ship (git)** + **named calendar event**. Gym: refuse and say why. Do not install ten plugins in the last hour.
