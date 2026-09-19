# Track 2 falsification cycle 1: Firecrawl discovery and primary adjudication

2026-09-19, session 47, baseline `c97bfb1`; feat-009. The owner authorized execution
of the standing falsification objective using Firecrawl. This is a bounded,
source-based author review, not a systematic review, independent panel, clinical
assessment or experiment. Scientific decisions are recorded in the v10 report,
validation plan and ledger; v9 and earlier packages remain preserved.

## Decision

**Revise experimental qualification and safety; do not promote a drug.** Everolimus
remains an optional mechanistic probe, HCQ reserve, and no candidate earns a rescue
priority. The search challenges both an optimistic mTOR-inhibition story and an
overly broad rejection of it. Findings support three concrete changes:

1. Keep the original excess-mTOR hypothesis as branch A, but do not treat absence
   of elevated measured mTOR readouts as a universal exclusion of every possible
   benefit. A separate, prospectively defined branch B would require a demonstrated
   autophagic-flux and regenerative-function deficit, relevant mechanism controls
   and its own confirmation. No such deficit is established in the selected pair.
2. Test concentration, timing, recovery and regeneration separately. Partial
   inhibition, continuous suppression, precursor activation and mature-tissue
   function need not share an outcome. Muscle mass, markers and short-term viability
   do not establish force, durable useful output or safety during repair.
3. Strengthen compound-specific normal-tissue, delayed-injury and exposure checks.
   Human CQ/HCQ myopathy, whole-blood partitioning, failed autophagy trials and
   allele-dependent treatment resistance make generic class arguments inadequate.

## Search execution and provenance

Used the existing `scripts/track2_firecrawl.py` STDIO MCP bridge and installed
Firecrawl MCP entry against `http://127.0.0.1:3002`. Discovery confirmed 26 advertised
tools. The new runner uses only search, paper search, metadata inspection, related
papers, passage reading and public-page scraping. Each worker has a separate MCP
process and archive; no agent, monitor, feedback, browser interaction or new paid
synthesis job was deliberately invoked. Search/retrieval paths can still involve
external services or provider processing; this is not an LLM-free or zero-retention
attestation. Existing Fireworks/provider-disclosure gaps remain.

Four fixed, archived plans cover 87 tool calls: discovery 41, adaptive follow-up 33,
primary clarification 8, and closure 5. They include neutral and contrary queries,
forward/backward citation retrieval from Goutas, Sieben and North, trial registries,
the current official label, and alternatives. The exact queries, result limits and
claim bindings are in `track2-falsification-{discovery,followup,primary,closure}-20260919.json`.
There is no lower date filter. Only the returned bounded result sets were considered;
ranking, indexing, language, access and passage selection limit coverage. Web snippets
and titles were screened for relevance; selected primary sections/abstracts were
adjudicated below. Returned records are not all fully read studies or independent evidence.

Actual transport outcomes: **68 non-error responses, 14 tool errors, two timeouts and
three empty passage responses**. The web results contain 180 rows/173 distinct exact
URLs; paper/citation tools returned 161 rows/145 distinct identifier strings. These
are discovery units, not independent studies. Structured primary retrieval made 27
requests: 25 returned records and two XML requests failed with HTTP 500. One of the
25 returned records was unrelated and explicitly rejected below. Six new full-text
XML articles were retrieved; review depth remains selected sections, not six entire
papers plus supplements. The complete status/hash accounting is in
`track2-falsification-retrieval-summary.json`.

Complementary Europe PMC structured searches/XML and ClinicalTrials.gov API records
are specified in `track2-falsification-records-20260919.json` and its supplement.
Two additional discovery queries cover HCQ/RMS and BUBR1/rapalog/rescue. General web
search helped resolve primary identifiers; it did not replace the Firecrawl work.
Original responses, request arguments, times, status and SHA-256 values are retained
in the ignored run directories. Scripts never read the project `.env`, raw subject
files or phenotype narrative, and no such data were sent to any service.

Reproduction (use new output-directory names):

```bash
uv run python scripts/track2_falsification_search.py discovery results/feat009/NEW-discovery
uv run python scripts/track2_falsification_search.py followup results/feat009/NEW-followup
uv run python scripts/track2_falsification_search.py primary results/feat009/NEW-primary
uv run python scripts/track2_falsification_search.py closure results/feat009/NEW-closure
uv run python scripts/track2_falsification_sources.py results/feat009/NEW-records
uv run python scripts/track2_falsification_sources.py results/feat009/NEW-records-supplement --supplement
```

Actual archives use `results/feat009/falsification-firecrawl-{discovery,followup,primary,closure}-v1/`
and `falsification-primary-records{-supplement}-v1/`. Each records the executed script
and plan bytes. These scripts return exit 2 for partial retrieval failure; the result
must be adjudicated, not relabeled a successful full search. No automatic retries.

## Findings that changed or constrained the design

| Source and reading depth | Finding and strongest objection | Consequence |
|---|---|---|
| [Balnis 2025](https://doi.org/10.1172/jci.insight.182842), retrieved XML; selected Results/Figs 7–10, main Methods/Discussion | Rapamycin improved satellite-cell proliferation, flux and transplantation-related myogenesis under hypercapnia while measured total/phosphorylated mTOR was not increased beforehand. Key experiments have n=3–4; some control data are reused across figures. The detailed dose/schedule supplement was not reviewed. These are adult mouse/C2C12 conditions, not MVA or an everolimus experiment. | A counterexample to the universal measured-excess requirement. Add a separate prospective flux/function hypothesis; do not infer a defect, benefit, dose or clinical margin for the selected pair. |
| [Joseph 2019](https://doi.org/10.1128/MCB.00141-19), XML; selected Results/Figs 2–8 and Methods | RAD001 at nominal administered doses 0.15 or 0.5 mg/kg daily for six weeks in aged male rats had muscle- and dose-dependent effects. Lower-dose tibialis-anterior mass improved; plantaris mass trended, gastrocnemius did not share the benefit. Muscle-weight groups have n=6–13; morphology groups n=4–5. Force improvement was not established by those outcomes, and static LC3 measures are not a full flux assay. | Preserve positive compound-proximal evidence, require graded rather than maximal inhibition, and separate size from function. The authors' cross-species dose-equivalence assertion supplies no child-specific free-exposure bridge. |
| [Ge 2009](https://doi.org/10.1152/ajpcell.00248.2009), verified primary abstract via Firecrawl; full-text retrieval failed | Rapamycin impaired injury-induced muscle regeneration; rapamycin-resistant mTOR restored it, and kinase-inactive/resistant constructs separated new-fiber formation from growth. Dose and full design were not freshly extracted. | Add stage-specific regeneration and recovery endpoints; favorable aged-muscle results cannot erase repair-context risk. |
| [Zhang 2015](https://doi.org/10.1016/j.bbrc.2015.05.032), indexed primary abstract; XML failed | Satellite-cell Mtor deletion impaired regeneration, proliferation and differentiation. Complete genetic deletion is not equivalent to a titrated rapalog. | Treat genetic perturbation as a mechanism control with its own dose/timing limits, not a quantitative toxicity surrogate. |
| [Naddaf 2021](https://doi.org/10.3389/fneur.2020.616075), XML; selected Methods/Results/Tables | Selected retrospective series of 13 adults: 10 HCQ, 2 CQ, 1 both; long exposure and vacuolar myopathy, sometimes swallowing/respiratory involvement. Many improved after withdrawal with residual weakness. Mixed compounds, referral selection, comorbidity and no exposed-population denominator prevent an incidence estimate or pediatric risk prediction. | HCQ protein accumulation cannot count as healthy muscle function. Require delayed muscle/lysosomal injury and recovery assessment before reopening the reserve. |
| [van Erp 2016](https://doi.org/10.1007/s40262-016-0414-3), XML; selected Methods/Results/limitations | Population model used data from 73 cancer patients. A hematocrit change from 45% to 20% predicted about half the whole-blood exposure without changing modeled plasma exposure or pharmacodynamics. This is a model with binding assumptions, not measured free exposure in this child. | Record hematocrit and matrix alongside blood PK; prohibit a blood-to-medium or blood-to-tissue shortcut. Clinical margins remain null. |
| [Goenka 2025](https://doi.org/10.1007/s12672-025-01904-w), XML; Methods, efficacy and biomarker Results/Discussion | Randomized ovarian-cancer trial: 59 enrolled, 56 response-evaluable; ORR 22/26 versus 24/30, p=0.65, without demonstrated survival or biomarker benefit. Limited sample, post-randomization response evaluability and blood rather than paired-tumour biomarkers constrain interpretation. No excess adverse events was reported in this regimen. | Retain a negative clinical autophagy-combination result without claiming zero HCQ effect in RMS or universal toxicity. Biomarker and exposure qualification remain essential. |
| [Bonatti 1998](https://doi.org/10.1007/s004120050335), indexed primary abstract only | Rapamycin-associated malsegregation in mammalian/yeast assays depended on cell-cycle context; an A-T line responded differently. No full-text dose or effect-size verification. | Record faithful ordinary division and entry state; do not extrapolate a class-wide clinical chromosome-harm rate. |
| [Yamada 2026](https://doi.org/10.1093/bbb/zbag087), indexed primary abstract only | Budding-yeast TORC1 inactivation produced a separase-independent route to cohesin degradation. Full text unavailable. | A mechanistic lead, not proof of mammalian/everolimus harm; retained as a transfer gap rather than an extra clinical risk estimate. |
| [Silva 2024](https://doi.org/10.1186/s12929-024-01056-z), XML; model generation, Fig 4 and Discussion | The title concerns monoallelic germline variants, but the functional RWPE-1 clones carry two different edited in-frame deletions. They showed reduced Taxol-induced growth inhibition/apoptosis at 10 nM for 96 h; four independent response experiments. Neither allele is the selected pair. | Do not infer a monoallelic drug response from the title or assume BUB1B deficiency sensitizes to all antimitotics. Match endogenous genotype, record growth-corrected response and ordinary-cell fate. |
| [Pun 2025](https://doi.org/10.1161/JAHA.124.038286), Firecrawl primary abstract and selected Results/Discussion passages | Heart-specific Bub1b knockout disrupted embryonic differentiation and morphogenesis. Early transcriptomic changes preceded detected proliferation/apoptosis changes. This does not prove complete independence from mitosis or drug rescue. | A muscle/division result cannot establish whole-development rescue. Add cardiac/developmental scope review before extending constitutional claims; no cardiac abnormality is inferred in the child. |

The [RMS/TMZ primary study](https://doi.org/10.1038/s41420-018-0115-9) was rechecked
through metadata and selected Methods/Results passages. Its inhibitor was bafilomycin
A1, not HCQ. Both RH30 and C2C12 cells showed enhanced death with autophagy blockade;
the mouse myoblast comparator is not BUB1B-deficient human normal tissue. The linked
publisher correction concerns volume assignment, not a demonstrated experimental
retraction. This preserves the historical distinction rather than adding independent
HCQ efficacy evidence. PP2A discovery again returned the already-reviewed off-target
critique; gene overexpression/NAD, senolysis and readthrough searches did not supply
a verified new approved-drug rescue candidate within the inspected result sets.

## Registries, labels and source integrity

- [NCT02338609](https://clinicaltrials.gov/study/NCT02338609): completed, results
  posted; 15 participants in a single-group long-term everolimus follow-up, 13
  completed. Small selected follow-up without a concurrent untreated comparator
  cannot prove general developmental safety. It is separate from the label's
  115-patient pooled pediatric follow-up and must not be counted as 15 new
  independent reassuring outcomes without checking overlap.
- [NCT01216839](https://clinicaltrials.gov/study/NCT01216839): the retrieved record
  is UNKNOWN with an estimated enrollment of 20, a 2013 last posted update and no
  posted results. It is not a demonstrated negative trial or actual enrollment.
- [NCT00786682](https://clinicaltrials.gov/study/NCT00786682): terminated; the stated
  reasons include lack of improvement versus historical controls and competing
  studies. Narrative and structured outcome denominators are not fully consistent.
  Retain the stopping rationale; do not manufacture a randomized effect estimate
  or treat posted zero denominators as zero responders in a known sample.
- [NCT02567435](https://clinicaltrials.gov/study/NCT02567435): posted EFS analysis
  uses 148+149 participants and p=0.44, consistent with the 297-person published
  analysis. Enrollment 325 includes other/excluded groups; it does not replace
  the analysis denominator or the published HR. The exact v9 plot is preserved.
- The [June 2026 everolimus label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)
  was retrieved through Firecrawl. Infection, pneumonitis, renal, wound-healing and
  interaction warnings remain relevant; pediatric experience is retained without
  inferring the child's regimen, organ function, risk or dose.
- Europe PMC correction metadata and the actual JCI correction were checked.
  The Sieben correction remains Figure 2E/lymphatic-tumour provenance, not the
  muscle phosphoprotein result. No correction link in a metadata record is not
  proof that no correction exists anywhere. The broad Goutas correction query
  returned an unrelated record, so it supplies no correction evidence.

**An error in this review was caught and excluded:** the supplemental structured
request labeled `regeneration_metadata` used PMID 19828831, which resolves to an
unrelated GPCR/analgesia article. That record was rejected by title/PMCID/DOI
comparison. Firecrawl independently resolves the intended PMC2793064 to PMID
19794149 and DOI 10.1152/ajpcell.00248.2009, then the closure metadata call verifies
that identity. The erroneous request remains in the provenance archive; it never
supports a scientific claim. Future reuse must use the corrected identifier.
The active supplemental plan now uses PMID 19794149 with a PMCID identity guard;
the archived first-run plan preserves the erroneous request for audit. A synthetic
test verifies that a wrong primary identity cannot pass that guard.

## Claim-by-claim disposition and remaining work

| Claim | Outcome of this cycle | What would change it next |
|---|---|---|
| F1: model/genotype transfer | Still unresolved; mutation, tissue and developmental context matter. No new phase inference. | Qualified endogenous allele-specific models and functional observations. |
| F2: intervention direction | Revise universal entry language; keep independent excess-pathway and flux/function hypotheses. | Replicated benefit or injury under prespecified branch-specific conditions and mechanism controls. |
| F3: abundance/flux as rescue | Reject abundance-only inference; both accumulation and depletion can mislead. | Localization, dynamic flux, checkpoint and useful tissue output with matched cell state. |
| F4: response versus selection | Retain all-cell fate accounting and add activation/regeneration/recovery stages. | Demonstrate benefit per original culture without sacrificing useful cells or later function. |
| F5: clinical exposure | Unresolved; blood partitioning strengthens the existing matrix limitation. | Justified free assay/tissue exposure-time measurements or defensible bounds; no assumed dose conversion. |
| F6: normal-tissue safety | Add delayed myopathy/repair endpoints and developmental-scope review. | Reproducible deficient-normal safety at the same exposure that benefits the target endpoint. |
| F7: tumour inference | HCQ stays reserve; trial and model signals cannot be combined into a patient-specific regimen. | Actual compound/subtype controls, growth-corrected response, matched normal safety and exposure. |
| F8: alternatives | No new rescue priority; positive rapalog results survive the challenge but remain indirect. | A stronger endogenous-function and exposure chain, including contrary results. |

Next high-impact gaps: selected-pair biology; full dose/schedule and independent
replication of the hypercapnia finding; an assay-qualified range for useful partial
inhibition versus repair impairment; chronic deficient-normal effects; and an actual
exposure bridge. Complete the supplement/methods audit before using that study to
choose an experimental dose. Do not induce hypercapnia or senescence merely to make
a model match the positive literature. Model/laboratory access, phase and clinical
context remain missing; literature cannot supply them.

This cycle stops after all eight declared dimensions receive discovery and an explicit
disposition, with the most consequential new leads checked at the recorded depth.
It does not establish saturation of all literature. Inaccessible full text, small
models, bibliographic noise, restricted result depth and unreviewed supplements
remain limitations. The standing falsification objective continues after this cycle.
