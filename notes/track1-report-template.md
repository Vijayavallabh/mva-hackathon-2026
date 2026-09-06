# Track 1: genome-wide phenotype-led variant prioritization

Participant: {{PARTICIPANT}}
Repository: {{GITHUB_URL}}
Code revision: `{{CODE_REVISION}}`
Prediction CSV SHA-256: `{{CSV_SHA256}}`

## Main finding and interpretation

The leading hypothesis is an unphased BUB1B pair: GRCh38 `chr15:40209701 T>G`
(p.Leu737Ter) and `chr15:40220612 T>G` (p.Asn1002Lys). Both are heterozygous calls in
the supplied germline VCF. Trans phase remains unconfirmed, including after read-backed
phasing of the new all-lane alignment. This is a candidate disease mechanism rather than
a molecular diagnosis, and the missense allele does not have sufficient evidence here
for an independent clinical pathogenicity classification.

Biallelic BUB1B disruption is a plausible explanation for a chromosome-instability
phenotype with malignancy. The gene was not used to restrict the initial search.
The original study linked BUB1B truncating/missense variants to constitutional aneuploidy
and cancer susceptibility ([Hanks et al., 2004](https://doi.org/10.1038/ng1449)). That
gene-level evidence supports the hypothesis but does not prove the effect or phase of
this particular pair.

## Phenotype representation

Seven standardized HPO observations were scored for the proband: HP:0002859
(Rhabdomyosarcoma), HP:0000121 (Nephrocalcinosis), HP:0004322 (Short stature), HP:0001508
(Failure to thrive), HP:0003202 (Skeletal muscle atrophy), HP:0001622 (Premature birth),
and HP:0001518 (Small for gestational age). HP:0200067 (Recurrent spontaneous abortion)
was retained separately as parental/family reproductive history. It was neither counted
as a proband abnormality nor discarded from mechanistic interpretation.

The interpretation considers oncologic, renal, growth, muscular, perinatal and family
reproductive domains together. No single feature establishes a diagnosis or inheritance
model. Protected narrative, exact ages, dates and measurements are omitted from this report.

## Data and reproducible methods

The single-subject input comprises a germline SNV/indel VCF and four paired FASTQ lanes
(eight compressed read files). The measured profile is approximately 45-fold mean depth,
5,012,204 VCF records and Ti/Tv 2.050. The exact reference is GRCh38 no-alt with hs38d1
decoy and the challenge's masked exclusions. Local contigs are unprefixed; the submission
converts them explicitly to `chr` prefixes. No CNV/SV records were present in the supplied
VCF. The absence of a long-ROH signal in the earlier screen does not establish the complete
absence of parental relatedness.

The baseline retained PASS calls on primary contigs, normalized and split multiallelic
alleles against the exact reference, joined the pinned ClinVar data by exact allele
identity, and annotated Ensembl 116 exon windows with offline VEP 116. Gene, selected
transcript, coding/splice consequence, gnomAD frequency fields and SIFT/PolyPhen predictions
were used for prioritization. The coding/splice filter retained alleles with maximum
observed population AF <=1%, or missing AF. Missing frequency is not proof of absence in
the population and receives less rarity evidence than a measured low value.

The pipeline retained 4,661,873 PASS primary records, generated 4,727,745 normalized
biallelic records, and annotated 29,701 coding/splice records after exon-window selection.
The resulting 418 rare damaging candidates produced 169 compound-pair and 195 dominant
hypotheses. Same-site alternate alleles were not paired. One best pair per gene was used
for the submitted ranking, preserving the deterministic baseline score order.

HPO gene associations were propagated through the ontology. The proband similarity
averages the best semantic match for each of the seven observations. Family similarity
is computed separately. The compound-pair score is:

```text
3 + mean(two allele evidence scores)
  + 8 * proband semantic similarity + 0.5 * family-history similarity
```

The allele score combines consequence, impact, observed frequency, computational
prediction, ClinVar annotation and quality penalties. The +3 model prior transparently
uses the organizers' public compound-pair scoring design. Neither that design nor the
ranking reveals the private answer key. The leading BUB1B score has similarity 0.648552,
coverage 6/7, and family similarity 0; its lead does not depend on a family-history bonus.

## Leading alleles: evidence and limits

| Evidence | BUB1B p.Leu737Ter | BUB1B p.Asn1002Lys |
|---|---|---|
| GRCh38 | chr15:40209701 T>G | chr15:40220612 T>G |
| Selected transcript | ENST00000287598.11 | ENST00000287598.11 |
| Coding change | c.2210T>G | c.3006T>G |
| Source genotype | heterozygous | heterozygous |
| Depth / genotype quality | 46 / 99 | 28 / 99 |
| Alternate allele balance | 0.543 | 0.464 |
| Consequence | stop gained | missense |
| Pinned annotation | ClinVar pathogenic/likely pathogenic | no ClinVar assertion in queried release |
| Computational support | predicted truncation | SIFT 0.01; PolyPhen 0.997 |

The current condition-specific ClinVar record RCV000641226.9 reports the stop allele as
pathogenic with one submitter. This is distinct from the aggregate annotation used in the
pinned pipeline. Its submitter also flags unreliable gnomAD frequency data at this locus;
the pipeline's maximum AF of 0.00009982 must therefore be treated cautiously, rather than
as precise independent rarity evidence ([ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/RCV000641226/),
checked 2026-09-06). Computational predictions for the missense allele are supporting
evidence only. No parental segregation, functional rescue or definitive shared phase
block was obtained.

## Independent screens

The all-lane copy-number/BAF screen used 100 kb bins, leave-one-chromosome-out GC
correction, mapping-quality filtering and Umap sensitivity thresholds of 0.90 and 0.95.
The preliminary chromosome 20 anomaly resolved after correction; chromosome 22 lacked
joint BAF support. Chromosome 19 retained a low-level gain signal under both masks.
This is a single-subject screening result, with no orthogonal cytogenetic confirmation,
and it neither establishes causality nor phases the small variants.

All four paired lanes were independently aligned with BWA-MEM2. HaplotypeCaller and
tumor-only Mutect2 re-called 185 genes from the initial candidate list plus CEP57 and
TRIP13 as explicit literature-prior controls. Novel calls were normalized, compared by
exact allele against the source PASS baseline, and annotated offline. Supported rare
screening retained 226 calls with overlapping categories: 13 coding/splice, 203 operational
deep-intronic and 62 low-complexity/repeat-adjacent flags. Same-gene reconstruction yielded
314 novel/existing pair hypotheses across 63 genes. None added a BUB1B/CEP57/TRIP13 small
allele under those filters.

The target-enriched DELLY screen retained 984 heterozygous PASS sites with QUAL >=300
and >=5 supporting split/paired reads; 125 overlapped a padded candidate-gene window.
No retained event overlapped BUB1B or CEP57. One overlapped the padded TRIP13 window and
remains unvalidated. The window overlap alone is not evidence that TRIP13 is disrupted.
WhatsHap found both leading BUB1B alleles, but neither entered a supported phase block.

These screens are incomplete for very low allele fractions, difficult mappings, regulatory
effects, repeat expansions and complex structural alleles. The deep-intronic definition
(>=20 bp from the nearest annotated exon boundary) is operational, not a functional
splice prediction. Low-complexity sequence is a triage flag, not repeat-expansion evidence.
Mutect2 lacked a matched normal and panel of normals; no base-quality recalibration with
validated known sites was performed. Negative screening therefore cannot exclude every
alternative mechanism.

## Exact submitted ranking

{{RANKING_TABLE}}

All ten rows are alternatives for the primary phenotype and use `finding_type=primary`.
Rows 2–10 preserve the baseline computational ordering and carry much less mechanistic
support than BUB1B. In particular, the HLA candidates are mapping-sensitive and should
not be interpreted as confirmed incidental diagnoses. No new evidence from targeted
recalling justified changing the first-ranked pair. The EPCR sequence is a declared
rank-preserving heuristic; its numeric values are not calibrated causal probabilities.

## Local submission validation

The exact CSV above has ten distinct descending EPCRs and twenty reference-confirmed,
minimal, left-aligned alleles. It passes the unmodified public scorer pinned at revision
`1c761cc23d90aebe6a011fd5b0b99517df42408c`. Assuming row 1 were the hidden truth gives
100 rank points and F-max 1.0. This is a hypothetical conformance test and provides no
measurement against the private answer key. No private ground-truth file was accessed.

## Reproduction and computational environment

All patient-data processing ran locally. The workflow uses uv, locally pinned binaries
and recorded resource checksums. Major tools are bcftools/samtools 1.24, BWA-MEM2 2.2.1,
VEP 116, GATK, DELLY 2.1.0 and WhatsHap 2.8. `tools/versions.tsv`, `tools/resources.tsv`
and `uv.lock` provide exact versions/checksums. No GPU training was used. Long alignment
and calling jobs were limited to the shared machine's available CPU/RAM and logged locally.

```bash
./init.sh
./scripts/run_vcf_triage.sh --self-check
./scripts/run_copy_number_screen.sh --self-check
./scripts/run_targeted_recall.sh --self-check
uv run python scripts/track1_submission.py --self-check
uv run python scripts/prepare_track1_package.py build --name {{PACKAGE_NAME}}
uv run python scripts/prepare_track1_package.py verify results/feat008/{{PACKAGE_NAME}}
```

The full alignment/calling commands and dataset-dependent outputs are documented in
`notes/vcf-triage.md`, `notes/copy-number-screen.md` and `notes/targeted-recall.md` at the
recorded revision. Rebuilding requires authorized local access to the challenge data;
the public code does not redistribute it. Package creation refuses to overwrite an
existing directory; choose a new package name for a later revision.

## AI assistance disclosure

{{AI_DISCLOSURE}}

AI assistance was used for code, tests, documentation and interpretation of permitted
derived summaries. The workflow restricts hosted-model inputs to allowed summaries and
submission candidates. Raw reads, alignments, VCF records and protected clinical narrative
are excluded from hosted-model inputs. Provider-account retention/training settings are
reported separately above and are not inferred from that local workflow policy.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking,
Evaluation, and Assessment Consortium for Science), with prize sponsorship from
AWS and Anthropic. We are deeply grateful to the child and their family who
generously contributed their data and their story to advance research into this
rare disease. We acknowledge their trust in making this Hackathon possible.
