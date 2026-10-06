# Reproducing the public Perturb-seq analysis

The completed campaign used only Replogle et al. public experiments, Figshare article
20029387 version 1 (CC BY 4.0), public methods and public code. No subject data were
transferred. The owner host root is `/home/prachh/v/mva-track2-perturbseq-20261007-v31`.
All eight GPU workers finished; no GPU job is pending.

## Public CPU review

```bash
uv run --no-project python scripts/check_track2_perturbseq_v31.py
uv run python -m unittest discover -s scripts -p 'test_track2_perturbseq_v31.py'
```

These commands check the public result record, missing states, comparison arithmetic,
claim challenges and bound sources. They do not repeat inference or validate biology.

## Archive and local reanalysis

The original archive has 226 files and 887,986,492 bytes. Its SHA-256 is
`8cd7f0b4c1c453fc10a586d66354c087aa95e2fbbb79ffc0247f9834641585ae`.
It retains source metadata, full result matrices, every per-repeat query result,
executed code/plans, logs, environment lock and download receipts. Six original H5ADs
and two reproducible prepared single-cell arrays are omitted to avoid duplicating
large public inputs; the manifest binds their digests. The original public counts
remain on the owner host. Five downloads match provider MD5 values. The RPE1 raw
export has no provider MD5; only its advertised size and locally observed SHA-256
are recorded. Do not claim an upstream checksum validation for that file.

Use a new extraction directory and a new replay output:

```bash
uv run python scripts/archive_track2_perturbseq_v31.py verify \
  results/feat009/perturbseq-v31/perturbseq-v31-audit.tar.gz \
  results/feat009/perturbseq-v31/extracted
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 \
  uv run --no-project --with numpy==2.4.3 --with pandas==3.0.1 python \
  scripts/summarize_track2_perturbseq_v31.py \
  results/feat009/perturbseq-v31/extracted \
  --output results/feat009/perturbseq-v31/local-reanalysis
uv run --no-project --with numpy==2.4.3 --with pandas==3.0.1 python \
  scripts/compare_track2_perturbseq_v31.py \
  results/feat009/perturbseq-v31/extracted/outputs/analysis \
  results/feat009/perturbseq-v31/local-reanalysis
```

Local reanalysis checks all seven table/matrix outputs and all 2,705 numerical
summary fields. The three full cross-cell matrices are numerically identical.
Minor floating-point summary differences are at most 2.23e-16; the summary bytes
are therefore not identical. Public results retain the original output. The local
summarizer adds an output-directory argument to the archived script; its calculations
are unchanged. The comparison command checks integer ranks and nonnumeric fields
exactly and floats against the declared 2e-5 tolerance.

Independent CPU FP64 calculations from original raw counts and full-library UMI
totals checked all seven RPE1 and nine K562 evaluable query mean profiles. Maximum
errors were 2.05e-6 and 2.83e-6 respectively. Those checks ran on the owner host,
using the RPE1 pilot and K562 worker 4; local replay uses archived derived arrays.
Neither is independent biological confirmation.

## Full campaign

Use the archived environment lock and pyproject with `uv sync --frozen` in an
isolated environment. The executed environment was Python 3.12, torch 2.11.0+cu126,
numpy 2.4.3, scipy 1.17.1, pandas 3.0.1 and h5py 3.16.0. The download entry point is
`scripts/track2_perturbseq_fetch_v31.py`; preparation and workers are in
`scripts/track2_perturbseq_v31.py`. The launcher records GPU availability, waits for
all workers and retains telemetry. It requires a completed pilot and raw-count CPU
audit before the main run. Reproduction requires adapting its fixed task/environment
paths to a new directory, preserving the plan and documented control-coverage amendment.

The original prepare script is in `inputs/initial-executed-script.py`. Preparation
preceded the amendment: all retained controls equalled the selected core set. The
amended worker replaces duplicate control views with four seed blocks per cell.
Both versions and the original plan are retained. A failed CPU audit caused by a
pandas read-only view was fixed by copying the array before normalization; its log
is preserved. Local archive verification was once started before SCP finished and
failed with EOF; the complete transfer subsequently passed the exact receipt hash
and all file checks. This was an incomplete-transfer observation, not a corrupt
source archive. No unsuccessful attempt is counted as a completed analysis.

The GPU products totaled 6.476 seconds, with worker wall times of 40-59 seconds and
sampled utilization peaks of 19-24%. Eight GPUs executed the calculation; sustained
saturation and new neural inference are not claimed. More resampling would not
supply independent guides, unselected controls, allele-specific effects or rescue.

All owner-host roots, caches and local project artifacts remain in the 24 November
2026 deletion scope. Earlier releases remain immutable.
