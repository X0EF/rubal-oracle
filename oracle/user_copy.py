"""User-facing help and onboarding (inject + /oracle help). Plain language only."""

USER_HELP = """Oracle — Hermes tracks commitments you choose.

You do not need a slash command. Say in chat what you'll do, by when, and how we'll check. Hermes saves it.

Proof — pick the matching source:

• Code / ship work → Git (no extra plugin). Name the repo path and what "done" means:
  matching commit subject, merged PR, files changed, or a named test passing.

• A meeting or calendar block that must exist → Hermes Google Calendar plugin
  (Google Workspace Calendar; email-only setup does not count). We look for a
  matching event in the window you name.

Not this version: gym/location, bank, Gmail, screen time.

After the deadline we check that proof: met / not met / couldn't verify.

Optional:
  /oracle status  — what's open
  /oracle help    — this card
"""

EMPTY_STORE_STATUS = "Nothing tracked yet.\n\n" + USER_HELP

HELP_INJECT = (
    "[Oracle — show this card to the user verbatim. Do not replace it with a "
    "status one-liner. Do not call oracle_status instead of showing this.]\n"
    + USER_HELP
)

FIRST_TURN_ONBOARDING = (
    "[Oracle — tell the user in plain words, ~4 sentences] "
    "Oracle helps you stick to goals you pick. Just say them in chat — Hermes captures; "
    "no slash command required. "
    "Proof is either Git (name a repo + how we'll know it's done) or Google Calendar "
    "(connect the Hermes Calendar plugin, then a matching event). "
    "Set a deadline. We verify from that data later — not vibes. /oracle help lists proof types."
)

TRACK_OFFER_USER = (
    "Sounds like a plan. Want Oracle to track it? "
    "Hermes can save it from this chat if they agree. "
    "Need: what you'll do, a deadline, and proof — Git (repo + done rule) or "
    "Google Calendar (Calendar plugin + matching event). "
    "Nothing is saved until they agree."
)
