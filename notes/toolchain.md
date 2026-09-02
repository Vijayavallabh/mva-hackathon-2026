# Toolchain and annotation resources

Installed locally on 2026-09-02 by `scripts/get_tools.sh` and
`scripts/get_resources.sh`. Large executables, archives and databases are gitignored;
their pinned versions, sources and checksums are recorded in `tools/versions.tsv` and
`tools/resources.tsv`.

## Why these resources

- **bcftools, samtools, bgzip and tabix** provide VCF/FASTA manipulation, normalization,
  indexing and aggregate QC.
- **VEP 116 with its indexed GRCh38 cache** supplies transcript consequences, gene symbols,
  SIFT/PolyPhen predictions, known-variant identifiers and population frequencies for
  offline annotation. Offline operation is important: no subject coordinate is sent to a
  web service.
- **gnomAD v4.1 frequencies** are embedded in that VEP cache. Keeping the cache copy avoids
  downloading redundant full gnomAD exome, genome and joint callsets, whose per-chromosome
  VCFs would consume hundreds of gigabytes. The cache is sufficient for the first-pass rare
  variant filter; any later population resource must also be downloaded in full rather than
  queried with subject coordinates.
- **ClinVar GRCh38** supplies clinical assertions independently of population frequency.
- **bwa-mem2, GATK and pigz** support the optional targeted re-alignment/re-call path.
- **Nextflow** provides a reproducible workflow engine when the pipeline is assembled.
- **HPO** reuses feat-002's local copy when present, and otherwise downloads the same pinned
  ontology release so a clean feat-003 installation is self-contained.
- **HPO gene-to-phenotype annotations** use the matching 2026-06-23 release. Feat-004 uses
  these public associations for genome-wide semantic similarity; family-history similarity
  is calculated separately from the seven proband observations.
- **Ensembl 116 GTF** is reduced deterministically by `scripts/build_coding_regions.py` to
  merged primary-contig exon windows with a 20 bp flank. This bounds coding/splice VEP
  runtime without sending coordinates to a remote service.

The native HTS tools were compiled locally because system-package installation is outside
this feature's scope. Optional bzip2/LZMA and remote-URL support in HTSlib are disabled; the
required local BGZF/VCF/FASTA operations are enabled. A private Temurin Java 17 runtime is
used by GATK and Nextflow, leaving the shared system Java untouched.

## Exact reference construction and validation

The VCF header names
`GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta`.
NCBI publishes the no-alt + hs38d1 analysis set and GIAB publishes the T2T v2 GRC-exclusion
BED. `scripts/build_reference.py` deterministically applies that mask and removes only a
leading `chr` from FASTA record names. This produces the header-named reference rather than
substituting an arbitrary GRCh38 FASTA.

The self-check and full local compatibility check were:

```bash
uv run python scripts/build_reference.py --self-check

ref=data/resources/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta
input=data/WGS_EX2312012_HGWCNDSX7.vcf.gz
total=$(tools/install/bin/bcftools view -H "$input" | wc -l)
matching=$(tools/install/bin/bcftools norm --check-ref x --fasta-ref "$ref" \
  --output-type u "$input" 2>/dev/null | tools/install/bin/bcftools view -H | wc -l)
printf 'vcf_records=%s reference_matching_records=%s excluded_ref_mismatch=%s\n' \
  "$total" "$matching" "$((total-matching))"
```

Result: **5,012,204 / 5,012,204 records match; zero REF mismatches.** This is an aggregate
compatibility result, not a release of any VCF record.

## Reproduce or verify

```bash
./scripts/get_tools.sh
./scripts/get_resources.sh
./scripts/get_tools.sh --check
./scripts/get_resources.sh --check
```

Both installers are idempotent and resumable. The tracked TSV files are lock manifests,
not generated observations. A download receives a `.complete` marker only after transfer
and pinned SHA-256 verification; `--check` re-hashes the local archives and resources and
checks installed versions against the locks. The large VEP cache is first extracted to a
temporary directory; only a successful extraction replaces the active cache and writes a
completion marker bound to the archive checksum.

The installed local footprint is approximately 2.2 GiB under `tools/` and 56 GiB under
`data/resources/`, against 3.7 TiB free on `/mnt/md0` at installation time. The latter
includes the 25.7 GiB VEP archive so its checksum remains independently reproducible.

Offline annotation was smoke-tested without a subject record, using the public rs699
benchmark variant:

```bash
printf '1\t230710048\t230710048\tA/G\t+\tpublic-rs699\n' | tools/install/bin/vep \
  --cache --offline --dir_cache data/resources/vep --assembly GRCh38 \
  --format ensembl --no_stats --af_gnomade --af_gnomadg --output_file STDOUT
```

The public benchmark completed successfully and returned populated `gnomADe_AF=0.458` and
`gnomADg_AF=0.5782` fields. The `--check` path requires both fields to be populated, while
cache metadata independently records `source_gnomADe v4.1` and `source_gnomADg v4.1`.

All local copies remain subject to the deletion deadline in `notes/deletion-plan.md`.
