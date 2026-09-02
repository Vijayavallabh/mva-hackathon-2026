#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOOLS="$ROOT/tools/install/bin"
INPUT="$ROOT/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
RESOURCES="$ROOT/data/resources"
REF="$RESOURCES/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta"
CLINVAR="$RESOURCES/clinvar/clinvar.vcf.gz"
VEP_CACHE="$RESOURCES/vep"
HPO="$RESOURCES/hp.obo"
HPO_GENES="$RESOURCES/hpo/genes_to_phenotype.txt"
EXON_WINDOWS="$RESOURCES/ensembl/Homo_sapiens.GRCh38.116.exons-plus-20bp.bed"
OUT="$ROOT/results/feat004"
PRIMARY=$(seq -s, 1 22),X,Y,M
THREADS=${MVA_TRIAGE_THREADS:-8}
export PATH="$TOOLS:$PATH"

usage() {
  echo "usage: $0 [--self-check]" >&2
}

if [[ ${1:-} == "--self-check" ]]; then
  [[ $# -eq 1 ]] || { usage; exit 2; }
  "$ROOT/scripts/get_tools.sh" --check >/dev/null
  "$ROOT/scripts/get_resources.sh" --check >/dev/null
  uv run python "$ROOT/scripts/rank_candidates.py" --self-check
  echo "VCF triage self-check ok"
  exit
fi
[[ $# -eq 0 ]] || { usage; exit 2; }
[[ "$THREADS" =~ ^[1-9][0-9]*$ ]] || {
  echo "MVA_TRIAGE_THREADS must be a positive integer" >&2
  exit 2
}

for path in \
  "$INPUT" "$INPUT.tbi" "$REF" "$CLINVAR" "$HPO" "$HPO_GENES" "$EXON_WINDOWS"; do
  [[ -s "$path" ]] || { echo "missing prerequisite: ${path#$ROOT/}" >&2; exit 1; }
done
mkdir -p "$OUT"

NORMALIZED="$OUT/pass.primary.normalized.vcf.gz"
CLINICAL="$OUT/pass.primary.normalized.clinvar.vcf.gz"
TARGETED="$OUT/pass.primary.normalized.clinvar.exon-window.vcf.gz"
ANNOTATED="$OUT/pass.primary.normalized.clinvar.vep.vcf.gz"
QC="$OUT/pipeline_qc.tsv"

locked_sha() {
  local resource=$1
  awk -F '\t' -v resource="$resource" \
    '$1 == resource {print $4; found=1} END {exit !found}' "$ROOT/tools/resources.tsv"
}

input_sha=$(sha256sum "$INPUT" | cut -d' ' -f1)
normalization_fingerprint=$(
  printf 'normalization-v1\n%s\n%s\n' "$input_sha" \
    "$(locked_sha reference-final)" |
    sha256sum | cut -d' ' -f1
)
clinvar_fingerprint=$(
  printf 'clinvar-v1\n%s\n%s\n' "$normalization_fingerprint" \
    "$(locked_sha ClinVar)" |
    sha256sum | cut -d' ' -f1
)
target_fingerprint=$(
  printf 'exon-window-v1\n%s\n%s\n' "$clinvar_fingerprint" \
    "$(locked_sha Ensembl-exon-windows)" |
    sha256sum | cut -d' ' -f1
)
vep_fingerprint=$(
  printf 'vep-coding-v1\n%s\n%s\n' "$target_fingerprint" \
    "$(locked_sha VEP-cache)" |
    sha256sum | cut -d' ' -f1
)

stage_complete() {
  local stage=$1 output=$2 expected=$3
  [[ -s "$output" && -s "$output.tbi" && -s "$OUT/.${stage}.complete" ]] &&
    [[ $(<"$OUT/.${stage}.complete") == "$expected" ]]
}

mark_complete() {
  local stage=$1 fingerprint=$2
  printf '%s\n' "$fingerprint" > "$OUT/.${stage}.complete"
}

if ! stage_complete normalized "$NORMALIZED" "$normalization_fingerprint"; then
  echo "stage 1/5: PASS, primary-contig filtering and biallelic normalization"
  tmp="$NORMALIZED.partial"
  "$TOOLS/bcftools" view --threads "$THREADS" --force-samples \
    --include 'FILTER="PASS"' --regions "$PRIMARY" --output-type u "$INPUT" |
    "$TOOLS/bcftools" norm --threads "$THREADS" --fasta-ref "$REF" \
      --multiallelics -any --keep-sum AD --output-type z --output "$tmp"
  "$TOOLS/tabix" --force --preset vcf "$tmp"
  mv "$tmp" "$NORMALIZED"
  mv "$tmp.tbi" "$NORMALIZED.tbi"
  mark_complete normalized "$normalization_fingerprint"
fi

if ! stage_complete clinvar "$CLINICAL" "$clinvar_fingerprint"; then
  echo "stage 2/5: exact-allele ClinVar annotation"
  tmp="$CLINICAL.partial"
  "$TOOLS/bcftools" annotate --threads "$THREADS" \
    --annotations "$CLINVAR" \
    --columns INFO/CLNSIG,INFO/CLNREVSTAT,INFO/CLNDN \
    --output-type z --output "$tmp" "$NORMALIZED"
  "$TOOLS/tabix" --force --preset vcf "$tmp"
  mv "$tmp" "$CLINICAL"
  mv "$tmp.tbi" "$CLINICAL.tbi"
  mark_complete clinvar "$clinvar_fingerprint"
fi

if ! stage_complete targeted "$TARGETED" "$target_fingerprint"; then
  echo "stage 3/5: exon-window prefilter for bounded VEP runtime"
  tmp="$TARGETED.partial"
  "$TOOLS/bcftools" view --threads "$THREADS" --regions-file "$EXON_WINDOWS" \
    --output-type z --output "$tmp" "$CLINICAL"
  "$TOOLS/tabix" --force --preset vcf "$tmp"
  mv "$tmp" "$TARGETED"
  mv "$tmp.tbi" "$TARGETED.tbi"
  mark_complete targeted "$target_fingerprint"
fi

if ! stage_complete vep "$ANNOTATED" "$vep_fingerprint"; then
  echo "stage 4/5: offline VEP coding/splice annotation with gnomAD frequencies"
  raw="$OUT/.vep-all.vcf.gz.partial"
  tmp="$ANNOTATED.partial"
  "$TOOLS/vep" \
    --input_file "$TARGETED" \
    --output_file "$raw" \
    --vcf --compress_output bgzip --force_overwrite --no_stats \
    --cache --offline --dir_cache "$VEP_CACHE" --assembly GRCh38 --fasta "$REF" \
    --fork "$THREADS" --buffer_size 5000 \
    --coding_only --pick \
    --pick_order mane_select,mane_plus_clinical,canonical,appris,tsl,biotype,ccds,rank \
    --symbol --canonical --mane --biotype --numbers --hgvs --protein \
    --sift b --polyphen b --check_existing --af_gnomade --af_gnomadg \
    --max_af --variant_class
  "$TOOLS/bcftools" view --threads "$THREADS" --include 'INFO/CSQ!="."' \
    --output-type z --output "$tmp" "$raw"
  "$TOOLS/tabix" --force --preset vcf "$tmp"
  mv "$tmp" "$ANNOTATED"
  mv "$tmp.tbi" "$ANNOTATED.tbi"
  case "$raw" in
    "$ROOT/results/feat004/.vep-all.vcf.gz.partial") rm -f "$raw" ;;
    *) echo "refusing unsafe temporary-file cleanup: $raw" >&2; exit 1 ;;
  esac
  mark_complete vep "$vep_fingerprint"
fi

echo "stage 5/5: phenotype-aware model ranking"
uv run python "$ROOT/scripts/rank_candidates.py" \
  --annotated-vcf "$ANNOTATED" \
  --ontology "$HPO" \
  --gene-annotations "$HPO_GENES" \
  --output "$OUT"

input_records=$($TOOLS/bcftools view --no-header "$INPUT" | wc -l)
pass_records=$($TOOLS/bcftools view --include 'FILTER="PASS"' --no-header "$INPUT" | wc -l)
primary_records=$($TOOLS/bcftools view --regions "$PRIMARY" --no-header "$INPUT" | wc -l)
normalized_records=$($TOOLS/bcftools index --nrecords "$NORMALIZED")
targeted_records=$($TOOLS/bcftools index --nrecords "$TARGETED")
annotated_records=$($TOOLS/bcftools index --nrecords "$ANNOTATED")
{
  printf 'metric\tvalue\n'
  printf 'input_records\t%s\n' "$input_records"
  printf 'pass_records\t%s\n' "$pass_records"
  printf 'nonprimary_records\t%s\n' "$((input_records-primary_records))"
  printf 'normalized_pass_primary_biallelic_records\t%s\n' "$normalized_records"
  printf 'exon_window_records\t%s\n' "$targeted_records"
  printf 'vep_coding_or_splice_records\t%s\n' "$annotated_records"
  printf 'threads\t%s\n' "$THREADS"
  printf 'vep_stage_fingerprint\t%s\n' "$vep_fingerprint"
} > "$QC"
echo "VCF triage complete; aggregate QC: $QC"
