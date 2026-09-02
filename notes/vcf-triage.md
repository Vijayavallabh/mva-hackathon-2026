# VCF triage baseline (feat-004)

This is the reproducible first-pass baseline for later ranking work. The pipeline runs
entirely offline. Subject-level normalized/annotated VCFs and candidate tables remain in
gitignored `results/feat004/`; tracked files contain code, methods, aggregate counts and
permitted reviewed findings only.

## Reproduce

```bash
./scripts/run_vcf_triage.sh --self-check
mkdir -p logs
nohup env MVA_TRIAGE_THREADS=8 ./scripts/run_vcf_triage.sh \
  > logs/feat004-triage.log 2>&1 </dev/null &
```

The default is eight workers. The 2026-09-02 pre-run resource snapshot recorded 64 physical
cores, 465 GB available RAM and 3.75 TB free disk, but a live load average near 25 and four
busy A100s. VEP is CPU-bound here; no GPU was used. Intermediate stages have checksum-bound
completion markers and are reused only when the input, resources and pipeline code match.

## Filtering and annotation

1. Retain `FILTER=PASS` on primary contigs `1`–`22`, `X`, `Y`, and `M`.
2. Left-align against the exact challenge reference and split multiallelic sites with
   `bcftools norm -m -any`, preserving allele-depth sums.
3. Join the pinned GRCh38 ClinVar release by exact chromosome, position, REF and ALT.
4. Intersect the normalized callset with all Ensembl 116 exons plus 20 bp on either side.
   The 401,607 merged windows span 227,971,665 bases and retain canonical splice regions.
5. Run VEP 116 offline against its indexed GRCh38 cache. Keep one MANE/canonical-preferred
   coding or splice consequence and add gene symbol, HGVS, SIFT, PolyPhen and gnomAD v4.1
   frequencies.
6. Retain records with a populated VEP consequence, then coding/splice candidates with
   consequence severity at least splice-region and
   maximum observed population AF no greater than 1% (or absent). Missing AF is retained
   but receives less rarity evidence than a measured very-low AF.

The raw VCF has 5,012,204 records. There are 4,740,790 PASS records; 116,485 records are on
non-primary contigs. Applying PASS and primary-contig criteria together retained 4,661,873
records. Normalization split 65,872 multiallelic records and realigned 39,670 records, with
zero REF mismatches removed, yielding 4,727,745 biallelic records.

## Models and phenotype score

The primary model is an unphased candidate compound heterozygote: two heterozygous rare,
damaging alleles at different loci in the same autosomal gene. Same-position alternate
alleles are never paired. A transparent +3 model prior reflects the challenge's public
compound-heterozygous answer-key statement; it does not restrict which genes are searched.

The secondary model is a rare heterozygous dominant singleton. Because the supplied VCF has
no parental samples, `de novo` is a hypothesis, not an observation. Likewise, candidate
compound pairs are not proven to be in trans; the tables explicitly say parental phasing is
required.

For each gene, HPO associations are propagated through the ontology and compared using
information-content semantic similarity. The proband score averages the best match for all
seven proband terms, so a single striking feature cannot dominate; coverage out of seven is
also reported. `HP:0200067` is calculated as a separate family-history similarity and has a
small mechanistic weight. It is never included in proband coverage.

The combined score is a prioritization heuristic, not a pathogenicity classification:

```text
compound = 3 + mean(two variant scores) + 8 × proband similarity
           + 0.75 × family-history similarity
dominant = one variant score + 8 × proband similarity
           + 0.5 × family-history similarity
```

Variant score combines consequence severity, VEP impact, measured rarity, SIFT/PolyPhen,
ClinVar and soft penalties for low depth, low genotype quality or imbalanced heterozygous
allele depth. Separate compound-het and dominant tables prevent one model from crowding the
other out of inspection.

## Coordinate contract

Every local VCF stage retains the source's unprefixed contigs so reference and resource joins
remain exact. Candidate tables perform one explicit presentation conversion: `1` becomes
`chr1`, and similarly for the other primary contigs. This is required because the challenge
scorer uses exact tuple equality and does not normalize chromosome names.

## Limitations

- Single-sample data cannot establish inheritance, de novo status or trans phase.
- VEP's selected transcript is a reproducible baseline, not a substitute for reviewing all
  biologically relevant transcripts around final candidates.
- The first pass focuses on coding/splice variants. Deep-intronic, repeat-adjacent, CNV and
  structural mechanisms require later analyses; the supplied VCF has no CNV/SV records.
- HPO annotations are incomplete and biased toward known disease genes. Genome-wide search
  is retained, and BUB1B/CEP57/TRIP13 are not hard-coded into the score.

## Outputs

The local run writes:

- `results/feat004/pass.primary.normalized.clinvar.vep.vcf.gz`
- `results/feat004/all_candidate_models.tsv`
- `results/feat004/candidate_models.tsv`
- `results/feat004/compound_het_candidates.tsv`
- `results/feat004/dominant_candidates.tsv`
- `results/feat004/candidate_qc.json`
- `results/feat004/pipeline_qc.tsv`

Final aggregate results and reviewed candidate interpretation are appended only after the
full run and validation complete.

## Completed baseline results — 2026-09-02

The exon-window stage retained 308,080 records. VEP assigned a selected coding/splice
consequence to 29,701 records. The rare-damaging filter retained 418 alleles across 366
genes and generated 115 compound-pair hypotheses plus 195 dominant-singleton hypotheses.
The review table keeps only the highest-scoring hypothesis per gene and model; the complete
pair enumeration remains in `all_candidate_models.tsv`.

The leading genome-wide compound-heterozygous hypothesis is **BUB1B**:

| | Allele 1 | Allele 2 |
|---|---|---|
| GRCh38 submission tuple | `chr15:40209701 T>G` | `chr15:40220612 T>G` |
| Genotype | `0/1` | `0/1` |
| DP / GQ / alternate balance | 46 / 99 / 0.543 | 28 / 99 / 0.464 |
| MANE consequence | stop gained, p.Leu737Ter | missense, p.Asn1002Lys |
| maximum population AF | 0.00009982 | absent from queried VEP fields |
| prediction / clinical database | ClinVar pathogenic/likely pathogenic; multiple submitters, no conflicts | SIFT 0.01 deleterious; PolyPhen 0.997 probably damaging; no ClinVar assertion |

Both alleles were independently re-queried from the source VCF and are PASS, heterozygous,
high-GQ records with balanced allele depth. Their selected transcript is
`ENST00000287598.11`. The BUB1B hypothesis has proband semantic similarity 0.648435 and
coverage 6/7; its separately computed family-history similarity is 0. It ranks first
without receiving any family-history boost and without restricting the search to known MVA
genes.

This is a strong candidate, not yet a confirmed result. The VCF is unphased, so the alleles
are not proven to be in trans. The stop allele has [public ClinVar support for
MVA1](https://www.ncbi.nlm.nih.gov/clinvar/RCV000641226/); the p.Asn1002Lys allele remains a computationally supported candidate requiring
manual evidence review. Do not convert this table into a submission until feat-006 validates
the exact CSV and scorer behavior.

Aggregate reproduction:

```bash
cat results/feat004/pipeline_qc.tsv
cat results/feat004/candidate_qc.json

tools/install/bin/bcftools query \
  -r 15:40209701,15:40220612 \
  -i '(POS=40209701 && REF="T" && ALT="G") || (POS=40220612 && REF="T" && ALT="G")' \
  -f '%CHROM\t%POS\t%REF\t%ALT\t%FILTER[\t%GT\t%DP\t%GQ\t%AD]\n' \
  data/WGS_EX2312012_HGWCNDSX7.vcf.gz
```
