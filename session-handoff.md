# Session handoff: Track 2 v30 presentation and harness

6 October 2026 IST, session 70. Only feat-009 is active. Use `notes/track2-current.json`,
`scripts/check_track2_harness.py` and `notes/track2-reviewer-guide-v30.md`.
Harness and presentation v30 integrate the frozen v29 research with all earlier
findings. The v21 drug ledger and decision contract remain unchanged. No model runs
were repeated for this update.

## New completed research

`notes/track2-orthogonal-v29.md` reports two completed waves on all eight H100s:

- ProteinMPNN through the pinned Anthropic optimization toolkit: 528 contexts,
  67,584 fixed-site samples, 10,560 aggregate site/amino-acid records. Four related
  checkpoints and six WT backbones are not independent biological replicates.
- Symmetric held-out expression analysis: 400 fits and 820,147,416 comparisons.
  All evaluated genes are excluded from projection fitting. CRISPR QC-only sensitivity
  is explicit; RNAi qualification limits persist.

N1002K ranks lowest among 17 matched N-to-K sites on all WT backbone/checkpoint
combinations, but historical control ordering passes only 1/24 primary and 0/24
expanded comparisons. Mutant-predicted backbones shift the score substantially,
including positive values. Do not infer stability, function or a drug branch.
D882N is retained for the historical 2012 measured endpoints, not universally functional:
2019 CENP-E phosphorylation and 2020 KARD/scaffolding results require endpoint-specific
interpretation. The catalytic disagreement is not resolved here.

HT29 PRIME RNAi/CRISPR agreement survives both symmetric fitting and removal of failed
CRISPR profiles. One guide, tumour context and RNAi seed/potency uncertainty remain.
MCF7 BUB1B drug reversal weakens after adjustment; its BUB1B query is absent after QC
restriction. MTOR matching remains first. Smaller within-fold ranks cannot be compared
with prior full-panel ranks. No joint drug-plus-deficit response was measured.

Use `notes/track2-orthogonal-validation-v29.md`, complete results, source review,
R43-R47 register, compute record, audit and reproduction guide. All 47 claim records
remain available. Failed setup/runtime attempts and original outputs are preserved.
The stock/exact pilot and direct conditional API check passed at their stated scope.

All owned GPU jobs finished. Remote folder:
`/home/prachh/v/mva-track2-orthogonal-20261006-v29`.
Original 3,838-file archive:
`results/feat009/orthogonal-v29/orthogonal-v29-audit.tar.gz`.
Its SHA-256 is `373d78784dabc003335813736f907348f7c90aaac510e242b0c917eff8e5280e`.
Local extraction/reanalysis is separate from public CPU consistency checks.
No raw subject transfer or new hosted biological model provider occurred. This folder,
its caches and all earlier `~/v/mva-*` folders remain in the November 24 deletion scope.

## Current presentation and preserved evidence

`notes/track2-report-v30.md`, `notes/track2-slides-v30.html`,
`notes/track2-pitch-v30.md`, plain transcript, disclosure and methods workbook
integrate v29. Nine slides accompany 326 narration words; runtime is unmeasured.
Exports are under `results/feat009/v30-slides-final2-20261006/` and
`v30-documents-final2-20261006/`. Snapshot and ZIP paths are in the current-state file.
All v28-bound sources and the frozen v29 research remain unchanged.

Keep frozen `notes/track2-transcriptome-v19.md`, v23 RNAi, v25 CRISPR and v27
protein-background/expression records. Their same-well overlap, failed QC, seed effects,
five- versus six-reagent HT29 findings and control failures persist. Earlier negative
scores and repeated windows are not calibrated probabilities. AF3/ESMFold confidence
does not establish function. Evo2's BRCA1 benchmark does not validate BUB1B.

No rescue-priority drug is supported. Everolimus remains an optional model-qualified
mechanistic probe; HCQ stays reserve. Phase, endogenous allele effects, relevant tissue
response and clinical exposure/benefit/injury margins remain unresolved. No wet-lab
experiment has been performed. Unknown evidence returns HOLD; safety failure overrides
apparent benefit; all-pass permits only further preclinical review. Tumour killing is
separate from non-cancer function.

## Restart and verification

```bash
./init.sh
uv run --no-project python scripts/check_track2_orthogonal_v29.py
uv run --no-project python scripts/check_track2_harness.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v30.py verify results/feat009/jvv7_track2_research_v30
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Actual final checks and fresh init output are in progress.md session 70. Preserve all
older bound inputs and use new versions for future research or presentation changes.

## Blockers

- Independent BUB1B perturbation/restoration, relevant non-cancer model qualification
  and joint functional treatment evidence remain missing. No compute closes these gaps.
- Endogenous branch qualification, independent confirmation and justified benefit,
  injury and exposure margins remain necessary. Protein control endpoint conflicts,
  predicted-backbone dependence and training overlap limit score interpretation.
- Balnis ex vivo units conflict by 1,000-fold; both disputed values stay quarantined.
- Fireworks and the earlier alignment service have unverified handling settings.
  OpenAI no-training remains an owner attestation, not an account/retention audit.
- Challenge CC BY scope versus linked historical AF3/non-AVI Atlas terms is unresolved.
  Preserve notices and the unsent clarification; organizer contact is not authorized.
- Video recording, runtime measurement, hosting, owner/live-portal checks and Track 2
  receipt remain open. October 6 requirements/discussions refresh covers 26 threads and 79 visible comments:
  three entries, latest only reviewed, quota unknown. Judging extends to December 17
  and winners to December 18; submission and November 24 deletion stay unchanged.
  Provider clarification does not verify account settings. No submission callback was used.
- Track 1's owner-reported 100/F-max 1 remains an attestation; receipt/byte identity is
  a separate administrative gap. Preserve submitted v4 and never request another upload.

## Next actions

The requested compute campaign and v30 presentation integration are complete. Preserve
all bound versions; future changes need a new release. Next scientific advancement requires
the v21 safeguards plus the new endpoint-specific qualification amendments. BindCraft2
remains deferred without a functional target and a validation route.

Rehearse/record the eventual current script with the full acknowledgement and measure
runtime. Resolve provider/distribution items and inspect final portal requirements
before delivery. Feat-009 remains in progress for those separate steps.

Raw subject files and clinical narrative stay on the original machine and out of hosted
context. No family contact or re-identification. Keep the live retired-object purge
guard; commit intended changes, push configured origin and verify upstream equality.
