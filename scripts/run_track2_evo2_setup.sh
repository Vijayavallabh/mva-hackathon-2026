#!/usr/bin/env bash
# Build against the verified host ABI rather than a mismatched prebuilt extension.
set -euo pipefail
cd /home/prachh/v/mva-track2-expanded-20260920
source scripts/track2_expansion_env.sh
export CUDA_HOME=/usr/local/cuda-12.5
export MAX_JOBS=8
export NVCC_THREADS=2
export FLASH_ATTN_CUDA_ARCHS=90
export FLASH_ATTENTION_FORCE_BUILD=TRUE
UV=/home/prachh/v/bin/uv
"$UV" add --project evo2-env ninja packaging setuptools wheel
"$UV" add --project evo2-env 'flash-attn==2.8.0.post2' --no-build-isolation-package flash-attn
"$UV" run --frozen --project evo2-env python -c 'import torch, flash_attn, evo2; print(torch.__version__, torch._C._GLIBCXX_USE_CXX11_ABI, flash_attn.__version__)'
