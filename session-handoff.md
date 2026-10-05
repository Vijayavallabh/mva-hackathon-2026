# Session handoff: Track 2 v29 research and harness

6 October 2026 IST, session 69. Only feat-009 is active. Use `notes/track2-current.json`,
`scripts/check_track2_harness.py` and `notes/track2-reviewer-guide-v29.md`.
Harness v29 checks the new research alongside preserved presentation v28 and all older
research. The v21 drug ledger and decision contract remain unchanged.

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

## Preserved presentation and earlier evidence

`notes/track2-report-v28.md`, `notes/track2-slides-v28.html`,
`notes/track2-pitch-v28.md`, plain transcript, disclosure and workbook remain frozen.
The presentation has nine slides and 330 narration words. It integrates v27, but **does
not yet integrate v29**; read it with the new addendum. Exports remain under
`results/feat009/v28-slides-final-20261001/` and `v28-documents-final-20261001/`.

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
uv run python scripts/track2_release_v28.py verify results/feat009/jvv7_track2_research_v28
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Actual final checks and fresh init output are in progress.md session 69. Preserve all
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
  receipt remain open. September 24-25 requirements/discussions are dated reviews:
  three entries, latest only reviewed, quota unknown. No submission callback was used.
- Track 1's owner-reported 100/F-max 1 remains an attestation; receipt/byte identity is
  a separate administrative gap. Preserve submitted v4 and never request another upload.

## Next actions

The requested compute campaign is complete. Incorporate v29 into a new presentation
release if requested; do not alter v28-bound files. Next scientific advancement requires
the v21 safeguards plus the new endpoint-specific qualification amendments. BindCraft2
remains deferred without a functional target and a validation route.

Rehearse/record the eventual current script with the full acknowledgement and measure
runtime. Resolve provider/distribution items and inspect final portal requirements
before delivery. Feat-009 remains in progress for those separate steps.

Raw subject files and clinical narrative stay on the original machine and out of hosted
context. No family contact or re-identification. Keep the live retired-object purge
guard; commit intended changes, push configured origin and verify upstream equality.
