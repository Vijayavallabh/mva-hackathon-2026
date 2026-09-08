# Track 2 final scientific and exposure review

Review opened 2026-09-08 at baseline `1a97a0e`; scope is feat-009 only.
This is a research-report review, not clinical clearance or a treatment recommendation.
Track 1 submitted files and the earlier Track 2 v1 snapshot remain immutable. Trans
phase remains unconfirmed. No subject files are needed for the literature search.

## Review specification

1. Challenge the intervention direction, allele/model transfer, functional endpoints,
   tumour-versus-normal selectivity, contradictory trials and regulatory eligibility.
2. Extend the previous searches through 2026-09-08, including RMS rapalogs, lysosomal
   and proteostasis dependencies, pediatric pharmacokinetics, adult hydroxychloroquine
   oncology trials and alternative RMS comparators. Follow relevant primary citations.
3. Separate retrieved records, screened summaries, selected text sections and fully read
   papers. Record failures, limits and overlapping records. Do not claim all literature.
4. Extract exposure with the actual analyte, units, matrix, sampling endpoint, population
   and experimental conditions. Unit conversion is not a therapeutic margin. Do not
   equate whole blood, plasma, unbound medium and intracellular lysosomes.
5. Revise decisions when evidence weakens them; require actual functional rescue or
   tumour killing and matched-normal safety, not merely target engagement.
6. Test the exposure checks and retrieval failure handling. Independently review the
   revised work, run init and disclosure checks, archive a new research snapshot and
   commit/push the intended changes. Do not upload a Track 2 entry in this review.

The search script is `scripts/track2_review_search.py`; its fixed queries contain only
public gene, drug and disease concepts. Retrieved public literature lives in ignored
`results/feat009/` directories. Preferred external skill services lack credentials;
public databases, official labels and local tables are used without another AI provider.

## Decision after review

**Retain one phenotype-first research priority: everolimus, conditional on measured
mTORC1 excess. Demote hydroxychloroquine (HCQ) to a reserve hypothesis.** Temsirolimus
remains an oncology evidence benchmark. The twelve-entry ledger now has one conditional
screen, one benchmark, four deprioritized entries and six exclusions. No medicine has
established benefit for this exact genotype, a verified normal/tumour exposure window,
or clinical clearance. A well-supported decision to stop is an acceptable experimental
outcome; the competition result is not guaranteed.

Everolimus is retained because the proposed first question is a falsifiable pathway
phenotype and pediatric PK information exists—not because a therapeutic window has been
demonstrated. HCQ requires an additional compound-transfer assumption, has no reviewed
direct RMS HCQ exposure/response bridge, and its proposed vulnerability also threatens
non-cancer cells. This is a prioritization judgment, not a head-to-head efficacy finding.

## Literature coverage and reproducibility

The supplementary search retrieves twelve fixed Europe PMC title/abstract query sets:

| Query | Retrieved / reported hits |
|---|---:|
| BUBR1/BUB1B interventions | 418 / 418 |
| MVA interventions | 13 / 13 |
| RMS rapalogs | 78 / 78 |
| RMS lysosome/proteostasis | 81 / 81 |
| Pediatric everolimus PK | 54 / 54 |
| HCQ oncology PK | 99 / 99 |
| HCQ cancer phase/randomized trials | 82 / 82 |
| Aneuploid stress/selectivity | 92 / 92 |
| RMS metformin | 4 / 4 |
| RMS bortezomib | 14 / 14 |
| BUBR1 readthrough/stabilization | 3 / 3 |
| RMS chemotherapy comparators | 39 / 39 |

These are overlapping sets: **941 distinct database source/ID records**, not 941 fully
read studies. Queries are capped at 1,000 records each; none reached that cap. DOI groups
are recorded separately. Preprints, final publications, related trial reports and
conference abstracts still require study-level linkage; they are not independent
replications. The prior PubMed/ClinicalTrials.gov searches and primary-source web/citation
following complement this retrieval but do not establish independent database coverage.

```bash
uv run python scripts/track2_review_search.py search results/feat009/final-review-search-v2-20260908
uv run python scripts/track2_review_search.py fulltexts results/feat009/final-review-fulltexts-v2-20260908
uv run python scripts/track2_evidence.py sources results/feat009/source-verification-v5
uv run python scripts/track2_exposure.py
```

Each command creates a **new** directory; use a new suffix for reproduction. The final
source ledger has 53 entries, including 23 added records. It distinguishes abstract-only
reading from selected methods/results/PK-table reading. No independent dual full-text
screening of all retrieved records, Embase subscription search, complete forward-citation
census, non-English full-text review or unpublished-result search was performed. This is
an expanded rapid scoping review, not PRISMA-complete systematic evidence or “all literature.”

Europe PMC's XML endpoint returned 11 usable articles and twelve HTTP 404 responses in the
23-article supplementary archive. A PMC record can exist without reusable full-text XML.
Those failures remain explicit; browser-accessible official text and abstracts supported
the corresponding selected reviews. CAPTCHA pages were not treated as papers or bypassed.
The earlier mixed run had eight full-text failures, and the first 14-article retry had
eleven. Preserve those logs. A script edit during the first mixed run also made its
end-of-run script hash an unreliable execution pin; use the later search-only snapshot,
which captures the script hash at import. None of these limitations is zero-hit evidence.

## Scientific findings that change or constrain the proposal

### 1. Gene association is not allele-specific pharmacology

The mouse mTOR finding is tissue- and allele-specific, and the study did not demonstrate
rapalog rescue. Mouse L1002P represents human L1012P, not human Asn1002Lys. The correction
concerns images and a method, not an independent reproduction. Protein abundance,
checkpoint timing, attachment correction and chromosome segregation remain separate
readouts. Neither cis/trans engineering nor a literature analogue resolves the subject's
phase. [Sieben study](https://doi.org/10.1172/JCI126863),
[corrigendum](https://doi.org/10.1172/JCI144781),
[MVA functional study](https://doi.org/10.1158/0008-5472.CAN-09-4319)

The broader MVA search also surfaced reports in other causal genes and symptom-management
contexts. Therefore our negative statement is narrowly: **no controlled efficacy study
for the selected BUB1B pair or a drug restoring its chromosome-segregation function was
identified in the reviewed evidence**. It is not “MVA has no treatment literature.”

### 2. Rapalog target engagement is not sufficient

| Evidence | Finding retained | Limitation / consequence |
|---|---|---|
| [Fouladi 2007](https://doi.org/10.1200/JCO.2007.11.4017) | Pediatric everolimus phase I: PBMC pathway inhibition, no objective responses | Mixed tumours; abstract-level PK extraction. Directly defeats “target suppressed, therefore tumour responds.” |
| [Santana 2020](https://doi.org/10.1002/cncr.32722) | Everolimus/bevacizumab: PK and biological effects; stable disease but no objective responses | Small combination study, not an allele-specific trial. Whole-blood peak and AUC are distinct quantities. |
| [Lenvatinib/everolimus 2025](https://doi.org/10.1002/pbc.31692) | Two of twenty RMS participants had partial responses by week 16; efficacy goals unmet | Preserve these exceptions. No control isolates either drug; responses were short. |
| [Everolimus/secukinumab 2024](https://doi.org/10.1158/1535-7163.MCT-23-0342) | IL17A-associated adaptation; combination improved preclinical inhibition | Abstract-only here. RMS PDX is distinct from the paper's A-204 rhabdoid and A-673 Ewing cultures. Not a clinically validated combination. |

The existing report retains the relapse ARST0921 comparison and negative ARST1431 addition
trial, plus the late response in temsirolimus monotherapy and negative cixutumumab
combination trial. Do not pool different backbones/settings or claim all RMS rapalog
trials had no responses. [ARST0921](https://doi.org/10.1200/JCO.19.00576),
[ARST1431](https://doi.org/10.1016/S1470-2045(24)00255-9),
[monotherapy](https://doi.org/10.1016/j.ejca.2011.09.021),
[cixutumumab combination](https://doi.org/10.1002/pbc.25334)

### 3. Autophagy evidence has compound, tissue and endpoint gaps

RMS culture studies support context-dependent lysosomal/proteostasis dependence, but the
interventions are not interchangeable: BEZ235/chloroquine, bortezomib/17-DMAG/chloroquine,
and temozolomide/bafilomycin are not everolimus/HCQ. Rapamycin sometimes protected stressed
RMS cells. Autophagy blockade increased chemotherapy-associated death in both RH30 and
non-transformed C2C12 cells. STAU1 perturbation also differed by cell context. These
observations strengthen the normal-cell and combination-antagonism gates, not a blanket
“block autophagy” recommendation. [BEZ235/CQ](https://doi.org/10.1016/j.canlet.2014.12.016),
[proteotoxic combinations](https://doi.org/10.1186/1471-2407-12-233),
[TMZ and non-transformed cells](https://doi.org/10.1038/s41420-018-0115-9),
[STAU1](https://doi.org/10.1007/s13402-021-00607-y)

Newer RMS work tested p97 inhibitors and **Lys05**, not HCQ. It contrasted inadequate mouse
MAL3-101 exposure with better CB-5083 exposure, and found heterogeneous resistance. That
is valuable translational counterevidence: attractive pathway biology does not ensure
deliverable exposure or a uniform response. No experimental compound in that paper is
silently substituted for an approved HCQ formulation.
[Kwong 2025](https://doi.org/10.18632/oncotarget.28764)

| HCQ clinical evidence | Positive finding | Counterweight |
|---|---|---|
| [Everolimus/HCQ phase I/II](https://doi.org/10.1158/1078-0432.CCR-18-2204) | Actual drug combination: two PRs in 33 evaluable adults; six-month PFS threshold met | Uncontrolled RCC, not RMS; variable HCQ PK and no significant AV rise in the small serial PBMC subset |
| [Temsirolimus phase I](https://doi.org/10.4161/auto.29119) | Vesicle changes and stable disease | No RECIST partial responses; tiny serial-tumour subset, no randomized attribution; proposed blood threshold was nonsignificant |
| [Glioblastoma phase I/II](https://doi.org/10.4161/auto.28984) | Exploratory blood/PBMC association at week 3 | Not significant at week 9; marrow toxicity constrained exposure; surrogate is not tumour efficacy |
| [Metastatic pancreatic randomized trial](https://doi.org/10.1001/jamaoncol.2019.0684) | Response rate 38.2% versus 21.1% | Primary one-year survival not improved; additional toxicity. Do not erase the response finding |
| [Preoperative pancreatic randomized trial](https://doi.org/10.1158/1078-0432.CCR-19-4042) | Better blinded histopathologic response | 98 randomized, 64 pathology-evaluable; substantial attrition. Not powered for survival, no OS/RFS difference demonstrated |
| [REVOLUTION 2026](https://doi.org/10.1136/jitc-2025-012864) | Responses and PD effects in an HCQ-containing cohort | Nonrandomized multi-drug study; tolerability reduced exposure; cannot isolate HCQ benefit |

These adult studies neither establish pediatric RMS benefit nor prove HCQ can never work.
They justify reserve status pending a direct, exposure-supported, normal-sparing result.

Independent review identified the omitted Haas trial in the retrieved PK set. It is
closer **drug-combination** evidence than the temsirolimus trial and is now included in
both candidate support and counterevidence. Its positive prespecified single-arm outcome
does not isolate HCQ's contribution, prove pharmacologic synergy or establish pediatric
RMS benefit. Reserve status therefore remains, for those limitations—not on a claim
that this combination has never reached clinical study.

### 4. Metformin and other alternatives deserve fair counter-review

The previous metformin rationale omitted a pediatric metformin/VIT phase I trial that
included an RMS partial response. It lacked a VIT-only comparator and closed before MTD
determination. Its small PK cohort and internally unclear matrix description are retained
as limitations, not silently harmonized. Metformin remains deprioritized, but not on the
false premise that no pediatric combination experience exists.
[Metts 2023, online 2022](https://doi.org/10.1002/cam4.5297)

The negative metformin xenograft experiment in the added sarcoma paper used **Ewing
sarcoma**, not RMS. Hypoxia and millimolar culture effects caution against extrapolation;
they are not proof of routine-dose clinical genotoxicity or failure in every tumour.
[Scotlandi 2013](https://doi.org/10.1371/journal.pone.0083832)

An exposure-aware RMS combination study is a useful design precedent, but compared
72-hour nominal-culture effects with published serum peaks. It is not a completed unbound
exposure bridge. High cell killing can coexist with antagonism by a combination index.
[Combination screen](https://doi.org/10.1007/s00280-016-3077-8)

Horizon findings were considered without inflating the twelve-drug shortlist:

| Finding | Why not promoted in this review |
|---|---|
| Everolimus plus secukinumab | Preclinical adaptation signal; no reviewed genotype-specific margin or pediatric combination efficacy |
| Auranofin with GSH-depleting partners | RMS culture mechanism, but no deficient-normal selectivity or reviewed approved-partner exposure bridge. [Primary paper](https://doi.org/10.1038/cddis.2017.412) |
| Posaconazole/Hedgehog | RMS preclinical abstract, unknown relevant tumour pathway and no reviewed free-exposure window. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8493378/) |
| MYOD1/IGF2–PI3K targeting | Molecular-subtype study; the relevant tumour subtype is unknown here. [Primary study](https://doi.org/10.1126/sciadv.aea6453) |
| HSP70/p97/Lys05 tools | Experimental intervention identity and exposure; not an approved-drug repurposing result |

These are coverage/eligibility decisions, not completed comparative drug development.
The existing exclusion reasons for gentamicin, ataluren, NMN, nicotinamide, senolytics and
checkpoint inhibition remain. No supplement, antibiotic or constitutional checkpoint
inhibitor is recommended.

## Exposure audit: what the numbers actually mean

The machine-readable [exposure ledger](track2-exposure.json) has eight public-study/label
records. Reproduction uses `uv run python scripts/track2_exposure.py`. For a mass
concentration, `nM = ng/mL × 1000 / molecular_weight(g/mol)`. This equation preserves
matrix and analyte; it does not estimate drug available inside a cell.

| Public observation | Correct unit conversion | What must not be inferred |
|---|---|---|
| Everolimus TSC whole-blood trough 5–15 ng/mL | 5.2–15.7 nM **total whole blood** | Not free plasma, RMS target or genotype rescue concentration |
| Pediatric combination whole-blood peak 52.1 nM; AUC0–24 307 nM·h | Already molar, but different dimensions | Peak is not sustained culture exposure; AUC is not trough |
| HCQ single-dose label peaks: blood 129.6, plasma 50.3 ng/mL | About 0.386 and 0.150 µM, respectively | Not a fixed partition ratio or chronic oncology target; maxima occur at different times |
| HCQ estimated blood splits 1,348 and 1,785 ng/mL in different trials | About 4.01 and 5.31 µM | Not two replications of a tumour threshold: the former was nonsignificant; the latter was exploratory PBMC PD |
| Metformin reported average steady-state 404 ng/mL | About 3.13 µM parent analyte | Matrix ambiguity remains; not a matched unbound culture comparison |

Sources: [everolimus label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[HCQ label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=34496b43-05a2-45fb-a769-52b12e099341),
the PK publications above, and PubChem parent molecular weights
[HCQ](https://pubchem.ncbi.nlm.nih.gov/compound/Plaquenil),
[metformin](https://pubchem.ncbi.nlm.nih.gov/compound/Metformin).

The HCQ sulfate mass in the tablet is not the parent analyte mass in a bioanalytical
concentration. Everolimus plasma binding cannot simply be applied to whole blood; a plasma
mass fraction is not a concentration ratio. PBPK lysosomal accumulation predictions are
not measured exposure in a pediatric RMS tumour. Tumour pH, binding, active metabolites,
co-medications and duration matter. [HCQ PBPK study](https://doi.org/10.1124/jpet.117.245639)

**No numerical clinical exposure margin is defensible from these data.** Missing quantities
include a genotype-relevant functional concentration-response, free medium concentration
over time, a justified human tissue exposure model and the injury threshold in matched
deficient non-cancer cells. All margin fields remain `null`; the checker refuses to turn
incompatible quantities into a favourable ratio. The table is not a dosing guide.

## Revised experimental and delivery gates

- First measure the genotype's pathway state, RNA/protein and chromosome-segregation
  phenotype. Stop the everolimus arm if the proposed pathway abnormality is absent.
- Measure actual assay exposure, free fraction, depletion and carryover; do not match a
  single human peak with continuous multi-day nominal dosing.
- Record serum conditions, cell density, pH, nutrient/oxygen state and assay duration.
  Reproduce a response across independent clones/days and orthogonal functional assays.
- Distinguish autophagosome accumulation from dynamic flux; a lysosomal pH-changing drug
  can alter fluorescent-reporter behaviour. Include assay controls and independent protein
  turnover/death measurements. Interpret PBMC target engagement separately from tumour PD.
- Require matched deficient-normal viability, differentiation, division accuracy and
  recovery alongside tumour effect. Assess antagonism as well as synergy before any
  combination, including whether cytostasis protects cells from a chemotherapy partner.
- A clinically relevant RMS comparator must be chosen for a documented tumour setting.
  VIT-0910 provides a randomized relapse benchmark, not a regimen to administer here.
  Its primary response comparison was not conventionally significant (p=.09), whereas
  secondary OS favoured VIT with more toxicity. [Trial](https://doi.org/10.1200/JCO.21.00124)
- If a window cannot be shown, retain the negative result and stop advancement. Clinical
  history, phase, function and present treatment remain unresolved; literature cannot
  replace those measurements or authorize sampling/treatment.

The scientific desk review can be completed with these uncertainties explicit. Laboratory
results are future research, not a prerequisite to honestly submitting a proposal. The
recorded three-minute pitch, hosted URL, final owner review, live rules/quota check and
portal receipt remain separate delivery gates. This review does not upload an entry.

## Independent re-review completed

Separate standards and specification reviewers checked the expanded draft against the
session baseline, then rechecked the fixes. Standards found three validation defects:
unbound parent/salt molecular-weight metadata, an accepted invented per-record margin,
and an accepted empty article body. These now fail validation, including package creation
for invalid exposure inputs. Specification review found the omitted Haas everolimus/HCQ
trial; its favourable result and applicability limits are now retained. Both reviewers
report no unresolved material finding in their bounded rechecks. All 107 tests pass;
this is not clinical/pharmacology sign-off or proof of exhaustive literature coverage.
The detailed initial findings and resolutions are in `track2-devils-advocate.md`.
