# Track 2 proposed validation plan

2026-09-08 · **Not performed; no patient treatment, sample acquisition or laboratory
order is authorized by this document.** An authorized laboratory would need to qualify
the models and protocol. Raw subject material/data remains local under the access terms.
Trans phase remains unconfirmed; engineered phase is not patient phase.

The [final scientific/exposure review](track2-final-review.md) retains everolimus as
one conditional, phenotype-first priority; HCQ is reserve and its assays below describe
requirements for reopening, not a currently selected second lead. No clinical margin is
established. The [public exposure ledger](track2-exposure.json) is reproducible with
`uv run python scripts/track2_exposure.py`; conversions are not dose recommendations.

## Gate 0: establish the model before choosing a drug

Question: does the selected pair impair BUBR1 availability, checkpoint control or
chromosome attachment in a way that creates a rescuable defect or selective tumour
vulnerability? A reporter signal alone cannot answer this.

Start with an appropriate nontransformed human-cell background, then add tissue-relevant
models only when justified. Candidate contrasts are wild-type, heterozygous stop alone,
heterozygous missense alone, the pair engineered in trans, the pair engineered in cis,
and a precisely corrected derivative. Use independent edited clones and mock-edited
controls. Verify edits/engineered phase, off-target concerns, copy number and background
karyotype locally under the laboratory's own approvals. Severe genotype effects or failure
to recover clones are selection phenomena requiring investigation, not proof of a specific
clinical effect. Overexpression is a mechanistic control, not an endogenous-dose substitute.

For a pilot, **propose**, rather than claim adequate power from, at least three independent
clones per viable genotype and three independently started culture days, with treatments
distributed across each day. These numbers are a feasibility starting point. With one
genetic background, inference is limited to that background; repeated days do not create
independent donors. A confirmatory study needs variance/ICC estimates, a justified minimum
effect and formal power planning before collection. Do not count cells as independent n.

## Gate 1: distinguish loss mechanisms

Measure endogenous transcript abundance, allele-specific transcript contribution where
feasible, full-length/truncated protein and protein stability. Use orthogonal RNA and
protein methods and appropriate standards. A premature stop might cause RNA decay or a
truncated product; neither outcome is established here. Normal missense protein abundance
does not prove normal function. A fall in total protein might reflect cell-cycle changes.

Assess kinetochore localization, checkpoint response and recovery after a controlled
attachment perturbation, plus live segregation outcomes during ordinary division. Measure
mitotic duration distributions, lagging chromosomes, bridges and micronuclei; distinguish
checkpoint activation from timely silencing. Include blinded image annotation and an
independent endpoint such as karyotype/FISH on a qualified subset. Existing genome-wide
read-depth screens are not substitutes for these experiments.

Primary mechanism endpoint: fraction of evaluable divisions with a prespecified segregation
error definition, estimated at the well/clone level. Supporting endpoints: protein level,
localization and checkpoint dynamics. Also record total divisions, viability and cell-cycle
distribution. Fewer abnormal divisions because cells never divide is not functional rescue.

## Gate 2: qualify the proposed target phenotype

For the everolimus hypothesis, assay phospho-S6 and phospho-4EBP1 under standardized basal,
starvation and refeeding conditions, matched for density, nutrients and cell cycle. These
are proposed pathway measures, not WGS-derived observations. A reproducible genotype-linked
increase with correction-responsive behaviour is needed before claiming mTORC1 excess.

For the hydroxychloroquine hypothesis, use **dynamic autophagic flux**, not LC3 abundance
alone. Combine an appropriately validated flux reporter with turnover assays and orthogonal
lysosomal-function assessment. Accumulating vesicles can reflect increased production or
blocked clearance; both can occur in drug combinations. Distinguish cytostasis, metabolic
assay interference, apoptosis and other cell death.

Control for pH-dependent changes in fluorescent reporters during lysosomal perturbation;
include independent protein-turnover/degradation and death measurements. A PBMC vesicle
association or a static LC3/p62 image cannot establish selective tumour autophagy blockade.

Absent pathway/flux dependence → stop that mechanistic branch. Do not search many assays
and relabel the first positive result as the original hypothesis. Exploratory results must
be identified and independently retested.

## Gate 3: exposure-bounded single-agent screen

No concentration series for the child is proposed. A pharmacologist must define an
**in-vitro** exposure envelope from public human PK, formulation, metabolites, tissue
penetration and free fraction, with assay-medium binding measured or appropriately bounded.
Specify duration, replenishment and washout before starting. Whole-blood troughs, total
plasma peaks and nominal cell-culture concentration must not be directly substituted.
For lysosomotropic compounds, intracellular accumulation adds uncertainty; an unmeasured
tumour concentration cannot justify escalating above tolerated exposure.

Record analyte/active-metabolite identity, salt versus parent mass, sample matrix, free
fraction, serum composition, pH, nutrient/oxygen state, actual concentration over time and
drug depletion/carryover. Match the time-dependent exposure, not only a published peak.
Do not silently harmonize contradictory blood/plasma descriptions in a paper. Missing
information means a failed advancement gate, not permission to assume a favourable ratio.

Randomize vehicle and a log-spaced concentration series within clone/day blocks, preserving
balanced edge/interior positions. Include common reference controls on each plate and
randomize processing order. Match solvent and handling. Use separate blinded treatment
codes for image scoring. Record passage, batch, reagent lot, baseline growth and exclusions.

Constitutional objective: reduce segregation error **per completed division**, while
preserving division capacity, viability and relevant tissue function. The required
improvement and acceptable injury margin must be set after assay qualification, before
confirmatory data—not chosen after seeing drug results.

Tumour objective: reproducible cell killing/clonogenic loss preferential to matched
non-cancer deficient models within the same justified exposure envelope. Use genuine
RMS models with documented molecular background; represent unknown tumour subtype as
uncertainty, not an inferred FOXO1 status. Tumour and non-cancer models differ in lineage,
growth and transformation, so include genotype-matched comparisons within each background
and growth-rate-aware analysis. If no relevant tumour model is available, do not report a
tumour therapeutic window.

**Mandatory oncology-comparator gate before tumour screening:** an oncology reviewer must
select and justify an RMS reference agent or clinically relevant regimen for the model's
documented subtype and treatment setting, with an assay-compatible exposure schedule.
If that context or comparator cannot be justified, no comparative therapeutic claim is
allowed and the tumour arm remains exploratory. The protocol must name the comparator
before data collection; do not infer the child's current regimen.

| Tumour experiment arm | Required matched non-cancer comparison | Purpose |
|---|---|---|
| Vehicle | Same solvent/handling in deficient and corrected backgrounds | Baseline effect and assay performance |
| Selected RMS reference treatment | Same justified exposure/schedule in deficient non-cancer models | Clinical-context benchmark for benefit and injury |
| Candidate alone | Same justified exposure/schedule in deficient non-cancer models | Incremental tumour-versus-normal selectivity |
| Candidate plus reference, only after single-agent gates | Reference alone, candidate alone and combination in matched normal models | Test added benefit and added harm, not just more killing |

Temsirolimus may supply a mechanistic class benchmark, but is not automatically the
appropriate RMS standard-of-care control. In-vitro comparisons cannot reproduce all
components of a clinical regimen, particularly host metabolism, surgery or radiotherapy;
record which clinical comparison is and is not represented.

Renal- and muscle-relevant non-cancer models help investigate context-specific harm, but
are not validated surrogates for all organ toxicity. Pair them with appropriate viability,
recovery and differentiation/function endpoints. A renal cell assay does not establish
the patient's eGFR or reverse nephrocalcinosis.

## Gate 4: reproduce benefit, challenge alternatives

Confirm dose-response and target engagement in an independent experimental run. Include
genetic correction, an orthogonal target perturbation where interpretable, washout/recovery,
and a second independent background when feasible. Stop if apparent improvement results
from selecting only less-abnormal surviving cells, a slowed cell cycle, altered imaging
detection or a changed baseline karyotype. Report failures to replicate.

Interpret washout according to the endpoint. Reversible on-treatment functional benefit
does not have to persist after withdrawal to qualify as a reproducible pharmacological
effect; record its exposure dependence and any rebound. Failure to recover normal-cell
function, persistent injury, or inability to reproduce the on-treatment effect is a
different concern. For a declared tumour-killing/clonogenic endpoint, quantify regrowth
after withdrawal: cytostasis followed by regrowth cannot be relabelled durable killing.

Only after single-agent results may a combination be explored. mTOR inhibition and
lysosomal blockade could interact in either direction. A factorial response surface must
contain each monotherapy, vehicle, appropriate exposure limits and normal-cell testing.
Predeclare the interaction model and distinguish model-relative synergy from clinical
benefit. Do not call a combination beneficial because it kills more cells indiscriminately.

## Statistical plan

- Experimental unit: independently treated well/culture; measured cells are nested in
  wells, wells in clone/day/plate structure. Clones estimate editing/background variation,
  not patient population variation. Report all levels separately.
- Analyze binary segregation outcomes with a model respecting clustering, e.g. a suitable
  binomial/beta-binomial mixed model after assumptions are checked. Report effect sizes and
  intervals. Few clones limit random-effect precision; a clone-level sensitivity analysis
  and transparent raw unit summaries are needed.
- Predefine a primary endpoint per branch. Label pathway and image features as supporting
  or exploratory; adjust for multiple confirmatory candidate/endpoint contrasts using a
  declared family, with no cherry-picked concentration or time point.
- Record failed wells, unreadable images, toxicity-related attrition and missingness before
  unblinding. Death is an outcome, not a missing value to silently exclude.
- Plan confirmatory sample size by simulation using pilot variance and clustering, target
  effect, error rate and power. No current dataset supports a numerical power claim.
- For an eventual selectivity ratio, use matched effect definitions, duration and exposure
  units, with uncertainty. Censored IC50 values are bounds, not exact estimates or infinity.
  An unmeasured normal-cell IC50 does not establish safety.

## Go / no-go ledger

| Observation | Interpretation and action |
|---|---|
| No genotype-linked pathway abnormality | Stop downstream-rescue claim; do not substitute a pathway name for evidence |
| More protein but persistent segregation error | Abundance is not function; stop protein-rescue claim |
| Fewer micronuclei with severe cytostasis/death | Possible denominator/selection artifact; not rescue |
| Tumour and deficient normal cells equally sensitive | No therapeutic window demonstrated; stop tumour-selective claim |
| Effect only above justified exposure | Translational no-go unless new credible PK evidence changes the envelope |
| On-treatment benefit fails independent replication | Do not advance; investigate reproducibility and assay confounding |
| Functional modulation reverses after washout | Record exposure dependence; not an automatic no-go or proof of durable correction |
| Persistent normal-cell injury or damaging rebound after washout | Safety no-go pending a credible mechanistic resolution |
| Claimed durable tumour killing becomes regrowth after withdrawal | Reject the durable-killing claim; distinguish cytostasis from cytotoxicity |
| Functional benefit, target engagement and normal-cell preservation replicate | Advance to further preclinical/specialist review, **not directly to patient dosing** |

## Deliverable and feasibility boundary

An authorized follow-up laboratory should produce an auditable protocol, randomized
layout, raw assay data under appropriate governance, blinded results, exposure memorandum
and go/no-go decision. We have none of these results yet. Code/ledger reuse is inexpensive;
model creation, assay qualification and specialist review require real resources and
permissions. No procurement, cell-line order or clinical action was taken.
