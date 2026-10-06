# Testing everolimus for useful cell function in BUB1B-associated MVA

Track 2 research proposal · jvv7 · 7 October 2026 · v32

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

Everolimus is an approved mTORC1 inhibitor proposed as an optional probe of non-cancer
function in a qualified BUB1B-deficient model. Advancement requires useful function
without unacceptable injury to division, viability, chromosome fidelity or regeneration.
No rescue-priority drug is supported. Selected-pair efficacy, trans phase and clinical
exposure margins are unresolved; no wet-lab experiment has been performed.

Public RPE1 data show a repeatable BUB1B expression response with weak own-target
retrieval. BUB1B matching across RPE1 and K562 is much weaker than MTOR matching.
One shared guide pair and selected controls leave model attribution unresolved.
The revised plan therefore requires independent perturbation/restoration, relevant
function and an appropriate control population before drug matching.

ProteinMPNN fails the expanded functional-control comparison in all 24 settings,
so its candidate score cannot qualify function. Symmetric held-out expression tests
retain HT29 as an assay-development lead after failed CRISPR profiles are removed.
One guide and tumour context still limit it. MCF7 has no QC-qualified BUB1B query;
its everolimus reversal weakens after shared-pattern removal while MTOR matching
remains first. These findings in different cells cannot supply a joint rescue result.

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

### Structural compatibility does not qualify BUBR1 function

The [ProteinMPNN analysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-v29.md)
used four related checkpoints, six WT domain backbones and 21 positions. Including
mutant-backbone sensitivity, 528 contexts produced 67,584 fixed-site samples.
Historical primary control ordering passes **1/24** comparisons; expanded ordering
passes **0/24**. These are model/control comparisons, not biological replicates.

N1002K has the lowest mean N-to-K log odds among 17 matched sites in all WT
backbone/checkpoint comparisons. WT-backbone values range from -5.6961 to -5.3893;
mutant-predicted backbones shift them to -2.7797 through +0.4625. This sensitivity
and the failed controls prevent a stability, pathogenicity or drug-priority inference.
The model ranks structural compatibility; it does not measure endogenous function.

Control labels depend on the endpoint. The 2012 study retained D882N/A in its
measured reconstitution assays. The 2019 study reports retained D882N stability but
lost CENP-E phosphorylation. The 2020 study retained D882N/A stability and KARD-S676
signals, supporting an indirect scaffolding account without excluding catalysis in
untested conditions. The catalytic disagreement remains unresolved. Preserve the
original control gate and test abundance, scaffolding and catalytic endpoints
separately, alongside endogenous chromosome attachment and segregation.
[Suijkerbuijk 2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[Huang 2019](https://doi.org/10.1038/s41422-019-0178-z),
[Gama Braga 2020](https://doi.org/10.1016/j.celrep.2020.108397).

### Drug and functional counterevidence

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

The v31 literature search screened 98 returned titles from eight bounded queries;
selected abstracts and primary passages were read. It was not a systematic review.
BIOMEDE randomized active tumour-treatment arms but compared its primary survival
endpoint with a historical cohort and stopped for futility. Favorable everolimus
tolerability and exploratory biomarker signals remain relevant within that study.
TEAMMATE's selected pediatric heart-transplant population had a nonsignificant primary
efficacy comparison, safety noninferiority and favorable secondary renal/CMV outcomes
under different combination regimens. Neither establishes MVA benefit or exposure.
A 2026 budding-yeast TORC1/cohesin finding adds a chromosomal-injury hypothesis;
only its primary abstract was available, and it does not establish human toxicity.
[BIOMEDE](https://doi.org/10.1038/s41591-026-04354-1),
[TEAMMATE](https://doi.org/10.1001/jama.2025.14338),
[yeast study](https://doi.org/10.1093/bbb/zbag087),
[reading depth and decisions](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-source-review-v31.md).

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
drug QC; all five correlate negatively with BUB1B. Signs survive the original
BUB1B-feature and common-response checks; the stronger v27 adjustments below weaken
that conclusion, including sign changes in A375. All five BUB1B queries have
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

### Stronger falsification tests separate the assay lead from the drug signal

The [v27 analysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-v27.md)
tests five shared cell contexts in raw and PRIME space. It removes 13 measured
cycle/stress features from a declared 20-feature set (seven are absent), then separately
removes the pooled mean direction plus 1, 3 or 10 principal components. These post-hoc
tests were chosen after the HT29 finding. The fit excludes BUB1B, MTOR and eight related
targets, but includes competing reference targets: this is not a symmetrically held-out
retrieval benchmark. Projection can remove real biology; attenuation does not prove
confounding, and residual cosine is not a causal estimate. Growth/death can influence
expression matching. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC6821211/).

| View | HT29 PRIME correlation | RNAi rank / 3,665 | CRISPR rank / 5,113 |
|---|---:|---:|---:|
| Original 978 features | 0.3712 | 4 | 4 |
| Remove 13 cycle/stress features | 0.3602 | 4 | 4 |
| Mean direction + PC1 removed | 0.3613 | 4 | 3 |
| Mean direction + PC3 removed | 0.1972 | 3 | 2 |
| Mean direction + PC10 removed | 0.1510 | 4 | 5 |

HT29 retains relative ranks 2-5 despite weaker absolute agreement. A375 and A549
attenuate more, while MCF7 and PC3 remain weakly negative. This strengthens the limited
HT29 attribution test; one guide, failed-batch QC and tumour context still prevent
independent qualification or transfer to non-cancer MVA.

For the reference-matching MCF7 everolimus profile at **0.1 µM nominal culture**,
BUB1B reversal ranks change **7 → 8 → 78 → 125 → 1,184** across the same five views
(4,274 target references). Correlation changes from −0.2144 to −0.0297. **MTOR stays
rank 1** throughout, with correlation 0.2836 to 0.2250. Drug QC passes; BUB1B query QC
fails in every view. The original rank 7 is not a robust rescue rationale. A375's small
BUB1B correlation changes sign in two sensitivities. HT29's 10 µM drug profile fails
QC and remains positively correlated in all five views. These are separate perturbations;
neither shared targets nor stronger HT29 concordance supplies a joint drug-rescue result.

Four local models (ESMC 300M/600M/6B and ESM3-open 1.4B) also scored complete
substitution backgrounds in three prior BUBR1 windows: **9,472 masked distributions,
179,968 non-reference scores and 19,950 distinct substitution identities**. Models and
windows reuse identities; this is not experimental deep mutational scanning. Between
71.6% and 89.8% of background scores are negative, so a negative sign alone is weak
evidence. N1002K is relatively incompatible among matched N→K substitutions in
ESMC 600M/6B, but its ranking varies by model and comparison set. These fractions are
not p-values or pathogenicity probabilities. In ESMC 6B, lysine is the second-most
compatible alternative at residue 1002: positional constraint does not identify a
uniquely damaging lysine. Original controls still pass 12/12; expanded separation
still fails 8/12. No score establishes benignity, functional defect, L737Ter RNA decay,
splicing, phase or drug response.

All eight H100s executed the v27 work, including new protein-model inference and
918,999,010 expression comparisons. Aggregate timed neural CUDA forward work was
1,004.196 seconds; setup and checkpoint verification are excluded. Each GPU reached
a sampled 100%, with unequal completion times, not continuous eight-GPU saturation.
Expression products took 0.572 seconds, excluding eigendecomposition, CPU work and I/O.
Original protein scores reproduce within 3.55 × 10⁻⁵ and sampled expression CPU/GPU
differences within 3.78 × 10⁻⁷. All jobs finished. Full matrices, failed attempts,
source-reading depth and the 178-file archive are bound in the
[reproduction record](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-reproduction-v27.md).
This checks numerical continuity; no new biological observation was collected.

### Symmetric held-out expression tests

The [v29 fixed plan and results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-v29.md)
address a limitation of the v27 projection: evaluated reference genes helped fit it.
The new analysis excludes all ten query genes and every evaluated reference gene
from fitting in both modalities. Five cells, raw/PRIME spaces, all-profile/QC-only
views and four repeated five-fold partitions give **400 fits / 820,147,416 comparisons**.
Pooled mean and PC1/3/10 removal are sensitivity analyses, not causal adjustments.
The plan preceded these runs but followed the earlier findings.

| View | HT29 PRIME correlation | RNAi retrieval rank | CRISPR retrieval rank |
|---|---:|---:|---:|
| All profiles, unadjusted | 0.3712 | 2-4 | 2-3 |
| All profiles, mean + PC10 removed | 0.1391-0.1670 | 1-3 | 1-4 |
| Passing CRISPR profiles only, unadjusted | 0.3500 | 2-3 | 2-4 |
| Passing CRISPR profiles only, mean + PC10 removed | 0.1223-0.1371 | 1-6 | 1-3 |

Ranges describe repeated partitions, not confidence intervals. Each fold has 715-781
RNAi references; CRISPR has 945-1,088 with all profiles or 276-340 after QC restriction.
Smaller within-fold ranks are not comparable with prior full-panel ranks. Removing
the failed HT29 batch retains favorable agreement, but one guide, RNAi seed/potency
uncertainty and tumour context still require independent perturbation/restoration
and relevant non-cancer model qualification.

MCF7 has **no QC-qualified BUB1B query**. This is missing evidence, not a zero score.
In its all-profile view, reference-matching everolimus at **0.1 µM nominal culture**
changes from BUB1B correlation -0.2144 to -0.0335 through -0.0259 after mean-plus-ten-PC
removal. Within-fold reversal rank changes from 1-3 to 204-308 among 787-920 references.
MTOR mimicry remains rank 1, including QC-restricted references. Drug quality and
target engagement cannot repair an unqualified BUB1B query. Cross-cell evidence and
separate perturbations still do not measure joint functional rescue.

Twenty full-panel unadjusted controls reproduce earlier ranks; maximum correlation
difference is 3.05e-7. CPU/GPU differences are at most 5.44e-7. All eight H100 workers
finished both campaigns. Local recomputation verifies all archived values; protein
aggregates differ by at most 1.78e-15 across runtimes. The
[3,838-file archive](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-reproduction-v29.md)
retains original outputs and failed attempts. Compute counts and numerical agreement
do not provide independent biological replication. Sampled protein-run utilization
reached 100% per GPU; continuous saturation is not claimed.

### Non-cancer Perturb-seq tests detectability and specificity separately

We reanalyzed Replogle et al. public CRISPRi data: 247,914 retained RPE1 cells and
310,385 K562 essential-screen cells. RPE1 is a non-cancer, hTERT-immortalized retinal
epithelial line; it does not reproduce the child's tissue or alleles. BUB1B has
106 RPE1 and 141 K562 cells from one shared paired-guide construct. These cells
and 1,024 random splits per cell type do not provide independent perturbation designs.
[Source study](https://doi.org/10.1016/j.cell.2022.05.013),
[public dataset](https://doi.org/10.25452/figshare.plus.20029387),
[complete analysis](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-v31.md).

The plan preceded target-effect inspection. A documented amendment removed a
proposed comparison that the export could not support: all retained non-targeting
cells already belong to provider-selected core controls (11,485 RPE1; 10,691 K562).
An unselected-control sensitivity is unavailable. Four seed blocks per cell replaced
those duplicate views. Expression uses log1p CP10k with original full-library UMI
totals, batch-matched controls and disjoint control halves. All ten planned query
states and three feature views remain in the results.

| Cell | BUB1B target/control CP10k ratio | Split-half median correlation | Median own-target rank, first / reverse direction |
|---|---:|---:|---:|
| RPE1 | 0.0487 | 0.6572 | 171.5 / 2,154; 183 / 2,154 |
| K562 | 0.0962 | 0.1197 | 323.5 / 2,077; 320 / 2,077 |

These values exclude the query transcripts, leaving 4,852 common measured features.
Despite substantial target suppression, BUB1B's first-direction top-10 retrieval
occurs in 0/1,024 RPE1 splits and 1/1,024 K562 splits. MTOR's median rank is first in
both directions and cells. Removing query and cell-cycle genes leaves BUB1B median
correlations of 0.6290 and 0.1166 without distinctive retrieval. This finite panel
contains selected essential-gene perturbations; ranks are contextual comparisons,
not calibrated classification accuracy or a biological threshold.

Across RPE1 and K562, BUB1B correlation is 0.1043, with ranks 980/2,077 and
386/2,154. MTOR correlation is 0.5836, with ranks 1/2,077 and 2/2,154. Cell type,
sampling time and CRISPRi effector differ. These results do not support transferring
BUB1B signatures across contexts merely because MTOR matches. Both BUB1B response
norms exceed all 1,024 matched selected-control draws, which establishes conditional
detectability only. Control selection may make this reference optimistic.

RICTOR is absent in both exports. RPE1 CDC20 and AURKB have 15 and 5 cells, below the
fixed 30-cell retrieval requirement. RPE1 RPTOR has 30 cells but its transcript is
unmeasured. None becomes a zero effect. The source authors' RNA-derived CNV scores
are expression-based estimates, not newly measured DNA or a clinical karyotype.
Retain RPE1 as a functional-assay comparator pending independent attribution,
restoration, division fidelity, daughter survival and later function. No joint
BUB1B-deficit-plus-drug response was measured.

All eight H100s completed 27,628,823,832 CUDA correlations and 2,048 split repetitions,
plus 13,421,574 CPU cross-cell comparisons. They reuse public observations. Timed
CUDA products totaled 6.476 seconds; worker wall times were 40-59 seconds and sampled
utilization peaked at 19-24%. This was statistical computation, not neural inference
or sustained GPU saturation. Original-count CPU checks agree within 2.83e-6.
Local reanalysis reproduces all three full cross-cell matrices exactly; summary
rounding differences are at most 2.23e-16. The verified 226-file archive preserves
original outputs, plans, amendment and failed attempts.
[Reproduction](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-reproduction-v31.md).

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
Prespecify expression adjustments before confirmation; compare growth, viability and
editing responses alongside target-specific restoration. Model scores need calibrated
functional controls and cannot replace endogenous measurements. The D882N conflict
requires endpoint-specific controls for abundance, KARD/PP2A scaffolding and catalysis;
measure chromosome attachment and segregation directly. The
[v29 qualification amendments](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-validation-v29.md)
apply alongside the earlier safeguards. The
[v31 amendments](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-validation-v31.md)
require distinct checks of detectability and specificity, unselected-control coverage,
independent constructs/restoration and context-specific qualification. Paired guides
in one construct and repeated cell splits do not supply biological replication. HT29 qualification cannot substitute for a relevant non-cancer model. Failed assay controls
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
uv run --no-project python scripts/track2_public_review_v32.py
```

This checks requirements, discussion coverage, control sensitivity, decisions and
slide/script alignment, including the three frozen expression campaigns, v27 sensitivity/protein backgrounds
and v29 structural/held-out tests and v31 Perturb-seq results, their favorable
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
[Rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/c9b4a7e6247574124cd5bbfd249af9af6f1bbac3/tabs/about.py).

## 6. Limits and delivery

The v21 falsification audit covers 27 claims, carrying forward the original 19 claims.
Five RNAi, five CRISPR, five protein/specificity and five structural/held-out
challenges supplement it, giving
52 claim records across six registers, including five Perturb-seq challenges.
Each records support, challenge, falsifier, stop/reopen criteria and a next action.
These are claim records, not independent studies.
[RNAi register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-register-v23.json),
[CRISPR register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-register-v25.json),
[v27 register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v27.json),
[v29 register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-register-v29.json). Original protein-control ordering passes
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

The October 6 refresh checked live source revision
`c9b4a7e6247574124cd5bbfd249af9af6f1bbac3`, the methods workbook and all 26 public
discussions/79 latest visible comments. New/edited comments were reread; unchanged
content retains the September review. Judging now ends December 17, with winners
announced December 18. Submission and data-deletion deadlines are unchanged. The
latest organizer consumer-tier correction does not verify our provider settings or
relax our raw-data rule. Organizers will not confirm candidate-specific phase during
the challenge. This cycle has no independent requirements reviewer.
[Official refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v30.md).

Submission requires a participant-named PDF/Markdown report, GitHub URL and three-minute
YouTube/Vimeo video. Three entries are allowed; only the latest is reviewed. Quota is
unknown. Runtime measurement, recording, hosting, owner/provider review, portal checks
and receipt remain open. No upload or contact occurred; prior submissions and snapshots
are preserved.

**Distribution scope remains unresolved.** Challenge CC BY requirements and historical
AF3/non-AVI Atlas output terms may cover linked materials differently. This report and
pitch omit their numerical outputs and figures; historical notices remain. That omission
does not settle submission scope or grant a blanket relicence. The
[readiness note](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v32.md)
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
source-well audits and original-coordinate numerical checks. The v27 follow-up added
local ESMC/ESM3 protein inference and expression sensitivity analyses on all eight H100s.
The v29 follow-up executed ProteinMPNN through Anthropic's uplifting-biomolecular-modeling
toolkit at `f4f62fa6592ae4938d49b1757bea0cfeff9f468e`, after its review-only use in v27.
Four related checkpoint sets use public predicted structures; fixed-site samples are
not independent models or biological replicates. A bounded stock/exact pilot and
sampling/direct-conditional check passed; failed attempts remain archived. V29 also
ran symmetric held-out expression/QC statistics on all eight H100s. Earlier local
FP32 runtimes remain recorded. No new hosted provider was added. V31 used public Replogle/Weissman Perturb-seq
counts for CUDA statistics on all eight H100s, with original-count CPU checks and
local archive reanalysis. It performed no new neural inference or subject-data transfer.
This v32 integration
used Codex/API-assisted editing, anonymous official-page/source checks and offline rendering,
with no additional biological-model inference. Raw subject reads, VCF records and clinical
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
coverage, reused wells, protein-score backgrounds, post-hoc projection sensitivity
and endpoint-specific protein controls, held-out reference comparisons, missing qualified
queries and the distinction between drug and model quality. V31 also retains selected-control
coverage, shared guide-pair identity, missing query states, resampling dependence and
weak cross-cell transfer. Agent and requirements reviews are not specialist clinical review.

**B12: Public versus proprietary evidence.** Drug/target evidence is public; earlier
genetic reasoning used gated challenge data. No proprietary drug-response data were
supplied. The project is not wholly public-input-only.

**B13: Public sources.** Primary papers, Europe PMC/PubMed, ClinicalTrials.gov,
DailyMed, NIH GEO/LINCS, Replogle/Weissman Figshare data, CLUE metadata, PubChem/NCATS, UniProt/PDB/model resources and official challenge pages; exact sources are
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
MVA. Phase and endogenous allele effects remain unresolved; no drug earns rescue priority.
Different-model mTOR findings motivate an optional mechanistic probe. Functional
counterevidence requires direct tests of benefit, injury and recovery.

ProteinMPNN separates expanded functional controls in 0/24 comparisons. Candidate
scores depend on predicted backbone; related checkpoints and sampling repeats do not
validate function. D882N literature findings require separate stability, scaffolding
and catalytic endpoints.

Earlier expression filters and RNAi seed controls leave target attribution uncertain.
Newer CRISPR coverage has 31 BUB1B profiles but one guide. Symmetric held-out projections
exclude evaluated genes from fitting. HT29 PRIME agreement survives CRISPR QC restriction;
its adjusted correlation ranges from 0.1223 to 0.1371. One guide and tumour context
still prevent independent qualification or transfer to non-cancer MVA.

MCF7 has no QC-qualified BUB1B query. Reference-matching everolimus reversal weakens
under adjustment while MTOR matching remains first. Drug QC cannot repair query QC;
HT29 and MCF7 cannot supply a joint rescue result. Reused source wells remain identified.

Public Perturb-seq adds 558,299 retained cells. BUB1B suppression produces a
repeatable RPE1 response but weak own-target retrieval and weak cross-cell matching.
One shared guide pair and selected controls leave attribution unresolved. Repeated
splits are not biological replication. RPE1 remains an assay comparator pending
functional qualification.

The 52 claim records retain favorable findings and counterevidence. Qualify endogenous
single-allele, cis/trans and corrected models with independent perturbation/restoration,
seed and editing-stress controls. Lock eligibility, missingness and multiplicity
before randomized, blinded drug-plus-deficit tests against each alone. Measure useful
function, accurate division, all cell fates and recovery. Confirm independently with
justified benefit/injury margins and matched exposure. Invalid assays hold inference;
imprecision holds advancement. Valid evidence excluding meaningful benefit stops that
tested claim. Failed safety stops advancement; all-pass permits preclinical review only.
HCQ remains reserve.

Public CPU checks support reproducibility. Biological results, clinical margins,
recording and final delivery remain unresolved.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
