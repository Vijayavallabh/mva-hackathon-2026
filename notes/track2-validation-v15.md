# Track 2 v15: validation plan and decision rules

2026-09-24 · Proposed research; no experiments have been performed. This plan authorizes
no sample acquisition, laboratory order, patient dosing or family contact. An authorized
laboratory would need qualified models, specialist input and its own approvals.
Trans phase remains unconfirmed. All clinical exposure margins remain unknown.

No drug currently earns a rescue priority. Everolimus is an optional mechanistic
probe after model qualification; it is not a preferred rescue candidate. HCQ remains
reserve; pralatrexate is an optional tumour-only direction for fusion-positive RMS.
The [v15 report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v15.md) and revised
[claim/decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json) set the evidence boundaries.

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
phospho-4EBP1. For branch A, require reproducible excess in the relevant model, an interpretable comparison
with correction and adequate assay dynamic range. A secondary abnormality could still
be modifiable; lack of genotype exclusivity or early temporal onset is not a universal
reason to reject it. Absence of the proposed excess stops branch A. Branch B below
requires its own prospective qualification; failure in A cannot be retrospectively
relabeled a success in B. Do not switch hypotheses after seeing results.
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

### 4a. Test both harmful-driver and adaptive-response explanations

Excess mTORC1 can be a correlate or a compensatory response. Define before perturbation
what result would support benefit, harm or indeterminate mechanism. Titrated RPTOR/pathway
perturbation, with appropriate non-targeting and restoration controls where feasible,
provides an orthogonal comparison to the drug. A second rapalog alone shares important
pharmacology and is not independent proof of target mediation. Genetic intervention
has its own dosage, timing and selection effects; a knockout is not exposure-equivalent
to everolimus. Discordance limits mechanism attribution, not necessarily a verified
drug-specific phenotype. Do not demand that the pathway be the earliest disease cause.

Goutas Figure 6 reports reduced BUBR1 with everolimus in late-passage stromal cells;
this introduces an explicit harm hypothesis. Measure endogenous RNA, BUBR1 abundance,
turnover and localization alongside dynamic autophagic flux, cell-cycle state and
absolute viable-cell counts before and after drug exposure. Match passage and cell
state, retain early/late-state comparisons when model-relevant, and use orthogonal
loading/per-cell normalization. A total-lysate protein decrease may reflect fewer
cycling cells, altered synthesis or selection, not simply direct degradation.
Lysosomal-inhibitor accumulation is not automatically beneficial flux or drug rescue.
Mechanistic rescue controls must themselves pass viability/checkpoint controls.
[Goutas](https://doi.org/10.1016/j.redox.2023.102701)

Predefine a material BUBR1-loss trigger during assay qualification. Crossing it pauses
advancement for blinded mechanistic review, including completed division and lineage
function; it does not alone establish patient harm. Worsened fidelity, depletion of
useful cells or failed injury bounds stops advancement. Protein preservation alone is
insufficient. HCQ's 100-micromolar/2-hour protein experiment supplies neither a safe
clinical exposure nor a reason to combine inhibitors to cancel each other's effects.

### 4b. Match the assay to the biological compartment

Proliferating progenitors support live division/fate measurements. Mature postmitotic
myotubes should instead be assessed for a qualified muscle-function endpoint (for
example evoked contraction), survival and differentiation history; requiring them to
divide would be a construct error. Evaluate precursor division and mature-lineage
function in linked but distinct experiments. Predefine total functional output per
starting culture as well as per-surviving-cell output to expose loss of useful cells.
Renal differentiation, uptake/barrier readouts or muscle contraction are assay choices
to qualify, not established deficits or patient-level surrogates.

A developmental endpoint and an ageing/senescence endpoint are not interchangeable.
Qualify model relevance before using artificial oxidative insult or high passage to
create a drug-responsive phenotype. A negative phenotype result can invalidate the
model or the hypothesis; it does not prove absence of patient disease.

### 4c. Qualify a separate flux/function hypothesis without moving the criteria

Branch B is a new hypothesis motivated by the hypercapnia literature, where
rapamycin-associated regenerative improvement did not require elevated baseline
measured mTOR readouts. It requires a reproducible, relevant dynamic-autophagy and
regenerative-function deficit, adequate assay range and a plausible mechanism in
an endogenous model. Neither deficit has been established in the selected pair.
A pathway phosphoprotein snapshot cannot diagnose the full flux mechanism.
[Balnis](https://doi.org/10.1172/jci.insight.182842)

Specify branch, eligibility, primary function, controls, thresholds and analysis
before treatment results. Use orthogonal pathway/flux perturbation with viability
and restoration controls where feasible. These controls test mediation; an ATG
knockdown that itself injures cells is not a clean therapeutic comparator. Lack of
benefit, loss of useful cells, worse fidelity or unacceptable delayed injury stops
advancement under the prespecified criteria. A newly observed phenotype can motivate
an explicitly exploratory, independently confirmed study, not rescue a failed test.
Do not manufacture a flux phenotype with senescence or hypercapnia solely to match
another disease model. The now-reviewed selected supplemental Methods report conflicting ex vivo units
(10 mM on PDF page 12; 10 μM on page 15). Quarantine that numerical inference until
resolved; do not silently choose the more plausible value or import it into a dosing
design. The qualitative biological observation remains indirect support only.

### 4d. Resolve dose, regenerative stage, delayed injury and exposure

Prespecify a graded concentration-time design after assay qualification; maximal
phosphoprotein suppression is not the optimization target. Analyze precursor
activation, expansion, differentiation/fusion and mature function as separate stages.
Include recovery after washout where interpretable, residual drug/carryover assessment,
and later useful output per originally enrolled culture. Partial RAD001 inhibition
and continuous/strong suppression cannot be assumed equivalent. Muscle mass, static
LC3, or an early metabolic-viability signal cannot substitute for force, dynamic flux
or sustained useful cell output. No numerical dose or injury threshold is invented
here. [Joseph](https://doi.org/10.1128/MCB.00141-19),
[Ge](https://doi.org/10.1152/ajpcell.00248.2009)

If HCQ is reopened, include delayed lysosomal/myofiber injury and post-exposure recovery
at the same justified exposure used for the proposed benefit. The selected adult
myopathy series motivates the hazard endpoint but provides no pediatric incidence.
Before expanding a scoped muscle result into a developmental-rescue claim, assess
cardiac/developmental model coverage; cardiac-specific knockout findings do not
identify an abnormality in the child or require every initial exploratory assay to
become a whole-organism experiment.
[Naddaf](https://doi.org/10.3389/fneur.2020.616075),
[Pun](https://doi.org/10.1161/JAHA.124.038286)

Add hematocrit, red-cell partitioning and the assumptions behind plasma estimates
to the exposure memorandum. Prefer measured relevant free exposures or defensible
bounds. A population PK simulation is not measurement of this subject's unbound
plasma or tissue, and the rat study's asserted human dose equivalence cannot establish
a pediatric margin. [van Erp](https://doi.org/10.1007/s40262-016-0414-3)

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
None has been produced. Cost, duration and scale require a laboratory quote.
For feasibility accounting only, seven groups × three clones × three days × two
conditions already imply 126 culture allocations before concentrations, technical
replicates, validation controls or added lineages. This arithmetic is not a sample-size
recommendation, an available model collection, independent donors or a power estimate.
Stage the work: model/assay qualification, a blinded exploratory benefit/harm probe,
then an independently locked confirmatory design only if justified. This proposal
specifies those dependencies so that any later experimental decision can be checked.

## 11. V15: falsification required at every decision

Use the [19-claim register](track2-falsification-register-v15.json),
[source review](track2-falsification-review-v15.md) and offline
`scripts/track2_falsification_v15.py check` before promoting any interpretation.
The register is not a laboratory preregistration: it identifies missing experiments
and rules. Qualified numerical margins, confirmatory sample size and assay timing
remain unset. Do not fabricate them to obtain a passing decision.

1. **Model attribution:** distinguish endogenous RNA decay from residual protein.
   Ectopic truncation complementation bypasses transcript regulation; expression-match
   it if used as a control. Separate attachment, checkpoint activation/maintenance,
   silencing and viable accurate daughter production. Do not assign L737Ter the
   phenotype of published 731X. Keep endogenous correction, single and cis controls.
2. **Evidence independence:** retain every sequence window/control and both original
   and expanded-control results. The expanded comparison is post-hoc, with secondary
   labels and a single underlying study. Do not calibrate function from score sign,
   count seeds as samples, or replace direct assays with Evo/Atlas/structure consensus.
3. **Engagement and flux:** use time-matched total and activated pathway readouts and
   mechanistically relevant feedback checks. For fluorescent flux, qualify expression,
   acidity, compound optical interference and cell loss, with orthogonal cargo turnover.
   A pH-driven signal is not a degradation result; engagement is not useful function.
4. **Tumour selectivity:** record direct viable counts at baseline and multiple times,
   with death/fate and qualified lineage function in deficient-normal controls. Report
   conventional endpoint and growth-rate-aware results where untreated controls grow
   sufficiently; do not calculate unstable/undefined GR values in non-growing cultures.
   A low tumour IC50 against a slow normal line alone is not a selectivity window.
5. **Missingness:** retain the original enrollment denominator. For a binary success
   endpoint with N enrolled, S verified successes and L unresolved outcomes, [S/N,
   (S+L)/N] are worst-case identification bounds. Treated-minus-control bounds are
   [Tlow-Chigh, Thigh-Clow]. These do not include sampling uncertainty; cluster-aware
   intervals remain necessary. If plausible missingness erases a claim, hold it.
6. **Meaningful benefit and injury:** lock minimum benefit and maximum acceptable
   injury from assay performance/pilot evidence before independent confirmation. For
   endpoints defined so larger values mean more benefit/injury, respectively, require
   the benefit interval's lower bound above the benefit margin and the injury interval's
   upper bound below the injury margin. Fix interval coverage and multiplicity handling
   in advance. Reorient decreasing-is-better endpoints explicitly. An interval crossing
   a decision margin is indeterminate, not equivalence or proof of no harm.
7. **Replication and scope:** cells/technical wells do not replace independent culture
   days, clones and backgrounds. Report every unit and leave-one-clone/day sensitivity.
   Improvement in one context remains scoped to it. Later fates, clonal composition,
   recovery and mature function test selection and rebound; no short assay establishes
   developmental restoration or whole-organism tumour safety.
8. **Source and exposure integrity:** an inconsistent concentration, unverified identity,
   inaccessible methods or unbounded relevant exposure blocks the corresponding inference.
   Keep unreported quantities null. A mechanistic assay may proceed under its own
   authorized protocol without a clinical bridge; it cannot then be called translationally
   qualified. Do not infer a dose for the child.
9. **Symmetric alternatives:** require the same chain for HCQ, pralatrexate and every
   rejected direction. Reserve status is not endorsement. BindCraft2 remains deferred
   without a defined functional target and experimental route. No priority is inherited
   because a competing candidate failed.

The executable gate distinguishes **hold_unresolved**, **stop_tested_context** and
**eligible_for_preclinical_review**. A failed safety condition overrides favorable
function. Post-hoc success stays exploratory. All current biological requirements
are unknown; no experiment has been performed. Evidence records are human-adjudicated:
software validates consistency and evidence type, not the truth or completeness of
measurements. Even a fully populated passing record cannot recommend treatment.

Primary methods motivating these additions are linked in the v15 review: the 2012/2020
BUBR1 experiments, Hafner growth-rate analysis, the primary flux-reporter study, O'Reilly
feedback experiments, the Balnis supplement and compound-specific safety records.
Reopen this audit on new evidence, model, endpoint, adverse signal or source correction.
Do not preserve a favored mechanism by changing endpoints, controls or thresholds after
seeing confirmatory outcomes.
