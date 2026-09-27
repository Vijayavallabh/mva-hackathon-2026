#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-transcriptome-20260927
cd "$TASK_ROOT"
export UV_CACHE_DIR="$TASK_ROOT/cache/uv"
export UV_PYTHON_INSTALL_DIR=/home/prachh/v/mva-track2-expanded-latest-20260921/python
export XDG_CACHE_HOME="$TASK_ROOT/cache"
export CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1
UV=/home/prachh/v/bin/uv
for ((i=0;i<720;i++)); do
  if [[ -f outputs/phase2-download-complete.txt && -f outputs/transcriptome-results.json ]]; then break; fi
  sleep 20
done
test -f outputs/transcriptome-results.json
test -f outputs/phase2-download-complete.txt
"$UV" run --no-sync python scripts/track2_transcriptome_phase2.py prepare "$TASK_ROOT" > logs/phase2-prepare.log 2>&1
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/phase2-prelaunch-gpus.csv
awk -F, '$2+0>1000 || $3+0>5 {bad=1} END {exit bad}' outputs/phase2-prelaunch-gpus.csv
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --no-sync python scripts/track2_transcriptome_phase2.py worker "$TASK_ROOT" --shard "$gpu" > "logs/phase2-gpu-$gpu.log" 2>&1 &
  pids+=("$!")
done
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
"$UV" run --no-sync python scripts/track2_transcriptome_phase2.py aggregate "$TASK_ROOT" > logs/phase2-aggregate.log 2>&1
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/phase2-postrun-gpus.csv
