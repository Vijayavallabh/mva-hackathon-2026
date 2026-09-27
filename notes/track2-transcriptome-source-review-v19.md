# Public perturbation analysis: rationale and adversarial review

27 September 2026. This review selected a new evidence type before inspecting its
expression values. The previous 84 protein scores, 192 structures and 100 DNA
comparisons remain unchanged. Additional fold predictions cannot measure a drug
response. Public perturbation experiments can challenge the downstream rationale,
provided that their model and measurement limits remain explicit.

The [fixed first-release plan](track2-transcriptome-plan-v19.json) tests BUB1B
knockdown reproducibility before interpreting chemical signatures. The
[second-release plan](track2-transcriptome-phase2-plan-v19.json) was added after
metadata inspection showed substantially more everolimus dose-series coverage.
Neither plan was selected using expression scores from this campaign. Metadata
and published QC values were already known, so this is not a fully blinded design.

## Evidence that could defeat this approach

- **Off-target RNAi:** the [Smith et al. study](https://doi.org/10.1371/journal.pbio.2003213)
  finds that shared shRNA seeds can drive stronger expression similarity than shared
  target genes. Its consensus and holdout methods motivate reagent-level checks.
  The primary operational gate does not verify independent seeds, exact provider
  consensus membership or the selected alleles. The post-hoc check below resolves
  membership only. A successful software gate cannot close the other gaps.
- **Unstable drug signatures:** [Lim and Pavlidis](https://doi.org/10.1038/s41598-021-97005-z)
  report poor agreement between CMap versions and dependence on expression strength,
  concentration and cell context. Retain all doses and failed QC; compare releases
  and do not select a favourable cell or concentration after inspecting scores.
- **Expression is not function:** [Hafner et al.](https://doi.org/10.1038/s41467-017-01383-w)
  measure transcription and growth in parallel and describe cases in which substantial
  expression changes occur without corresponding growth effects. Our analysis has no
  paired chromosome-segregation, regeneration or survival endpoint. Its shared-pattern
  and mitosis-control projections test specificity; they are not validated corrections
  for proliferation and can remove relevant biology.
- **Wrong counterfactual:** these releases measure drug treatment and genetic knockdown
  separately. Their correlations do not observe treatment of BUB1B-deficient cells.
  Knockdown is not the selected genotype, and opposing an adaptive expression response
  could be harmful. No correlation sign supplies a treatment effect.
- **Transfer and exposure:** tumour cells, primary adipose cells, neural progenitors
  and immortalized kidney cells remain separate. None establishes the child's tissue
  response. Culture concentrations do not establish free tissue exposure or a dose.

Contrary evidence must also constrain rejection: positive correlation does not rule out
a benefit outside expression reversal, while low-quality or absent signatures cannot
prove that a compound is inactive. Results may change the strength of the transcriptomic
rationale and the controls needed for a functional experiment. They cannot promote a drug.

## Sources, reading depth and access

Sources are the public NIH GEO releases [GSE92742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92742)
and [GSE70138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70138), the
[provider's data guide](https://clue.io/connectopedia/guide_to_geo_l1000_data),
[quality definitions](https://clue.io/connectopedia/signature_quality_metrics), and
the primary papers above. The landmark analysis differs from the provider's connectivity
algorithm: it uses rank correlations and explicitly described projections, not CMap tau.
The [public-data redistribution policy](https://clue.io/connectopedia/data_redistribution)
permits redistribution with source attribution and description of processing changes.
No authenticated CLUE dataset or access key was used.

Reading depth: provider guide/QC/policy passages; Smith's seed-effect, consensus and
holdout sections; Lim's abstract, principal retrieval results and discussion excerpts;
Hafner's abstract and selected transcription/phenotype results and discussion. These
are selected primary passages, not a systematic review or a full-paper audit. The
original CMap article was identified as [Subramanian et al., 2017](https://doi.org/10.1016/j.cell.2017.10.049);
its Europe PMC full-text retrieval returned HTTP 500. No conclusion relies on unviewed
full text. Some browser requests failed; direct public downloads of the other six
sources succeeded and their hashes are retained locally.

Searches covered GSE92742 Level5 metadata, BUB1B/L1000, connectivity-map reproducibility,
RNAi seed effects and proliferation confounding. Public metadata contains no BUB1B
CRISPR record in the inspected second release. This is a bounded resource check,
not proof that no such experiment exists elsewhere.

## Chemical identity check, before expression interpretation

The second release labels three BRD identifiers as everolimus. Their supplied
InChIKeys share connectivity but differ in stereochemical information:

| BRD identifier | Supplied InChIKey | Interpretation |
|---|---|---|
| BRD-K13514097 | HKVAMNSJSFKALM-GKUWKFKPSA-N | Matches the reference everolimus record |
| BRD-A25736793 | HKVAMNSJSFKALM-UHFFFAOYSA-N | Stereochemistry unspecified in supplied structure |
| BRD-K13154216 | HKVAMNSJSFKALM-MUKRYTAKSA-N | Supplied stereochemistry differs from the reference |

The reference match is confirmed by the [NIH NCATS record](https://drugs.ncats.io/drug/everolimus)
and [PubChem CID 6442177](https://pubchem.ncbi.nlm.nih.gov/compound/6442177).
This is a metadata discrepancy, not proof that the experimental vial contained the
wrong material. Keep the other two identifiers as separate, unresolved labelled
records; do not pool them into compound-specific everolimus evidence or a dose curve.

## Analysis semantics

The code's `shared_pc1_removed` label denotes the leading right singular direction
of the uncentered matrix of rank-normalized non-BUB1B shRNA profiles. It is not
mean-centered PCA. The growth-span projection uses the full available span of the
eight fixed control genes. Projected-out genetic controls have undefined residual
correlations and are removed from that space's reference denominator explicitly.

The resampling null recomputes the same median-over-balanced-splits statistic for
each random reagent set. It samples whole measured-gene vectors, not exchangeable
individual genes. Seed identity, reagent potency and off-target patterns are not
matched, so its tail areas and BH adjustment serve an operational reproducibility
filter, not calibrated probabilities of on-target biology or clinical accuracy.

## Follow-up that challenges the negative finding

After all primary gates failed, a separately fixed
[post-hoc plan](track2-transcriptome-followup-plan-v19.json) tested shared-pattern
removal and exact provider membership. Each consensus `distil_id` list resolved to
existing BUB1B shRNA signatures with the same cell and perturbation time. This resolves
the membership-access limitation; it does not establish independent seeds, on-target
potency or the provider's weighting. Forty-two arm/context comparisons used 420,000
additional random reagent sets and a separate BH adjustment. The original results
remain unchanged. The [findings](track2-transcriptome-v19.md) retain HT29's limited
favourable result and distinguish an operational failure from biological disproof.
