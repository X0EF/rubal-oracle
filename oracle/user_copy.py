"""User-facing help and onboarding (inject + /oracle help). Plain language only."""

USER_HELP = """Oracle — stick to commitments you choose.

1. Make a commitment (what you'll do)
2. Link proof — git (matching commit) or Google Calendar (event exists)
3. Set a deadline

Later we check proof and say met / not met / couldn't verify.

Commands:
  /oracle status  — what's open
  /oracle help    — this card

Say in chat: "Track: ship X by Friday, checked with git in <repo>."
"""

FIRST_TURN_ONBOARDING = (
    "[Oracle — tell the user in plain words, ~3 sentences] "
    "Oracle helps you stick to goals you pick. "
    "Three steps: say what you'll do, choose proof (git or Calendar), set a deadline. "
    "We verify from data later — not vibes. Ask what they want to commit to, or use /oracle status."
)

TRACK_OFFER_USER = (
    "Sounds like a plan. Want Oracle to track it? "
    "You need: what you'll do, how we check (git or Calendar), and a deadline. "
    "Nothing is saved until they agree."
)
