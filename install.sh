#!/usr/bin/env bash
# Install the game-theory skill into a skills directory.
#
#   bash ./install.sh                 # -> ~/.workbuddy-ai/skills/game-theory
#   bash ./install.sh /path/to/skills # custom root
#   bash ./install.sh --force         # overwrite without asking
set -euo pipefail

FORCE=0
if [ "${1:-}" = "--force" ]; then
  FORCE=1
  shift
fi

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${1:-$HOME/.workbuddy-ai/skills}"
DEST="$ROOT/game-theory"

mkdir -p "$ROOT"

if [ -e "$DEST" ]; then
  if [ "$FORCE" -eq 0 ]; then
    if [ -t 0 ]; then
      printf 'Destination exists: %s\nOverwrite? [y/N] ' "$DEST"
      read -r ans
      case "$ans" in
        [yY]*) ;;
        *) echo "Aborted."; exit 1 ;;
      esac
    else
      echo "Destination exists: $DEST (re-run with --force to overwrite)" >&2
      exit 1
    fi
  fi
  rm -rf "$DEST"
fi

mkdir -p "$DEST"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git' --exclude '__pycache__' --exclude 'out' "$SRC/" "$DEST/"
else
  tar --exclude='.git' --exclude='__pycache__' --exclude='out' \
      -cf - -C "$SRC" . | tar -xf - -C "$DEST"
fi

echo "Installed to: $DEST"
echo "Verify with:  python \"$DEST/tests/run_tests.py\""
