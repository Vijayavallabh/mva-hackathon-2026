# Track 2 v36 reviewer guide

For a short entry point, read [the reviewer brief](track2-reviewer-brief-v36.md).
Then use [the report](track2-report-v36.md), [nine slides](track2-slides-v36.html)
and [355-word recording script](track2-pitch-v36.md). The
[current record](track2-current.json) routes the PDF, methods workbook, transcript
and recording-materials ZIP. All earlier releases remain frozen.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v36.py
uv run --no-project python scripts/check_track2_optical_v36.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v36.py verify results/feat009/jvv7_track2_research_v36
uv run python scripts/track2_bundle_v36.py verify
```

The public checks need no subject files, credentials, network, GPU, weights or old
snapshots. Strict release/bundle verification also checks retained local packages
and exports. Python audit guards test dependency isolation, not operating-system
sandbox security. Passing these checks establishes consistency, not biology.

The completed [v31 Perturb-seq analysis](track2-perturbseq-v31.md) retains weak BUB1B
specificity, one shared guide pair and selected controls. The
[v29 analysis](track2-orthogonal-v29.md) retains failed protein controls, limited
HT29 agreement and no qualified MCF7 BUB1B query. Earlier
[v19 expression results](track2-transcriptome-v19.md), v23/v25/v27 studies and
58 claim records across seven registers remain checked. No rescue-priority drug,
phase or clinical exposure margin is established.

The [completed optical comparison](track2-optical-v36.md) retains all 16 corrected
fits, 12 baseline methods per arm, original gates and explicitly exploratory controls.
BUB1B interphase full-profile ranks are 1, 3, 3 and 2 among 994 genes. This favorable
morphology lead is distinct from the failed practical neural-gain gate in both arms.
Mitotic counts 11/15/11/25 remain insufficient; missing is not a zero score or a
negative biological result. Median, sampling, classification and post-hoc plate
controls accompany the finding. HeLa lacks functional p53; the study does not
qualify a non-cancer rescue assay or drug response.

The original coordinate-contaminated fits and empty-shard failure remain archived.
Original-count CPU reductions, workbook reconciliation and rank-to-MRR/paired
interval replay test arithmetic and provenance. Bootstrap replay reuses the
registered algorithm; it is not an independent statistical implementation.
The six [optical falsification records](track2-optical-register-v36.json) specify
what could overturn each interpretation and what changes before a drug experiment.

The [October 19 requirements review](track2-requirements-review-v33.md) covers seven
official files and 29 public threads/83 visible comments. Four changed comments were
reread; unchanged text retains earlier review. The [active deletion plan](deletion-plan-v2.md)
requires deletion and confirmation to cnb@sagebase.org by November 23. Earlier frozen
dates are superseded. Submission remains October 24 at 23:59 UTC.

[Delivery readiness](track2-owner-readiness-v36.md) separately tracks recording,
runtime, hosting, provider/distribution questions, portal checks and receipt.
