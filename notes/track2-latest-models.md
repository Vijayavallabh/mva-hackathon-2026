# Track 2: newer-model falsification follow-up

2026-09-21 · Session 53 · Feat-009 · Computational research addendum.

**AlphaFold3-derived findings below are subject to the [AlphaFold3 Output Terms](alphafold3-output-terms.md)
and [Legally Binding Terms of Use notice](alphafold3-Legally-Binding-Terms-of-Use.txt).**
Coordinates are unchanged; CA-coordinate comparisons and numerical summaries are our
derived analyses. Cite Abramson et al., [Nature (2024)](https://doi.org/10.1038/s41586-024-07487-w).

The owner requested the newer models identified after the v13 comparison. The
[fixed plan](track2-latest-model-plan.json) retains the earlier controls, three protein
windows and exact 100-row public-reference DNA design. Model families were selected
before this cycle's scores; earlier results were already known. This is a model
comparison, not an independent clinical validation or a complete survey of every
state-of-the-art model.

All inference runs locally on the owner's H100 host, under
`~/v/mva-track2-expanded-latest-20260921/`. Inputs are public references, published
engineered substitutions and permitted report-derived candidates. No subject reads,
VCF records, phenotype narrative, `.env` or credentials were transferred. No new
hosted inference or alignment-service request was made. The remote directory is in
the deletion inventory. Prior v1–v13 inputs and packages remain unchanged.

## What changed scientifically

The newer protein sequence models give consistently negative N1002K scores and pass
the small prespecified control-ordering challenge. This strengthens the **computational
case for testing the missense allele**, compared with the failed controls and sign
disagreements in the earlier ESM-1v/ESM-2 campaign. It does not erase those results,
establish the candidate's function, validate a clinical classification or prove that
the variants are in trans. The studies reuse evolutionary information and are not
independent biological replications.

Confident structures still occur for an experimentally impaired control. ESM3 also
shows substantial WT seed-to-seed structural variability. Neither high confidence
nor a small candidate/WT difference supports normal function or a folding-rescue
drug. No model measured cellular abundance, chromosome segregation, drug response,
NMD, tissue exposure or benefit to a child. The v10 drug decisions remain unchanged:
no rescue-priority drug; everolimus optional qualified mechanistic probe; HCQ reserve.

## Protein sequence comparison

ESMC 300M/600M/6B and ESM3-open 1.4B each produced 21 scores: six published controls
and N1002K in three windows. All four passed the primary control gate in every window;
repeated masked distributions matched exactly. The endpoint is natural-log
probability of alternate minus reference at a masked residue. Lower values indicate
less sequence compatibility, not a calibrated probability of pathogenicity.

| Model | N-terminal 1–1022 | C-terminal 29–1050 | Domain 721–1044 |
| --- | ---: | ---: | ---: |
| ESMC 300M | −0.190749 | −0.262950 | −0.090961 |
| ESMC 600M | −2.309415 | −2.664999 | −1.859905 |
| ESMC 6B | −6.362635 | −5.645506 | −4.718565 |
| ESM3-open | −0.269117 | −0.132473 | −0.075246 |

Score magnitudes cannot be compared as effect sizes between models. The 6B model's
larger negative value does not establish a larger biological effect. ESMC 6B used
24.13 GiB peak allocated tensors and took 14.40 seconds after its initial checksum;
setup, download, hashing and non-PyTorch allocations are excluded.

The same [published control study](https://doi.org/10.1016/j.devcel.2012.03.009)
underlies this and the previous campaign. The primary retained control is D882N;
V793R, K795R and D911N are primary impaired controls. K795A and D882A remain secondary
contextual checks. D882A's supplementary experiment was reported in the previously
read main text; the supplement was not independently reviewed. These engineered
assays do not provide clinical benign/pathogenic labels or a representative
validation set for all BUB1B alleles. The gate is a conservative directional check,
not a fitted classifier, sensitivity estimate or clinical threshold.

## AlphaFold3 and ESM3 structures

AlphaFold3 completed 120 structures: eight variants × three seeds × five diffusion
samples, ten recycles, the fixed shared 623-record public-WT-derived MSA, no templates
and no ligands. Each structure contains the 324-residue domain. All samples are
retained; none was selected after seeing the candidate results.

| AlphaFold3 | Mean CA pLDDT, 0–100 | CA RMSD versus WT, Å |
| --- | ---: | ---: |
| WT | 90.93–91.33 | 0.189–0.764 between WT samples |
| Impaired D911N | 91.12–91.59 | 0.154–0.861 |
| N1002K | 90.83–91.19 | 0.281–0.828 |

The impaired control is as confident as WT. This refutes the proposed shortcut
that a confident, similar fold establishes retained cellular function in this
comparison. It does not refute the published assay or the model's structure-prediction
benchmarks. The 1,680 pairwise comparisons reuse 120 predictions and are correlated.

ESM3-open produced 24 single-sequence structures with 64 generation steps and three
fixed seeds per variant. WT CA pLDDT averages were 85.35–87.80, but WT seed-pair RMSD
was 7.10–9.10 Å. N1002K/WT comparisons span 1.53–11.56 Å. Substantial sampling
variability prevents attribution of those global differences to the candidate.
The 24 structures and all 66 comparisons are retained.

## ESMFold2

Both ESMFold2 arms completed all 24 structures: eight variants and three seeds,
20 loops and 100 diffusion steps. One arm uses sequence alone; the other reuses
the fixed alignment. The model contains a frozen ESMC 6B backbone, so its evidence
is not independent of ESMC. Default LM-embedding dropout is 0.3 and MSA column
masking is 0.1; all seeds are retained. No templates, ligands or affinity predictions
are involved. The CA fields exported by the model use the 0–100 confidence scale;
the separate SDK confidence records use 0–1.

| ESMFold2 arm / variant | Mean CA pLDDT, 0–100 | CA RMSD versus WT, Å |
| --- | ---: | ---: |
| Sequence-only WT | 90.24–90.35 | 0.297–0.350 between WT seeds |
| Sequence-only impaired D911N | 89.70–90.06 | 0.491–0.772 |
| Sequence-only N1002K | 89.84–90.23 | 0.318–0.575 |
| Shared-MSA WT | 91.96–92.43 | 0.477–0.834 between WT seeds |
| Shared-MSA impaired D911N | 91.50–92.15 | 0.150–0.930 |
| Shared-MSA N1002K | 91.46–92.24 | 0.191–0.853 |

The newer model substantially improves sequence-only structural consistency over
our earlier sequence-only Boltz arm on this domain. That is an observed comparison
of these settings, not a general model leaderboard. The impaired control still
produces a confident, similar fold. There is no calibrated functional threshold
for these RMSDs, and no candidate/WT structural difference proves a folding defect.
All 48 structures and 132 comparisons are retained.

## Evo2 20B

The newer 20B checkpoint completed the same 96-site BRCA1 benchmark and four
candidate/window comparisons on two H100s. Its upstream mean-loss test matched
0.2166748046875 exactly, and the repeated reference likelihood also matched exactly.
The fixed benchmark AUROC was 0.9201389, with FUNC/LOF median score changes of
−0.00119607/−0.00643893. It passes the original gate, but is not better than the earlier
7B's 0.9418403 on this small selected subset. Its AUROC equals the earlier 40B's;
that does not imply identical predictions or performance on other tasks.

| Evo2 20B | 8,192-base window | 32,768-base window |
| --- | ---: | ---: |
| L737Ter | −0.01076916 | −0.00271291 |
| N1002K | −0.00208187 | −0.000537515 |

These are averages of forward and reverse-strand changes in whole-window mean
autoregressive log likelihood. Both strands remain in the result matrix. Window
length changes the scale, so smaller long-window values do not imply a weaker
biological effect. The BRCA1 benchmark cannot establish BUB1B accuracy; pretraining
overlap remains unknown. Public reference plus one synthetic alternate is not a
subject haplotype and cannot resolve phase, splicing, NMD or drug sensitivity.

## Versions and computational scope

The [source audit](track2-latest-model-source-audit.json) records pinned official
repositories and model revisions. Biohub ESM source is
`43b4548b86762edfa747b07d5f440aad3c33acee`, SDK 3.4.1.post1, using Torch 2.11.0+cu126.
Sequence scores use float32 with TF32 disabled; ESM3 generation and ESMFold2 use
their documented folding precision. Optional ESM fused kernels are unavailable in
this environment; upstream PyTorch fallbacks are used. A CUDA-13 optional-kernel
load warning does not mean those kernels ran. This is disclosed rather than treated
as numerical equivalence with every upstream optimized runtime.

AlphaFold3 source is `c0f97eda2f1f482fd94d3a38bece18c7069b4a5c`, with JAX 0.10.2.
Parameters came directly from Google's documented public download; compressed
transport size and local SHA-256 values are retained. A post-run CRC32C check matches
Google's `0h6mjg==` header; the original downloader had checked size but had no
upstream MD5 header to compare. The full local input
pipeline was skipped because a checked alignment was supplied. No claim of
full-length BUBR1, ligand-affinity or protein-complex modeling follows.

Evo2 uses current source `53f195997257c56c00e5ef8d33a54f5baad143a6` and the pinned
20B checkpoint `8b0f0a9a70c66367ed181a17d049b95699a28fed`, with Vortex 1.1.0,
Torch 2.6.0+cu124 and required FP8/Transformer Engine. The previously qualified
per-process cuBLAS 12.8 preload is retained. It uses 8K/32K inputs, not the full
one-million-base context supported by the model family.

ESM3 means the downloaded **1.4B open checkpoint**, not the hosted 7B or 98B models.
ESMC 6B is downloaded locally. Model generation and checkpoint identities should
not be confused with SDK release dates or universal state-of-the-art performance.

## Falsification search and reading depth

Alongside the fixed adverse controls and numerical checks, public searches targeted
`AlphaFold 3 limitations mutations protein stability conformational dynamics`,
`ESMC ESMFold2 limitations`, and `Evo 2 variant limitations`. Selected primary
sections were read, not a systematic review or a full-paper review of every result.

The [AlphaFold3 paper's model-limitations section](https://www.nature.com/articles/s41586-024-07487-w)
states that random seeds do not approximate the solution conformational ensemble;
its static predictions can miss relevant states. That supports treating seed variation
as computational sensitivity, not measured molecular dynamics. Conversely,
[McBride et al.'s primary abstract](https://arxiv.org/abs/2204.06860) reports population-level
correlation between local predicted strain and mutation effects. We therefore do
not claim all structural mutation analysis is impossible; our confidence/global-RMSD
comparison lacks demonstrated functional discrimination for these controls.

A newly indexed adversarial-mutation paper's PMC page returned a browser challenge;
its search snippet was not promoted to a verified full-text finding. The pinned
[AlphaFold3 known-issues page](https://github.com/google-deepmind/alphafold3/blob/c0f97eda2f1f482fd94d3a38bece18c7069b4a5c/docs/known_issues.md)
was also reviewed: its V100 and SMILES-ligand issues do not describe these H100,
protein-only runs. Its MSA sensitivity warning remains relevant; using the same
alignment aids comparison but is not exhaustive MSA optimization or independent
cross-model evidence.

## Technical deviations retained

The first download launcher selected an environment without `huggingface_hub`, then
its incremental status writer attempted to overwrite an exclusive file. No inference
occurred in that attempt. The corrected launcher used the installed Hub client and
verified every pinned checkpoint against upstream size and LFS hashes.

The first ESMC 300M invocation omitted the device filter and used default GPU 0.
It completed and released the device before inspection; no other job was stopped.
Its result is retained with `devices: null` in the original registration, rather
than relabeled as a GPU-6 run. All subsequent protein runs enforce one explicitly
selected device. A transient utilization reading immediately after ESMC 6B paused
the launcher; bounded idle checks then resumed it without rerunning completed scores.

ESMFold2 initially received a CCD **file** where its API expects a cache **directory**.
The retained failure occurred before a structure was produced. The corrected script
changes only that resource path and uses a separate output directory.

The Evo2 launcher let `uv run --frozen` reconcile one `transformer-engine-cu12`
installation with its existing lock. Consequently, the raw registration's generated
`previous_environment_reused_without_mutation: true` flag is too strong and is
superseded by this correction. The locked package, numerical self-test, repeat and
full benchmark are recorded; the flag is not evidence that environment bytes were
unchanged. Historical outputs and bound source files remain preserved.

The fixed plan inherited some prose from the earlier comparison: “all seven models,”
“both prespecified models,” the old 7B/40B runtime description and a blanket float32
limitation. The explicit new model lists and precision fields governed execution:
four protein sequence models, Evo2 20B with current source/FP8, and documented folding
precision. These copied descriptions are corrected here; the original plan's bytes,
thresholds, controls, windows and seeds remain unchanged. Its original Evo design
timestamp is inherited; the outer plan timestamp identifies this comparison cycle.

The first archive check rejected an untracked ESM `build/` directory generated by
the wheel builder. The corrected check permits only that generated directory and
still rejects tracked source changes. The finished archive contains the earlier
failed logs as well as successful outputs. Initial exact-equality comparison of
local and remote coordinate analysis detected floating-point differences; after
inspection, maximum absolute difference was 1.43e-14, within a documented 1e-10
comparison tolerance. Score values and gate decisions matched exactly.

## Complete results and reproduction

The public derived matrices are [all 84 protein scores](track2-latest-protein-results.json),
[AlphaFold3](track2-alphafold3-results.json), [ESM3 structures](track2-esm3-structure-results.json),
[ESMFold2 sequence-only](track2-esmfold2-single-results.json),
[ESMFold2 shared-MSA](track2-esmfold2-msa-results.json) and
[all 100 Evo2 20B rows](track2-evo2-20b-results.json). The [local audit](track2-latest-model-audit.json)
and [provenance record](track2-latest-model-provenance.json) bind the original plan,
source, checkpoints, runtime locks and all 685 archived member hashes. Archive size
is 37,529,461 bytes, with SHA-256
`084c764b8beb33ae831c5070e702173611c5ba8d8b88e5e61ee75ec9d715baa6`.
There are 686 files including the manifest. Model weights and credentials are absent.
The supplementary CRC32C record was created after this archive and is explicitly
stored outside it. All GPU inference finished; the final device query showed all
eight H100s idle. No other user's process was terminated.

The following local commands reproduce the archive validation and analysis without
GPU inference. Each extraction, analysis and export destination must be new; the
exporter also checks the public plan, executed scripts and runtime locks. This
checks complete outputs and arithmetic; it is author verification, not independent
experimental replication or an independent reviewer.

```bash
uv run python scripts/track2_latest_verify_archive.py \
  results/feat009/latest-model-remote-v1/latest-model-comparison-v1.tar.gz \
  results/feat009/latest-model-archive-v1 \
  > results/feat009/latest-model-archive-verification-v1.json
uv run --with numpy --with biopython python scripts/track2_latest_analysis.py \
  results/feat009/latest-model-archive-v1 results/feat009/latest-model-local-audit-v1
uv run python scripts/track2_latest_publish_results.py \
  results/feat009/latest-model-archive-v1 results/feat009/latest-model-local-audit-v1 \
  notes results/feat009/latest-model-remote-v1/af3-crc32c-postrun.json
uv run python -m unittest discover -s scripts -p 'test_track2*.py'
uv run python scripts/track2_release_v13.py verify results/feat009/jvv7_track2_research_v13
```

For a fresh inference replay, create a new owner-hosted root and update only the
scripts' root paths; do not overwrite this run. Clone the three pinned upstream
revisions, retain the exact public FASTA/alignment/DNA inputs and fixed plan, and
copy `track2_latest_esm_environment.toml`/`track2_latest_esm.uv.lock` and
`track2_latest_af3_environment.toml`/`track2_latest_af3.uv.lock` into the corresponding
environment directories as `pyproject.toml`/`uv.lock`, then use `uv sync --frozen`.
The executed downloader is `track2_latest_resources_retry.py`; the original failed
downloader is retained separately. `track2_latest_af3.py prepare` and `weights`
prepare AF3 inputs and obtain parameters directly from Google under its terms.
The recorded launcher implements AF3 and Evo2 commands, including the qualified
Evo2 cuBLAS preload. Evo2 reuses the earlier locked FP8 environment with current
source explicitly prepended, not the old package's model registry.

Use `track2_latest_protein.py score <repository> <new-label>` for each protein
sequence model and `fold EvolutionaryScale/esm3-sm-open-v1 <new-label>` for ESM3.
For both ESMFold2 arms, use `track2_latest_protein_ccd_fix.py fold biohub/ESMFold2
<new-label> --arm single_sequence` or `--arm shared_msa`; the generic historical
launcher still records the first failed CCD-file invocation. Select an actually
idle GPU explicitly with `CUDA_VISIBLE_DEVICES`; keep caches and background logs
inside the authorized root. Replays may differ numerically across hardware/software
and must repeat the unchanged numerical and functional gates.

All 543 Track 2 regression tests pass, including ten new tests of matrix integrity,
control labels, nonfinite outputs and unsupported clinical promotion. Fresh
`./init.sh`, core checks, the live publication/purge guard and immutable v13
verification pass; actual outputs are recorded in `progress.md`. The new supplement
must accompany future synthesis, including its model and AlphaFold3 output disclosure.
It does not change a submitted file, create a recorded video or close feat-009.
