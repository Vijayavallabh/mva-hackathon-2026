#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-orthogonal-20261006-v29
UV=/home/prachh/v/bin/uv
cd "$TASK_ROOT"
export UV_CACHE_DIR="$TASK_ROOT/cache/uv" UV_PYTHON_INSTALL_DIR="$TASK_ROOT/cache/python"
export MPNN_DIR="$TASK_ROOT/ProteinMPNN" MODEL_OPT_JIT_ROOT="$TASK_ROOT/cache/jit"
export MODEL_OPT_STATE="$TASK_ROOT/cache/model-state" PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache"
export CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda" TMPDIR="$TASK_ROOT/cache/tmp"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1 PYTHONHASHSEED=0
mkdir -p "$TMPDIR" "$MODEL_OPT_JIT_ROOT"
test -f outputs/setup-complete.txt
if [[ ! -f outputs/prepare-complete.txt ]]; then
  "$UV" run --project "$TASK_ROOT" --no-sync python scripts/track2_orthogonal_v29.py prepare "$TASK_ROOT"
fi
nvidia-smi --query-gpu=index,uuid,name,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/prelaunch-gpus.csv
awk -F, '$4+0>1000 || $5+0>5 {bad=1} END {exit bad}' outputs/prelaunch-gpus.csv
nvidia-smi --query-gpu=timestamp,index,uuid,utilization.gpu,memory.used,power.draw --format=csv --loop=1 > logs/gpu-monitor.csv &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT
CUDA_VISIBLE_DEVICES=0 "$UV" run --project "$TASK_ROOT" --no-sync python scripts/track2_orthogonal_v29.py pilot "$TASK_ROOT" > logs/pilot.log 2>&1
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --project "$TASK_ROOT" --no-sync python scripts/track2_orthogonal_v29.py run "$TASK_ROOT" --shard "$gpu" > "logs/mpnn-$gpu.log" 2>&1 &
  pids+=("$!")
done
printf '%s\n' "${pids[@]}" > outputs/mpnn-pids.txt
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
date -u +%FT%TZ > outputs/mpnn-complete.txt
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/mpnn-postrun-gpus.csv
