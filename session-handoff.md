# Session handoff

**Last updated:** 2026-08-28 (session 2 — harness audit)

**Current objective / active feature:** feat-002 (phenotype to HPO terms). feat-001 is done.

**State:** 84.99 GB dataset downloaded and integrity-verified (all 11 files match
the remote HF tree by size). Harness in place, repo pushed to
`git@github-vijay:Vijayavallabh/mva-hackathon-2026` (private). No analysis has
been attempted yet.

## Blockers

None.

## Files in flight

None. Working tree is clean.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** feat-002 - read `data/Challenge_Clinical_Phenotype_1.docx` and write HPO
terms into `notes/phenotype.md`. Term IDs and labels only; keep narrative text,
dates and places out of tracked files.

**Open decision:** feat-004 (realignment + mosaic-aware calling) can run on this
box's 5x A100 80GB or sync to PrakashDGX_H2's H100s. Data stays local by default.

## Do not

Commit anything under `data/`, `results/`, `logs/`, or paste genomic or clinical
content into a third-party service. The pre-commit hook blocks the first case;
the second is on you.

**Deadlines:** submissions close 2026-10-24 23:59 UTC. All data deleted and
confirmed by email by 2026-11-24.
