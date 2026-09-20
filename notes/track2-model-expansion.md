# Track 2: ensemble, model size and structural falsification

2026-09-20–21 · Session 52 · Feat-009 · Computational research addendum.

The owner authorized expanded modeling on the eight-H100 host. The campaign uses
public UniProt BUBR1, permitted candidate protein notation and published experimental
controls. Raw subject files, clinical narrative, project `.env` and credentials are
excluded. All remote work is under `~/v/mva-track2-expanded-20260920/`, with the
previous pilot preserved. This directory belongs in the deletion inventory.

The five-checkpoint ESM-1v ensemble and ESM-2 at 3B and 15B test dependence on
checkpoint, model size and sequence context. Boltz-2 tests whether structural
comparisons are interpretable against the same experimentally studied controls.
These are correlated computational comparisons, not independent biological
replications. No model score establishes a therapeutic benefit.

## Completed sequence-model findings

[All seven checkpoint results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-esm-expanded-results.json) retain 147
variant/window scores, including every failed control comparison. Numerical repeats
were exact. Only ESM-1v checkpoints 1 and 5 pass the primary gate in all contexts.
The five-checkpoint ensemble itself fails in the N-terminal window. Its candidate
means are −0.0554, −0.1052 and −0.2482 in the N-terminal, C-terminal and domain
contexts, respectively; individual checkpoints change sign in every context.
These ranges are model sensitivity, not confidence intervals.

| Checkpoint | Primary gate across three contexts | N1002K: N-terminal / C-terminal / domain |
| --- | --- | --- |
| ESM-1v 1 | Pass / pass / pass | +0.709 / +0.586 / +0.483 |
| ESM-1v 2 | Fail / pass / pass | −0.393 / −0.447 / −0.265 |
| ESM-1v 3 | Fail / fail / pass | +0.103 / +0.354 / +0.335 |
| ESM-1v 4 | Fail / fail / pass | −0.019 / −0.193 / −0.566 |
| ESM-1v 5 | Pass / pass / pass | −0.677 / −0.827 / −1.228 |
| ESM-2 3B | Fail / fail / pass | −7.137 / −7.489 / −7.514 |
| ESM-2 15B | Fail / fail / fail | −10.096 / −9.403 / −8.865 |

The larger ESM-2 models produce stronger sequence-incompatibility scores for the
candidate, but fail the experimental-control qualification. Score magnitudes are
not calibrated across models. Their outputs cannot be used as validated evidence
of allele function. Conversely, the positive pilot scores cannot support benignity.
The session-51 pilot is reproducible but is not representative of the full
checkpoint/scale comparison. The selected control set tests one narrow assay
extrapolation; failure does not prove a model universally inaccurate.

The 15B run actually used an H100: 145.41 seconds after its initial checkpoint
checksum, with 56.85 GiB peak allocated tensors. These numbers exclude download,
setup, initial hashing and non-PyTorch allocations. More capacity did not repair
its control-ordering failure.

## Completed Boltz comparisons

Both arms completed 24 structures, each checked against its exact intended protein
sequence and all 324 residue positions. See the
[single-sequence results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-boltz-single-summary.json) and
[shared-MSA results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-boltz-msa-summary.json).

The public-WT-only alignment request returned 623 records, including the query;
this is not 623 independent homologs or experiments. Without the alignment, WT
mean pLDDT ranged 0.327–0.341 and its three seed-pair C-alpha RMSDs were
19.43–21.25 Å. Fine structural interpretation of that arm is unsupported.

With the alignment, WT pLDDT rose to 0.872–0.877 and its seed-pair RMSDs were
0.585–1.013 Å. However, impaired D911N also had high pLDDT, 0.876–0.877; other
impaired and retained controls likewise produced similar confident folds.
N1002K pLDDT was 0.872–0.874, with mutant/WT cross-seed RMSDs 0.415–1.223 Å.
These predictions do not demonstrate functional discrimination or a repairable
folding defect. A model can confidently predict a folded conformation without
predicting how much functional protein survives in a cell.

## Completed AlphaFold2 comparisons

The [separate prospective plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-alphafold-plan.json) produced all 120
predictions: eight sequences, five AlphaFold2 pTM parameter sets and three seeds
(11/12/13), using ColabFold 1.6.3 and alphafold-colabfold 2.3.20. All use the same
324-residue construct and public-WT-derived alignment, three recycles, no early
stopping, templates, relaxation or dropout. This is AlphaFold2, not AlphaFold3.
Every expected sequence and C-alpha position passed the output checks. The
[complete results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-alphafold-results.json) retain every parameter set and
seed; the most confident prediction was not selected as the answer.

On AlphaFold's 0–100 pLDDT scale, WT averaged 85.74–88.40 and N1002K averaged
85.47–88.14. Within the same parameter set, WT seed-pair C-alpha RMSD ranged
0.148–1.274 Å; N1002K/WT comparisons ranged 0.292–1.319 Å. Impaired D911N also
produced high confidence (85.57–88.69) and similar folds (0.078–1.269 Å versus WT).
The 330 pairwise comparisons reuse 120 predictions and are not 330 independent
observations. Confidence and fold similarity cannot distinguish the experimental
control functions here, establish the candidate's normality, or justify a
folding-rescue drug. AlphaFold and Boltz also share alignment and evolutionary
information; their agreement is not independent functional validation.
[AlphaFold source](https://github.com/google-deepmind/alphafold),
[ColabFold source](https://github.com/sokrypton/ColabFold).

## Evo2 DNA-model comparison

The [fixed Evo2 plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-plan.json) separates numerical qualification,
a public BRCA1 assay benchmark and diagnostic candidate DNA-context comparisons.
The 7B run completed all 96 controls and four candidate/window comparisons;
[all results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-7b-results.json) retain both forward and reverse strands.
Its official self-test mean loss was 0.34716797 versus the expected 0.3476563,
within the fixed 0.001 tolerance. The repeated reference score was identical.

For the 48 functional and 48 loss-of-function BRCA1 controls, the descriptive AUROC
was 0.94184, and the median alternate-minus-reference mean log scores were
−0.0005812 and −0.0050846, respectively. This passes the fixed resource-qualification
gate. It is a small, deliberately balanced, deterministic subset of the published
Findlay saturation-editing benchmark, not clinical validation; possible overlap
with pretraining and transfer from BRCA1 to BUB1B remain unresolved.
[Official benchmark example](https://github.com/ArcInstitute/evo2/tree/main/notebooks/brca1).

| Evo2 7B candidate | 8,192-base window | 32,768-base window |
| --- | ---: | ---: |
| L737Ter | −0.00768372 | −0.00203502 |
| N1002K | −0.00161082 | −0.000342846 |

Values are the average of the two strand-specific changes in whole-window mean
log likelihood. Both substitutions are less sequence-compatible in these settings;
that does not establish their functional effect or classify them clinically.
Averaging over more bases changes the score scale, so the smaller magnitudes in
the long window cannot be read as a reduced biological effect. Reference windows
came from public GRCh38; alternates were constructed synthetically from the
permitted report-derived tuples. They are not subject haplotypes and do not encode
phase. Scores do not measure splicing, NMD, drug response or tissue exposure.
The 7B run took 162.0 seconds after initial checkpoint hashing and peaked at
30.33 GiB allocated tensors, including the 32,768-base comparisons.

The 40B checkpoint's first FP8 runtime failed before biological scores. After
isolating the cuBLAS mismatch, the fixed 96-row benchmark completed with AUROC
0.92014; FUNC/LOF median deltas were −0.0011114/−0.0063219. The first long-window
candidate exhausted the two-H100 allocation. The
[runtime](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-runtime-amendment.md)
and [memory amendments](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-memory-amendment.json)
preserve both failures and every partial output. Neither failure is biological
evidence or a zero score.

The all-eight-H100 continuation completed all four fixed candidate/window
comparisons. Its numerical loss was 0.21569824 versus expected 0.2159424, within
the original tolerance. Reference repeats, the original reference score and all
four strand-specific likelihoods of the duplicated short-window candidate matched
exactly across placements. The [full 40B results](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-40b-results.json)
explicitly combine the two-H100 benchmark with the eight-H100 candidate matrix;
this was not one uninterrupted run.

| Evo2 40B candidate | 8,192-base window | 32,768-base window |
| --- | ---: | ---: |
| L737Ter | −0.01058024 | −0.00273630 |
| N1002K | −0.00208712 | −0.000533462 |

Both models' diagnostic DNA scores are negative for both candidates, but agreement
may reuse evolutionary/pretraining information. It cannot override the protein
control limitations, establish a mechanism, or validate drug rescue. The 40B model's
lower descriptive BRCA1 AUROC is not a statistically established model ranking.
The eight-H100 continuation took 94.06 seconds after initial checkpoint hashing;
peak allocated tensors ranged 7.70–46.80 GiB per device. Setup, hashing and the
original benchmark/OOM time are additional and retained in the archived statuses.


## Fixed questions and controls

[The campaign plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-model-expansion-plan.json) was saved and hashed before
expanded inference. It explicitly acknowledges that checkpoint 1 had already been
observed in session 51. This is an extension, not a blinded validation study.

The ESM score remains masked `ln P(alternate) − ln P(reference)`, evaluated in
residues 1–1022, 29–1050 and 721–1044. All seven models use float32 with TF32 disabled.
The primary ordering compares retained-function D882N with impaired V793R, K795R
and D911N in each context. K795A and D882A remain secondary checks; their shared
sites do not provide independent replication. D882A's original supplementary panel
has not been independently reviewed. The underlying controls are engineered
reconstitution assays, not clinically benign/pathogenic labels.
[Primary control study](https://doi.org/10.1016/j.devcel.2012.03.009).

Unlike the earlier resource-allocation pilot, this fixed comparative campaign
retains candidate diagnostic outputs even from a model failing the primary gate.
This prevents an ensemble selected only from passing models. A failed gate bars
functional interpretation; it is never converted to a missing or zero score.
Every prespecified checkpoint and window must be present before aggregation.

Boltz-2 2.2.1 uses wild type, all six controls and N1002K in the published 721–1044
construct, seeds 11/22/33, three recycles and 200 sampling steps, one diffusion
sample per job. It uses the upstream bf16-mixed default and `--no_kernels` on
torch 2.5.1+cu124. There are no ligand, affinity or template inputs. The upstream
downloader requires the affinity checkpoint to be present, but no affinity
inference is requested. This is upstream Boltz, not a benchmark of Anthropic's
optimization kits or a claimed exact/fast-mode equivalence.

The [MSA amendment](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-structure-msa-plan.json) was fixed before inspecting any
structural output. It repeats the same 24 jobs with a shared homolog alignment,
changing only its first query row for each substitution. One bounded ColabFold
search receives only the public wild-type domain. Both arms and all seeds are
retained. An MSA does not supply independent functional observations.
[Official Boltz prediction documentation](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md).

## Experimental-structure audit

The [coordinate audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-structure-reference-audit.json) checks the deposited
sequence and actual C-alpha coordinates separately. Human PDB 5KHU chain Q contains
219 observed C-alpha positions spanning 18–308; 6TLJ chain S contains 293 spanning
19–345. Neither resolves residues 721–1044 or N1002, although both list a deposited
1050-residue BUBR1 sequence. These entries therefore cannot validate a prediction
at the candidate site. This is a bounded audit of the two full-length-mapped human
entries, not proof that no relevant structure could exist elsewhere.
[5KHU](https://www.rcsb.org/structure/5KHU),
[6TLJ](https://www.rcsb.org/structure/6TLJ).

## Technical provenance

The [public provenance manifest](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-model-provenance.json)
retains model-resource hashes, pinned Evo revisions, all structural registrations
and public DNA-source URLs/hashes. The ESM result ledger separately retains each
checkpoint digest and runtime. Digests identify received upstream bytes; they are
not independent signatures or evidence of model accuracy. Exact reproduction
requires the recorded checkpoint digests and pinned revisions; a future fetch
from a changing upstream `main` is not automatically the same resource.

The initial 3B attempt stopped during model loading because upstream fair-esm
requires its official contact-regression companion. No inference was produced.
The separate resource script retrieves and hashes both ESM-2 companion files;
contact prediction stays disabled. The retry uses the identical scoring script,
plan, weights, precision and windows, in a new output directory. The failed log
and initial worker status remain archived.

Each ESM result binds the plan, public reference, scoring script, pilot helpers
and checkpoint digest. Structural registration binds the input sequences,
schedule and locked environment. The analysis checks every output sequence and
residue coordinate, then retains all wild-type seed pairs and all mutant/WT seed
combinations. Pairwise combinations are sampling diagnostics, not a sample-size
increase. Confidence and C-alpha RMSD are not thermodynamic stability, protein
abundance, PP2A recruitment, checkpoint function or pathogenicity measurements.

At the start, the host had three substantial pre-existing workloads. Jobs were
assigned to available GPUs 2/4/5/6/7 with resource checks; no existing job was
terminated and no driver/system package was changed. A later check found all eight
devices idle; Evo2 7B uses one H100. The 40B benchmark uses two; its
long-context continuation uses all eight after a memory failure. All environments,
managed Python, caches, temporary files and logs stay under the authorized `~/v` tree.

Local artifacts and commands:

```bash
uv run python scripts/test_track2_model_expansion.py
uv run --with numpy python scripts/test_track2_structure_analysis.py
uv run --with biopython==1.84 python scripts/track2_structure_reference_audit.py \
  results/feat009/model-expansion-sources-20260920 <new-audit-output.json>
```

Remote scoring, downloads and structural jobs use `uv run --frozen` and `nohup`
logs. Locked environments are recorded in `scripts/track2_esm_pilot.uv.lock`,
`track2_boltz.uv.lock`, `track2_alphafold.uv.lock`, `track2_evo2.uv.lock`,
`track2_evo2_fp8.uv.lock` and the isolated `track2_evo2_cublas.uv.lock`.
The corresponding TOML files describe the final environments; Evo files explicitly
named `bootstrap_environment.toml` retain earlier setup attempts and are not the
final inference specifications. Exact
commands, status records, prerequisites and source hashes are retained with the
results. Use new directories for reruns; do not overwrite the original attempts.

## Reanalysis and archive

The completed protein-model archive is
`results/feat009/model-expansion-remote-v1/completed-protein-models-v1.tar.gz`,
SHA-256 `789c2bc60a20051f3d7731844894924eb2afbdff8c408462eb771db0f73d994c`.
It contains public inputs, output structures, logs and scripts, not model weights
or environments. Its regular files were extracted locally; the two absolute
public-input symlinks were materialized from the identical files inside the
archive, without following an external target. All structural analyses were then
recomputed locally and the ESM ensemble rebuilt from all seven run summaries.
The [audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-protein-model-audit.json) passes 71 bound-file checks and matches
all values to 1e-10. This checks provenance and arithmetic, not biological validity.

```bash
uv run --with biopython==1.85 --with numpy==2.0.2 python scripts/track2_alphafold_analysis.py \
  results/feat009/model-expansion-archive-v1 <new-alphafold-analysis.json>
uv run --with biopython==1.84 --with numpy==1.26.4 python scripts/track2_structure_analysis.py \
  results/feat009/model-expansion-archive-v1 <new-single-sequence-analysis.json>
uv run --with biopython==1.84 --with numpy==1.26.4 python scripts/track2_structure_analysis.py \
  results/feat009/model-expansion-archive-v1/msa-arm <new-msa-analysis.json>
uv run python scripts/track2_model_result_audit.py \
  results/feat009/model-expansion-archive-v1 <new-audit.json>
```

Use new output paths; the writers refuse to overwrite. The initial local analyses
succeeded with uv-managed Python 3.13 and compiled NumPy packages. Redundant
Python-3.12 attempts subsequently hit the existing-output guard and produced no
replacement; they are not additional independent validations.

The complete Evo archive is
`results/feat009/model-expansion-remote-v1/completed-evo2-v1.tar.gz`, SHA-256
`2dc84faf0b1a0187857f593378f1a2f64a54e32cb57c60b8d38c4c0d60181bcc`.
The [Evo audit](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-result-audit.json)
checks both 100-row matrices, input identities, all score arithmetic, numerical
and benchmark gates, environment hashes and the declared continuation. The same
96 public controls are reused across models; they are not 192 independent assays.

```bash
uv run python scripts/track2_evo2_result_audit.py \
  results/feat009/model-expansion-evo-archive-v1 <new-evo-audit.json>
```

## Disclosure and practical boundaries

ESM, Boltz, AlphaFold2 and Evo2 inference executes on the owner's remote machine.
Public model/resource downloads use their documented upstream HTTPS sources. ColabFold
is an additional external alignment service; its use must be disclosed separately
from owner-hosted neural inference. No training/retention claim is made for that
service. No subject sequence or candidate substitution is sent to it.

Preserve v12 and every earlier release. This addendum is additional research and
is integrated, with failed controls and provider disclosure, into the new
[v13 report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v13.md). The new eight-page v13 deck and 329-word script
also integrate the findings and disclosure; historical files remain preserved.
The bundle is not an uploaded entry, recording, wet-lab result, phase test,
clinical exposure estimate or treatment recommendation.
