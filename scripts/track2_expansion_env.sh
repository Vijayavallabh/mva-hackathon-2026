#!/usr/bin/env bash
set -euo pipefail
case "$PWD" in /home/prachh/v/mva-track2-expanded-*) ;; *) exit 2 ;; esac
umask 077
export UV_CACHE_DIR="$PWD/cache/uv"
export UV_PYTHON_INSTALL_DIR="$PWD/python"
export UV_TOOL_DIR="$PWD/tools"
export UV_TOOL_BIN_DIR="$PWD/bin"
export XDG_CACHE_HOME="$PWD/cache"
export XDG_DATA_HOME="$PWD/share"
export XDG_CONFIG_HOME="$PWD/config"
export TMPDIR="$PWD/tmp"
export TORCH_HOME="$PWD/cache/torch"
export HF_HOME="$PWD/cache/huggingface"
export CUDA_CACHE_PATH="$PWD/cache/cuda"
export PYTHONPYCACHEPREFIX="$PWD/cache/pycache"
export TRITON_CACHE_DIR="$PWD/cache/triton"
export MPLCONFIGDIR="$PWD/cache/matplotlib"
export BOLTZ_CACHE="$PWD/cache/boltz"
export WANDB_MODE=disabled
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export CUBLAS_WORKSPACE_CONFIG=:4096:8
