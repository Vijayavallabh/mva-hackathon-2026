# Track 2 transcriptome campaign: execution and reproduction

27 September 2026. Scientific interpretation is in
[the addendum](track2-transcriptome-v19.md). This record distinguishes numerical
verification from biological validation and records what the hardware actually did.

## Inputs and execution

Owner host: `PrakashDGX_H2`, directory
`/home/prachh/v/mva-track2-transcriptome-20260927`. All eight H100 80GB GPUs were idle
at the initial check. Each launch rechecked occupancy and assigned exactly one visible
GPU per worker. No unrelated process was stopped. Local NVML had a driver/library
mismatch; its GPU availability was unknown, not zero.

Only public NIH GEO inputs, code, plans and the pinned environment were transferred or
downloaded. No subject files, project `.env`, credentials or model API were used.
`track2_transcriptome_environment.toml` was staged as `pyproject.toml` and
`track2_transcriptome.uv.lock` as `uv.lock`; `uv sync --frozen` built the remote
environment. Registration records retain Python-package versions, CUDA 12.6, device,
script, plan and lock hashes. PyTorch was 2.11.0+cu126; TF32 was disabled.

The two public GCTX downloads total 26,693,213,446 compressed bytes. Both matrices and
the five checked metadata files per release matched upstream SHA512 entries. The
prepared matrices preserve original signature identifiers/order and the same 978
landmark genes. Phase II uses the 2017-03-06 matrix, with 2017-04-28 cell metadata.
It supplies a second release, not an independently validated allele or experiment.
Exact overlapping signature IDs were checked; none required exclusion.

Executed durable jobs, in dependency order (each writes its own logs):

```bash
nohup bash scripts/run_track2_transcriptome_download.sh > logs/download.log 2>&1 &
nohup bash scripts/run_track2_transcriptome.sh > logs/campaign.log 2>&1 &
nohup bash scripts/run_track2_transcriptome_phase2_download.sh > logs/phase2-download.log 2>&1 &
nohup bash scripts/run_track2_transcriptome_phase2.sh > logs/phase2-campaign.log 2>&1 &
nohup bash scripts/run_track2_transcriptome_followup.sh > logs/followup-campaign.log 2>&1 &
nohup /home/prachh/v/bin/uv run --no-sync python scripts/track2_transcriptome_audit.py /home/prachh/v/mva-track2-transcriptome-20260927 > logs/audit.log 2>&1 &
```

The follow-up plan was added only after primary results, as labelled. It did not change
the primary plan or scores. The wrappers document the original execution target and
refuse existing outputs. For a fresh reproduction, stage their listed public inputs,
three plans, scripts and environment into a **new** directory under `~/v`; change only
the wrapper's `TASK_ROOT`/initial `cd`, record that patch, and use `uv sync --frozen`.
Do not rerun the commands against the archived campaign directory. The standalone
Python programs also accept the new root as their positional argument.

## Computation and measurement limits

| Wave | GPU workers completed | Longest worker wall time | Sum of worker wall times | Peak tensor allocation per worker |
|---|---:|---:|---:|---:|
| First release, including primary resampling | 8/8 | 91.25 s | 574.72 s | 2.35–2.52 GiB |
| Second release | 8/8 | 23.25 s | 148.03 s | 1.62–1.67 GiB |
| Post-hoc reproducibility sensitivity | 8/8 | 13.92 s | 89.73 s | 0.15–0.90 GiB |

Wall times include CPU work and are not GPU kernel time or GPU-hours. Five-second
monitoring recorded peak utilization percentages of 2, 16, 41, 1, 0, 3, 1 and 4 on
GPUs 0–7. It can miss short kernels. Registration, CUDA-only operations and numerical
checks establish execution on all eight devices; the monitoring does **not** establish
sustained or full utilization. This workload benefited from batched matrix operations
but did not need all available VRAM. No training or new neural-model inference ran.

The 39 query/space vectors per release have 205,034 and 107,404 scores respectively:
7,996,326 + 4,188,756 = 12,185,082. All 78 vectors were checked locally for finite
values. Primary resampling used 14×10,000 random reagent sets; post-hoc sensitivity
used 42×10,000. These are reused observations and computational resamples, not new
biological replicates. Complete same-cell genetic-reference comparisons also ran;
their large matrices remain on the remote host and are hash-inventoried.

Connectivity used float32 CUDA and CPU float64 comparisons; primary maximum absolute
error was 6.03×10⁻⁸, second-release error 5.71×10⁻⁸. Resampling used float64 tied
ranks and the identical statistic on observed and null sets. Sampled null CPU/CUDA
differences were at most 3.34×10⁻¹⁶. Separately, SciPy `spearmanr` read original
GCTX coordinates and checked all 139 raw everolimus-labelled comparisons; maximum
error was 4.75×10⁻⁸. These are independent numerical implementations by the same
agent, not an independent scientific review.

## Corrections and limitations retained

- An initial unit test caught nonfinite input becoming finite during ranking. The
  finite-input rejection was fixed before production computation; six numerical tests
  then passed. No production result used the rejected implementation.
- Initial workers emitted a pandas mixed-type warning for unused `pert_dose` metadata.
  Recorded doses come from the preserved `pert_idose` string; values were not imputed.
- The frozen plan's “PC1” wording is clarified: `shared_pc1_removed` uses the leading
  right singular direction of an **uncentered** rank-normalized non-BUB1B matrix.
  Neither that projection nor the fixed mitosis-gene span is a validated growth
  correction. Controls projected to zero are explicitly excluded from that reference
  space's denominator.
- Exact provider consensus membership became available through `distil_id` in the
  post-hoc check. This resolves membership access, not weighting, seed independence,
  potency, selected-genotype relevance or off-target effects.
- Full-text access to the original CMap article failed. The source review records
  selected passages read elsewhere; no systematic or full-paper audit is claimed.

## Archive and local checks

The 117,668,567-byte archive contains 457 regular files, including its manifest.
All 456 listed members passed local size/hash verification; paths were checked before
extraction. Archive SHA256:
`2a5749f0cffaedce2eb68bba7a5b99ad5478dce57879808011ba168d67c56272`.

Local archive: `results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz`.
It includes score vectors, matched tables, nulls, selected public metadata, registrations,
plans, code, lockfile and logs. It omits the downloadable GCTX matrices, prepared
landmark matrices and large genetic-reference score matrices. The output inventory
hashes 421 scientific files, including those omitted arrays. The audit log is outside
its own archive. No neural weights or protected inputs are included.

```bash
uv run --no-project python scripts/check_track2_transcriptome.py
uv run --no-project python scripts/verify_track2_transcriptome_archive.py results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run --with matplotlib python scripts/plot_track2_transcriptome.py results/feat009/transcriptome-figure-new
./init.sh
```

The first check needs only public tracked files and Python's standard library. It
checks fixed decisions, multiplicity, completion, chemical identity, QC flags and
hashed campaign artifacts; it does not recompute the full public expression analysis.
The archive verifier needs the retained archive but extracts or executes nothing.
Full reproduction requires public GEO downloads and CUDA. Existing v18 and Track 1
checks remain separate. The entire remote campaign is on the deletion inventory.
