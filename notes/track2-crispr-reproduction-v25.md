# Reproduce the v25 public-data campaign

The working root is `/home/prachh/v/mva-track2-crispr-20261001-v25` on the owner host.
All eight GPU jobs and the separate CPU audit finished. Use new output directories
for any new run; preserve this campaign and all earlier releases.

## Inputs and environment

- Original anonymous Broad objects and their source lengths, ETags, versions and
  SHA256 values: [source manifest](track2-crispr-source-manifest-v25.json).
- Fixed design: [plan](track2-crispr-plan-v25.json). Its registration timestamp and
  SHA256 are inside the evidence archive. The plan preceded new matrix inspection.
- Frozen dependencies: `scripts/track2_transcriptome_environment.toml` and
  `scripts/track2_transcriptome.uv.lock`. The run reused the already installed
  `/home/prachh/v/mva-track2-transcriptome-20260927` environment through `uv run
  --project … --no-sync`. It did not install packages or alter older environments.
- The existing v19 and v23 public-data campaigns supply RNAi matrices and provenance
  references. Their preparation manifests are bound by the new campaign. A fresh
  host must first reproduce them using the [v19 instructions](track2-transcriptome-reproduction-v19.md)
  and the commands in [v23](track2-rnai-v23.md). No subject files are needed.

The six downloads total approximately 42.5 GB. The numerical campaign uses about
4 GB of prepared landmark arrays plus dense derived matrices retained remotely.
Read the recorded resource audit before scheduling; the executed run found eight
idle H100s and approximately 974 GB available system RAM. No unrelated job was stopped.

## Execution

These are the executed entry points, shown from the campaign root. Use the pinned
environment with `uv`; the launcher fixes cache paths below the campaign directory,
checks GPU availability and records one-second utilization.

```bash
uv run --project /home/prachh/v/mva-track2-transcriptome-20260927 --no-sync \
  python scripts/download_track2_crispr_v25.py "$PWD"
bash scripts/run_track2_crispr_v25.sh
uv run --project /home/prachh/v/mva-track2-transcriptome-20260927 --no-sync \
  python scripts/summarize_track2_crispr_v25.py "$PWD"
uv run --project /home/prachh/v/mva-track2-transcriptome-20260927 --no-sync \
  python scripts/audit_track2_crispr_v25.py "$PWD"
uv run --project /home/prachh/v/mva-track2-transcriptome-20260927 --no-sync \
  python scripts/audit_track2_crispr_continuity_v25.py "$PWD"
uv run --project /home/prachh/v/mva-track2-transcriptome-20260927 --no-sync \
  python scripts/archive_track2_crispr_v25.py "$PWD"
```

The launcher was run under `nohup`, with output in `logs/launch.log`. Its stages are
`prepare`, eight concurrent `worker --shard 0…7` commands and `combine`. For a new
root, change the launcher root before registration; the Python entry points accept
the root as an argument. Source downloads are hash-recorded, not an instruction to
silently substitute later source bytes. Compare them with the frozen source manifest.

Implementation corrections and failed attempts are disclosed in the
[registration review](track2-crispr-registration-review-v25.md). In particular, the
1,956 extra CRISPR matrix columns are controls, and two 0.1-µM signatures regroup
older singleton wells despite having different signature IDs.

## Retained evidence

`results/feat009/crispr-v25/crispr-v25-audit.tar.gz` is the local derived-evidence
archive. It retains the complete 57,044-row cross-batch benchmark, 31,932 orthogonal
rows, 16,696 named-drug comparisons, all 285,488 BUB1B-to-compound scores, worker
registrations, source manifests, original-coordinate checks, logs and code. Dense
matrices and prepared/source data stay hash-inventoried on the owner host. The
archive is not a clinical result, recorded video or competition submission.

The public repository contains the full structured findings, a 282-row
[BUB1B/MTOR everolimus table](track2-crispr-everolimus-v25.tsv), and original code.
RPTOR was specified but is absent from the assayed target means; do not infer a
negative RPTOR result from that absence. Source data files are not redistributed.

```bash
uv run --no-project python scripts/check_track2_crispr_v25.py
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/verify_track2_crispr_archive_v25.py \
  results/feat009/crispr-v25/crispr-v25-audit.tar.gz \
  --metadata results/feat009/crispr-v25/archive.json
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Numerical checks are internal, not independent scientific review. All measurements
and clinical margins required by the biological decision contract remain unfilled.
The remote campaign is included in the standing **24 November 2026** deletion scope.
