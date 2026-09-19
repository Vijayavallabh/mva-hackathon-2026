# Track 2 v5: validation plan and decision rules

2026-09-19 · Proposed research; no experiments have been performed. This plan authorizes
no sample acquisition, laboratory order, patient dosing or family contact. An authorized
laboratory would need qualified models, specialist input and its own approvals.
Trans phase remains unconfirmed. All clinical exposure margins remain unknown.

Everolimus is the single conditional hypothesis for constitutional function. HCQ remains
reserve; pralatrexate is an optional tumour-only direction for fusion-positive RMS.
The [v5 report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v5.md) and unchanged
[claim/decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v4.json) set the evidence boundaries.

## 1. Fix the questions and experimental units

The constitutional question is whether an intervention improves a prespecified functional
deficit in a qualified BUB1B-deficient model with the proposed target phenotype, without
reducing useful division, survival or lineage function. The tumour question is whether
a relevant RMS model shows reproducible benefit relative to a justified comparator while
sparing deficient non-cancer cells at matched, justified exposure.

Keep the branches separate. A composite ranking must not hide normal-tissue injury behind
tumour killing. No study in this proposal measures clinical benefit in the child.

Assign treatment to wells or cultures. Cells, divisions and daughter cells are nested
observations, with clones and independently started culture days as additional levels.
These counts are not interchangeable. Separate edited clones do not create independent
human donors. Report the sample size and losses at every level.

## 2. Qualify models before screening

Compare parental wild type, mock-edited controls, heterozygous stop alone, heterozygous
missense alone, the pair engineered in trans, the pair engineered in cis, and a precisely
corrected derivative. Confirm engineered edits, phase, expression, background karyotype
and copy number, and relevant off-target concerns. Failure to recover clones is a
selection or feasibility outcome, not proof of a particular patient mechanism.

A feasibility pilot could start with at least three independent clones per viable genotype
and three independently initiated culture days, with treatments on each day. These are
proposed resource assumptions, not a power calculation. An authorized lab may revise
them with justification before work. A separate confirmatory experiment requires pilot
variance, within-clone correlation, a meaningful effect target and a new fixed design.

First qualify one tractable non-transformed human-cell background. Add renal/muscle
lineages and a second background only after establishing assay feasibility. Match controls
for lineage differentiation, baseline proliferation and editing history. A renal assay
does not measure patient eGFR; a muscle assay does not establish whole-body developmental
rescue. The germline pair and phenotype do not identify a tumour subtype.

## 3. Separate molecular mechanism from functional rescue

Use orthogonal methods to assess endogenous transcript abundance, allele-specific RNA
where feasible, full-length and truncated protein, turnover and localization. A stop can
cause decay, truncation or other context-dependent outcomes; none has been measured here.
Normal missense protein abundance does not establish normal function.

Measure attachment and checkpoint response, recovery, ordinary live segregation, error
types, mitotic timing and daughter-cell fate. Fixed-cell alignment, protein abundance and
a metaphase karyotype cannot establish a prior slippage trajectory. A qualified FISH or
karyotype endpoint can support the live assay, but cannot replace it.

Engineered PP2A-B56 kinetochore recruitment is an optional mechanistic control, not an
approved drug. Xu's published MVA-cell result measured alignment under MG132 arrest;
the Aurora-B-inhibitor experiment used engineered HeLa perturbations. They do not jointly
establish chemical rescue in MVA cells. Alignment improvement qualifies that endpoint
alone. A full segregation-rescue claim also requires accurate completed divisions and
viable daughters. Global PP2A activation and generic kinase activity are insufficient
substitutes for localized BUBR1 scaffold and checkpoint function.
[Xu](https://doi.org/10.1242/bio.20134051)

## 4. Qualify target phenotype and exposure separately

For everolimus, prespecify nutrient, density, cell-cycle, starvation/refeeding and timing
conditions. Quantify total and activated pathway readouts. Phospho-S6 and phospho-4EBP1
are proposed assays; the motivating mouse Figure 5 measured phospho-p70 S6 kinase and
phospho-4EBP1. Require reproducible excess in the relevant model, an interpretable comparison
with correction and adequate assay dynamic range. A secondary abnormality could still
be modifiable; lack of genotype exclusivity or early temporal onset is not a universal
reason to reject it. Absence of the proposed excess stops this rationale. Do not switch
targets after seeing results; exploratory alternatives need separate preregistration.
[Sieben](https://doi.org/10.1172/JCI126863)

Prepare an exposure memorandum before a translational screen. Record the compound,
parent/salt, active metabolites, formulation, matrix, free fraction, serum composition,
pH, stability, sampling times, depletion and carryover. Compare concentration-time profiles
instead of isolated peaks. Measure free assay exposure or give defensible bounds. Whole
blood cannot substitute for plasma, a total peak for a free trough, or nominal medium
concentration for tissue exposure. Temsirolimus itself is active and also produces active
sirolimus; describing it as an inactive prodrug loses necessary analyte information.
[TORISEL label](https://labeling.pfizer.com/showlabeling.aspx?id=490)

Without justified exposure, an experiment may answer a mechanistic question but cannot
support translational advancement. A calculated nominal-culture/free-plasma ratio is not
a therapeutic margin. Unknown tissue accumulation cannot justify a favourable assumption.
No drug concentration or dose for the child is specified.

## 5. Enroll before exposure and retain every cell fate

Fix enrollment, observation horizon, imaging interval, handling of tracking loss, mitotic
entry definitions and event adjudication before outcomes are available. Treat baseline
cell-cycle state as a covariate or stratum, not a reason to select treatment survivors.

| Outcome record | Denominator and interpretation |
|---|---|
| First accurate completed division | All baseline-enrolled cells; daughter survival is a separate follow-up outcome |
| First error-containing division | All baseline-enrolled cells, plus error per completed division as a distinct measure |
| Death before or during division | Retained outcome, not excluded missing data |
| Slippage without division | Distinct from accurate division, mitotic death and persistent arrest |
| No division/persistent arrest at the fixed horizon | Retained competing outcome; subdivide mitotic/interphase state when observable |
| Tracking loss | Censored/missing with reason and treatment-specific rate; never automatically death |
| Daughter/post-slippage survival, later errors and regrowth | Follow-up conditional on the explicitly named earlier state; do not replace the enrollment denominator |

Use mutually exclusive first-event categories, followed by a separate longitudinal table
for later events. Repeated divisions are not new independent biological replicates.
Publish absolute counts and denominators. A lower error fraction among completed divisions
may coexist with fewer useful divisions, death or slippage, so cannot establish benefit
alone. The A549 rapamycin study's death-versus-slippage percentage cannot be used as an
MVA rate or a proportion of all enrolled cells.
[Yamada](https://doi.org/10.1016/j.isci.2021.103675)

## 6. Endpoints and advancement decisions

For a qualified division-defect model, a candidate primary endpoint is the change in
the fraction of baseline-enrolled cells producing an accurately divided, viable daughter
pair within a fixed observation horizon. Prespecify the error definition and
daughter-survival horizon. Report error per completed division, mitotic entry, division
count and every competing fate alongside this endpoint. If it does not capture the
model's deficit, redesign before screening. Cell-cycle effects and tracking uncertainty
need sensitivity analyses. This endpoint is not a clinical surrogate. Derive the
composite from first-event and daughter-follow-up records, retaining later daughter
deaths and missing tracks.

For an mTOR-associated lineage-function deficit without a demonstrable baseline division
deficit, prespecify the relevant lineage-function endpoint before screening. Improvement
with unchanged segregation is downstream functional mitigation, not chromosome repair.
Division accuracy and capacity, with all fate outcomes, remain mandatory safety measures.
Choose the qualified-model primary endpoint before drug screening. Do not switch between
these alternatives to salvage a negative treatment result.

Every constitutional test needs a prespecified meaningful functional improvement and
acceptable bounds on deficient-normal injury, division capacity, differentiation and
lineage function. Define numerical improvement and injury margins during assay
qualification, before confirmatory collection. Missing limits and nonsignificant toxicity
tests do not establish safety. Numerical thresholds, variance, power and margins are
currently unset.

The tumour primary endpoint should be a predeclared direct viable-burden or clonogenic
outcome relative to the selected RMS comparator, paired with deficient-normal injury under
matched schedule and exposure. Distinguish cytostasis, killing and durable post-withdrawal
suppression. Normalize original-population survival separately from assays that reseed
equal numbers of viable survivors; both are useful but answer different questions.

| Result | Decision |
|---|---|
| No qualified defect or target phenotype | Stop the declared hypothesis; investigate model adequacy separately |
| Target engagement without functional gain | Do not claim functional rescue or substitute biomarker success |
| Apparent gain explained only by arrest, death or slippage | Reject the rescue interpretation |
| Functional gain with unacceptable deficient-normal injury | Do not advance, even with tumour activity |
| Effect above justified exposure or exposure unresolved | Retain as a mechanistic result; no translational advancement |
| No replication or strong clone/batch dependence | Resolve confounding before any pooled success claim |
| Repeatable on-treatment benefit that reverses harmlessly on withdrawal | Record exposure dependence; this is not an automatic failure |
| Persistent injury or harmful rebound after washout | Stop for safety pending credible resolution |
| Initial tumour regression followed by regrowth | Reject durable eradication; retain the bounded on-treatment effect |
| Functional gain and safety bounds pass, with matched exposure and replication | Further preclinical and specialist review only; no patient dosing |

## 7. Tumour and reserve branches

Reopening HCQ requires compound-specific dynamic flux measurements, pH and reporter
interference controls, orthogonal turnover/lysosomal measures and deficient-normal
comparisons. Static LC3 or vesicle accumulation cannot establish flux direction or causal
autophagy-dependent death. Findings from other compounds or cancers cannot supply that
evidence.

Reopening pralatrexate requires a verified fusion-positive RMS experimental model, without
assuming the subject's subtype. Specify an oncology-selected reference treatment and
compatible schedule before testing. Include vehicle, reference and candidate alone before
any combination. Compare the same justified exposures in deficient-normal models; add
marrow-relevant safety if qualified. Thymidine rescue cannot distinguish a unique direct
TYMS target from upstream folate-pathway effects. Track schedule-dependent injury and
regrowth after withdrawal. No dose or supplementation plan is implied.
[Pralatrexate study](https://doi.org/10.1038/s41467-026-73749-y)

Any combination requires each monotherapy, a predeclared interaction reference model,
matched normal testing and an explicit indication/context. The child's regimen is unknown.
Do not assemble azole/rapalog/statin combinations from separate positive papers. Official
interaction categories include contraindications, not only dose adjustments. Every
oncology comparison requires an appropriately selected comparator.

## 8. Optional mechanistic assays

Readthrough assays must separately establish endogenous RNA availability, actual stop
traversal, full-length protein and checkpoint/segregation function. A spanning peptide
alone does not prove an intact protein. Barcode abundance requires translation-coupled
sorting or selection. A generic library-positive/endogenous-negative result does not
identify the failed step. Normal-stop readthrough toxicity needs its own measurement;
the amino-acid spectrum at premature stops cannot establish it.

Senescence/proteostasis assays must report absolute viable numbers, cell-type composition,
death, regeneration and chromosome outcomes. Lower p21 is not a universal benefit:
published muscle/fat protection differs from the lens effects. Ercc1 drug senolysis and
genetic population deletion do not establish BUBR1 drug rescue.

PP2A chemistry requires compound- and isoform/localization-specific engagement checks,
with assessment of microtubule and ER/Golgi alternatives. Binding or stabilizing PR65
with a different compound does not settle DT-061 cellular specificity. This plan does
not adopt the model's unsupported ordinary-isotope cryo-EM contrast suggestion.

The [constitutional adjudication](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-constitutional-review.md) records primary
support and reading limits. These are proposals for future assays, not experimental results.

## 9. Analysis, missingness and reproducibility

Randomize treatment and processing order within clone/day/plate blocks, balance plate
positions and use solvent/handling controls. Blind scoring and independently review
ambiguous events. Retain prespecified exclusions, code versions and deviations.

Pilot a clustered binomial or multinomial/time-to-event analysis suited to the chosen
estimand (the quantity to estimate) and competing fates. Include clone/day/plate dependence. If few clusters
undermine model estimation, use transparent well/clone summaries and cluster-level
sensitivity analyses. Do not assume tracking loss is unrelated to outcome: compare rates,
investigate causes and report plausible bounds for missing outcomes. Retain death as an
outcome.

Report effect sizes and intervals, not p-values alone. After pilot qualification and
before separate confirmatory data collection, fix the confirmatory hypotheses,
concentrations/times, minimum meaningful effect, injury bounds, family of multiple
comparisons and analysis code. Simulation using pilot variance and intracluster
correlation (ICC) can size the confirmatory design; no current data justify a numerical
power claim. An endpoint selected using the pilot cannot count as preregistered
confirmation on that same pilot. Do not use outcome-driven optional stopping to claim
statistical success; the prespecified safety stops still apply.

Publish negative and positive results subject to governance and the manuscript embargo.
Sharing a plan does not authorize sharing protected subject data. Any future laboratory's
raw assay data would have their own governance requirements. No laboratory data exist here.

## 10. Required laboratory records

An authorized laboratory would need qualified-model records, an exposure memorandum, a
fixed protocol and analysis plan, randomized allocation, blinded fate/function data,
missingness and deviation logs, replication results, and a signed-off advancement decision.
None has been produced. Cost, duration and scale require a laboratory quote. This proposal
specifies those dependencies so that any later experimental decision can be checked.
