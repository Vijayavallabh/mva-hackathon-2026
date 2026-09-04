#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOOLS="$ROOT/tools/install/bin"
export PATH="$TOOLS:$PATH"
REF="$ROOT/data/resources/reference/"
REF+="GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_"
REF+="maskedGRC_exclusions_v2_no_chr.fasta"
GTF="$ROOT/data/resources/downloads/Homo_sapiens.GRCh38.116.gtf.gz"
SOURCE_VCF="$ROOT/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
SOURCE_NORMALIZED="$ROOT/results/feat004/pass.primary.normalized.vcf.gz"
CANDIDATES="$ROOT/results/feat004/all_candidate_models.tsv"
LEADING="$ROOT/results/feat004/candidate_models.tsv"
VEP_CACHE="$ROOT/data/resources/vep"
OUT="$ROOT/results/feat005b"
TMP="$OUT/tmp"
TARGETS="$OUT/targets.bed"
MANIFEST="$OUT/targets.json"
SV_TARGETS="$OUT/sv-targets.bed"
SV_MANIFEST="$OUT/sv-targets.json"
SV_BAM="$OUT/sv-targeted.pairs.bam"
PHASE_TARGET="$OUT/phase-target.bed"
BAM="$OUT/all-lanes.markdup.bam"
ALIGN_THREADS=${MVA_RECALL_ALIGN_THREADS:-32}
SORT_THREADS=${MVA_RECALL_SORT_THREADS:-8}
DECOMP_THREADS=${MVA_RECALL_DECOMP_THREADS:-4}
CALL_THREADS=${MVA_RECALL_CALL_THREADS:-8}
PADDING=${MVA_RECALL_GENE_PADDING:-20000}
SV_PADDING=${MVA_RECALL_SV_PADDING:-1000000}
REUSE_RAW_CALLS=${MVA_RECALL_REUSE_RAW_CALLS:-0}
REUSE_RAW_SV=${MVA_RECALL_REUSE_RAW_SV:-0}
for value in "$REUSE_RAW_CALLS" "$REUSE_RAW_SV"; do
  if [[ $value != 0 && $value != 1 ]]; then
    echo "MVA_RECALL_REUSE_RAW_CALLS and MVA_RECALL_REUSE_RAW_SV must be 0 or 1" >&2
    exit 2
  fi
done

self_check() {
  uv run python "$ROOT/scripts/build_recall_intervals.py" --self-check
  uv run python "$ROOT/scripts/analyze_targeted_recall.py" --self-check
  uv run python "$ROOT/scripts/build_phase_interval.py" --self-check
  "$ROOT/scripts/get_tools.sh" --check >/dev/null
  uv run whatshap --version | rg -q '^2\.8$'
  bash -n "$ROOT/scripts/run_targeted_recall.sh"
  echo "run_targeted_recall self-check ok"
}

MODE=run
if [[ ${1:-} == "--self-check" ]]; then self_check; exit; fi
if [[ ${1:-} == "--signatures" ]]; then MODE=signatures; shift; fi
if [[ $# -ne 0 ]]; then echo "usage: $0 [--self-check|--signatures]" >&2; exit 2; fi

"$ROOT/scripts/get_tools.sh" --check >/dev/null
"$ROOT/scripts/get_resources.sh" --check >/dev/null
uv run python "$ROOT/scripts/verify_data.py" >/dev/null
mkdir -p "$OUT" "$TMP" "$ROOT/logs"
case "$OUT" in "$ROOT/results/feat005b") ;; *) echo "unsafe output path" >&2; exit 1 ;; esac
case "$TMP" in "$ROOT/results/feat005b/tmp") ;; *) echo "unsafe temporary path" >&2; exit 1 ;; esac

mapfile -t R1 < <(find "$ROOT/data" -maxdepth 1 -name '*_R1_001.fastq.gz' -print | sort)
mapfile -t R2 < <(find "$ROOT/data" -maxdepth 1 -name '*_R2_001.fastq.gz' -print | sort)
if [[ ${#R1[@]} -ne 4 || ${#R2[@]} -ne 4 ]]; then
  echo "expected four paired FASTQ lanes" >&2
  exit 1
fi
for index in "${!R1[@]}"; do
  left=$(basename "${R1[$index]}" _R1_001.fastq.gz)
  right=$(basename "${R2[$index]}" _R2_001.fastq.gz)
  [[ $left == "$right" ]] || { echo "FASTQ mate mismatch: $left != $right" >&2; exit 1; }
done

fingerprint() {
  sha256sum "$@" | sha256sum | cut -d' ' -f1
}
reads_signature=$(stat --printf='%n:%s:%Y\n' "${R1[@]}" "${R2[@]}" | sha256sum | cut -d' ' -f1)
interval_signature=$(
  {
    sha256sum "$ROOT/scripts/build_recall_intervals.py" "$CANDIDATES"
    stat --printf='%n:%s:%Y\n' "$GTF"
    printf 'padding=%s\n' "$PADDING"
  } | sha256sum | cut -d' ' -f1
)

if [[ ! -s "$TARGETS" || ! -s "$MANIFEST" || ! -f "$OUT/intervals.done" || \
      $(<"$OUT/intervals.done") != "$interval_signature" ]]; then
  uv run python "$ROOT/scripts/build_recall_intervals.py" \
    "$CANDIDATES" "$GTF" "$TARGETS" "$MANIFEST" --padding "$PADDING"
  printf '%s\n' "$interval_signature" > "$OUT/intervals.done"
fi

sv_interval_signature=$(
  {
    sha256sum "$ROOT/scripts/build_recall_intervals.py" "$CANDIDATES"
    stat --printf='%n:%s:%Y\n' "$GTF"
    printf 'padding=%s\n' "$SV_PADDING"
  } | sha256sum | cut -d' ' -f1
)
if [[ ! -s "$SV_TARGETS" || ! -s "$SV_MANIFEST" || \
      ! -f "$OUT/sv-intervals.done" || \
      $(<"$OUT/sv-intervals.done") != "$sv_interval_signature" ]]; then
  uv run python "$ROOT/scripts/build_recall_intervals.py" \
    "$CANDIDATES" "$GTF" "$SV_TARGETS" "$SV_MANIFEST" --padding "$SV_PADDING"
  printf '%s\n' "$sv_interval_signature" > "$OUT/sv-intervals.done"
fi

alignment_stage() {
  "$TOOLS/bwa-mem2" mem -t "$ALIGN_THREADS" -K 100000000 \
    -R '@RG\tID:WGS\tSM:PROBAND01\tPL:ILLUMINA\tLB:WGS' "$REF" \
    <("$TOOLS/pigz" -dc -p "$DECOMP_THREADS" "${R1[@]}") \
    <("$TOOLS/pigz" -dc -p "$DECOMP_THREADS" "${R2[@]}") | \
    "$TOOLS/samtools" fixmate -m -@ "$SORT_THREADS" -u - - | \
    "$TOOLS/samtools" sort -@ "$SORT_THREADS" -m 4G -T "$TMP/coord" -O bam - | \
    "$TOOLS/samtools" markdup -r -@ "$SORT_THREADS" -O bam - "$BAM.partial"
  mv "$BAM.partial" "$BAM"
  "$TOOLS/samtools" index -@ "$SORT_THREADS" "$BAM"
  "$TOOLS/samtools" quickcheck -v "$BAM"
  "$TOOLS/samtools" flagstat -@ "$SORT_THREADS" "$BAM" > "$OUT/alignment.flagstat.txt"
  "$TOOLS/samtools" stats -@ "$SORT_THREADS" "$BAM" > "$OUT/alignment.stats.txt"
}
alignment_signature=$(
  {
    declare -f alignment_stage
    printf '%s\n' "$reads_signature"
    stat --printf='%n:%s:%Y\n' "$REF"
    awk -F '\t' '$1 == "samtools+htslib" || $1 == "bwa-mem2" || $1 == "pigz"' \
      "$ROOT/tools/versions.tsv"
    printf '%s:%s:%s\n' "$ALIGN_THREADS" "$SORT_THREADS" "$DECOMP_THREADS"
  } | sha256sum | cut -d' ' -f1
)
if [[ $MODE == signatures ]]; then
  printf 'interval_expected=%s\ninterval_recorded=%s\n' \
    "$interval_signature" "$(<"$OUT/intervals.done")"
  printf 'alignment_expected=%s\nalignment_recorded=%s\n' \
    "$alignment_signature" "$(<"$OUT/alignment.done")"
  exit
fi
if [[ ! -s "$BAM" || ! -s "$BAM.bai" || ! -f "$OUT/alignment.done" || \
      $(<"$OUT/alignment.done") != "$alignment_signature" ]]; then
  rm -f "$BAM" "$BAM.bai" "$BAM.partial" "$OUT/alignment.done"
  /usr/bin/rm -rf "$TMP"
  mkdir -p "$TMP"
  alignment_stage
  printf '%s\n' "$alignment_signature" > "$OUT/alignment.done"
  /usr/bin/rm -rf "$TMP"
fi

annotate_vep() {
  local input=$1 output=$2
  if [[ $("$TOOLS/bcftools" view -H "$input" | wc -l) -eq 0 ]]; then
    "$TOOLS/bcftools" view -Oz -o "$output" "$input"
    "$TOOLS/tabix" --force --preset vcf "$output"
    return
  fi
  "$TOOLS/vep" --input_file "$input" --output_file "$output" \
    --vcf --compress_output bgzip --force_overwrite --no_stats \
    --cache --offline --dir_cache "$VEP_CACHE" --assembly GRCh38 --fasta "$REF" \
    --fork "$CALL_THREADS" --buffer_size 5000 --pick \
    --pick_order mane_select,mane_plus_clinical,canonical,appris,tsl,biotype,ccds,rank \
    --symbol --canonical --mane --biotype --numbers --hgvs --protein \
    --sift b --polyphen b --check_existing --af_gnomade --af_gnomadg \
    --max_af --variant_class
  "$TOOLS/tabix" --force --preset vcf "$output"
}

small_call_stage() {
  if [[ $REUSE_RAW_CALLS == 0 || ! -s "$OUT/haplotypecaller.raw.vcf.gz" ]]; then
    "$TOOLS/gatk" --java-options '-Xmx64g' HaplotypeCaller \
      -R "$REF" -I "$BAM" -L "$TARGETS" --native-pair-hmm-threads "$CALL_THREADS" \
      -O "$OUT/haplotypecaller.raw.vcf.gz"
  fi
  "$TOOLS/bcftools" norm -f "$REF" -m -any "$OUT/haplotypecaller.raw.vcf.gz" -Ou | \
    "$TOOLS/bcftools" view -f '.,PASS' -Oz \
      -o "$OUT/haplotypecaller.pass.normalized.vcf.gz"
  "$TOOLS/tabix" --force --preset vcf "$OUT/haplotypecaller.pass.normalized.vcf.gz"

  if [[ $REUSE_RAW_CALLS == 0 || ! -s "$OUT/mutect2.filtered.vcf.gz" ]]; then
    "$TOOLS/gatk" --java-options '-Xmx64g' Mutect2 \
      -R "$REF" -I "$BAM" -L "$TARGETS" --native-pair-hmm-threads "$CALL_THREADS" \
      --f1r2-tar-gz "$OUT/mutect2.f1r2.tar.gz" -O "$OUT/mutect2.raw.vcf.gz"
    "$TOOLS/gatk" LearnReadOrientationModel -I "$OUT/mutect2.f1r2.tar.gz" \
      -O "$OUT/mutect2.orientation-priors.tar.gz"
    "$TOOLS/gatk" --java-options '-Xmx32g' FilterMutectCalls \
      -R "$REF" -V "$OUT/mutect2.raw.vcf.gz" \
      --ob-priors "$OUT/mutect2.orientation-priors.tar.gz" \
      -O "$OUT/mutect2.filtered.vcf.gz"
  fi
  "$TOOLS/bcftools" view -f PASS "$OUT/mutect2.filtered.vcf.gz" -Ou | \
    "$TOOLS/bcftools" norm -f "$REF" -m -any -Oz -o "$OUT/mutect2.pass.normalized.vcf.gz"
  "$TOOLS/tabix" --force --preset vcf "$OUT/mutect2.pass.normalized.vcf.gz"

  "$TOOLS/bcftools" isec -C -w1 -Oz -o "$OUT/haplotypecaller.novel.vcf.gz" \
    "$OUT/haplotypecaller.pass.normalized.vcf.gz" "$SOURCE_NORMALIZED"
  "$TOOLS/tabix" --force --preset vcf "$OUT/haplotypecaller.novel.vcf.gz"
  "$TOOLS/bcftools" isec -C -w1 -Oz -o "$OUT/mutect2.novel.vcf.gz" \
    "$OUT/mutect2.pass.normalized.vcf.gz" "$SOURCE_NORMALIZED"
  "$TOOLS/tabix" --force --preset vcf "$OUT/mutect2.novel.vcf.gz"
  annotate_vep "$OUT/haplotypecaller.novel.vcf.gz" "$OUT/haplotypecaller.novel.vep.vcf.gz"
  annotate_vep "$OUT/mutect2.novel.vcf.gz" "$OUT/mutect2.novel.vep.vcf.gz"
}
small_signature=$(
  {
    declare -f small_call_stage annotate_vep
    sha256sum "$TARGETS"
    stat --printf='%n:%s:%Y\n' "$BAM" "$SOURCE_NORMALIZED"
    awk -F '\t' '$1 == "GATK" || $1 == "bcftools" || $1 == "Ensembl-VEP"' \
      "$ROOT/tools/versions.tsv"
    printf 'call_threads=%s\n' "$CALL_THREADS"
  } | sha256sum | cut -d' ' -f1
)
if [[ ! -s "$OUT/haplotypecaller.novel.vep.vcf.gz" || \
      ! -s "$OUT/mutect2.novel.vep.vcf.gz" || ! -f "$OUT/small-calls.done" || \
      $(<"$OUT/small-calls.done") != "$small_signature" ]]; then
  small_call_stage
  printf '%s\n' "$small_signature" > "$OUT/small-calls.done"
fi

structural_stage() {
  if [[ $REUSE_RAW_SV == 0 || ! -s "$OUT/delly.raw.bcf" ]]; then
    "$TOOLS/samtools" view -@ "$SORT_THREADS" --fetch-pairs -L "$SV_TARGETS" \
      -b -o "$SV_BAM.partial" "$BAM"
    mv "$SV_BAM.partial" "$SV_BAM"
    "$TOOLS/samtools" index -@ "$SORT_THREADS" "$SV_BAM"
    "$TOOLS/samtools" quickcheck -v "$SV_BAM"
    "$TOOLS/delly" call -g "$REF" -h "$CALL_THREADS" \
      -o "$OUT/delly.raw.bcf" "$SV_BAM"
  fi
  # DELLY's germline filter assumes a cohort. For this single subject, retain
  # discovery-PASS sites at DELLY's default site-quality threshold instead.
  "$TOOLS/bcftools" view -f PASS -i 'QUAL>=300' -Ob \
    -o "$OUT/delly.pass.bcf" "$OUT/delly.raw.bcf"
  "$TOOLS/bcftools" index --force "$OUT/delly.pass.bcf"
}
structural_signature=$(
  {
    declare -f structural_stage
    stat --printf='%n:%s:%Y\n' "$BAM" "$REF" "$SV_TARGETS"
    awk -F '\t' '$1 == "DELLY" || $1 == "samtools+htslib"' \
      "$ROOT/tools/versions.tsv"
    printf 'threads=%s\n' "$CALL_THREADS"
  } | sha256sum | cut -d' ' -f1
)
if [[ ! -s "$OUT/delly.pass.bcf" || ! -f "$OUT/structural.done" || \
      $(<"$OUT/structural.done") != "$structural_signature" ]]; then
  structural_stage
  printf '%s\n' "$structural_signature" > "$OUT/structural.done"
fi

phase_stage() {
  uv run python "$ROOT/scripts/build_phase_interval.py" \
    "$MANIFEST" "$PHASE_TARGET" --gene BUB1B
  "$TOOLS/bcftools" view -R "$PHASE_TARGET" "$SOURCE_VCF" \
    -Oz -o "$OUT/target-source.vcf.gz"
  "$TOOLS/tabix" --force --preset vcf "$OUT/target-source.vcf.gz"
  printf 'PROBAND01\n' > "$OUT/sample-name.txt"
  "$TOOLS/bcftools" reheader -s "$OUT/sample-name.txt" \
    -o "$OUT/target-source.proband.vcf.gz" "$OUT/target-source.vcf.gz"
  "$TOOLS/tabix" --force --preset vcf "$OUT/target-source.proband.vcf.gz"
  uv run whatshap phase --sample PROBAND01 --reference "$REF" \
    -o "$OUT/target-source.phased.vcf.gz" "$OUT/target-source.proband.vcf.gz" "$BAM"
  "$TOOLS/tabix" --force --preset vcf "$OUT/target-source.phased.vcf.gz"
}
phase_signature=$(
  {
    declare -f phase_stage
    sha256sum "$ROOT/scripts/build_phase_interval.py"
    stat --printf='%n:%s:%Y\n' "$BAM" "$SOURCE_VCF" "$MANIFEST"
    uv run whatshap --version
  } | sha256sum | cut -d' ' -f1
)
if [[ ! -s "$OUT/target-source.phased.vcf.gz" || ! -f "$OUT/phase.done" || \
      $(<"$OUT/phase.done") != "$phase_signature" ]]; then
  phase_stage
  printf '%s\n' "$phase_signature" > "$OUT/phase.done"
fi

uv run python "$ROOT/scripts/analyze_targeted_recall.py" \
  --hc-vep "$OUT/haplotypecaller.novel.vep.vcf.gz" \
  --mutect-vep "$OUT/mutect2.novel.vep.vcf.gz" \
  --delly "$OUT/delly.pass.bcf" --manifest "$MANIFEST" \
  --phased "$OUT/target-source.phased.vcf.gz" --candidates "$LEADING" \
  --novel-candidates "$OUT/novel-candidates.tsv" --target-svs "$OUT/target-svs.tsv" \
  --summary "$OUT/summary.json"

echo "targeted recall complete: $OUT/summary.json"
