# Session handoff: Track 2 v27 research with preserved v26 materials

1 October 2026 IST, session 67. Only feat-009 is active. Use `notes/track2-current.json`,
`scripts/check_track2_harness.py` and `notes/track2-reviewer-guide-v27.md`.
Presentation is v26 and the combined harness is v27; the drug ledger and base validation remain v21 with
frozen v23/v25 qualification addenda. All older bound files and releases are preserved.

## Current materials

- `notes/track2-report-v26.md`: eleven-page report, methods B7-B17, 269-word abstract.
- `notes/track2-slides-v26.html`: nine slides, including new HT29 and MCF7 evidence figures.
- `notes/track2-pitch-v26.md` and `notes/track2-transcript-v26.txt`: 343 spoken words;
  cue timings are unmeasured three-minute rehearsal allocations.
- `notes/track2-video-description-v26.md`: disclosure matches report B9 exactly.
- `results/feat009/v26-slides-final-20261001/`: slide PDF and nine PNGs.
- `results/feat009/v26-documents-final-20261001/`: report PDF/Markdown/HTML and methods XLSX.
- `results/feat009/jvv7_track2_research_v26`: immutable research snapshot.
- `results/feat009/jvv7_track2_video_materials_v26.zip`: recording/review materials.
- Versioned design/editorial/integration reviews, render/document audits and
  `notes/track2-harness-review-v26.md` record checks and their limits.

## Scientific position

Read `notes/track2-falsification-v27.md` alongside the preserved v26 presentation.
The completed four-model scan covers 9,472 masked distributions and 179,968 substitution
scores: negative scores are common, but matched N-to-K backgrounds retain qualified
favorable candidate evidence. Expanded controls still fail separation in 8/12 comparisons.
New 918,999,010 expression comparisons retain HT29 BUB1B PRIME ranks 2–5 under stronger
feature/projection sensitivities. MCF7 BUB1B drug reversal declines from rank 7 to 1,184
while MTOR mimicry stays first; query QC remains failed. Projections may remove real
biology and are not causal adjustment. All 42 claim records retain contrary evidence.
Five new R38-R42 challenges, complete matrices, archive and public checker are available.
All eight H100s completed both waves; no owned job is pending. The reviewed Anthropic
kit was not executed. Its different SDK/checkpoint pins were not substituted into the
established full-precision comparison. New folder `~/v/mva-track2-falsification-20261001-v27`
is included in the November 24 deletion scope.

No rescue-priority drug is supported. Everolimus remains an optional model-qualified
mechanistic probe; HCQ stays reserve. Phase, endogenous allele effects, relevant tissue
response and clinical exposure/benefit/injury margins remain unresolved. No wet-lab
experiment has been performed. The v21 decision contract returns HOLD with null inputs.
Invalidity, imprecision, scoped futility, injury and further preclinical review are
separate decisions. Tumour killing is separate from non-cancer function.

`notes/track2-crispr-v25.md` reports the completed 2,474,445,074-comparison LINCS2020
campaign. The 31 BUB1B profiles across 19 contexts use one guide. HT29 has PRIME
correlation 0.3712 and fourth-place retrieval in both RNAi/CRISPR directions, unchanged
after removing BUB1B's transcript. One failed-QC batch and tumour context limit this
to assay development; independent perturbation/restoration and a relevant non-cancer
model remain necessary.

MCF7 has favorable reference-matching everolimus/MTOR connections at 0.1 µM nominal
culture exposure, but its BUB1B query fails QC and disagrees with RNAi. HT29's available
reference-matching 10 µM drug profile fails QC. Never combine those cells into a joint
rescue claim. A375/NPC signatures regroup older wells under new IDs; better aggregation
does not create independent replication. Preserve the older QC failures.

The frozen `notes/track2-rnai-v23.md` retains 45/54 seed-associated comparisons in each
representation, the six-reagent HT29 PRIME finding, and 0.01422 to 0.08532 finite-reference
sensitivity. The observed effect is unchanged, comparison-family tails change; neither
is calibrated FDR. Its lack of BUB1B CRISPR applies to that older panel only.
`notes/track2-transcriptome-v19.md` retains failed 0/14 and 0/42 operational filters and
the distinct five-reagent projected HT29 partial positive. These campaigns reuse RNAi
experiments and do not establish biological independence. The three claim registers
now contain 37 records, not studies. All eleven drug dispositions persist.

The full source analyses and safe archive verifiers remain in v19/v23/v25. Those earlier
H100 campaigns were not rerun; the new v27 campaign addresses different questions.
V25 product time totals 1.231 seconds with an 8% peak in one-second monitoring.
Do not call this sustained saturation or new neural inference. Public-only remote
folders under `~/v` remain in the November 24 deletion scope.

## Verification and restart

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_falsification_v27.py
uv run --no-project python scripts/track2_public_review_v26.py
uv run python scripts/track2_release_v26.py verify results/feat009/jvv7_track2_research_v26
uv run python scripts/track2_bundle_v26.py verify
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Actual checks and fresh init output are in progress.md session 67. Public checks need
no subject files, credentials, network, GPUs or old snapshots; strict release verification
also checks local historical archives. Visual review covers all slides and report pages;
workbook checks preserve official prompts, Track 1 values/styles and exact answers.
These are internal checks, not independent specialist/clinical review.

## Blockers

- Independent BUB1B guide/function evidence is missing. HT29 and MCF7 findings answer
  different questions; no relevant joint drug-plus-deficit response is measured.
- Endogenous model/branch qualification, independent confirmation and justified benefit,
  injury and exposure margins remain necessary for scientific advancement.
- Seed processing, potency, model transfer, compound identity, model dependence and
  pretraining overlap limit inference. Balnis units conflict by 1,000-fold; quarantine
  both disputed values. Protein-control sensitivity remains 8/12 failures and 11/24
  negative retained-function scores, without a calibrated accuracy estimate.
- Fireworks/earlier alignment-service handling remains unverified. OpenAI no-training
  is an owner attestation, not an account or zero-retention audit.
- Challenge CC BY scope versus linked historical AF3/non-AVI Atlas terms is unresolved.
  Preserve notices and the unsent clarification; organizer contact is not authorized.
- Video recording, runtime measurement, hosting, owner/live-portal checks and Track 2
  receipt remain open. September 24-25 requirements/discussions are dated reviews:
  three entries, latest only reviewed, quota unknown. No callback was invoked here.
- Track 1's owner-reported 100/F-max 1 remains an attestation; receipt/byte identity is
  a separate administrative gap. Never request another upload to resolve it.

## Next actions

Integrate v27 findings in a new presentation revision before using the frozen v26
materials as a complete account of current research. Do not edit old bound files.

Rehearse the v26 script, record with the complete acknowledgement and measure runtime.
Resolve provider/distribution items and check final portal materials before delivery.
The editing task is complete independently of those delivery steps; feat-009 remains
in progress. Research advancement uses v21 validation plus v23/v25 qualification
controls. BindCraft2 stays deferred without a functional target and validation route.

Raw subject files and clinical narrative stay on the original machine and out of hosted
context. No family contact or re-identification. Keep the live retired-object purge
guard; commit intended changes, push configured origin and verify upstream equality.
