# DEMO_VIDEO — rubal-oracle hackathon launch (<90s)

> Audience: Hermes hackathon judges + Typeform submission.  
> Feel: Apple product film — full black, big type, UI chrome as hero.  
> No talking head. No watermarks.

---

## 1. Tooling (how to produce without watermarks)

### Recommended stack

| Layer | Tool | Why |
|---|---|---|
| **Truth layer** (product proof) | Owner screen-records Hermes CLI or Hermes Desktop directly | Only this shows the real product — real injection, real settle, real refuse |
| **Motion/title layer** (the "Apple" polish) | Self-contained `demo.html` built from the `frontend-slides` skill | Zero-dependency HTML + CSS + JS — plays locally, no watermark, no account |
| **Stitch** | `ffmpeg` | Free, runs locally: `ffmpeg -i titles.mp4 -i hermes.mp4 -filter_complex concat demo.mp4` |
| **Screen capture** | `ffmpeg -f x11grab` (Linux) or OBS Studio | Both free, no watermarks |

### What NOT to use

- **Luma, Runway, Kling, Pika, Sora** — all watermark free-tier exports. Even if a workaround exists tonight, the risk of a watermarked submission is not worth the time.
- **Cursor `GenerateVideo`** — watermark status is **unknown** as of this writing. Do not assume it is clean; confirm before using in a submission context.
- **Canva, CapCut free tier** — watermarked.

### Minimum-viable night-of workflow

```
1. Build demo.html (titles + motion frames) — ~30 min.
   Run: xdg-open docs/demo.html
   Record: ffmpeg -f x11grab -s 1920x1080 -i :0.0 -r 30 titles.mp4

2. Record Hermes terminal session for each product beat — ~20 min.
   Use a tmux session with large font (20pt+), dark terminal, no tab bar.
   Record: ffmpeg -f x11grab -s 1920x1080 -i :0.0 -r 30 hermes.mp4

3. Edit in Kdenlive (free, Linux, no watermark) or splice with ffmpeg.
   Total render: < 5 min.
```

---

## 2. Beat sheet (0–90s)

Each beat maps to a real product behaviour. No manufactured feature is shown.

| Time | Beat | What happens on screen | Product truth |
|---|---|---|---|
| 0–7s | **Hook** | Black. Single line fades in: *"You made a plan."* Pause. Second line: *"Again."* | Establishes the planning-fallacy tension — product's core rationale |
| 7–14s | **Contrast** | Cut. White text: *"Most assistants help you make plans."* Hard cut to next line: *"This one checks whether you did it."* | Direct product pitch from SPEC |
| 14–28s | **Beat 1 — Capture (git)** | Hermes terminal live. User types naturally: *"I want to ship the auth refactor this week — commit with 'auth' in the message by Friday."* Oracle intercept appears above the reply: `Oracle — tracking: auth refactor · settler: git commit · deadline: Fri` Cursor blinks. | `pre_llm_call` hook, `/oracle` capture, git settler — all shipped |
| 28–40s | **Beat 2 — Capture (calendar)** | Hermes terminal. User: *"Put the demo review on the calendar Thursday afternoon."* Oracle line: `Oracle — tracking: demo review · settler: calendar event · deadline: Thu 18:00` | Calendar settler — shipped if Calendar plugin `ok` |
| 40–50s | **Beat 3 — The honest refuse** | User: *"Track that I go to the gym Monday."* Oracle responds — full-screen UI chrome: `Oracle — refused. No proof source for gym or location. Git and Calendar only.` Subtitle: *"No proof source. We say so."* | COMMITMENT_SOURCES.md rows 19–20: gym is explicitly refused |
| 50–63s | **Beat 4 — Forecast inject** | New Hermes session, different message (e.g. "what should I focus on today"). Oracle inject appears at top of context — shown as a dim card: `Open: auth refactor · 40% · 3 similar weeks, 1 shipped on time · calendar packed Thu–Fri` Hermes reply arrives below it, informed. | `pre_llm_call` hook — inject with outside-view reasoning, not invented |
| 63–73s | **Beat 5 — Path B (subtract)** | Oracle card updates. New line appears: `Suggest: smaller scope — auth middleware only?` User types: `yes`. Oracle: `Revision logged. Original on record.` | Subtract offer — product hypothesis, logged; original not erased |
| 73–83s | **Beat 6 — Settle** | Friday. Timer style: *"Friday. Deadline."* Cut to terminal: `/oracle status` → `Settling auth refactor…` Git checked. Result appears large: `met` — green, no animation flourish, just the word. | Settler runs, outcome is met/not met/couldn't verify |
| 83–90s | **Close** | Full black. Tagline in large type, one word at a time: *"It predicts you."* Pause. *"Then helps you beat it."* Product name small below: `rubal-oracle · hermes plugin` | — |

---

## 3. Shot list

Every shot is described as: **what is on screen / type treatment / motion direction**.

Apple-ish constraint: black background, one idea per frame, type as hero, UI chrome only when it carries information.

### Shot 1 — Hook (0–7s)

- **Screen:** Full black. `SF Pro Display` or `Inter` weight 700, 96px, white, centered.
- **Line 1:** "You made a plan." — fades in over 0.6s, holds 1.5s.
- **Line 2:** "Again." — fades in 0.4s, sits below, slightly smaller (72px), holds 2s.
- **Motion:** No slide. Opacity only. Silence or low drone audio.

### Shot 2 — Contrast (7–14s)

- **Screen:** Full black. Two lines, staggered.
- **Line 1:** "Most assistants help you make plans." — 48px, weight 400, dim white (rgba 255,255,255,0.6).
- **Line 2:** "This one checks whether you did it." — 64px, weight 700, full white. Appears 1s after line 1.
- **Motion:** Line 2 rises 8px on enter (translateY -8px → 0). No bounce.

### Shot 3 — Capture / git (14–28s)

- **Screen:** Hermes terminal, full-bleed, large font. Dark terminal chrome only — no tab bar, no window decoration if possible. Crop to the chat area.
- **UI beat:** Oracle intercept block appears above Hermes reply — styled differently (dim border, monospace, `Oracle —` prefix). Should look like a system annotation, not a reply.
- **Motion:** The Oracle line types in character by character (~80ms/char). Hermes reply below fades in after Oracle settles.
- **Label overlay (optional):** Small bottom-left caption: `git settler` — 14px, rgba white 0.5, fades out after 2s.

### Shot 4 — Capture / calendar (28–40s)

- **Screen:** Same terminal. Different message.
- **Motion:** Same intercept animation. Calendar settler label.
- **Cut:** Hard cut from git shot. No transition — mirrors Apple hardware cuts.

### Shot 5 — The honest refuse (40–50s)

- **Screen:** Terminal OR a minimal full-bleed UI card. If using a card: black background, single text block, left-aligned, 48px weight 700 white, subtitle 24px weight 400 dim.
- **Primary text:** `refused.`
- **Secondary text:** `No proof source for gym or location. Git and Calendar only.`
- **Motion:** Text clips in from left (clipPath or translateX). Hold 4s.
- **Why this beat matters:** Shows honesty. Do not cut it. Judges will notice if gym is claimed as working.

### Shot 6 — Forecast inject (50–63s)

- **Screen:** Hermes terminal. Oracle inject renders as a dim horizontal card at the top of the reply area. Show enough to read the odds and the "3 similar weeks" reasoning.
- **Key UI element to show:** The odds (`40%`) and the reason (`calendar packed`) — these distinguish Oracle from a reminder app.
- **Motion:** Card slides down from top edge, settles. Hermes reply types in below it normally.
- **Do NOT animate the 40% number counting up** — this implies precision we do not have.

### Shot 7 — Subtract / Path B (63–73s)

- **Screen:** Terminal or card. Oracle suggestion appears as a single additional line.
- **Text:** `Suggest: smaller scope — auth middleware only?`
- **User response:** `yes` typed, Oracle confirms: `Revision logged. Original on record.`
- **Motion:** Both lines appear as terminal output — no card animation needed here.
- **Keep this brief.** One exchange. Do not over-explain the subtract hypothesis.

### Shot 8 — Settle (73–83s)

- **Screen:** Two beats. First: full-black title card — `Friday.` in large type (80px), hold 1s. Second: terminal showing `/oracle status` output scrolling to `met`.
- **The word `met`:** Display it at 96px, weight 700, white — the same scale as the hook. No green colour unless it reads clearly on film. Simple is better.
- **Motion:** `met` fades in, no bounce, no particle effect.

### Shot 9 — Close (83–90s)

- **Screen:** Full black. Tagline, word by word.
- **Line 1:** "It predicts you." — weight 700, 72px, appears word by word (0.2s each).
- **Line 2 (pause 0.8s):** "Then helps you beat it." — same treatment.
- **Product name:** `rubal-oracle` — 20px, weight 400, dim white, fades in last.
- **Motion:** No logo animation. No sparkle. The stillness is the tone.

---

## 4. Scripts

### 4a. Optional voice-over (sparse — key beats only)

Use VO only on beats where the screen alone is ambiguous. No VO on the refuse beat — let it land silently.

```
[0–7s — silence]

[7–14s]
"Most assistants help you plan. This one checks whether you did it."

[14–28s — silence, let the UI speak]

[40–50s]
"Gym? Refused. No proof source. Git and Calendar only."

[50–63s]
"Before Hermes replies — your open bets, and odds from similar past weeks.
Calendar packed. Forty percent."

[73–83s]
"Friday. Git checked."

[83–90s — silence]
```

VO style: flat, dry, no announcement energy. Think Jony Ive 2013 cadence, not startup pitch.

---

### 4b. Silent version (titles only — preferred)

This version works without audio and is the safer submission default.

| Time | Full-screen title card |
|---|---|
| 0–7s | You made a plan. / Again. |
| 7–14s | Most assistants help you make plans. / **This one checks whether you did it.** |
| 14–28s | *(no title — UI only)* |
| 28–40s | *(no title — UI only)* |
| 40–50s | **refused.** / No proof source for gym or location. Git and Calendar only. |
| 50–63s | *(no title — Oracle inject card carries the message)* |
| 63–73s | *(no title)* |
| 73–83s | Friday. / **met.** |
| 83–90s | It predicts you. / Then helps you beat it. / `rubal-oracle` |

---

## 5. Critique pass — what to cut or not claim

This pass applies the product's own honesty rules to the video. If the SPEC says we cannot claim it, the video cannot show it.

| Element | Verdict | Reason |
|---|---|---|
| Gym commitment tracked live | ❌ **Cut** | Rows 19–20 in COMMITMENT_SOURCES.md: refused, no proof source. Showing it would be a lie. |
| "20 live APIs" montage | ❌ **Cut** | COMMITMENT_SOURCES says 6 more settlers are TODO; only git + calendar are shipped. A plugin montage overclaims. |
| Counting 40% number animating up | ❌ **Cut** | Implies calibration precision. SPEC: "With one or two outcomes, we do not claim Oracle is well calibrated." |
| "Oracle is well calibrated" or Brier score claims | ❌ **Cut** | Same: not claimable from a few personal history points. |
| Showing GitHub issue / Linear / Notion done | ⚠️ **Only with disclaimer** | These are fixture/TODO — show only if the settler is actually wired and tested tonight. Otherwise cut. |
| Oracle suggesting to go to gym / eat well / focus | ❌ **Cut** | Outside the product scope entirely. |
| Subtract offer (beat 5) | ✅ **Keep, brief** | Product hypothesis — honest as long as it is framed as a suggestion, not a proven intervention. |
| The refuse beat (beat 3) | ✅ **Keep, prominent** | This is a trust signal. Cutting it to look more capable is the wrong move in a hackathon. |
| "couldn't verify" outcome path | ✅ **Mention in help text if time** | Not required in the film — but do not hide it if judges ask. |
| Brier score or mirror screen | ⚠️ **Optional** | Fine if you have two or more settled outcomes with real data tonight; not fine if you are faking the numbers. |
| Tagline "It predicts you, then helps you beat the prediction." | ✅ **Keep** | Accurate summary of the core loop. |

### Hard-cut list (do not add these back under time pressure)

- Any live OAuth demonstration that was not tested end-to-end before the deadline.
- A "trusted by X users" or "X commitments tracked" stat unless the number is real.
- Any animation implying the forecast model is more sophisticated than a base-rate + calendar adjustment.
- A talking-head recording of you explaining the product — the SPEC and this film do the job.

---

## 6. Pre-flight checklist

Before submitting to Typeform:

- [ ] No third-party watermarks visible anywhere in the exported file
- [ ] Hermes terminal font is ≥ 18pt and readable at 720p
- [ ] The refuse beat (gym) is in the final cut
- [ ] No claim of a live settler that was not tested tonight
- [ ] Tagline appears verbatim in the close card
- [ ] File is under Typeform's size limit (check their form; usually 200MB for video)
- [ ] Export at 1920×1080, H.264, ~8 Mbps — readable on a judge's laptop screen
