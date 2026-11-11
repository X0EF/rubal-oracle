# Submit tonight — last hour

Deadline: **2026-11-11 23:00 Africa/Lagos** (same as `2026-11-11T23:00:00+01:00`).

Do these in order. Stop when the clock says so. Do not open a second agent session for “one more feature.”

---

## 1. Git / GitHub (do this first)

Repo: `git@github.com:X0EF/rubal-oracle.git` (user **X0EF**). Public. Default branch must contain the plugin.

**Must be committed and pushed:**

- Root `plugin.yaml` and `__init__.py` `register(ctx)` (plugin, not a prompt)
- `oracle/` engine
- `docs/` (at least SPEC + this file if you already committed it)
- Tests / fixtures if they are already on the branch — do not add new ones now

**Commands (from `/home/ostheperson/dev/oracle-rubal`):**

```bash
git status
git log -1 --oneline
git rev-parse HEAD
./scripts/catalog_validate.sh
```

1. If `git status` shows uncommitted plugin files you intend to ship, commit them yourself. Subject should contain `plugin` if you still need a git settler match.
2. If the branch is ahead of origin, **push**. Agents will not push unless you tell them. You push.
3. Confirm GitHub shows that commit: `https://github.com/X0EF/rubal-oracle`
4. Copy `git rev-parse HEAD`. That SHA is what you pin if you open a catalog PR.

If push fails, stop and fix remote/auth. Do not start the demo on unpushed code.

---

## 2. Hermes — one live pass (no restart theatre unless it is already off)

**Enable**

1. Hermes Desktop or CLI is running (X11 if GPU crashes on Wayland).
2. Dev plugin path: this repo, or a copy under `~/.hermes/plugins/`.
3. Enable **rubal-oracle**. Restart Hermes once if you just enabled it.

```bash
hermes plugins doctor "$(pwd)" --ci
hermes plugins list | rg -i rubal
```

Doctor **OK**, plugin **enabled**, no `rubal-oracle` errors in `~/.hermes/logs/agent.log`. If not enabled, stop. Nothing else counts.

**New chat**

Open a **new** Hermes chat. Do not reuse a long thread.

**Capture ONE git ship commitment** (required)

Ask Hermes to call `oracle_commit` (or say it in natural language):

| Field | Value |
|-------|--------|
| `statement` | Ship Oracle Hermes plugin before hackathon deadline |
| `deadline` | `2026-11-11T23:00:00+01:00` |
| `success_criteria` | Commit on main whose subject contains `plugin` |
| `settler` | `git` |
| `repo` | `/home/ostheperson/dev/oracle-rubal` |
| `match` | `plugin` |
| `tag` | `feature` |

You need `ok: true`, `saved: true`, an `id`. No percentage is fine (Path B). Refusal means the settler is broken — fix `repo` path, do not switch to gym.

**Optional calendar event** (only if Calendar is already connected)

- Hermes → Google Workspace → **Calendar** (not email-only). If this is not already connected, **skip**. Do not start OAuth with 40 minutes left.
- If connected: create an event whose title contains **`hackathon demo`**. Optionally capture a second `oracle_commit` for that event. If capture is refused because Calendar is offline, drop it and move on.

**Status**

```text
/oracle status
```

Expect the ship commitment **open**, statement and deadline matching what you saved.

**Inject (~15 seconds)**

Send one normal message, e.g. “What should I work on tonight?”

Expect: Hermes still replies; Oracle text is **added** (open commitment, odds or Path B). Must **not** block the message.

That is the live proof. Quit/restart only if you have spare minutes and want persistence on camera. Skip restart if the clock is tight.

---

## 3. Video, X, Typeform (this is the submit)

Judges need a **video URL** and a **Typeform** row. Catalog PR is not a substitute.

**Video — under 90 seconds**

You may use a **generated Apple-like clip** instead of a live screen record. Either way:

- Length: **&lt; 90s**
- Must show **tools or hooks**, not a prompt-only chat
- Live-record beats if you record: capture → `/oracle status` → ~15s inject (optional: settle/mirror). Do not script a gym story.
- Generated clip: same beats. Git ship + inject. Calendar only if you actually have it.

**X**

- Post the video on **X**
- Tag **@NousResearch**
- Copy the post URL

Oracle does **not** settle “posted on X.” You still post.

**Typeform (required)**

- Form: https://form.typeform.com/to/FwJLvOln
- Fields the docs name: **PR URL** + **video URL**
- If you have no catalog PR (step 4 skipped), put the **public GitHub repo URL** (`https://github.com/X0EF/rubal-oracle`) in the PR field. Do not wait for catalog CI.
- Submit before **23:00 Africa/Lagos**
- Screenshot the confirmation

If Typeform asks for anything else not listed in these docs: fill it honestly; do not invent a second form URL.

---

## 4. Catalog PR — only if ≥ 60 minutes left

Catalog guide: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission

**Skip this entire section if it is after 22:00 Africa/Lagos** (under 60 minutes to deadline). Go to Typeform with the GitHub repo URL. A late catalog PR does not save a missed form.

If you still have ≥ 60 minutes:

1. Confirm push from step 1.
2. `git rev-parse HEAD` — pin **that** SHA.
3. `scripts/catalog_validate.sh` exits 0 at that SHA.
4. Open the catalog entry PR: `plugin.yaml`, `register`, repo URL, **pinned SHA**, author metadata. `docs/design-rationale.md` if the catalog copy cites research.
5. Save the PR URL. Put it in Typeform.

Do not wait for catalog CI to go green before Typeform.

---

## 5. Do not

- Do **not** capture a gym / location / bank / screen-time commitment. Oracle **refuses** those. That is correct. Do not “fix” it.
- Do **not** install ten plugins. Git + (optional) Calendar is the demo. Notion, Linear, Gmail, kanban, Drive, Sheets — not tonight.
- Do **not** add features, settlers, Path A history seeding, offer-to-track, backfill, or SPEC stretch (M6).
- Do **not** invent past weeks or a fake percentage.
- Do **not** spend the last hour on catalog copy, ECC, or doctoring Wayland.
- Do **not** miss Typeform because you wanted a prettier video.

**Done** means: code is on GitHub, Typeform is submitted with a video URL and a repo/PR URL, X post tags @NousResearch. Everything else is optional.
