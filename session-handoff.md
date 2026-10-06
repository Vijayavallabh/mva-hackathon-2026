# Session handoff: Track 2 v32 materials and v31 Perturb-seq

7 October 2026 IST, session 71. Only feat-009 is active. Use `notes/track2-current.json`,
`scripts/check_track2_harness.py` and `notes/track2-reviewer-guide-v32.md`.
Presentation and harness v32 integrate completed v31 research. The v21 drug ledger,
base safeguards and all historical release inputs remain unchanged.

## Completed research and interpretation

`notes/track2-perturbseq-v31.md` reports public Replogle/Weissman data from 247,914
RPE1 and 310,385 K562 essential-screen cells. All eight H100s ran the public campaign:
27,628,823,832 CUDA correlations, 2,048 dependent split repetitions and 13,421,574 CPU
cross-cell comparisons. CUDA products totaled 6.476 seconds; workers took 40-59 seconds.
Sampled utilization peaked at 19-24%, with no new neural-model inference or continuous
saturation claim. All owned jobs are complete.

BUB1B depletion is detectable but poorly retrieves its own target among essential-gene
responses. Query-excluded split medians are 0.6572 in RPE1 and 0.1197 in K562;
first-direction median ranks are 171.5/2,154 and 323.5/2,077. Cross-cell BUB1B correlation
is 0.1043 versus MTOR 0.5836. One shared paired-guide construct contains 106/141 BUB1B
cells. Both retained control populations equal provider-selected core controls, so
an unselected-control sensitivity is unavailable. The original plan and amendment
remain distinct. RICTOR absence, low CDC20/AURKB coverage and unmeasured RPE1 RPTOR
transcript remain separate missing states.

Keep RPE1 as a functional-assay comparator pending independent perturbation/restoration,
protein/function, division fidelity, daughter survival and later function. MTOR matching
cannot qualify BUB1B, transfer signatures or establish joint drug rescue. The bounded
source review screened 98 returned titles and selected abstracts/passages. Favorable
clinical counterevidence remains alongside primary endpoint failures and species limits.
R48-R52 join earlier registers, for 52 claims across six registers.

## Provenance and preservation

Remote root: `/home/prachh/v/mva-track2-perturbseq-20261007-v31`.
Archive: `results/feat009/perturbseq-v31/perturbseq-v31-audit.tar.gz`, 226 files,
887,986,492 bytes, SHA-256
`8cd7f0b4c1c453fc10a586d66354c087aa95e2fbbb79ffc0247f9834641585ae`.
All file digests passed. Local complete-output reanalysis reproduces three cross-cell
matrices exactly; summary differences are at most 2.23e-16. Original-count CPU checks
ran on the owner host and agree within 2.83e-6. The archive omits six redownloadable
H5ADs and two reproducible arrays but binds their digests. All raw inputs are public.
The premature local verification during SCP failed with EOF; the completed transfer
then passed. The earlier pandas read-only audit failure is also retained.

Use `notes/track2-perturbseq-reproduction-v31.md`, the public audit and complete results.
No source VCF, read data or clinical narrative was transferred. All remote roots and
caches remain in the November 24 deletion scope. Previous ProteinMPNN/ESM/structure,
Evo2 and public expression work is preserved, including failed controls and reused wells.
`notes/track2-transcriptome-v19.md` remains the original expression campaign record.
V29 keeps its favorable limited HT29 result and weak MCF7 drug connection; the new
RPE1 evidence neither replaces those records nor supplies a joint rescue experiment.

## Current materials and verification

`notes/track2-report-v32.md`, `notes/track2-slides-v32.html`,
`notes/track2-pitch-v32.md`, `notes/track2-transcript-v32.txt` and video description
are synchronized. There are nine slides, 335 narration words, sixteen report pages
and eleven methods fields with a 313-word abstract. Runtime remains unmeasured.
Exports use `results/feat009/v32-slides-final-20261007` and
`results/feat009/v32-documents-final-20261007`. Snapshot/ZIP paths are in the current state.

```bash
./init.sh
uv run --no-project python scripts/check_track2_harness.py
uv run --no-project python scripts/check_track2_perturbseq_v31.py
uv run python scripts/audit_track2_harness.py
uv run python scripts/track2_release_v32.py verify results/feat009/jvv7_track2_research_v32
uv run python scripts/track2_bundle_v32.py verify
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

Final checks and fresh init output are in progress.md session 71. Preserve all earlier
bound inputs; future changes require a new version. No rescue-priority drug is supported.
Everolimus is an optional model-qualified probe; HCQ stays reserve. Phase and clinical
margins remain unknown. No wet-lab experiment has been performed. Unknown evidence
returns HOLD; safety failure overrides apparent benefit; all-pass permits preclinical
review only. Tumour killing is separate from non-cancer function.

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

The authorized compute and presentation integration are complete. Further scientific
advancement requires the v21 safeguards and v23/v25/v27/v29/v31 qualification amendments,
including independent attribution and joint functional treatment evidence. Extra splits
or larger language models cannot supply those measurements. BindCraft2 remains deferred
without a functional target and a validation route.

Rehearse and record the current script with the complete acknowledgement, measure runtime,
and host the video. Resolve provider/distribution items and inspect live portal requirements
before delivery. Feat-009 remains in progress for those separate steps. The latest full
requirements/discussions review is October 6, not a new October 7 community review.

Keep raw subject files and narrative on the original machine. No family contact or
re-identification. Retain the live purge guard, commit intended changes, push configured
origin and verify upstream equality. Preserve Track 1 v4; do not request another upload.
