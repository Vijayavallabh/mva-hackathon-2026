# Track 2 v4: staged validation and decision specification

2026-09-19 · Proposed research, **not performed**. No sample acquisition, laboratory
order, patient dosing or family contact is authorized. An appropriately authorized
laboratory would need qualified models, specialist input and its own approvals.
Trans phase remains unconfirmed. All clinical exposure margins remain unknown.

This consolidates the prior plans without changing them. Everolimus is the single
conditional constitutional hypothesis; HCQ is reserve; pralatrexate is an optional
fusion-positive RMS tumour-only horizon. The [v4 report](track2-report-v4.md) and
[claim/decision ledger](track2-evidence-v4.json) define the evidence boundaries.

## 1. Lock the question and the experimental units

Constitutional question: in a qualified BUB1B-deficient model with the proposed target
phenotype, does the intervention improve a prespecified functional deficit without
reducing useful division, survival or lineage function? Tumour question: does a relevant
RMS model show reproducible benefit relative to a justified comparator while deficient
non-cancer cells are spared at matched, justified exposure?

These are separate branches. No composite ranking may hide normal-tissue injury behind
tumour killing. No study here measures a clinical benefit in the child.

The treatment-assignment unit is the well/culture. Cells, divisions and daughter cells
are nested observations; clones and independently started culture days are additional
levels, not interchangeable replicate counts. Separate edited clones do not create
independent human donors. Report every level's n and losses.

## 2. Model qualification before screening

Proposed contrasts: parental wild type, mock-edited controls, heterozygous stop alone,
heterozygous missense alone, the pair engineered in trans, the pair engineered in cis,
and a precisely corrected derivative. Confirm engineered edits, phase, expression,
background karyotype/copy number and relevant off-target concerns. Failure to recover
clones is a selection/feasibility outcome, not proof of a particular patient mechanism.

A starting feasibility pilot could use at least three independent clones per viable
genotype and three independently initiated culture days with treatments on each day.
These are proposed resource assumptions, **not a power calculation**. An authorized lab
may revise them with justification before work. Subsequent confirmation requires pilot
variance, within-clone correlation, a meaningful effect target and a new frozen design.

Initially qualify one tractable non-transformed human-cell background. Add renal/muscle
lineages and a second background only after assay feasibility. Lineage differentiation,
baseline proliferation and editing history require matched controls. A renal assay does
not measure patient eGFR; a muscle assay does not establish whole-body developmental rescue.
No tumour subtype is inferred from the germline pair or phenotype.

## 3. Distinguish molecular mechanism from functional rescue

Assess endogenous transcript abundance, allele-specific RNA where feasible, full-length
and truncated protein, turnover and localization with orthogonal methods. A stop can
cause decay, truncation or other context-dependent outcomes; none is measured here.
Normal missense protein abundance does not establish normal function.

Measure attachment/checkpoint response and recovery, ordinary live segregation, error
types, mitotic timing and daughter-cell fate. Fixed-cell alignment, protein abundance
and a metaphase karyotype cannot establish a prior slippage trajectory. A qualified
FISH/karyotype endpoint can support, but not replace, the live assay.

Engineered PP2A-B56 kinetochore recruitment is an optional mechanistic control, not an
approved drug. Xu's published MVA-cell result was alignment under MG132 arrest; its
Aurora-B-inhibitor experiment used engineered HeLa perturbations. Do not merge them into
chemical MVA rescue. Alignment improvement qualifies only that endpoint; claiming full
segregation rescue additionally requires accurate completed divisions and viable daughters.
Neither global PP2A activation nor a generic kinase-activity assay is a
substitute for localized BUBR1 scaffold/checkpoint function.
[Xu](https://doi.org/10.1242/bio.20134051)

## 4. Qualify target phenotype and exposure independently

For everolimus, prespecify nutrient, density, cell-cycle, starvation/refeeding and timing
conditions; quantify total/activated pathway readouts. Phospho-S6 and phospho-4EBP1 are
proposed assays; the motivating mouse Figure 5 measured phospho-p70 S6 kinase and
phospho-4EBP1. Reproducible excess in the relevant model, interpretable comparison with
correction and adequate dynamic range are required. A secondary abnormality could still
be modifiable; lack of genotype exclusivity or early temporal onset is not a universal
veto. Absence of the proposed excess stops this particular rationale rather than inviting
post-hoc target switching. Exploratory alternatives require separate preregistration.
[Sieben](https://doi.org/10.1172/JCI126863)

An exposure memorandum must precede a translational screen. Record compound, parent/salt,
active metabolites, formulation, matrix, free fraction, serum composition, pH, stability,
sampling times, depletion and carryover. Compare concentration-time profiles rather than
one isolated peak. Measure free assay exposure or give defensible bounds; do not equate
whole blood with plasma, a total peak with a free trough, or nominal medium with tissue.
Temsirolimus itself is active and also produces active sirolimus; calling it simply an
inactive prodrug loses necessary analyte information.
[TORISEL label](https://labeling.pfizer.com/showlabeling.aspx?id=490)

If relevant exposure cannot be justified, an experiment may remain mechanistic but cannot
pass the translational gate. A calculated nominal-culture/free-plasma ratio is not a
therapeutic margin. Unknown tissue accumulation cannot justify a favourable assumption.
No drug concentration or dose for the child is specified.

## 5. Enroll before exposure; retain all cell fates

Freeze enrollment, observation horizon, imaging interval, track-loss handling, mitotic
entry definitions and event adjudication before outcomes are available. Baseline cell-cycle
state is a covariate/stratum, not a reason to select treatment survivors.

| Outcome record | Denominator and interpretation |
|---|---|
| First accurate completed division | All baseline-enrolled cells; daughter survival is a separate follow-up outcome |
| First error-containing division | All baseline-enrolled cells, plus error per completed division as a distinct measure |
| Death before or during division | Retained outcome, not excluded missing data |
| Slippage without division | Distinct from accurate division, mitotic death and persistent arrest |
| No division/persistent arrest at the fixed horizon | Retained competing outcome; subdivide mitotic/interphase state when observable |
| Tracking loss | Censored/missing with reason and treatment-specific rate; never automatically death |
| Daughter/post-slippage survival, later errors and regrowth | Follow-up conditional on the explicitly named earlier state; do not replace the enrollment denominator |

Use mutually exclusive first-event categories, then a separate longitudinal table for
later events. Repeated divisions do not become new independent biological replicates.
Publish both absolute counts and denominators. A lower error fraction among completed
divisions may coexist with fewer useful divisions, death or slippage; it cannot stand alone.
The A549 rapamycin study's death-versus-slippage percentage cannot be transplanted as an
MVA rate or as a proportion of all enrolled cells.
[Yamada](https://doi.org/10.1016/j.isci.2021.103675)

## 6. Proposed endpoints and advancement logic

**Candidate primary endpoint for a qualified division-defect model:** change in the fraction of baseline-enrolled
cells producing an accurately divided, viable daughter pair within the fixed observation
horizon. Prespecify an error definition and daughter-survival horizon. Report error per
completed division, mitotic entry, division count and every competing fate alongside it.
If the model's deficit is not captured by this endpoint, redesign before screening, not
after treatment results. Cell-cycle effects and tracking uncertainty require sensitivity
analyses; the endpoint is not a clinical surrogate. Derive this composite from first-event
and daughter-follow-up records without dropping later daughter deaths or missing tracks.

For an mTOR-associated lineage-function deficit without a demonstrable baseline division
deficit, prespecify the relevant lineage-function endpoint before screening. Improvement
with unchanged segregation is **downstream functional mitigation, not chromosome repair**.
Division accuracy/capacity and all fate outcomes remain mandatory safety guardrails.
Select the qualified-model primary endpoint before drug screening; do not switch between
these alternatives to salvage a negative treatment result.

**Mandatory paired safety/function gates:** a prespecified meaningful functional improvement
and acceptable bounds on deficient-normal injury, division capacity, differentiation and
lineage function. Define numerical improvement and injury margins during assay qualification,
before confirmatory collection. Do not label missing limits or a nonsignificant toxicity
test as safety. Current numerical thresholds, variance, power and margins are unset.

**Tumour primary endpoint:** predeclared direct viable-burden or clonogenic outcome relative
to the selected RMS comparator, paired with deficient-normal injury under matched schedule
and exposure. Distinguish cytostasis, killing and durable post-withdrawal suppression.
Normalize original-population survival separately from assays that reseed equal numbers
of viable survivors; both are useful but answer different questions.

| Gate result | Decision |
|---|---|
| No qualified defect/target phenotype | Stop that declared hypothesis; investigate model adequacy separately |
| Target engagement but no functional gain | No functional-rescue claim; do not substitute biomarker success |
| Apparent gain explained only by arrest, death or slippage | Reject rescue interpretation |
| Functional gain with unacceptable deficient-normal injury | Do not advance, even with tumour activity |
| Effect above justified exposure or exposure unresolved | No translational advancement; mechanistic result only |
| No replication or strong clone/batch dependence | Resolve confounding; no pooled success declaration |
| Repeatable on-treatment benefit that reverses harmlessly on withdrawal | Record exposure dependence; not an automatic failure |
| Persistent injury or harmful rebound after washout | Safety stop pending credible resolution |
| Initial tumour regression followed by regrowth | Reject durable-eradication claim; retain bounded on-treatment effect |
| Functional gain and safety bounds pass, with matched exposure and replication | Further preclinical/specialist review only—not patient dosing |

## 7. Tumour and reserve branches are not shortcuts

HCQ re-entry requires compound-specific dynamic flux, pH/reporter-interference controls,
orthogonal turnover/lysosomal measures and deficient-normal comparisons. Static LC3 or
vesicle accumulation cannot establish flux direction or causal autophagy-dependent death.
Other compounds and other cancers do not supply this evidence.

Pralatrexate re-entry requires a verified fusion-positive RMS experimental model, not an
assumed subject subtype. Specify the oncology-selected reference treatment and compatible
schedule before testing. Include vehicle, reference and candidate alone before any
combination. Compare the same justified exposures in deficient-normal models; add
marrow-relevant safety if qualified. Thymidine rescue cannot distinguish a unique direct
TYMS target from upstream folate-pathway effects. Track schedule-dependent injury and
regrowth after withdrawal. No dose or supplementation plan is implied.
[Pralatrexate study](https://doi.org/10.1038/s41467-026-73749-y)

Any combination needs each monotherapy, a predeclared interaction reference model, matched
normal testing and an explicit indication/context. The child's regimen is unknown.
Azole/rapalog/statin combinations must not be assembled from separate positive papers;
official interaction categories include contraindications, not only dose adjustments.
No oncology comparison is justified without an appropriately selected comparator.

## 8. Corrected optional mechanistic assays

- **Readthrough:** separately establish endogenous RNA availability, actual stop traversal,
  full-length protein and checkpoint/segregation function. A spanning peptide alone does
  not prove an intact protein. Barcode abundance needs translation-coupled sorting or
  selection. A generic library-positive/endogenous-negative result does not identify
  which step failed. Normal-stop readthrough toxicity is a separate measurement, not
  inferred from the amino-acid spectrum at premature stops.
- **Senescence/proteostasis:** report absolute viable numbers, cell-type composition,
  death, regeneration and chromosome outcomes. Lower p21 is not a universal benefit:
  published muscle/fat protection and lens effects differ. Do not translate Ercc1 drug
  senolysis or genetic population deletion into BUBR1 drug rescue.
- **PP2A chemistry:** verify compound and isoform/localization-specific engagement;
  assess microtubule and ER/Golgi alternatives. Different-compound PR65 binding/stability
  is not resolution of DT-061 cellular specificity. No ordinary-isotope cryo-EM contrast
  experiment is adopted from the model's unsupported suggestion.

Primary support and reading limits are in the
[constitutional adjudication](track2-glm-constitutional-review.md); these are future
assay-design inferences, not new experimental results.

## 9. Analysis, missingness and reproducibility

Randomize treatment and processing order within clone/day/plate blocks, balance plate
position and use solvent/handling controls. Blind scoring with independent review of
ambiguous events; retain prespecified exclusions, code versions and deviations.

Pilot a clustered binomial or multinomial/time-to-event analysis appropriate to the
chosen estimand and competing fates. Include clone/day/plate dependence; use transparent
well/clone summaries and cluster-level sensitivity analyses when few clusters undermine
model estimation. Track loss is not assumed noninformative: compare rates, investigate
causes and report plausible missing-outcome bounds. Death remains an outcome.

Report effect sizes and intervals, not p-values alone. Freeze confirmatory hypotheses,
concentrations/times, minimum meaningful effect, injury bounds, multiplicity family and
analysis code after pilot qualification but before separate confirmatory data. A simulation
using pilot variance/ICC can size the confirmatory design; no present data justify a
numerical power claim. A pilot-chosen endpoint cannot be called preregistered confirmation
on that same pilot. No outcome-driven optional stopping.

Publish negative and positive results subject to governance and the manuscript embargo.
Sharing a plan does not authorize sharing protected subject data. Raw assay data from any
future laboratory have their own governance requirements. No laboratory data exist here.

## 10. Minimum authorized follow-up deliverable

A laboratory would need: qualified-model records; exposure memorandum; frozen protocol
and analysis plan; randomized allocation; blinded fate/function data; missingness and
deviation logs; replication results; and a signed-off advancement decision. None has been
produced. Cost, duration and scale need a laboratory quote. The present deliverable is a
reproducible proposal that makes these dependencies visible.
