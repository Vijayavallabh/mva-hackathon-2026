#!/usr/bin/env bash
# Public GEO study data only; all files stay below the user-authorized ~/v root.
set -euo pipefail
TASK_ROOT=/home/prachh/v/mva-track2-rnai-20260927-v23
cd "$TASK_ROOT"
base=https://ftp.ncbi.nlm.nih.gov/geo/series/GSE106nnn/GSE106127/suppl
files=(GSE106127_SHA512SUMS.txt.gz GSE106127_sig_info.txt.gz GSE106127_sig_metrics.txt.gz GSE106127_gene_info.txt.gz GSE106127_level_5_modz_n119013x978.gctx.gz GSE106127_level_5_PRIME_modz_n119013x978.gctx.gz)
for file in "${files[@]}"; do
  test ! -e "inputs/$file"
  curl --fail --location --silent --show-error --max-time 3600 "$base/$file" -o "inputs/$file.partial"
  mv "inputs/$file.partial" "inputs/$file"
done
date -u +%FT%TZ > outputs/download-complete.txt
