#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOOLS="$ROOT/tools/install/bin"
REF="$ROOT/data/resources/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta"
MAP="$ROOT/data/resources/mappability/k100.umap.MultiReadMappability.bedgraph.gz"
VCF="$ROOT/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
OUT="$ROOT/results/feat005a"
TMP="$OUT/tmp"
BIN_SIZE=100000
ALIGN_THREADS=${MVA_ALIGN_THREADS:-24}
SORT_THREADS=${MVA_SORT_THREADS:-6}
DECOMP_THREADS=${MVA_DECOMP_THREADS:-2}

self_check() {
  uv run python "$ROOT/scripts/build_copy_number_bins.py" --self-check
  uv run python "$ROOT/scripts/count_alignment_depth.py" --self-check
  uv run python "$ROOT/scripts/analyze_copy_number.py" --self-check
  bash -n "$ROOT/scripts/run_copy_number_screen.sh"
  echo "run_copy_number_screen self-check ok"
}

MODE=run
if [[ ${1:-} == "--self-check" ]]; then self_check; exit; fi
if [[ ${1:-} == "--signatures" ]]; then MODE=signatures; shift; fi
if [[ $# -ne 0 ]]; then echo "usage: $0 [--self-check|--signatures]" >&2; exit 2; fi

"$ROOT/scripts/get_tools.sh" --check >/dev/null
"$ROOT/scripts/get_resources.sh" --check >/dev/null
uv run python "$ROOT/scripts/verify_data.py" >/dev/null
mkdir -p "$OUT" "$TMP" "$ROOT/logs"
case "$TMP" in
  "$ROOT/results/feat005a/tmp") ;;
  *) echo "refusing unsafe temporary path: $TMP" >&2; exit 1 ;;
esac

mapfile -t R1 < <(find "$ROOT/data" -maxdepth 1 -name '*_R1_001.fastq.gz' -print | sort)
mapfile -t R2 < <(find "$ROOT/data" -maxdepth 1 -name '*_R2_001.fastq.gz' -print | sort)
if [[ ${#R1[@]} -ne 4 || ${#R2[@]} -ne 4 ]]; then
  echo "expected four paired FASTQ lanes" >&2
  exit 1
fi
for index in "${!R1[@]}"; do
  r1_key=$(basename "${R1[$index]}" _R1_001.fastq.gz)
  r2_key=$(basename "${R2[$index]}" _R2_001.fastq.gz)
  if [[ $r1_key != "$r2_key" ]]; then
    echo "FASTQ mate mismatch: $r1_key != $r2_key" >&2
    exit 1
  fi
done

vcf_signature=$(stat --printf='%n:%s:%Y\n' "$VCF" | sha256sum | cut -d' ' -f1)
reads_signature=$(stat --printf='%n:%s:%Y\n' "${R1[@]}" "${R2[@]}" | sha256sum | cut -d' ' -f1)
bins_signature=$(
  {
    sha256sum "$ROOT/scripts/build_copy_number_bins.py"
    awk -F '\t' '$1 == "reference-final" || $1 == "Umap-k100-multiread"' "$ROOT/tools/resources.tsv"
    stat --printf='%n:%s:%Y\n' "$REF" "$MAP"
    printf 'bin_size=%s\n' "$BIN_SIZE"
  } | sha256sum | cut -d' ' -f1
)

baf_stage() {
  {
    printf 'chrom\tpos\tdp\tref_count\talt_count\n'
    "$TOOLS/bcftools" view --threads 2 -f PASS -m2 -M2 -v snps \
      -i 'GT="het" && FORMAT/DP>=20 && FORMAT/DP<=90 && FORMAT/GQ>=30 && FORMAT/AD[0:0]>=5 && FORMAT/AD[0:1]>=5' \
      "$VCF" -Ou | "$TOOLS/bcftools" query -f '%CHROM\t%POS[\t%DP\t%AD]\n' | \
      awk -F '\t' 'BEGIN{OFS="\t"} {split($4,a,","); print $1,$2,$3,a[1],a[2]}'
  } > "$OUT/baf.tsv"
}
baf_signature=$(
  {
    declare -f baf_stage
    awk -F '\t' '$1 == "bcftools"' "$ROOT/tools/versions.tsv"
    printf '%s\n' "$vcf_signature"
  } | sha256sum | cut -d' ' -f1
)

alignment_stage() {
  # BWA emits GO:query with each pair grouped, satisfying fixmate without a name sort.
  "$TOOLS/bwa-mem2" mem -t "$ALIGN_THREADS" -K 100000000 \
    -R '@RG\tID:WGS\tSM:PROBAND01\tPL:ILLUMINA\tLB:WGS' "$REF" \
    <("$TOOLS/pigz" -dc -p "$DECOMP_THREADS" "${R1[@]}") \
    <("$TOOLS/pigz" -dc -p "$DECOMP_THREADS" "${R2[@]}") | \
    "$TOOLS/samtools" fixmate -m -@ "$SORT_THREADS" -u - - | \
    "$TOOLS/samtools" sort -@ "$SORT_THREADS" -m 2G -T "$TMP/coord" -O bam - | \
    "$TOOLS/samtools" markdup -r -@ "$SORT_THREADS" -u - - | \
    "$TOOLS/samtools" view -h - | \
    uv run python "$ROOT/scripts/count_alignment_depth.py" "$OUT/bins.tsv" \
      "$OUT/depth-counts.tsv" "$OUT/alignment-stats.json" --minimum-mapq 30
}
alignment_signature=$(
  {
    declare -f alignment_stage
    sha256sum "$ROOT/scripts/count_alignment_depth.py"
    awk -F '\t' '$1 == "samtools+htslib" || $1 == "bwa-mem2" || $1 == "pigz"' \
      "$ROOT/tools/versions.tsv"
    printf '%s:%s:%s:%s:%s\n' \
      "$reads_signature" "$bins_signature" "$ALIGN_THREADS" "$SORT_THREADS" "$DECOMP_THREADS"
  } | sha256sum | cut -d' ' -f1
)
if [[ $MODE == signatures ]]; then
  printf 'bins=%s\nbaf=%s\nalignment=%s\n' \
    "$bins_signature" "$baf_signature" "$alignment_signature"
  exit
fi

if [[ ! -s "$OUT/bins.tsv" || ! -f "$OUT/bins.done" || $(<"$OUT/bins.done") != "$bins_signature" ]]; then
  rm -f "$OUT/bins.tsv" "$OUT/bins.done"
  uv run python "$ROOT/scripts/build_copy_number_bins.py" "$REF" "$MAP" "$OUT/bins.tsv" \
    --bin-size "$BIN_SIZE"
  printf '%s\n' "$bins_signature" > "$OUT/bins.done"
fi

if [[ ! -s "$OUT/baf.tsv" || ! -f "$OUT/baf.done" || $(<"$OUT/baf.done") != "$baf_signature" ]]; then
  rm -f "$OUT/baf.tsv" "$OUT/baf.done"
  baf_stage
  printf '%s\n' "$baf_signature" > "$OUT/baf.done"
fi

index_files=("$REF.0123" "$REF.amb" "$REF.ann" "$REF.bwt.2bit.64" "$REF.pac")
index_missing=0
for path in "${index_files[@]}"; do [[ -s "$path" ]] || index_missing=1; done
if (( index_missing )); then
  "$TOOLS/bwa-mem2" index "$REF"
fi

if [[ ! -s "$OUT/depth-counts.tsv" || ! -s "$OUT/alignment-stats.json" || \
      ! -f "$OUT/alignment.done" || $(<"$OUT/alignment.done") != "$alignment_signature" ]]; then
  rm -f "$OUT/depth-counts.tsv" "$OUT/alignment-stats.json" "$OUT/alignment.done"
  rm -rf "$TMP"
  mkdir -p "$TMP"
  alignment_stage
  printf '%s\n' "$alignment_signature" > "$OUT/alignment.done"
  rm -rf "$TMP"
fi

uv run python "$ROOT/scripts/analyze_copy_number.py" \
  "$OUT/bins.tsv" "$OUT/depth-counts.tsv" "$OUT/baf.tsv" \
  "$OUT/summary.json" "$OUT/chromosomes.tsv" --bin-size "$BIN_SIZE" \
  --minimum-mappability 0.90 --minimum-acgt 0.95
uv run python "$ROOT/scripts/analyze_copy_number.py" \
  "$OUT/bins.tsv" "$OUT/depth-counts.tsv" "$OUT/baf.tsv" \
  "$OUT/summary-map095.json" "$OUT/chromosomes-map095.tsv" --bin-size "$BIN_SIZE" \
  --minimum-mappability 0.95 --minimum-acgt 0.95

echo "copy-number screen complete: $OUT/summary.json"
