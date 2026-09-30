#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-falsification-20261001-v27
ENV_ROOT=/home/prachh/v/mva-track2-expanded-latest-20260921/envs/esm
UV=/home/prachh/v/bin/uv
cd "$TASK_ROOT"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache" CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=index,uuid,name,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/prelaunch-gpus.csv
awk -F, '$4+0>1000 || $5+0>5 {bad=1} END {exit bad}' outputs/prelaunch-gpus.csv
nvidia-smi --query-gpu=timestamp,index,uuid,utilization.gpu,memory.used,power.draw --format=csv --loop=1 > logs/gpu-monitor.csv &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_saturation_v27.py "$TASK_ROOT" --shard "$gpu" > "logs/protein-$gpu.log" 2>&1 &
  pids+=("$!")
done
printf '%s\n' "${pids[@]}" > outputs/worker-pids.txt
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/postrun-gpus.csv
date -u +%FT%TZ > outputs/protein-complete.txt
