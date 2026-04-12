#!/usr/bin/env bash
set -euo pipefail

WS_DIR="${WS_DIR:-/home/ubuntu/ws_mikata_arm}"

cd "$WS_DIR"

for d in build install log; do
  path="$WS_DIR/$d"
  if [ -d "$path" ]; then
    echo "[clean] Removing contents of: $path"
    sudo find "$path" -mindepth 1 -delete
  else
    echo "[clean] Skip (not found): $path"
  fi
done

echo "[clean] Done."
