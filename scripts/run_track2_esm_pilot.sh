#!/usr/bin/env bash
# Remote entry point; all persistent/scratch output remains in the pilot directory.
set -euo pipefail
source scripts/track2_esm_remote_env.sh
trap 'code=$?; printf "%s\n" "$code" > logs/inference.exit' EXIT
export CUDA_VISIBLE_DEVICES=4
export CUBLAS_WORKSPACE_CONFIG=:4096:8
/home/prachh/v/bin/uv run --frozen python - <<'PY'
import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
raw = subprocess.check_output(['nvidia-smi', '-i', '4', '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader,nounits'], text=True)
memory, utilization = map(int, raw.strip().split(','))
if memory > 1000 or utilization > 5:
    raise RuntimeError('Selected GPU is occupied; no inference launched')
paths = ['inputs/track2-esm-pilot-plan.json', 'inputs/uniprot-O60566.fasta',
         'scripts/track2_esm_pilot.py', 'scripts/track2_esm_remote_env.sh',
         'scripts/run_track2_esm_pilot.sh', 'pyproject.toml', 'uv.lock']
record = {'frozen_before_inference_utc': datetime.now(timezone.utc).isoformat(),
          'input_sha256': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths},
          'gpu_physical_index': 4, 'gpu_used_mib': memory, 'gpu_utilization_percent': utilization}
with Path('outputs/preregistration.json').open('x') as f:
    json.dump(record, f, indent=2)
    f.write('\n')
print(json.dumps(record, indent=2), flush=True)
PY
/home/prachh/v/bin/uv run --frozen python scripts/track2_esm_pilot.py run \
  --plan inputs/track2-esm-pilot-plan.json --fasta inputs/uniprot-O60566.fasta \
  --weights cache/weights-v2 --out outputs/controls-first-v1
