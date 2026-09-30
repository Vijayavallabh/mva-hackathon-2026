# Track 2: review the completed v25 CRISPR addendum with presentation v24

Start with [the new findings](track2-crispr-v25.md), then the preserved
[v24 report](track2-report-v24.md). The deck and transcript remain v24 and do not yet
integrate this new campaign. [Current state](track2-current.json) records this split.

The new evidence strengthens HT29 as an assay-qualification lead. It retains favorable
everolimus/MTOR connections in MCF7 while showing that the BUB1B model there fails
qualification. Never combine those different cell contexts into a claimed joint result.
No rescue drug, clinical margin or wet-lab finding is established.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_crispr_v25.py
```

The combined public check verifies v24 presentation, v21 decisions, v19 transcriptomics,
v23 RNAi and v25 CRISPR findings. It requires no subject data, credentials, network,
GPUs or old local archives. Its isolated audit blocks those accesses explicitly.
It verifies internal consistency, not clinical validity or submission eligibility.

The v25 record includes the [fixed plan](track2-crispr-plan-v25.json),
[full structured findings](track2-crispr-results-v25.json),
[summary](track2-crispr-summary-v25.json), [well-level continuity](track2-crispr-continuity-v25.json),
[five claim challenges](track2-crispr-register-v25.json),
[validation changes](track2-crispr-validation-v25.md) and
[reproduction instructions](track2-crispr-reproduction-v25.md).
The local 186-file archive retains complete result tables and failed attempts.
All eight GPU jobs finished; their short CUDA execution does not establish saturation.

Preserve the earlier [v19 campaign](track2-transcriptome-v19.md),
[v23 findings](track2-rnai-v23.md), submitted Track 1 files and all frozen snapshots.
The [v24 readiness note](track2-owner-readiness-v24.md) still governs unresolved
video, provider, distribution, live-portal and receipt items. There was no new portal
audit or upload. A future presentation revision must incorporate the new research
before it is described as integrated.
