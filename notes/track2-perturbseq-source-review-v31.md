# V31 source review and consequences

7 October 2026. Eight bounded Europe PMC searches returned 98 records; all returned
titles were screened. Selected abstracts and primary-source passages were read.
This is not a systematic review or independent peer review. Exact queries, dates,
result counts and cache digests are in [the source record](track2-perturbseq-sources-v31.json).
Eight initial API requests failed with HTTP 503; revised queries succeeded. A failed
request is not negative evidence. Broad web searches supplied additional primary sources.

| Source and reading depth | Finding relevant to falsification | Consequence |
|---|---|---|
| [Replogle et al., Cell 2022](https://doi.org/10.1016/j.cell.2022.05.013); retrieved full text, read design, guide construction, filtering, normalization, cell-cycle/CNV methods and selected results | RPE1 adds a non-cancer context. Paired guides occupy one construct; core controls were selected by expression. Cells and genes were filtered. RNA-derived chromosome and cycle measures are estimates. | Count constructs, not guides or cells, as perturbation designs. Test batch influence and transcript exclusion. Retain survivor, control-selection and generic-depletion limitations. |
| [Szalai et al., NAR 2019](https://doi.org/10.1093/nar/gkz805); abstract, methods and selected results/discussion | Viability and proliferation can generate similarity between perturbations with different mechanisms. | Keep functional fate endpoints and cell-cycle sensitivity. Transcriptomic similarity alone cannot establish rescue. |
| [Ahlmann-Eltze et al., Nature Methods 2025](https://doi.org/10.1038/s41592-025-02772-6); abstract and selected benchmark passages | The evaluated deep models did not beat simple baselines on the tested perturbation tasks. This is not a verdict on every newer model or task. | Any later learned representation must beat a matched expression baseline on held-out perturbations before it changes a decision. More model complexity is not evidence of better biological inference. |
| [BubR1 cortical-loss study, 2023](https://doi.org/10.3389/fcell.2023.1282182); abstract, design and selected results | Trp53 co-deletion only partly alleviated consequences of BubR1 loss; death and genomic injury persisted. This is a mouse conditional-loss model. | A p53-associated expression difference cannot explain every consequence. Retain DNA damage, apoptosis and later tissue function alongside cell-cycle markers. No p53-suppression treatment proposal follows. |
| [NUF2/BUB1B lung-cancer study, 2025](https://doi.org/10.21037/jtd-2025-704); abstract, experimental design and selected results | BUB1B overexpression restored mTORC1-associated tumour growth after NUF2 silencing. Overexpression and tumour proliferation are different endpoints from correcting constitutional BUB1B deficiency. | Measure pathway direction in the qualified non-cancer model; do not infer that all BUB1B-related states share mTOR overactivation. Co-immunoprecipitation supports association, not by itself direct molecular binding. |
| [TORC1/cohesin study, 2026](https://doi.org/10.1093/bbb/zbag087); indexed primary abstract only, full text unavailable | In budding yeast, TORC1 inactivation caused an additional route to cohesin degradation and chromatid dissociation. | Strengthen the existing cohesion/segregation stop rule. This is a mechanistic hazard hypothesis, not evidence of a human everolimus effect or exposure threshold. |
| [BIOMEDE, 2026](https://doi.org/10.1038/s41591-026-04354-1); abstract and selected design, safety, biomarker and discussion passages | The primary survival comparison with a historical DIPG cohort met futility criteria. Randomization was among active treatments. Exploratory mTOR-associated signals and relatively favorable tolerability remain. | Preserve both unfavorable primary evidence and favorable exploratory findings; neither establishes benefit in MVA or an unrelated tumour. Do not describe the historical-control contrast as placebo-randomized. |
| [TEAMMATE, 2025](https://doi.org/10.1001/jama.2025.14338); indexed primary abstract, full-text request failed | In selected six-month pediatric heart-transplant survivors, an everolimus/low-tacrolimus regimen met its comparative safety criterion and did not improve the primary efficacy composite; some secondary renal/CMV outcomes favored it. | Do not claim everolimus uniformly worsens renal outcomes. Equally, this combination-regimen result cannot establish MVA safety or a tissue exposure margin. |
| [ARST1431](https://pubmed.ncbi.nlm.nih.gov/38936378/); refreshed indexed abstract; earlier review retained | The temsirolimus addition did not significantly improve the trial's primary event-free survival outcome. | Existing negative tumour evidence remains; do not transfer a class hypothesis into a proven RMS benefit. |
| [Everolimus label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=67e62e26-448d-46ec-b5a1-00dc1b5e26c6); indexed label warnings | Renal failure, infection, metabolic and wound-healing risks remain relevant. Different product indications and regimens are not interchangeable. | Preserve injury monitoring and null clinical margins. No dose conversion or dosing recommendation is made. |

The refreshed autophagy search also recovered the previously reviewed
[mitotic-error/senescence study](https://pubmed.ncbi.nlm.nih.gov/37094517/) and
[older rapamycin chromosome-malsegregation findings](https://pubmed.ncbi.nlm.nih.gov/9914383/).
They remain in the historical challenge record. Newly finding an old source is not a
new experiment. HCQ is not promoted by adverse evidence about another candidate.

No raw subject inputs were searched or transmitted. The Anthropic toolkit was rechecked
as a source of optimizations; the completed v29 ProteinMPNN execution remains the
relevant use. This cycle tests an experimental dataset with CUDA statistics, not a new
neural model, protein design or drug-response simulation. All inherited provider and
distribution qualifications remain unresolved as previously recorded.
