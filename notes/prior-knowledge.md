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
