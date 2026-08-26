#!/usr/bin/env bash
# Download the gated MVA hackathon dataset (~85 GB) into ./data.
# Resumable: re-run after any interruption, completed files are skipped.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data logs
export HF_XET_HIGH_PERFORMANCE=1
uv run hf download SageBio/mva-hackathon-2026-data \
  --repo-type dataset --local-dir data --max-workers 8 \
  2>&1 | tee -a logs/download.log
uv run python scripts/verify_data.py
