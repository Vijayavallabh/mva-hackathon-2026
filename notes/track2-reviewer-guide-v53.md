# Track 2 v53 reviewer guide

For a short entry point, read [the reviewer brief](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-reviewer-brief-v53.md).
Then use [the report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v53.md), [nine slides](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v53.html)
and [369-word recording script](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-pitch-v53.md). The
[current record](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-current.json) routes the PDF, methods workbook, transcript
and recording-materials ZIP. All earlier releases remain frozen.

The broad [v41 literature addendum](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-v41.md)
preserves five public searches, fourteen selected 2025-2026 sources and twenty-one
receipts. It adds checkpoint/corona/MCC, mitochondrial and proteostasis readouts.
The targeted [v43 TORC1-segregation addendum](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-v43.md)
adds direct mTORC1 engagement and mitotic lagging-DNA/anaphase-bridge readouts based
on one open-access fission-yeast full text. Neither addendum changes any drug
disposition, and neither is biological validation.

The full [v42 requirements refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v42.md)
read 31 public threads/89 visible comments. Thread 32 permits a clearly labeled
published-paper example in the pitch; it does not require changing the current
369-word script. The current anonymous [v53 latest-thread refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v53.md)
rechecked all official files and the 32/16 discussion listing through the new open
thread 33 (an SDK/README pull request, not a Track 2 requirement change). Threads
32 and 31 were reread; no new organizer requirement appeared.

For a two-minute demonstration, open [Every enrolled cell](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-demo-v37.html).
Move from the actual unmeasured HOLD state to the synthetic injury and all-pass cases;
inspect the exact inputs and download the explanation. The [small public kit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-community-kit-v37.md)
includes everything needed to replay the 18 examples with standard-library Python.
These examples test implementation, not policy validity or clinical performance.

For the proposal, use the [laboratory handoff](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-lab-handoff-v53.md) and
[reviewer questions](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-judge-questions-v44.md). The [competition plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-competition-plan-v39.md)
maps actual work to rigor 35%, impact 25%, innovation 25% and scalability 15%.
The owner-selected voice workflow is in the [timed recording guide](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-recording-guide-v53.md)
and [offline teleprompter](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-teleprompter-v53.html). No recording has been made.

```bash
uv run --no-project python scripts/check_track2_harness_v53.py
uv run --no-project python scripts/track2_public_review_v53.py
uv run --no-project python scripts/check_track2_requirements_v53.py
uv run --no-project python scripts/check_track2_optical_v36.py
uv run --no-project python scripts/track2_demo_v37.py
uv run python scripts/audit_track2_harness_v53.py --output <new-output.json>
uv run python scripts/track2_release_v48.py verify results/feat009/jvv7_track2_research_v48-verified154
uv run python scripts/track2_bundle_v53.py verify
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

The current [v53 requirements refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v53.md)
checks the live Space revision, seven official-file hashes and the 31/16 discussion
listing. It found no new organizer requirement and did not reread thread bodies. The [active deletion plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/deletion-plan-v2.md)
requires deletion and confirmation to cnb@sagebase.org by November 23. Earlier frozen
dates are superseded. Submission remains October 24 at 23:59 UTC.

[Delivery readiness](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v53.md) separately tracks recording,
runtime, hosting, provider/distribution questions, portal checks and receipt.

## Exact current deliverables

- Report source: `notes/track2-report-v53.md`
- Report PDF/workbook directory: `results/feat009/v53-documents-final-20261023-1`
- Slide deck source: `notes/track2-slides-v53.html`
- Rendered slides/PDF: `results/feat009/v53-slides-final-20261023-1`
- Methods workbook: `results/feat009/v53-documents-final-20261023-1/jvv7_track2_methods_v53.xlsx`
- Recording materials ZIP: `results/feat009/jvv7_track2_video_materials_v53_39.zip`
- Preserved historical release snapshot: `results/feat009/jvv7_track2_research_v48-verified154` (do not rebuild for a presentation-only v53 change)
- Public repository HEAD: `1fc4163ff7ba67c51decd73e14062d06fe86101d`

No recorded video or video URL exists. These exact local deliverables are not yet
an uploaded submission or a submission receipt. The owner-facing exact portal-field
checklist is [submission prep](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-submission-prep-v3.md).
