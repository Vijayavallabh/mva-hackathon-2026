# Testing everolimus for useful cell function in BUB1B-associated MVA

Track 2 research proposal · jvv7 · 25 September 2026 · v18

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

Everolimus is an approved mTORC1 inhibitor that could be tested for downstream
non-cancer function in a qualified BUB1B-deficient model. The question is whether
function improves while accurate division, viability and regeneration are preserved.
First establish the endogenous phenotype and relevant mechanism. No rescue-priority drug is supported: everolimus remains an optional mechanistic probe. Selected-pair
efficacy, trans phase and clinical exposure margins are unresolved; no wet-lab
experiment has been performed. No treatment or dose for the child is proposed.

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
chromosome repair. Oncology and TSC indications establish approval and known
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

## 2. Evidence for testing, and against promotion

| Finding | Consequence for this proposal |
|---|---|
| Everolimus increased selected muscle-mass outcomes in aged rats; force benefit was not established. | Measure useful function directly. [Joseph](https://doi.org/10.1128/MCB.00141-19) |
| Everolimus reduced BUBR1 in late-passage human stromal cells; early-passage response differed. | Monitor BUBR1, chromosome fidelity and cell state. Protein loss alone does not prove harm. [Goutas](https://doi.org/10.1016/j.redox.2023.102701) |
| Rapamycin impaired injured-mouse muscle regeneration. | Measure regeneration and recovery; compounds, exposures and tissues are not interchangeable. [Ge](https://doi.org/10.1152/ajpcell.00248.2009) |
| ARST1431: adding temsirolimus to VAC/VI did not establish event-free-survival benefit in 297 evaluable intermediate-risk RMS participants (HR 0.86; 95% CI 0.58-1.26; p=0.44). | Retain this randomized tumour result. It establishes neither non-cancer everolimus rescue nor exactly zero effect in every context. [Trial](https://doi.org/10.1016/S1470-2045(24)00255-9) |

Uncontrolled pediatric TSC growth follow-up and a pediatric transplant-regimen safety
comparison argue against assuming inevitable developmental harm. They neither establish
MVA safety nor isolate everolimus's effect. Renal, infection, marrow/metabolic,
wound-healing and interaction risks remain. Additional clinical laboratory and
treatment-history records are unavailable, so individual suitability cannot be assessed.
[Label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[transplant trial](https://doi.org/10.1001/jama.2025.14338),
[organizer clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/14).

HCQ remains reserve: flux signals and tumour activity do not establish deficient-normal
safety or monotherapy benefit. Pralatrexate is a tumour-only hypothesis for relevant
fusion-positive RMS models; temsirolimus is a clinical benchmark. Entinostat, vorinostat,
niclosamide and posaconazole remain deprioritized. PP2A tools, senolysis and readthrough
remain excluded. No combination is proposed; a competitor's failure confers no priority.
The [63-source, 11-decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json)
records each rationale, approval/indication and exposure limitation.

## 3. Experiment and stopping rules

**Qualify.** Compare wild type, mock editing, each single allele, cis, trans and corrected
derivatives in an editable non-cancer context. Verify engineered genotype/phase,
endogenous RNA/protein and comparable cell states. Measure attachment, checkpoint
activation/maintenance/silencing, accurate viable daughter production and lineage
function separately. Published 731X complementation cannot assign L737Ter's phenotype;
ectopic cDNA can bypass RNA decay. Renal or muscle models need their own qualification.
Without a reproducible relevant phenotype, hold drug advancement and revise the model;
an absent result does not establish clinical normality.

**Probe.** Lock branch eligibility. Include vehicle, an assay-qualified positive control,
corrected-model comparisons and an interpretable orthogonal pathway perturbation.
Randomize within clone/day/plate blocks and blind scoring. Measure graded exposure,
time-matched engagement, useful function, BUBR1/chromosome fidelity and delayed recovery.
Orthogonal disagreement limits mechanism attribution without automatically disproving
a drug-specific effect. Without a clinical exposure bridge, the probe stays exploratory.

**Confirm.** Use pilot performance to prespecify meaningful benefit, acceptable injury,
outcome definitions, missingness analysis, multiplicity handling and sample size before
collecting independent confirmation data. Replicate across clones/backgrounds and culture
days; cells and technical wells are not independent biological replicates. Current data
justify no numerical margin, power estimate, laboratory budget or timeline.

| Evidence | Decision |
|---|---|
| Phenotype, mechanism or confirmation unresolved | Hold. A failed prespecified branch stops that branch. |
| Only a marker or surviving-cell ratio improves | Do not advance. Require replicated function and accurate viable output across enrolled units. |
| Division, viability, fidelity, regeneration or recovery exceeds prespecified injury bounds | Stop despite apparent benefit. |
| Exposure is unmatched or unknown | Block translational promotion. Match analyte, matrix, free fraction, schedule and sampling context. |
| All requirements met | Preclinical review only. |

Whole-blood trough, total-plasma peak, nominal culture concentration and unbound tissue
exposure are not interchangeable. All clinical exposure margins remain null. Operational
details are in the [validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v15.md)
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

## 4. Contribution and reuse

A validated positive result could justify further investigation; a well-measured
negative or harmful result could stop that route in the tested context. The contribution
combines genotype/phase alternatives, active falsification, all-enrolled outcomes and
benefit/harm/exposure gates. The individual methods are established; superiority over
another framework is untested.

Reviewers can check public evidence consistency on a CPU without subject files, API keys,
SSH or model weights:

```bash
uv run --no-project python scripts/track2_public_review_v18.py
```

This checks requirements, discussion coverage, control sensitivity, decisions and
slide/script alignment. It neither reruns models nor validates biology. Complete model
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

## 5. Limits and delivery

The falsification audit covers 19 claims. Original protein-control ordering passes
12/12 comparisons, but post-hoc expanded-control separation fails 8/12; 11/24
retained-function scores are negative. Dependent models/windows and small engineered
control sets cannot calibrate clinical pathogenicity. The secondary-control supplement
remains independently unreviewed. No prediction establishes allele function, phase,
drug response or exposure. [Audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-review-v15.md),
[register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v15.json).

Reading depth varies from indexed abstracts to selected primary passages. Retrieval
failures remain recorded and supply no negative evidence. Balnis units, endogenous
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
[readiness note](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-owner-readiness-v18.md)
records the outstanding question.

## 6. Methods answers and AI disclosure

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
service training/retention policies remain unverified. This revision used no new GPU
inference or additional model provider. Raw subject reads, VCF records and clinical
narrative stay local. Unknown settings are not silently attested. Historical AF3-derived
materials retain [AlphaFold3 Output Terms](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-output-terms.md), the
[Legally Binding Terms of Use notice](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphafold3-Legally-Binding-Terms-of-Use.txt),
modifications disclosure and [Abramson citation](https://doi.org/10.1038/s41586-024-07487-w).

**B10: Automated versus curated.** AI suggests leads; author/source review determines
decisions. Scripts check provenance and declared constraints. Model agreement or passing
software checks does not predict efficacy.

**B11: Curation.** Compare proposals with primary passages, abstracts, labels and
registries. Record reading depth, failed retrievals, contradictions, wrong matches and
units. Agent and requirements reviews are not specialist clinical review.

**B12: Public versus proprietary evidence.** Drug/target evidence is public; earlier
genetic reasoning used gated challenge data. No proprietary drug-response data were
supplied. The project is not wholly public-input-only.

**B13: Public sources.** Primary papers, Europe PMC/PubMed, ClinicalTrials.gov,
DailyMed, UniProt/PDB/model resources and official challenge pages; exact sources are
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
MVA. The selected pair's phase and endogenous effects are unresolved. Different-model
mTOR findings motivate testing; BUBR1 reduction, regeneration concerns and mixed tumour
evidence constrain the claim. No drug earns rescue priority.

A 19-claim register records supporting and contrary evidence, reading limits and stop
rules. Expanded protein controls expose prediction sensitivity; a disputed 1,000-fold
concentration discrepancy is quarantined. First qualify endogenous, single-allele,
cis/trans and corrected models. Lock either excess mTOR activity with functional
impairment or impaired flux and regeneration. A blinded probe records function, accurate
division, all cell fates and recovery, with controls for assay artifacts. Independent
confirmation requires prespecified benefit/injury margins, replication and a defensible
exposure comparison. Unknown evidence means hold; failed safety stops advancement;
all-pass permits preclinical review only.

Public CPU checks support reuse without subject files or GPUs. New tissues require
fresh qualification. No wet-lab result, clinical margin or efficacy claim is available.
Provider handling, distribution scope, recording and submission checks remain open.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
