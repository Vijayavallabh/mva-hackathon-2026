#!/usr/bin/env bash
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-20260920
source scripts/track2_expansion_env.sh
export CUDA_HOME=/usr/local/cuda-12.5
export CUDNN_PATH="$PWD/evo2-fp8-env/.venv/lib/python3.11/site-packages/nvidia/cudnn"
export MAX_JOBS=8
export NVTE_BUILD_THREADS_PER_JOB=1
export NVTE_FRAMEWORK=pytorch
export FLASH_ATTN_CUDA_ARCHS=90
export FLASH_ATTENTION_FORCE_BUILD=TRUE
UV=/home/prachh/v/bin/uv
"$UV" sync --project evo2-fp8-env --python /home/prachh/v/mva-track2-pilot-20260920/.venv/bin/python
"$UV" add --project evo2-fp8-env 'transformer-engine-torch==2.3.0' --no-build-isolation-package transformer-engine-torch
"$UV" add --project evo2-fp8-env 'flash-attn==2.8.0.post2' --no-build-isolation-package flash-attn
"$UV" run --frozen --project evo2-fp8-env python -c 'import torch, flash_attn, transformer_engine.pytorch, evo2; print(torch.__version__,torch.backends.cudnn.version(),flash_attn.__version__)'
