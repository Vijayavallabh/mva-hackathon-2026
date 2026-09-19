# Track 2 v5: editorial and scientific-fidelity review

2026-09-19 · feat-009 · baseline `13c8b46`

Scope: edit the current report and validation plan, then independently check the
main editor's v5 pitch and five-slide deck against the reviewed scientific record.
This review does not change the drug priorities, confirm phase or supply experimental
evidence. Historical Track 1 and Track 2 files remain outside the editing scope.

## Editing method and what changed

Read `humanizer/SKILL.md`, `no-ai-slop/SKILL.md` and its `eval.md` in full, then read
the complete v4 report and validation plan before writing the v5 files. Used the
humanizer draft/audit/revision loop and checked the result against the no-ai-slop
evaluation checklist. These are editing aids, not tests of authorship.

The report now opens with the research decision and reads as a standalone proposal.
Removed descriptions of the previous editing session from the scientific argument,
reduced decorative emphasis and split sentences where qualifications obscured the point.
Defined trans in context and expanded EFS. The validation plan keeps its detailed
requirements while using direct instructions; it explains the estimand and ICC where
they first matter. Technical distinctions and necessary negative statements remain.

The amount of detail is deliberate. The report and validation supplement preserve
the evidence and controls; the slides and narration carry the shorter presentation.
Editing does not reduce uncertainty or turn a research priority into a recommendation.
The mandatory acknowledgement is unchanged, including its original wording.

## Claim-preservation checks

| Area | Preserved in the v5 report or validation plan |
|---|---|
| Genetic starting point | Exact submitted pair, transcript, owner-reported Track 1 scores, missing independently archived receipt, unconfirmed trans and lack of exact-allele functional proof |
| Phenotype scope | Broad non-verbatim context; family history separate from the proband; no inferred cancer activity, fusion status, regimen, organ function or karyotype |
| Atlas | AVI values 33.7641 and 25.6084; merged-splicing values 0.08699 and 0.04813; DNM1 comparison 2.522; rank/aggregate semantics, dependence on existing predictors and absent tissue/junction evidence |
| Review limits | Adaptive rapid scoping review; baseline 53 sources/12 candidates; 19 accepted jobs with 18 completions and one retrieval failure; ten topic reviews, seven corrective passes and the rejected initial PP2A answer; six pre-execution rejections; 35 URLs are not validated studies |
| Decision ledger | The unchanged v4 ledger contains 32 cumulative source records and 11 decisions; no claim of 32 newly read papers or exhaustive September 19 coverage |
| Everolimus | Sole conditional constitutional priority; measure mTORC1 excess first; different mouse alleles; original phospho-p70 S6 kinase/phospho-4EBP1; two depicted animals/group; no randomization/blinding or rapalog rescue; correction retained |
| Clinical class evidence | Approved uses do not imply MVA/RMS approval; mixed everolimus findings; ARST0921 active comparator; ARST1431 66.8% versus 64.8% EFS, HR 0.86, 95% CI 0.58-1.26, p=0.44, 297 evaluable participants; nonsignificance does not prove zero effect |
| Other candidates | HCQ remains reserve; pralatrexate remains an optional fusion-positive RMS tumour-only direction; no subtype inference; all deprioritized and excluded directions, including the favourable evidence and counterevidence, remain |
| Corrected mechanisms | PP2A alignment is not completed segregation rescue; DT-061 uncertainty remains despite other-compound PR65 binding; p21 tissue directions differ; Ercc1 drug evidence is not BubR1 rescue; readthrough stages remain separate |
| Exposure | Compound, active metabolite, formulation, matrix, free fraction, schedule and sampling differences retained; all clinical margins unknown; no dose or numerical safe concentration |
| Model qualification | Wild type, mock edit, both single alleles, cis, trans and correction; engineered phase does not resolve subject phase; proposed three clones and three culture days are feasibility assumptions, not statistical power |
| Outcomes | Enrollment before exposure; accurate/error division, death, slippage, no division and tracking loss; first events separate from later daughter survival; no survivor-only denominator |
| Functional interpretation | Model-appropriate endpoint chosen before screening; downstream lineage benefit need not be chromosome repair; division and fate outcomes remain safety requirements |
| Analysis | Randomization, blinding, nested wells/cells/clones/days, missing-outcome bounds, confirmatory power from pilot variance, multiplicity and no outcome-driven optional stopping for statistical success; safety stops remain applicable |
| Advancement | Unacceptable deficient-normal injury cannot be offset by tumour activity; recurrence excludes durable eradication but not every on-treatment benefit; passing preclinical criteria does not authorize patient dosing |
| Disclosure | OpenAI API non-training statement remains owner-attested; Google Atlas precomputed outputs and terms retained; Fireworks credits do not verify training/retention; no new GLM calls; K-Dense installation is not inference |
| Delivery | Report/deck/script are not a recorded or hosted pitch or a receipt; live rules, identity/quota, provider confirmation and owner review remain open |

All external source URLs in the report match v4 except the intended cross-link from
`track2-validation-v4.md` to `track2-validation-v5.md`. All external source URLs in the
validation plan match v4. Later packaging checks converted relative repository links
in the pitch/validation plan to absolute links to the same sources, so copied package
files do not contain broken relative links. The report's acknowledgement is byte-identical to v4.
New v5 reproduction commands supplement, rather than replace, historical verification.

## Independent pitch and deck review

The pitch preserves the difference between constitutional function and tumour control,
the conditional mTOR rationale and the negative ARST1431 result. It states that no
experiments have been performed and that phase, efficacy and exposure remain unresolved.
It retains the entinostat jurisdiction caveat, the engineered-phase distinction,
randomization/blinding/replication, all major fate categories and separate tracking-loss
reporting. It discloses the three used providers and unresolved Fireworks settings.
The full required acknowledgement is retained in the video description.

The figures are conceptual. Abstract chromosome marks do not depict the subject's
karyotype. Branch lengths and symbols carry no measured frequency, effect size or drug
response. The fate tree separates missing tracking information from observed biological
outcomes; daughter survival follows division rather than redefining the first event.
The report and narration supply the qualifications that do not fit on screen.

| Finding | Required or suggested revision | Status |
|---|---|---|
| Slide 2 said to stop when injury "outweighs benefit" | State that unacceptable deficient-normal injury stops advancement regardless of tumour benefit | Resolved: "Stop for absent pathway excess or unacceptable injury." |
| Slide 5 used "Advance" without a local definition | Specify further preclinical review so that passing gates cannot imply patient dosing | Resolved: "Preclinical only" appears directly below "Advance"; narration explicitly rejects patient dosing |
| Slide 4 title claimed to follow lost cells | Account for tracking loss without implying that unobserved fates are known | Resolved: "Account for every cell" and "Report tracking loss separately." |
| Pitch panel answer summarized ARST1431 as no tumour benefit | Prefer the measured endpoint: no demonstrated EFS benefit from adding temsirolimus | Resolved: the answer explicitly names ARST1431, EFS and addition of temsirolimus |

Final source review found no remaining material scientific-fidelity issue. Reviewed deck
SHA-256: `61a209762b61ac16962ba9c87a17c9c1167720cc4aa32477ac8992d55bb0ae86`.
Reviewed pitch SHA-256: `ae627a43cbea30974c83d42beb80d4ab93866fa4a3f54d243080c15eb14cc6d6`.
The narration contains 337 whitespace-separated words, excluding headings. The stated
112.3 words/minute is a three-minute planning estimate, not a recorded duration. The
video description contains the exact required acknowledgement.

Haas 2019 matches the existing ledger. A bounded metadata check confirmed that Yamada
2022 is the issue citation year, despite the DOI containing 2021 and an online article
date of 2021-12-27. The issue date is 2022-02-18. This was a metadata check, not a new
full-paper review. Direct PMC rendering returned a browser challenge, and an initial
author-institution URL with a trailing slash failed. The indexed primary record and
author-institution metadata supplied the date distinction.
[PubMed record](https://pubmed.ncbi.nlm.nih.gov/35141499/),
[author-institution record](https://tohoku.elsevierpure.com/en/publications/torc1-inactivation-promotes-apcc-dependent-mitotic-slippage-in-ye)

## Editorial evaluation

All applicable no-ai-slop checks passed on the edited report and validation plan.
The scientific register remains neutral; no invented personal voice, examples, study
results or certainty were added. Specific quantitative findings and source attribution
remain. Strong existing sentences were retained where they already explained the point.
Lists and tables remain where they compare decisions or specify an experimental protocol.
The drafts contain no em/en dashes or decorative bold. Reading them aloud prompted
sentence-level edits, not removal of scientific caveats.

This review covers text and scientific meaning. Pixel-level inspection, browser/PDF
rendering, release integrity tests and the repository disclosure audit are separate checks
recorded by the main editor. Neither this review nor a rendered slide verifies the
runtime or accessibility of a future hosted video.
