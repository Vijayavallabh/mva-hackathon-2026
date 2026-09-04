# Prior knowledge (before looking at the data)

Recorded up front so the analysis can be judged against a stated prior rather
than a hypothesis invented after the fact.

Mosaic Variegated Aneuploidy has three established gene associations in the
literature:

| Gene | OMIM phenotype | Inheritance | Mechanism |
|---|---|---|---|
| BUB1B | MVA1 | biallelic (AR) | spindle assembly checkpoint |
| CEP57 | MVA2 | biallelic (AR) | centrosome / microtubule nucleation |
| TRIP13 | MVA3 | biallelic (AR) | spindle assembly checkpoint silencing |

Implications for the search:
- Expect a **compound heterozygous or homozygous** pair, which is why the
  submission template has two allele slots per row.
- A deep-intronic or structural second allele is a known failure mode of
  exome-style triage; feat-004 exists for that reason.
- Not finding one of these three is a legitimate outcome, not a bug. Novel
  genes in the same pathway (MAD1L1, MAD2L1, CENPE, ...) are in scope.

These are candidates, not an answer. Nothing here has been checked against
this child's data yet.

---

## Checked against the data — 2026-08-28

The prior above stands as written; it was recorded before any file was opened and is left
intact on purpose. What the first screening pass (`data-profile.md`) says about it:

- **The compound-het expectation is confirmed, from an independent direction.** The
  challenge's own published `evaluation.py` describes "a clinically validated
  compound-heterozygous answer key". The two allele slots per row were the right read.
- **Homozygous-by-descent is now unlikely.** A 1 Mb runs-of-homozygosity scan found zero
  runs of ≥3 Mb. No consanguinity signal. So of the two AR routes, expect **two different
  rare alleles**, not one allele on a shared haplotype.
- **The "deep-intronic or structural second allele" failure mode is still live and is now
  the main justification for touching the FASTQ at all.** The provided VCF is a Sentieon
  diploid germline SNV/indel call set with no CNV, SV or symbolic-allele records whatsoever.
  Anything the germline caller dropped is invisible until we realign (feat-005b).
- **"Not finding one of these three is a legitimate outcome" is stronger than it looked.**
  The clinical phenotype document names no gene, no karyotype and no prior genetic testing
  at all. We were given HPO terms with presentation context, but no genetic shortlist.
  There is no external hint pointing at BUB1B, CEP57 or TRIP13 in this dataset — only the literature prior above and the organizers' public
  statement that the child is "fighting cancer cells", which fits BUB1B/MVA1. The search
  stays genome-wide; the three genes are a prior to be tested, not a shortlist to filter to.
- **The phenotype is a constellation, with scope attached.** Seven terms apply to redacted
  proband across oncologic, renal, growth, neuromuscular and perinatal domains. The eighth
  is parental/family reproductive history: retain it as evidence relevant to chromosome
  instability and inheritance hypotheses, but do not mislabel it as a proband abnormality.
  Neither that history nor the full pattern establishes inherited versus de novo origin.
  Treat the reproductive-history term as a separate phenotype input dimension: in a
  chromosome-instability model it is compatible with inherited susceptibility or a newly
  arising causal event, and genomic evidence must decide between them.
- **The preliminary aneuploidy result required correction.** Blood WGS at 45× excluded
  high-level aneuploidy but not low-level mosaicism, and its chr20-led signal was confounded
  with GC/mappability bias. Feat-005a subsequently resolved chr20 as unsupported after
  correction, while chr19 retained concordant low-level depth and BAF evidence. That is a
  single-sample screening signal, not a clinical karyotype; see `copy-number-screen.md`.

---

## Genome-wide baseline result — 2026-09-02

Feat-004 tested the prior without restricting the search to the three established genes.
The leading unique-gene compound-pair hypothesis is BUB1B: one stop-gained allele and one
missense allele at different loci, both PASS heterozygous calls with strong depth, genotype
quality and allele balance. It ranks above 114 other compound-pair hypotheses using the
same consequence, rarity and seven-term phenotype scoring policy.

This materially strengthens the original BUB1B/MVA1 prior but does not yet prove causality:
the single-sample VCF cannot establish trans phase, and the missense allele has prediction
support rather than a ClinVar assertion. See `vcf-triage.md` for tuples, evidence and exact
reproduction commands.

The independent feat-005a screen does not change that phase assessment. Copy-number and BAF
evidence cannot determine whether the two BUB1B alleles reside on opposite homologues;
**trans phase remains unconfirmed**.

Feat-005b independently realigned all lane pairs and re-called the full genome-wide survivor
set with diploid and mosaic-sensitive callers plus a target-enriched SV screen. It screened
supported coding/splice, operational deep-intronic and repeat-adjacent calls, reconstructed
novel/existing same-gene hypotheses, and found no additional BUB1B candidate or supported
BUB1B-window SV. WhatsHap found both leading alleles but could not place either in a
supported phase block. The prior is therefore unchanged: BUB1B remains first, while
**trans phase remains unconfirmed**.
