#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-rnai-20260927-v23
cd "$TASK_ROOT"
UV=/home/prachh/v/bin/uv
export UV_CACHE_DIR="$TASK_ROOT/cache/uv"
export XDG_CACHE_HOME="$TASK_ROOT/cache"
export CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1
# Reuse the already pinned environment read-only; reproduction can uv sync --frozen here.
ENV_ROOT=/home/prachh/v/mva-track2-transcriptome-20260927
for ((i=0;i<360;i++)); do
  [[ -f outputs/download-complete.txt ]] && break
  sleep 10
done
test -f outputs/download-complete.txt
"$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_rnai_v23.py prepare "$TASK_ROOT" > logs/prepare.log 2>&1
nvidia-smi --query-gpu=index,uuid,name,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/prelaunch-gpus.csv
awk -F, '$4+0>1000 || $5+0>5 {bad=1} END {exit bad}' outputs/prelaunch-gpus.csv
nvidia-smi --query-gpu=timestamp,index,uuid,utilization.gpu,memory.used,power.draw --format=csv --loop=1 > logs/gpu-monitor.csv &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_rnai_v23.py worker "$TASK_ROOT" --shard "$gpu" > "logs/gpu-$gpu.log" 2>&1 &
  pids+=("$!")
done
printf '%s\n' "${pids[@]}" > outputs/worker-pids.txt
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
"$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_rnai_v23.py aggregate "$TASK_ROOT" > logs/aggregate.log 2>&1
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/postrun-gpus.csv
date -u +%FT%TZ > outputs/complete.txt
