# Session handoff: integrated Track 2 v24

27 September 2026, session 64. Only feat-009 is active. Use `notes/track2-current.json`,
`scripts/check_track2_harness.py`, `notes/track2-reviewer-guide-v24.md` and
`notes/track2-owner-readiness-v24.md`. V24 integrates the completed v23 RNAi findings
into the report, deck, script, workbook and recording materials. Drug decisions remain
v21. All older bound inputs, v19/v23 research and submitted Track 1 v4 are preserved.
No new GPU/model execution, wet-lab experiment, contact, recording or upload occurred.

## Current materials

- `notes/track2-report-v24.md`: nine-page report with methods B7-B17 and 227-word abstract.
- `notes/track2-slides-v24.html`: nine slides, with a dedicated RNAi result and controls.
- `notes/track2-pitch-v24.md` and `notes/track2-transcript-v24.txt`: 342 spoken words;
  cue timings are unmeasured three-minute rehearsal allocations.
- `notes/track2-video-description-v24.md`: disclosure matches report B9 exactly.
- `results/feat009/v24-slides-final-20260927/`: slide PDF and nine PNGs.
- `results/feat009/v24-documents-final-20260927/`: report PDF/Markdown/HTML and original
  filled methods workbook.
- `results/feat009/jvv7_track2_research_v24`: immutable research snapshot.
- `results/feat009/jvv7_track2_video_materials_v24.zip`: recording/review materials.
- `notes/track2-harness-review-v24.md`, design/editorial/integration reviews and versioned
  render/document audits document checks and remaining limitations.

## Scientific position

No rescue-priority drug is supported. Everolimus remains an optional model-qualified
mechanistic probe; HCQ is reserve. Phase, endogenous allele effects, tissue response,
clinical exposure and meaningful biological margins remain unresolved. Tumour killing
is separate from non-cancer function. Invalidity, imprecision, scoped futility, injury
and further preclinical review are distinct decisions.

The frozen `notes/track2-rnai-v23.md` records eight-H100 CUDA statistics: 1,536,619,950
pair comparisons, 5,843,968 conditional control evaluations and 2,364,754 orthogonal
reference comparisons. All 116,782 RNAi signature IDs and replicate-ID sets overlap
v19. These are dependent computations, not independent biological experiments.
All ten BUB1B reagents have distinct annotated seeds; actual processing, potency and
on-target function remain unmeasured. In each representation, 45/54 evaluable BUB1B
records resemble unrelated same-seed reagents more than BUB1B peers. One HEPG2 reagent
lacks a comparator; missing is unknown.

HT29's six-reagent PRIME coherence is favorable: batch-reference adjusted tail 0.01422,
but 0.08532 under labelled post-hoc finite-reference sensitivity. The observed effect
is unchanged; other tails in the fixed 36-test family change. Neither calculation
establishes calibrated FDR. Five primary threshold crossings become zero in that
sensitivity. Other-gene/MTOR CRISPR agreement cannot qualify BUB1B or drug benefit;
no BUB1B CRISPR profile is present. `notes/track2-rnai-validation-v23.md` specifies seed,
batch, endogenous-function and independent perturbation/restoration controls.

The earlier `notes/track2-transcriptome-v19.md` remains intact: 312,438 compound
profiles, 12,185,082 comparisons and 560,000 resamples. Filters pass 0/14 primary
contexts and 0/42 post-hoc comparisons. HT29's distinct five-provider-reagent projected
q=0.042 is retained despite missing the six-reagent rule. Of 180 second-release
everolimus-labelled profiles, 174 have unresolved stereochemical metadata; the six
reference-matching 0.1 µM nominal-culture profiles fail drug QC. No qualified lower-dose
reversal or biological disproof follows. Both campaigns used GPUs briefly, not at
sustained full utilization. All jobs finished.

The v21 ledger preserves eleven v15 drug dispositions. Its 27 claim records plus five
v23 challenges give 32 records, not independent studies. Biological decision-contract
measurements/margins remain null and its result HOLD. Primary protein-control ordering
passes 12/12; expanded-control separation fails 8/12 and 11/24 retained-function scores
are negative. Balnis units conflict by 1,000-fold; neither value sets a dose.

## Verification and restart

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_rnai_v23.py
uv run --no-project python scripts/check_track2_transcriptome.py
uv run python scripts/track2_release_v24.py verify results/feat009/jvv7_track2_research_v24
uv run python scripts/track2_bundle_v24.py verify
```

The final nine-slide render has no detected clipping/overlap, minimum 24px slide text
and 5.257:1 checked contrast. All slides and all nine report pages were visually
inspected. The workbook preserves official prompts and Track 1 values/styles and
round-trips all answers; its appearance was not rendered. The public isolated checks
use six blocked audit probes without project dependencies or protected inputs.
These are internal consistency checks, not independent specialist/clinical review.
Actual regressions, historical-input preservation and fresh init output are recorded
in progress.md session 64.

The v23 archive `results/feat009/rnai-v23/rnai-v23-audit.tar.gz` has 161 files and a
non-extracting verifier. Large arrays stay hash-inventoried at
`/home/prachh/v/mva-track2-rnai-20260927-v23`. The 457-file v19 archive and original
campaign `/home/prachh/v/mva-track2-transcriptome-20260927` also remain preserved.
Reproduction instructions and numerical validation are in the frozen research notes.

## Blockers

- Biological advancement needs relevant endogenous function, model/branch qualification,
  direct drug-plus-deficit response, independent confirmation and justified benefit,
  injury and exposure margins. Subject phase remains unconfirmed.
- Annotated seed independence is checked, but actual processed products, potency,
  off-target attribution, model transfer and compound-identity gaps remain.
- Balnis units, secondary-control review, model dependence, cross-gene transfer and
  pretraining overlap limit inference. More correlated predictions cannot resolve them.
- Fireworks/earlier alignment-service handling is unverified. OpenAI no-training remains
  an owner attestation, not an account or zero-retention audit.
- Challenge CC BY scope versus linked historical AF3/non-AVI Atlas terms is unresolved.
  Retain notices and the unsent clarification; organizer contact is not authorized.
- Video recording, runtime measurement, hosting, owner/live-portal checks and Track 2
  receipt remain open. September 24-25 requirements/discussions are dated reviews:
  three entries, latest only reviewed, remaining quota unknown. Do not invoke callbacks.
- Track 1's owner-reported 100/F-max 1 remains an attestation; receipt/byte identity is
  an administrative gap. Never request another upload to resolve it.

## Next actions

Rehearse and record the v24 pitch with the complete acknowledgement. Measure the
recorded file, resolve provider/distribution items and verify final portal materials.
Research advancement begins with v21 validation and the v23 qualification addendum.
No GPU job is pending. BindCraft2 remains deferred without a functional target and
validation route. Preserve all earlier releases and failed attempts.

Raw subject files/narrative stay on the original machine and out of hosted context.
No family contact or re-identification. Remote folders under ~/v remain on the
November 24 deletion inventory. Keep the live retired-object purge guard; commit
intended changes, push configured origin and verify upstream equality.
