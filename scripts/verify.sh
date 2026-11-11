#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH=.
echo "== unittest =="
python3 -m unittest discover -s tests -p 'test_*.py' -q
echo "== hermes plugins doctor =="
if command -v hermes >/dev/null 2>&1; then
  hermes plugins doctor "$ROOT" --ci
  bash "$ROOT/scripts/catalog_validate.sh"
else
  echo "WARN: hermes CLI not found; skip doctor + catalog validate"
fi
echo "OK"
