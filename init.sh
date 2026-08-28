#!/usr/bin/env bash
# Standard startup + verification. Must pass before claiming any feature done.
set -euo pipefail
cd "$(dirname "$0")"
unset VIRTUAL_ENV || true

echo "=== 1. uv environment ==="
uv sync --quiet
uv run python -c "import huggingface_hub as h; print('huggingface_hub', h.__version__)"

echo "=== 2. no subject data in git ==="
./scripts/no_data_in_git.sh

echo "=== 3. verify_data self-check ==="
uv run python scripts/verify_data.py --self-check

echo "=== 4. dataset integrity ==="
if [ -d data ] && [ -n "$(ls -A data 2>/dev/null)" ]; then
  if ! uv run python scripts/verify_data.py; then
    echo "  FAIL: dataset incomplete or truncated - re-run ./scripts/download_data.sh"
    echo "  No feature may be claimed done against an unverified dataset."
    exit 1
  fi
else
  echo "  data/ empty - run ./scripts/download_data.sh (analysis features cannot start)"
fi

echo "=== OK ==="
