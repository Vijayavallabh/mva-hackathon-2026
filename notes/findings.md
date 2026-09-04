# Findings

## 2026-09-02 — feat-004 baseline

The first offline genome-wide coding/splice triage identifies a BUB1B compound-heterozygous
pair as the leading hypothesis. One allele is a known stop-gained pathogenic/likely
pathogenic variant; the other is a rare/absent missense candidate with concordant damaging
SIFT and PolyPhen predictions. Both source calls are PASS, heterozygous, high quality and
balanced.

Interpretation status: **leading candidate, not confirmed**. The two sites are unphased,
and the missense allele needs manual evidence review. The phenotype match uses all seven
proband observations; parental reproductive history is retained as a separate dimension
and contributes zero to this candidate's score. Full evidence and commands are in
`notes/vcf-triage.md`.

## 2026-09-03 — feat-005a copy-number/BAF screen

The GC- and mappability-corrected whole-genome screen resolves the preliminary chr20
outlier as technical bias: its corrected depth interval spans one and its BAF-excess
interval spans zero. Chr22 has a small depth shift but no independent BAF support. Chr19
retains joint depth and BAF evidence at both mappability thresholds, consistent with an
approximately 4–9% low-level mosaic gain signal.

Interpretation status: **credible screening signal, not a clinically confirmed mosaic
trisomy**. This result neither proves causality nor phases the leading small variants. The
BUB1B alleles remain unphased, and trans phase remains unconfirmed. Full methods, aggregate
results and limitations are in `notes/copy-number-screen.md`.

## 2026-09-04 — feat-005b targeted missed-allele screen

All four FASTQ lane pairs were realigned and independently re-called across every gene
surviving feat-004. The screen retained 24 rare coding/splice rows, but none adds an allele
in BUB1B, CEP57 or TRIP13 and none is supported by both callers. Structural discovery found
no high-quality event in the BUB1B or CEP57 windows; one TRIP13-window event remains an
unvalidated local review item. These findings do not displace the leading BUB1B pair.

Read-backed phasing across the padded BUB1B locus found both leading alleles but left both
unphased, without a shared phase set. Interpretation status: **BUB1B remains the leading
candidate; trans phase remains unconfirmed**. Full methods, aggregate counts, commands and
limitations are in `notes/targeted-recall.md`.
