#!/usr/bin/env bash
# The first FP8 environment attempt timed out on the simultaneous 7B build's cache lock.
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-20260920
source scripts/track2_expansion_env.sh
export CUDA_HOME=/usr/local/cuda-12.5
export MAX_JOBS=8
export NVCC_THREADS=2
export FLASH_ATTN_CUDA_ARCHS=90
export FLASH_ATTENTION_FORCE_BUILD=TRUE
export UV_LOCK_TIMEOUT=1800
UV=/home/prachh/v/bin/uv
"$UV" add --project evo2-fp8-env 'flash-attn==2.8.0.post2' --no-build-isolation-package flash-attn
"$UV" run --frozen --project evo2-fp8-env python -c 'import torch, flash_attn, transformer_engine.pytorch, evo2; print(torch.__version__,torch.backends.cudnn.version(),flash_attn.__version__)'
