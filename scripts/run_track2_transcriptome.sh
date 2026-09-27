#!/usr/bin/env bash
# Durable owner-host job. Does not source project credentials or contact model APIs.
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-transcriptome-20260927
cd "$TASK_ROOT"
export UV_CACHE_DIR="$TASK_ROOT/cache/uv"
export UV_PYTHON_INSTALL_DIR=/home/prachh/v/mva-track2-expanded-latest-20260921/python
export XDG_CACHE_HOME="$TASK_ROOT/cache"
export CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache"
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
export PYTHONUNBUFFERED=1
UV=/home/prachh/v/bin/uv
for ((i=0;i<720;i++)); do
  if [[ -f outputs/matrix-download-complete.txt ]]; then break; fi
  sleep 20
done
test -f outputs/matrix-download-complete.txt
"$UV" run --no-sync --project "$TASK_ROOT" python scripts/track2_transcriptome.py prepare "$TASK_ROOT" > logs/prepare.log 2>&1
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/prelaunch-gpus.csv
if awk -F, '$2+0>1000 || $3+0>5 {bad=1} END {exit bad}' outputs/prelaunch-gpus.csv; then
  pids=()
  for gpu in {0..7}; do
    CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --no-sync --project "$TASK_ROOT" python scripts/track2_transcriptome.py worker "$TASK_ROOT" --shard "$gpu" > "logs/gpu-$gpu.log" 2>&1 &
    pids+=("$!")
  done
  printf '%s\n' "${pids[@]}" > outputs/worker-pids.txt
  failed=0
  for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
  test "$failed" = 0
  "$UV" run --no-sync --project "$TASK_ROOT" python scripts/track2_transcriptome.py aggregate "$TASK_ROOT" --output outputs/transcriptome-results.json > logs/aggregate.log 2>&1
  nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/postrun-gpus.csv
else
  echo 'GPU occupancy changed; no inference started. Recheck without terminating any other process.'
  exit 2
fi
