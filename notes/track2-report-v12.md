# Testing benefit and harm before prioritizing a drug for BUB1B-associated MVA

## A model-first decision, with everolimus retained as a mechanistic probe

Participant jvv7 · research draft 12 · 2026-09-19

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

Research only. No experiments have been performed. Drug efficacy and clinical exposure
margins remain unestablished, and trans phase remains unconfirmed. This report makes no
treatment recommendation. Provider disclosure verification, owner review, a recorded
and hosted pitch, live portal checks and submission remain open.

## The proposed experiment

We propose testing whether everolimus can improve a measurable functional deficit in
BUB1B-deficient non-cancer cells. An exploratory drug perturbation requires a qualified
functional deficit and a prespecified mechanistic hypothesis. Branch A tests reproducible excess mTOR-associated
signaling; branch B separately tests a demonstrated autophagic-flux and regenerative-
function deficit. Neither branch is established for the selected pair. Excess alone
does not establish that inhibition is beneficial: the response could be adaptive.
Advancement would require replicated functional benefit with
preserved division, viability and tissue-relevant function at a justified exposure.
The v9 adversarial review withdraws the comparative priority assigned to everolimus.
It remains an optional, model-qualified mechanistic probe, not a preferred rescue
candidate. No reviewed drug has established efficacy for the selected pair.

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
pathway marker alone would not establish benefit. Failure to qualify the prespecified branch, unacceptable deficient-normal injury,
unattainable exposure or failure to replicate would stop advancement. Absence of
excess stops branch A; it does not automatically license branch B.

Tumour suppression has a separate success criterion and requires matched BUB1B-deficient
non-cancer controls. It cannot substitute for functional benefit in normal tissue.
Hydroxychloroquine (HCQ) remains reserve; pralatrexate remains an optional tumour-only
direction for fusion-positive rhabdomyosarcoma (RMS). Neither is promoted,
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

The [v9 adversarial audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-adversarial-v9.md)
reviews all prior workstreams and records new source checks separately from inherited
reviews. It identifies a material missing contrary experiment and revises the
prioritization, protocol and presentation. This is not an exhaustive new search.


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

The [v10 decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v10.json)
supports this report without replacing the historical ledgers. Its cumulative source records
and 11 research decisions link each retained direction to evidence, limitations and a
stop rule. These counts represent neither all-new papers nor the exhaustive baseline.
Reading-depth fields describe cumulative archived reviews. The
[independent v4 review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-v4-primary-review.md)
identifies the claims rechecked on September 19. Even a strong cancer experiment can
provide only indirect evidence for improvement in non-cancer tissue.

## 4. Everolimus: mechanistic probe only after model qualification

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

### Contrary evidence that changes the priority

The earlier synthesis omitted an experiment using everolimus itself. In late-passage
human Wharton's-jelly stromal cells, Goutas and colleagues reported lower BUBR1 protein
after 24 hours of everolimus; early-passage cells did not show the same response.
The Methods specify 50 nM nominal culture concentration at 24 hours and a separate
100 nM/3-hour condition. These are different concentration/time conditions, not a
single longitudinal exposure series. HCQ increased late-passage BUBR1 abundance at
100 micromolar for two hours. The cells were cultured with 10% fetal bovine serum.
Neither observation establishes improved division, selected-pair rescue or a clinical
exposure margin. The pharmacologic and protein-association results are consistent
with an autophagy/lysosome mechanism, but do not isolate it from cell-cycle,
transcriptional, translational or population-selection effects in our proposed model.
[Goutas 2023, Results/Figure 6 and Methods](https://doi.org/10.1016/j.redox.2023.102701)

This is a relevant potential adverse mechanism, not proof of patient harm. The same
standard applies to favourable evidence: increased BUBR1 abundance does not promote
HCQ to a constitutional rescue drug. BUBR1 amount, localization, checkpoint activity,
completed division and tissue function remain separate measurements.

Excess pathway activity could also be compensatory. In denervated mouse muscle,
Quy and colleagues found that rapamycin worsened atrophy; later work by Castets and
colleagues found timing-dependent pathway/flux relationships and stronger atrophy
with muscle Raptor loss. Neither study tests this genotype. They defeat the general
inference that elevated mTORC1 necessarily identifies a beneficial inhibition target.
[Quy 2013](https://doi.org/10.1074/jbc.M112.399949),
[Castets 2019](https://doi.org/10.1038/s41467-019-11227-4)

Favourable functional evidence also exists outside MVA: everolimus improved
vasoconstriction in HGPS tissue-engineered vessels, whereas improvement in dilation
was not demonstrated with everolimus alone. The model involves progerin/LMNA pathology,
not this BUB1B pair; small experiments, limited follow-up and combination-specific
toxicity constrain transfer. This prevents a blanket conclusion that everolimus cannot
help non-cancer tissue, while supplying no MVA response or exposure prediction.
[Abutaleb 2023](https://doi.org/10.1038/s41598-023-32035-3)

We therefore withdraw the claim that everolimus is the preferred rescue candidate.
Its retained role is a bounded hypothesis-testing perturbation, after model and
assay qualification. Measure functional response and BUBR1/flux/cell-state changes
together. A material BUBR1 decrease pauses advancement for mechanistic review;
worsening chromosome fidelity or lineage function fails the relevant safety gate.
A protein change alone does not prove damage, and unchanged protein alone does not
establish safety. An orthogonal, titrated pathway perturbation can help assign a
mechanism; discordance limits mechanism attribution rather than erasing a measured
drug-specific effect. Excess need not be the initiating disease event to be modifiable.
Absent model phenotype, unjustified exposure, persistent injury or nonreplication
stops advancement. Removing indirect evidence leaves no rescue-priority candidate.

### What the first continuing falsification cycle changes

The [Firecrawl falsification review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-cycle1.md)
adds primary findings that challenge both benefit and harm assumptions. It executes
87 bounded retrieval calls plus complementary public records; those counts are not
numbers of validated studies. The cumulative v10 ledger has 52 source records and
11 candidate decisions, including rechecked registry/baseline sources.

In a hypercapnia model, rapamycin improved satellite-cell proliferation, autophagic
flux and transplantation-related myogenesis despite unchanged baseline measured
mTOR readouts. Key experiments were small, some displayed controls were reused,
and the detailed dose/schedule supplement was not reviewed. This is a reason to
avoid a universal measured-excess entry rule, not evidence that this child's cells
have the same problem. Branch A retains its original excess requirement. A new
branch B must independently demonstrate a relevant flux/function deficit and
mechanistic plausibility before a prospectively specified experiment; it cannot
be substituted after an unfavorable result. No BUB1B or everolimus response was
shown in that study. [Balnis](https://doi.org/10.1172/jci.insight.182842)

Positive compound-specific evidence also exists in aged rats: lower-dose RAD001
improved selected muscle mass and morphology outcomes, with different responses
across muscles and doses. Force improvement and a free human tissue-exposure
window do not follow from those endpoints. Conversely, a primary muscle-injury
study reports impaired regeneration with rapamycin and rescue with a resistant
mTOR construct. These findings require graded inhibition, stage-specific precursor
activation/differentiation, and recovery testing, rather than maximizing pathway
suppression or using muscle size alone as success.
[Joseph](https://doi.org/10.1128/MCB.00141-19),
[Ge](https://doi.org/10.1152/ajpcell.00248.2009)

HCQ remains reserve. A selected adult CQ/HCQ myopathy series documents clinically
important muscle/lysosomal injury, sometimes with incomplete recovery. It cannot
estimate pediatric incidence. A small randomized ovarian-cancer trial did not
demonstrate benefit from adding HCQ, while reporting no excess adverse events in
that regimen. Neither observation determines RMS efficacy. Together they reinforce
compound-specific flux, delayed muscle safety and exposure requirements; protein
accumulation is not functional rescue.
[Naddaf](https://doi.org/10.3389/fneur.2020.616075),
[Goenka](https://doi.org/10.1007/s12672-025-01904-w)

A population PK model based on 73 cancer patients shows why hematocrit and red-cell
partitioning matter when interpreting everolimus whole blood. Its plasma/PD outputs
rely on binding assumptions, not measured unbound tissue concentrations. All clinical
margins therefore remain unknown. Public registry review distinguishes a small,
uncontrolled growth follow-up from a stale pediatric trial with no posted results;
absence of results is not a failed trial. The updated ARST1431 record preserves
297 in the EFS analysis despite 325 overall enrolled; the published plot remains
unchanged. [van Erp](https://doi.org/10.1007/s40262-016-0414-3),
[growth follow-up](https://clinicaltrials.gov/study/NCT02338609),
[pediatric trial](https://clinicaltrials.gov/study/NCT01216839),
[ARST1431 registry](https://clinicaltrials.gov/study/NCT02567435)

Genotype and tissue transfer require similar care. The functional Taxol experiments
in a paper about monoallelic BUB1B variants actually used RWPE-1 clones with two edited
in-frame alleles. Reduced drug sensitivity there cannot predict the selected pair's
response. Cardiac-specific Bub1b knockout also disrupts embryonic differentiation;
a muscle or division assay cannot establish whole-development rescue. No cardiac
abnormality or antimitotic resistance is inferred in this child.
[Silva](https://doi.org/10.1186/s12929-024-01056-z),
[Pun](https://doi.org/10.1161/JAHA.124.038286)

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
HCQ requires compound-specific flux and selectivity evidence. The newly retained
protein-abundance observation does not establish constitutional benefit or justify
combining HCQ with everolimus. Static LC3, PBMC vesicles
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

The [v10 validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v10.md)
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

The official rubric weights these criteria at 35%, 25%, 25% and 15%, respectively.
The following makes the contribution and its limits explicit; it is not a self-score.

| Criterion | Concrete contribution | What would establish value; current limitation |
|---|---|---|
| Scientific rigor — 35% | Connect the stop-gain/missense hypothesis to BUBR1 function, distinguish downstream mTOR perturbation from gene repair, retain contrary evidence and test independent A/B hypotheses. | Endogenous function, model qualification, replicated benefit/harm and exposure evidence are required. None is established for the selected pair. |
| Potential impact — 25% | Determine whether a proposed intervention helps useful MVA cell function or causes harm, and identify which mechanism merits follow-up. | A validated result could improve understanding and research prioritization. This is not a diagnostic validation or a clinical benefit estimate. |
| Innovation — 25% | Combine genotype/phase-aware comparisons, evidence falsification and complete first-division/daughter-fate accounting to challenge apparent rescue caused by selection. | The proposed integration is the contribution. Its superiority and first-ever novelty have not been demonstrated. |
| Scalability — 15% | Reuse the public evidence schema, retrieval/code provenance, model comparisons and stop rules in other chromosome-instability contexts. | Each new genotype, tissue or disease needs fresh mechanism, model, safety and exposure qualification. Laboratory throughput, capacity, cost and timeline are unmeasured. |

Source: [official About-page rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/about.py).

The proposal retains null and unfavourable findings, model and allele identity, reading
depth, exposure units and prespecified success/failure criteria. Removing indirect support
removes the mechanistic probe's motivating rationale. Requiring direct-pair rescue or measured exposure
leaves no passing candidate. This sensitivity describes a limitation, not a calibrated
drug score.

The potential value is to identify a useful intervention or reject a harmful idea early.
The evidence supports neither a clinical benefit estimate nor a probability of winning.
The proposed contribution is a genotype-aware benefit/harm assessment across tumour and
non-cancer contexts, with complete cell-fate accounting. We do not claim to have discovered
mTOR biology, autophagy or these drugs, or to have proved that this framework is unique.

The public evidence, explicit decisions and local checks can be reused for other
chromosome-instability hypotheses. Begin with one qualified context and one bounded
mechanistic question; add lineages and backgrounds only when the earlier requirements are met. Clone
construction, assay qualification, exposure measurement and specialist input limit the
scale. No cost, timeline or laboratory capacity has been estimated.

Phase, allele function, tumour context and organ function remain unknown. Other limitations
include indirect transfer between models, incomplete source coverage, publication bias,
unmeasured exposure and the absence of experimental efficacy or safety data. Additional
computation cannot resolve these unknowns on its own.

## 8. Reproducibility and delivery status

The [website review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-challenge-review-20260919.md)
records the live rules, rubric, template and organizer clarifications checked on
September 19. The running public app and Space metadata still point to the established
public revision. The official task accepts mechanism-grounded hypotheses for further
investigation; established efficacy is not a prerequisite. Everolimus has existing
approved uses and remains an optional, model-qualified candidate for that investigation,
not a rescue priority. An investigational compound used as a mechanism control is not
being submitted as a market-approved repurposing candidate.

```bash
uv run python scripts/track2_evidence.py check
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/track2_evidence.py track1
uv run python scripts/track2_release_v10.py verify results/feat009/jvv7_track2_research_v10
uv run python scripts/track2_release_v11.py verify results/feat009/jvv7_track2_research_v11
uv run python scripts/track2_release_v12.py check
uv run python scripts/track2_release_v12.py build results/feat009/jvv7_track2_research_v12
uv run python scripts/track2_release_v12.py verify results/feat009/jvv7_track2_research_v12
```

The new v12 package binds this report, the updated pitch/deck, a video-description
draft and website review to the unchanged v10 scientific ledger, validation plan and
falsification review. Earlier snapshots and their bound inputs remain preserved.
The historical baseline checker reproduces historical decisions; the v10 decisions
remain current. Local checks establish integrity and declared invariants, not clinical
validity, eligibility, a judging score or upload readiness.

Use [the v12 slides](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v12.html)
and [aligned script](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-pitch-v12.md).
The seventh page carries the complete required acknowledgement and must be included
within the three-minute video. The [video-description draft](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-video-description-v12.md)
also includes that acknowledgement and detailed AI disclosure. Rehearsal, recording,
a playable YouTube/Vimeo URL, final owner review and live authenticated checks remain open.

The portal requires a PDF or Markdown report with participant/team identity in its
filename, a GitHub URL and the video link. Use the packaged `jvv7_track2_report_v12.md`.
Three entries are allowed; only the latest is reviewed. The workbook's older one-entry
wording is superseded by the live instructions and organizer announcement. No remaining
quota was checked, and no upload or submit callback was invoked. The full submission
requires provider/plan/data-handling disclosure; unresolved settings are not silently
attested. Organizer clarification says the later-publication dataset citation is not
an extra Track 2 report requirement at present.
[Instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/submit_track2.py),
[quota update](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/10),
[dataset-citation clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/13).

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
v5 editorial revision, v6 story/design rebuild or v9 adversarial revision. The v9
review is the main agent's author audit, not a new independent panel review.
The v10 cycle used Firecrawl retrieval tools and complementary public primary APIs;
no new agent-synthesis job was deliberately invoked. Retrieval processing can still
involve external providers. Current routing/training/retention were not audited.

The v11 presentation and v12 website-alignment work used local rendering and
public-source checks; no new external model provider or protected payload was added.

K-Dense BYOK was installed and smoke-tested previously. No inference or provider login
was recorded in that setup; installation produced no scientific result.

This work uses public literature and permitted derived summaries. Protected reads, raw
VCF records/subsets and clinical narrative were not sent through this workflow. The slides
are rendered locally without external images, fonts or model calls; slide generation adds
no new model provider. Historical single-provider attestations describe earlier sessions,
not the expanded workflow. Manuscript embargo and local deletion obligations remain in
force. No family contact, treatment or submission occurred here.

## 10. Methods answers aligned to the official template

These answers follow Track 2 cells A7–A17 of the organizer's workbook. The report
provides them directly; an additional spreadsheet upload is not required by the
inspected submission instructions. The AI-disclosure answer is required; the other
fields are recommended. No response claims clinical expert validation.

**A7 — Team/participant.** jvv7; individual submission identity. Final account identity
and submission receipt still require authenticated owner review.

**A8 — Variant/mechanism-to-drug approach.** Start from the preserved Track 1 ranked
BUB1B pair. Separate allele predictions and unconfirmed phase from demonstrated
gene-level biology. Review BUBR1/checkpoint, downstream stress and tissue-function
mechanisms; search market-approved candidates, contrary studies, exposure and safety.
Retain everolimus only as an optional mechanistic probe, HCQ as reserve and other
candidate dispositions in section 5. Qualify the model and prospective hypothesis
before an intervention; require function, safety, exposure and replication to advance.

**A9 — Generative-AI provider, tier and data handling.** OpenAI Codex/API tier, with
owner-attested no training on content; not an independent account audit. Firecrawl's
self-hosted service used Fireworks-hosted GLM through owner-confirmed credit-based API
access; training/retention settings remain unverified. Google DeepMind AlphaGenome
Atlas supplied precomputed API/download outputs, not on-demand inference; no broader
plan or account data-policy assertion is made. Section 9 contains the full disclosure,
output-term qualifications and historical scope. Unknown settings remain a final
review item, not a no-training attestation.

**A10 — Automated versus curated identification.** LLM-assisted public search and
literature synthesis supported candidate discovery. Author/agent source adjudication
and rule-based ledgers determine the reported decisions; they are not an automatically
validated efficacy predictor. Deterministic scripts check provenance, consistency,
conversions, figures and release hashes.

**A11 — Curation.** Selected primary sections or indexed abstracts were compared with
model-generated proposals and older interpretations. Read depth, retrieval failures,
model/compound identities, positive and negative findings, and decision changes are
logged. Earlier sessions include independent agent checks; the recent v9/v10 author
reviews and this website review are not new independent panels or clinician reviews.
The missing Goutas concern, distinct rapalog effects, wrong bibliographic identifier
and source-access gaps remain visible rather than silently corrected away.

**A12 — Public versus proprietary evidence.** Drug/target evidence uses public
literature, trial registries and official labels. No proprietary drug-response dataset
was supplied. The starting case derives from the gated challenge genome and permitted
derived findings, so the entire project is not described as public-input-only. Raw
subject records and narrative stay local; external literature calls use public material
and permitted summaries only.

**A13 — Public sources.** Primary journal papers and indexed records via Europe PMC/
PubMed, ClinicalTrials.gov, DailyMed and relevant regulatory sites supply drug and
mechanism evidence. Public AlphaGenome precomputed resources add annotation context,
not drug response or phase. The source ledger, exposure ledger and individual review
notes preserve identifiers, query plans, reading limits and model-transfer objections.
Commercial search/model services are tools, not independent scientific sources.

**A14 — Proprietary/gated sources.** The organizer-provided single-subject WGS and
phenotype inputs under the signed access terms informed earlier local Track 1 analysis.
Only permitted derived outputs enter this report. No other proprietary experimental,
clinical or drug/target evidence is claimed.

**A15 — Mechanism characterization.** The stop-gain is compatible with loss of function,
but endogenous RNA decay versus truncation is unknown; the missense's residual function,
instability or dominant-negative effect is unmeasured. Gene-level BUBR1 dysfunction can
impair checkpoint/attachment control and chromosome segregation. Everolimus acts on
mTORC1, a downstream hypothesis, and does not replace BUBR1. Branch A needs qualified
pathway excess plus a functional deficit; branch B separately needs relevant dynamic-flux
and regenerative deficits. Neither has been demonstrated for the selected pair.

**A16 — Time/effort.** Research and revisions are recorded across dated sessions beginning
September 8. Total person-hours, compute time and API/laboratory costs have not been
aggregated or estimated. Search-call counts and local test runtimes are not estimates
of total effort. Per-call timestamps and reproducible commands are available; no cost,
throughput or clinical timeline is promised.

**A17 — Method abstract (under 500 words).**

We assess approved-drug hypotheses for BUB1B-associated mosaic variegated aneuploidy
using permitted derived variant findings, public molecular evidence, drug studies,
trial records and regulatory labels. We separate gene-level mechanism from unmeasured
allele function and phase, and constitutional tissue function from tumour killing.
LLM-assisted discovery is followed by source adjudication with explicit reading depth,
retrieval failures, model identity and contradictory evidence. No new biological
experiment is reported.

Everolimus remains an optional, model-qualified mTORC1 probe rather than a comparative
rescue priority. Hydroxychloroquine remains reserve. A continuing falsification search
retains positive partial-inhibition findings alongside BUBR1-loss, regeneration and
normal-tissue safety concerns. Two prospectively separate hypotheses require either
pathway excess with a functional deficit or relevant dynamic-autophagic-flux and
regenerative deficits; neither is established for the selected pair.

The proposed validation compares endogenous genotype/phase alternatives and corrected
models, randomizes treatment, blinds scoring, and measures graded exposure, tissue
function, first-division events, daughter fate, regeneration and recovery. Advancement
requires functional benefit, acceptable deficient-normal safety, justified exposure
and replication. Cell loss or survivor selection cannot substitute for rescue.
Clinical exposure margins remain unknown.

The contribution is a reproducible framework for deciding what to test and what to
reject, with public code, evidence ledgers and explicit stop rules. Reuse in other
individuals or diseases requires fresh model, mechanism, exposure and safety qualification.
Indirect evidence, limited source coverage, missing biological observations and
unverified provider settings constrain interpretation and delivery readiness.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
