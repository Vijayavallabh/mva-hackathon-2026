# Track 2 public literature refresh, version 41

19-20 October 2026. This note adds a bounded current-literature check to the
frozen v40 presentation. It **does not change any drug disposition**: no rescue
priority is established; everolimus remains a mechanistic probe on HOLD, and
HCQ remains reserve. The selected BUB1B pair's phase, endogenous protein
deficit, useful function, safety, exposure margin and drug response remain
unmeasured.

## Search method and coverage

Searches used only public article indexes and public article records. The exact
query receipts, summaries and selected records are preserved under
`sources/public-literature-v41/` with SHA-256 values in
[the audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-audit-v41.json). No subject VCF, FASTQ, BAM,
phenotype document bytes or subject identifier were queried, transferred or
stored. The remote host was used only to observe idle hardware; no subject data
was sent there.

| Query | Date/index | Coverage result |
|---|---|---|
| BUB1B/BUBR1/MVA records in 2025-2026 | PubMed eSearch/eSummary/eFetch | 141 records found; 100 latest returned |
| BUB1B/BUBR1/MVA records from 2025 onward | OpenAlex title/abstract search | 206 records found; 100 latest returned |
| mTOR/rapalogs plus BUB1B/BUBR1/SAC/aneuploidy, 2025-2026 | PubMed | 13 records found |
| NAD/NMN/SIRT2 plus BUB1B/BUBR1/aneuploidy/CIN, 2025-2026 | PubMed | 7 records found |
| hTERT-RPE1 plus BUB1B/BUBR1/SAC/aneuploidy, 2025-2026 | PubMed | 2 records found |

The broad lists contained many indirect cancer biomarker papers and unrelated
'BUB1'-adjacent terms. Review therefore focused on records with direct MVA,
SAC/BUBR1 mechanism or developmental-CIN evidence, not on every returned title.

## What changed in the literature since the v40 source set

### 1. BUBR1 architecture: one protein, several endpoint-specific functions

Two 2025-2026 papers sharpen the central qualification problem. BUB1 and
BUBR1 scaffold the kinetochore fibrous corona through nonredundant assembly
branches, including a BUB1-ROD interaction uncovered after CENP-E depletion
[Cmentowski and Musacchio 2025](https://doi.org/10.1126/sciadv.ady6890).
The BubR1 TPR domain promotes MCC formation and MCC-APC/C interaction through
contacts with Mad2, Cdc20-APC/C, Apc2 and an intramolecular 'lasso'
[Zhang et al. 2026](https://doi.org/10.1038/s42003-026-10384-9).

**Proposal consequence.** These papers support adding three explicit corona/MCC
readouts to the first experiment: kinetochore BUBR1/MAD2/ZW10 localization,
MCC abundance or APC/C engagement, and durable checkpoint maintenance. They do
not make a BUBR1 abundance measurement sufficient: restored protein can be
mislocalized or fail to assemble an active checkpoint complex.

### 2. K250 is now even less suitable as a generic rescue control

A 2026 *Nucleic Acids Research* study reports that Aurora B phosphorylates
BubR1 at S16/S39, promotes K250 acetylation, sustains the fibrous corona and
maintains MCC stability. A K250 acetylation-mimetic rescued defects caused by
S16A/S39A phosphorylation mutants
[Choi et al. 2026](https://doi.org/10.1093/nar/gkaf1517).

**Proposal consequence.** K250 sits in an attachment-coupled regulatory axis,
not in a generic stabilizing slot. This strengthens the existing decision to
measure K250/S16/S39 state only as a mechanistic endpoint. It does **not**
promote a SIRT2/NAD intervention, make K250 acetylation universally beneficial
(or harmful), or convert a K250 mimetic into a valid generic rescue control.

### 3. Complex aneuploidy can injure stem cells through proteostasis and mitochondria

A 2026 Drosophila neural-stem-cell SAC model reports loss of stemness after
accumulation of complex chromosome gains/losses, with contributions from
proteostasis failure and mitochondrial dysfunction. ROS scavengers,
mitochondrial chaperones and apoptosis inhibition dampened selected
deleterious effects [González-Blanco et al. 2026](https://doi.org/10.1038/s41467-026-70521-0).
A related review places MVA and early developmental chromosome instability in
the same biological frame [Milán 2025](https://doi.org/10.1016/j.ceb.2025.102537).

**Proposal consequence.** This is the only new line that materially expands the
‘useful function’ endpoint set. Add mitochondrial integrity/proteostasis
markers—e.g. mitochondrial membrane potential, organelle morphology, a
proteotoxicity/ubiquitin-proteasome stress readout—with all-enrolled later
daughter outcome. These genetic Drosophila interventions are **not** drug
evidence for the child. They should be measured as injury mechanisms, not used
to justify antioxidant or anti-apoptotic treatment.

### 4. Heterozygous BUB1B, reproductive phenotypes and diagnostic scope

A 2026 recurrent-pregnancy-loss paper identified two novel heterozygous BUB1B
missense variants (p.W722R, p.A739S), found elevated premature chromatid
separation in probands' lymphocytes and reported a trend toward lower BUB1B
RNA/BUBR1 protein, classifying the variants as VUS
[Wei et al. 2026](https://doi.org/10.3389/fendo.2026.1838559). A 2026 *Human
Reproduction Update* review systematically searched PubMed, Embase and Cochrane
records through 12 January 2026 and found that BUB1B remains a candidate gene
whose aneuploidy-conception association requires further validation
[Ha et al. 2026](https://doi.org/10.1093/humupd/dmag012).

**Proposal consequence.** Heterozygous evidence cannot qualify this child's
compound pair. It nevertheless reinforces our proposed non-malignant
engineered comparator and boosts confidence that endogenous RNA/protein plus
segregation phenotypes are the correct first measurements. It also warns
against extending an MVA therapy claim toward reproductive indications without
a separate validated study.

### 5. MVA genetics continue to diversify without changing a BUB1B therapy claim

New reports include a CEP57 organizational mechanism for MVA2
[Nature Communications 2026](https://doi.org/10.1038/s41467-026-77795-4),
MVA in Mulibrey nanism/TRIM37 patients
[Hakonen et al. 2026](https://doi.org/10.1136/jmg-2025-111325),
a CEP57 MVA2 case report
[Viudes et al. 2026](https://doi.org/10.1515/jpem-2025-0643), recessive SMC5
variants in a near-tetraploidy/MVA family
[Diagnostics 2025](https://doi.org/10.3390/diagnostics15233022), and TRIP13
MVA syndrome 3 with sequential tumours
[Vempuluru et al. 2026](https://doi.org/10.1080/01676830.2026.2715719).
BUBR1 insufficiency has also been linked to cardiac ageing/heart failure in mice
[Pun et al. 2025](https://doi.org/10.1111/acel.70160), and BUBR1/STAT3
signalling to neonatal hypoxic-ischemic brain injury in a mouse model
[Chang et al. 2025](https://doi.org/10.1002/cbin.70033).

**Proposal consequence.** This diversity reinforces genome-wide candidate
selection and transferability planning rather than a single founder-gene
assumption. The BUBR1-specific ageing and nerve-regeneration papers remain
scope-limited: neither evaluates constitutional MVA, this pair, a human child,
or a drug rescue. They are not treatment evidence.

## No promotion found for everolimus, NAD/SIRT2 or HCQ

The targeted searches found **no 2025-2026 paper that tests everolimus,
sirolimus, NMN, nicotinamide, nicotinic acid, HCQ or another approved drug as a
rescue intervention for constitutional BUB1B-associated MVA**. No paper found
here changes the v21 disposition table, awards rescue priority, or supplies a
clinical exposure margin. Missing studies are not disproof; the appropriate
decision remains the prespecified qualification experiment.

The closest mechanistically relevant BUB1B paper is in adult castration/enzalutamide
-resistant prostate cancer: it shows BUB1B/CENP-E-dependent tumour growth and
CENP-E inhibition [Martinez et al. 2026](https://doi.org/10.1158/0008-5472.CAN-26-0874).
That result does not promote CENP-E inhibition or increased BUB1B activity for
constitutional MVA. It adds a reason to keep tumour and deficient-normal useful-output
endpoints separate.

## How v41 changes the proposal, without overclaiming

1. **Primary biological qualification remains unchanged:** endogenous BUBR1
   effect, independently attributable perturbation/restoration, and a useful
   functional endpoint in a proposed engineered hTERT-RPE1 comparator.
2. **Add three checkpoint-architecture readouts:** BUBR1/MAD2/ZW10 kinetochore
   corona localization, MCC/APC/C engagement, and durable checkpoint maintenance.
   A protein-abundance-only endpoint is insufficient.
3. **Add two injury mechanism panels:** mitochondrial integrity and
   proteostasis/ubiquitin-proteasome stress, interpreted alongside all-enrolled
   later daughter fate. These panels must be prespecified and analysis-ready
   before any intervention experiment.
4. **Treat the K250/Aurora-B axis as mechanism, not medicine:** measure K250
   acetylation with attachment state and checkpoint outcome; do not promote a
   NAD/SIRT2 intervention from that mechanistic link.
5. **Do not transfer heterozygous reproductive evidence, ageing phenotypes,
   nerve-regeneration findings, or adult cancer inhibitor results into a
   constitutional MVA treatment claim.**

## Failure/stop rules for the new v41 additions

| Claim to test | Support needed | Falsifier / stopping condition | Next discriminating action |
|---|---|---|---|
| BUBR1 restoration restores useful checkpoint architecture | Endogenous BUBR1 correction increases BUBR1/MAD2/ZW10 corona signal, MCC/APC/C engagement and segregation fidelity versus mock/single-allele controls | Restored abundance without corona/MCC improvement fails the architecture claim | Measure checkpoint maintenance and chromosome segregation after independent perturbation/restoration |
| Mitochondrial/proteostasis injury tracks complex aneuploid daughter fate | Prespecified correlation between injury markers and later daughter loss in the qualified model | Markers improve without later daughter survival/output, or injury improves while segregation worsens | Build a ranked, multiparameter injury index; test with blinded morphometrics |
| K250/Aurora-B state is a useful mechanistic marker, not a drug target claim | K250 state co-varies with attachment/checkpoint outcome after BUBR1 correction | K250 state improves without checkpoint/segregation benefit | Do not promote a NAD/SIRT2 or K250 intervention; proceed only with measured BUBR1 function |
| Heterozygous BUB1B reproductive evidence informs BUBR1 assay qualification | Independent non-malignant models show endogenous dosage effects on SAC fidelity | Heterozygous missense evidence transfers to compound nonsense/missense function without direct pair-level testing | Use heterozygous evidence as comparator rationale only; not a treatment claim |
| MVA genetic heterogeneity affects transferability | New genes produce distinguishable centriole/SAC/CIN injury mechanisms | A single mechanism model cannot distinguish different MVA subtypes | Build a context-transfer checklist per gene/assay rather than declaring universal applicability |

## Reproduction

```bash
uv run --no-project python scripts/check_track2_literature_v41.py
uv run --no-project python scripts/track2_public_review_v41.py
uv run --no-project python scripts/check_track2_harness.py
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
```

The literature script checks public receipt hashes, required source statements,
absence of subject-data markers, and preservation of v40. It **does not** make
a biological claim or verify full-text claims not captured here.
