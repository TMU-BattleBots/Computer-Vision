#!/usr/bin/env bash
set -euo pipefail

# Fast Raspberry Pi run script for day-to-day use.
# Assumes initial setup was completed with scripts/pi_setup_and_run.sh.
# Usage examples:
#   ./scripts/pi_run.sh
#   HEADLESS=1 ./scripts/pi_run.sh --camera-index 0 --target-id 7

if [[ ! -d ".venv" ]]; then
  echo "Error: .venv was not found. Run ./scripts/pi_setup_and_run.sh first." >&2
  exit 1
fi

source .venv/bin/activate

EXTRA_ARGS=()
if [[ "${HEADLESS:-0}" == "1" ]]; then
  EXTRA_ARGS+=(--no-preview)
fi

exec python -m vision.mvp_runner "${EXTRA_ARGS[@]}" "$@"