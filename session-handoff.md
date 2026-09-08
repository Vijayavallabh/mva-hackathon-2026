# Session handoff

**Last updated:** 2026-09-08 (session 29 — score uncertainty and native-phase audit)

**Current objective:** respond to the owner's request to fix score overconfidence
and pursue phase. Feat-006b adds `scripts/audit_track1_evidence.py` with score
scenarios, fixed-universe rank sensitivity and native GT/PS plus PGT/PID checks.
Tests and real audits pass; final review is pending. See
`notes/track1-evidence-audit.md` for scope, commands and measured limitations.

The actual score is unknown. BUB1B is first in 26/34 declared sensitivity settings
over 169 pairs/27 genes, but falls under combined annotation ablation; this
fraction is not confidence. Three native/recalled phase inputs supply no linkage.
Trans remains unconfirmed. V4 files are unchanged and verify successfully. The
owner was asked whether any upload already occurred; no receipt is available.

Feat-007 remains complete:
GitHub confirms PUBLIC, anonymous clean-main/current-blob controls return 200, all
13 retired blobs return 404, authenticated purge passes and the all-ref audit at
`e8b9113` passes 40 commits/289 blobs. No Support or publication blocker remains.

Feat-001 through feat-007, including feat-005c, are done. Feat-008's unchanged v4
passes live preflight with no blockers. The remaining blocker is authenticated portal
access: HF API whoami confirms jvv7, but the read-only portal quota callback using
available Bearer credentials returns an empty string, not a quota. No browser OAuth
session is available to this workflow. No upload endpoint or submission callback was
invoked. The exact browser handoff is in `notes/track1-submission.md` (session 28).
Do not infer owner-side submission status or quota without a receipt/history check.
See `notes/publication-audit.md` and `notes/track1-submission.md`.

The phase follow-up remains scientifically unchanged: both alleles are unphased.
`notes/phase-connectivity.md` records the evidence; completion does not confirm trans.

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
all four lane pairs and re-called 185 survivor genes plus two explicit controls. Supported
coding/splice, operational deep-intronic, repeat-adjacent, same-gene reconstruction and
heterozygous-SV screens found no extra BUB1B candidate; read-backed phasing left both
leading alleles unphased. See `notes/targeted-recall.md`.

**Read these before touching anything:** `notes/data-profile.md` (measured baseline, with
the command for every number) and `notes/challenge-spec.md` (scoring mechanics and the two
traps that silently score zero).

## Blockers

- **Scientific uncertainty is not fixed by relabelling outputs.** The official
  score requires a receipt. Native phase tags and existing read-connectivity
  evidence do not establish trans or cis. New authorized phase-informative data
  offers a different route; no family contact or raw-data transfer is permitted.
  Do not claim all possible existing-data analysis is exhausted.
- **Purge is resolved, not a blocker.** The owner supplied Support's reply dated
  2026-09-08 10:41 UTC. Ticket correspondence was not independently fetched, but
  removal is independently verified by authenticated API checks with controls.
  Preserve `notes/publication-removed-objects.json` and the live guard.
- **Public-first policy is satisfied.** GitHub is PUBLIC; anonymous clean-branch and
  retired-object checks pass with controls. Feat-007 is done. Continue the live
  preflight guard before uploads, but do not recreate this as an unresolved gate.
- **AI disclosure is no longer a blocker.** The owner confirmed OpenAI/Codex API tier,
  and on 2026-09-08 confirmed no model training and no other AI providers. The config
  records owner attestations, not an independent account audit or zero-retention claim.
- **Portal browser authentication, quota and receipt remain outstanding.** Local API
  credentials identify jvv7 but did not produce portal quota. The read-only quota
  callback returned HTTP 200 / complete / `[""]`; it did not consume an attempt.
  Use the owner's signed-in official browser to check quota and upload the two exact
  v4 files once. Never fabricate OAuth profiles, use identity overrides, or request
  passwords/cookies/tokens. Share the receipt, not credentials.
- **The box is shared and contended.** 2026-08-28: load average 109 on 64 cores, GPUs 0/1/2
  at 100% with other users' jobs, only GPU 4 free. 3.3 TB free on `/mnt/md0` (92% full).
  Check `uptime` and `nvidia-smi` before planning anything large.

## Files in flight

Feat-005c is finished. Its ignored `results/feat005c/` directory contains initial and
final aggregate connectivity reports plus the recalled-locus input and phased VCFs.
The final evidence files are `source-connectivity-final.json` and
`union-connectivity-final.json`; the latter checks both original and recalled phase
outputs. All subject-level files stay local. The log is `logs/feat005c-hc-phase.log`.
The new analysis does not change the CSV, report, ranking or the trans-unconfirmed caveat.

Feat-005b's subject BAM/VCF/BCF and review tables remain gitignored under
`results/feat005b/`; only code and aggregate interpretation are tracked. The local toolchain and public
annotation resources are intentionally gitignored; their versions, sources and checksums
are tracked in `tools/versions.tsv` and `tools/resources.tsv`.
The fetched `data/resources/hp.obo` is reused rather than duplicated.
The protected Presentation/Notes wording was not copied; only reviewed categorical context
is tracked.
Feat-007 recovery bundles, mirrors and maps are under ignored `results/feat007/`; some
contain obsolete history. Never push or share those refs. Include them and local unreachable
Git objects/reflogs in the deletion plan.
Feat-008's current package is `results/feat008/jvv7_genomewide_mva_v4/`, built from
`13f06ad` with complete owner disclosure. Offline verification and regressions pass;
the session-28 PUBLIC live preflight exits 0 with no blockers. Purge, live origin,
reachable-history audit and pinned official contract pass. This is not portal login.
V1/v2/v3 must not be reused; never edit
old deliverables in place. No upload, official score or receipt is recorded by this workflow.
Hashes and verification outcomes are in `notes/track1-submission.md`.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** follow the signed-in browser handoff in the submission
notes: account jvv7, verify quota/history, upload unchanged v4 CSV and report with
the public GitHub URL, submit once and preserve the receipt. If the owner already
submitted outside this workflow, obtain that receipt instead of a duplicate upload.
No automated uploader was added. Local HF API authentication did not establish portal
identity; do not retry unchanged quota calls or rebuild packages as a substitute.
Do not create v5 unless configuration, code or evidence changes; v4 already includes the
completed disclosure. V4 has been rechecked after the purge was resolved.
The owner's request to ignore the purge gate was not implemented. The owner subsequently
submitted the Support ticket and restored private visibility; no agent sent a message or
changed visibility. No continuous monitoring has been scheduled.

The feat-004 candidate is not confirmed: both alleles are unphased, and the second BUB1B
missense allele has computational prediction support but no ClinVar assertion in the pinned
release. Feat-005a does not phase small variants. Preserve the exact distinction between
candidate, phase, and classification: **trans phase remains unconfirmed**.

**Persistent repository workflow:** commit every intended change, however small. At the
end of each session, push all new commits to the configured `origin` and verify that the
branch matches upstream. Parent-directory filesystem access does not permit placing gated
raw subject data or clinical narrative in hosted model context.

**Open decisions:**
- One supported heterozygous DELLY event overlaps the padded TRIP13 window but is not orthogonally
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
