# Session handoff: Track 2 v18 presentation / v19 public transcriptome addendum

27 September 2026, session 58. Only feat-009 is active. Authoritative paths are in
`notes/track2-current.json`. Submitted Track 1 v4 and every v1-v18 bound input/package
remain preserved. V18 is the frozen presentation; v19 is a separate completed public
perturbation reanalysis. V15 drug dispositions remain unchanged.

## Current materials

- `notes/track2-transcriptome-v19.md`: new findings and revised experiment requirements;
  complete results, fixed plans, source/chemical-identity review, SVG and audit accompany it.
- `notes/track2-transcriptome-reproduction-v19.md`: exact computation scope, limits,
  executed commands and archive verification. The completed remote campaign is under
  `/home/prachh/v/mva-track2-transcriptome-20260927`; no worker/monitor remains active.
- `results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz`: verified
  457-file audit archive. No subject input or new hosted model was used.
- `notes/track2-report-v18.md`: 2,119 words, 27.18% shorter than v17. Full disclosure,
  citations, methods B7-B17 and acknowledgement preserved; abstract 166 words.
- `notes/track2-slides-v18.html`: eight redesigned slides, seven SVG figures.
- `notes/track2-pitch-v18.md` and `notes/track2-transcript-v18.txt`: 334 spoken words,
  reframed for the Track 2 candidate, mechanism, experiment, impact and reuse.
- `notes/track2-video-description-v18.md`: matched AI disclosure and acknowledgement.
- Six-page PDF, Markdown and filled workbook: `results/feat009/v18-documents-final-b-20260925/`.
- Eight-slide PDF/PNGs: `results/feat009/v18-slides-competition-20260925/`.
- Research snapshot: `results/feat009/jvv7_track2_research_v18`.
- Recording/review ZIP: `results/feat009/jvv7_track2_video_materials_v18.zip`.
- `notes/track2-v18-design.md`, `track2-v18-editorial-review.md` and versioned audits
  document the skills used, changes, source preservation and visual checks.
- Public review: `notes/track2-reviewer-guide-v18.md`. Remaining delivery steps and
  unsent clarification: `notes/track2-owner-readiness-v18.md`.

## Official brief and competition framing

The September 25 anonymous website recheck finds the same source revision
`aeeef5ad49f51204a7439352e59e9d310aee5e9e`. Six pinned source files are unchanged;
trimmed live submission component 40 matches its source. Full runtime config differs,
so do not claim the entire config is identical. See `notes/track2-v18-brief-review.md`
and `notes/track2-v18-brief-audit.json`.

Track 2 seeks approved-drug hypotheses supported by variant mechanisms. The eight-slide
story now leads with everolimus, explains the conditional BUB1B/BUBR1 link, weighs
compound-specific evidence, proposes qualification/probing/confirmation, defines useful
output, and closes with impact and reuse. Rubric weights remain 35/25/25/15.
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

The v15 ledger has 63 sources, 11 unchanged decisions and 19 falsifiable claims.
Primary protein ordering passes 12/12; post-hoc expanded-control separation fails 8/12;
11/24 retained-control scores are negative. Small/dependent controls cannot calibrate
clinical pathogenicity. The secondary-control supplement remains independently unreviewed.
Balnis source units conflict by 1,000-fold; neither value sets a dose. Unknown means
hold; failed safety stops; all-pass permits preclinical review only.

## Verification and restart

```bash
./init.sh
uv run --no-project python scripts/track2_public_review_v18.py
uv run python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_transcriptome.py
uv run --no-project python scripts/verify_track2_transcriptome_archive.py results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz
uv run python scripts/track2_release_v18.py verify results/feat009/jvv7_track2_research_v18
uv run python scripts/track2_bundle_v18.py verify
```

All eight final slide PDF pages and six report pages were visually reviewed. Geometry,
minimum 24px slide text, contrast and 640px viewport pass. The PDF embeds fonts; HTML
uses sans-serif fallback where Ubuntu is unavailable. Initial cramped text/fork alignment
was corrected. Workbook contents round-trip; workbook appearance was not visually rendered.
The isolated public checker passes without data/results/logs/.env/.git or network
(0.315 seconds, one local consistency check). Final regression counts, release/bundle
hashes, publication checks and fresh-shell init output are in session 57 progress.
No independent reviewer inspected this visual/editorial revision.

V19 checked every archive member and retained null array locally; a separate SciPy
implementation from original GCTX coordinates agrees on all 139 raw everolimus-labelled
comparisons (max error <4.75e-8). This is numerical verification, not an independent
scientific review. The new figure was visually checked; the initial legend spacing was
corrected. Final regression counts, preservation checks and fresh init output are in
session 58 progress. The v19 check is now part of `./init.sh`.

## Blockers

- Biological advancement still needs endogenous function, subject phase, model/branch
  qualification, tissue response, matched exposure and justified benefit/injury margins.
- Public transcriptomic query qualification failed. RNAi seeds/off-target effects,
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

Rehearse and record the eight-slide pitch with the full acknowledgement inside three
minutes. Resolve provider/distribution items and verify final portal materials. Research
advancement begins with model/branch qualification, the existing falsification plan
and the v19 experimental requirements. No additional GPU jobs are pending.
BindCraft2 remains deferred without a functional target and validation route.

Raw subject files and narrative stay on the original machine and out of hosted context.
No family contact or re-identification. Remote model folders under ~/v remain in the
Nov24 deletion inventory. Preserve historical notices, failed attempts and all releases.
Keep the live retired-object purge guard for publication. Commit intended changes,
push configured origin and verify upstream equality.
