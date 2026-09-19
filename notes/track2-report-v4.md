# Preserve normal tissue before pursuing tumour vulnerability

## A falsifiable BUB1B-guided drug-repurposing proposal

Participant **jvv7** · **research draft 4** · 2026-09-19

Repository: https://github.com/Vijayavallabh/mva-hackathon-2026

**Research only. No experiments performed, no established efficacy, no clinical
exposure margin, and no treatment recommendation. Trans phase remains unconfirmed.**
This is a new synthesis, not a modification of any uploaded Track 1 file or earlier
Track 2 snapshot. The pitch materials are not a recorded/hosted video. Final provider
disclosure verification, owner review, live portal checks and submission remain open.

## Executive decision

Our proposal asks whether a drug can improve function in BUB1B-deficient non-cancer
cells, or selectively suppress a relevant tumour, without worsening the constitutional
vulnerability. Those are different objectives and require different success criteria.

**Everolimus is the sole conditional constitutional research priority:** first establish
excess mTORC1 activity in a qualified model, then test whether modulation improves
function at a defensible exposure without injury. It is not a predicted best treatment.
**Hydroxychloroquine (HCQ) remains reserve.** **Pralatrexate remains an optional
fusion-positive rhabdomyosarcoma (RMS) tumour-only horizon**, not BUBR1 repair.

The distinguishing contribution is a **matched deficient-normal safety requirement**
combined with complete cell-fate tracking. Killing abnormal cells, blocking their entry
into mitosis, or letting them escape arrest can improve a surviving-cell statistic
without restoring useful division. A proposal that measures only tumour potency or
protein abundance would miss that distinction.

The expanded literature does not promote a new drug. It improves controls, rejects
unsupported exposure bridges and preserves both positive findings and contrary evidence.
The decisive next evidence is experimental; more agreement between language models is
not replication. This report integrates the adjudicated GLM supplement rather than
reproducing its uncorrected proposals.

## 1. Genetic starting point and scope

The owner reports Track 1 scores of 100 rank points and F-max 1 on the first submission.
The receipt and uploaded-byte identity have not been independently archived. The selected
pair is GRCh38 **chr15:40209701 T>G, p.Leu737Ter**, and **chr15:40220612 T>G,
p.Asn1002Lys**, annotated on ENST00000287598.11. These are permitted submission-derived
variants; the raw VCF and read data are not redistributed.

Our [genome-wide evidence audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track1-evidence-audit.md)
and [phase-connectivity audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/phase-connectivity.md)
provide reproducible methods. No eligible fragments connect the pair directly or through
the screened markers. Unphased coexistence and a competition answer-key match do not
establish trans, exact allele function, or a drug response.

BUB1B encodes BUBR1, a mitotic checkpoint and chromosome-attachment regulator; BUB1 is
a different protein. Biallelic BUB1B disruption is an established MVA mechanism at the
gene level. The stop-gain is consistent with loss of function, but RNA decay versus
truncated protein has not been measured. The missense allele has computational support,
not demonstrated instability, dominant-negative activity or residual function.
[Hanks 2004](https://doi.org/10.1038/ng1449),
[Suijkerbuijk 2010](https://doi.org/10.1158/0008-5472.CAN-09-4319)

The broad phenotype motivates renal-, muscle- and developmental-context safety testing
alongside the malignancy history. Renal calcification is not a renal-filtration measurement.
Parental reproductive loss is a separate inheritance signal, not a proband abnormality.
We do not infer active cancer, fusion status, treatment regimen, stage or organ function.
The low-level chromosome copy-number screening result is not a clinical karyotype or
drug-sensitivity assay. No single phenotype determines the intervention.

### What AlphaGenome adds

Precomputed Atlas AVI PHRED values are **33.7641** and **25.6084**, respectively; major
attributions reuse termination, AlphaMissense and conservation information. These are
calibration ranks, not disease probabilities or independent functional confirmation.
Local queries of the public merged-splicing archive returned **0.08699** and **0.04813**;
the public DNM1 comparison returned **2.522**. These unsigned aggregate magnitudes are
not splice fractions or validated clinical cutoffs. Small values do not prove normal RNA
processing or absent transcript decay. Tissue/junction-resolved evidence remains missing.

Neither output resolves phase or supports drug efficacy, ranking or exposure. See the
[authenticated audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphagenome-authenticated-results.md)
and [splicing audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/alphagenome-splicing-results.md)
for request scope, source/reference checks, hashes and limitations. No on-demand AlphaGenome
inference occurred; endogenous RNA/protein/function assays remain necessary.

## 2. Mechanism: test the direction before the drug

BUBR1 helps restrain APC/C–CDC20 until chromosome attachments are appropriate and recruits
PP2A-B56 to regulate attachment-associated phosphorylation. Dysfunction can generate
chromosome missegregation. Chromosomal instability is an error process; aneuploidy is a
chromosome-number state. The proposed interventions must not confuse suppressing a
checkpoint signal with repairing the underlying process.
[Gama Braga 2020](https://doi.org/10.1016/j.celrep.2020.108397)

Published work describes catalytic and noncatalytic interpretations of BUBR1's C-terminal
domain. The present proposal does not require settling that debate: localization,
checkpoint timing and faithful division are functional outcomes, whereas a kinase assay
alone is not a universal rescue criterion.
[Suijkerbuijk 2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[Huang 2019](https://doi.org/10.1038/s41422-019-0178-z)

| Objective | A result that could support advancement | A misleading substitute |
|---|---|---|
| Constitutional functional rescue | Reproducible functional gain with preserved division, viability and tissue-relevant function | More protein, fewer abnormal surviving mitoses, or a lower senescence-marker fraction alone |
| Tumour suppression | Relevant-model activity and a measured separation from deficient-normal injury at matched exposure | Nominal potency, unrelated-tumour responses, or indiscriminate toxicity |
| Durable tumour killing | Post-withdrawal loss of regrowth under a prespecified assay | On-treatment arrest or initial regression followed by recurrence |

## 3. Evidence process and reading limits

This is an **adaptive rapid scoping review**, not an exhaustive systematic review.
The baseline searches through 2026-09-08 produced a curated 53-source/12-candidate ledger.
Later selected-section/abstract reviews and official regulatory checks broadened coverage;
v4 integrates these and performs targeted primary-source rechecks on 2026-09-19. That date
does not mean all literature has been searched through September 19.

The archived expanded GLM work contains nineteen accepted jobs: eighteen completions and
one failed retrieval. The completions comprise ten abstract-based topic reviews, seven
corrective/adversarial passes and an initial PP2A answer rejected as source-grounded
evidence. Six overlong prompts were rejected before execution. Neither jobs nor the
35 supplied URLs are counts of validated studies or fully read papers.

The initial full-text retrieval limitations prompted indexed-primary-abstract comparisons.
Independent reviewers checked consequential claims against available primary sections,
abstracts and labels. Abstract silence cannot negate previously inspected Methods/Results.
The [GLM audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-review.md),
[constitutional review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-constitutional-review.md)
and [oncology review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-glm-oncology-review.md)
retain access failures, reading depth and rejected claims. Repeated model outputs are
not independent experiments. Citation identity checks do not validate a causal claim.

The new [v4 decision ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v4.json)
is a focused integration layer, not a replacement for the preserved historical ledgers.
It contains **32 source records and 11 research decisions**, linking each retained
direction to evidence, limitations and a stop rule. These counts are neither all-new
papers nor the exhaustive baseline. Reading-depth fields describe cumulative archived
reviews; the [independent v4 review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-v4-primary-review.md)
identifies what was specifically rechecked on September 19. An apparently strong cancer
experiment can still be highly indirect for constitutional rescue.

## 4. Conditional lead: everolimus

The rationale is a testable downstream phenotype, not universal mTOR activation by BUB1B
variants. Sieben and colleagues found elevated phospho-p70 S6 kinase and phospho-4EBP1
in **BubR1+/X753 gastrocnemius muscle**;
the +/L1002P comparison did not share that pattern. Mouse L1002P models human L1012P,
not the submitted Asn1002Lys. The study did not test rapalog rescue. Its H/L1002P animals
are biallelic disease models, not monoallelic carriers. Its published correction must
also be retained. This supplies a hypothesis to measure, not pair-specific intervention
evidence. Figure 5 depicts two animals/group for these blots, and the Methods state
that experiments were not randomized or blinded. Proposed phospho-S6 assays below
are future readouts, not a relabelling of that original measurement.
[Study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781)

Everolimus has approved uses, including specified pediatric TSC indications/formulations;
approval does not extend to MVA or RMS. Infection, mucosal, renal, developmental and
interaction concerns make deficient-normal function a necessary endpoint.
[US label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)

RMS clinical evidence is not uniformly positive or negative. Pediatric everolimus studies
showed pathway inhibition without objective responses; a later lenvatinib/everolimus
cohort had two partial responses among twenty RMS participants while missing efficacy
goals. Combination responses cannot be attributed to everolimus alone.
[Fouladi 2007](https://doi.org/10.1200/JCO.2007.11.4017),
[Santana 2020](https://doi.org/10.1002/cncr.32722),
[combination study](https://doi.org/10.1002/pbc.31692)

Temsirolimus supplies an important class benchmark. ARST0921 favoured its relapse regimen
over a bevacizumab-containing regimen, not chemotherapy alone. ARST1431 did not demonstrate
improved three-year EFS from adding temsirolimus: 66.8% versus 64.8%, HR 0.86,
95% CI 0.58–1.26, p=0.44, among 297 evaluable participants. Different populations and
backbones must remain distinct. A nonsignificant result is not proof of exactly zero
effect; neither trial tests constitutional everolimus rescue.
[ARST0921](https://doi.org/10.1200/JCO.19.00576),
[ARST1431](https://doi.org/10.1016/S1470-2045(24)00255-9)

A separate rapamycin experiment in nocodazole-arrested A549 cells increased **mitotic
slippage** in its death-versus-slippage comparison. That denominator is not all enrolled
cells, and this is not evidence of clinical everolimus harm. It does require complete
fate measurement before calling fewer abnormal mitoses rescue.
[Yamada](https://doi.org/10.1016/j.isci.2021.103675)

**Decision:** qualify pathway excess and assay performance first. Advance only if target
modulation and a prespecified functional benefit replicate while deficient-normal cells
retain function and justified exposure is respected. Pathway excess need not be exclusive
to one genotype or the earliest causal event to be modifiable; nevertheless, failure to
establish the proposed excess stops this specific mTOR rationale. Persistent injury,
unattainable exposure or nonreplication stops advancement. A negative result is useful.

## 5. Candidate decisions after expanded review

| Direction | Evidence worth retaining | Reason for current decision |
|---|---|---|
| HCQ — reserve | Adult everolimus/HCQ RCC study met its single-arm six-month PFS threshold; two partial responses among 33 evaluable participants. | No monotherapy comparator or pediatric RMS/deficient-normal window. Chloroquine sensitivity in trisomic fibroblasts is also a normal-tissue warning, not direct HCQ selectivity. [Haas](https://doi.org/10.1158/1078-0432.CCR-18-2204), [Tang](https://doi.org/10.1016/j.cell.2011.01.017) |
| Pralatrexate — tumour-only horizon | Regression in some fusion-positive RMS models, including RH4 regression followed by recurrence. | Model subtype, schedule-dependent toxicity and withdrawal outcomes constrain transfer. It is not BUB1B repair or established selective TYMS inhibition; thymidine rescue alone cannot identify a unique direct target. [Study](https://doi.org/10.1038/s41467-026-73749-y), [PTCL label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=cc3df863-c51c-49c5-283a-d6808fb49258&version=6) |
| Entinostat — deprioritized tumour direction | Model-dependent favourable combination results and genuine Chinese marketing approval for a defined breast-cancer setting. | Do not call globally unapproved. Prior RMS experiments include antagonism; daily mouse and weekly human schedules are not exposure-matched. Not a pediatric RMS indication or validated window. [2019](https://doi.org/10.1002/pbc.27820), [2024](https://doi.org/10.1038/s41598-024-66545-5), [NMPA](https://english.nmpa.gov.cn/2024-04/30/c_1049690.htm) |
| Vorinostat — deprioritized | An ERMS case had transient clinical improvement. | Progression and severe toxicity followed; paired PDX necrosis did not suppress growth/Ki67. A case exception is not controlled efficacy. [Case/PDX](https://doi.org/10.3389/fonc.2017.00327) |
| Niclosamide/TBX screen — deprioritized | Endogenous validation and RMS assays; a reformulated adult study improved the feasibility picture. | Micromolar nominal activity, some extrapolated EC50s, no deficient-normal safety window. Original and reformulated scheduled total-plasma samples cannot define free RMS exposure. [Screen](https://doi.org/10.1002/cam4.70303), [original PK](https://doi.org/10.1371/journal.pone.0198389), [correction](https://doi.org/10.1371/journal.pone.0202709), [reformulation](https://doi.org/10.1038/s41598-021-85969-x) |
| Posaconazole — deprioritized | RD xenograft growth inhibition, not eradication. | Liver histologic injury, formulation dependence and major interaction constraints. Nonsignificant enzyme comparisons do not erase histology. No nominal-culture/free-plasma ratio establishes a clinical margin. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8493378/), [label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0bdf77ae-3639-49c1-b7c7-533f9d073084) |
| PP2A compounds — excluded from approved-drug shortlist; retain mechanistic controls | Engineered PP2A-B56 recruitment improved alignment in published MVA cells. | The endpoint was fixed-cell alignment under arrest, not faithful daughter divisions. DT-061 specificity is disputed; different-compound isolated-PR65 binding/stabilization does not settle it. [Xu](https://doi.org/10.1242/bio.20134051), [Leonard](https://doi.org/10.1016/j.cell.2020.03.038), [Vit](https://doi.org/10.15252/embj.2022110611), [Naqvi](https://doi.org/10.1021/jacsau.6c00003) |
| Drug senolysis/HSP90 inhibition — excluded as a constitutional priority | Genetic senescent-cell clearance has BubR1-model evidence; D+Q/HSP90 studies provide favourable findings in other contexts. | Ercc1 drug studies are not BubR1 rescue; p21 protects muscle/fat but promotes the lens phenotype in the cited BubR1 model. HSP90 inhibition can deplete unstable BUBR1. [Baker 2011](https://doi.org/10.1038/nature10600), [Baker 2013](https://doi.org/10.1016/j.celrep.2013.03.028), [Zhu](https://doi.org/10.1111/acel.12344), [Fuhrmann](https://doi.org/10.1038/s41467-017-00314-z), [BUBR1 stability](https://doi.org/10.1158/0008-5472.CAN-09-4319) |
| Ataluren/gentamicin readthrough — excluded as current clinical candidates | Positive and negative context-dependent readthrough studies inform controls. | No selected-pair functional rescue; reporter/full-length/function are separate endpoints. Gentamicin toxicity is a major objection. EU Translarna authorization was not renewed in March 2025. [Roy](https://doi.org/10.1073/pnas.1605336113), [Bolze](https://doi.org/10.1038/s41598-017-01093-9), [EMA](https://www.ema.europa.eu/en/medicines/human/EPAR/translarna) |

These are research-priority decisions, not universal verdicts on approved clinical uses.
HCQ requires compound-specific flux and selectivity evidence to reopen; static LC3,
PBMC vesicles or another lysosomal inhibitor cannot supply it. Relevant positive and
negative adult HCQ trials remain in the preserved baseline review.

Additional baseline exclusions/deprioritizations also survive: sodium phenylbutyrate lacks
a demonstrated repairable missense-folding defect; proteasome blockade is not precise
BUBR1 repair; metformin/VIT responses lack a VIT-alone comparator and do not establish an
exposure window; NMN protein-abundance effects are not the lifespan effect of a SIRT2
transgene. Ordinary-ageing SIRT2 results are a different biological context, not a failed
same-model replication. Direct checkpoint inhibitors may oppose constitutional rescue.
See the [baseline review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-final-review.md),
[North](https://doi.org/10.15252/embj.201386907) and [Wu](https://doi.org/10.1111/acel.14027).

Two other corrections prevent accidental promotion: the redox paper's abstract versus
Results disagree on the ROS/AIF compound attribution, and its colony assay reseeded
viable survivors rather than measuring original-population survival. Statin/radiation
findings are tumour-damage hypotheses, not muscle rescue or a validated low-signature
eligibility rule. Both remain unpromoted.
[Chico](https://doi.org/10.1002/ddr.70304),
[Codenotti](https://doi.org/10.3390/cancers16050853)

## 6. Proposed validation: measurable gates, not invented results

The [v4 validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v4.md)
consolidates the prior design and corrected assay logic. It authorizes no laboratory
work, material acquisition, family contact or patient intervention.

1. **Qualify models.** Independently engineered wild-type, single-allele, cis and trans
   models, mock edits and corrected derivatives distinguish alternative mechanisms.
   Verify engineered phase without claiming to resolve the subject's phase.
2. **Measure the defect.** Endogenous RNA/protein, localization, checkpoint response,
   accurate division and lineage function precede drug selection. Protein abundance
   alone cannot pass. Add renal/muscle-relevant models only after qualification.
3. **Qualify target and exposure.** Confirm the proposed pathway phenotype; measure or
   credibly bound free-medium and relevant human exposure over the same schedule.
   Record parent/metabolite, formulation, matrix, binding and sampling time. Whole-blood
   trough, total-plasma peak and nominal culture concentration are not interchangeable.
4. **Track complete outcomes.** Enroll cells before exposure and account for accurate
   division, erroneous division, death, persistent arrest, slippage and tracking loss.
   Follow daughters and recovery. Use prespecified denominators, not survivors alone.
5. **Replicate before advancement.** Randomize within clone/day/plate blocks, blind
   scoring, and retain wells/clones—not cells—as the relevant clustering structure.
   Pilot variance informs a separate confirmatory power calculation. No power is claimed.

Constitutional improvement must survive a paired assessment of useful division and
deficient-normal tissue function. The tumour branch requires documented model subtype,
an oncology-selected comparator, single-agent controls and matched normal testing before
combination work. A prespecified interaction model is necessary to call synergy.
Reversible on-treatment benefit can be real; recurrence prevents a durable-killing claim,
not every pharmacological-benefit claim. Harmful rebound and persistent injury are stop
results. Zero detected injury is not proof of zero risk.

The [exposure ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-exposure.json)
contains eight public-study/label observations and unit-conversion checks, not dosing
recommendations. **All clinical exposure margins remain unknown.** No numerical safe
concentration, therapeutic ratio or dose for the child is proposed.

## 7. Rigor, impact, innovation and scalability

**Rigor:** preserve null and unfavourable findings, model/allele identity, reading depth,
exposure units and prespecified success/failure criteria. Remove indirect support and
the conditional lead loses its basis; require direct-pair rescue or measured exposure
and no candidate passes. That sensitivity is a limitation, not a calibrated drug score.

**Potential impact:** identify a useful intervention or reject a harmful idea early.
Neither a clinical benefit estimate nor a winning probability is supported.

**Innovation:** applying a genotype-aware, two-context benefit/harm assessment with full
cell-fate accounting. We do not claim discovery of mTOR biology, autophagy or these drugs,
nor prove that this framework has never been used elsewhere.

**Scalability:** fixed public evidence, transparent decisions and local checks can be
reused for other chromosome-instability hypotheses. Start with one qualified context
and one conditional agent; add lineages/backgrounds only after earlier gates pass.
Clone construction, assay qualification, exposure measurement and specialist input are
the actual bottlenecks. There is no fabricated cost, timeline or laboratory capacity.

Limitations include unknown phase/function, tumour context and organ function; indirect
model transfer; incomplete source coverage and publication bias; unmeasured exposure;
and no experimental efficacy or safety data. An honest research proposal can disclose
these unknowns; it cannot turn them into evidence by additional computation.

## 8. Reproducibility and delivery status

```bash
uv run python scripts/track2_evidence.py check
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/track2_evidence.py track1
uv run python scripts/track2_release.py verify results/feat009/jvv7_track2_research_v3
uv run python scripts/test_track2_release_v4.py
uv run python scripts/track2_release_v4.py verify results/feat009/jvv7_track2_research_v4
```

The new release binds the report, decision ledger, validation plan, pitch/deck and supporting
reviews to hashes. Earlier Track 1 v4 and Track 2 v2/v3 remain intact. Hashes establish
integrity/drift, not truth, signatures, clinical readiness or a portal receipt.

The three-minute narration and local deck require rehearsal, recording and a playable
YouTube/Vimeo URL. The official portal accepts a PDF or Markdown report with the participant
name, a GitHub URL and the video link, and reviews the latest entry. Provider, plan/tier
and relevant data-handling settings must be disclosed. The current submission-tab source
was rechecked; authenticated remaining quota and final live requirements were not.
[Official instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/raw/main/tabs/submit_track2.py)

## 9. AI disclosure and data handling

- **OpenAI / Codex, API tier:** owner-attested setting that content is **not used to train**
  OpenAI models. This is not an independent account audit or zero-retention claim.
  Assistance includes code, public-source research, synthesis and independent agent reviews.
- **Google DeepMind / AlphaGenome Atlas:** precomputed-output API and public downloadable
  merged-splicing assets; no on-demand model inference. The access route is recorded;
  no broader account training/retention setting is inferred. The
  [AlphaGenome Output Terms](https://deepmind.google.com/science/alphagenome/output-terms)
  and applicable non-commercial artifact conditions remain relevant. Extraction,
  serialization, tables and interpretation are modifications, not a new output licence.
- **Firecrawl self-hosted MCP / Fireworks-hosted GLM:** the archived public-literature
  jobs returned `accounts/fireworks/models/glm-5p3-flash`. On 2026-09-19 the owner
  confirmed **credit-based API usage**. This describes billing/access, not an
  independently audited plan or data policy. Fireworks **training and retention
  settings remain unverified**. This is an unresolved final-disclosure gate, not a no-training or zero-retention
  attestation. Local service storage can retain prompts/results; self-hosting is not
  local model inference. Earlier conditional Google/Vertex code paths do not establish
  their actual execution. No new GLM calls were made for this v4 integration.
- **K-Dense BYOK:** installed and smoke-tested previously; no inference or provider login
  was recorded in that setup. Installation is not another scientific result.

This integration uses public literature and permitted derived summaries. Protected reads,
raw VCF records/subsets and clinical narrative were not sent through this workflow.
No new provider was added for slide generation: the deck is rendered locally without
external images, fonts or model calls. Historical single-provider attestations describe
their earlier sessions, not this expanded workflow. Manuscript embargo and local deletion
obligations remain in force. No family contact, treatment or submission occurred here.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
