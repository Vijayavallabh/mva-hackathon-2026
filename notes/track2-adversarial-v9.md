# Track 2 adversarial audit and v9 revision

2026-09-19 · feat-009 · baseline `0777a15`. Owner-authorized review of all Track 2
progress, with revisions where warranted. This is the main agent's source-based
author audit, not a newly independent reviewer, full systematic review or laboratory
sign-off. No paid/model literature reruns, subject-file analysis or upload occurred.

## Verdict

**Revision required.** The strongest defect is a missed contrary experiment with
everolimus itself: lower BUBR1 protein in late-passage human stromal cells. A second
defect is the incomplete treatment of adaptive mTORC1 activity. Neither establishes
patient harm; together they undermine a comparative rescue priority based principally
on a different-allele mouse phosphoprotein observation.

Withdraw **“sole conditional research priority”** as a comparative drug-ranking claim.
Retain everolimus as an **optional, model-qualified mechanistic probe**. No drug earns
a rescue priority from the reviewed evidence. This does not rank HCQ first, rule out
everolimus benefit, or require the downstream pathway to initiate the disease. HCQ
remains reserve, and tumour-only horizons remain separate. Phase and all clinical
exposure margins remain unresolved. The new v9 report, ledger, validation plan, pitch
and deck supersede the corresponding current-use claims; every v1-v8 artifact is
preserved as history.

## Findings, consequences and resolution

| ID / importance | Adversarial finding | Resolution in v9 |
|---|---|---|
| A1 / major | The synthesis omitted Goutas 2023, including an everolimus-associated BUBR1 decrease, despite prioritizing this drug for BUB1B-deficient cells. | Add the actual drug, cell state, exposure and endpoint; downgrade to a mechanistic probe; add BUBR1/flux/fate monitoring and an advancement pause trigger. |
| A2 / major | A high phosphoprotein readout does not identify a harmful pathway. Adaptive signaling could make suppression counterproductive. | Add contrary denervation experiments and competing harmful-driver/adaptive-response hypotheses. Require functional response, not suppression, to support advancement. |
| A3 / major design gap | Orthogonal pathway perturbation was explicit in the earliest plan but absent from the consolidated v5 plan. Correction alone cannot assign a drug's beneficial mechanism to mTORC1. | Restore titrated orthogonal perturbation and appropriate controls; separate phenotypic benefit from target-mechanism attribution. |
| A4 / moderate | The experimental plan can be misread as requiring useful division in mature muscle cells. Progenitor proliferation and postmitotic tissue function are different constructs. | Specify paired precursor fate and mature-lineage function assays; do not require myotubes to divide. |
| A5 / moderate | Protein/biomarker improvement or fewer abnormal survivors can hide cytostasis, loss of useful cells, cell-cycle redistribution or selection. Existing all-cell fate accounting is strong but does not fully protect lysate and lineage assays. | Add per-culture and per-survivor outputs, matched cell state, RNA/turnover/localization, orthogonal normalization and later function. |
| A6 / moderate | A bounded search can miss an important paper. A reassuring tally of sources, GLM jobs or passed tests is not a completeness estimate. | Record the omission and new query scope; explicitly retain “rapid scoping review,” and distinguish prior review from fresh primary reading. |
| A7 / presentation | Slide 2's mouse observation → everolimus inhibition layout understates the competing mechanism; the supplied read-aloud script shares that omission. | New slide 2 and narration show the conflicting signal. Keep the requested cover-line removal and the exact published trial plot. |
| A8 / feasibility | Clone/day minima and a large model menu are not powered, available laboratory capacity. | Add transparent 126-allocation base arithmetic, staged feasibility and explicit pre-confirmatory requirements; no invented power, budget or timeline. |
| A9 / exposure, retained | The new 50 nM culture result can look numerically close to a recorded 52.1 nM whole-blood peak. These quantities are not interchangeable. | Store conditions separately; forbid clinical-margin inference. No concentration is recommended for this child. |
| A10 / alternatives, retained | HCQ raises BUBR1 in the same paper, tempting a reversed shortlist. | Retain its 100 micromolar, two-hour protein endpoint and lack of functional/exposure bridge; do not promote HCQ or invent an everolimus/HCQ rescue combination. |
| A11 / bias control | A contrary paper could trigger overcorrection. Positive non-cancer everolimus functional evidence and pediatric experience must remain visible. | Add HGPS vessel results and retain labelled TSC experience; neither is MVA evidence. No universal harmful/ineffective claim. |
| A12 / administrative, retained | A revised script/deck, public code, AI consensus or passing integrity checks cannot finish Track 2. | Keep recording/hosting, provider verification, owner/live checks and receipt open. No readiness promotion. |

## Primary-source adjudication

### The omitted drug experiment

[Goutas 2023](https://doi.org/10.1016/j.redox.2023.102701), Results/Figure 6 and
Methods, used Wharton's-jelly mesenchymal stromal cells from three donors, cultured
with 10% FBS. Early/late passage and oxidative-stress models are not the selected
BUB1B pair. At 24 hours the reported nominal everolimus condition was 50 nM; the
separate three-hour condition was 100 nM. Late-passage BUBR1 protein decreased at
24 hours; early-passage cells did not show the same pattern. HCQ at 100 micromolar
for two hours increased late-passage protein abundance.

This is more compound-proximal adverse-mechanism evidence than an unrelated rapamycin
experiment, but still not drug-induced segregation failure, exact-pair toxicity or a
clinical margin. The paper's late-passage SAC defects are not a demonstrated effect
of everolimus treatment. Cell-state, synthesis and population effects require controls
before assigning a protein decrease specifically to degradation. HCQ accumulation is
not functional rescue. Three donor cultures and Student t-tests do not establish broad
population reproducibility; no numerical effect size was extracted or invented.

### mTOR activity is not an intervention direction

[Sieben](https://doi.org/10.1172/JCI126863) remains a motivating observation in
heterozygous `+/X753` mouse muscle, not the submitted pair. Neither rapalog rescue nor
causal harm from pathway excess was tested. Its [corrigendum](https://doi.org/10.1172/JCI144781)
corrects Figure 2E lymphatic-tumour images/methods, not the Figure 5 mTOR blots; do not
use the correction as if it specifically invalidated the phosphoprotein finding.

[Quy](https://doi.org/10.1074/jbc.M112.399949) reports worse denervation atrophy with
rapamycin. [Castets](https://doi.org/10.1038/s41467-019-11227-4) shows temporal and
genetic-context dependence, including greater atrophy with muscle Raptor loss.
These are counterexamples to a universal inhibition rationale, not direct MVA harm.
A weak secondary disease mechanism might still be treatable; insisting that it be
the initiating or genotype-exclusive event would be another reasoning error.

### Positive evidence survives the challenge

[Abutaleb](https://doi.org/10.1038/s41598-023-32035-3) reports improved vasoconstriction
with everolimus in HGPS engineered vessels; monotherapy did not establish improved
vasodilation. LMNA/progerin biology, small experiments and nominal exposures limit
transfer. Combination findings cannot all be credited to everolimus. Selected
Results/Figures 4–5 and Methods were reviewed, not the entire supplement. This is a
useful functional-assay precedent and a counterweight to a blanket toxicity claim.

The [everolimus label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)
retains specified pediatric TSC indications. Its limited open-label follow-up did
not appear to show adverse growth/puberty effects, with explicit uncertainty and
no comparator in that follow-up. Renal, infectious and other warnings remain. The
right conclusion is unknown MVA benefit/risk, not inevitable growth harm or general
pediatric safety.

### Trial boundary remains correct

[ARST1431](https://pubmed.ncbi.nlm.nih.gov/38936378/) retains 297 evaluable participants,
HR 0.86, 95% CI 0.58–1.26 and p=0.44. It neither establishes EFS benefit for that
temsirolimus addition nor proves zero effect. It does not test constitutional
everolimus rescue. Its absence of benefit is a tumour-claim boundary, not direct
counterevidence to every constitutional effect. The deck's logarithmic plot remains
unchanged. The favourable active-comparator ARST0921 evidence is retained separately.

## Coverage of all Track 2 workstreams

This table audits the complete decision/workflow scope. “Retain” means the current
bounded interpretation survives; it does not mean every source was freshly read.

| Workstream | Strongest objection tested | Disposition / reading basis |
|---|---|---|
| Selected alleles and phase | Competition recovery might be mistaken for phase/function/drug-response confirmation. | Retain the distinction; use existing local audits, no subject-file reread or phase inference. |
| HPO and copy-number context | Single-symptom anchoring; family history as a proband feature; screen as karyotype. | Retain separate family-history scope and screening limits; no treatment/subtype inference. |
| Atlas AVI/attribution | Reused consequence/conservation evidence could be double counted. | No drug-ranking weight; preserve composite-only results, null server-version pin and failed molecular requests. Existing audit reviewed; no new API call. |
| Splicing archive | Low unsigned scores could be mistaken for normal splicing. | Retain raw-magnitude interpretation and missing tissue/junction evidence; no new cache job. |
| Everolimus | Wrong mechanism direction and missed direct-compound adverse mechanism. | Revise as above; fresh selected primary sections and method extraction. |
| HCQ / autophagy | Protein accumulation or adult RCC response could be promoted to pediatric rescue/selectivity. | Reserve only; new Goutas reading plus preserved adult positive/negative reviews. Haas indexed primary abstract rechecked; no new full-trial reread claimed. |
| Temsirolimus / RMS trials | Class, backbone and population transfer; null result as zero effect. | Benchmark only; ARST1431 primary abstract rechecked, prior detailed trial review retained. |
| Pralatrexate | Fusion-positive specificity assumed for the child; thymidine rescue as unique TYMS assignment; regression as cure. | Tumour-only horizon; primary title/abstract identity rechecked, prior selected-section relapse/toxicity reading retained. |
| Phenylbutyrate | A predicted missense change implies a repairable folding defect. | Deprioritized; no verified repairable defect or functional rescue. No new efficacy paper claimed. |
| Bortezomib / proteostasis | General toxicity mistaken for selective benefit. | Deprioritized; preserve exposure and deficient-normal tests. Prior primary review. |
| Metformin | Combination response attributed to metformin; incompatible PK or Ewing results transferred to RMS. | Deprioritized, with positive pediatric combination exception retained. Prior primary review. |
| NMN / nicotinamide / SIRT2 | NMN abundance result conflated with transgenic lifespan; precursor and sirtuin-inhibitor effects conflated. | No approved-drug rescue promotion; North primary abstract/selected Results rechecked. No universal nutritional or toxicity claim. |
| Ataluren / gentamicin | Reporter rescue equals intact functional protein; historical approval assumed current. | Excluded as present clinical candidates. EMA non-renewal rechecked; prior functional-assay/regulatory distinctions retained. |
| Senolysis / HSP90 | Genetic cell clearance or Ercc1 benefits transferred to drug rescue in BUB1B deficiency. | Excluded as constitutional priority; preserve tissue-dependent p21 and unstable-BUBR1 objections. Prior primary review. |
| Checkpoint inhibition | BUB1/BUBR1 confusion and tumour killing as constitutional repair. | No constitutional priority; retain distinct proteins and selectivity limits. |
| PP2A chemistry/recruitment | Alignment under arrest, isolated binding and disputed drug annotation combined into faithful division. | Optional mechanistic controls only; preserve conflicting primary studies and assay-specific claims. Prior primary review. |
| Entinostat / vorinostat | Approval jurisdiction, combination antagonism, transient case response and daily/weekly schedules ignored. | Deprioritized; NMPA scope freshly rechecked; prior favourable/contrary primary reviews retained. |
| TBX screen / niclosamide / pyrvinium / piroctone | Reporter/extrapolated EC50s and reformulation treated as matched free exposure. | Deprioritized; original/reformulation counterbalance retained. Prior primary review. |
| Posaconazole / statins / redox agents | Growth delay as eradication; missing interactions; survivor reseeding; contradictory mechanism attribution. | No promotion; prior source disputes and normal-tissue/exposure gaps remain unresolved. |
| Additional progeria hits | Progerin-targeted peptide or lonafarnib biology transferred to this genotype. | HGPS vessel result retained as indirect counterweight; UPCP primary abstract identifies a different mechanism and unapproved peptide, not a new MVA candidate. |
| GLM / Firecrawl / K-Dense | Job/tool counts or AI agreement as scientific replication; local hosting as local inference. | Preserve actual provider and retrieval-depth disclosures. No model/tool exercise repeated to force agreement. |
| Exposure ledger | Conversion mistaken for pharmacologic comparability. | Existing eight-record checker passes; new culture observations are separate with null margins. |
| Experimental plan | Pseudoreplication, informative tracking loss, undefined margins, stage mismatch and causal overidentification. | Retain nested-unit and missingness safeguards; add A3–A5 controls. Numerical thresholds/power still require pilot qualification. |
| Report/deck/video/release | Attractive slides or hundreds of tests as evidence or upload readiness. | New v9 content, local render and frozen package; no recording, hosting, account-policy verification or receipt. |

## Search and reading depth

Targeted public searches included `BUBR1 BUB1B mTOR rapamycin everolimus tissue muscle
rescue aneuploidy`, `BUBR1 deficiency treatment rescue 2025 2026`, `BUBR1
hydroxychloroquine senescence`, the exact Goutas title, `BUBR1 everolimus`, `BUB1B drug
rescue 2026`, `BUBR1 phenylbutyrate`, the ARST1431 title/numbers, the Haas DOI,
the pralatrexate DOI, `BubR1 nicotinamide SIRT2 2014` and the HGPS vessel/UPCP titles.
Date: 2026-09-19. Search locators and snippets were followed to primary records or
official sites; reviews/vendors were not accepted as primary support.

Identifier search for `102701|37094517|Goutas` in the preserved September 8 search
and selected-fulltext archives and current Track 2 notes returned no match. This is
a traceable search-coverage omission, not proof of its cause or a claim that every
prior retrieved record was fully screened. The new searches are neither exhaustive
nor independently dual-screened. Absence from a query is not absence of evidence.

The fixed public Europe PMC XML requests for PMC6934189, PMC10149375, PMC3542997,
PMC11550893 and PMC6639401 returned two valid articles and three HTTP 500 failures.
The later balancing request for PMC10050176 succeeded. Requests/results/hashes are in
`results/feat009/adversarial-v9-primary-20260919/retrieval*.json`. No failures were
converted to negative studies. Three XML articles supported selected-section reading;
JCI/Quy/ARST1431 used accessible indexed primary sections/abstracts or the official
correction as specified. Browser CAPTCHA/access failures were retained, not bypassed.

| Local primary XML | SHA-256 |
|---|---|
| PMC10149375 / Goutas | `ad1d093ae75cbff333e882d80aa8169ba75fb258b33630d2907b5b77986d9f47` |
| PMC6639401 / Castets | `2f2e6a322483e7ed7a35ca47e4e4cd7e9fd8b413fd63f7d6253a04ade75f4759` |
| PMC10050176 / Abutaleb | `51de25de4f3753c11fed436e4d312c77955972e46417113846775da4d0c02c8d` |

Retrieval is reproducible with a public request to
`https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML`; the local
operation parsed the XML article root, saved bytes, recorded SHA-256 and extracted
paragraph/title/caption text. No subject input or credential was needed. Existing
files must not be overwritten; service availability and bytes may change.

## Re-review of the proposed correction

The author challenged the revision itself: do not call late-passage stromal cells an
MVA model, protein loss chromosome damage, HCQ abundance functional rescue, a culture
value clinical exposure, or denervation a model of this child's muscle phenotype.
Do not demand genotype exclusivity/early causation, discard positive HGPS function,
or infer a need for irreversible drug withdrawal when reversible benefit could be
real. These boundaries are explicit in the revised report and protocol.

The strongest retained contribution is a falsifiable benefit/harm study with complete
cell accounting. The weakest area is still biological and pharmacologic translation,
not deck aesthetics or software correctness. No current evidence supports a numeric
probability of efficacy, a therapeutic margin or a guaranteed competition result.

## Verification and deliverables

The revised ledger contains 36 cumulative source records and 11 decisions, including
four newly incorporated primary studies; this is not 36 newly or completely read
papers. All 450 Track 2 tests pass (13 new v9 integrity/content regression tests),
as do 108 AlphaGenome tests, the core self-checks, unchanged Track 1 v4 byte checks
and the eight-record historical exposure checker. The latter and the old sensitivity
command reproduce historical decisions, not v9 priority. The v9 checker returns no
rescue-priority candidates and a null clinical margin. Tests check implementation
and retained qualifiers; they cannot establish scientific truth.

All five final PDF pages were visually inspected after rasterization. The deck has
320 visible words (40/72/60/72/76), minimum 24 px slide text, zero text overlap or
out-of-bounds text, and no horizontal overflow at 640 px. It retains the v8 palette,
regular serif headings, static inline SVG, exact trial plot and requested cover-line
removal. Slide 2 now contrasts distinct experimental contexts; the arrow denotes
the reported protein change, not a demonstrated degradation pathway or patient harm.
The final PDF has five 960 × 540 pt pages and no JavaScript. The narration has 339
words; three-minute timing remains a rehearsal target, not measured runtime.

```bash
uv run python scripts/track2_release_v9.py check
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python -m unittest discover -s scripts -p 'test_alphagenome*.py'
uv run python scripts/test_track2_release_v9.py
uv run node scripts/render_track2_slides_v9.mjs v9-slide-review-final-20260919
uv run pdftoppm -png -scale-to 1280 results/feat009/v9-slide-review-final-20260919/track2-slides-v9.pdf results/feat009/v9-slide-review-final-20260919/pdf-page
uv run python scripts/track2_release_v9.py build results/feat009/jvv7_track2_research_v9
uv run python scripts/track2_release_v9.py verify results/feat009/jvv7_track2_research_v9
```

Source HTML SHA-256:
`c84e0ca12d7c47aaa63d04b23e1b099843e367161beb1ec33fc7a4e4877dcf8c`.
The final PDF, five page previews and overview are under
`results/feat009/v9-slide-review-final-20260919/`; source/code/export hashes are in
`render.json`. The v9 snapshot binds six files/84 inputs and recursively verifies
v1-v8 preservation. No previous bound source was edited. Fresh init output and
publication-audit commands/results are recorded in `progress.md`.

Recording/hosting, Fireworks settings verification, final owner/live submission
checks and receipt remain outstanding. This completes the requested desk audit and
revision, not the Track 2 submission or biological validation.
