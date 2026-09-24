# Session handoff — Track 2 v16 presentation / v15 falsification revision

Updated 2026-09-24, session 55. Only feat-009 is active. Use
`notes/track2-current.json` as the current artifact/status record. Presentation is v16 and
science is v15; drug dispositions remain those of v10. Prior v1–v15 snapshots
and submitted Track 1 v4 are immutable.

## Current artifacts and result

- `notes/track2-report-v16.md`, `notes/track2-evidence-v15.json` (63 sources/11 decisions)
  and `notes/track2-validation-v15.md` carry the revised interpretation and protocol.
- `notes/track2-falsification-review-v15.md`, the 19-claim register, source audit and
  analysis record support/challenge, falsifiers, stop/reopening criteria and next actions.
- `notes/track2-slides-v16.html`, `notes/track2-pitch-v16.md` and plain transcript:
  nine slides, 328 narration words. Runtime remains unmeasured.
- `notes/track2-video-description-v16.md` retains full acknowledgement/provider/AF3 terms.
- Final PDF/PNGs/terms: `results/feat009/v16-slide-review-final-20260924/`.
- New research snapshot and recording-materials bundle use
  `results/feat009/jvv7_track2_research_v16` and
  `results/feat009/jvv7_track2_video_materials_v16.zip`.

The newer sequence models still pass the original primary ordering in 12/12
model/window comparisons. Adding already-retained secondary controls breaks complete
separation in 8/12; 11/24 retained-control scores are negative. This is post-hoc
sensitivity using one study, not a new primary gate or clinical accuracy estimate.
D882A's secondary label is stated in main text; its supplement remains unreviewed.
Keep every result and older failed controls. No new GPU inference was needed.

The Balnis supplement was downloaded and its conflicting ex vivo units visually
verified: PDF page 12 says 10 mM, page 15 says 10 micromolar in related methods.
Do not silently correct either or adopt the disputed concentration. Qualitative
support for a separate flux/function question remains indirect. No author contact.

The new protocol adds growth-rate and flux/pH artifact controls, explicit useful
output/denominators, missingness bounds, meaningful-effect/safety margins before
confirmation, and stronger delayed-fate/recovery checks. Unknown means hold; failed
means stop the tested context. Favorable safety evidence is retained with context
limits. No rescue-priority drug; everolimus optional qualified mechanistic probe;
HCQ reserve. Phase and clinical exposure remain unresolved. No wet-lab results.

## Verification

Run the commands below. Actual final outputs, test counts, release/bundle hashes,
publication checks and Git synchronization are recorded in session 55 of progress.md.
Visual review covers all nine pages, full-size changed pages, zero clipping/overlap,
24px minimum and a passing 640px viewport. Software verifies consistency, not biology.
The audit was performed by the author; no independent specialist or agent review.

```bash
./init.sh
uv run python scripts/check_track2_harness.py
uv run python scripts/track2_falsification_v15.py check
uv run python scripts/track2_release_v16.py check
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v16.py verify results/feat009/jvv7_track2_research_v16
```

## Next discriminating work

1. Qualify endogenous allele effects and correction in a relevant non-cancer model;
   distinguish RNA/protein, checkpoint activation/maintenance/silencing, attachment,
   useful division and lineage function. Keep single/cis/trans alternatives.
2. Resolve source concentration ambiguity before using that experiment to design an
   exposure-linked study. Broader source retrieval and independent functional controls
   can improve the audit; more correlated structure predictions will not close it.
3. Before any new candidate/model/endpoint or promotion, update the relevant claim's
   falsifier and reopening rule, search contrary and favorable primary evidence,
   distinguish unknown from failed and create a new version. Do not tune criteria
   after confirmatory outcomes. BindCraft2 remains deferred without a functional target.
4. Rehearse/record/host the nine-slide video with full acknowledgement; separately
   resolve provider/owner/live portal checks and archive a submission receipt.

## Blockers

- Endogenous function, subject phase, model qualification, tissue response, clinical
  exposure and meaningful assay margins are unestablished. No biological advancement.
- Balnis ex vivo units unresolved; 2012 secondary-control supplement not independently
  reviewed; cross-gene transfer/pretraining overlap and model dependence remain.
- All four new Firecrawl searches failed. Eight initial structured requests failed;
  adaptive and journal/registry retrieval supplied bounded evidence. One incorrect
  ARST identifier was rejected and the correct identity verified. Access failure is
  not a null result. Search depth/correction coverage is explicitly incomplete.
- Fireworks and external alignment-service training/retention remain unverified;
  OpenAI no-training is an owner attestation. No new provider-policy attestation.
- Narration runtime, recording, hosted URL, owner/live checks and Track 2 receipt open.
- Track 1 owner-reported 100/F-max 1 is retained; independent receipt/byte identity
  remains unverified. Never request another upload to resolve that archive gap.

## Preservation and data boundary

No protected subject file was opened by the research workflow or transmitted. Local
startup integrity programs may process permitted local data without exposing records.
No clinical narrative/VCF/read data may leave the original box or enter hosted context.
No family contact or re-identification. Remote model directories under ~/v remain in
the deletion inventory; no owned model job is pending from this cycle. Check actual
hardware before new compute. All source failures and initial/final slide previews
are retained. Keep AF3 terms/notice with exported derivatives and live purge checks
for publication. Close: 2026-10-24 23:59 UTC; deletion/confirmation: 2026-11-24.
Commit intended changes, push configured origin and verify upstream equality.
