#!/bin/bash
# Make this deck fully self-contained for GitHub Pages.
# Run from the deck folder: bash scripts/export.sh
# What it does:
#   1. Replaces the music symlink with a real copy of the MP3s
#   2. Reminds you of the remaining ship checklist
set -e
cd "$(dirname "$0")/.."

if [ -L music ]; then
  TARGET="$(readlink music)"
  rm music
  mkdir music
  cp "$TARGET"/*.mp3 music/
  echo "Replaced symlink with real copies: $(ls music | wc -l | tr -d ' ') tracks"
elif [ -d music ]; then
  echo "music/ is already a real folder. Nothing to do."
else
  echo "No music/ here. If this deck has no timers, that is fine."
fi

cat <<'CHECKLIST'

Ship checklist (see CLAUDE.md section: Publishing a finished deck):
  [ ] Deck file is named index.html
  [ ] og-image.png regenerated for this workshop (scripts/build-og-image.py)
  [ ] Head meta: [Workshop Name] and [One-line promise] placeholders replaced
  [ ] og:image / twitter:image switched to the absolute Pages URL after deploy
  [ ] README.md written (title, promise, live URL, date, audience, contact)
  [ ] All asset paths relative; test by opening from a sibling folder
  [ ] Move folder from WIP/ to GitHub Pages/ and push to its own repo
CHECKLIST
