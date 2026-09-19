# Testing everolimus in BUB1B-deficient cells

## One conditional experiment for non-cancer tissue function

Participant jvv7 · research draft 6 · 2026-09-19

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

Research only. No experiments have been performed. Drug efficacy and clinical exposure
margins remain unestablished, and trans phase remains unconfirmed. This report makes no
treatment recommendation. Provider disclosure verification, owner review, a recorded
and hosted pitch, live portal checks and submission remain open.

## The proposed experiment

We propose testing whether everolimus can improve a measurable functional deficit in
BUB1B-deficient non-cancer cells. Drug testing begins only if a qualified model shows
excess mTORC1 activity. Advancement would require replicated functional benefit with
preserved division, viability and tissue-relevant function at a justified exposure.
Everolimus is the sole conditional research priority; no drug has established efficacy
for the selected pair.

BUB1B encodes BUBR1, which helps control chromosome attachment and the timing of cell
division. Disruption of both copies is an established mechanism of mosaic variegated
aneuploidy. The selected stop-gain and missense pair gives us a genetic starting point,
but its phase and allele-specific functions remain unresolved. That uncertainty belongs
in the experiment: engineered cis, trans and single-allele models would test the
alternatives without claiming to resolve the subject's phase.
[Hanks 2004](https://doi.org/10.1038/ng1449),
[Suijkerbuijk 2010](https://doi.org/10.1158/0008-5472.CAN-09-4319)

The reason to investigate everolimus is narrow. A study of mice carrying different
BubR1 alleles found increased mTOR-associated phosphoproteins in one muscle/genotype
comparison. It did not test rapalog rescue. We would first ask whether excess pathway
activity exists in a model relevant to the selected pair, then test whether reducing
it improves a prespecified function. Such improvement could be downstream mitigation;
chromosome repair would require its own evidence.
[Sieben study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781)

The experiment must account for every enrolled cell. Fewer abnormal surviving mitoses
could reflect accurate division, death, blocked mitotic entry or escape from arrest.
We would record first-division outcomes and follow daughter survival separately, report
tracking loss, and measure tissue-relevant function. Protein abundance or a suppressed
pathway marker alone would not establish benefit. Failure to establish pathway excess,
unacceptable deficient-normal injury, unattainable exposure or failure to replicate
would stop advancement.

Tumour suppression has a separate success criterion and requires matched BUB1B-deficient
non-cancer controls. It cannot substitute for functional benefit in normal tissue.
Hydroxychloroquine (HCQ) remains reserve; pralatrexate remains an optional tumour-only
direction for fusion-positive rhabdomyosarcoma (RMS). Neither is an equal-priority lead,
and no BUBR1-repair claim follows from tumour activity. These are research priorities,
not a prediction of the best treatment.

The report retains favourable and contrary findings, and the candidate review explains
why other directions do not displace this experiment. Corrected primary-source reviews
support the decisions. Agreement between language models cannot supply replication;
the next decisive evidence requires experiments.

## 1. Genetic starting point and scope

The owner reports Track 1 scores of 100 rank points and F-max 1 on the first submission.
The receipt and uploaded-byte identity have not been independently archived. The selected
pair is GRCh38 chr15:40209701 T>G, p.Leu737Ter, and chr15:40220612 T>G,
p.Asn1002Lys, annotated on ENST00000287598.11. These are permitted submission-derived
variants; the raw VCF and read data are not redistributed.

The [genome-wide evidence audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track1-evidence-audit.md)
and [phase-connectivity audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/phase-connectivity.md)
describe reproducible methods. No eligible fragments connect the pair directly or through
the screened markers. Finding both variants and matching a competition answer key do not
establish that they lie on opposite chromosome copies (in trans), how either allele
functions, or whether a drug will work.

BUB1B encodes BUBR1, a regulator of the mitotic checkpoint and chromosome attachment.
BUB1 is a different protein. Disruption of both BUB1B copies is an established MVA
mechanism at the gene level. The stop-gain is consistent with loss of function, but
RNA decay versus truncated protein has not been measured. Computational evidence supports
the missense allele; instability, dominant-negative activity and residual function have
not been demonstrated.
[Hanks 2004](https://doi.org/10.1038/ng1449),
[Suijkerbuijk 2010](https://doi.org/10.1158/0008-5472.CAN-09-4319)

The broad phenotype supports renal, muscle and developmental safety testing alongside
the malignancy history. Renal calcification does not measure renal filtration. Parental
reproductive loss is a separate inheritance signal, not an abnormality of the proband.
We do not infer active cancer, fusion status, treatment regimen, stage or organ function.
The low-level chromosome copy-number screening result is neither a clinical karyotype nor
a drug-sensitivity assay. No single phenotype determines the intervention.

### What AlphaGenome adds

Precomputed Atlas AVI PHRED values are 33.7641 and 25.6084, respectively. Their major
attributions reuse termination, AlphaMissense and conservation information. These are
calibration ranks, not disease probabilities or independent functional confirmation.
Local queries of the public merged-splicing archive returned 0.08699 and 0.04813;
the public DNM1 comparison returned 2.522. These unsigned aggregate magnitudes are
not splice fractions or validated clinical cutoffs. Small values do not prove normal RNA
processing or absent transcript decay. Tissue/junction-resolved evidence remains missing.

Neither output resolves phase or supports drug efficacy, ranking or exposure. The
[authenticated audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphagenome-authenticated-results.md)
and [splicing audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphagenome-splicing-results.md)
record request scope, source/reference checks, hashes and limitations. No on-demand
AlphaGenome inference occurred. Endogenous RNA, protein and function assays are still needed.

## 2. Test the mechanism before the drug

BUBR1 helps restrain APC/C-CDC20 until chromosome attachments are appropriate and recruits
PP2A-B56 to regulate attachment-associated phosphorylation. Dysfunction can cause chromosome
missegregation. Chromosomal instability describes an error process; aneuploidy describes
a chromosome-number state. Suppressing a checkpoint signal does not necessarily repair
the process that caused it.
[Gama Braga 2020](https://doi.org/10.1016/j.celrep.2020.108397)

Published work offers catalytic and noncatalytic interpretations of BUBR1's C-terminal
domain. This proposal does not depend on settling that debate. Localization, checkpoint
timing and faithful division are functional outcomes; a kinase assay alone cannot serve
as a universal test of rescue.
[Suijkerbuijk 2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[Huang 2019](https://doi.org/10.1038/s41422-019-0178-z)

| Objective | A result that could support advancement | An insufficient substitute |
|---|---|---|
| Constitutional functional rescue | Reproducible functional gain with preserved division, viability and tissue-relevant function | More protein, fewer abnormal surviving mitoses, or a lower senescence-marker fraction alone |
| Tumour suppression | Relevant-model activity and a measured separation from deficient-normal injury at matched exposure | Nominal potency, unrelated-tumour responses, or indiscriminate toxicity |
| Durable tumour killing | Post-withdrawal loss of regrowth under a prespecified assay | On-treatment arrest or initial regression followed by recurrence |

## 3. Evidence process and reading limits

This is an adaptive rapid scoping review, not an exhaustive systematic review.
Baseline searches through 2026-09-08 produced a curated 53-source/12-candidate ledger.
Later selected-section and abstract reviews, with official regulatory checks, broadened
coverage. Targeted primary-source rechecks took place on 2026-09-19. This does not mean
that all literature was searched through September 19.

The archived GLM work contains nineteen accepted jobs: eighteen completions and one
failed retrieval. The completions comprise ten abstract-based topic reviews, seven
corrective/adversarial passes and an initial PP2A answer rejected as source-grounded
evidence. Six overlong prompts were rejected before execution. Neither the job count nor
the 35 supplied URLs measures the number of validated studies or fully read papers.

Full-text retrieval limits prompted comparisons against indexed primary abstracts.
Independent reviewers checked consequential claims against available primary sections,
abstracts and labels. An abstract's silence cannot negate previously inspected Methods
or Results. The [GLM audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-review.md),
[constitutional review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-constitutional-review.md)
and [oncology review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-oncology-review.md)
retain access failures, reading depth and rejected claims. Repeated model outputs are
not independent experiments, and checking a citation's identity does not validate its
use to support a causal claim.

The [v4 decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v4.json)
supports this report without replacing the historical ledgers. Its 32 source records
and 11 research decisions link each retained direction to evidence, limitations and a
stop rule. These counts represent neither all-new papers nor the exhaustive baseline.
Reading-depth fields describe cumulative archived reviews. The
[independent v4 review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-v4-primary-review.md)
identifies the claims rechecked on September 19. Even a strong cancer experiment can
provide only indirect evidence for improvement in non-cancer tissue.

## 4. Conditional priority: everolimus

The rationale depends on a measurable downstream abnormality. It does not assume that
all BUB1B variants activate mTOR. Sieben and colleagues found elevated phospho-p70 S6
kinase and phospho-4EBP1 in BubR1+/X753 gastrocnemius muscle; the +/L1002P comparison did
not share that pattern. Mouse L1002P models human L1012P, not the submitted Asn1002Lys.
The study did not test rapalog rescue. Its H/L1002P animals are biallelic disease models,
not monoallelic carriers. The published correction also matters to interpretation.
Figure 5 depicts two animals/group for these blots, and the Methods state that experiments
were not randomized or blinded. These findings give us a hypothesis to measure, not
intervention evidence for the selected pair. Phospho-S6 assays proposed below are future
readouts, not a new name for the original measurement.
[Study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781)

Everolimus has approved uses, including specified pediatric TSC indications/formulations;
approval does not extend to MVA or RMS. Infection, mucosal, renal, developmental and
interaction concerns make deficient-normal function a necessary endpoint.
[US label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)

RMS clinical evidence is mixed. Pediatric everolimus studies showed pathway inhibition
without objective responses. A later lenvatinib/everolimus cohort had two partial responses
among twenty RMS participants but missed efficacy goals. Those combination responses
cannot be attributed to everolimus alone.
[Fouladi 2007](https://doi.org/10.1200/JCO.2007.11.4017),
[Santana 2020](https://doi.org/10.1002/cncr.32722),
[combination study](https://doi.org/10.1002/pbc.31692)

Temsirolimus provides a class benchmark. ARST0921 favoured its relapse regimen over a
bevacizumab-containing regimen, not chemotherapy alone. ARST1431 did not demonstrate
improved three-year event-free survival (EFS) from adding temsirolimus: 66.8% versus 64.8%,
HR 0.86, 95% CI 0.58-1.26, p=0.44, among 297 evaluable participants. The populations and
treatment backbones differ. A nonsignificant result does not prove exactly zero effect;
neither trial tests constitutional everolimus rescue.
[ARST0921](https://doi.org/10.1200/JCO.19.00576),
[ARST1431](https://doi.org/10.1016/S1470-2045(24)00255-9)

In a separate rapamycin experiment, nocodazole-arrested A549 cells showed more mitotic
slippage in the death-versus-slippage comparison. Its denominator does not include all
enrolled cells, and it is not evidence of clinical everolimus harm. It supports measuring
complete cell fates before interpreting fewer abnormal mitoses as rescue.
[Yamada](https://doi.org/10.1016/j.isci.2021.103675)

We would qualify pathway excess and assay performance first. Advancement requires
replicated target modulation and a prespecified functional benefit, with preserved
deficient-normal function at a justified exposure. Pathway excess need not be exclusive
to one genotype or the earliest causal event to be modifiable. Failure to establish the
proposed excess nevertheless stops this mTOR rationale. Persistent injury, unattainable
exposure or failure to replicate also stops advancement. A negative result would remain
part of the evidence.

## 5. Candidate decisions

| Direction | Evidence worth retaining | Reason for current decision |
|---|---|---|
| HCQ, reserve | Adult everolimus/HCQ RCC study met its single-arm six-month PFS threshold; two partial responses among 33 evaluable participants. | No monotherapy comparator or pediatric RMS/deficient-normal window. Chloroquine sensitivity in trisomic fibroblasts is also a normal-tissue warning, not direct HCQ selectivity. [Haas](https://doi.org/10.1158/1078-0432.CCR-18-2204), [Tang](https://doi.org/10.1016/j.cell.2011.01.017) |
| Pralatrexate, tumour-only horizon | Regression in some fusion-positive RMS models, including RH4 regression followed by recurrence. | Model subtype, schedule-dependent toxicity and withdrawal outcomes constrain transfer. It is not BUB1B repair or established selective TYMS inhibition; thymidine rescue alone cannot identify a unique direct target. [Study](https://doi.org/10.1038/s41467-026-73749-y), [PTCL label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=cc3df863-c51c-49c5-283a-d6808fb49258&version=6) |
| Entinostat, deprioritized tumour direction | Model-dependent favourable combination results and Chinese marketing approval for a defined breast-cancer setting. | It is not globally unapproved. Prior RMS experiments include antagonism; daily mouse and weekly human schedules are not exposure-matched. There is no pediatric RMS indication or validated window. [2019](https://doi.org/10.1002/pbc.27820), [2024](https://doi.org/10.1038/s41598-024-66545-5), [NMPA](https://english.nmpa.gov.cn/2024-04/30/c_1049690.htm) |
| Vorinostat, deprioritized | An ERMS case had transient clinical improvement. | Progression and severe toxicity followed; paired PDX necrosis did not suppress growth/Ki67. A case exception is not controlled efficacy. [Case/PDX](https://doi.org/10.3389/fonc.2017.00327) |
| Niclosamide/TBX screen, deprioritized | Endogenous validation and RMS assays; a reformulated adult study improved the feasibility picture. | Micromolar nominal activity, some extrapolated EC50s, no deficient-normal safety window. Original and reformulated scheduled total-plasma samples cannot define free RMS exposure. [Screen](https://doi.org/10.1002/cam4.70303), [original PK](https://doi.org/10.1371/journal.pone.0198389), [correction](https://doi.org/10.1371/journal.pone.0202709), [reformulation](https://doi.org/10.1038/s41598-021-85969-x) |
| Posaconazole, deprioritized | RD xenograft growth inhibition, not eradication. | Liver histologic injury, formulation dependence and major interaction constraints. Nonsignificant enzyme comparisons do not erase histology. No nominal-culture/free-plasma ratio establishes a clinical margin. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8493378/), [label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0bdf77ae-3639-49c1-b7c7-533f9d073084) |
| PP2A compounds, excluded from the approved-drug shortlist; mechanistic controls retained | Engineered PP2A-B56 recruitment improved alignment in published MVA cells. | The endpoint was fixed-cell alignment under arrest, not faithful daughter divisions. DT-061 specificity is disputed; different-compound isolated-PR65 binding/stabilization does not settle it. [Xu](https://doi.org/10.1242/bio.20134051), [Leonard](https://doi.org/10.1016/j.cell.2020.03.038), [Vit](https://doi.org/10.15252/embj.2022110611), [Naqvi](https://doi.org/10.1021/jacsau.6c00003) |
| Drug senolysis/HSP90 inhibition, excluded as a constitutional priority | Genetic senescent-cell clearance has BubR1-model evidence; D+Q/HSP90 studies provide favourable findings in other contexts. | Ercc1 drug studies are not BubR1 rescue; p21 protects muscle/fat but promotes the lens phenotype in the cited BubR1 model. HSP90 inhibition can deplete unstable BUBR1. [Baker 2011](https://doi.org/10.1038/nature10600), [Baker 2013](https://doi.org/10.1016/j.celrep.2013.03.028), [Zhu](https://doi.org/10.1111/acel.12344), [Fuhrmann](https://doi.org/10.1038/s41467-017-00314-z), [BUBR1 stability](https://doi.org/10.1158/0008-5472.CAN-09-4319) |
| Ataluren/gentamicin readthrough, excluded as current clinical candidates | Positive and negative context-dependent readthrough studies inform controls. | No selected-pair functional rescue; reporter/full-length/function are separate endpoints. Gentamicin toxicity is a major objection. EU Translarna authorization was not renewed in March 2025. [Roy](https://doi.org/10.1073/pnas.1605336113), [Bolze](https://doi.org/10.1038/s41598-017-01093-9), [EMA](https://www.ema.europa.eu/en/medicines/human/EPAR/translarna) |

These decisions concern research priorities, not every approved clinical use. Reopening
HCQ requires compound-specific flux and selectivity evidence. Static LC3, PBMC vesicles
or results from another lysosomal inhibitor cannot supply it. The preserved baseline
review retains both positive and negative adult HCQ trials.

Other baseline exclusions and deprioritizations remain. Sodium phenylbutyrate lacks a
demonstrated repairable missense-folding defect. Proteasome blockade is not precise BUBR1
repair. Metformin/VIT responses lack a VIT-alone comparator and do not establish an exposure
window. NMN protein-abundance effects do not establish the lifespan effect of a SIRT2
transgene. Ordinary-ageing SIRT2 results concern a different biological context, rather
than a failed replication in the same model. Direct checkpoint inhibitors may oppose
constitutional rescue.
[Baseline review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-final-review.md),
[North](https://doi.org/10.15252/embj.201386907), [Wu](https://doi.org/10.1111/acel.14027)

Two unresolved interpretation problems also prevent promotion. The redox paper's abstract
and Results disagree on ROS/AIF compound attribution, and its colony assay reseeded viable
survivors rather than measuring survival in the original population. Statin/radiation
findings support tumour-damage hypotheses, not muscle rescue or a validated low-signature
eligibility rule. Neither direction is promoted.
[Chico](https://doi.org/10.1002/ddr.70304),
[Codenotti](https://doi.org/10.3390/cancers16050853)

## 6. Proposed validation and stop rules

The [v5 validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v5.md)
specifies the models, assays and decisions. It authorizes no laboratory work, material
acquisition, family contact or patient intervention.

1. Qualify independently engineered wild-type, single-allele, cis and trans models,
   mock edits and corrected derivatives. Confirm phase in the engineered models without
   claiming to resolve the subject's phase.
2. Measure endogenous RNA/protein, localization, checkpoint response, accurate division
   and lineage function before drug selection. Protein abundance alone is insufficient.
   Add renal/muscle-relevant models only after qualification.
3. Confirm the proposed pathway phenotype and measure, or credibly bound, free-medium
   and relevant human exposure over the same schedule. Record parent/metabolite,
   formulation, matrix, binding and sampling time. Whole-blood trough, total-plasma peak
   and nominal culture concentration are not interchangeable.
4. Enroll cells before exposure and account for accurate division, erroneous division,
   death, persistent arrest, slippage and tracking loss. Follow daughters and recovery.
   Prespecify denominators rather than counting only survivors.
5. Randomize within clone/day/plate blocks and blind scoring. Retain wells and clones,
   rather than treating cells as independent replicates. Use pilot variance for a separate
   confirmatory power calculation. No statistical power is claimed here.

Constitutional improvement requires paired assessment of useful division and
deficient-normal tissue function. Tumour testing requires documented model subtype,
an oncology-selected comparator, single-agent controls and matched normal testing before
combination work. Calling an effect synergistic requires a prespecified interaction model.
Reversible on-treatment benefit can be real. Recurrence rules out a durable-killing claim
but does not erase every pharmacological benefit. Harmful rebound and persistent injury
are reasons to stop. Zero detected injury does not prove zero risk.

The [exposure ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-exposure.json)
contains eight public-study/label observations and unit-conversion checks, not dosing
recommendations. All clinical exposure margins remain unknown. No numerical safe
concentration, therapeutic ratio or dose for the child is proposed.

## 7. Rigor, impact, innovation and scalability

The proposal retains null and unfavourable findings, model and allele identity, reading
depth, exposure units and prespecified success/failure criteria. Removing indirect support
removes the conditional lead's basis. Requiring direct-pair rescue or measured exposure
leaves no passing candidate. This sensitivity describes a limitation, not a calibrated
drug score.

The potential value is to identify a useful intervention or reject a harmful idea early.
The evidence supports neither a clinical benefit estimate nor a probability of winning.
The proposed contribution is a genotype-aware benefit/harm assessment across tumour and
non-cancer contexts, with complete cell-fate accounting. We do not claim to have discovered
mTOR biology, autophagy or these drugs, or to have proved that this framework is unique.

The public evidence, explicit decisions and local checks can be reused for other
chromosome-instability hypotheses. Begin with one qualified context and one conditional
agent; add lineages and backgrounds only when the earlier requirements are met. Clone
construction, assay qualification, exposure measurement and specialist input limit the
scale. No cost, timeline or laboratory capacity has been estimated.

Phase, allele function, tumour context and organ function remain unknown. Other limitations
include indirect transfer between models, incomplete source coverage, publication bias,
unmeasured exposure and the absence of experimental efficacy or safety data. Additional
computation cannot resolve these unknowns on its own.

## 8. Reproducibility and delivery status

```bash
uv run python scripts/track2_evidence.py check
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/track2_evidence.py track1
uv run python scripts/track2_release.py verify results/feat009/jvv7_track2_research_v3
uv run python scripts/test_track2_release_v4.py
uv run python scripts/track2_release_v4.py verify results/feat009/jvv7_track2_research_v4
uv run python scripts/test_track2_release_v5.py
uv run python scripts/track2_release_v5.py verify results/feat009/jvv7_track2_research_v5
uv run python scripts/test_track2_release_v6.py
uv run python scripts/track2_release_v6.py verify results/feat009/jvv7_track2_research_v6
```

The v6 release binds the report, unchanged v4 scientific decision ledger, v5 validation
plan, new pitch and deck, and supporting reviews to hashes. Track 1 v4 and every earlier
Track 2 snapshot, including v1 through v5, are preserved. Hashes detect drift; they do
not establish truth, signatures, clinical readiness or a portal receipt.

The three-minute narration and local deck still require rehearsal, recording and a
playable YouTube/Vimeo URL. The official portal accepts a PDF or Markdown report with
the participant name, a GitHub URL and the video link, and reviews the latest entry.
Provider, plan/tier and relevant data-handling settings must be disclosed. The public
submission-tab source was rechecked on September 19; authenticated remaining quota and
final live requirements were not.
[Official instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/raw/main/tabs/submit_track2.py)

## 9. AI disclosure and data handling

OpenAI Codex was used through the API tier for code, public-source research, synthesis,
editorial work and independent agent reviews. The owner attests that content is not used
to train OpenAI models. This is not an independent account audit or a zero-retention claim.

Google DeepMind AlphaGenome Atlas supplied precomputed-output API results and public
downloadable merged-splicing assets. No on-demand model inference occurred. The access
route is recorded; no broader account training or retention setting is inferred. The
[AlphaGenome Output Terms](https://deepmind.google.com/science/alphagenome/output-terms)
and applicable non-commercial artifact conditions remain relevant. Extraction,
serialization, tables and interpretation are modifications, not a new output licence.

Firecrawl's self-hosted MCP service called Fireworks-hosted GLM for archived public-literature
jobs, which returned `accounts/fireworks/models/glm-5p3-flash`. On 2026-09-19 the owner
confirmed credit-based API usage. This describes billing/access, not an independently
audited plan or data policy. Fireworks training and retention settings remain unverified,
so final disclosure is unresolved. This is neither a no-training nor a zero-retention
attestation for Fireworks. The local service can retain prompts/results; self-hosting does not mean
that model inference was local. Earlier conditional Google/Vertex code paths do not
establish that those paths executed. No new GLM calls were made for the v4 integration,
v5 editorial revision or v6 story and design rebuild.

K-Dense BYOK was installed and smoke-tested previously. No inference or provider login
was recorded in that setup; installation produced no scientific result.

This work uses public literature and permitted derived summaries. Protected reads, raw
VCF records/subsets and clinical narrative were not sent through this workflow. The slides
are rendered locally without external images, fonts or model calls; slide generation adds
no new model provider. Historical single-provider attestations describe earlier sessions,
not the expanded workflow. Manuscript embargo and local deletion obligations remain in
force. No family contact, treatment or submission occurred here.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
