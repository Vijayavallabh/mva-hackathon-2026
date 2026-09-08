# Session handoff

**Last updated:** 2026-09-08 (session 22 — owner AI disclosure completed; v4 preparation)

**Current objective / active feature:** feat-008 (Track 1 CSV/report package).
Feat-001 through feat-006 are done; feat-007 is blocked, not active. The history rewrite
and force-push are complete. The owner made the repository PUBLIC; the independent
obsolete-object purge remains unresolved. See `notes/publication-audit.md`. Feat-008 preparation can proceed
locally, but no upload or official score is claimed. See `notes/track1-submission.md`.

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

- **Public visibility confirmed by owner:** the owner deliberately made the repository
  PUBLIC. The most recent 13-object purge check still failed. This confirmation explains
  the change but does not waive confidentiality or establish successful removal.
  Treat the previous PRIVATE snapshots as historical, not current. Feat-007 is not done.
- **Publication safety remains unresolved:** reachable history is clean after the authorized
  rewrite and force-push, but all 13 retired blobs remain retrievable through GitHub's API.
  GitHub Support must purge the retained objects and cached references. A request with
  object identifiers only is prepared at `notes/github-support-request.md`; it has not been
  sent. No extra authorization for the already-completed history rewrite is needed.
- **Our public-first policy remains active.** The official portal permits private
  repositories until competition end, contrary to our earlier inference. The owner
  has been asked whether to keep the stricter rule or allow the private URL at upload;
  no change is assumed. After Support confirms the purge,
  run `uv run python scripts/check_publication_remote.py` and the full local disclosure
  audit, verify newly introduced remote refs/surfaces and anonymous access; PUBLIC
  visibility is already owner-confirmed. Feat-007 remains `blocked`, not done.
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
Feat-008's v3 draft is now historical because the owner completed the configuration.
Commit the new disclosure and build `results/feat008/jvv7_genomewide_mva_v4/`, then
verify the paired files and run regressions and live preflight. V1/v2/v3 must not be
reused; never edit old deliverables in place. The purge gate remains independent.
Hashes and verification outcomes are in `notes/track1-submission.md`.

**Resume with:**
```bash
cd /mnt/md0/IITM/BackUp/Home/vijayavallabh/mva-hackathon-2026
./init.sh
```

**Recommended next step:** validate the v4 package with the completed owner disclosure.
Separately, resolve the failed purge gate: the prepared GitHub
Support request is still unsent, and public visibility does not clear it. After removal,
run the publication checks and a fresh package preflight. The remote
checker prints availability counts, never retrieved blob contents. No automated uploader
was added; the exact authenticated upload/receipt procedure is in the submission notes.
Do not rerun unchanged draft creation as a substitute for resolving the remaining inputs.
The owner's request to ignore the purge gate was not implemented; the latest follow-up
continued only safe local preparation. No authorization to send Support a message or
change visibility has been inferred from that request.

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
