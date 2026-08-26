#!/usr/bin/env bash
# Gate: fail if any subject-data file is tracked or staged. Also runs as pre-commit hook.
set -euo pipefail
cd "$(dirname "$0")/.."
BAD=$( { git ls-files; git diff --cached --name-only; } 2>/dev/null \
  | grep -Ei '(^|/)(data|results)/|\.(fastq|fq|bam|cram|vcf|bcf|docx)(\.gz)?$' || true )
if [ -n "$BAD" ]; then
  echo "REFUSING: subject data in git:"; echo "$BAD"; exit 1
fi
echo "no-data-in-git: ok"
