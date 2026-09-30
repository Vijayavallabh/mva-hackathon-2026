# Reproduce Track 2 v27

This campaign reuses public sources and model environments; it does not require subject
inputs. Current presentation v26 and every older bound input remain preserved.

## Public review, no inference

```bash
uv run --no-project python scripts/check_track2_falsification_v27.py
uv run --no-project python scripts/check_track2_harness.py
```

The first command checks four complete masked-distribution TSVs, every expected
coordinate, descriptive background fractions, all five transcriptome representations,
QC separation, retained contrary evidence, completion records and fixed input hashes.
This is consistency checking, not biological validation.

## Original output archive and local reanalysis

Retained archive:
`results/feat009/falsification-v27/falsification-v27-audit.tar.gz`

SHA-256: `e6ed7cf8d7f2cbde6a65d079946c4c6e1147309ce1a63a833d07a57074d5b435`.
It contains 178 files and is 4,277,889 bytes. It includes all 16 workers' outputs,
full shared-gene retrieval panels, projection bases, logs, plans, reference sequence,
checkpoint manifests, environment locks and executed source files. Model weights,
large reused expression matrices, credentials and protected subject inputs are absent.

Use **new destinations**:

```bash
uv run python scripts/archive_track2_falsification_v27.py verify \
  results/feat009/falsification-v27/falsification-v27-audit.tar.gz \
  results/feat009/v27-replay-archive
uv run python scripts/analyze_track2_falsification_v27.py \
  results/feat009/v27-replay-archive . results/feat009/v27-replay-analysis
uv run python -m unittest discover -s scripts -p 'test_track2_falsification_v27.py'
uv run python -m unittest discover -s scripts -p 'test_track2_falsification_check_v27.py'
```

Reanalysis uses NumPy/SciPy in the repository environment. Compare generated files
byte-for-byte with the public v27 TSV/JSON/FASTA files. Older 84 protein scores and 20
BUB1B/MTOR cross-modal comparisons are numerical controls, not new experimental labels.

## Fresh inference replay on the owner host

Original root: `/home/prachh/v/mva-track2-falsification-20261001-v27`.
Create a new root under `~/v` and update the two launchers' `TASK_ROOT` only. Copy the
fixed plans to `inputs/plan.json` and `inputs/specificity-plan.json`, and copy the public
reference FASTA and executed scripts. Do not overwrite the original run. Run:

```bash
nohup bash scripts/run_track2_saturation_v27.sh > logs/launcher.log 2>&1 < /dev/null &
nohup bash scripts/run_track2_specificity_v27.sh > logs/specificity-launcher.log 2>&1 < /dev/null &
```

The second launcher waits for protein completion. Both launchers check that all eight
GPUs are available before starting and never stop unrelated processes. Shards 0–1 use
ESMC 300M, 2–3 use 600M, 4–5 use 6B, and 6–7 use ESM3-open. Each model pair partitions
positions by parity within each window. Exact model revisions are in the scan plan.

Frozen protein environment/reference resources:
`/home/prachh/v/mva-track2-expanded-latest-20260921/`.
Frozen expression environment:
`/home/prachh/v/mva-track2-transcriptome-20260927/`.
Prepared expression sources:
`/home/prachh/v/mva-track2-crispr-20261001-v25/outputs/prepared/`.
The v25 reproduction note rebuilds those public matrices. The newer-model reproduction
note rebuilds the ESM environment. No new dependency installation was needed here.

`provenance_track2_falsification_v27.py` verifies reused matrix/metadata hashes, records
all prepared-source hashes and confirms the pinned ESM tracked source is unchanged.
`archive_track2_falsification_v27.py build` archives only completed jobs. `verify`
rejects duplicate, absolute/traversing, symlink and nonregular members, checks all
hashes before extraction and requires a new destination.

The optimization repository was reviewed from five pinned upstream files in
`results/feat009/v27-source-review-20261001/`, with a URL/hash manifest. It was not
installed or executed. Local PyTorch fallback warnings remain in the original logs;
they are not evidence that optional fused kernels ran. No new hosted provider or
alignment-service request was made. All v27 remote/local materials remain in the
24 November 2026 deletion scope.
