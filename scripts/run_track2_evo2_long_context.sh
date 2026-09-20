#!/usr/bin/env bash
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-20260920
source scripts/track2_expansion_env.sh
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export PYTHONUNBUFFERED=1
export LD_LIBRARY_PATH="$PWD/evo2-fp8-env/.venv/lib/python3.11/site-packages/nvidia/cudnn/lib"
export LD_PRELOAD="$PWD/cublas-compat-env/.venv/lib/python3.11/site-packages/nvidia/cublas/lib/libcublasLt.so.12:$PWD/cublas-compat-env/.venv/lib/python3.11/site-packages/nvidia/cublas/lib/libcublas.so.12"
/home/prachh/v/bin/uv run --frozen --project evo2-fp8-env python scripts/track2_evo2_long_context.py
