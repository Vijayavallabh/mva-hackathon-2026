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

## 2026-08-26 - session 1 continued: download complete

- 84.99 GB / 11 files landed; `./init.sh` reports
  `COMPLETE: all files present at expected size`. feat-001 done.
- Repo pushed private to `Vijayavallabh/mva-hackathon-2026`, local git identity
  set to `Vijayavallabh <be23b041@smail.iitm.ac.in>` (the global config on this
  box belongs to a different user, so this had to be set per-repo).
- Instruction file is `AGENTS.md`; `CLAUDE.md` is a gitignored local symlink.
- Dropped the `hf_transfer` extra - deprecated upstream, replaced by
  `HF_XET_HIGH_PERFORMANCE=1` in `scripts/download_data.sh`.
- Disk after download: 3.3 TB free on /mnt/md0.

Next: feat-002, HPO terms from the clinical docx.

## Resume

Run `./init.sh` from a clean shell. It is the only setup step; it is idempotent
and safe to re-run at any point.

## 2026-08-28 — session 2: harness audit, verification gate closed

Audited the harness (harness-creator validator: 96/100). The validator named
`lifecycle` as the bottleneck; that was a keyword check. The real defect was in
verification and it was live:

- `init.sh` step 4 ran `verify_data.py || echo "..."`, so a failed integrity
  check printed its error and the script still exited 0 with `=== OK ===`.
  The definition of done says "`./init.sh` passes" — for the one check that
  guards 85 GB of subject data, it could not fail. Fixed: step 4 now exits 1.
  Proved with a stubbed failure (`false` in place of the verify call) -> exit 1.
- That hole was masking a real `INCOMPLETE`: `TRUNCATED README.md 5062/5076`.
  Cause: the dataset's own README instructs `--exclude "README.md"
  ".gitattributes"`, `download_data.sh` never passed it, and upstream edited
  README.md after our copy landed. Both files are repo metadata, not subject
  data. Now excluded in `download_data.sh` and skipped in `verify_data.py`.
  All 11 payload files were and are intact — no re-download needed.
- `feat-001`'s evidence string claimed "COMPLETE" while the repo reported
  INCOMPLETE. Re-recorded against today's real run.
- `no_data_in_git.sh` did not cover `logs/` although `.gitignore` does. Added.
  Proved: staging `logs/download.log` now makes the gate exit 1.

Verified: `./init.sh` -> `COMPLETE: all files present at expected size`, exit 0.

Next: feat-002, HPO terms from the clinical docx. Unchanged.
