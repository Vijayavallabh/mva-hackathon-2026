# Session handoff

**Last updated:** 2026-09-04 (session 17 — feat-005b targeted recall)

**Current objective / active feature:** feat-007 (history-safe public repository).
Feat-001 through feat-006 are done; keep exactly one feature active. Do not begin feat-007's
destructive history rewrite until the user explicitly authorizes that operation.

**State:** 84.99 GB subject dataset downloaded and integrity-verified. The data has been
profiled; its HPO IDs, labels, reviewed context and concise clinical-significance summaries
have been extracted.
Seven terms are proband phenotypes and one is parental/family history. Feat-004 completed
the first offline genome-wide coding/splice analysis and identified a BUB1B compound-het
pair as the leading unphased candidate; see `notes/vcf-triage.md`. `feature_list.json` was
rewritten in session 3 from 7 to 11 features
against what the data and the challenge's published scoring code actually say.
Feat-005a then resolved the preliminary chr20/19/22 ambiguity: chr20 returns to baseline,
chr22 lacks joint BAF support and chr19 retains a credible low-level gain signal at both
mappability thresholds. See `notes/copy-number-screen.md`. Feat-006 pinned the public
official scorer and produced a ten-row local draft that passes schema, identity, EPCR and
reference-normalization checks; see `notes/submission-conformance.md`. Feat-005b realigned
all four lane pairs and re-called all 187 survivor genes: no extra rare BUB1B allele or
high-quality BUB1B-window SV was recovered, and read-backed phasing left both leading
alleles unphased. See `notes/targeted-recall.md`.

**Read these before touching anything:** `notes/data-profile.md` (measured baseline, with
the command for every number) and `notes/challenge-spec.md` (scoring mechanics and the two
traps that silently score zero).

## Blockers

- **Do not make the repository public:** current tracked files have zero non-HPO three-word
  overlap with protected table wording, but reachable commit `05ed1cc` has two overlaps.
  Feat-007 must rewrite that content out of history and force-push the configured origin;
  this destructive history operation requires an explicit user task.
- **This repo is private, and every Track 1 submission requires a public GitHub URL.**
  Feat-007 remains blocked until the protected overlaps in reachable commit `05ed1cc` are
  removed by the explicitly authorized history rewrite described above. Re-audit the full
  rewritten history before changing repository visibility.
- **The box is shared and contended.** 2026-08-28: load average 109 on 64 cores, GPUs 0/1/2
  at 100% with other users' jobs, only GPU 4 free. 3.3 TB free on `/mnt/md0` (92% full).
  Check `uptime` and `nvidia-smi` before planning anything large.

## Files in flight

Feat-005b's subject BAM/VCF/BCF and review tables remain gitignored under
`results/feat005b/`; only code and aggregate interpretation are tracked. The local toolchain and public
annotation resources are intentionally gitignored; their versions, sources and checksums
are tracked in `tools/versions.tsv` and `tools/resources.tsv`.
The fetched `data/resources/hp.obo` is reused rather than duplicated.
The protected Presentation/Notes wording was not copied; only reviewed categorical context
is tracked.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** feat-007 — after explicit authorization, rewrite reachable
history to remove the two protected-text overlaps in commit `05ed1cc`, force-push the
configured origin, repeat the full-history disclosure audit, and only then make the
repository public. Do not change visibility before every audit passes.

The feat-004 candidate is not confirmed: both alleles are unphased, and the second BUB1B
missense allele has computational prediction support but no ClinVar assertion in the pinned
release. Feat-005a does not phase small variants. Preserve the exact distinction between
candidate, phase, and classification: **trans phase remains unconfirmed**.

**Persistent repository workflow:** commit every intended change, however small. At the
end of each session, push all new commits to the configured `origin` and verify that the
branch matches upstream. Parent-directory filesystem access does not permit placing gated
raw subject data or clinical narrative in hosted model context.

**Open decisions:**
- One high-quality DELLY event overlaps the padded TRIP13 window but is not orthogonally
  validated; keep it as a local manual-review item, not a causal claim.
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

The current draft has been hypothetically self-scored but has not been uploaded. Its local
100 / 1.0 result assumes row 1 is truth and is only a scorer plumbing test; it is not a
score against the private key.

**Deadlines:** submissions close 2026-10-24 23:59 UTC. All data deleted and
confirmed by email by 2026-11-24.
