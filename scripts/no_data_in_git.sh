#!/usr/bin/env bash
# Gate: fail if any subject-data file is tracked or staged. Also runs as pre-commit hook.
set -euo pipefail
GATE_SCRIPT=$(readlink -f "$0")
cd "$(dirname "$GATE_SCRIPT")/.."
BAD=$( { git ls-files; git diff --cached --name-only; } 2>/dev/null \
  | rg -i '(^|/)(data|results|logs)/|\.(fastq|fq|sam|bam|cram|vcf|bcf|docx)(\.gz)?($|\.)|\.(bai|crai|tbi|csi)$|(^|/)\.env($|\.)' || true )
if [ -n "$BAD" ]; then
  echo "REFUSING: prohibited paths in git (names withheld)"; exit 1
fi
if [[ -f data/Challenge_Clinical_Phenotype_1.docx && -f scripts/audit_publication.py ]]; then
  uv run python scripts/audit_publication.py --staged >/dev/null || {
    echo "REFUSING: staged disclosure audit failed; run scripts/audit_publication.py --staged locally"
    exit 1
  }
fi
echo "no-data-in-git: ok"
