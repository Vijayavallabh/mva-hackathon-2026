# Track 2 v34 reviewer guide

For a short entry point, read [the reviewer brief](track2-reviewer-brief-v34.md).
Then use [the report](track2-report-v34.md), [nine slides](track2-slides-v34.html)
and [336-word recording script](track2-pitch-v34.md). The
[current record](track2-current.json) routes the PDF, methods workbook, transcript
and recording-materials ZIP. All earlier releases remain frozen.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v34.py
uv run --no-project python scripts/check_track2_optical_progress_v33.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v34.py verify results/feat009/jvv7_track2_research_v34
uv run python scripts/track2_bundle_v34.py verify
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
52 claim records across six registers remain checked. No rescue-priority drug,
phase or clinical exposure margin is established.

The [v33 optical study](track2-optical-progress-v33.md) is in progress. Preparation
and launch receipts are checked; model gains are unvalidated. BUB1B mitotic counts
11/15/11/25 leave one qualifying guide where two are required. Slide 4 reports
missing coverage, not a negative biological result. The interphase arm, complete
model comparison, plate sensitivity and independent numerical checks remain open.
The smoke run is excluded. Frozen v34 status describes its recorded capture time;
read remote status and the handoff for later operational progress.

The [October 19 requirements review](track2-requirements-review-v33.md) covers seven
official files and 29 public threads/83 visible comments. Four changed comments were
reread; unchanged text retains earlier review. The [active deletion plan](deletion-plan-v2.md)
requires deletion and confirmation to cnb@sagebase.org by November 23. Earlier frozen
dates are superseded. Submission remains October 24 at 23:59 UTC.

[Delivery readiness](track2-owner-readiness-v34.md) separately tracks recording,
runtime, hosting, provider/distribution questions, portal checks and receipt.
