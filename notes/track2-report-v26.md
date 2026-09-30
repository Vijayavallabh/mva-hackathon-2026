# Testing everolimus for useful cell function in BUB1B-associated MVA

Track 2 research proposal · jvv7 · 1 October 2026 · v26

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

Everolimus is an approved mTORC1 inhibitor proposed as an optional probe of non-cancer
function in a qualified BUB1B-deficient model. Advancement requires useful function
without unacceptable injury to division, viability, chromosome fidelity or regeneration.
No rescue-priority drug is supported. Selected-pair efficacy, trans phase and clinical
exposure margins are unresolved; no wet-lab experiment has been performed.

Public CRISPR data strengthen HT29 as a place to develop a BUB1B assay, but all
31 BUB1B profiles use one guide. HT29 is a tumour line, and one of its two CRISPR
batches fails the declared quality filter. MCF7 has a favorable everolimus connection,
but its BUB1B query fails quality checks and disagrees with RNAi. These findings in
different cells cannot be combined into a joint rescue result.

The proposal starts with endogenous model and assay qualification, then a randomized
joint drug-plus-deficit experiment in a relevant non-cancer context. Useful function,
cell fate, injury and recovery decide advancement. No treatment or dose for the child
is proposed.

## 1. Mechanism and eligibility

The retained hypothesis is BUB1B p.Leu737Ter / p.Asn1002Lys. BUB1B encodes BUBR1,
which contributes to spindle-checkpoint and chromosome-attachment control. Biallelic
BUB1B disruption is an established MVA mechanism, but this pair's endogenous RNA/protein effects and
residual function are unknown. Engineered single-allele, cis and trans models test
alternatives; they cannot establish the subject's phase. Competition performance and
model predictions do not resolve these gaps. [Hanks](https://doi.org/10.1038/ng1449),
[Suijkerbuijk](https://doi.org/10.1158/0008-5472.CAN-09-4319).

A different BubR1-mutant mouse context showed increased mTOR-associated
phosphoproteins in muscle, without testing rapalog rescue. Excess signaling might
be adaptive. Everolimus inhibits mTORC1; it neither replaces BUBR1 nor establishes
chromosome repair. Specified TSC indications establish approval and known
pharmacology, not MVA efficacy or safety.
[Mouse study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781),
[label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2).

Qualify one of two branches before exposure:

- **A:** excess mTOR-associated activity with a functional deficit.
- **B:** impaired dynamic autophagic flux and regeneration, with separate mechanistic controls.

Neither is established for this pair. Do not switch branches after seeing results.
The hypercapnia study motivating B reports conflicting ex vivo units, 10 mM versus
10 micromolar, in related supplemental methods. Quarantine this 1,000-fold discrepancy;
neither value can set the experimental concentration.
[Balnis](https://doi.org/10.1172/jci.insight.182842),
[supplement](https://insight.jci.org/articles/view/182842/sd/pdf/render/1).

## 2. Functional evidence determines the next test

| Finding | Consequence for this proposal |
|---|---|
| Everolimus increased selected muscle-mass outcomes in aged rats; force benefit was not established. | Measure useful function directly. [Joseph](https://doi.org/10.1128/MCB.00141-19) |
| Everolimus reduced BUBR1 in late-passage human stromal cells; early-passage response differed. | Monitor BUBR1, chromosome fidelity and cell state. Protein loss alone does not prove harm. [Goutas](https://doi.org/10.1016/j.redox.2023.102701) |
| Rapamycin impaired injured-mouse muscle regeneration. | Measure regeneration and recovery; compounds, exposures and tissues are not interchangeable. [Ge](https://doi.org/10.1152/ajpcell.00248.2009) |
| RAPA-EX-01: 40 older adults, sirolimus plus exercise; primary difference −2.13 chair stands (95% CI −4.61 to 0.34; p=0.089). | No established functional benefit. Sensitivity analyses favored placebo; they do not replace the primary result. Indirect for everolimus/MVA. [Trial](https://doi.org/10.1002/jcsm.70274) |
| ARST1431: adding temsirolimus to VAC/VI did not establish event-free-survival benefit in 297 evaluable intermediate-risk RMS participants (HR 0.86; 95% CI 0.58-1.26; p=0.44). | Retain this randomized tumour result. It establishes neither non-cancer everolimus rescue nor exactly zero effect in every context. [Trial](https://doi.org/10.1016/S1470-2045(24)00255-9) |

The final PoWeR study retained exercise-associated grip-strength and myofiber gains
in adult female mice receiving rapamycin. Missing sedentary drug arms and differing
running volume limit interpretation. Together with young-rat force impairment, this
argues for context-specific function and recovery tests, not inevitable class-wide
benefit or harm. [PoWeR](https://doi.org/10.1111/acel.70183),
[rat study](https://doi.org/10.1371/journal.pone.0312859).

Uncontrolled pediatric TSC growth follow-up and a pediatric transplant-regimen safety
comparison argue against assuming inevitable developmental harm. They neither establish
MVA safety nor isolate everolimus's effect. Renal, infection, marrow/metabolic,
wound-healing and interaction risks remain. Additional clinical laboratory and
treatment-history records are unavailable, so individual suitability cannot be assessed.
[Label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[transplant trial](https://doi.org/10.1001/jama.2025.14338),
[organizer clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/14).

HCQ remains reserve. Chromatin-timing effects in tumour cells and nuclear extracts
undermine its use as a selective autophagy control; the small studies and high nominal
exposures do not establish harm in MVA. Require independent flux and chromosome-function
tests. [Primary study](https://doi.org/10.1080/15384101.2024.2402191). Pralatrexate is a tumour-only hypothesis for relevant
fusion-positive RMS models; temsirolimus is a clinical benchmark. Entinostat, vorinostat,
niclosamide and posaconazole remain deprioritized. PP2A tools, senolysis and readthrough
remain excluded. No combination is proposed; a competitor's failure confers no priority.
The [63-source, 11-decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json)
records each rationale, approval/indication and exposure limitation. The
[v21 amendment](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v21.json) retains all eleven dispositions.
NAD/SIRT2 remains a competing mechanism to qualify: genetic SIRT2 survival, NMN-associated
BUBR1 abundance and niacin muscle findings are different experiments and compounds.
They do not establish niacin rescue of this pair. Check residual useful protein,
checkpoint timing and deficient-normal function before promotion.
[SIRT2/NMN](https://doi.org/10.15252/embj.201386907),
[K250 counterpoint](https://doi.org/10.1016/j.bbrc.2014.09.128),
[niacin study](https://doi.org/10.1016/j.cmet.2020.04.008),
[methods correction](https://doi.org/10.1016/j.cmet.2020.05.020). The correction changes
COX/SDH incubation times; the authors state that findings are unchanged.

## 3. Public expression screening changes the next experiment

We reanalysed [GSE92742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92742)
and [GSE70138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70138): 312,438
compound-treatment profiles across 978 measured landmark genes. These are profiles,
not distinct drugs or independent experiments. Three completed waves used eight H100s
for 12,185,082 query-compound comparisons and 560,000 reagent-set resamples. This was
statistical reanalysis, not new neural-model inference; GPU activity was brief and
bursty. The two primary plans preceded expression inspection; the follow-up was post-hoc.

| Test | Result and limit |
|---|---|
| Qualify BUB1B knockdown signatures | 0/14 contexts pass the full primary filter. It requires at least six reagents, negative median target-transcript z-score, positive median pairwise/split agreement and an adjusted empirical tail ≤0.05. |
| Challenge that negative result | 0/42 post-hoc comparisons pass the full filter. HT29 retains favourable evidence: five verified provider-member reagents after shared-pattern removal, split agreement 0.321 and adjusted tail 0.042. It misses the six-reagent requirement. |
| Primary everolimus comparisons | 13/19 matched comparisons have positive raw correlation at 10 µM nominal culture exposure. The 19 comparisons reuse 14 drug profiles; query qualification remains unresolved. Positive correlation does not prove harm. |
| Second-release compound identity | 174/180 everolimus-labelled profiles have unresolved stereochemical metadata. All six reference-matching profiles at 0.1 µM nominal culture concentration fail the specified drug QC in this older release. Newer aggregation is assessed separately below. |

The operational filter is uncalibrated, with unknown sensitivity and specificity.
Its null does not match shRNA seed, potency or off-target effects; the six-reagent
minimum is not a biological boundary. Calibration requires independent known-positive
and negative perturbations, with preprocessing and comparison family locked before
validation. Reusing HT29 to tune and validate the rule would be circular. Missing its threshold does not disprove BUB1B biology. The
HT29 result warrants follow-up without replacing the primary result. Shared-pattern
projection can remove real biology. Chemical metadata disagreement does not prove
wrong material in the vial; it prevents pooling three identifiers into one dose curve.
The six exact-identity profiles each have one sample, missing replicate-correlation
metadata and low activity scores.

Drug-only and knockdown-only profiles do not measure drug response in deficient cells.
Expression reversal may oppose compensation, while useful function might improve
without reversal. These results establish neither benefit nor harm and do not promote
HCQ by elimination. [RNAi seed effects](https://doi.org/10.1371/journal.pbio.2003213),
[CMap reproducibility](https://doi.org/10.1038/s41598-021-97005-z),
[expression and phenotype](https://doi.org/10.1038/s41467-017-01383-w).

The next experiment must establish endogenous BUBR1/function and independent genetic
perturbation/correction, verify compound identity, then measure drug-plus-deficit
function directly. Independently reproducible on-target signatures and replicated
functional benefit could overturn the present hold. Complete scores, nulls, exclusions,
chemical identifiers and favourable exceptions remain in the
[research record](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-transcriptome-v19.md)
and [reproduction guide](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-transcriptome-reproduction-v19.md).
A separate SciPy recalculation of 139 raw correlations agrees within 4.75×10⁻⁸;
this checks arithmetic, not biology. No independent scientist reviewed this analysis.
Public data are attributed to Broad/LINCS and the originating investigators; projections
and analyses are our modifications under the
[redistribution policy](https://clue.io/connectopedia/data_redistribution).

### Seed and batch alternatives: what the follow-up changes

The [GSE106127 reanalysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-v23.md)
uses 119,013 public signatures, including 116,782 RNAi profiles and 55 BUB1B profiles
across nine cell lines. All RNAi signature IDs and underlying replicate-ID sets overlap
v19: this is not independent biological replication. Raw and deposited PRIME matrices
are separate representations; PRIME is the authors' processing, not our earlier
rank-space projection. The plan was fixed after metadata/prior results but before
opening these matrices. The source study motivates seed controls;
our BUB1B-specific results are a new reanalysis.
[Smith et al.](https://doi.org/10.1371/journal.pbio.2003213).

| Finding | Consequence |
|---|---|
| All ten BUB1B reagents have distinct deposited 6-mer/7-mer seeds. | Annotated seed independence is checked; mature products, alternate seeds and potency remain unmeasured. |
| In each representation, 45/54 evaluable BUB1B reagent-context records correlate more with unrelated same-seed reagents than BUB1B peers. One HEPG2 record lacks a comparator. | Include same-seed, different-target controls. This association does not prove that all BUB1B signal is off-target. |
| HT29: six-reagent PRIME coherence 0.1187; 236/100,000 batch/replicate-count controls equal or exceed it. Add-one tail 0.002370, fixed 36-test BH-adjusted tail 0.01422; raw adjusted tail 0.21276. | Retain a model-qualification lead. This differs from v19's five-provider-reagent finding and is not a non-cancer MVA model. |
| Most exact seed references contain only 4-40 combinations. A post-hoc add-one sensitivity across all finite sets changes 5/36 primary threshold crossings to 0/36 after BH; HT29's batch value becomes 0.08532. | Other tails in the same fixed family changed; HT29's observed effect did not. Zero exceedances do not mean zero error probability. Prespecify coverage and multiplicity. |
| Other-gene RNAi/CRISPR intended-target top ranks: raw 14/297, PRIME 21/297; MTOR PRIME ranks 1-13 across six cell pairs. No BUB1B CRISPR profile is available in this older panel; LINCS2020 supplies newer coverage below. | Orthogonal agreement is sometimes recoverable. Dependent, selected targets and parental/Cas9 cell differences limit this reference; it does not qualify BUB1B or everolimus. |

Missing HEPG2 comparisons stay unknown; neither operational tail analysis establishes
exchangeability or calibrated false-discovery rates. Finite-reference sensitivity
challenges certainty, not the existence of BUB1B biology. Independent target/function
confirmation is still needed. The [qualification addendum](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-validation-v23.md)
requires seed/coverage records, batch-aware allocation, independent BUB1B perturbation
and restoration, and fixed missing-data rules. Compare joint treatment with deficit
alone and drug alone; engagement, expression reversal and functional benefit are
separate endpoints.

Eight H100s completed 1,536,619,950 pair comparisons, 5,843,968 conditional control-set
evaluations and 2,364,754 orthogonal reference comparisons. These reuse observations;
they are not sample sizes. CUDA statistics were brief and bursty, with no new neural
inference. Public audit hashes bind full results and the 161-file archive. Original
GCTX coordinate spotchecks agree with SciPy within 5.27×10⁻⁸. This checks arithmetic,
not independent scientific review. The two RNAi analyses do not change drug priority,
phase, clinical margins or the need for a direct joint-treatment experiment.

### New CRISPR coverage strengthens assay qualification, with limits

The [LINCS2020 reanalysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-v25.md)
uses original Broad matrices with 140,945 CRISPR treatment profiles, 1,956 controls and
720,216 compound profiles. Exact metadata joins leave no unannotated columns. There
are 31 BUB1B CRISPR profiles across 19 cell contexts, all from one guide ID,
BRDN0001148077. Their source wells do not overlap each other or the older BUB1B panel;
repeated batches still do not supply independent guides. RNAi comparisons reuse v23.
The plan preceded new matrix inspection, after metadata and earlier-result review.
[Source manifest](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-source-manifest-v25.json).

HT29 has the strongest PRIME RNAi/CRISPR concordance among the five shared BUB1B
contexts. Scores use 978 measured genes. The two retrieval directions compare the
observed BUB1B match with all assayed targets in that context:

| Cell | PRIME correlation | Rank among RNAi targets | Rank among CRISPR targets |
|---|---:|---:|---:|
| A375 | 0.2144 | 159 / 3,826 | 827 / 5,119 |
| A549 | 0.2084 | 74 / 3,724 | 443 / 5,137 |
| HT29 | 0.3712 | 4 / 3,665 | 4 / 5,113 |
| MCF7 | −0.0887 | 2,860 / 3,471 | 3,839 / 4,274 |
| PC3 | −0.0293 | 3,525 / 3,822 | 4,032 / 5,113 |

Removing BUB1B's measured transcript leaves HT29's correlation at 0.3693 and both
ranks fourth. Its two CRISPR batches correlate at 0.3594 and retrieve the same guide
first in both directions. Across nine repeated BUB1B contexts, only 2/30 directed
retrievals rank first; both belong to this pair and the 30 retrievals reuse 15
correlations. One HT29 batch fails QC. These results support a narrow attribution
test in HT29, not independent-guide qualification or transfer to non-cancer MVA.

The broader benchmark retains unfavorable findings: 8,623/57,044 directed cross-batch
queries retrieve their guide first. Among 7,983 shared gene/context records, PRIME
retrieves the intended RNAi target first in 72 cases and the CRISPR target in 94.
Selection and dependent observations prevent treating these fractions as population
accuracy or p-values.

### Favorable drug connections do not supply the missing model

Of 628 everolimus-labelled profiles, 271 match the reference InChIKey and 82 pass the
declared drug QC across the source release. The other 357 retain unresolved chemical
identity. Among the 15 reference-matching comparisons in BUB1B contexts, five pass
drug QC; all five correlate negatively with BUB1B, with signs retained after either
BUB1B-feature removal or common-response sensitivity. All five BUB1B queries have
zero passing profiles. Three passing drug profiles use 0.1 µM nominal culture exposure:

| Cell | BUB1B correlation | Reversal rank among CRISPR targets | Passing BUB1B query profiles |
|---|---:|---:|---:|
| A375 | −0.0043 | 2,402 / 5,119 | 0 |
| YAPC | −0.0261 | 616 / 5,113 | 0 |
| MCF7 | −0.2144 | 7 / 4,274 | 0 |

MCF7 also retrieves MTOR first among 4,274 targets (correlation 0.2836), with one
passing MTOR query profile. Retain that mechanism evidence alongside failed BUB1B
query QC and RNAi disagreement. HT29's available reference-matching everolimus profile
is at 10 µM, fails drug QC and correlates positively with BUB1B loss. No context has
independent-guide qualification plus a joint functional rescue result. HT29 model
findings and MCF7 drug findings cannot be combined into one experiment.

The [source-well audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-continuity-v25.json)
finds that newer A375 and NPC 0.1 µM signatures regroup three older singleton wells
per cell under new IDs. A375's aggregate now passes drug QC. Better aggregation
preserves the earlier failures and does not create independent replication. The
MCF7, YAPC, A549 and PC3 0.1 µM profiles have no shared wells with that older GSE70138
release. This continuity audit does not establish clinical exposure or a dose response.

The [qualification requirements](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-validation-v25.md)
add independent guides/restoration, a complementary perturbation that avoids the same
DNA-cutting event, and controls for editing stress, residual function and survivor
selection. Favorable acute genotoxic-stress findings in human T cells do not establish
everolimus rescue in MVA. Editing-associated p53 responses and incomplete developmental
rescue after Trp53 co-deletion in BubR1-deficient mice also limit response suppression
as an endpoint. These are different experiments; reading depth and limitations are
recorded in the [targeted source review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-sources-v25.json).

All eight H100 workers completed 2,474,445,074 comparisons, including sensitivity
analyses and reused profiles, across cross-batch, orthogonal and compound panels.
285,488 compound profiles were scored in matched contexts. Timed CUDA products totaled
1.231 seconds; preparation, CPU summaries and I/O dominated. One-second monitoring
peaked at 8% GPU utilization. This was brief GPU execution, without new neural inference
or sustained saturation. Original-coordinate CPU checks of 141 BUB1B/everolimus
comparisons agree within 2.83 × 10⁻⁷ (tolerance 2 × 10⁻⁵). Numerical agreement is internal
verification, not independent biological review. The
[186-file archive and reproduction guide](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-reproduction-v25.md)
retain complete results, provenance and failed attempts. No drug priority, phase or
clinical exposure margin changes.

## 4. Experiment and stopping rules

**Qualify.** Compare wild type, mock editing, each single allele, cis, trans and corrected
derivatives in an editable non-cancer context. Verify engineered genotype/phase,
endogenous RNA/protein and comparable cell states. Confirm the deficit with an independent
genetic perturbation and expression-matched correction control. Record seed/alternate-seed
coverage and target engagement; include unrelated same-seed controls for RNAi. Preserve
replicate IDs and batch allocation, with finite-control and missing-data rules fixed
before confirmation. Count guide identities and source wells separately from profiles.
Use independent perturbation/restoration and a complementary method that avoids the
same DNA-cutting event; measure editing stress, residual function and survivor selection.
HT29 qualification cannot substitute for a relevant non-cancer model. Failed assay controls
make the measurement invalid; insufficient precision is inconclusive. Neither makes
an allele benign. Measure attachment, checkpoint
activation/maintenance/silencing, accurate viable daughter production and lineage
function separately. Published 731X complementation cannot assign L737Ter's phenotype;
ectopic cDNA can bypass RNA decay. Renal or muscle models need their own qualification.
Without a reproducible relevant phenotype, hold drug advancement and revise the model;
an absent result does not establish clinical normality.

**Probe.** Lock branch eligibility. Include vehicle, an assay-qualified positive control,
corrected-model comparisons and an interpretable orthogonal pathway perturbation.
Resolve compound identity before dosing. Test drug plus the qualified deficit; separate
single-perturbation profiles cannot substitute. Randomize independently treated wells/cultures within clone/day/plate blocks and
blind scoring. Cells are nested observations; technical repeats do not add biological
backgrounds. Model crossed clone/day effects or justify aggregation. Measure graded exposure,
time-matched engagement, useful function, BUBR1/chromosome fidelity and delayed recovery.
Orthogonal disagreement limits mechanism attribution without automatically disproving
a drug-specific effect. Without a clinical exposure bridge, the probe stays exploratory.

**Confirm.** Use pilot performance to prespecify meaningful benefit, acceptable injury,
outcome definitions, missingness analysis, multiplicity handling and sample size before
collecting independent confirmation data. Replicate across clones/backgrounds and culture days; multiple clones do not create
independent donors. Genotype-specific benefit needs an interaction contrast, while
useful benefit shared with corrected cells need not be rejected. Current data
justify no numerical margin, power estimate, laboratory budget or timeline.

| Evidence | Decision |
|---|---|
| Failed assay/control or changed confirmation plan | Invalid/hold inference; this does not refute biology. |
| Phenotype, mechanism or confirmation unresolved | Hold. A valid test rejecting branch eligibility stops that branch. |
| Valid interval excludes meaningful benefit | Stop that tested claim; an interval spanning the target remains inconclusive. |
| Only a marker or surviving-cell ratio improves | Do not advance. Require replicated function and accurate viable output across enrolled units. |
| Division, viability, fidelity, regeneration or recovery exceeds prespecified injury bounds | Stop despite apparent benefit. |
| Exposure is unmatched or unknown | Block translational promotion. Match analyte, matrix, free fraction, schedule and sampling context. |
| All requirements met | Preclinical review only. |

A benefit interval must clear a justified meaningful-effect threshold; every injury
interval must exclude unacceptable harm. Nonsignificance is not safety. All actual
measurements and margins in the [decision contract](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-decision-contract-v21.json)
remain null, so the executable rule returns HOLD. It checks proposed logic, not biology.

Whole-blood trough, total-plasma peak, nominal culture concentration and unbound tissue
exposure are not interchangeable. All clinical exposure margins remain null. Operational
details are in the [validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v21.md)
and [exposure ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-exposure.json).

Enroll cells before exposure; retain accurate/erroneous division, death, persistent
arrest, slippage and tracking loss separately. Follow daughters and recovery. Mature
non-dividing tissue needs qualified lineage-function endpoints. Tumour killing requires
documented subtype and matched deficient-normal controls, separate from non-cancer rescue.

In a **synthetic example, not experimental data**, 100 cells are enrolled per arm.
Errors among completed divisions fall from 20/80 (25%) to 5/45 (11.1%), while accurate
viable output falls from 60/100 to 40/100. The first ratio conceals worse output.
The executable example retains death, arrest and missing tracks; missingness bounds
do not replace sampling uncertainty.

Check flux reporters for pH, expression, optical interference and cell-loss artifacts,
using orthogonal cargo turnover. Compare tumour/normal viable counts from baseline
over time; growth-rate sensitivity requires sufficiently growing untreated controls.
ATP/metabolic signal alone is not a viability endpoint.
[Growth-rate methods](https://doi.org/10.1038/nmeth.3853),
[flux reporter](https://pmc.ncbi.nlm.nih.gov/articles/PMC3121655/).

## 5. Contribution and reuse

A validated positive result could justify further investigation; a well-measured
negative or harmful result could stop that route in the tested context. The contribution
combines genotype/phase alternatives, active falsification, all-enrolled outcomes and
benefit/harm/exposure gates. The individual methods are established; superiority over
another framework is untested.

Reviewers can check public evidence consistency on a CPU without subject files, API keys,
SSH or model weights:

```bash
uv run --no-project python scripts/track2_public_review_v26.py
```

This checks requirements, discussion coverage, control sensitivity, decisions and
slide/script alignment, including all three frozen expression campaigns, their favorable
HT29 findings, seed controls, finite-reference sensitivity, guide independence and
source-well continuity. It neither reruns models nor validates biology. Complete model
plans, matrices and failed attempts remain in the technical history.

Laboratory reuse starts with one qualified context and branch. A new genotype or tissue
requires fresh mechanism, assay, exposure and safety qualification. Models, imaging,
function assays, exposure measurement and replication are the resource constraints.
Seven groups × three clones × three days × two conditions gives 126 culture allocations
before concentrations or technical replicates: planning arithmetic, not a sample-size
recommendation, available collection or power estimate. Fund each stage after its
preceding decision.

The rubric weights rigor 35%, impact 25%, innovation 25% and scalability 15%; this
proposal addresses them through the evidence, experiment and reuse plan. No judging
score or likelihood of winning is estimated.
[Rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py).

## 6. Limits and delivery

The v21 falsification audit covers 27 claims, carrying forward the original 19 claims.
Five RNAi and five CRISPR challenges supplement it, giving 37 claim records across
three registers.
Each records support, challenge, falsifier, stop/reopen criteria and a next action.
These are claim records, not independent studies.
[RNAi register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-register-v23.json),
[CRISPR register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-register-v25.json). Original protein-control ordering passes
12/12 comparisons, but post-hoc expanded-control separation fails 8/12; 11/24
retained-function scores are negative. Dependent models/windows and small engineered
control sets cannot calibrate clinical pathogenicity. The secondary-control supplement
remains independently unreviewed. No prediction establishes allele function, phase,
drug response or exposure. [Audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-review-v21.md),
[register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v21.json).

The preserved v21 targeted review contains twelve source adjudications, including two rechecks and
a protocol/result overlap. Web discovery and PubMed queries were complemented by
sixteen failed Europe PMC requests; those failures provide no negative evidence.
Registry amendment history remains unverified. Reading depth varies from indexed abstracts to selected primary passages. Balnis units, endogenous
effects, tissue response, exposure and meaningful margins remain unresolved; specialist
review and biological measurements are still needed.

The September 24 review covered the live website, source revision
`aeeef5ad49f51204a7439352e59e9d310aee5e9e`, methods workbook and all 24 public
discussions/68 latest comments. A separate agent checked requirements, not clinical or
experimental validity. [Website review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-official-requirements-review-20260924.md),
[discussion review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-community-review-20260924.md).

Submission requires a participant-named PDF/Markdown report, GitHub URL and three-minute
YouTube/Vimeo video. Three entries are allowed; only the latest is reviewed. Quota is
unknown. Runtime measurement, recording, hosting, owner/provider review, portal checks
and receipt remain open. No upload or contact occurred; prior submissions and snapshots
are preserved.

**Distribution scope remains unresolved.** Challenge CC BY requirements and historical
AF3/non-AVI Atlas output terms may cover linked materials differently. This report and
pitch omit their numerical outputs and figures; historical notices remain. That omission
does not settle submission scope or grant a blanket relicence. The
[readiness note](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v26.md)
records the outstanding question.

## 7. Methods answers and AI disclosure

These answers map to B7-B17 of the official template. B9 is required; other answers
are recommended. The filled workbook preserves the questions and comments on its
stale one-entry instruction; live instructions allow three entries.

**B7: Participant.** jvv7, individual entry; no institutional affiliation asserted.

**B8: Identification approach.** Connect the retained BUB1B pair to conditional
mechanisms; assess approved drugs, contrary evidence, exposure and deficient-normal
safety. Everolimus remains an optional probe, HCQ reserve; all eleven dispositions persist.

**B9: AI provider, plan and handling.** OpenAI Codex/API was used for code, literature
research, synthesis, editorial work and agent reviews. The owner attests no training on
content; this is not an independent account or zero-retention audit. Firecrawl's local
bridge previously used Fireworks-hosted GLM on owner-confirmed API credits for public
literature; training/retention settings remain unverified. Local retrieval is not proof
of local inference. Google DeepMind AlphaGenome Atlas supplied precomputed API/download
outputs, not on-demand inference; its output/service terms remain applicable. Owner-hosted
research used ESM-1v/ESM-2, ESMC 300M/600M/6B, ESM3-open 1.4B, Boltz-2, AlphaFold2,
AlphaFold3, ESMFold2 and Evo2 7B/20B/40B with public references and permitted derived
substitutions. Earlier ColabFold alignment search received only public wild-type protein;
service training/retention policies remain unverified. The public LINCS, RNAi and CRISPR campaigns used all eight owner-host H100s for statistical reanalysis,
not new neural-model inference, with brief, bursty kernels. Only public NIH/Broad data and
code were transferred under the owner's `~/v` folder. The v21 research used public literature searches and local decision-logic checks.
The v23 follow-up used public RNAi/CRISPR matrices, CUDA statistics and local numerical
checks. The v25 follow-up used public LINCS2020 CRISPR and compound matrices,
source-well audits and original-coordinate numerical checks. This v26 integration used
local editing, public-page spot-checks and offline rendering; it did not repeat the
September 24 full requirements/community audit. These revisions added no model provider or neural inference. Raw subject reads, VCF records and clinical
narrative stay local. Unknown settings are not silently attested. Historical AF3-derived
materials retain [AlphaFold3 Output Terms](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md), the
[Legally Binding Terms of Use notice](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt),
modifications disclosure and [Abramson citation](https://doi.org/10.1038/s41586-024-07487-w).

**B10: Automated versus curated.** AI suggests leads; author/source review determines
decisions. Scripts check provenance and declared constraints. Model agreement or passing
software checks does not predict efficacy.

**B11: Curation.** Compare proposals with primary passages, abstracts, labels and
registries. Record reading depth, failed retrievals, contradictions, wrong matches and
units. Public expression screening also retains failed QC, chemical-identity uncertainty
and post-hoc findings separately, including finite-control sensitivity, one-guide
coverage, reused wells and the distinction between drug and model quality. Agent and requirements reviews are not specialist clinical review.

**B12: Public versus proprietary evidence.** Drug/target evidence is public; earlier
genetic reasoning used gated challenge data. No proprietary drug-response data were
supplied. The project is not wholly public-input-only.

**B13: Public sources.** Primary papers, Europe PMC/PubMed, ClinicalTrials.gov,
DailyMed, NIH GEO/LINCS, CLUE metadata, PubChem/NCATS, UniProt/PDB/model resources and official challenge pages; exact sources are
in the ledgers. Search/model services are tools, not independent evidence.

**B14: Gated sources.** Organizer WGS and phenotype informed earlier local analysis
under signed terms. Only permitted derived findings appear here; no other proprietary
experimental, clinical or drug/target dataset is claimed.

**B15: Mechanism.** BUBR1 checkpoint/attachment dysfunction is established at gene level.
Pair-specific function and phase are unknown. Everolimus tests conditional downstream
mTORC1 hypotheses; both branches require qualification.

**B16: Effort.** Work began September 8. Total person-hours, GPU time and API/lab costs
are unaggregated. Any reported CPU review time covers that command only; no overall
speedup, budget or clinical timeline is claimed.

**B17: Method abstract (under 500 words).**

We propose a qualified everolimus experiment for non-cancer function in BUB1B-associated
MVA. Phase and endogenous allele effects are unresolved; no drug earns rescue priority.
Different-model mTOR findings motivate an optional probe. Functional counterevidence
requires direct tests of benefit, injury and recovery.

Earlier uncalibrated expression filters and RNAi seed controls leave target attribution
uncertain. HT29 retains favorable RNAi coherence with sensitivity to finite reference
sets. New public CRISPR data contain 31 BUB1B profiles across 19 contexts, all from one
guide. HT29 ranks fourth in both PRIME RNAi/CRISPR retrieval directions, unchanged after
removing BUB1B's measured transcript. One batch fails QC; a tumour line cannot establish
non-cancer model validity.

Three reference-matching everolimus profiles at 0.1 µM nominal culture exposure pass
drug QC and correlate negatively with BUB1B. Their BUB1B queries all fail QC. MCF7
retrieves MTOR first, but its BUB1B result disagrees with RNAi. Do not combine HT29
model findings with MCF7 drug findings into a joint rescue claim. Source-well checks
also identify reaggregated older experiments under new signature IDs.

The 37 claim records preserve favorable findings, model-control failures and functional
counterevidence. Qualify endogenous single-allele, cis/trans and corrected models with
independent perturbation/restoration, seed controls and editing-stress controls. Lock
eligibility, missingness and multiplicity before randomized, blinded drug-plus-deficit
tests against each alone. Measure useful function, accurate division, all cell fates
and recovery. Confirm independently with justified benefit/injury margins and matched
exposure. Invalid assays hold inference; imprecision holds advancement. Valid evidence
excluding meaningful benefit stops that tested claim. Failed safety stops advancement;
all-pass permits preclinical review only. HCQ remains reserve.

Public CPU checks support reproducibility. Biological results, clinical margins,
recording and final delivery remain unresolved.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
