# Session handoff

**Last updated:** 2026-09-08 (session 27 — Support purge independently verified)

**Current objective:** verify the owner-supplied Support removal reply for ticket
4738585. This is complete: all 13 retired blobs and three checked retired commits
return authenticated 404s, with successful current-object controls. The all-ref audit
at `6d2d8d0` passes 39 commits/281 blobs. The purge gate is resolved; do not ask the owner
to wait for another reply or submit another ticket.

Feat-001 through feat-006, including feat-005c, are done. Feat-007 is `next`, ready for
its remaining publication and anonymous-access checks: GitHub still reports PRIVATE.
The owner previously said they would make it public, so this session left visibility
unchanged. Feat-008 remains `blocked` only by public-first visibility in fresh v4
preflight; purge, offline package validation, live origin, disclosure audit and the
pinned official contract pass. No upload or official score is claimed. Do not infer
owner-side submission status or quota without a receipt/history check.
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

- **Purge is resolved, not a blocker.** The owner supplied Support's reply dated
  2026-09-08 10:41 UTC. Ticket correspondence was not independently fetched, but
  removal is independently verified by authenticated API checks with controls.
  Preserve `notes/publication-removed-objects.json` and the live guard.
- **Our public-first policy remains active.** GitHub reports PRIVATE. Complete
  publication, verify anonymous access to the clean branch and rejection of every
  retired object, then rerun preflight before finishing feat-007. The private-state
  authenticated purge check already passes; anonymous 404s alone would not suffice.
  No further history rewrite or duplicate Support request is currently needed.
- **AI disclosure is no longer a blocker.** The owner confirmed OpenAI/Codex API tier,
  and on 2026-09-08 confirmed no model training and no other AI providers. The config
  records owner attestations, not an independent account audit or zero-retention claim.
- **Actual portal quota and receipt are unknown.** Confirm authenticated identity and
  remaining attempts immediately before a real upload. Do not conflate local hypothetical
  scorer output with an official score or count this preparation as a spent attempt.
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
the session-27 PRIVATE live preflight exits 1 only on public-first visibility.
Purge, live origin synchronization, reachable-history audit and pinned official contract pass.
V1/v2/v3 must not be reused; never edit
old deliverables in place. No upload, official score or receipt is recorded by this workflow.
Hashes and verification outcomes are in `notes/track1-submission.md`.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** the purge no longer prevents publication. The owner said
they would make the repository public; it is still PRIVATE at the latest check.
After publication, complete anonymous-access checks and fresh package preflight. The remote
checker prints availability counts, never retrieved blob contents. No automated uploader
was added; the exact authenticated upload/receipt procedure is in the submission notes.
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
