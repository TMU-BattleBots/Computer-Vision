#!/usr/bin/env bash
set -euo pipefail

# One-command Raspberry Pi bootstrap + run script.
# Usage examples:
#   ./scripts/pi_setup_and_run.sh
#   HEADLESS=1 ./scripts/pi_setup_and_run.sh --camera-index 0 --target-id 7

sudo apt-get update
sudo apt-get install -y \
  python3-venv \
  libatlas-base-dev \
  libjpeg62-turbo \
  libopenjp2-7 \
  libtiff6 \
  libgtk-3-0

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-pi.txt

EXTRA_ARGS=()
if [[ "${HEADLESS:-0}" == "1" ]]; then
  EXTRA_ARGS+=(--no-preview)
fi

exec python -m vision.mvp_runner "${EXTRA_ARGS[@]}" "$@"