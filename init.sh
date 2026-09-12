#!/usr/bin/env bash
# Standard startup + verification. Must pass before claiming any feature done.
set -euo pipefail
cd "$(dirname "$0")"
unset VIRTUAL_ENV || true
# Keep bootstrap writable and self-contained in restricted agent environments.
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.uv-cache}"

echo "=== 1. uv environment ==="
uv sync --quiet
uv run python -c "import huggingface_hub as h; print('huggingface_hub', h.__version__)"

echo "=== 2. no subject data in git ==="
HOOK_PATH=$(git rev-parse --git-path hooks/pre-commit)
if [[ ! -e "$HOOK_PATH" && ! -L "$HOOK_PATH" ]]; then
  mkdir -p "$(dirname "$HOOK_PATH")"
  ln -s "$PWD/scripts/no_data_in_git.sh" "$HOOK_PATH"
fi
if [[ ! -x "$HOOK_PATH" || $(readlink -f "$HOOK_PATH") != "$PWD/scripts/no_data_in_git.sh" ]]; then
  echo "FAIL: pre-commit hook is not the executable repository data gate."
  echo "Existing hook preserved; integrate it with scripts/no_data_in_git.sh before continuing."
  exit 1
fi
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

echo "=== 5. local bioinformatics toolchain ==="
uv run bash ./scripts/get_tools.sh --check

echo "=== 6. offline annotation resources ==="
./scripts/get_resources.sh --check

echo "=== OK ==="
