#!/usr/bin/env bash
# Public NIH LINCS inputs only. Run on the owner host under ~/v.
set -euo pipefail
cd /home/prachh/v/mva-track2-transcriptome-20260927
base=https://ftp.ncbi.nlm.nih.gov/geo/series/GSE92nnn/GSE92742/suppl
for file in GSE92742_SHA512SUMS.txt.gz GSE92742_Broad_LINCS_sig_info.txt.gz GSE92742_Broad_LINCS_sig_metrics.txt.gz GSE92742_Broad_LINCS_gene_info.txt.gz GSE92742_Broad_LINCS_cell_info.txt.gz GSE92742_Broad_LINCS_pert_info.txt.gz GSE92742_Broad_LINCS_README.pdf; do
  test ! -e "inputs/$file"
  curl --fail --location --silent --show-error --max-time 600 "$base/$file" -o "inputs/$file.partial"
  mv "inputs/$file.partial" "inputs/$file"
done
date -u +%FT%TZ > outputs/metadata-download-complete.txt
file=GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx.gz
test ! -e "inputs/$file"
curl --fail --location --silent --show-error --max-time 14400 "$base/$file" -o "inputs/$file.partial"
mv "inputs/$file.partial" "inputs/$file"
date -u +%FT%TZ > outputs/matrix-download-complete.txt
