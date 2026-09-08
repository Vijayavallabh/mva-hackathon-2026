# AlphaGenome merged-splicing score: offline interpretation

Reviewed 2026-09-09, session 36, feat-009. This independent review uses public
documentation and source code only. It did not read `.env`, invoke an API, process
subject VCF records or access clinical narrative. Archive verification and local
lookups are performed separately by the main session; this note does not invent
their results.

## What the downloaded number measures

The published merger is:

```text
merged_splicing = max(raw_splice_sites)
                + max(raw_splice_site_usage)
                + max(raw_splice_junctions) / 5
```

Each component is aggregated across available genes/tracks; underlying spatial
scores also aggregate relevant positions or junctions. The three maxima can arise
from **different** contexts. This is a sum of unsigned model-effect magnitudes,
not a signed splice-direction estimate or three independent experimental findings.
The junction contribution receives a smaller weight because its numerical scale is
larger. [Official tutorial](https://www.alphagenomedocs.com/colabs/splicing_variant_scoring.html),
[Atlas manuscript, input-feature methods](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

For example, component maxima of `0.10`, `0.20` and `2.0` produce
`0.10 + 0.20 + 2.0/5 = 0.70`. This arithmetic example is not an observed variant
or a 70% probability. The aggregate is neither AVI nor AVI PHRED, a SHAP value,
SpliceAI delta, percent spliced in, nor measured transcript abundance.

## Components and transformations

| Component | Public implementation | Information lost in the scalar |
|---|---|---|
| Splice-site class | Maximum absolute REF/ALT probability difference under a gene mask | Which donor/acceptor position changed, and the direction |
| Splice-site usage | Maximum absolute REF/ALT usage difference under a gene mask | Which site and tissue drove the change |
| Junctions | Absolute difference of natural logs of predicted junction counts, each with `1e-7` added, followed by aggregation | Which junction/tissue and whether predicted counts increased or decreased |

The inspected research code uses gene-body/strand-aware processing. Junction scoring
restricts to protein-coding, variant-overlapping genes, processes at most 256 splice
sites, and can return an empty result when no eligible gene/junction is present.
The junction implementation casts the log difference through float16 before returning
absolute scores; the downloaded decimal should not imply unlimited precision.
[Gene-mask implementation](https://github.com/google-deepmind/alphagenome_research/blob/0db53bd4352c66d1e00a049a81da373a066e6670/src/alphagenome_research/model/variant_scoring/gene_mask.py),
[junction implementation](https://github.com/google-deepmind/alphagenome_research/blob/0db53bd4352c66d1e00a049a81da373a066e6670/src/alphagenome_research/model/variant_scoring/splice_junction.py)

These code details establish the inspected **research implementation**, not a verified
producer revision for the downloaded archive. Its exact build/model provenance cannot
be deduced from an SDK revision. The client also marks all three recommended splicing
scorers as unsigned. [Pinned scorer definitions](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/models/variant_scorers.py)

## Range, calibration and thresholds

The official tutorial describes a nonnegative, theoretically unbounded range; most
values reportedly fall between 0 and 6. It notes that scores above 1 often show large
effects, while explicitly stating that a recommended cutoff is still being developed.
This informal observation is **not** a validated clinical threshold, sensitivity
estimate or negative predictive value.
[Tutorial interpretation section](https://www.alphagenomedocs.com/colabs/splicing_variant_scoring.html)

Consequently:

- Require finite, nonnegative numbers; do not reject a legitimate value merely for
  exceeding 1 or 6.
- Do not convert this raw merged score using the AVI CDF-to-PHRED formula.
- Do not borrow thresholds from another predictor or call values below 1 benign.
- A low finite value supports only a small **predicted aggregate splicing effect in
  the scored model contexts**. A larger comparison value is useful context, not a
  calibrated likelihood ratio.

## Genome coordinates and missingness

The Atlas resource is GRCh38/hg38-reference anchored. The manuscript excludes ambiguous
reference bases and non-reference-to-non-reference changes, and the initial public
release is SNV-only. Reference/alternate reversal is not an equivalent lookup.
[Atlas manuscript, indexing and data availability](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

The main session inspected this public archive's header:

```text
#CHROM  POS  REF  ALT  alphagenome_splicing
```

Fields are tab-separated. The main session parsed the accompanying TBI header:
24 contigs; format `2` (VCF preset); sequence column `1`, start column `2`, end
column `0`; comment byte `35` (`#`); no skipped lines and no zero-based flag.
Contigs are `chr1` through `chr22`, `chrX`, and `chrY`. The preset does **not** turn
this five-column table into a valid VCF. Use indexed text retrieval and an explicit
five-column parser, not a VCF record reader. For its 1-based SNV point at `POS=p`,
a 0-based half-open indexed request is `[p-1,p)`, followed by exact
chromosome/position/REF/ALT matching and local reference verification. Keep the
original row value, not just a rounded report number.

No inspected primary source established that an absent row in this specific archive
must mean a zero score. Distinguish `found_zero`, `found_positive`, `not_found`,
`malformed_or_nonfinite`, `reference_mismatch`, `ambiguous_duplicate` and index/read
failure. The first displayed records do not prove full-genome coverage or explain
all omissions. Never fill missing archive records with zero.

The tutorial's convenience `fillna(0)` and default-zero component retrieval are not a
missing-data contract for bulk downloads. Likewise, an empty model gene/junction
result is not a negative experimental observation. The aggregate archive does not
retain component completeness, so it cannot retrospectively demonstrate which
components were computed or omitted for an individual row.

## Interpretation for Track 2

Low merged-splicing scores cannot establish that a coding allele is harmless:
protein termination, altered protein function, transcript decay and other mechanisms
are not excluded by a small splice-effect scalar. They also cannot prove normal
splicing in unrepresented cell types, developmental states or experimental conditions.

If the exact selected alleles have low scores after archive/index/identity validation,
the defensible revision is: **this resource does not add strong predicted splicing
support for those alleles**. Do not claim that it disproves the coding mechanism or
confirms the proposed drug mechanism. The scalar cannot specify a junction-directed
intervention, demonstrate functional rescue, establish clinical drug exposure/safety,
or resolve cis/trans phase. Trans remains unconfirmed.

A documented public splice-effect example can test access and provide scale context.
Other alternate alleles at the same public positions are useful allele contrasts,
but are not validated benign controls. Tissue/junction-resolved predictions and
appropriate RNA/protein/function experiments would be needed to refine mechanism.
No wet-lab result is implied by this lookup.

## Provenance and review limits

The research skill directed this independent review. Sources inspected were the
official tutorial, the cached public Atlas manuscript and pinned client/helper code.
The research-code pin was independently resolved to
`0db53bd4352c66d1e00a049a81da373a066e6670`, committed 2026-09-02 11:45:55 UTC;
client pin is `aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d` and helper pin is
`28b8482603a420708c8896f6fe5e06c276d9933d`. The review did not benchmark thresholds,
estimate false-negative rates or scan the whole archive. Download integrity, exact
Tabix semantics and actual queried values must be documented with the main session's
commands and artifacts, separately from these interpretation rules.
