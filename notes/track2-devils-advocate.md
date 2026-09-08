# Track 2 adversarial revision record

Research checkpoints for feat-009, started 2026-09-08 at `21896c6`. Objections change
the work; they are not a cosmetic list attached to an unchanged recommendation.
No clinical efficacy, allele function or patient trans phase is established by this log.

## R0 — challenge the starting model

| Tempting claim | Objection | Revision / consequence |
|---|---|---|
| A maximum Track 1 score proves the whole mechanism | It is an owner-reported answer-key result, not phase or functional measurement | Preserve the result and its attestation level; retain cis/trans experimental alternatives. |
| A stop plus a damaging missense proves biallelic loss of function | Nonsense-mediated decay and this missense allele's function were not measured | Separate predicted consequences from RNA/protein/checkpoint assays. |
| Mouse L1002P is our human residue-1002 variant | Different substitution and species numbering; it models human L1012P | Explicitly reject allele equivalence; downgrade mTOR rationale to other-allele animal evidence. |
| BUBR1 is categorically catalytically inactive | Primary studies disagree about catalytic activity | Explain the controversy; therapeutic direction must not depend on settling it. |
| Renal calcification proves renal failure | Filtration is not supplied | Retain renal safety concern without inventing eGFR, dose or eligibility. |

## R1 — challenge intervention direction and transfer

| Tempting claim | Objection | Revision / consequence |
|---|---|---|
| An aneuploid-cell poison is ideal for MVA | Nonmalignant deficient cells may share the vulnerability | Tumour killing and constitutional functional rescue are separate objectives; matched-normal injury stops advancement. |
| Mouse mTORC1 activity establishes everolimus efficacy | No rapalog rescue experiment; allele/tissue-specific signal | Require pathway excess, target engagement and functional benefit at appropriate exposure. |
| Chloroquine sensitivity proves HCQ works | Different compound; model and exposure transfer unvalidated | HCQ is a conditional direct-test hypothesis, not a demonstrated response. |
| More BUBR1 protein equals repaired checkpoint | Stable protein can remain dysfunctional | Demand endogenous full-length protein and chromosome-segregation endpoints. |
| Fewer abnormal cells means corrected chromosomes | Arrest or selective death changes the denominator | Track completed divisions, errors per division, viability and post-washout function. |
| A SIRT2 mouse result justifies vitamin treatment | NMN, nicotinamide and SIRT2 transgene are different interventions | Exclude supplement inference; distinguish abundance from lifespan intervention. |
| Genetic removal of senescent cells validates a drug combination | INK-ATTAC is not dasatinib/quercetin | Exclude unvalidated combination; preserve alternative mechanisms as research context. |

## R2 — actively seek evidence against the shortlist

- Retained both ARST0921 and ARST1431. Relapse active-comparator EFS advantage cannot
  replace the later negative chemotherapy-addition trial or establish an isolated drug effect.
- Added primary monotherapy and cixutumumab/temsirolimus phase II studies. Corrected an
  overbroad negative interpretation: failure of the early response criterion does not
  erase one late RMS response. Nonresponse, stable disease and EFS are different endpoints.
- Checked the JCI corrigendum: corrected Figure 2E images/methods are not independent
  replication of Figure 5's mTOR association. No correction-free certainty claimed.
- Verified EU ataluren non-renewal rather than treating an old preclinical paper as
  current approval. Regulatory facts are jurisdiction-specific.
- Compared label risks for all approved-drug entries. No drug is called low risk merely
  because it is inexpensive, familiar or used for a different pediatric indication.
- Kept clinical exposure margins unknown: no experimental concentration-response data
  or assay-specific free-exposure comparison exists for this pair.
- Corrected source reading-depth labels to selected sections/abstracts. Fetching a page
  or resolving its DOI is not full-text review or claim confirmation.

## R3 — computation and alternative explanations

The offline evidence stress test is deliberately qualitative, not a drug-response model:

| Required evidence / removed assumption | Conditional screens remaining |
|---|---|
| Baseline indirect rationale | Everolimus; hydroxychloroquine |
| Require direct-pair intervention evidence | None |
| Require a measured clinical exposure margin | None |
| Remove the other-allele animal rationale class | Hydroxychloroquine only |
| Remove the other-compound/cancer rationale class | Everolimus only |

Removal is by the declared principal rationale class, not a complete causal graph or
source-by-source meta-analysis. Remaining entries are not independent replications or
validated treatments. Passing ledger tests checks consistency, not biological truth.

An actual retrieval bug returned a version-only Europe PMC object with HTTP 200.
The first summary was invalid; it is excluded from evidence. Schema checks and a
regression test prevent missing results from becoming a false zero-hit claim.
Package checks detect changed inputs, missing/extra files, path traversal, stale or
tampered derived tables and accidental changes to the immutable Track 1 package.

## R4 — independent reviews and final verification

Two separate agents reviewed `git diff 21896c6...9ccf8b2` against repository standards
and `track2-plan.md`, then independently rechecked the working-tree fixes. Neither opened
protected subject inputs or edited files. These are not clinical/pharmacology sign-off
or evidence of performed experiments. Initial findings are preserved separately below.

### Standards

No confirmed AGENTS.md violation. Three implementation findings and one heuristic finding:

- P2: successful HTTP responses could produce false success accounting. Empty Europe PMC
  bodies and error envelopes from PubMed/ClinicalTrials were not counted as failures.
- P2: malformed nested Europe PMC/Crossref/Space objects could raise unhandled
  `AttributeError`, aborting collection instead of recording an unavailable result.
- P2: omitting `clinical_exposure_margin` passed validation but failed sensitivity analysis.
- Heuristic, possible Primitive Obsession: unconstrained `evidence_level` strings controlled
  ablation. An evidence-class typo could silently retain a candidate in the wrong scenario.

Revisions: validate bodies and endpoint-specific nested shapes before success; record
schema failures and preserve other successful requests; nonzero CLI exit for partial
searches or unresolved source checks; require an explicit unknown exposure field; constrain
evidence and approval vocabularies. Added malformed, empty, mixed-response and CLI tests.

Independent recheck: **all four resolved**, 60 tests pass. A mixed-response simulation
retained five valid searches while counting four complementary-service failures and
reporting `complete=False`. No directly introduced regression found in the bounded recheck.

### Spec

Two P2 findings, no material unrequested scope:

- The specified clinically relevant oncology controls were not assigned to tumour
  experiments. Generic reference controls and a literature benchmark were insufficient.
- The washout rule conflated reversible pharmacology with failed replication, potentially
  rejecting real on-treatment benefit. Loss after withdrawal is not automatically failure.

Revisions: require oncology-reviewer selection of an RMS comparator before data collection;
specify vehicle/reference/candidate arms and matched deficient-normal assessments, plus
single-agent controls for any later combination. Do not assume the subject's regimen or
make temsirolimus an automatic clinical standard. Separately assess independent replication,
reversible modulation, normal-cell recovery/injury/rebound, and regrowth after a declared
durable tumour-killing endpoint. Report and validation plan now agree.

Independent recheck: **both resolved**, no new material issue identified. The central
source interpretations withstood spot checks: mouse-allele mismatch, chloroquine-to-HCQ
extrapolation, deficient-normal hazards, negative trials and unconfirmed phase remain clear.

Summary: Standards initially 3 implementation issues plus 1 heuristic; Spec initially
2 design issues. Both review axes report no unresolved material findings after revision.
This is bounded review, not proof that every possible defect or scientific uncertainty is absent.

Outstanding limits: no direct-pair drug data, no verified exposure window, no active-tumour
model or treatment context, no experimental phase resolution, and no recorded/hosted pitch.
A research proposal can document these gaps; it must not imply that future validation
has happened. Feat-009 remains in progress until the complete deliverable set is ready.
