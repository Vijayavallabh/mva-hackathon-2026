# Track 2 v43 reviewer guide

For a short entry point, read [the reviewer brief](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-reviewer-brief-v42.md).
Then use [the report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v43.md), [nine slides](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v43.html)
and [367-word recording script](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-pitch-v40.md). The
[current record](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-current.json) routes the PDF, methods workbook, transcript
and recording-materials ZIP. All earlier releases remain frozen.

The [v43 literature addendum](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-v43.md) preserves five public searches,
fourteen selected 2025-2026 sources and twenty-one receipts. It adds checkpoint/corona/MCC,
mitochondrial and proteostasis readouts without changing any drug disposition; it is
public-source evidence review, not biological validation.

A later [v42 requirements refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v42.md) found the seven
official files unchanged, but public discussion now has 31 threads/89 visible comments.
Thread 32 permits a clearly labeled published-paper example in the pitch; it does not
require changing the current 367-word script.

For a two-minute demonstration, open [Every enrolled cell](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-demo-v37.html).
Move from the actual unmeasured HOLD state to the synthetic injury and all-pass cases;
inspect the exact inputs and download the explanation. The [small public kit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-community-kit-v37.md)
includes everything needed to replay the 18 examples with standard-library Python.
These examples test implementation, not policy validity or clinical performance.

For the proposal, use the [laboratory handoff](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-lab-handoff-v40.md) and
[reviewer questions](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-judge-questions-v42.md). The [competition plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-competition-plan-v39.md)
maps actual work to rigor 35%, impact 25%, innovation 25% and scalability 15%.
The owner-selected voice workflow is in the [timed recording guide](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-recording-guide-v42.md)
and [offline teleprompter](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-teleprompter-v40.html). No recording has been made.

```bash
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/track2_public_review_v43.py
uv run --no-project python scripts/check_track2_optical_v36.py
uv run --no-project python scripts/track2_demo_v37.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v43.py verify results/feat009/jvv7_track2_research_v43-verified32
uv run python scripts/track2_bundle_v43.py verify
```

The public checks need no subject files, credentials, network, GPU, weights or old
snapshots. Strict release/bundle verification also checks retained local packages
and exports. Python audit guards test dependency isolation, not operating-system
sandbox security. Passing these checks establishes consistency, not biology.

The completed [v31 Perturb-seq analysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-v31.md) retains weak BUB1B
specificity, one shared guide pair and selected controls. The
[v29 analysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-v29.md) retains failed protein controls, limited
HT29 agreement and no qualified MCF7 BUB1B query. Earlier
[v19 expression results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-transcriptome-v19.md), v23/v25/v27 studies and
58 claim records across seven registers remain checked. No rescue-priority drug,
phase or clinical exposure margin is established.

The [completed optical comparison](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-optical-v36.md) retains all 16 corrected
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
The six [optical falsification records](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-optical-register-v36.json) specify
what could overturn each interpretation and what changes before a drug experiment.

The current [v42 requirements refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v42.md) checks seven
official files and 31 public threads/89 visible comments. It found the official files
unchanged and read new organizer/public clarifications in threads 31, 32 and 29.
An 11:49 UTC live recheck found the same Space revision and the same 31 listed public
discussions. The [active deletion plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/deletion-plan-v2.md)
requires deletion and confirmation to cnb@sagebase.org by November 23. Earlier frozen
dates are superseded. Submission remains October 24 at 23:59 UTC.

[Delivery readiness](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v43.md) separately tracks recording,
runtime, hosting, provider/distribution questions, portal checks and receipt.
