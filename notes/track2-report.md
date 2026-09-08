# Track 2 research proposal: test the therapeutic window, not just the target

**Participant:** jvv7 · **Version:** research draft 1 · **Date:** 2026-09-08

**Repository:** https://github.com/Vijayavallabh/mva-hackathon-2026

**Status:** computational evidence synthesis and proposed experiments only. No drug was
tested in this subject, no treatment is recommended, and no Track 2 entry has been uploaded.
A recorded three-minute pitch and hosted video URL remain outstanding. This is a
competition research report, not a clinical treatment plan or manuscript submission.

## Executive conclusion

The owner reports that our first Track 1 submission achieved 100 rank points and F-max 1.
The selected BUB1B pair therefore provides a defensible competition starting point for
mechanistic research. We have not independently inspected the portal receipt or verified
uploaded bytes, and **trans phase remains unconfirmed** by our local analyses. Neither a
leaderboard match nor a pathogenicity prediction supplies a drug-response experiment.

We propose two **conditional preclinical hypotheses**, not two medicines to administer:

| Hypothesis | Candidate | Required observation before advancement |
|---|---|---|
| Attenuate an abnormal downstream growth/stress pathway | Everolimus | Demonstrate excessive mTORC1 activity in the relevant genotype and functional improvement without harming deficient non-cancer cells |
| Exploit tumour lysosomal dependence | Hydroxychloroquine | Demonstrate tumour killing within an exposure-supported window that spares matched non-cancer BUB1B-deficient cells |

Temsirolimus is a clinical-evidence benchmark, not an additional independent discovery.
The ten entries other than the two conditional screens are not promoted as therapeutic
leads. The complete ledger contains twelve
entries: two conditional screens, one benchmark, three deprioritized hypotheses and six
exclusions. These are manually reviewed research decisions, not efficacy rankings.

The central innovation is an explicit **matched-normal safety requirement**: constitutional
chromosome instability may make non-cancer cells vulnerable to the same interventions
that appear attractive against aneuploid cancer. A positive tumour assay alone is therefore
insufficient. No candidate currently has direct intervention evidence for this exact pair
or an established clinical exposure margin.

## 1. What the genetic result does—and does not—establish

Our genome-wide workflow, targeted recall and phase audits are reproducible in the
[Track 1 evidence audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track1-evidence-audit.md)
and [phase-connectivity notes](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/phase-connectivity.md).
The submitted leading pair is GRCh38 chr15:40209701 T>G, p.Leu737Ter, and
chr15:40220612 T>G, p.Asn1002Lys, annotated on ENST00000287598.11. These are submission
variants, not newly disclosed raw records. The local v4 CSV and report are preserved
byte-for-byte; current-file hash verification is not independent evidence of uploaded bytes.

The stop-gain is consistent with loss of function, but transcript decay and residual
protein have not been measured. The missense allele has computational support in the
pinned annotation; its stability, folding, interaction partners and residual function
have not been established. We do not label it experimentally proven loss of function,
gain of function, dominant-negative, or a druggable misfolding defect. Biallelic BUB1B
disruption is a known MVA mechanism at the gene level.
[Hanks et al., 2004](https://doi.org/10.1038/ng1449)

Our working model is impaired BUBR1 function/availability. BUB1B is the gene; BUBR1/BubR1
is its protein. BUB1 is a related but different protein. Published MVA-cell replacement
experiments show that both reduced abundance and function-specific defects can matter.
Consequently, increasing protein abundance is not by itself evidence of successful rescue.
[Suijkerbuijk et al., 2010](https://doi.org/10.1158/0008-5472.CAN-09-4319)

We retain cis, trans and residual-function alternatives in the proposed experimental
controls. Historical ranking sensitivity is not a probability of causality. The low-level
copy-number screening signal is not a clinical karyotype, a tumour assay, or evidence of
drug sensitivity. No pathway activity, tumour fusion status, current cancer stage,
medication list, renal filtration measurement or treatment response is supplied by this
analysis. Do not assume active cancer or a particular ongoing regimen.

## 2. Mechanistic chain and intervention direction

BUBR1 participates in the mitotic checkpoint complex, which restrains APC/C–CDC20 until
chromosome attachment is appropriate. Its kinetochore-associated functions also help
balance phosphorylation through PP2A-B56 recruitment. Disruption can increase chromosome
missegregation. **Chromosomal instability** is an ongoing error process; **aneuploidy** is
an abnormal chromosome-number state. A measurement of one does not quantify the other.
[Gama Braga et al., 2020](https://doi.org/10.1016/j.celrep.2020.108397)

```text
Selected BUB1B alleles (phase and exact functional effects unresolved)
                         |
            hypothesized BUBR1 dysfunction
                         |
          checkpoint / attachment disturbances
                         |
        chromosome missegregation and cell stress
                  /                        \
     Non-cancer developmental tissues       Tumour compartment, if present
     preserve function and viability        kill tumour while sparing normal cells
                  \                        /
          require a measured differential benefit
```

The broad phenotype spans malignancy, renal involvement, growth impairment, muscular
abnormalities and adverse developmental history. This motivates testing multiple tissue
contexts, not claiming one pathway explains every finding. Renal calcification is not
equivalent to renal failure. Family reproductive history remains a separate inheritance
signal, not a proband abnormality or a treatment target. A drug cannot be assumed to
reverse developmental changes that have already occurred.

The C-terminal domain is frequently described as a pseudokinase, but its catalytic status
has been debated: structural/cellular studies supported a noncatalytic stability role,
whereas another study reported catalytic activity and CENP-E phosphorylation. Our proposal
does not require resolving that controversy. Neither interpretation justifies inhibiting
an already compromised checkpoint protein as constitutional therapy.
[Suijkerbuijk et al., 2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[Huang et al., 2019](https://doi.org/10.1038/s41422-019-0178-z)

## 3. Search, selection and evidence quality

This is an **adaptive rapid scoping review**, not an exhaustive systematic review or
meta-analysis. Public searches used BUB1B/BUBR1 with mutation, deficiency, rescue,
SIRT2/NAD, mTOR, aneuploid stress and RMS trial terms through 2026-09-08. We searched the
web, Europe PMC, PubMed and ClinicalTrials.gov, then verified medicinal uses and warnings
against US labels and the relevant EU regulatory decision. Europe PMC and PubMed overlap;
they are not independent replications. Author reputation was not used as an evidence grade.

The fixed search implementation and provenance are documented in
[search notes](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-search.md).
The initial broad full-text queries were noisy; focused title/abstract queries were added.
Record retrieval counts are not counts of fully read or eligible studies. Key papers were
selected for mechanistic relevance, closest model, counterevidence or regulatory relevance.
Some evidence was accessible only at abstract level. This can miss details, unpublished
negative experiments, indexing updates and papers outside the retrieved pages/languages.

Each source has a claim, model, reading depth and limitation in
[the source ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-sources.json).
DOI/title verification establishes bibliographic identity, not scientific truth. We also
checked the corrigendum to the mouse allele study: duplicated Figure 2E sample images and
the corresponding mitotic-index method were corrected; this is neither a new drug trial
nor a replication of the mTOR result.
[Sieben et al., corrigendum](https://doi.org/10.1172/JCI144781)

For clinical evidence, we assess randomization, comparator, attrition, endpoints and
precision. For cells/animals, we assess allele match, tissue, intervention identity,
replication unit and functional endpoints. We do not apply an undifferentiated numerical
score or call animal evidence high-certainty clinical GRADE evidence. Most therapeutic
bridges here are low-directness hypotheses. No clinical MVA efficacy study was identified
in the bounded review; that is not proof none exists.

## 4. Candidate A: everolimus—conditional downstream modulation

The biological rationale is **conditional mTORC1 excess**, not a claim that every BUB1B
mutation activates mTOR. In a mouse allele study, mTORC1 substrate phosphorylation was
elevated in muscle of heterozygous X753 animals, whereas another mutant did not show the
same pattern. That study did not test rapalog rescue. Importantly, mouse L1002P models
human L1012P, **not** the submitted human Asn1002Lys. These allele differences require
measurement of the proposed pathway before drug screening.
[Sieben et al., 2020](https://doi.org/10.1172/JCI126863)

Everolimus inhibits mTORC1 and has approved pediatric TSC uses in a specific oral-suspension
formulation. This offers relevant formulation/monitoring experience, not MVA or RMS approval.
Its label warns about infections, renal injury, mucositis and important drug interactions.
Developmental vulnerability makes preservation of normal-cell growth and tissue function
part of the experiment, not an afterthought.
[Everolimus US label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)

**Advance only if:** the genotype produces reproducible excess phospho-S6/phospho-4EBP1,
drug exposure suppresses that excess, and an independently measured functional outcome
improves without worsened viability, differentiation, chromosome segregation or recovery
after washout. Suppressed cell proliferation alone is not constitutional rescue.

**Devil's advocate:** a mouse tissue-specific association is a weak bridge to this child;
mTOR inhibition could impede useful growth or protect stressed malignant cells through
adaptive processes. A trial-negative class analogue cannot be sidestepped by changing the
drug name. We therefore nominate everolimus for a gated experiment, not as the predicted
best clinical therapy. Without pathway excess, this arm stops.

## 5. Candidate B: hydroxychloroquine—tumour-only stress hypothesis

Experiments in trisomic fibroblasts and cancer cell lines identified aneuploidy-associated
sensitivity to selected stress-inducing compounds, including **chloroquine**. That is
not direct hydroxychloroquine evidence, not universal CIN selectivity, and not proof of
tumour specificity. Sensitivity in nonmalignant trisomic fibroblasts is especially relevant
to the hazard in a constitutional chromosome-instability syndrome.
[Tang et al., 2011](https://doi.org/10.1016/j.cell.2011.01.017)

Hydroxychloroquine is a pragmatic approved-compound hypothesis for lysosomal/autophagy
perturbation, with adult oncology pharmacodynamic experience. An adult phase I combination
study does not establish pediatric MVA/RMS efficacy, and neither target engagement nor
stable disease proves clinical benefit. We do not propose the combination as a treatment.
[Rangwala et al., 2014](https://doi.org/10.4161/auto.29119)

The label includes cardiac/QT, retinal, muscle/nerve and renal toxicity warnings. A
pediatric malaria indication does not resolve pediatric oncology safety. Plasma, whole-blood,
intracellular and lysosomal concentrations are not interchangeable exposure measures.
[Hydroxychloroquine US label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=34496b43-05a2-45fb-a769-52b12e099341)

**Advance only if:** a validated tumour model is more sensitive than matched deficient
non-cancer cells at justified exposure, with dynamic flux measurements and orthogonal
cell-death assays. Lower metabolic-dye signal is insufficient. If the relevant tumour
model is unavailable, retain this as a hypothesis rather than claiming a therapeutic window.

**Devil's advocate:** this may be a broadly toxic lysosomal poison in the relevant context.
Constitutional aneuploid-cell depletion could worsen organ function. Equal or greater
normal-cell sensitivity is a stop result, even if tumour killing looks impressive.

## 6. Temsirolimus: retain both clinical results

| Study | What was compared | What can be inferred |
|---|---|---|
| ARST0921, randomized phase II, first relapse | Temsirolimus versus bevacizumab, each with vinorelbine/cyclophosphamide | Favoured the temsirolimus-containing regimen for EFS; not a comparison against chemotherapy alone |
| ARST1431, randomized phase III, intermediate risk | VAC/VI plus maintenance, with or without temsirolimus | Did not demonstrate improved three-year EFS from adding temsirolimus |

The relapse study randomized 87 participants; it was an active-comparator selection trial
and did not show a significant overall-survival difference. The later phase III analysis
included 297 evaluable participants from 325 enrolled. Three-year EFS was 66.8% with
temsirolimus versus 64.8% without it: HR 0.86, 95% CI 0.58–1.26, p=0.44. These populations,
backbones and trial questions differ; the results must not be pooled casually or presented
as contradictory answers to an identical question.
[Mascarenhas et al., 2019](https://doi.org/10.1200/JCO.19.00576),
[Gupta et al., 2024](https://doi.org/10.1016/S1470-2045(24)00255-9)

The US label approves temsirolimus for advanced renal cell carcinoma, not MVA/RMS.
We retain it as a benchmark that prevents overclaiming a novel rapalog solution. The
subject's clinical setting and eligibility for either historical trial are unknown.
[TORISEL US label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=95b7dc92-2180-42f1-8699-3c28f609e674)

Two additional phase II studies constrain enthusiasm without erasing exceptions. Pediatric
temsirolimus monotherapy missed its prespecified early-response threshold in all three
tumour cohorts, but one RMS participant had a partial response confirmed at week 18.
Therefore, “no RMS response ever occurred” would overstate the negative result. A separate
cixutumumab/temsirolimus sarcoma study observed no objective responses in 43 response-evaluable
participants, with relevant toxicities. Neither single-arm study establishes BUB1B-specific
effects or the safety of constitutional mTOR inhibition.
[Geoerger et al., 2012](https://doi.org/10.1016/j.ejca.2011.09.021),
[Wagner et al., 2015](https://doi.org/10.1002/pbc.25334)

## 7. Attractive alternatives that did not survive review

| Entry | Reason not promoted |
|---|---|
| Sodium phenylbutyrate | General chaperone hypothesis; no demonstrated Asn1002Lys folding defect or BUBR1 rescue. ER-stress findings in diabetes are a distant bridge; renal handling and sodium load matter. [Primary study](https://doi.org/10.1126/science.1128294), [label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=463a36fa-3eb2-4326-8bd0-c8c7a11bca3a) |
| Bortezomib | Strong cell-culture activity did not reliably translate to pediatric solid-tumour xenografts. Global proteasome inhibition is not precise protein repair; neuropathy/cytopenias are concerns. [Primary study](https://doi.org/10.1002/pbc.21214), [label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1521d321-e724-4ffc-adad-34bf4f44fac7) |
| Metformin | AICAR findings cannot be transferred by pathway name. Millimolar cancer-cell effects require exposure scrutiny; high-dose genotoxicity and renal restrictions oppose an automatic low-risk designation. [Primary study](https://doi.org/10.1016/j.fct.2022.113129), [label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=8cd5555c-f6b2-28d8-e053-2a95a90a5f1e) |
| Gentamicin | A premature stop motivates readthrough research, not chronic antibiotic administration. Endogenous transcript survival and functional protein restoration are unknown; nephrotoxicity and ototoxicity are major objections. [Label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0cce2238-28d3-4280-b520-ffc3067a2ffa) |
| Ataluren | Early readthrough models are not BUB1B rescue; EU conditional authorisation was not renewed in March 2025. It is not a currently EU-approved shortcut. [Early study](https://doi.org/10.1038/nature05756), [EMA decision](https://www.ema.europa.eu/en/medicines/human/EPAR/translarna) |
| NMN / nicotinamide | Distinct interventions. NMN increased mouse BubR1 abundance; the lifespan intervention was a SIRT2 transgene. Nicotinamide reduced abundance in high-concentration cell assays. No approved MVA medicine or dietary change follows. [Primary study](https://doi.org/10.15252/embj.201386907) |
| Dasatinib plus quercetin | INK-ATTAC genetic removal of senescent cells in mice is not evidence for this drug combination in pediatric MVA. No verified clinical window. [Primary mouse study](https://doi.org/10.1038/nature10600) |
| Bubristatin / direct checkpoint inhibition | Research-tool activity is not an approved drug. Inhibition may worsen the proposed constitutional defect. Docking cannot establish restorative direction or safety. [Primary study](https://doi.org/10.1038/s41422-019-0178-z) |

These are research exclusions/deprioritizations, not assertions that a medicine is
universally ineffective or contraindicated for its approved indications.

## 8. Validation plan and explicit stop rules

No wet-lab work has been performed. The complete proposed design is in
[the validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation.md).
It requires an appropriately authorized laboratory and material access; no new patient
samples, family contact or external subject-data transfer is authorized by this proposal.

First characterize RNA, full-length protein, localization, checkpoint timing and actual
segregation errors in independent engineered clones. Use wild-type, single-allele,
trans-model and cis-model controls, with genetic correction as a positive rescue control.
Confirm engineered phase; do not confuse it with the patient's unresolved phase. Assess
endogenous expression and distinguish decay from truncation or stable dysfunctional protein.

Then measure pathway/flux phenotypes before drug screening. Keep constitutional and
tumour objectives separate. Include renal- and muscle-relevant non-cancer models where
feasible; lineage differences need explicit controls. A tumour line bearing the same gene
name is not automatically a model of this child's cancer. Initial single-agent work must
precede any combination hypothesis; shared target class does not count as independent evidence.

Randomize treatments within clone/day/plate blocks and blind image scoring. Wells receive
treatment; imaged cells are nested observations, not independent biological replicates.
Use independently derived clones and repeat-day cultures to assess reproducibility.
A pilot estimates variance and intraclone correlation; specify the minimum biologically
important effect and power the subsequent confirmatory design before collecting it.

Drug-specific exposure ceilings must be established from appropriately reviewed human
PK, formulation, protein binding, metabolites and planned assay conditions. No dose for
the child is proposed. Report unbound exposure where meaningful; do not compare whole-blood
troughs directly with nominal culture concentrations. An effect above a justified envelope
does not pass. No numeric clinical exposure margin has been calculated here.

Predefined stop outcomes include absent pathway abnormality; increased protein without
functional rescue; apparent error reduction explained by mitotic arrest or selective cell
death; benefit lost after washout; excess normal-cell injury; and no attainable exposure
window. Report negative results and all prespecified endpoints. Observed variability, not
the number of imaged cells, determines the strength of evidence.

## 9. Reproducibility, sensitivity and adversarial revision

```bash
uv run python scripts/track2_evidence.py check
uv run python scripts/track2_evidence.py sensitivity
uv run python scripts/test_track2_evidence.py
uv run python scripts/track2_evidence.py track1
```

The candidate ledger supplies every decision's supporting sources, counterevidence,
regulatory boundary, exposure gap and falsification criterion. The ablation removes
other-allele animal support, other-compound/cancer support, or requires direct-pair evidence
and a measured exposure margin. Neither conditional screen survives the strict direct-pair
or measured-margin requirement. This is a useful limitation, not a failed attempt to claim
clinical validation. It is not a fitted ML model or calibrated drug-ranking algorithm.

The [revision log](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-devils-advocate.md)
records why tempting claims were weakened or rejected. Repeated challenges include allele
identity, kinase controversy, opposite drug directions, normal-tissue toxicity, negative
randomized evidence, regulatory changes, publication corrections and assay confounding.

## 10. Impact, innovation, scalability and limitations

**Potential impact:** a falsifiable route to discovering useful differential responses,
with early rejection of compounds likely to worsen systemic vulnerability. We do not
estimate survival benefit, clinical efficacy or chances of winning from the available evidence.

**Innovation:** pair-specific functional characterization linked to a two-context benefit/harm
test and an auditable rejection ledger. The novelty claimed is the proposed evaluation
framework and its application, not discovery of mTOR biology, autophagy or a new compound.

**Scalability:** the lightweight ledgers and offline checks can be reused for another
chromosome-instability genotype by revisiting its mechanism, evidence and tissue model.
No large GPU job, proprietary model or gated-data redistribution is required. Laboratory
throughput, clone construction and assay qualification—not inference compute—are likely
the main resource requirements. Cost and delivery time require a laboratory quote; none
has been fabricated.

**Limitations:** unresolved phase and allele function; no tumour/functional measurements;
unknown regimen and organ function; indirect model transfer; incomplete literature coverage;
potential publication bias; uncertain exposure; no clinical efficacy study for this pair;
no performed experiments and no hosted pitch yet. Even a favourable laboratory result
would require specialist-led translational, ethical and safety review before any clinical use.

## 11. AI use and data handling

OpenAI, Codex, **API tier**. The owner attests that data is **not used to train** the
provider's models and that no other AI providers have been used. This is an owner
attestation, not an independent account audit or a zero-retention claim. AI assisted
public-literature retrieval, coding, synthesis and adversarial review. The preferred
external search/image services were not authenticated or used for research generation;
no additional model provider was introduced. Raw subject reads, variant records and
phenotype narrative were not supplied to external services; only permitted derived
results and public literature informed this work. Proposed experiments are explicitly
separated from measured computational results.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
