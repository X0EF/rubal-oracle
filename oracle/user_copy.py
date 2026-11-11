"""User-facing help and onboarding (inject + /oracle help)."""

USER_HELP = """Oracle is a Hermes plugin. You give it a goal and a deadline. Later it looks at git or Google Calendar to see whether you actually did the thing. It does not take your word for it.

Talk in the chat. You do not have to type a slash command. Say what you will do, when it is due, and how we should check. Hermes will save that (the tool is oracle_commit). If your message already sounds like a plan, Oracle may ask before saving. Nothing is stored until you agree.

How we check depends on the kind of goal.

Shipping code, a PR, a commit, or a named test uses git. You do not add another plugin for that. Name a real repo path on this machine, then pick one done rule and keep it:
- a commit whose subject contains a word you choose (for example "search")
- a merged pull request whose title or branch matches
- commits that touch paths you named
- a named test that passed

If the goal is "this meeting or block has to exist on my calendar," use Google Calendar. Connect the Hermes Google Calendar plugin (Google Workspace Calendar). Email-only Google login does not count. We look for an event whose title matches, inside the start and end you named. A calendar event only proves the event exists. It does not prove you went to the gym.

We refuse gym, bank, Gmail, location, and screen time. There is no checker for those here.

After the deadline we run the checker. The result is met (proof matched), not met (we could read git or Calendar and the bar was not hit), or couldn't verify (the source was unreadable). Couldn't verify is not the same as failing.

/oracle status lists what is open. /oracle help prints this again.
"""

EMPTY_STORE_STATUS = "Nothing tracked yet.\n\n" + USER_HELP

HELP_INJECT = (
    "[Oracle — show the following explanation to the user verbatim. "
    "Do not replace it with a one-line status. Do not call oracle_status instead.]\n"
    + USER_HELP
)

FIRST_TURN_ONBOARDING = (
    "[Oracle — explain this in ordinary sentences, not a slogan. A bit of length is fine.] "
    "Oracle is this plugin. The user talks in chat about a goal, a deadline, and how we will check. "
    "Hermes saves it; they do not need a slash command. "
    "Checking is either git (a repo path plus a done rule: matching commit, merged PR, paths, or a named test) "
    "or Google Calendar (Hermes Calendar plugin connected, then a matching event in a window). "
    "We will not take gym, bank, or location goals. After the deadline we say met, not met, or couldn't verify."
)

TRACK_OFFER_USER = (
    "That sounds like a plan. Want Oracle to track it? "
    "If they say yes, Hermes can save it from this chat. "
    "We still need what they will do, a deadline, and how we check: git (repo plus a done rule) "
    "or Google Calendar (Calendar plugin plus a matching event). "
    "Do not save anything until they agree."
)
