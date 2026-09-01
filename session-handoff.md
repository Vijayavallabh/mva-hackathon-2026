# Session handoff

**Last updated:** 2026-09-01 (session 5 — parent-directory authorization)

**Current objective / active feature:** feat-002 (extract the embedded HPO terms).
feat-001 is done. feat-003 (toolchain + annotation resources) remains queued until feat-002
is complete; keep exactly one feature active.

**State:** 84.99 GB dataset downloaded and integrity-verified. The data has now been
profiled — see `notes/data-profile.md` — but **no analysis has been run and no candidate
variant proposed.** `feature_list.json` was rewritten in session 3 from 7 to 11 features
against what the data and the challenge's published scoring code actually say.

**Read these before touching anything:** `notes/data-profile.md` (measured baseline, with
the command for every number) and `notes/challenge-spec.md` (scoring mechanics and the two
traps that silently score zero).

## Blockers

- **No bioinformatics tooling is installed** — no bcftools, samtools, tabix, bwa-mem2, vep,
  gatk, nextflow, pigz. Nothing beyond coreutils, `awk`, `zcat`, `docker` and the uv env.
  feat-003 fixes this and gates feat-004 onward.
- **This repo is private, and every Track 1 submission requires a public GitHub URL.**
  feat-007. History is clean today (4 commits, 15 files, nothing under `data/`/`results/`/
  `logs/`), so this is a visibility flip plus a re-audit, not a rewrite.
- **The box is shared and contended.** 2026-08-28: load average 109 on 64 cores, GPUs 0/1/2
  at 100% with other users' jobs, only GPU 4 free. 3.3 TB free on `/mnt/md0` (92% full).
  Check `uptime` and `nvidia-smi` before planning anything large.

## Files in flight

None. Working tree is clean.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** feat-002 — write `scripts/extract_hpo.py` to pull the 8 embedded
`HP:\d{7}` IDs out of the docx's `word/document.xml` with stdlib `zipfile`, resolve labels
against `hp.obo`, and fill the table in `notes/phenotype.md`. IDs and labels only; no
narrative, no dates, no places. Fetch and record `hp.obo` as the one scoped input needed by
feat-002; leave the broader toolchain and annotation-resource setup queued as feat-003.

**Open decisions:**
- feat-005b (targeted realignment) can run on this box's A100s or sync to PrakashDGX_H2's
  H100s. Data stays local by default. Note it is now *optional and contingent* on feat-004's
  candidate list — the case for it is recovering a second compound-het allele the germline
  caller dropped, not aneuploidy detection.
- L003 R1's index ends `…GGAGA` where L001/L002/L004 end `…GGAGC`. Confirm whether that is a
  first-read artefact or a systematic difference before treating the four lanes as one library.

## Do not

Commit anything under `data/`, `results/`, `logs/`, or send raw subject data — FASTQ, BAM,
VCF records, the clinical narrative — to any external service, third-party model APIs
included. The pre-commit hook blocks the first case; the second is on you. Derived outputs
(aggregate statistics, HPO IDs and labels, gene names, submitted candidates) are explicitly
permitted and are what this repo tracks — see `AGENTS.md` rule 1.

Do not spend a Track 1 submission on a CSV that has not been self-scored locally (feat-006).
There are only six.

**Deadlines:** submissions close 2026-10-24 23:59 UTC. All data deleted and
confirmed by email by 2026-11-24.
