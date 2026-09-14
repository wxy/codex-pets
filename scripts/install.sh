#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PET_ID="${1:-crt-monitor}"
SOURCE="$ROOT/pets/$PET_ID"
DEST="${CODEX_HOME:-$HOME/.codex}/pets/$PET_ID"

if [[ ! "$PET_ID" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || [[ ! -f "$SOURCE/pet.json" ]] || [[ ! -f "$SOURCE/spritesheet.webp" ]]; then
  echo "Unknown pet: $PET_ID" >&2
  echo "Available pets:" >&2
  find "$ROOT/pets" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort >&2
  exit 1
fi

mkdir -p "$DEST"
cp "$SOURCE/pet.json" "$DEST/pet.json"
cp "$SOURCE/spritesheet.webp" "$DEST/spritesheet.webp"

echo "Installed pet '$PET_ID' to: $DEST"
echo "Restart Codex and select it under Settings -> Appearance -> Pets."
