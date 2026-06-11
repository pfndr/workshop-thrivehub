#!/bin/bash
# Link the canonical music library into this deck (WIP mode, zero duplication).
# Run once from the deck folder: bash scripts/setup-music.sh
# The deck's config.js expects LOFI_DIR = "./music/".
set -e
cd "$(dirname "$0")/.."

# Walk up until we find the repo root (the folder containing _assets/music)
ROOT="$PWD"
while [ ! -d "$ROOT/_assets/music" ]; do
  PARENT="$(dirname "$ROOT")"
  if [ "$PARENT" = "$ROOT" ]; then
    echo "Could not find _assets/music above $PWD" >&2
    exit 1
  fi
  ROOT="$PARENT"
done

if [ -e music ] || [ -L music ]; then
  echo "music already exists here. Remove it first if you want to re-link."
  exit 0
fi

# Relative symlink so the link survives folder moves, cloud sync, and different machines
REL="$(python3 -c "import os; print(os.path.relpath('$ROOT/_assets/music', '$PWD'))")"
ln -s "$REL" music
echo "Linked music -> $REL"
echo "Note: this is a symlink. Run scripts/export.sh before shipping to GitHub Pages."
