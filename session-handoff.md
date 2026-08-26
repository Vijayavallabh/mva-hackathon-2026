# Session handoff

**Active feature:** feat-001 (environment and data acquisition).

**State:** harness complete, 85 GB download running in the background
(`logs/download.nohup.log`). Nothing analytical has been attempted yet.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh                              # tells you if the download finished
./scripts/download_data.sh             # re-run if incomplete; it resumes
```

**Then:** feat-002 — read `data/Challenge_Clinical_Phenotype_1.docx` and write
HPO terms into `notes/phenotype.md`. Keep narrative text out of tracked files.

## Blockers

None. Download is running; nothing is waiting on a human except the GitHub
remote (see progress.md).

## Files in flight

`scripts/download_data.sh` is writing into `data/`. No tracked file is mid-edit.

## Do not
 commit anything under `data/`, `results/`, `logs/`, or paste genomic
or clinical content into a third-party service. The pre-commit hook blocks the
first case; the second is on you.

**Deadlines:** submissions close 2026-10-24 23:59 UTC. All data deleted and
confirmed by email by 2026-11-24.
