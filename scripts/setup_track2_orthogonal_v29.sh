#!/usr/bin/env bash
# Owner-host setup; no system packages and no mutation of prior environments.
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-orthogonal-20261006-v29
UV=/home/prachh/v/bin/uv
cd "$TASK_ROOT"
export UV_CACHE_DIR="$TASK_ROOT/cache/uv" UV_PYTHON_INSTALL_DIR="$TASK_ROOT/cache/python"
test "$(git -C toolkit rev-parse HEAD)" = f4f62fa6592ae4938d49b1757bea0cfeff9f468e
if [[ ! -d ProteinMPNN ]]; then git clone https://github.com/dauparas/ProteinMPNN.git ProteinMPNN; fi
git -C ProteinMPNN checkout --detach 8907e6671bfbfc92303b5f79c4b5e6ce47cdef57
cat > pyproject.toml <<'TOML'
[project]
name = "track2-orthogonal-v29"
version = "0.1.0"
requires-python = ">=3.11,<3.12"
dependencies = ["torch==2.5.1", "numpy==1.26.4", "biopython==1.84", "setuptools==68.1.2", "opt-core", "proteinmpnn-opt"]
[[tool.uv.index]]
name = "pytorch-cu124"
url = "https://download.pytorch.org/whl/cu124"
explicit = true
[tool.uv.sources]
torch = {index = "pytorch-cu124"}
opt-core = {path = "toolkit/common/opt_core", editable = true}
proteinmpnn-opt = {path = "toolkit/proteinmpnn/opt", editable = true}
TOML
"$UV" sync --python 3.11.5
export MPNN_DIR="$TASK_ROOT/ProteinMPNN" MODEL_OPT_JIT_ROOT="$TASK_ROOT/cache/jit"
export MODEL_OPT_STATE="$TASK_ROOT/cache/model-state" PYTHONPYCACHEPREFIX="$TASK_ROOT/cache/pycache"
"$UV" run --no-sync bash toolkit/proteinmpnn/run.sh check --config h100 --mode exact
cp pyproject.toml inputs/model.pyproject.toml
cp uv.lock inputs/model.uv.lock
date -u +%FT%TZ > outputs/setup-complete.txt
