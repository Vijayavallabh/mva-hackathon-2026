# Track 2: biomolecular models and GPU allocation

2026-09-20 · Session 50 · Public-source feasibility assessment, not model results.

**Recommendation:** a small, benchmarked pilot on one working H100 80 GB is
reasonable. Its purpose would be to refine the unresolved BUBR1 missense mechanism
and choose informative validation assays. There is no present justification for
reserving eight H100s or clearing all local GPUs. Model qualification, functional
rescue, normal-tissue injury and exposure remain the decisive Track 2 gaps.

No weights were downloaded, models installed, GPU jobs launched, remote host
accessed or subject inputs transferred. Current v12 deliverables and v10 scientific
decisions remain unchanged: no rescue-priority drug; everolimus is an optional
model-qualified mechanistic probe; HCQ is reserve; phase and clinical margins are
unresolved. This is an author assessment, not an independent review or exhaustive
model benchmark.

## What the proposed repository supplies

Reviewed [Anthropic's repository](https://github.com/anthropics/uplifting-biomolecular-modeling/tree/f4f62fa6592ae4938d49b1757bea0cfeff9f468e)
at commit `f4f62fa6592ae4938d49b1757bea0cfeff9f468e`. It contains 36 inference
optimization kits for existing tools. The authors describe it as a reference
release without ongoing maintenance. Faster execution does not improve the
underlying model's biological validity.

The [Boltz-2 kit](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/boltz2/README.md)
pins Boltz 2.2.1 and offers stock, exact, fast and memory-saving modes. Its claimed
output identity and speedups have **not** been tested here. Start with stock versus
exact on identical inputs/seeds; leave approximate modes out of a mutation-effect
comparison until their numerical changes are measured. H100 is the simpler initial
target: the kit documents A100 exact-mode exclusions, including a 1,024–1,099-token
band. Actual token count and peak memory must be measured for the chosen construct.
The kit requires a working NVIDIA 580-series-or-newer driver stack.

## Prioritized uses and limits

| Approach | Potential contribution | Decision and limitation |
| --- | --- | --- |
| ESM-1v variant scoring; E1 as a possible comparison | Check whether p.Asn1002Lys is unusual relative to experimentally characterized substitutions; test dependence on sequence context and evolutionary conservation | Conditional first pilot. Qualify the benchmark before interpreting the candidate. Scores are neither clinical probabilities nor drug-response predictions. |
| Boltz-2 structure prediction; Chai-1 as a sensitivity check | Map the missense site and plausible local structural or interface hypotheses against experimental structures | Conditional second stage. A difference between predicted structures does not establish altered stability or function; a normal-looking structure does not establish a normal allele. |
| Public perturbation-data analysis | Test whether BUB1B deficiency and drug perturbation support or contradict the proposed pathway direction in relevant cells | Potentially more directly useful to Track 2 than another structure. First find and qualify actual datasets, controls, cell states, dose and timing. No matched dataset was established by this assessment. |
| Boltz-2 affinity scoring or broad docking | Generate binding hypotheses for a defined target and suitable small molecules | Defer broad screening. Binding alone cannot distinguish useful rescue, growth arrest and deficient-normal injury. Everolimus presents an additional model-domain problem below. |
| Evo 2, Borzoi/Flashzoi and other genomic models | Additional sequence/regulatory predictions | Low immediate priority. A new score needs a specific unanswered molecular question and incremental information beyond the existing Atlas/AlphaMissense/conservation evidence. It cannot determine phase or therapeutic benefit. |
| Binder generation, de novo protein design, large molecular-dynamics campaigns | New molecules or detailed mechanistic hypotheses | Defer. Designed binders do not directly satisfy the approved-drug repurposing objective; dynamics need validated starting states, parameters and a decision-relevant question. |

[ESM-1v's official variant workflow](https://github.com/facebookresearch/esm/tree/main/examples/variant-prediction)
provides substitution-scoring methods and an ensemble. [E1](https://github.com/Profluent-AI/E1)
supports substitution scoring with or without retrieved homologs, but its weights
have separate attribution/license terms; the toolkit's license does not replace
them. ESM C embeddings are not automatically validated variant-effect scores.
For every selected checkpoint, verify sequence-length limits, isoform numbering,
context/window handling and licenses before execution. Do not silently truncate a
sequence or select the window giving the most damaging score.

## Attempts to disprove the value of the proposed computation

**Everolimus affinity is an especially weak starting point.** The official
[Boltz prediction documentation](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md)
warns against affinity inputs substantially larger than its training limit of
56 atoms under its specified RDKit counting convention. Everolimus has formula
C53H83NO14, hence **68 heavy atoms** by direct element counting, already above
that range. This is a domain warning, not proof every prediction is wrong or a
statement that the input parser rejects the molecule.
[PubChem compound record](https://pubchem.ncbi.nlm.nih.gov/compound/6442177)

Its established FKBP12/mTORC1 mechanism also does not require hypothetical direct
BUBR1 binding. Rediscovering a plausible binding pose would not determine whether
mTORC1 is a harmful driver or adaptive response in a relevant deficient cell.
See the [official label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6f1ae129-c21e-4c25-84c1-a6757d9a7eb2)
and the separate prospective branches in [v10 validation](track2-validation-v10.md).

**Adverse benchmark findings must be interpreted fairly.** A March 2026
[Boltz-2 evaluation preprint](https://arxiv.org/abs/2603.05532v1) reports weak
agreement with calculated free energies in two target datasets and poor agreement
among top-ranked compounds. Only its abstract was reviewed here. Its comparator
is another computational method, not definitive experimental ground truth, and
those targets are not BUBR1/mTOR. It supports benchmarking and abstention, not a
universal claim that Boltz-2 fails.

A [primary AlphaFold fold-switching study](https://www.nature.com/articles/s41467-024-51801-z)
finds failures of conformational sampling and confidence-based selection in that
specific setting. Abstract and introductory scope were read, not all methods or
supplements. It warns against equating confidence with physical stability; it does
not directly benchmark our proposed BUBR1 variants or establish that Boltz/Chai
share identical errors. Conversely, a successful wild-type reconstruction may
reflect training overlap, not prospective variant-effect accuracy.

**Agreement can recycle evidence.** Protein language models, AlphaMissense,
structures and homolog-based scores share evolutionary/training information.
Multiple agreeing outputs are not independent experimental replications. An
incremental-value comparison against conservation and the existing evidence is
required. Models cannot establish expression of a hypothetical truncated protein,
nonsense-mediated decay, trans phase, tissue exposure or developmental safety.
Do not concatenate the two alleles into one artificial protein or treat a
two-protein cofold as a validated model of compound heterozygosity.

**Expression reversal can also mislead.** Public searches returned mixed cancer,
other-gene and tissue contexts; BUB1 must not be substituted for BUB1B. No patient
RNA expression profile is available in this work. A synthetic disease signature
must not be represented as measured, and reversing proliferation-associated genes
could reflect cytostasis rather than functional rescue. The public-data route
requires its own relevance audit before any drug ranking.

## A bounded pilot with explicit stopping points

1. **Qualify inputs and controls on CPU.** Pin public reference sequences,
   experimental structures, annotations and assay sources. Select measured
   function-altering and measured near-neutral substitutions before candidate
   scoring; do not use other predictor labels as ground truth. Separate tuning
   controls from held-out checks and disclose training overlap where known. If
   sufficiently relevant controls cannot be assembled, retain exploratory status
   and do not allocate a large run.
2. **Start with one GPU.** Run a small variant-scoring baseline. Attempt structure
   prediction only if it addresses a prespecified assay-relevant hypothesis.
   Compare stock and exact inference first. Use fixed seeds, matched input context
   and all outputs; repeat structures across at least three seeds as an initial
   feasibility check. Three seeds are not biological replication or a power claim.
3. **Stop or abstain when uninformative.** Stop escalation if controls fail, the
   effect is within seed/numerical/context variability, the relevant region or
   interface is unreliable, or results add no decision-relevant information over
   existing annotations. Identical mutant/wild-type structures are indeterminate.
   Report disagreements and null results. Set any quantitative interpretation
   thresholds using control data before inspecting candidate results.
4. **Scale only after a useful pilot.** Reserve additional GPUs for a fixed list
   of control/candidate/seed jobs or demonstrated memory needs. Prefer parallel
   independent jobs to unnecessary model-size expansion. An eight-H100 host could
   shorten a justified second-stage batch; it is not needed to begin. Runtime and
   peak memory are currently unmeasured, so this is an allocation recommendation,
   not a capacity or turnaround guarantee.
5. **Use results to improve experiments.** The deliverable would be a reproducible
   mechanism/assay addendum with failed controls and uncertainty, not a promoted
   drug or a rescue claim. Any later integration uses a new immutable release.

Only public references and permitted derived candidates would be staged on an
additional host. Raw subject files and clinical narrative remain on this machine.
Audit MSA-server/network defaults; use precomputed permitted inputs and local
inference. Isolate a uv-managed environment and pin code/weights. This assessment
introduced no additional model-provider processing.

## Observed resources and reproducibility

The resource skill was run with:

```bash
uv run python /home/sports/.agents/skills/get-available-resources/scripts/detect_resources.py -o results/feat009/model-assessment-resources-20260920.json
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,driver_version --format=csv
uptime
cat /proc/driver/nvidia/version
```

Resource snapshot: approximately 503.55 GiB RAM, 454.71 GiB available and
4,775.62 GiB free disk; load average 54.22/46.34/39.04 on 64 logical CPUs.
`nvidia-smi` failed with `Failed to initialize NVML: Driver/library version mismatch`
(exit 18): NVML 580.173 versus loaded kernel module 580.178.04. GPU availability
is **unknown**, not zero; the skill's empty GPU list is a detection failure.
Freeing jobs alone does not fix that mismatch. No reboot, driver change or other
user's job termination was attempted. The offered H100 host's SSH details, driver
health and schedulable resources have not been verified.

Eight public documentation files and GitHub commit metadata were retrieved by
anonymous bounded GETs using `uv run python` with standard-library urllib,
40-second timeouts, a 5 MB per-response cap and three download workers. No foreign
code was executed. Archive:
`results/feat009/model-assessment-public-20260920/manifest.json` records every
pinned URL, SHA-256, byte count and retrieval time; all eight returned successfully.
The main README hash is
`36f47640f3e5ac7b1f7149821a5474e5091febfea44a6a1e25b50d6775541c25`.
The selected kits' task/setup/limitations sections and Boltz STOCK pins were
reviewed; this was not a source-code/security audit or performance benchmark.

Additional web searches covered model limitations, variant-effect benchmarks,
everolimus chemistry, BUBR1 mechanisms and public perturbation data. Linked primary
documentation was read where used; search hits alone are not supporting evidence.
Resource observations and document hashes are reproducible audit facts; expected
scientific value and GPU allocation above are the author's conditional judgments.
