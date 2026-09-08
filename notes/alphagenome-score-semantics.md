# AlphaGenome Atlas score semantics and validation contract

Reviewed 2026-09-08 for feat-009 using public source only. This note prepares a
bounded, authenticated lookup; it does not report that a lookup succeeded. This
reviewer did not read `.env`, access credentials, run the external helper, or query
any variant. Preserve submitted Track 1 bytes, unknown clinical exposure margins
and unconfirmed trans phase.

## Source pins

- Client: `google-deepmind/alphagenome`
  `aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d`.
- Helper: `google-deepmind/science-skills`
  `28b8482603a420708c8896f6fe5e06c276d9933d`.

These are **client/source revisions**, not verified model or Atlas dataset versions.
The inspected [Atlas protocol](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/protos/atlas_service.proto)
has no explicit model/dataset release field. Preserve UTC time, metadata and returned
bytes/hashes; leave an unknown release identifier unknown. The API package name
`v1main` is not a substitute for an immutable dataset version.

## Raw score, calibration and displayed PHRED

The official helper reads `AVI_SCORE.X` as the raw score and the optional
`AVI_SCORE.layers['quantiles']` as a **CDF** value. Its conversion computes
`tail = max(1e-7, 1 - cdf)` and `phred = -10 * log10(tail)`. Its exported
`avi_quantile` is then the **tail**, not the original API CDF. Keep distinct field
names such as `api_cdf_quantile` and `tail_fraction`; otherwise the same word can
quietly invert the ranking. [Pinned helper, `_cdf_to_phred` and `_score_single_variant`](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py)

| API CDF | Tail fraction | Displayed PHRED | Meaning |
|---|---:|---:|---|
| 0.90 | 0.10 | 10 | Top 10% of the calibration score distribution |
| 0.99 | 0.01 | 20 | Top 1%, not 99% disease probability |
| 0.999 | 0.001 | 30 | Top 0.1%, not an effect-size estimate |
| 1.0 | Unresolved at returned precision | Helper caps at 70 | Do not report an exact observed tail of `1e-7` |

Proposed local validation, not an upstream guarantee:

- Raw AVI must be a finite scalar; no `[0,1]` bound is documented for raw logits.
- Validate finite CDF in `[0,1]` **before** conversion. Do not let the helper's clamp
  make an invalid input appear usable.
- Preserve the unclipped complement where representable, the display convention,
  and whether clipping occurred. Float32 calibration limits tail precision.
- Missing calibration means PHRED unavailable. Missing or non-finite raw score means
  unavailable, not zero. Never mix raw and PHRED values in one numeric ranking.

## Shape, identity and attribution

The protocol transports row-major float32 arrays with explicit shapes; calibration
is optional. The SDK converts each scorer to AnnData: matrix values in `X`, gene or
variant observations in `obs`, track metadata in `var`, and calibration in a
`quantiles` layer. The single-variant return must be checked against the requested
allele, not assigned an identity merely because it arrived after that request.
[Protocol](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/protos/atlas_service.proto),
[conversion and client code](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/atlas/atlas.py)

For the narrow single-variant composite check, require one AVI value and one
18-feature vector, with exactly one requested variant and 18 unique, recognized
feature names. Bind values by returned `var['name']` order; the static enum's order
does not establish server tensor order. Reject duplicate names, inconsistent shapes,
unknown labels or missing metadata rather than guessing. Reordered recognized labels
are acceptable after explicit name binding.

The static expected set consists of ten molecular features
(`MERGED_SPLICING`, `MAX_ABS_RNA_SEQ`, `MAX_ABS_ATAC`, `MAX_ABS_DNASE`,
`MAX_ABS_CHIP_TF`, `MAX_ABS_CHIP_HISTONE`, `MAX_ABS_CAGE`, `MAX_ABS_PROCAP`,
`MAX_ABS_POLYADENYLATION`, `MAX_ABS_CONTACT_MAPS`) and eight other features
(`ALPHAMISSENSE`, `CACTUS_241_WAY`, `PROTEIN_TERMINATION`, `START_LOST`,
`STOP_LOST`, `PHASTCONS_470_WAY`, `IS_INSERTION`, `IS_DELETION`). The helper picks
the largest **absolute** attribution, which may be negative. Negative contribution
is not automatically decreased gene expression.
[Official `AviFeature` and attribution helper](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py)

### SHAP additivity is a diagnostic, not an invented strict gate

The launch manuscript's overview describes the 18 contributions as summing to raw
AVI. Its methods describe expected-gradients SHAP approximating `f(x) - f(0)`, with
a zero-feature background. An all-zero feature vector does not itself prove a zero
model output. No baseline output or approximation error estimate is present in the
inspected Atlas response schema. [Manuscript, feature-attribution methods](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

Record `raw_minus_sum_attributions` using full returned precision. Do not invent a
baseline to force agreement or hard-fail solely because the residual exceeds an
arbitrary machine-epsilon tolerance. A stable residual across examples is not proof
of a universal baseline. Conversely, agreement on one public example is not a
validated error tolerance. A local serialization check such as `rtol=1e-5` and
`atol=1e-6` would test numerical copying only, **not** scientific SHAP additivity.
Report contribution percentages, if any, only with an explicit denominator and
signed-versus-absolute convention; do not imply literal percentages of causality.

## Molecular scores: preserve gene and tissue context

**Molecular calibration is not universally AVI calibration.** For signed molecular
scorers the official documentation maps calibration CDF `p` to `2*p - 1`, giving
`[-1,1]`; unsigned scorers retain `[0,1]`. Use the returned scorer metadata's
signedness, preserve the generic API quantile and never apply the AVI PHRED formula
to signed molecular calibration. A synthetic RNA-seq value of `-0.97` is therefore
valid, not a missing response. The reported finite-background saturation in the
base-model documentation is not an independently verified Atlas-release precision
guarantee. [Official calibration FAQ](https://www.alphagenomedocs.com/faqs.html#what-is-the-difference-between-a-quantile-score-and-raw-score)

Session 35 independent review caught and corrected the initial authenticated
parser's universal `[0,1]` gate and misleading generic CDF label. This was a real
code defect; the first failed live pair request had insufficient stage diagnostics
to establish that this defect was the cause of that particular failure.

`query_variant` supports scorer, gene and ontology filters. In the inspected filter
builder, scorers are OR-combined, genes/IDs are OR-combined, and filter groups are
AND-combined. Ontology filtering exempts scorers with no ontology metadata; gene
filtering has no corresponding exemption. Therefore request AVI and its feature
breakdown **without gene filters**, and request molecular results separately with
explicit relevant filters. A tissue filter does not turn global AVI into a
tissue-specific composite. [Filter implementation](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/atlas/atlas_utils.py)

Choose tissue/cell CURIEs from live returned track metadata, not from patient HPO
terms. HPO describes phenotypes; it is not the biosample catalogue. Keep unfiltered
results separate from a declared relevant-tissue subset. Preserve scorer name,
signedness, track name, biosample, ontology, gene ID/name, strand and junction bounds
where supplied. An effect on a neighbouring gene is not automatically a BUB1B
effect; an all-track maximum is not a normal-cell measurement. If no suitable tissue
exists, record that coverage gap instead of relabelling another cell line.

Do not copy these helper shortcuts into a rigorous parser:

- `np.nan_to_num` before finding maxima converts missingness into apparent values.
- Flattening all matrices and selecting element zero can hide extra rows or wrong
  identities.
- Batched SDK requests collect futures in completion order; bind by returned variant,
  never original list position.
- The inspected SDK's junction observation columns are spelled `junction_Start` and
  `junction_End`; accommodate verified schema explicitly, not an assumed spelling.

These are directly observed implementation behaviours, not evidence of a failed
production response. [SDK](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/atlas/atlas.py),
[helper](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py)

## Public control and stopping criteria

Use the official helper's public DNM1 example, **GRCh38 `chr9:128225994:G>A`**,
as a transport/parser smoke control, with `AVI_SCORE` and
`AVI_SCORE_FEATURE_IMPORTANCE`. This exact allele is documented in the
[pinned example](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/SKILL.md).
Do not substitute a neighbouring portal example or claim a predicted numeric value
without obtaining it. A successful control means valid access, identity and shape—not
validation of patient causality, drug response or assay calibration.

The main session should stop before candidate requests if credentials, metadata,
control identity/shape, or terms/account scope fail. Empty scorers, absent calibration,
non-finite values and network/authentication failures must remain distinguishable.
Metadata or control success does not authorize a whole-VCF annotation, interval scan,
clinical-narrative upload or on-the-fly inference. A bounded candidate request, if
performed, must use only explicitly permitted submission-derived alleles and must
record its exact payload scope without recording credentials.
