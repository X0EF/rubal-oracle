#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v hermes >/dev/null 2>&1; then
  echo "WARN: hermes CLI not found; skip catalog validate"
  exit 0
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

rsync -a \
  --exclude='.git/' \
  --exclude='.cursor/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  --exclude='.mypy_cache/' \
  --exclude='.ruff_cache/' \
  --exclude='node_modules/' \
  "$ROOT/" "$TMPDIR/"

echo "== hermes plugins validate (catalog sync) =="
hermes plugins validate "$TMPDIR"

echo "OK"
