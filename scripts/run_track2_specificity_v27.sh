#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-falsification-20261001-v27
ENV_ROOT=/home/prachh/v/mva-track2-transcriptome-20260927
UV=/home/prachh/v/bin/uv
cd "$TASK_ROOT"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache" CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1
for ((i=0;i<360;i++)); do
  [[ -f outputs/protein-complete.txt ]] && break
  sleep 10
done
test -f outputs/protein-complete.txt
nvidia-smi --query-gpu=index,uuid,name,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/specificity-prelaunch-gpus.csv
awk -F, '$4+0>1000 || $5+0>5 {bad=1} END {exit bad}' outputs/specificity-prelaunch-gpus.csv
nvidia-smi --query-gpu=timestamp,index,uuid,utilization.gpu,memory.used,power.draw --format=csv --loop=1 > logs/specificity-gpu-monitor.csv &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_specificity_v27.py "$TASK_ROOT" --shard "$gpu" --gpu "$gpu" > "logs/specificity-$gpu.log" 2>&1 &
  pids+=("$!")
done
printf '%s\n' "${pids[@]}" > outputs/specificity-pids.txt
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/specificity-postrun-gpus.csv
date -u +%FT%TZ > outputs/specificity-complete.txt
