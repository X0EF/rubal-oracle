#!/usr/bin/env bash
# After a plugin change: commit → reinstall → handler check → hermes chat -q --oneshot.
# Oneshot is an LLM turn (what you see in CLI). That is part of the verdict.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL="${HERMES_PLUGIN_INSTALL:-$HOME/.hermes/plugins/rubal-oracle}"
HERMES_SRC="${HERMES_SRC:-$HOME/.hermes/hermes-agent}"

if ! command -v hermes >/dev/null 2>&1; then
  echo "FAIL: hermes CLI not on PATH"
  exit 1
fi

if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "FAIL: working tree dirty — file:// install clones git, so Hermes would miss these files:"
  git -C "$ROOT" status --porcelain
  echo "Commit (or stash) first, then re-run."
  exit 1
fi

echo "== doctor (repo) =="
hermes plugins doctor "$ROOT" --ci

echo "== reinstall =="
hermes plugins remove rubal-oracle || true
hermes plugins install "file://${ROOT}" --enable --yes-deps

echo "== gateway restart (chat -q uses gateway-loaded tools; install defers them) =="
hermes gateway restart
for _ in $(seq 1 15); do
  if hermes gateway status 2>/dev/null | grep -q "active (running)"; then
    break
  fi
  sleep 2
done

echo "== doctor (install) =="
hermes plugins doctor "$INSTALL" --ci

HEAD="$(git -C "$ROOT" rev-parse --short HEAD)"
INSTALLED="$(git -C "$INSTALL" rev-parse --short HEAD 2>/dev/null || echo missing)"
if [[ "$HEAD" != "$INSTALLED" ]]; then
  echo "FAIL: install SHA $INSTALLED != repo $HEAD"
  exit 1
fi
if [[ ! -f "$INSTALL/oracle/user_copy.py" ]]; then
  echo "FAIL: install missing oracle/user_copy.py"
  exit 1
fi

PY=""
for cand in \
  "$HOME/.hermes/installs/"*/environments/*/venv/bin/python3 \
  "$HERMES_SRC/.hermes/bin/python3"; do
  if [[ -x "$cand" ]]; then PY="$cand"; break; fi
done
if [[ -z "$PY" ]]; then PY="$(command -v python3)"; fi

echo "== plugin handler /oracle help =="
HELP_OUT="$("$PY" - "$HERMES_SRC" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
from hermes_cli.plugin_command_dispatch import invoke_plugin_command
from hermes_cli.plugins import (
    get_plugin_command_handler,
    resolve_plugin_command_result,
    _ensure_plugins_discovered,
)
_ensure_plugins_discovered()
h = get_plugin_command_handler("oracle")
if h is None:
    print("FAIL: no /oracle plugin command registered", file=sys.stderr)
    sys.exit(1)
text = str(resolve_plugin_command_result(invoke_plugin_command(h, "help")) or "")
sys.stdout.write(text)
PY
)"
echo "$HELP_OUT"
echo "$HELP_OUT" | grep -qi "Hermes will save" || {
  echo "FAIL: handler help missing 'Hermes will save'"
  exit 1
}

_chat_shows_howto() {
  local label="$1"
  local query="$2"
  echo "== hermes chat -q --oneshot ($label) =="
  echo "Q: $query"
  local out rc=0
  out="$(cd "$ROOT" && hermes chat -q "$query" --oneshot -Q --max-turns 8 --run-budget 180)" || rc=$?
  echo "$out"
  if [[ "$rc" -ne 0 ]]; then
    echo "FAIL: hermes chat exited $rc ($label)"
    exit 1
  fi
  local body
  body="$(printf '%s\n' "$out" | grep -v '^session_id:')"
  if printf '%s\n' "$body" | grep -qiE 'Hermes will save|Google Calendar|Nothing tracked|oracle_commit'; then
    echo "OK chat: $label"
    return 0
  fi
  echo "FAIL chat: $label — CLI response did not show how to use Oracle / proof types"
  exit 1
}

_chat_shows_howto "slash-as-message" "/oracle help"
_chat_shows_howto "plain-question" "How do I use Oracle? What proof can I use for a commitment?"

echo "OK: install $INSTALLED — handler + hermes chat -q oneshot both show how-to."
