#!/usr/bin/env bash
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-latest-20260921
source scripts/track2_expansion_env.sh
UV=/home/prachh/v/bin/uv
mkdir -p envs/esm envs/af3
cp scripts/track2_latest_esm_environment.toml envs/esm/pyproject.toml
cp scripts/track2_latest_af3_environment.toml envs/af3/pyproject.toml
"$UV" sync --project envs/esm > logs/esm-setup.log 2>&1 &
ESM_SETUP_PID=$!
"$UV" sync --project envs/af3 > logs/af3-setup.log 2>&1 &
AF3_SETUP_PID=$!
ESM_EXIT=0
AF3_EXIT=0
wait "$ESM_SETUP_PID" || ESM_EXIT=$?
wait "$AF3_SETUP_PID" || AF3_EXIT=$?
echo "esm=$ESM_EXIT af3=$AF3_EXIT"
test "$ESM_EXIT" -eq 0 && test "$AF3_EXIT" -eq 0
