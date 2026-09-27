# Session handoff: v23 RNAi research / preserved v22 presentation

27 September 2026, session 63. Only feat-009 is active. Authoritative paths are in
`notes/track2-current.json`. V22 presents the preserved v21 falsification findings and fixed public transcriptome evidence
into the report, slides, narration, methods workbook and recording materials. All
older sources/packages, fixed v19 research and submitted Track 1 v4 remain preserved.
The v21 evidence/validation/decision contract and all eleven v15 drug dispositions stay unchanged. V22 combines computational qualification, adds a dedicated functional-evidence slide and distinguishes five decision outcomes.

Use `uv run --no-project python scripts/check_track2_harness.py` and
`notes/track2-reviewer-guide-v23.md`. The current readiness note is
`notes/track2-owner-readiness-v22.md`; `notes/track2-harness-review-v23.md` records this
integration. Session 63 completed a new public-data CUDA analysis on all eight H100s. No new neural
inference, wet-lab work, contact or submission occurred.

## New research addendum

`notes/track2-rnai-v23.md`, its complete result matrix, fixed plan, source/search records,
five-claim register, qualification revisions, figure and audits document the completed
campaign in `/home/prachh/v/mva-track2-rnai-20260927-v23`. All 116,782 RNAi signature
IDs/replicate sets overlap v19. Distinct annotated BUB1B seeds resolve that metadata
gap only. Same-seed similarity exceeds same-target similarity in 45/54 evaluable
BUB1B records per representation. HT29 remains a favorable follow-up clue, but the
finite-reference sensitivity removes all five primary threshold crossings. HEPG2's
missing seed control stays unknown. Other-gene/MTOR CRISPR agreement cannot transfer
to BUB1B or drug benefit. See `notes/track2-rnai-validation-v23.md`.

All eight GPU workers finished; no jobs are pending. Utilization was brief, not
saturated. The primary archive `results/feat009/rnai-v23/rnai-v23-audit.tar.gz` has
161 files; all 160 listed members passed local non-extracting verification. The large
matrices remain hash-inventoried remotely. The combined harness now includes v23 via
`scripts/check_track2_rnai_v23.py`. V22 exported report/slides/script/workbook and
recording ZIP remain unchanged; the new addendum is separate.

## Current materials

- `notes/track2-report-v22.md`: integrated findings, balanced evidence, proposed
  experiment, full disclosure, methods B7-B17 and 215-word abstract.
- `notes/track2-slides-v22.html`: eight slides with combined computational qualification, a human/animal evidence comparison and five decision outcomes.
- `notes/track2-pitch-v22.md` and `notes/track2-transcript-v22.txt`: 337 spoken words
  with matching slide cues and unmeasured three-minute rehearsal allocations.
- `notes/track2-video-description-v22.md`: matched disclosure and acknowledgement.
- Report PDF/Markdown and original filled workbook: `results/feat009/v22-documents-final-b-20260927/`.
- Eight-slide PDF/PNGs: `results/feat009/v22-slides-final-20260927/`.
- Research snapshot: `results/feat009/jvv7_track2_research_v22`.
- Recording/review ZIP: `results/feat009/jvv7_track2_video_materials_v22.zip`.
- `notes/track2-v22-design.md`, `track2-v22-editorial-review.md` and versioned audits
  describe visual/editorial review, scientific limits and export hashes.
- `notes/track2-transcriptome-v19.md` and `notes/track2-transcriptome-reproduction-v19.md`:
  frozen complete findings, sources, fixed plans, result matrices, figure and methods.
- `results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz`: verified
  457-file public-data archive. Remote campaign remains under
  `/home/prachh/v/mva-track2-transcriptome-20260927`; no owned jobs are pending.

## Official brief and competition framing

The September 25 anonymous website recheck finds the same source revision
`aeeef5ad49f51204a7439352e59e9d310aee5e9e`. Six pinned source files are unchanged;
trimmed live submission component 40 matches its source. Full runtime config differs,
so do not claim the entire config is identical. See `notes/track2-v18-brief-review.md`
and `notes/track2-v18-brief-audit.json`.

Track 2 seeks approved-drug hypotheses supported by variant mechanisms. The eight-slide
story now leads with everolimus, explains the conditional BUB1B/BUBR1 link, weighs
public expression findings and their limits, proposes joint drug-plus-deficit
qualification/probing/confirmation, and closes with impact and reuse. Rubric weights remain 35/25/25/15.
No completed efficacy or wet-lab result is required for a hypothesis submission.

The full September 24 community review remains separately dated: 24 public discussions,
68 latest visible comments, three administrative images. No new discussion enumeration,
hidden-history search, contact or portal callback occurred. Three entries/latest-only;
remaining quota unknown. The workbook's old one-entry instruction stays with a comment.

## Scientific position

No rescue-priority drug. Everolimus is an optional model-qualified mechanistic probe;
HCQ reserve. Phase, endogenous allele effects, tissue response, clinical exposure and
meaningful assay margins remain unresolved. Tumour killing is separate from non-cancer
function. V19 adds CUDA statistical reanalysis, not new neural-model inference or wet-lab work.

All eight H100s completed three waves. 312,438 public compound profiles yielded
12,185,082 query/compound comparisons and 560,000 reagent-set resamples; these are
dependent observations and computational draws, not independent experiments. GPU
utilization was bursty, not saturated. Primary operational query filters pass 0/14;
post-hoc full filters pass 0/42. Preserve HT29's five-reagent projected q=0.042 partial
positive; this prevents overclaiming biological disproof. Provider CGS membership is
verified, but weighting, seed independence and on-target function remain unresolved.
Everolimus has 13/19 positive primary raw correlations at 10 µM nominal culture
exposure. Of 180 second-release labelled profiles, 174 have unresolved stereochemical
metadata; the six reference-matching 0.1 µM profiles fail drug QC. Do not pool them or
claim a dose curve. Qualify the perturbation before testing joint drug/deficit function.

The historical v15 ledger retains 63 sources and 11 decisions. The v21 amendment adds twelve source adjudications, 27 claims and the proposed decision contract; actual result HOLD.
Primary protein ordering passes 12/12; post-hoc expanded-control separation fails 8/12;
11/24 retained-control scores are negative. Small/dependent controls cannot calibrate
clinical pathogenicity. The secondary-control supplement remains independently unreviewed.
Balnis source units conflict by 1,000-fold; neither value sets a dose. Unknown means
hold; failed safety stops; all-pass permits preclinical review only.

## Verification and restart

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_transcriptome.py
uv run --no-project python scripts/verify_track2_transcriptome_archive.py results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz
uv run python scripts/track2_release_v22.py verify results/feat009/jvv7_track2_research_v22
uv run python scripts/track2_bundle_v22.py verify
```

V22 has eight slide pages and eight report pages. The visible slide text is at least
24px, all geometry/overlap checks pass, and contrast is at least 5.26:1. Rendered
screenshots and all report pages were visually checked. Tables and the acknowledgement
remain intact; earlier pagination defects were corrected. The workbook round-trips its
answers, questions and original Track 1 styles; its appearance was not visually rendered.
The isolated v22 public check passes with six blocked audit probes, without project
venv, network, protected paths or source checkout/history. No independent scientific
review is claimed. Final tests, preservation checks and init output are in session 62.

V19 checked every archive member and retained null array locally; a separate SciPy
implementation from original GCTX coordinates agrees on all 139 raw everolimus-labelled
comparisons (max error <4.75e-8). This is numerical verification, not an independent
scientific review. The new figure was visually checked; the initial legend spacing was
corrected. Final regression counts, preservation checks and fresh init output are in
session 58 progress. Session 59 makes the v19 check part of the combined harness,
removes the duplicate startup call, validates research routes/counts and pins the
frozen campaign audit. The isolated public run, new regressions and 346 preserved
input hashes are recorded in session 59 progress. `./init.sh` invokes the combined check.

## Blockers

- Biological advancement still needs endogenous function, model/branch qualification,
  tissue response, matched exposure and justified benefit/injury margins. Subject phase
  remains necessary for trans-specific attribution to the child; its uncertainty does
  not prevent properly qualified engineered-model research.
- Public transcriptomic query qualification is unresolved. Annotated seed independence
  is checked by v23, but off-target effects,
  selected-genotype transfer, joint-treatment response and chemical-identity gaps remain.
  More correlations cannot close these gaps; neither can an arbitrary stricter filter.
- Balnis units, secondary-control review, model dependence, cross-gene transfer and
  pretraining overlap remain limitations. More correlated structures do not resolve them.
- Fireworks/earlier alignment-service handling remains unverified. OpenAI no-training
  is an owner attestation, not an account or zero-retention audit.
- Challenge CC BY scope versus linked historical AF3/non-AVI Atlas output terms is
  unresolved. Numerical outputs/figures are omitted from the pitch/report; notices
  remain. The clarification draft has not been sent; do not contact organizers.
- Video runtime, recording, hosting, owner/live portal checks and Track 2 receipt remain
  open. Script times are allocations. Do not infer quota or test submission callbacks.
- Track 1 owner-reported 100/F-max 1 is retained; receipt/byte identity remains an
  administrative gap. Never request another upload to resolve it.

## Next actions

V23 changes assay controls without promoting a drug. A future presentation revision
can integrate this separate addendum while preserving v22. V22 integrates the earlier
findings into synchronized presentation/report materials. Rehearse
and record the v22 pitch
with the full acknowledgement inside three minutes. Resolve provider/distribution
items and verify final portal materials. Research
advancement begins with model/branch qualification and notes/track2-validation-v21.md.
The 27-claim register, five v23 supplemental challenges and decision contract retain
unknown biological gates and null margins.
No additional GPU jobs are pending.
BindCraft2 remains deferred without a functional target and validation route.

Raw subject files and narrative stay on the original machine and out of hosted context.
No family contact or re-identification. Remote model folders under ~/v remain in the
Nov24 deletion inventory. Preserve historical notices, failed attempts and all releases.
Keep the live retired-object purge guard for publication. Commit intended changes,
push configured origin and verify upstream equality.
