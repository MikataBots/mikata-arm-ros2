#!/usr/bin/env bash
set -euo pipefail

# Ensure ROS 2 environment is available
# NOTE: ROS setup scripts may reference unset vars; don't run them under `set -u`.
if [ -f "/opt/ros/humble/setup.bash" ]; then
  # shellcheck disable=SC1091
  set +u
  source "/opt/ros/humble/setup.bash"
  set -u
fi

WS_DIR="/home/ros/ws_mikata_arm"
cd "$WS_DIR"

# Named volumes are typically mounted as root:root. Make sure this user can write.
sudo mkdir -p "$WS_DIR/build" "$WS_DIR/install" "$WS_DIR/log"
if [ ! -w "$WS_DIR/build" ] || [ ! -w "$WS_DIR/install" ] || [ ! -w "$WS_DIR/log" ]; then
  sudo chown -R "$(id -u)":"$(id -g)" "$WS_DIR/build" "$WS_DIR/install" "$WS_DIR/log"
fi

# Build on container start so the environment is ready to use.
# Skip build if install/setup.bash exists and no source files have changed since last build.
if [ ! -d "$WS_DIR/src" ]; then
  echo "No src directory found. Skipping build."
elif ! command -v colcon >/dev/null 2>&1; then
  echo "ERROR: colcon is not installed. Install python3-colcon-common-extensions in the image." >&2
  exit 1
else
  NEED_BUILD=0
  
  if [ ! -f "$WS_DIR/install/setup.bash" ]; then
    # First run - need to build
    NEED_BUILD=1
    echo "First run detected. Building workspace..."
  elif [ "${FORCE_BUILD:-0}" = "1" ]; then
    # Force build requested via environment variable
    NEED_BUILD=1
    echo "Force build requested. Building workspace..."
  else
    # Check if any source files are newer than install/setup.bash
    if find "$WS_DIR/src" -type f -newer "$WS_DIR/install/setup.bash" 2>/dev/null | grep -q .; then
      NEED_BUILD=1
      echo "Source changes detected. Building workspace..."
    else
      echo "No source changes detected. Skipping build."
    fi
  fi
  
  if [ "$NEED_BUILD" = "1" ]; then
    colcon build --symlink-install
  fi
fi

# Source workspace overlay for interactive shells and for any following commands.
# NOTE: Colcon-generated setup scripts may reference unset vars; don't run them under `set -u`.
if [ -f "$WS_DIR/install/setup.bash" ]; then
  # shellcheck disable=SC1091
  set +u
  source "$WS_DIR/install/setup.bash"
  set -u

  BASHRC="/home/ros/.bashrc"
  LINE="source $WS_DIR/install/setup.bash"
  if [ -f "$BASHRC" ] && ! grep -qxF "$LINE" "$BASHRC"; then
    echo "$LINE" >> "$BASHRC"
  fi
fi

exec "$@"
