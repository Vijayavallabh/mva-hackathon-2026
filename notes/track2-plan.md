# Track 2: evidence-led repurposing specification

Started 2026-09-08, feat-009, baseline `21896c6`. Research only; no prescribing,
patient contact, sample acquisition, external raw-data transfer or portal upload.
The submitted Track 1 v4 CSV and report are immutable for this work.

## Question and scope

Which already-approved medicines merit **preclinical investigation**, given the
leading BUB1B pair and the broad malignancy, renal, growth/muscle and developmental
context? Evaluate constitutional functional rescue separately from tumour killing.
Compare with vehicle, isogenic correction and clinically relevant oncology controls;
seek improved chromosome segregation or tumour-selective activity without injuring
nonmalignant BUB1B-deficient cells. Family reproductive history informs inheritance
reasoning, not a symptom or treatment target in the child.

The owner reports a first Track 1 submission scoring 100 rank points and F-max 1,
displayed at position 93. Receipt and uploaded-byte identity have not been independently
verified. This supports proceeding on the selected pair; it does not supply functional
assays, segregation, tumour genotype or clinical treatment information. **Trans phase
remains unconfirmed.** Do not recast historical hypothetical tests as official scores.

## Acceptance criteria for the research package

1. Recheck and record public Track 2 rules, source revision and hashes; reconcile stale
   one-submission documentation. Keep report completion distinct from video and upload.
2. Explain gene, allele and pathway evidence separately. Do not turn a missense predictor,
   an unrelated mutant, or a protein-abundance increase into demonstrated functional rescue.
3. Perform a documented rapid scoping review, including negative studies, across public web,
   Europe PMC and complementary PubMed/trial/regulatory searches. Record query dates,
   coverage limits and access failures. Do not claim an exhaustive systematic review.
4. Produce a machine-readable source/claim/candidate ledger, with approved-use jurisdiction,
   evidence model, target direction, mechanistic bridge, counterevidence, normal-tissue risk,
   exposure gaps, decision and falsification criterion. No invented efficacy probabilities.
5. Independently verify citation identifiers/metadata and retain public-source provenance.
   Content support still requires human/agent reading; DOI resolution alone is not validation.
6. Use explicit gates before any prioritization: regulatory status, correct intervention
   direction, constitutional-versus-tumour context, adequate exposure and safety. Unknowns
   stay unknown. Assess whether the shortlist changes when indirect evidence is removed.
7. Write a detailed Markdown report, concise evidence table and a three-minute pitch script
   and storyboard. Include methods, AI disclosure, limitations and required acknowledgement.
8. Specify a staged, falsifiable validation plan: genotype/phase alternatives, protein/RNA
   and checkpoint readouts, matched normal/tumour testing, blinded assessment, replication
   units, exposure constraints, stop rules, and future power estimation from pilot variance.
   Proposed assays are not performed experiments. Do not fabricate experimental outputs.
9. Implement repeatable offline ledger/package checks with adversarial synthetic tests.
   Verify Track 1 hashes unchanged, disclosure gate and fresh `./init.sh`.
10. Keep a devil's-advocate revision log. Review the eventual diff against this specification
    and repository standards in two independent review agents, fix material issues, record
    remaining scientific uncertainty, commit and push cleanly.

## Search and evidence policy (declared before the structured search)

Include primary gene/variant functional studies, directly relevant animal/cell work,
prospective clinical trials in the tumour type, and official medicine labels. Reviews
may aid discovery but are not substitutes for primary claim support. Search without a
lower date cutoff through 2026-09-08; identify preprints and publication updates explicitly.
English accessible text is a practical limitation, not a scientific quality criterion.
Exclude advertisements, generic longevity claims, docking-only efficacy claims and
uncorroborated AI summaries. Retain mechanistically tempting but rejected candidates.
Author prestige and citation count do not override design quality or contradictory results.

Initial exploratory searches identify BUBR1 dosage/stability, NAD/SIRT2, mTOR, aneuploid
stress and rhabdomyosarcoma trials as themes. This is an adaptive scoping search, not a
preregistered confirmatory systematic review. The clinical-stage/risk group and ongoing
regimen are unknown; no trial eligibility or patient-specific safety conclusion is possible.

## Review checkpoints

- R0: challenge the disease/allele model before candidate selection.
- R1: challenge every intervention's direction and evidence transfer.
- R2: actively seek negative trials, toxicity, pharmacokinetic barriers and alternatives.
- R3: sensitivity/ablation of evidence; reject apparent rescue caused by cytostasis or death.
- R4: independent specification and standards reviews; revise and rerun checks.

Feat-009 remains in progress until the full deliverable set is ready. A report draft,
storyboard or locally generated video is not a hosted pitch URL or submission receipt.

## Session 32: final scientific/exposure review

The user explicitly requests extensive final review. Baseline is `1a97a0e` (clean and
upstream-matched at start). The detailed bounded specification and findings are in
`notes/track2-final-review.md`. Reuse the two-axis independent review requirement above
against this baseline, including new exposure semantics, public-only retrieval and
preservation of historical bundles. Scientific unknowns must remain explicit; this review
does not authorize a portal upload, patient intervention or changes to Track 1 artifacts.
