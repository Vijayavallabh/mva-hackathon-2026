# V31 execution details

The [fixed plan](track2-perturbseq-plan-v31.json) precedes inspection of target
expression effects. Schema inspection found 247,914 retained RPE1 cells and 310,385
retained K562 essential-screen cells. BUB1B has one paired-guide construct in each
cell line, with 106 and 141 cells respectively. The pair is shared across cell lines.
These are cell subsamples of pooled experiments, not 247 independent perturbations.

Implementation details fixed before the GPU pilot:

- Normalize by the deposited **full library UMI count**, since the exported count
  matrix contains a subset of measured genes. Do not normalize by its smaller row sum.
- Select common features using core-control mean counts of at least 0.25 in each
  cell line. No target expression response enters feature selection.
- Each split uses distinct control cells for its two halves. Matching controls by
  gemgroup prevents differing batch proportions from creating an apparent target
  effect. At least 20 controls per included batch gives at least 10 per half.
- Retrieval references contain non-control constructs with at least 30 cells. Report
  full reference denominators and all ten prespecified queries, including missing ones.
  Broader retrieval counts are context, not calibrated accuracy for BUB1B; the primary
  feature exclusion removes the ten query transcripts, not every reference's transcript.
- Null pseudo-perturbations match each query's batch counts. Their cells are excluded
  from the reference controls. Each relevant batch must retain at least 20 reference
  controls. The tail count describes this finite, conditional reference only; it is
  not biological FDR, a clinical probability or independent replication.
- Three feature views: all selected features; remove ten query transcripts; remove
  those transcripts plus the 97-gene Seurat/Regev list distributed in the official
  [Scanpy tutorial](https://scanpy.readthedocs.io/en/stable/how-to/cell-cycle.html).
  File SHA256: `eb666ba4f7b7a8b2845e1586d42687feaf813e9fa1fdadba89dacd4093411ac0`.
  Excluding those genes does not remove all cell-cycle biology or establish causality.
- Leave-one-gemgroup-out profiles are compared with the full profiles, which include
  retained cells. This tests influence of a partition; it is not held-out validation.
- A two-repeat pilot precedes eight workers. Source inspection required a documented
  [amendment](track2-perturbseq-amendment-v31.json): all retained non-targeting cells
  are core controls, so an unselected-control sensitivity is unavailable. The main
  wave uses four seed blocks per cell, 256 repeats per worker and 1,024 per cell.
  Extra seeds are sampling partitions, not biological replication or a substitute
  for the unavailable control test. The pilot is preserved and excluded from totals.
  Source-count CPU FP64 reconstruction checks CUDA profiles before full execution.

The original deposits are CC BY 4.0 and are credited to Replogle and colleagues,
[Cell 2022](https://doi.org/10.1016/j.cell.2022.05.013),
[Figshare](https://doi.org/10.25452/figshare.plus.20029387).
There is no subject input. No new hosted biological-model provider is involved.
The previous Anthropic ProteinMPNN campaign remains frozen; its optimizations do not
address the non-cancer perturbation question in this cycle.
