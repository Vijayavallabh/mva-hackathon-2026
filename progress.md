# Progress

## 2026-08-26 — session 1: repo, harness, data

Done:
- uv project created (`uv init --bare`, python 3.12), `huggingface_hub[cli]` added.
- Harness: `AGENTS.md`, `feature_list.json` (7 real features), `init.sh`, this file.
- Safety: `.gitignore` blocks `data/ results/ logs/` and every genomic extension;
  `scripts/no_data_in_git.sh` is symlinked as the git pre-commit hook and refuses
  any commit touching those paths.
- `scripts/download_data.sh` (resumable) + `scripts/verify_data.py` (compares every
  local file against the remote HF tree by size; `--self-check` proves the checker
  fails on an empty dir).
- HF access confirmed: user `jvv7`, gated approval active, LFS download works.
- 85 GB download started in background at ~64 MB/s.

Verified: `verify_data.py --self-check` → `self-check ok`;
`no_data_in_git.sh` → `no-data-in-git: ok`.

Next: feat-002, extract HPO terms from the clinical docx once the download lands.

Open question for the user: whether to run heavy realignment (feat-004) on the
local A100s or sync to PrakashDGX_H2's H100s. Data stays local by default.

## Resume

Run `./init.sh` from a clean shell. It is the only setup step; it is idempotent
and safe to re-run at any point.
