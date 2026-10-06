#!/usr/bin/env bash
# Eight independent CUDA statistics workers; public experimental data only.
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-perturbseq-20261007-v31
ENV_ROOT=/home/prachh/v/mva-track2-transcriptome-20260927
UV=/home/prachh/v/bin/uv
cd "$TASK_ROOT"
export PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache" CUDA_CACHE_PATH="$TASK_ROOT/cache/cuda"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONUNBUFFERED=1
test -f outputs/prepared/manifest.json
test -f outputs/pilot-0/completion.json
"$UV" run --project "$ENV_ROOT" --no-sync python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('outputs/pilot-0/cpu-original-counts-audit.json').read_text())
assert j['passed'] and j['queries'] and all(r['max_absolute_error']<=2e-5 for r in j['queries'])
PY
nvidia-smi --query-gpu=index,uuid,name,memory.used,utilization.gpu --format=csv,noheader,nounits > outputs/prelaunch-gpus.csv
awk -F, '$4+0>1000 || $5+0>5 {bad=1} END {exit bad}' outputs/prelaunch-gpus.csv
nvidia-smi --query-gpu=timestamp,index,uuid,utilization.gpu,memory.used,power.draw --format=csv --loop=1 > logs/gpu-monitor.csv &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT
pids=()
for gpu in {0..7}; do
  CUDA_VISIBLE_DEVICES="$gpu" "$UV" run --project "$ENV_ROOT" --no-sync python scripts/track2_perturbseq_v31.py worker "$TASK_ROOT" --shard "$gpu" > "logs/worker-$gpu.log" 2>&1 &
  pids+=("$!")
done
printf '%s\n' "${pids[@]}" > outputs/worker-pids.txt
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
test "$failed" = 0
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv > outputs/postrun-gpus.csv
date -u +%FT%TZ > outputs/campaign-complete.txt
