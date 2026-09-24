# Can everolimus improve useful cell function in BUB1B-associated MVA?

**Track 2 research proposal · jvv7 · 24 September 2026 · v17**

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

## Proposal at a glance

**Candidate:** everolimus, an existing market-approved mTORC1 inhibitor, proposed for
an experimental test of downstream non-cancer tissue function. **Question:** can a
qualified BUB1B-deficient model gain useful function without losing accurate division,
viability or regenerative capacity? **First decision:** establish a reproducible
endogenous phenotype and the relevant mechanism before drug testing. **Current result:**
no rescue-priority drug; everolimus remains an optional mechanistic probe. No wet-lab
experiment, selected-pair efficacy, confirmed trans phase or clinical exposure margin
is available. This is a hypothesis for investigation, not a treatment recommendation.

The contribution is an experiment designed to distinguish useful functional improvement
from selection of surviving cells, pathway-marker suppression or tumour killing. It can
reject the candidate as well as support further preclinical study. The accompanying
code makes the evidence checks and decision rules inspectable without rerunning the GPU
campaign. Clinical action would require evidence well beyond this proposal.

## 1. The variant-to-mechanism-to-drug chain

The retained genetic hypothesis contains BUB1B p.Leu737Ter and p.Asn1002Lys. BUB1B encodes
BUBR1, which contributes to spindle-checkpoint and chromosome-attachment control.
Biallelic BUB1B disruption is an established MVA mechanism; the selected pair's endogenous
RNA/protein effects, residual function and trans phase remain unconfirmed. Engineered
single-allele, cis and trans models test alternatives; they cannot resolve the subject's
phase. Neither competition performance nor a computational prediction supplies that
missing evidence. [Hanks](https://doi.org/10.1038/ng1449),
[Suijkerbuijk](https://doi.org/10.1158/0008-5472.CAN-09-4319).

The mechanistic bridge is **conditional**. A different BubR1-mutant mouse context showed
increased mTOR-associated phosphoproteins in muscle, without testing rapalog rescue.
This motivates asking whether a relevant non-cancer model has excess pathway activity
and a functional deficit. Excess signaling could be adaptive, so reducing it is not
itself success. Everolimus inhibits mTORC1 downstream; it does not replace BUBR1 or
establish chromosome repair. Its existing oncology and TSC indications establish an
approved medicine and known pharmacology, not efficacy or safety for MVA.
[Mouse study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781),
[official label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2).

Two hypotheses must be qualified separately. **Branch A** requires excess mTOR-associated
activity plus a functional deficit. **Branch B** requires a relevant dynamic-autophagic-
flux and regenerative-function deficit plus its own mechanistic controls. Neither is
established for the selected pair. A failed A result cannot be relabeled B after seeing
outcomes. The different-disease hypercapnia study motivating B contains unresolved ex
vivo concentration units: 10 mM versus 10 micromolar in related supplemental methods.
The 1,000-fold discrepancy is quarantined; neither value becomes a design concentration.
[Balnis](https://doi.org/10.1172/jci.insight.182842),
[supplement](https://insight.jci.org/articles/view/182842/sd/pdf/render/1).

## 2. Why test this hypothesis—and what argues against it?

The evidence supports a bounded question, not a comparative rescue ranking.

| Observation | What it contributes | What it cannot establish |
|---|---|---|
| Different BubR1-mutant mice showed increased mTOR-associated phosphoproteins in one muscle/genotype comparison. | A mechanistic question that can be measured before perturbation. | Rapalog rescue, the selected pair's pathway state or clinical benefit. |
| Everolimus improved selected muscle-mass outcomes in aged rats; force benefit was not established. | Compound-specific evidence that a functional investigation is reasonable. | Restoration of useful MVA muscle function. [Joseph](https://doi.org/10.1128/MCB.00141-19) |
| Everolimus reduced BUBR1 in late-passage human stromal cells; early-passage response differed. | Direct compound-specific reason to monitor BUBR1, chromosome fidelity and cell state. | That protein loss alone proves clinical harm. [Goutas](https://doi.org/10.1016/j.redox.2023.102701) |
| Rapamycin impaired injured-mouse muscle regeneration in a separate study. | Test regeneration and recovery, not just an on-treatment marker. | Interchangeable effects across compounds, doses and tissues. [Ge](https://doi.org/10.1152/ajpcell.00248.2009) |
| ARST1431: adding temsirolimus to VAC/VI did not establish an event-free-survival benefit: HR 0.86, 95% CI 0.58–1.26, p=0.44; 297 evaluable intermediate-risk RMS participants. | A randomized tumour boundary against a broad rapalog-success narrative. | Non-cancer everolimus rescue, or exactly zero effect in every context. [Trial](https://doi.org/10.1016/S1470-2045(24)00255-9) |

Published favorable safety observations also constrain rejection: uncontrolled pediatric
TSC growth follow-up and a pediatric transplant-regimen safety comparison do not support
inevitable developmental harm. They also do not establish safety in MVA or isolate an
everolimus effect. Renal, infection, marrow/metabolic, wound-healing and interaction
risks remain relevant. Additional clinical laboratory or treatment-history records are
not available in the challenge release; no individualized suitability is inferred.
[Label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[transplant trial](https://doi.org/10.1001/jama.2025.14338),
[organizer clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/14).

Alternatives face the same tests. HCQ remains reserve: lysosomal/flux signals and tumour
activity do not establish deficient-normal safety or monotherapy benefit. Pralatrexate
is a tumour-only horizon restricted to relevant fusion-positive RMS models, not a
constitutional rescue proposal. Temsirolimus supplies a clinical benchmark. Entinostat,
vorinostat, niclosamide and posaconazole remain deprioritized; PP2A tools, senolysis and
readthrough directions remain excluded under the current evidence. No combination is
proposed, and no candidate inherits priority because a competitor failed. The complete
[63-source, 11-decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json) retains the rationale and sources
for every disposition, including approval/indication and exposure limitations.

## 3. A staged experiment with a decision at each stage

**Stage 1 — qualify the model and the question.** Begin with an editable non-cancer
context capable of reporting the relevant endogenous phenotype. Compare wild type,
mock editing, each single allele, cis, trans and corrected derivatives. Verify engineered
genotype/phase, endogenous RNA/protein and cell-state comparability. Separate attachment,
checkpoint activation/maintenance/silencing, viable accurate daughter production and
lineage function. Published 731X complementation cannot assign a phenotype to L737Ter,
and ectopic cDNA can bypass RNA decay. Extend to renal- or muscle-relevant models only
when that context is qualified. If no reproducible relevant phenotype exists, hold drug
advancement and revise the model; absence of a result is not evidence of clinical normality.

**Stage 2 — run a blinded benefit/harm probe.** Lock A or B eligibility before exposure.
Use vehicle, an assay-qualified positive control, corrected-model comparisons and an
interpretable orthogonal pathway perturbation. Randomize within clone/day/plate blocks;
blind scoring. Measure graded exposure and time-matched engagement, useful function,
BUBR1/chromosome fidelity and delayed recovery. Orthogonal disagreement limits mechanism
attribution rather than automatically erasing a drug-specific effect. A mechanistic probe
without a clinical exposure bridge must remain exploratory.

**Stage 3 — independently confirm only a worthwhile result.** Use pilot performance to
fix the minimum meaningful benefit, maximum acceptable injury, outcome definitions,
missingness analysis, multiplicity handling and sample size before new confirmatory
observations. Clone/background and culture-day replication are required; many cells or
technical wells are not independent biological replicates. No current assay data justify
numerical margins, a power claim, a calendar promise or a laboratory budget.

| Decision-changing question | Required observation | Consequence |
|---|---|---|
| Is the phenotype and selected branch reproducible? | Endogenous/corrected comparisons plus functional and mechanistic qualification. | Unknown: hold. Failure of the prespecified branch: stop that branch. |
| Is useful output improved? | Prespecified function and accurate viable output across enrolled units, with independent replication. | A marker-only or survivor-only improvement cannot advance. |
| What is the cost to deficient-normal tissue? | Division, viability, chromosome fidelity, regeneration and later recovery within prospectively justified injury bounds. | Failed safety stops advancement despite apparent benefit. |
| Is the exposure claim supportable? | Same analyte, matrix, free fraction, schedule and sampling context, measured or defensibly bounded. | Unmatched or unknown exposure blocks translational promotion. |
| Would a repeat test change the conclusion? | Locked independent confirmation with appropriate uncertainty and missingness bounds. | Inconclusive: hold. All requirements met: preclinical review only. |

Whole-blood trough, total-plasma peak, nominal culture concentration and unbound tissue
exposure are not interchangeable. All clinical exposure margins remain null. No dose,
therapeutic ratio or treatment schedule for the child is proposed. Full operational
requirements are in the [validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v15.md) and
[exposure ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-exposure.json).

## 4. Measure useful output, not selected survivors

Enroll cells before exposure and retain accurate division, erroneous division, death,
persistent arrest, slippage and tracking loss as separate outcomes. Follow daughters
and recovery. For mature non-dividing tissue, measure qualified lineage function rather
than forcing a proliferation endpoint. Tumour killing is a separate objective requiring
documented tumour subtype and matched deficient-normal controls; it cannot substitute
for non-cancer functional improvement.

A deliberately **synthetic example, not experimental data**, illustrates the trap:
among 100 enrolled cells per arm, errors among completed divisions fall from 20/80
(25%) to 5/45 (11.1%), while accurate viable output falls from 60/100 to 40/100.
Reporting only the first ratio would conceal a worse functional outcome. The executable
counterexample retains deaths, arrest and missing tracks. Missingness bounds do not
replace sampling uncertainty.

Qualify flux reporters against pH, expression, optical interference and cell loss, with
orthogonal cargo turnover. Compare tumour and normal viable counts from baseline over
time; use growth-rate-aware sensitivity only when untreated controls grow sufficiently.
ATP/metabolic signal alone is not a viability endpoint. These controls test whether an
apparently promising result is an assay artifact.
[Growth-rate methods](https://doi.org/10.1038/nmeth.3853),
[flux reporter](https://pmc.ncbi.nlm.nih.gov/articles/PMC3121655/).

## 5. Value to MVA research and a practical reuse path

**Potential impact:** a supported result could justify further investigation of useful
function; a well-measured negative or harmful result could prevent pursuing that route
in the tested context. Neither outcome is guaranteed. The first deliverable to a future
laboratory is a model-qualification decision and interpretable evidence, not a dose.

**Innovation:** the contribution is the integration of genotype/phase alternatives,
active falsification, all-enrolled cell-fate accounting and explicit benefit/harm/exposure
gates. We do not claim to have invented mTOR biology, these drugs, or these individual
methods, or to have demonstrated superiority over another framework.

**Scalability has two distinct levels.** Reviewers can reproduce the public evidence
consistency checks on a CPU without subject files, API keys, SSH or model weights:

```bash
uv run --no-project python scripts/track2_public_review_v17.py
```

That command checks the current requirements record, all-discussion coverage, archived
control sensitivity, conservative decisions and slide/script alignment. It is not a
rerun of model inference or proof of a biological claim. Full model plans, complete
matrices and failed attempts remain in the separately labelled technical history.

Laboratory reuse begins with one qualified context and one branch. Use the same claim
schema, outcome taxonomy and stopping logic for a new genotype or tissue, but requalify
its mechanism, assays, exposure and safety. The model panel, imaging/cell-function
assays, exposure quantification and independent replication are the resource bottlenecks.
A planning example of seven groups × three clones × three days × two conditions gives
126 culture allocations before concentrations or technical replicates; it is arithmetic,
not a sample-size recommendation, available cell collection or power estimate. Stage
funding and work by the preceding decision rather than commit to a broad drug screen.

The official weights are rigor 35%, impact 25%, innovation 25%, scalability 15%.
Sections 1–4 address rigor; the first paragraph here addresses impact; the integrated
experiment addresses innovation; the CPU check and staged transfer rules address reuse.
This mapping is not a self-score or prediction of winning.
[Current rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py).

## 6. Evidence limitations, provenance and delivery

The v15 falsification audit covers 19 claims and includes contrary as well as favorable
evidence. Its post-hoc expanded protein-control analysis fails separation in 8/12
model/window comparisons despite the original primary ordering passing 12/12; 11/24
retained-function scores are negative. Dependent models/windows and a small engineered
control set cannot calibrate clinical pathogenicity. The secondary-control supplement
remains independently unreviewed. No model result establishes allele function, phase,
drug response or exposure. The report therefore makes no model-derived rescue claim.
[Full audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-review-v15.md), [claim register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v15.json).

Source coverage is bounded; some studies were read only as indexed abstracts or selected
passages. Retrieval failures are retained, not converted into negative findings. The
Balnis units, endogenous allele effects, relevant tissue response, exposure and meaningful
assay margins remain unresolved. Further independent specialist review and biological
measurements would add evidence that software checks cannot provide.

On September 24 we reviewed the live website, pinned source revision
`aeeef5ad49f51204a7439352e59e9d310aee5e9e`, the methods workbook, and all 24 publicly
listed discussions/68 latest visible comments. A separate agent checked the official
requirements; this was not clinical or independent experimental validation.
[Website review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-official-requirements-review-20260924.md),
[all discussions](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-community-review-20260924.md).

The portal accepts a participant-named PDF or Markdown report, GitHub URL and a
three-minute YouTube/Vimeo pitch. Three entries are allowed and only the latest is
reviewed; remaining quota is unknown. The accompanying slides/narration are not a
recording. Timing, hosting, owner review, provider settings, live portal checks and
receipt remain open. No upload or contact occurred. Prior submissions and research
snapshots remain unchanged.

**Distribution scope remains unresolved.** The challenge states CC BY for submissions,
code and reports. Historical AF3 and non-AVI Atlas materials carry separate output terms.
This judge-facing report/pitch omits their numerical outputs and derived figures, while
honestly disclosing the tools used. Their historical notices and separate research
records remain intact. This separation does not establish that the linked history is
outside submission scope, and no blanket relicensing or resolved eligibility is claimed.
The [readiness note](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v17.md) states the exact remaining question.

## 7. Required AI disclosure and methods answers

These answers map to Track 2 template cells B7–B17. AI disclosure is required; the
remaining methods questions are recommended. The optional filled workbook preserves
the official questions. The original template's old one-entry instruction is superseded
by the live three-entry instruction and organizer announcement.

**B7 — Participant.** jvv7, individual entry. No institutional affiliation is asserted.

**B8 — Identification approach.** Start from the retained derived BUB1B pair and unresolved
phase; connect gene function to conditional pathway hypotheses; compare approved-drug
literature, contrary findings, exposure and deficient-normal safety. Everolimus is an
optional qualified mechanistic probe; HCQ reserve. All eleven dispositions are retained.

**B9 — AI provider, plan and handling.** OpenAI Codex/API was used for code, literature
research, synthesis, editorial work and agent reviews. The owner attests no training on
content; this is not an independent account or zero-retention audit. Firecrawl's local
bridge previously used Fireworks-hosted GLM on owner-confirmed API credits for public
literature; training/retention settings remain unverified. Local retrieval is not proof
of local inference. Google DeepMind AlphaGenome Atlas supplied precomputed API/download
outputs, not on-demand inference; its output/service terms remain applicable. Owner-hosted
research used ESM-1v/ESM-2, ESMC 300M/600M/6B, ESM3-open 1.4B, Boltz-2, AlphaFold2,
AlphaFold3, ESMFold2 and Evo2 7B/20B/40B with public references and permitted derived
substitutions. Earlier ColabFold alignment search received only public wild-type protein;
service training/retention policies remain unverified. This revision used no new GPU
inference or additional model provider. Raw subject reads, VCF records and clinical
narrative stay local. Unknown settings are not silently attested. Historical AF3-derived
materials retain [AlphaFold3 Output Terms](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md), the
[Legally Binding Terms of Use notice](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt),
modifications disclosure and [Abramson citation](https://doi.org/10.1038/s41586-024-07487-w).

**B10 — Automated versus curated.** AI-assisted discovery proposes leads; author/source
adjudication determines decisions. Deterministic scripts check provenance and declared
invariants. Model agreement and passing code checks are not efficacy predictions.

**B11 — Curation.** Selected primary text, abstracts, labels and registry records were
compared with proposals; reading depth, failed retrievals, contradictions, wrong matches
and source units were recorded. Earlier agent checks and the current requirements review
do not constitute a specialist clinical review.

**B12 — Public versus proprietary evidence.** Drug/target evidence is public. Earlier
local genetic reasoning uses the gated challenge dataset and permitted derived findings.
No proprietary drug-response data were supplied; the whole project is not public-input-only.

**B13 — Public sources.** Primary papers, Europe PMC/PubMed, ClinicalTrials.gov, DailyMed,
public UniProt/PDB/model resources and official challenge pages. Search/model services
are tools, not independent scientific sources. Exact records and sources are in the ledgers.

**B14 — Gated sources.** Organizer-provided WGS and phenotype under signed terms informed
earlier local analysis. This report contains only permitted derived findings; no other
proprietary experimental, clinical or drug/target dataset is claimed.

**B15 — Mechanism.** BUBR1 checkpoint/attachment dysfunction is a gene-level mechanism;
allele-specific function and phase are unknown. Everolimus probes a conditional downstream
mTORC1 hypothesis, not replacement of BUBR1. Both proposed branches need qualification.

**B16 — Effort.** Dated work began September 8. Total person-hours, GPU time and API/lab
costs have not been aggregated. Measured CPU review time, where reported, covers only
that reproducibility command; no end-to-end speedup, budget or clinical timeline is claimed.

**B17 — Method abstract (under 500 words).**

We propose a falsifiable test of everolimus, an approved mTORC1 inhibitor, for downstream
non-cancer function in BUB1B-associated mosaic variegated aneuploidy. The selected
stop-gain/missense pair has unresolved phase and endogenous function. Different-model
mTOR observations motivate a qualified experiment, while compound-specific BUBR1
reduction, regeneration concerns and mixed tumour evidence oppose an unqualified rescue
claim. No drug currently earns rescue priority.

Public literature, labels and trial records are adjudicated with explicit reading depth,
source failures and a 19-claim falsification register. Expanded protein controls expose
post-hoc sensitivity; model predictions do not establish function. An unresolved
1,000-fold concentration discrepancy is quarantined rather than converted into a dose.

The staged design first qualifies endogenous, single-allele, cis/trans and corrected
models. Separate locked branches require either excess pathway activity with a functional
deficit, or relevant dynamic-flux and regenerative deficits. A blinded exploratory probe
records useful function, accurate division, death, arrest, slippage, missing tracks and
later recovery. Growth-rate and flux-reporter controls test measurement artifacts.
Independent confirmation requires prospectively justified benefit/injury margins,
replication and a defensible exposure comparison. Unknown evidence means hold; failed
safety stops advancement; all-pass permits preclinical review only.

The contribution is the integrated experiment and its reusable public evidence checks.
A CPU review command needs no subject files or GPU inference; transfer to another genotype
or tissue requires new biological qualification. No wet-lab experiment, clinical exposure
margin, dose recommendation or efficacy claim is made. Positive or negative results could
improve research prioritization if validated. Provider handling, distribution scope,
recorded video and final submission checks remain open.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
