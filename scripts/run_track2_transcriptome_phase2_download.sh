#!/usr/bin/env bash
set -euo pipefail
cd /home/prachh/v/mva-track2-transcriptome-20260927
mkdir -p inputs/phase2
base=https://ftp.ncbi.nlm.nih.gov/geo/series/GSE70nnn/GSE70138/suppl
for file in GSE70138_SHA512SUMS.txt.gz GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz GSE70138_Broad_LINCS_sig_metrics_2017-03-06.txt.gz GSE70138_Broad_LINCS_gene_info_2017-03-06.txt.gz GSE70138_Broad_LINCS_cell_info_2017-04-28.txt.gz GSE70138_Broad_LINCS_pert_info_2017-03-06.txt.gz GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx.gz; do
  test ! -e "inputs/phase2/$file"
  curl --fail --location --silent --show-error --max-time 7200 "$base/$file" -o "inputs/phase2/$file.partial"
  mv "inputs/phase2/$file.partial" "inputs/phase2/$file"
done
date -u +%FT%TZ > outputs/phase2-download-complete.txt
