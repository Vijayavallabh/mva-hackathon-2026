# Testing everolimus for useful cell function in BUB1B-associated MVA

Track 2 research proposal | jvv7 | 19 October 2026 | v36

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

We propose testing everolimus, an approved mTORC1 inhibitor, in a functionally
qualified non-cancer BUB1B model. It remains an optional mechanistic probe.
No rescue-priority drug is supported. The next useful result is a controlled
measurement of function, injury and recovery after joint drug-plus-deficit exposure.
Selected-pair efficacy, trans phase and clinical exposure margins remain unresolved.
No wet-lab experiment has been performed; no treatment or dose for the child is proposed.

## 1. Establish the mechanism before exposure

The retained hypothesis is BUB1B p.Leu737Ter / p.Asn1002Lys. BUB1B encodes BUBR1,
which contributes to spindle-checkpoint and chromosome-attachment control. Biallelic
disruption is an established MVA mechanism. This pair's endogenous RNA/protein effects
and residual function remain unknown. Engineered single-allele, cis and trans models
can test alternatives; they cannot establish the subject's phase. Competition scores
do not establish drug response. [Hanks](https://doi.org/10.1038/ng1449),
[Suijkerbuijk](https://doi.org/10.1158/0008-5472.CAN-09-4319).

A different BubR1-mutant mouse context showed increased mTOR-associated
phosphoproteins in muscle, without testing rapalog rescue. The excess might be
adaptive. Everolimus could modify a downstream consequence; it does not replace
BUBR1 or establish chromosome repair. Specified TSC indications establish approval
and known pharmacology, not MVA efficacy or safety.
[Mouse study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781),
[label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2).

Lock one branch before exposure: **A**, excess mTOR-associated activity with a
functional deficit; or **B**, impaired dynamic autophagic flux and regeneration,
with separate mechanistic controls. Neither branch is established for this pair.
Do not switch branches after seeing results. Branch B's motivating hypercapnia
study has conflicting ex vivo units, 10 mM versus 10 micromolar, in related
supplemental methods. Both values remain quarantined; the 1,000-fold discrepancy
cannot set a concentration. [Balnis](https://doi.org/10.1172/jci.insight.182842),
[supplement](https://insight.jci.org/articles/view/182842/sd/pdf/render/1).

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
supply non-cancer rescue. [ARST1431](https://doi.org/10.1016/S1470-2045(24)00255-9),
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
niacin rescue of this pair. Residual useful protein and deficient-normal function
must be tested before promotion. The
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

**Qualify the model.** Compare wild type, mock editing, each single allele, cis,
trans and corrected derivatives in an editable non-cancer context. Verify engineered
genotype/phase, endogenous RNA/protein and comparable cell states. Establish a
reproducible functional deficit with an independent perturbation/restoration method;
include expression-matched correction, seed controls for RNAi and a method that
avoids the same DNA-cutting event. Measure editing stress and survivor selection.
Count independent guide designs and source wells separately from profiles.
Failed assay controls hold inference; absent or imprecise effects do not establish
clinical normality. Renal and muscle contexts require their own qualification.

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

## 5. Contribution, reuse and limits

The contribution is a reproducible path from an approved-drug hypothesis to a
specific biological decision, with explicit counterevidence and all-enrolled
benefit/injury outcomes. The component methods are established; superiority over
another framework and therapeutic impact remain untested. A valid negative result
can stop the route in the tested context; a positive result supports further
preclinical review.

Review public consistency without subject files, GPUs, SSH, API keys or model weights:

```bash
uv run --no-project python scripts/track2_public_review_v36.py
```

Heavy computation is needed to reproduce model fitting, not to inspect the retained
results. New tissues/genotypes require fresh mechanism, assay, exposure and safety
qualification. Model development, imaging, function assays and independent replication
are the laboratory constraints. Start with one qualified context and fund the next
stage only after its decision. The public records retain failed attempts and missing
results; no specialist or independent biological review is claimed.

Literature work was targeted, not systematic. Reading depth ranges from abstracts
to selected primary passages; failed retrievals are not negative evidence. The
v35 addition rereads Funk methods and selected Cohen-Sharir results/methods. Earlier
source adjudications and the yeast TORC1/cohesin hypothesis remain in the linked
records. Registry amendment history, the Balnis units conflict, endogenous effects,
tissue response and clinical margins remain unresolved.

## 6. Competition delivery

The October 19 refresh checked seven official files at
`60e1c30e337ce6fe01813040dbe49979eb8c50aa` and 29 public discussions with 83 visible
comments. Four new/changed comments were reread; unchanged material retains its
previous review. Rigor, impact, innovation and scalability carry 35%, 25%, 25% and
15%. Track 1 perfect-score recognition is consortium authorship; it does not
establish drug efficacy. Track 2 placements and the separate Innovation Prize are
organizer decisions, with no estimated winning probability.
[Source review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-requirements-review-v33.md),
[announcement 28](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/28).

Submit by **October 24, 23:59 UTC**: a participant-named PDF/Markdown report,
GitHub URL and three-minute YouTube/Vimeo video. Three entries are allowed; only
the latest is reviewed. Quota remains unknown. Recording, measured runtime,
hosting, owner/provider review, live-portal checks and receipt remain open.
Delete the data and confirm to **cnb@sagebase.org by November 23**; earlier frozen
dates/recipients are superseded. Winners are announced December 18. No upload,
contact or deletion occurred. [Readiness](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v36.md).

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
V35 corrects four image-position features in the public HeLa optical campaign.
V36 completes both optical arms, with 16 corrected 3,000-step fits, 16 plate
workers and 16 complete-guide median workers on the same eight H100s. The
purpose-built MLP is a benchmark, not a state-of-the-art foundation-model claim.
Twelve baseline methods per arm, shuffled labels, independent CPU reductions,
public-workbook counts and local archive replay accompany the results. The
matched-sample and median comparisons are exploratory; plate-only/within-plate
controls are post-hoc. Original coordinate-contaminated fits and the legitimate
empty-shard execution failure remain preserved. CPU/I/O stages and brief GPU
kernels prevent interpreting worker counts as continuous GPU saturation.
Carbon annotation was reviewed and deferred because it does not answer the
functional-rescue question. This v36 integration used Codex/API-assisted editing
and offline rendering. No additional hosted model provider was used. Raw subject reads, VCF records and clinical
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
mTORC1 hypotheses; both branches require qualification.

**B16: Effort.** Work began September 8. Total person-hours, GPU time and API/lab costs
are unaggregated. Any reported CPU review time covers that command only; no overall
speedup, budget or clinical timeline is claimed.

**B17: Method abstract (under 500 words).**

We propose a qualified everolimus experiment for non-cancer function in BUB1B-associated
MVA. This approved mTORC1 inhibitor remains an optional mechanistic probe; no drug
earns rescue priority. Pair-specific endogenous effects, phase and clinical exposure
margins remain unresolved. Different-model mTOR findings motivate the hypothesis;
functional counterevidence requires direct benefit, injury and recovery measurements.

ProteinMPNN fails expanded functional-control ordering in all 24 comparisons.
RNAi/CRISPR analyses retain a favorable HT29 attribution lead but one guide and
tumour context limit transfer. MCF7 has no qualified BUB1B query; adjusted everolimus
reversal weakens while MTOR matching remains first. Public RPE1 Perturb-seq shows
a repeatable BUB1B response with weak own-target retrieval. One shared guide pair,
selected controls and reused splits limit attribution. These separate perturbations
do not measure rescue after joint drug-plus-deficit treatment.

Corrected public HeLa imaging places BUB1B among the top three genes for all four
interphase guides using simple full profiles. Neither arm passes the practical
neural-gain rule. Mitotic BUB1B retrieval is missing for coverage. This favorable
morphology lead requires acquisition, aggregation and functional qualification;
it does not establish non-cancer rescue.

Qualify endogenous single-allele, cis/trans and corrected models using independent
perturbation/restoration, seed and editing-stress controls. Lock one pathway branch,
then randomize and blind the joint-treatment experiment against each perturbation
alone. Measure useful function, accurate first division, all enrolled cell fates,
daughter survival and sustained output through prespecified follow-up and recovery.
Early relative sensitivity can reverse; a favorable snapshot is insufficient.

Independent confirmation needs justified benefit/injury margins and matched exposure.
Invalid assays hold inference; imprecision holds advancement. Valid evidence excluding
meaningful benefit stops that claim; injury stops advancement despite apparent benefit.
All-pass permits preclinical review only. HCQ remains reserve. Public CPU checks
support review and reuse; no biological experiment, clinical efficacy or recorded
video is claimed.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
