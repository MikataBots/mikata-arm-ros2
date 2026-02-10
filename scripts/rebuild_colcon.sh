#!/usr/bin/env bash
set -euo pipefail

WS_DIR="${WS_DIR:-/home/ros/ws_mikata_arm}"
REPO_DIR="$WS_DIR/src/mikata-arm-ros2"

cd "$WS_DIR"

if ! command -v colcon >/dev/null 2>&1; then
  echo "ERROR: colcon is not installed in this container." >&2
  exit 1
fi

if [ -f "$REPO_DIR/scripts/clean_colcon_artifacts.sh" ]; then
  bash "$REPO_DIR/scripts/clean_colcon_artifacts.sh"
else
  echo "WARN: clean script not found at $REPO_DIR/scripts/clean_colcon_artifacts.sh" >&2
  echo "      Skipping clean step." >&2
fi

echo "[rebuild] Building workspace..."
colcon build --symlink-install

echo "[rebuild] Build finished. To use the overlay in the current shell:"
echo "  source $WS_DIR/install/setup.bash"
