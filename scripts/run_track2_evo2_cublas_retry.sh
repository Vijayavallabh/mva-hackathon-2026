#!/usr/bin/env bash
# Preserves the failed original runtime; fixes dynamic library selection per process.
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-20260920
source scripts/track2_expansion_env.sh
export LD_LIBRARY_PATH="$PWD/evo2-fp8-env/.venv/lib/python3.11/site-packages/nvidia/cudnn/lib"
export LD_PRELOAD="$PWD/cublas-compat-env/.venv/lib/python3.11/site-packages/nvidia/cublas/lib/libcublasLt.so.12:$PWD/cublas-compat-env/.venv/lib/python3.11/site-packages/nvidia/cublas/lib/libcublas.so.12"
UV=/home/prachh/v/bin/uv
"$UV" run --frozen --project ../mva-track2-pilot-20260920 python - <<'PY'
import hashlib,json,os
from pathlib import Path
from datetime import datetime,timezone
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  while b:=f.read(8*1024*1024):h.update(b)
 return h.hexdigest()
files=os.environ['LD_PRELOAD'].split(':')+['cublas-compat-env/pyproject.toml','cublas-compat-env/uv.lock',
 'scripts/track2_evo2_comparison.py','scripts/run_track2_evo2_model.py','scripts/run_track2_evo2_cublas_retry.sh']
with Path('outputs/evo2_40b-runtime-cublas128v2.json').open('x') as f:
 json.dump(dict(created_utc=datetime.now(timezone.utc).isoformat(),files={p:digest(p) for p in files},
  reason='Original cuBLAS 12.4 FP8 Linear fails; 12.8.4.1 LD_PRELOAD resolves the isolated operation. Strict model qualification remains required.',
  loaded_cublasLt_version_in_minimal_test=120804,scoring_plan_changed=False),f,indent=2)
PY
"$UV" run --frozen --project ../mva-track2-pilot-20260920 python scripts/run_track2_evo2_model.py evo2_40b cublas128v2
