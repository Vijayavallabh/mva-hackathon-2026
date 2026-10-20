# External review adjudication, version 46

20 October 2026. The owner supplied an outside reviewer's final Track 2 review.
This adjudication accepts only recommendations that are consistent with current
evidence and the official rubric. No reviewer contact occurred beyond receipt of
this review. No biological validation, video recording, hosting or submission is
established.

## Accepted and implemented

1. **Conditional nomination, not therapeutic promotion.** The report and reviewer
   brief now state: everolimus is nominated as a conditional approved-drug
   hypothesis worth investigating, not a treatment recommendation or rescue-priority
   claim.
2. **Candidate-selection rationale.** Judge questions now explicitly answer why
   everolimus rather than NAD/SIRT2 or HCQ: approval and mTORC1 pharmacology make a
   bounded downstream test concrete; NAD/SIRT2 is more proximal but sex/site/context
   evidence conflicts; HCQ remains reserve.
3. **Evidence-status chain.** The report now labels each major link: gene-level
   mechanism established; pair-specific function, relevant non-cancer dysfunction,
   mTORC1 state, drug response and sustained output unmeasured.
4. **Four-arm language.** The deck/report/lab handoff use **deficient/corrected ×
   vehicle/everolimus**, not ambiguous "joint treatment."
5. **Primary endpoint and units.** The lab handoff now defines the primary endpoint as
   useful cellular output per founder cell enrolled before exposure, with a
   prespecified daughter-fate/recovery window; cultures are independent units, cells
   are nested observations.
6. **Useful-output denominator.** The synthetic example now defines founder cells,
   the ratio numerator, useful-output numerator and follow-up, and the deck says
   "Useful cellular output," not "Patient-centered outcomes."
7. **Contrary-evidence framing.** "Falsification" is replaced in current-facing
   materials with "contrary evidence constrained us" / "evidence that constrained us."
8. **Software verification versus biological validation.** The report and deck state
   that the demo verifies implementation, not biological validity.
9. **Decision contribution of each computation.** The report now states what each
   computational analysis changed and which analyses remain appendix-level rather
   than validation.
10. **Closed-access reading depth.** The v45 literature addendum honestly labels
    griseofulvin/norlichexanthone and computational BUB1B inhibitor papers as
    abstract/metadata only and excludes them from constitutional-MVA promotion.
11. **Narration revision.** The new v46 script is 369 words, still within the planned
    three-minute allocation, and says "nominate everolimus conditionally," "four
    arms," and "software, not biology."

## Accepted in principle, retained within existing artifacts

- The reviewer's request for transcript accession/version, DNA-level description,
  zygosity and phase status is covered by the report's caveat that engineered models
  cannot establish subject phase and the retained pair label; no additional protected
  genotype detail is added here.
- The reviewer's H100 robustness workplan is accepted as a future option, but no new
  GPU campaign is justified now. Existing held-out, plate, guide and sensitivity
  limitations are already reported in the v36 optical record. The current decisive
  evidence is biological, not another model benchmark.
- The reviewer's suggested video timing is broadly consistent with the existing script.
  The owner's actual measured runtime remains decisive.

## Not accepted as stated

- We do not call everolimus the "best" candidate or imply superiority over NAD/SIRT2.
  The evidence supports only conditional eligibility for investigation.
- We do not imply a patient outcome from the synthetic example. It is explicitly
  patient-motivated cellular reasoning, not measured patient benefit.
- We do not replace the current report with the reviewer's suggested thesis without
  preserving the existing safety, missing-data and stop rules.
- We do not treat the reviewer's proposed GPU allocation as evidence or authorization
  to run more compute. GPU use remains capability, not validation.
- We do not silently edit frozen v40 recording assets. The accepted narration changes
  were copied into new v46 assets.

## Verification

Run:

```bash
uv run --no-project python scripts/track2_public_review_v43.py
uv run python scripts/track2_release_v43.py check
uv run python scripts/check_track2_harness_v43.py
uv run python scripts/track2_release_v43.py verify results/feat009/jvv7_track2_research_v43-verified58
uv run python scripts/track2_bundle_v43.py verify
```

The second command is intentionally not the current entry point; the current harness
is `scripts/check_track2_harness_v43.py`. This note records adjudication, not
biological validation.
