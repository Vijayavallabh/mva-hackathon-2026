# Track 2 v15: falsification across the full evidence chain

2026-09-24 · Session 55 · Feat-009 · Author audit of v14 and drug-science v10.
This is a bounded research revision, not independent peer review, a systematic review,
an experiment or a treatment recommendation. All older releases remain immutable.

The strongest improvement is to make every consequential inference defeasible.
The [19-claim register](track2-falsification-register-v15.json) records the claim,
support, challenge, observable falsifier, stop/reopening criteria and next action.
The [reanalysis](track2-falsification-analysis-v15.json) checks actual retained scores
and demonstrates endpoint failure modes using explicitly synthetic examples.
The current disposition remains **no rescue-priority drug**. Everolimus is an optional
qualified mechanistic probe; HCQ stays reserve. Every biological advancement gate is
unresolved. That means hold the inference, not that every intervention is disproven.

## Findings that change the proposal

### 1. The newer model pass is narrower than the presentation suggested

Reanalysis of all 84 archived newer protein scores reproduces the original primary
control ordering in 12/12 model/window comparisons. Including the already-retained
secondary controls leaves complete impaired/retained separation in only 4/12:

| Model | Primary ordering, 3 windows | Separation with all six controls |
|---|---:|---:|
| ESMC 300M | 3/3 | 3/3 |
| ESMC 600M | 3/3 | 1/3 |
| ESMC 6B | 3/3 | 0/3 |
| ESM3-open 1.4B | 3/3 | 0/3 |

Retained-function controls receive negative scores in **11/24** comparisons; impaired
controls receive positive scores in **2/48**. Thus score sign cannot be a universal
functional threshold. The original primary test remains a success. The expanded
comparison is **post-hoc sensitivity analysis**, not a replacement preregistered gate
or a new accuracy benchmark. D882A's secondary label is stated in the previously
retrieved main paper; its supplementary experiment was not independently reviewed.
Two substitutions at residue 882, related models and repeated windows do not provide
independent clinical calibration. No pooled significance or pathogenicity probability
is calculated. [Control study](https://doi.org/10.1016/j.devcel.2012.03.009).

**Revision:** replace the unbalanced “strengthens computational motivation” headline
with the narrower observation plus its control-set sensitivity. Preserve candidate
negativity, older failed controls and all structural/DNA limitations. Do not run more
similar models to obtain agreement. A new run must first specify a discriminating
question, independent controls and a decision it could change.

### 2. A consequential supplement has a real unresolved unit discrepancy

The Balnis supplement was previously a reading gap. Its PDF now has a verified local
copy, SHA-256 `5cbc048a9b2200c33e3794e9b932a96809c8785e96f7ee61b1d698b2c6b15a43`.
PDF page 12 (printed Methods page 6) specifies **10 mM** for ex vivo rapamycin;
PDF page 15 (printed page 9) specifies **10 μM** in the primary-cell section.
Both pages were visually inspected, so this is not inferred from PDF extraction alone.
They differ by a factor of 1,000. They describe related ex vivo experiments; we cannot
determine whether the discrepancy reflects an error or different actual conditions.
Do not silently correct the source or assign either concentration to the disputed assay.
[Supplement](https://insight.jci.org/articles/view/182842/sd/pdf/render/1).

The reported in vivo schedule and different disease model supply no human free-tissue
exposure bridge. The positive qualitative result is retained, but branch B remains a
separately qualified mechanistic hypothesis. **Revision:** quarantine the disputed
concentration; resolve it through a corrected primary record or authorized clarification
before using it to design an exposure-linked experiment. No author or family contact
was made. This ambiguity does not prove that the biological result is false.

### 3. A stop codon or a stable domain does not specify the whole cellular mechanism

The 2012 complementation study reports retained function for its 731X truncation in
the assays used. A later study reports defects in PP2A-B56 recruitment, checkpoint
silencing and alignment when that domain is removed. The constructs, expression and
endpoints matter; 731X is not the selected L737Ter allele, and ectopic cDNA does not
measure endogenous transcript decay. **Revision:** retain a loss-of-function hypothesis
without treating a C-terminal truncation as a measured null; separate checkpoint
activation/maintenance from silencing, attachment and accurate daughter production.
[2012](https://doi.org/10.1016/j.devcel.2012.03.009),
[2020](https://doi.org/10.1016/j.celrep.2020.108397).

A 2026 TPR-domain study reinforces that N-terminal MCC/APC/C interactions lie outside
the modeled C-terminal fragment. A separate two-family study concerns different
heterozygous variants, which remain VUS; expression trends and chromosome separation
findings do not establish the selected pair or the family's genotype. These are scope
checks, not new subject findings. **Revision:** keep single-allele and cis alternatives;
do not infer benignity of a single allele or import a family-history mechanism.
[TPR study](https://doi.org/10.1038/s42003-026-10384-9),
[heterozygous study](https://doi.org/10.3389/fendo.2026.1838559).

### 4. Apparent functional rescue needs stronger measurement controls

The pre-existing all-cell requirement is now backed by an executable counterexample.
In a **synthetic** population of 100 cells per arm, the error fraction among completed
divisions falls from 25% to 11.1%, while accurately divided viable output falls from
60% to 40%. Even favorable missing-outcome assignments cannot turn that example into
improvement. Another synthetic example has a positive observed change whose worst-case
missingness bounds include zero. These are identification bounds, not confidence
intervals, power estimates or biological measurements.

Tumour-versus-normal endpoint IC50 comparisons can be distorted by different baseline
growth rates. **Revision:** retain direct baseline/time-course viable counts and deaths;
use growth-rate-aware analysis as a sensitivity check where its assumptions hold.
It is undefined or unstable when controls do not meaningfully grow. Do not “correct”
postmitotic muscle into a proliferation endpoint or make ATP/metabolic signal the
sole viability measure. [Hafner](https://doi.org/10.1038/nmeth.3853).

Fluorescent flux reporters depend on acidity, expression and optical behavior as well
as turnover. **Revision:** pair dynamic flux readouts with pH, expression/interference
and viability controls plus orthogonal cargo degradation. Protein accumulation after
lysosomal inhibition remains insufficient for rescue.
[Primary reporter study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3121655/).

### 5. Engagement, safety and benefit need separate tests

Published mTOR inhibition can induce upstream/Akt feedback in tumour contexts.
The compound-specific stromal-cell BUBR1 decrease remains a relevant concern, with
early/late passage and distinct exposure schedules preserved. **Revision:** graded,
time-matched total/activated pathway measurements and interpretable orthogonal
perturbations; no biomarker-only success and no automatic combination to suppress
feedback. Discordance restricts mechanism attribution, not every measured drug effect.
[O'Reilly](https://doi.org/10.1158/0008-5472.CAN-05-2925),
[Goutas](https://doi.org/10.1016/j.redox.2023.102701).

Contrary evidence must also challenge rejection. The June 2026 official label retains
favorable but uncontrolled pediatric TSC growth follow-up alongside renal, infection,
wound-healing, marrow/metabolic and interaction warnings. A 211-participant pediatric
heart-transplant randomized trial reports a safety noninferiority result for a specific
everolimus/low-dose-tacrolimus regimen begun in six-month survivors, while its primary
efficacy comparison was not significant. That design cannot isolate everolimus or
establish MVA safety. **Revision:** do not describe developmental harm as inevitable;
require context-specific, sufficiently precise safety bounds.
[Label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2),
[Trial](https://doi.org/10.1001/jama.2025.14338).

The 2026 BIOMEDE abstract reports futility versus a historical DIPG cohort, better
tolerability on some outcomes and exploratory mTOR-response associations. Treatment
allocation among drugs was randomized; the historical efficacy comparator was not.
Those observations do not establish a general mTOR biomarker rule or RMS/constitutional
efficacy. ARST1431 remains the relevant randomized RMS boundary; retain its confidence
interval and comparator. Neither null trial proves exactly zero effect everywhere.
[BIOMEDE](https://doi.org/10.1038/s41591-026-04354-1),
[ARST1431](https://doi.org/10.1016/S1470-2045(24)00255-9).

## Coverage and decisions across the solution

| Layer / claim IDs | What can break the inference | Required improvement |
|---|---|---|
| Attribution and alleles / G01–G02 | Unresolved phase, residual function, construct/context mismatch | Endogenous assays and single/cis/trans/corrected comparisons; no subject-phase inference from engineered cells |
| Models / M01–M04 | Wrong control sign/order, correlated evidence, cross-gene transfer, confident impaired folds | Full matrices, control sensitivity, evidence-dependence map; no clinical calibration claim |
| Mechanism / H01–H03 | Adaptive excess, absent eligibility, feedback or non-mediated effects | Separate locked branches, graded perturbation and functional outcomes |
| Measurement / E01–E03 | Survivor selection, growth-rate/ATP/pH artifacts, missing tracks | All-enrolled output, orthogonal readouts, missingness bounds and valid denominators |
| Exposure / X01 | Unmatched matrix, analyte, free fraction or schedule | Measured/defensibly bounded exposure; all clinical margins remain null |
| Safety and timing / S01–S02 | Delayed injury, lost regeneration, unstable clone expansion, irrelevant tissue/time | Prespecified injury bounds, later fates and recovery; no whole-development inference |
| Statistics and sources / T01, R01 | Pseudoreplication, imprecision, outcome switching, wrong identity/units | Pilot-qualified margins; separate confirmation; explicit source quarantine |
| Alternatives / A01 | Different drug/model/indication and missing normal-tissue window | Same criteria for every candidate; no promotion by elimination; BindCraft2 remains deferred |
| Delivery / D01 | Polished slides or software checks mistaken for validated biology | Aligned claims and uncertainty; no upload/readiness promotion |

The [v15 protocol](track2-validation-v15.md) states operational changes. No numerical
benefit, injury or power threshold can honestly be specified before assay qualification.
A statistically inconclusive result is held unresolved. An adequately precise failure
can reject the meaningful-effect claim in the tested context. A safety signal can stop
advancement even before definitive mechanism attribution. All-pass software output
permits, at most, **preclinical review**, never patient treatment.

## Search record, reading depth and remaining gaps

The [initial plan](track2-falsification-search-v15.json),
[adaptive follow-up](track2-falsification-followup-v15.json) and
[source audit](track2-falsification-source-audit-v15.json) retain exact queries,
returned identifiers, result order/limits, timestamps, hashes and failures. Searches
used no lower date/language cutoff and a publication upper bound of September 24.
Only the first six API records per query were considered. The initial plan called the
order “relevance”; no explicit sort was set, so it is recorded as API-default instead.
Noisy full-text matches prompted targeted title/abstract queries. Returned titles were
screened; retrieval is not full-paper reading or a count of independent experiments.

Firecrawl MCP discovery succeeded, but all four search calls returned tool errors with
no usable result. The 30 initial structured retrievals had 22 HTTP successes and eight
HTTP failures (seven 503, one 500); two separate public downloads succeeded. The 11
adaptive retrievals succeeded at transport level. One returned an unrelated paper:
the guessed ARST1431 identifier 38838360 was rejected. The correct 38936378 and DOI
were verified in the tumour search and PubMed. An unquoted-DOI query returned no record;
that was a query failure, not absence of the study. No failed query was retried blindly.

Reading depth: Balnis main text selected results/methods and supplemental Methods
pages 6–13 (PDF pages 12–19), with visual checks of the two disputed pages; Hafner and
the flux-reporter paper selected full-text sections; archived Goutas Methods/Figure 6
and 2012 main-text control passages; 2020 domain paper indexed primary passages;
2026 TPR/heterozygous papers selected full-text passages; new transplant/BIOMEDE trials
indexed abstracts only. New trial supplements and detailed biomarker/multiplicity
analyses were not reviewed. No new drug priority rests on those abstract-only signals.

Four registry records were read: NCT02579044 still has no posted results and was last
updated April 2, 2026; NCT01216839 is stale/unknown with no results; NCT02338609 and
NCT02567435 have posted results. Absence of results is not a negative trial. Reviewed
metadata carries the known JCI corrigendum and distinguishes commentary/preprints
from corrections. No comprehensive retraction clearance is claimed; the critical
Goutas metadata refresh failed, though the archived primary text was rechecked.
[HGPS registry](https://clinicaltrials.gov/study/NCT02579044).

Stopping point: every layer has an adjudication, concrete revisions are implemented,
and the highest-value remaining questions need primary clarification or experimental
evidence. Broader multilingual/full-text retrieval, independent control calibration,
the 2012 supplement, the disputed concentration and biological qualification remain
open. The author audit can itself be wrong; independent specialist review would add
value. No subagents, new GPU inference, laboratory orders, family contact or submission
were used. Source/code checks cannot close those scientific gaps.

## Reproduction

```bash
uv run python scripts/track2_falsification_v15.py check
uv run python scripts/test_track2_falsification_v15.py
# Only for a genuinely needed new retrieval cycle; use new output directories:
uv run python scripts/track2_falsification_retrieve_v15.py records results/feat009/new-v15-sources
uv run python scripts/track2_falsification_retrieve_v15.py followup results/feat009/new-v15-followup
uv run python scripts/track2_falsification_retrieve_v15.py firecrawl results/feat009/new-v15-firecrawl
```

Existing raw/public retrievals are under `results/feat009/v15-public-sources-20260924`,
`v15-public-followup-20260924` and `v15-firecrawl-20260924`. No protected subject file
was opened or transmitted. Future cycles must update claims and stop/reopening rules
before interpreting new results, preserve failed attempts and recheck source identity.
