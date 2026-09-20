# Evo2 FP8 runtime compatibility audit

Session 52, 2026-09-21. This technical amendment follows a 40B runtime exception,
before any 40B benchmark or candidate score. The original plan, weights, inputs,
scoring code, windows, strands and strict numerical/functional gates remain fixed.

The source-built FlashAttention 2.8.0.post2 resolved the prebuilt wheel's C++ ABI
failure. The 40B environment additionally required its isolated cuDNN library path.
Transformer Engine 2.3.0 then raised a cuBLAS unsupported-parameter error during the
first official forward test. A standalone 512-by-512 FP8 Linear operation reproduced
the same failure on one H100, before loading Evo weights. This distinguishes the
observed failure from a candidate-specific score or evidence of biological effect.

The first environment combines the prebuilt Transformer Engine CUDA-12 core with
Torch 2.6.0's cuBLAS 12.4.5.8. The bounded follow-up tests a separately locked cuBLAS
12.8.4.1 library directory via explicit per-process library preloading. The original
environment and failed output directory are preserved. No driver, system package,
model weights, model math settings or FP8 requirement is changed. The isolated
cuDNN 9.3.0.75 override is also explicit; compatibility is tested, not presumed.

First repeat the small FP8 operation. Only if it executes, retry the original 40B
run in a new directory and require the original expected-loss tolerance and exact
reference-score repeat. Do not loosen these gates or disable FP8 to obtain scores.
All errors and original attempts remain archived. A passing technical check is
not clinical validation or a guarantee of every input's numerical fidelity.

The [official Evo2 instructions](https://github.com/ArcInstitute/evo2) require FP8
for the 40B checkpoint and tests after configuration changes. NVIDIA documents
[CUDA minor-version compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)
with feature restrictions; an adequate major-version driver is not a universal
compatibility guarantee. The runtime/library test therefore determines whether
this isolated combination is usable for the fixed research comparison.

The initial `LD_LIBRARY_PATH` test still loaded cuBLAS 12.4 (queried runtime version
120405); Torch's library search precedence defeated that attempted override.
Explicit `LD_PRELOAD` of the isolated `libcublasLt.so.12` and `libcublas.so.12`
then reported version 120804, with both actual loaded paths in the isolated
compatibility environment. The same minimal FP8 operation succeeded with output
shape (1,128,512). The full retry uses a new `cublas128v2` output directory;
`outputs/evo2_40b-runtime-cublas128v2.json` records library and launcher hashes.
Transformer Engine still emits its FlashAttention version-range warning; the
installed version follows Evo2's instructions, and neither warning nor a successful
small operation substitutes for the model-level numerical gate.


The corrected two-H100 runtime passed the official forward test (mean loss
0.21569824 versus expected 0.2159424; difference below 0.001) and an exact repeated
reference score. It completed the 96 fixed BRCA1 controls (AUROC 0.92014) and the
first short-window candidate. The first 32,768-base candidate then exhausted GPU
memory while requesting a 16 GiB allocation. This is a resource failure, not a
negative biological score. The separate fixed
[memory amendment](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evo2-memory-amendment.json) moves all four prespecified
candidate/window comparisons to eight idle H100s and requires strict numerical,
reference and duplicated-candidate agreement before any integrated report.


The eight-H100 continuation passed the same official loss (0.21569824), with zero
difference both on the repeated reference and against its two-H100 reference
score. All four strand-specific reference/alternate likelihoods for the duplicated
8,192-base L737Ter comparison matched the original two-H100 values exactly. These
checks justify combining the declared hardware split; they do not turn BRCA1
qualification into clinical validation or make model scales interchangeable.


All four eight-H100 candidate/window comparisons completed. The final summary
explicitly combines the original 96-row benchmark with the continued four-row
candidate matrix, retaining the failed runs and duplicated short-window record.
The local result audit checks both models' complete matrices and provenance.
The follow-up is complete; no GPU job remains running.
