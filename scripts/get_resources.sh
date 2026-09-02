#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
RESOURCES="$ROOT/data/resources"
DOWNLOADS="$RESOURCES/downloads"
REFERENCE="$RESOURCES/reference"
VEP_CACHE="$RESOURCES/vep"
CLINVAR="$RESOURCES/clinvar"
HPO_ANNOTATIONS="$RESOURCES/hpo"
ENSEMBL="$RESOURCES/ensembl"
TOOLS="$ROOT/tools/install/bin"
RESOURCE_MANIFEST="$ROOT/tools/resources.tsv"
VEP_EXTRACT_MARKER="$VEP_CACHE/.vep-116-GRCh38-extract-complete"
mkdir -p \
  "$DOWNLOADS" "$REFERENCE" "$VEP_CACHE" "$CLINVAR" "$HPO_ANNOTATIONS" "$ENSEMBL"

locked() {
  local resource=$1 column=$2
  awk -F '\t' -v resource="$resource" -v column="$column" \
    '$1 == resource { print $column; found=1 } END { exit !found }' "$RESOURCE_MANIFEST"
}

verify_sha256() {
  local resource=$1 path=$2 expected
  expected=$(locked "$resource" 4)
  printf '%s  %s\n' "$expected" "$path" | sha256sum --check --status || {
    echo "checksum mismatch: ${path#$ROOT/} ($resource)" >&2
    return 1
  }
}

download() {
  local resource=$1 url=$2 dest=$3
  local marker="$dest.complete"
  if [[ -s "$dest" ]] && verify_sha256 "$resource" "$dest"; then
    touch "$marker"
    return
  fi
  if [[ -f "$marker" ]]; then
    echo "discarding corrupt completed download: ${dest#$ROOT/}" >&2
    rm -f "$marker" "$dest"
  fi
  if [[ ! -f "$marker" ]]; then
    curl --fail --location --retry 8 --continue-at - --output "$dest" "$url"
    if ! verify_sha256 "$resource" "$dest"; then
      rm -f "$dest"
      return 1
    fi
    touch "$marker"
  fi
}

check_resources() {
  local failed=0 path vep_output
  for path in \
    "$REFERENCE/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta" \
    "$REFERENCE/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta.fai" \
    "$VEP_CACHE/homo_sapiens/116_GRCh38/info.txt" \
    "$VEP_EXTRACT_MARKER" \
    "$CLINVAR/clinvar.vcf.gz" \
    "$CLINVAR/clinvar.vcf.gz.tbi" \
    "$RESOURCES/hp.obo" \
    "$HPO_ANNOTATIONS/genes_to_phenotype.txt" \
    "$ENSEMBL/Homo_sapiens.GRCh38.116.exons-plus-20bp.bed" \
    "$RESOURCE_MANIFEST"; do
    if [[ ! -s "$path" ]]; then echo "missing: ${path#$ROOT/}" >&2; failed=1; fi
  done
  (( failed == 0 )) || return 1
  verify_sha256 reference-base "$DOWNLOADS/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna.gz"
  verify_sha256 reference-mask "$DOWNLOADS/GCA_000001405.15_GRCh38_GRC_exclusions_T2Tv2.bed"
  verify_sha256 reference-final "$REFERENCE/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta"
  verify_sha256 VEP-cache "$DOWNLOADS/homo_sapiens_vep_116_GRCh38.tar.gz"
  verify_sha256 ClinVar "$CLINVAR/clinvar.vcf.gz"
  verify_sha256 HPO "$RESOURCES/hp.obo"
  verify_sha256 HPO-gene-annotations "$HPO_ANNOTATIONS/genes_to_phenotype.txt"
  verify_sha256 Ensembl-GTF "$DOWNLOADS/Homo_sapiens.GRCh38.116.gtf.gz"
  verify_sha256 Ensembl-exon-windows \
    "$ENSEMBL/Homo_sapiens.GRCh38.116.exons-plus-20bp.bed"
  [[ $(<"$VEP_EXTRACT_MARKER") == "$(locked VEP-cache 4)" ]]
  "$TOOLS/samtools" faidx "$REFERENCE/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta" 1:1-1 >/dev/null
  "$TOOLS/tabix" -l "$CLINVAR/clinvar.vcf.gz" >/dev/null
  rg -q '^source_gnomADe\tv4\.1$' "$VEP_CACHE/homo_sapiens/116_GRCh38/info.txt"
  rg -q '^source_gnomADg\tv4\.1$' "$VEP_CACHE/homo_sapiens/116_GRCh38/info.txt"
  vep_output=$(printf '1\t230710048\t230710048\tA/G\t+\tpublic-rs699\n' | \
    "$TOOLS/vep" --cache --offline --dir_cache "$VEP_CACHE" --assembly GRCh38 \
      --format ensembl --no_stats --af_gnomade --af_gnomadg --output_file STDOUT 2>/dev/null)
  rg -q 'gnomADe_AF=[0-9]' <<<"$vep_output"
  rg -q 'gnomADg_AF=[0-9]' <<<"$vep_output"
  echo "annotation resources ready"
}

if [[ ${1:-} == "--check" ]]; then check_resources; exit; fi
if [[ $# -ne 0 ]]; then echo "usage: $0 [--check]" >&2; exit 2; fi
"$ROOT/scripts/get_tools.sh" --check >/dev/null

BASE_REF="$DOWNLOADS/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna.gz"
EXCLUSIONS="$DOWNLOADS/GCA_000001405.15_GRCh38_GRC_exclusions_T2Tv2.bed"
REF_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna.gz"
BED_URL="https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/references/GRCh38/GCA_000001405.15_GRCh38_GRC_exclusions_T2Tv2.bed"
download reference-base "$REF_URL" "$BASE_REF"
download reference-mask "$BED_URL" "$EXCLUSIONS"
FINAL_REF="$REFERENCE/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta"
if [[ ! -s "$FINAL_REF" ]] || ! verify_sha256 reference-final "$FINAL_REF"; then
  rm -f "$FINAL_REF" "$FINAL_REF.fai" "${FINAL_REF%.*}.dict"
  uv run python "$ROOT/scripts/build_reference.py" "$BASE_REF" "$EXCLUSIONS" "$FINAL_REF"
  verify_sha256 reference-final "$FINAL_REF"
fi
[[ -s "$FINAL_REF.fai" ]] || "$TOOLS/samtools" faidx "$FINAL_REF"
[[ -s "${FINAL_REF%.*}.dict" ]] || "$TOOLS/gatk" CreateSequenceDictionary -R "$FINAL_REF" >/dev/null

VEP_ARCHIVE="$DOWNLOADS/homo_sapiens_vep_116_GRCh38.tar.gz"
VEP_URL="https://ftp.ensembl.org/pub/release-116/variation/indexed_vep_cache/homo_sapiens_vep_116_GRCh38.tar.gz"
if [[ -s "$VEP_ARCHIVE" ]] && verify_sha256 VEP-cache "$VEP_ARCHIVE"; then
  touch "$VEP_ARCHIVE.complete"
else
  rm -f "$VEP_ARCHIVE.complete"
  uv run python "$ROOT/scripts/parallel_download.py" "$VEP_URL" "$VEP_ARCHIVE" \
    --workers "${MVA_DOWNLOAD_WORKERS:-12}"
  if ! verify_sha256 VEP-cache "$VEP_ARCHIVE"; then
    rm -f "$VEP_ARCHIVE"
    exit 1
  fi
  touch "$VEP_ARCHIVE.complete"
fi
if [[ ! -s "$VEP_EXTRACT_MARKER" ]] || \
   [[ $(<"$VEP_EXTRACT_MARKER") != "$(locked VEP-cache 4)" ]]; then
  VEP_EXTRACT_TMP="$VEP_CACHE/.extracting-116-GRCh38"
  case "$VEP_EXTRACT_TMP" in
    "$ROOT/data/resources/vep/.extracting-116-GRCh38") ;;
    *) echo "refusing unsafe extraction path: $VEP_EXTRACT_TMP" >&2; exit 1 ;;
  esac
  rm -rf "$VEP_EXTRACT_TMP"
  mkdir -p "$VEP_EXTRACT_TMP"
  tar -xzf "$VEP_ARCHIVE" -C "$VEP_EXTRACT_TMP"
  [[ -s "$VEP_EXTRACT_TMP/homo_sapiens/116_GRCh38/info.txt" ]]
  rm -rf "$VEP_CACHE/homo_sapiens"
  mv "$VEP_EXTRACT_TMP/homo_sapiens" "$VEP_CACHE/homo_sapiens"
  rmdir "$VEP_EXTRACT_TMP"
  locked VEP-cache 4 > "$VEP_EXTRACT_MARKER"
fi

CLINVAR_RELEASE=20260822
CLINVAR_URL="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/archive_2.0/2026/clinvar_${CLINVAR_RELEASE}.vcf.gz"
download ClinVar "$CLINVAR_URL" "$CLINVAR/clinvar.vcf.gz"
[[ -s "$CLINVAR/clinvar.vcf.gz.tbi" ]] || "$TOOLS/tabix" --preset vcf "$CLINVAR/clinvar.vcf.gz"

HPO_URL="https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-23/hp.obo"
download HPO "$HPO_URL" "$RESOURCES/hp.obo"
HPO_GENE_URL="https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-23/genes_to_phenotype.txt"
download HPO-gene-annotations "$HPO_GENE_URL" "$HPO_ANNOTATIONS/genes_to_phenotype.txt"

ENSEMBL_GTF="$DOWNLOADS/Homo_sapiens.GRCh38.116.gtf.gz"
ENSEMBL_GTF_URL="https://ftp.ensembl.org/pub/release-116/gtf/homo_sapiens/Homo_sapiens.GRCh38.116.gtf.gz"
download Ensembl-GTF "$ENSEMBL_GTF_URL" "$ENSEMBL_GTF"
EXON_WINDOWS="$ENSEMBL/Homo_sapiens.GRCh38.116.exons-plus-20bp.bed"
if [[ ! -s "$EXON_WINDOWS" ]] || ! verify_sha256 Ensembl-exon-windows "$EXON_WINDOWS"; then
  rm -f "$EXON_WINDOWS"
  uv run python "$ROOT/scripts/build_coding_regions.py" \
    "$ENSEMBL_GTF" "$EXON_WINDOWS" --flank 20
  verify_sha256 Ensembl-exon-windows "$EXON_WINDOWS"
fi

check_resources
