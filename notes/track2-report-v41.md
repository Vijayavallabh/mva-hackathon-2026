# Qualifying drug hypotheses for useful function in BUB1B-associated MVA

Track 2 research proposal | jvv7 | 20 October 2026 | v41

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

We propose qualifying endogenous BUB1B function before advancing a drug hypothesis.
Everolimus, an approved mTORC1 inhibitor, is a worked conditional branch, currently
on HOLD for missing biological prerequisites. It remains an optional mechanistic
probe. No rescue-priority drug is supported. We contribute a staged biological experiment
and an inspectable research review tool. The experiment asks whether useful function
can improve without worsening division, injury or recovery; the tool makes missing
evidence and reasons to stop visible to other teams.
Selected-pair efficacy, trans phase and clinical exposure margins remain unresolved.
No wet-lab experiment has been performed; no treatment or dose for the child is proposed.

**Decision in order.** First establish an endogenous deficit and independently
attributable functional restoration. Then qualify one intervention hypothesis in
the same model. Only then test joint treatment, useful output, injury and recovery.
All four stages remain unmeasured. The first experiment is model qualification.

**Why work through everolimus?** Its approved pharmacology makes mTORC1 perturbation
concrete, and carrier-mouse muscle supplies a bounded rationale. This is a testable
example, not demonstrated superiority over NAD/SIRT2 or the other retained candidates.
The [candidate comparison](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-candidate-comparison-v39.md)
sets out the supporting evidence, objections and prerequisites for each route.

## 1. Establish the mechanism before exposure

The retained hypothesis is BUB1B p.Leu737Ter / p.Asn1002Lys. BUB1B encodes BUBR1,
which contributes to spindle-checkpoint and chromosome-attachment control. Biallelic
disruption is an established MVA mechanism. This pair's endogenous RNA/protein effects
and residual function remain unknown. Engineered single-allele, cis and trans models
can test alternatives; they cannot establish the subject's phase. Competition scores
do not establish drug response. [Hanks](https://doi.org/10.1038/ng1449),
[Suijkerbuijk](https://doi.org/10.1158/0008-5472.CAN-09-4319).

The mouse mTORC1 rationale is narrower than a general BUB1B-deficiency signal.
Sieben Figure 5 measured increased p70 S6 kinase and 4EBP1 phosphorylation in
skeletal muscle of heterozygous BubR1+/X753 mice, relative to +/L1002P and wild type,
with relevance to later sarcopenia. It did not establish the same pathway state in
the retained compound-pair hypothesis or test rapalog rescue. The excess might be
pathogenic or adaptive. Everolimus could modify a downstream consequence; it does not replace
BUBR1 or establish chromosome repair. Specified TSC indications establish approval
and known pharmacology, not MVA efficacy or safety.
[Mouse study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781),
[label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2).

The first qualification question is **endogenous functional deficit and reversibility**,
shared by competing intervention hypotheses. Only then can **branch A**, excess
mTOR-associated activity with a functional deficit, qualify an everolimus experiment.
**Branch B**, impaired dynamic autophagic flux and
regeneration, remains a separately justified alternative with its own locked plan
and mechanistic controls. Neither branch is established for this pair.
Here A and B name two downstream mTOR-related hypotheses; the NAD/SIRT2
residual-protein hypothesis is a separate competing route, discussed below.
Do not switch branches after seeing results. The mouse L1002P allele is not the
retained human Asn1002Lys allele; similar numbering does not establish equivalent
function. The gene mechanism, pair-specific defect, downstream pathway and drug
response are four separate links in the evidence chain. Branch B's motivating hypercapnia
study has conflicting ex vivo units, 10 mM versus 10 micromolar, in related
supplemental methods. Both values remain quarantined; the 1,000-fold discrepancy
cannot set a concentration. [Balnis](https://doi.org/10.1172/jci.insight.182842),
[supplement](https://insight.jci.org/articles/view/182842/sd/pdf/render/1).

## 1b. V41 public literature addendum

A bounded [public literature refresh](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-v41.md)
checked PubMed and OpenAlex on 20 October 2026. Five searches, fourteen selected
2025-2026 sources and twenty-one public receipts are preserved in its
[audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-audit-v41.json).
The search found no constitutional-MVA rescue study for everolimus, NAD/SIRT2
or HCQ, so no drug disposition changed: everolimus remains a mechanistic probe
on HOLD and HCQ remains reserve.

Two consequences improve the first experiment without promoting any drug.
Current BUBR1 corona/MCC studies require checkpoint-architecture readouts:
BUBR1/MAD2/ZW10 kinetochore localization, MCC/APC/C engagement and durable
checkpoint maintenance, not protein abundance alone. A chromosomal-instability
microcephaly model motivates prespecified mitochondrial integrity and
proteostasis/ubiquitin-proteasome injury markers alongside later daughter fate.
A 2026 Aurora-B/BubR1 study places K250/S16/S39 in an attachment-coupled axis;
K250 state is therefore a mechanistic endpoint, not a generic rescue control.
This is bounded index/abstract-level literature review, not a new biological
result.

## 2. Counterevidence changed the experiment

| Evidence | Required change |
|---|---|
| Everolimus increased selected muscle-mass outcomes in aged rats, without established force benefit. Rapamycin impaired injured-mouse muscle regeneration. | Measure useful force/function and recovery directly; mass alone cannot qualify benefit. [Joseph](https://doi.org/10.1128/MCB.00141-19), [Ge](https://doi.org/10.1152/ajpcell.00248.2009). |
| Everolimus reduced BUBR1 in late-passage human stromal cells; early-passage response differed. | Measure BUBR1, chromosome fidelity and cell state. Protein loss alone does not establish injury. [Goutas](https://doi.org/10.1016/j.redox.2023.102701). |
| RAPA-EX-01: 40 older adults receiving sirolimus or placebo with exercise; primary difference -2.13 chair stands (95% CI -4.61 to 0.34; p=0.089). | No established functional benefit. Sensitivity analyses favored placebo but do not replace the primary result. This is indirect for everolimus/MVA. [Trial](https://doi.org/10.1002/jcsm.70274). |
| Young male rats lost force with rapamycin; adult female mice in PoWeR retained exercise-associated grip-strength/myofiber gains. | Context matters. PoWeR lacked sedentary drug arms and running volume differed; neither experiment establishes class-wide benefit or harm. [Rats](https://doi.org/10.1371/journal.pone.0312859), [PoWeR](https://doi.org/10.1111/acel.70183). |
| In experimental diploid/near-diploid and aneuploid cells, relative sensitivity to BUB1B/MAD2/TTK perturbation could reverse between early and prolonged assessment. | Prespecify later daughter fate, sustained output and recovery. The study used splitting/recovery and renewed perturbation, not continuous all-enrolled tracking, and did not test everolimus rescue. [Cohen-Sharir](https://doi.org/10.1038/s41586-020-03114-6). |

Tumour evidence remains separate. ARST1431 did not establish event-free-survival
benefit from adding temsirolimus to VAC/VI in 297 evaluable intermediate-risk RMS
participants (HR 0.86; 95% CI 0.58-1.26; p=0.44). BIOMEDE stopped for futility;
its primary survival comparison used a historical cohort despite randomized active
treatment arms. Favorable tolerability and exploratory biomarker findings do not
supply non-cancer rescue. [ARST1431](https://doi.org/10.1016/S1470-2045%2824%2900255-9),
[BIOMEDE](https://doi.org/10.1038/s41591-026-04354-1).

Selected pediatric TSC follow-up and TEAMMATE argue against assuming inevitable
developmental harm. TEAMMATE found safety noninferiority and favorable secondary
renal/CMV outcomes under different transplant combination regimens, with a
nonsignificant primary efficacy comparison. These data cannot isolate everolimus's
effect or establish MVA safety. Infection, renal, marrow/metabolic, wound-healing
and interaction risks require context-specific review. Additional individual
laboratory/treatment records are unavailable.
[TEAMMATE](https://doi.org/10.1001/jama.2025.14338),
[label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[organizer clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/14).

HCQ remains reserve. Its tumour/extract chromatin-timing effects prevent treating
it as a selective autophagy control; those studies do not establish MVA harm.
Pralatrexate remains a tumour-only hypothesis for relevant fusion-positive RMS;
temsirolimus is a clinical benchmark. Entinostat, vorinostat, niclosamide and
posaconazole remain deprioritized; PP2A tools, senolysis and readthrough remain
excluded. No combination is proposed. Genetic SIRT2 survival, NMN-associated BUBR1
abundance and niacin muscle findings are distinct experiments; they do not establish
niacin rescue of this pair. North's genetic SIRT2 intervention increased median
lifespan preferentially in male hypomorphic mice; females had no median-lifespan
change. That model retains low amounts of wild-type BUBR1, so the mechanism is not
established as allele-agnostic. Residual useful protein and deficient-normal function
must be tested before promotion. [North](https://doi.org/10.15252/embj.201386907).

Site and cell context also matter. Mouse K243 corresponds to human K250; these are
not two independent sites. Human K668 regulates stability in North's experiments.
SIRT2 knockdown in Suematsu altered K250 acetylation without the claimed total-protein
or prometaphase-to-anaphase changes. Qiu's K243R result concerns aged-oocyte meiosis;
Park's K243R/+ mice developed checkpoint defects, missegregation and spontaneous
tumors. This opposing somatic evidence rules out treating K243R as a generally
qualified rescue control, without proving all SIRT2 interventions harmful.
[Suematsu](https://doi.org/10.1016/j.bbrc.2014.09.128),
[Qiu](https://doi.org/10.1111/acel.12698),
[Park](https://doi.org/10.1083/jcb.201210099).

Use product-specific safety information. Zortress has a transplant boxed warning;
the inspected Afinitor/Afinitor Disperz label lists serious warnings and precautions
without that same boxed-warning section. A molecule-database flag or name stem
cannot establish a proposed use's risk-benefit.
[Afinitor](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=2150f73a-179b-4afc-b8ce-67c85cc72f04),
[Zortress](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=e082a024-7850-400b-a5c2-2a140612562a).

The
[63-source ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json)
and [v21 amendment](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v21.json)
retain all eleven dispositions, approval/indication details and source corrections.

## 3. What the computational work establishes

The public-data campaigns test model adequacy and alternative explanations.
Separate drug-only and deficit-only profiles cannot measure rescue in deficient
cells. Expression reversal might oppose compensation; useful function might
improve without reversal. A retrieval score is not a therapeutic endpoint.

| Analysis | Finding and consequence |
|---|---|
| Protein language models and ProteinMPNN | Original language-model controls pass 12/12, but expanded separation fails 8/12 and 11/24 retained-function scores are negative. ProteinMPNN used 528 contexts and 67,584 fixed-site samples; primary control ordering passes 1/24 and expanded ordering 0/24. Candidate scores depend on the predicted backbone. Do not infer endogenous function from them. |
| Public RNAi, CRISPR and compound profiles | Primary BUB1B expression qualification passes 0/14 contexts; the filter is uncalibrated. Seed, finite-reference, chemical-identity and QC sensitivities weaken drug matching. HT29 retains a favorable attribution lead after QC restriction and symmetric held-out fitting, with adjusted PRIME correlation 0.1223-0.1371, but tumour context and one CRISPR guide remain. |
| Everolimus matching | MCF7 has no QC-qualified BUB1B query. At 0.1 µM nominal culture exposure, reference-matching everolimus reversal weakens after adjustment while MTOR stays first. HT29 drug QC fails. Findings in different cells cannot supply a joint rescue experiment. |
| Public Perturb-seq | Among 558,299 retained cells, the RPE1 BUB1B response is repeatable (median split correlation 0.6572) but own-target retrieval is weak (median first-direction rank 171.5/2,154). Cross-cell BUB1B matching is 0.1043 versus MTOR 0.5836. One shared guide pair and selected controls limit attribution; repeated splits reuse cells. |

D882N/A control labels depend on the endpoint. The 2012 reconstitution assays,
2019 stability/CENP-E findings and 2020 KARD/scaffolding work do not resolve the
catalytic disagreement. Separate abundance, scaffolding and catalytic measurements,
then measure endogenous attachment and segregation. Ectopic complementation can
bypass RNA decay; published 731X behavior cannot assign L737Ter's phenotype.
[2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[2019](https://doi.org/10.1038/s41422-019-0178-z),
[2020](https://doi.org/10.1016/j.celrep.2020.108397).

Complete results, favorable exceptions, exclusions, source-well overlap and numerical
checks remain in the public records:
[expression](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-transcriptome-v19.md),
[RNAi](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-rnai-v23.md),
[CRISPR](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-crispr-v25.md),
[specificity](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-v27.md),
[ProteinMPNN/held-out tests](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-orthogonal-v29.md),
[Perturb-seq](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-perturbseq-v31.md).
Arithmetic checks do not constitute independent scientific review or biological
validation. Related models, overlapping public data and resampling are not
independent replication.

### Corrected optical comparison

The corrected comparison covers **838,224 mitotic cells** and **31,046,046
interphase cells**. All 16 real/shuffled fits finished. The original fits retained
four prohibited centroid features and are excluded; corrected inputs contain
1,064 features. Original-count checks and a public-workbook reconciliation preserve
coverage. A legitimate zero-row source shard required a recorded implementation
repair; its failed attempt remains archived.

| View | Full-guide mean MRR | Full-guide median MRR, training-median scaling |
|---|---:|---:|
| Mitotic, 950 test genes | 0.047518 | 0.044256 |
| Interphase, 994 test genes | 0.234113 | 0.227001 |

Full means are the strongest of twelve simple methods in both arms. Four neural
seeds score 0.050422-0.055476 in mitotic cells and 0.143636-0.148017 in interphase.
Neither arm meets the fixed 0.02 gain rule with positive paired/joint intervals.
Interphase's four paired intervals are wholly below zero against the full-data
baseline. The comparison uses 20,000 gene-level resamples, not cells as replicates.

There is a favorable **BUB1B interphase signal**: full-mean own-target ranks are
1, 3, 3 and 2 among 994 genes, with 859/1,219/839/1,435 cells per guide. MAD2L1 and
TTK are competing matches, so this is not uniquely BUB1B-specific. The fourth guide
ranks 836 with medians under mean-derived scaling, 9 with training-median scaling,
and 770-788 across neural seeds. Its cross-plate full-mean ranks range from 2 to
520; plate cohorts contain 991-994 genes. Aggregation and acquisition sensitivity
prevent treating pooled agreement as uniform robustness. Mitotic counts
11/15/11/25 leave one eligible guide where two are required: its retrieval is missing.

The equal-information sensitivity favors learning: under the same 128-cell cap,
interphase means score 0.093093, below every neural seed. This separates sampling
volume from representation and does not rescue the failed full-data gain rule.
Complete-guide medians and matched-sample means are exploratory additions. Post-hoc
plate-only BUB1B ranks are 138/907/397/119; simple plate proportions do not reproduce
the favorable morphology ranks, but this does not exclude batch effects. A separately
specified single-plate-only control has no eligible genes and stays unavailable.
The cross-plate encoder still trained on other genes from every plate.

**Decision:** retain simple imaging as an assay-development lead, test the unstable
guide with independent restoration and batch-aware collection, and measure useful
function before drug matching. All twelve baselines, seeds, query directions,
missing states and timing declarations remain in the
[complete comparison](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-optical-v36.md)
and [six falsification records](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-optical-register-v36.json).

The public Funk HeLa data are transformed, aneuploid and lack functional p53.
The source classifier separates interphase and mitotic cells, and the source
normalizes measurements within each class. A changed class fraction may reflect
entry, exit, loss or classification. BUB1B-specific classification error is
unmeasured. Fixed-cell images cannot establish all-enrolled daughter survival or
non-cancer rescue. Source medians motivated an added exploratory median baseline;
it does not reproduce the authors' full PHATE pipeline.
[Study](https://doi.org/10.1016/j.cell.2022.10.017),
[dataset](https://doi.org/10.7910/DVN/VYKTI5),
[method reread](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-optical-interpretation-v35.md).

## 4. The experiment that can change the decision

**Qualify the model.** The proposed first comparator is engineered hTERT-RPE1,
a nonmalignant but immortalized cell system, not a renal/muscle surrogate or an
available patient line. Its retained expression specificity is weak. Availability,
clone feasibility and functional qualification remain unconfirmed; no completion
before the submission deadline is promised. Compare wild type, mock editing, each
single allele, cis, trans and corrected derivatives. Verify engineered
genotype/phase, endogenous RNA/protein and comparable cell states. Establish a
reproducible functional deficit with an independent perturbation/restoration method;
include expression-matched correction, seed controls for RNAi and a method that
avoids the same DNA-cutting event. Measure editing stress and survivor selection.
Count independent guide designs and source wells separately from profiles.
Failed assay controls hold inference; absent or imprecise effects do not establish
clinical normality. Renal and muscle contexts require their own qualification.

The minimum panel measures residual BUBR1, checkpoint maintenance, unchallenged
division/segregation and later useful output/recovery. The v41 literature supplement
adds BUBR1/MAD2/ZW10 corona localization, MCC/APC/C engagement, mitochondrial
integrity and proteostasis/ubiquitin-proteasome stress. Mitotic index alone confounds
entry, arrest, slippage and death; localization or protein abundance alone does not
prove complex checkpoint function.
SIRT2 overexpression is a separate, pleiotropic perturbation, not an independent
BUBR1-specific restoration control. Site-specific assays require validated reagents
and controls; their availability is unknown. A precise valid negative can close
the tested prerequisite in that model. Unknowns remain HOLD, not a negative result.

**Test joint treatment.** Once a branch qualifies, compare deficit + vehicle,
deficit + everolimus, corrected + vehicle and corrected + everolimus. Include an
assay-qualified positive control and interpretable orthogonal pathway perturbation.
Verify compound identity. Randomize independently treated cultures within clone,
day and plate blocks; blind scoring. Cells are nested observations. Model crossed
clone/day effects or justify aggregation; multiple clones do not create donors.
Measure engagement, graded exposure, useful function and injury in the same context.
Orthogonal disagreement limits mechanism attribution without automatically disproving
a drug-specific effect.

**Follow every enrolled unit.** Enroll before exposure. Retain accurate and erroneous
first divisions, death, persistent arrest, slippage and tracking loss separately.
Then measure daughter fate, sustained useful output and recovery through a locked
window justified by model division rate and untreated recovery. Fixed-cell class
fractions and selected survivors cannot replace these observations. Mature,
non-dividing tissue needs a qualified lineage-function endpoint. Flux reporters need
pH/expression/interference controls and orthogonal cargo turnover; ATP alone is not
viability. Tumour killing needs its own subtype and deficient-normal controls.
[Growth-rate methods](https://doi.org/10.1038/nmeth.3853),
[flux reporter](https://pmc.ncbi.nlm.nih.gov/articles/PMC3121655/).

A **synthetic example, not experimental data**, shows why the denominator matters.
With 100 enrolled cells per arm, errors among completed divisions fall from 20/80
(25%) to 5/45 (11.1%), but accurate viable output falls from 60/100 to 40/100.
A better surviving-cell ratio can conceal worse output. The executable example
retains death, arrest and missing tracks; missingness bounds do not replace sampling
uncertainty.

**Confirm independently.** Use pilot performance to fix meaningful benefit,
acceptable injury, follow-up, missingness rules, multiplicity and sample size before
independent confirmation. Replicate across backgrounds and culture days. A
genotype-specific claim needs an interaction contrast; useful benefit shared with
corrected cells need not be rejected. Current data justify no numerical benefit or
injury margin, power estimate, laboratory budget or clinical timeline.

| Evidence state | Decision |
|---|---|
| Failed assay/control or changed confirmation plan | Invalid; hold inference. This does not refute biology. |
| Unknown mechanism or imprecise effect | Hold advancement. A valid test rejecting branch eligibility stops that branch. |
| Valid interval excludes meaningful benefit | Stop the tested claim. An interval spanning the target is inconclusive. |
| Injury exceeds the prespecified bound | Stop despite apparent benefit. |
| Unmatched or unknown exposure | Block translational promotion. |
| All requirements met | Preclinical review only. |

Benefit must clear a justified threshold; injury intervals must exclude unacceptable
harm. Nonsignificance is not safety. Whole-blood trough, total-plasma peak, nominal
culture concentration and unbound tissue exposure are not interchangeable. Match
analyte, matrix, free fraction, schedule and sampling context. All clinical exposure
margins and actual measurements remain null; the executable rule returns HOLD.
[Decision contract](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-decision-contract-v21.json),
[validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v21.md),
[exposure ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-exposure.json).

## 5. Contribution, patient relevance and reuse

The specific contribution is an inspectable connection between evidence states,
all-enrolled outcomes and the next laboratory decision. The demo exposes the exact
inputs and reasons for HOLD or STOP; the handoff states what measurement can change
them. This integration is the innovation claim to assess. The component methods are
established, and broad novelty or superior clinical performance is not claimed.

The useful deliverable is a decision that another lab can test. A validated
allele-to-function assay could improve mechanistic characterization of BUB1B
variants; diagnostic use would still require calibrated controls and independent
validation. A valid negative result could stop an unsupported drug route before
scarce material is spent on it. A positive joint-treatment result could justify
further preclinical work. Neither outcome establishes benefit for this child.

The [laboratory handoff](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-lab-handoff-v40.md)
sequences endogenous mechanism, one qualified non-cancer model, joint intervention
and independent confirmation. It identifies assay capabilities and decisions without
inventing budgets, sample sizes or timelines. Muscle contraction/recovery and renal
transport/barrier function are candidate assay families requiring their own
qualification, not established surrogate endpoints. The first work uses engineered
models and existing public evidence; it does not request a new family sample.
Useful function, all-enrolled outcomes and injury take priority over a favorable
biomarker. This design has not been co-developed with the family.

The **Every enrolled cell** offline
[demo](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-demo-v37.html)
lets a reviewer inspect the actual unknown state, select teaching cases, explore
missing observations and download the exact input/reason. It makes the existing
policy usable without reading code. The schema, standard-library replay and
[small community kit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-community-kit-v37.md)
require no subject files, GPUs, model weights, keys or network access.

The teaching set contains **17 synthetic cases and one actual unmeasured state**.
A deliberately incomplete benefit-only rule advances 11 cases held or stopped by
the full policy; adding only viability still advances 9. These are author-selected
failure modes, not a representative, held-out or external clinical benchmark.
Python and JavaScript agree on 83 valid checks, and both reject 12 invalid records.
This verifies implementation behavior; it does not validate the policy or its
scientific inputs. Synthetic margins cannot qualify a real experiment. The
component methods are established; therapeutic novelty, general superiority,
external adoption and patient benefit remain untested.

Review the examples, then the full scientific record:

```bash
uv run --no-project python scripts/track2_demo_v37.py
uv run --no-project python scripts/track2_public_review_v41.py
```

The reusable elements are the evidence states, provenance, schema, all-enrolled
outcomes and explicit stop rules. Other tissues, genotypes and diseases need new
mechanism, assay, functional endpoint, exposure and safety qualification. Heavy
model fitting is optional for reviewing the retained evidence. The laboratory
constraints are model development, live imaging, functional assays and independent
replication. No measured community adoption, specialist review or independent
biological review is claimed.

Literature work was targeted, not systematic. Reading depth ranges from abstracts
to selected primary passages; failed retrievals are not negative evidence. The
v35 addition rereads Funk methods and selected Cohen-Sharir results/methods. The
v39 review rechecked the primary mouse discussion and found no new direct
selected-pair treatment validation in four bounded search results. Earlier source
adjudications, registry amendment history, the yeast TORC1/cohesin hypothesis and
Balnis units conflict remain in the linked records. Endogenous effects, tissue
response and clinical margins remain unresolved. V41 adds a bounded public-source literature refresh to those retained sources;
it changes readout design, not any drug disposition. It adds no biological experiment.

## 6. Competition delivery

The October 19 refresh checked seven official files at
`60e1c30e337ce6fe01813040dbe49979eb8c50aa` and 30 public discussions with 84 visible
comments. Only new discussion 31 differs from the preceding capture; its unanswered
participant question does not change requirements. Unchanged material retains its
previous review. Rigor, impact, innovation and scalability carry 35%, 25%, 25% and
15%. Track 1 perfect-score recognition is consortium authorship; it does not
establish drug efficacy. Track 2 placements and the separate Innovation Prize are
organizer decisions, with no estimated winning probability.
[Current source review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v42.md),
[preceding v39 capture](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v39.md)
and [announcement 28](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/28).
The anonymous v42 refresh found the seven official files unchanged and public discussion at 31 threads/89 visible
comments. An 11:49 UTC live recheck found the same Space revision and the same 31
listed public discussions; no new organizer requirement appeared. Thread 32 permits a clearly labeled published-paper example in the pitch while
the written report covers the challenge case. The current non-genomic 367-word script
remains compliant; no rewrite is required. Thread 31 documents a Synapse alternative
for teams constrained from GitHub; our public-first GitHub route remains selected.

Submit by **October 24, 23:59 UTC**: a participant-named PDF/Markdown report,
GitHub URL and three-minute YouTube/Vimeo video. Three entries are allowed; only
the latest is reviewed. Quota remains unknown. Recording, measured runtime,
hosting, owner/provider review, live-portal checks and receipt remain open.
Delete the data and confirm to **cnb@sagebase.org by November 23**; earlier frozen
dates/recipients are superseded. Winners are announced December 18. No upload,
contact or deletion occurred. [Readiness](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v41.md).

**Distribution scope remains unresolved.** Challenge CC BY requirements may conflict
with linked historical AF3/non-AVI Atlas output terms. This report/pitch omit those
numerical outputs and figures and preserve notices; that does not resolve licensing
or relicense earlier materials.

## 7. Methods answers and AI disclosure

These answers map to B7-B17 of the official template. B9 is required; other answers
are recommended. The filled workbook preserves the questions and comments on its
stale one-entry instruction; live instructions allow three entries.

**B7: Participant.** jvv7, individual entry; no institutional affiliation asserted.

**B8: Identification approach.** Connect the retained BUB1B pair to conditional
mechanisms; assess approved drugs, contrary evidence, exposure and deficient-normal
safety. Everolimus remains an optional probe, HCQ reserve; all eleven dispositions persist.

**B9: AI provider, plan and handling.** OpenAI Codex/API assisted code, literature research, synthesis,
editing and reviews. The owner attests no training on content; account settings and
zero retention were not independently audited. The self-hosted Firecrawl bridge
previously used Fireworks-hosted GLM with owner-confirmed API credits for public
literature. Fireworks training/retention remain unverified; local retrieval does not
imply local inference. Google DeepMind AlphaGenome Atlas supplied precomputed API
and downloaded outputs, not on-demand inference. Its service/output terms apply.
Earlier ColabFold alignment search received public wild-type protein only; service
training/retention remain unverified.

Owner-hosted models used public references and permitted derived substitutions:
ESM-1v/ESM-2, ESMC 300M/600M/6B, ESM3-open 1.4B, Boltz-2, AlphaFold2, AlphaFold3,
ESMFold2 and Evo2 7B/20B/40B. Later work on eight owner-host H100s added public
LINCS/RNAi/CRISPR statistics, ESMC/ESM3 sensitivity inference and Perturb-seq
reanalysis. V29 executed ProteinMPNN through Anthropic's uplifting-biomolecular-modeling
toolkit at `f4f62fa6592ae4938d49b1757bea0cfeff9f468e`, following review-only use in
v27. Related checkpoints and predicted backbones are not independent biological
replicates. Numerical/stock pilots, failed attempts, CPU checks and source/QC
limitations remain in the linked campaign records.

V35 removed four image-position features from the public HeLa optical inputs.
V36 completed 16 corrected MLP fits, plate and median analyses against twelve
baselines per arm. The purpose-built MLP is a benchmark, not a foundation-model
claim. Shuffled labels, complete counts and CPU/archive replay accompany it.
Exploratory and post-hoc controls retain their timing; coordinate-contaminated fits
and the empty-shard failure stay preserved. CPU/I/O stages and bursty kernels
prevent interpreting worker counts as continuous GPU use. No protected subject
input was transferred; all remote campaign work stayed under the owner's `~/v`.
Carbon annotation was reviewed and deferred as irrelevant to functional rescue.

V37 adds an offline synthetic teaching demo, Python/JavaScript checks and an
own-voice recording guide. V39 adjudicates the owner's rehearsal; v40 clarifies the
presentation order and derives recording counts and cue rates from the script. V41
adds the current public literature readouts, and v42 updates this video destination text
without claiming that a recording has been made. These revisions use Codex-assisted
editing and local rendering. No
additional hosted model provider, new GPU model campaign or biological experiment
was used. Raw subject reads, VCF records and clinical narrative stay local. Unknown
settings are not attested. Historical AF3-derived materials retain
[AlphaFold3 Output Terms](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md),
the [Legally Binding Terms notice](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt),
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
V35 preserves the coordinate-policy violation, excluded original fits, corrected
reruns, full-data and matched-sample baselines, missing mitotic BUB1B retrieval,
class-selection and delayed-fate alternatives. Exploratory analyses retain their
timing and cannot rescue a failed primary gate.

**B12: Public versus proprietary evidence.** Drug/target evidence is public; earlier
genetic reasoning used gated challenge data. No proprietary drug-response data were
supplied. The project is not wholly public-input-only.

**B13: Public sources.** Primary papers, Europe PMC/PubMed, ClinicalTrials.gov,
DailyMed, NIH GEO/LINCS, Replogle/Weissman Figshare data, CLUE metadata, PubChem/NCATS, UniProt/PDB/model resources and official challenge pages; exact sources are
in the ledgers. V33 also uses the public Funk HeLa screen and Harvard Dataverse.
Search/model services are tools, not independent evidence.

**B14: Gated sources.** Organizer WGS and phenotype informed earlier local analysis
under signed terms. Only permitted derived findings appear here; no other proprietary
experimental, clinical or drug/target dataset is claimed.

**B15: Mechanism.** BUBR1 checkpoint/attachment dysfunction is established at gene level.
Pair-specific function and phase are unknown. Everolimus tests conditional downstream
mTORC1 hypotheses; both branches require qualification. The carrier-muscle mouse
signal cannot establish this pair's pathway state. NAD/SIRT2 is a competing
residual-protein hypothesis with opposing site/context evidence, not a promoted drug.

**B16: Effort.** Work began September 8. Total person-hours, GPU time and API/lab costs
are unaggregated. Any reported CPU review time covers that command only; no overall
speedup, budget or clinical timeline is claimed.

**B17: Method abstract (under 500 words).**

We propose qualifying endogenous BUB1B function before advancing a drug hypothesis.
Everolimus is a worked conditional branch, on HOLD for missing prerequisites;
no drug earns rescue priority. Its mouse rationale comes from heterozygous
BubR1+/X753 skeletal muscle and sarcopenia, not demonstrated compound-pair rescue.
The competing NAD/SIRT2 route has a proximal stability mechanism and male-biased
genetic survival evidence, alongside opposing site/context findings. Neither route
establishes efficacy, phase or clinical exposure margins. The proposed first
comparator is engineered hTERT-RPE1; availability and qualification remain unconfirmed.

Falsification narrowed the proposal. ProteinMPNN failed expanded functional-control
ordering in all 24 comparisons. Expression studies retain partial attribution
signals but do not measure rescue after joint drug-plus-deficit treatment.
Corrected public HeLa imaging places BUB1B among the top three genes for four
interphase guides using full means; one guide varies by method and plate.
Neither optical arm meets the required neural gain, and mitotic BUB1B coverage is
insufficient. Favorable and adverse findings remain available for review.

The proposed experiment qualifies endogenous single-allele, cis/trans and corrected
models with independent perturbation/restoration, then tests drug and deficit
together. Randomized, blinded cultures provide biological replication; nested
cells provide fate and functional measurements. Enroll before exposure, retain
all outcomes, and measure daughter survival, sustained function and recovery.
Independent confirmation requires justified benefit/injury margins and matched
exposure. Injury stops advancement despite apparent benefit; unknown evidence
holds it. All-pass permits preclinical review only.

Our offline Every enrolled cell demo and small public kit make these distinctions
inspectable without patient data, models or GPUs. Seventeen synthetic cases and
the actual unmeasured state illustrate incomplete shortcuts and missingness;
they test software behavior, not clinical performance. A validated assay could
support mechanistic understanding, while a valid negative result could stop an
unsupported route. New contexts require fresh biological qualification. No wet-lab
experiment, family co-design, external adoption or therapeutic efficacy is claimed.

The owner's rehearsal was adjudicated against primary sources. Genotype and
sex qualifiers were accepted; mouse K243/human K250 numbering and the proposed
generic K243R rescue control were corrected. This is not independent outside review.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
