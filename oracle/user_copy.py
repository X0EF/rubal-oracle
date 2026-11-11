"""User-facing help and onboarding (inject + /oracle help)."""

USER_HELP = """rubal-oracle is a Hermes plugin. Name a goal, a deadline, and how we check. Talk in chat; Hermes will save it. No slash command required.

Git (no extra plugin): a repo path plus one done rule — matching commit, merged PR, files touched, or a named test.

Google Calendar: connect Hermes Calendar / Google Workspace Calendar (not email-only). Matching event in your window, or an empty slot if that is the goal.

When that source is connected: GitHub (issue closed), Notion (task done), Linear (issue done), Gmail (email sent), kanban (card done), or Strava / Apple Health / athletedata (workout logged).

After the deadline: met, not met, or couldn't verify.

Rubal is the forecast. Enough similar past attempts → a % with those attempts named, adjusted for this week's calendar. If you are slipping we may suggest a smaller goal. We can also stay quiet.

/oracle status lists what is open. /oracle help prints this again.
"""

EMPTY_STORE_STATUS = "Nothing tracked yet.\n\n" + USER_HELP

HELP_INJECT = (
    "[Oracle — show the following explanation to the user verbatim. "
    "Do not replace it with a one-line status. Do not call oracle_status instead.]\n"
    + USER_HELP
)

FIRST_TURN_ONBOARDING = (
    "[Oracle — a few ordinary sentences.] "
    "rubal-oracle tracks a goal from chat (deadline + how we check). No slash required. "
    "Git = repo + done rule. Google Calendar = Hermes Calendar plugin + matching event. "
    "Also GitHub, Notion, Linear, Gmail, kanban, or Strava / Apple Health when that source is connected. "
    "Rubal = odds from similar past attempts, or we say we do not have enough history."
)

TRACK_OFFER_USER = (
    "That sounds like a plan. Want Oracle to track it? "
    "Need: what they will do, a deadline, and proof — Git, Google Calendar, GitHub, Notion, Linear, Gmail, kanban, Strava, or Apple Health. "
    "Nothing is saved until they agree."
)
