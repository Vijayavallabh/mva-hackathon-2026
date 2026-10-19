# Track 2 v39 reviewer guide

For a short entry point, read [the reviewer brief](track2-reviewer-brief-v39.md).
Then use [the report](track2-report-v39.md), [nine slides](track2-slides-v39.html)
and [364-word recording script](track2-pitch-v39.md). The
[current record](track2-current.json) routes the PDF, methods workbook, transcript
and recording-materials ZIP. All earlier releases remain frozen.

For a two-minute demonstration, open [Every enrolled cell](track2-demo-v37.html).
Move from the actual unmeasured HOLD state to the synthetic injury and all-pass cases;
inspect the exact inputs and download the explanation. The [small public kit](track2-community-kit-v37.md)
includes everything needed to replay the 18 examples with standard-library Python.
These examples test implementation, not policy validity or clinical performance.

For the proposal, use the [laboratory handoff](track2-lab-handoff-v39.md) and
[reviewer questions](track2-judge-questions-v39.md). The [competition plan](track2-competition-plan-v39.md)
maps actual work to rigor 35%, impact 25%, innovation 25% and scalability 15%.
The owner-selected voice workflow is in the [timed recording guide](track2-recording-guide-v39.md)
and [offline teleprompter](track2-teleprompter-v39.html). No recording has been made.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v39.py
uv run --no-project python scripts/check_track2_optical_v36.py
uv run --no-project python scripts/track2_demo_v37.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v39.py verify results/feat009/jvv7_track2_research_v39
uv run python scripts/track2_bundle_v39.py verify
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

The [October 19 requirements review](track2-requirements-review-v39.md) covers seven
official files and 30 public threads/84 visible comments. The one new participant comment was
read; it has no organizer reply; unchanged text retains earlier review. The [active deletion plan](deletion-plan-v2.md)
requires deletion and confirmation to cnb@sagebase.org by November 23. Earlier frozen
dates are superseded. Submission remains October 24 at 23:59 UTC.

[Delivery readiness](track2-owner-readiness-v39.md) separately tracks recording,
runtime, hosting, provider/distribution questions, portal checks and receipt.
