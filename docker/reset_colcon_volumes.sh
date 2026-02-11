#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

echo "This will remove named volumes (build/install/log) used by docker/docker-compose.yml."
echo "All persisted colcon artifacts will be deleted."
echo

read -r -p "Proceed? [y/N] " ans
case "${ans:-}" in
  y|Y) ;;
  *) echo "Aborted."; exit 1;;
esac

docker compose -f docker/docker-compose.yml down -v

echo "Volumes removed. Next start the container again (e.g. docker compose up -d)."
