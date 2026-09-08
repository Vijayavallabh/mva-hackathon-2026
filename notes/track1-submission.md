# Track 1 submission preparation (feat-008)

## Conditional CSV update decision — session 30

On 2026-09-08 the owner authorized updating the submission CSV if required.
Review of feat-006b finds **no evidence-backed CSV change currently warranted**:

- No new allele or phase assignment was established by that follow-up.
- Sensitivity to removing evidence bonuses does not establish that an alternative
  pair is a better causal prediction. The existing baseline order is retained.
- All ten CSV `notes` cells already explicitly state `trans phase unconfirmed`.
- The report already distinguishes the unphased hypothesis and uncalibrated EPCRs
  from established causality. Rescaling EPCRs with order and distinctness unchanged
  would not improve the pinned scorer's metrics; there is no calibration dataset
  supporting new numerical probabilities.
- A temporary regeneration using `build_submission(DEFAULT_CANDIDATES, path)`
  matches the existing v4 CSV byte-for-byte. Package verification and regression
  tests pass with 10 rows and 20 normalized alleles.

The v4 CSV SHA-256 remains
`a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
Neither deliverable was overwritten and no redundant v5 was generated. This is
an evidence-based retention decision, not a claim that the current answer is correct.
Actual scores and owner-side upload status remain unverified.

A future allele correction, supported change of pair/order, or reviewed phase
evidence can justify a new immutable CSV/report package. Preserve the old bytes,
document the scientific reason, run reference/conformance/scenario checks, and
verify portal history before any upload. This conditional edit authorization is
not permission to spend another attempt or assert trans without evidence.

Checks run:

```bash
uv run python scripts/prepare_track1_package.py verify results/feat008/jvv7_genomewide_mva_v4
uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v4
uv run python scripts/test_track1_evidence.py
```

The direct regeneration and notes-cell checks are recorded in `progress.md`.

## Previous evidence and publication status

**Session 29 evidence clarification:** the actual competition score remains
unknown. [Feat-006b](track1-evidence-audit.md) now exposes score scenarios, ranking
sensitivity and native-phase uncertainty. It does not change the v4 CSV/report,
confirm trans, verify an owner-side upload, or spend an attempt. Read it before
interpreting the local 100/1 test as a predicted result.

Status on 2026-09-08 (session 28): publication and purge are verified; unchanged v4
passes live preflight with no blockers. Authenticated portal quota/upload/receipt
remain outstanding because the available API credentials did not establish portal
identity. No submission has been uploaded
by this workflow and no official score or remaining-attempt count is claimed.
The selected account from the local authenticated HF identity is `jvv7`; an empty
display name uses that username. Never print the token or complete identity response.

## Contract correction and unresolved owner decisions

The [official upload source](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/1c761cc23d90aebe6a011fd5b0b99517df42408c/tabs/submit_track1.py)
requires CSV, report (`.md` or `.pdf`) and a GitHub URL. It permits private repositories
during the competition, with public visibility required when the competition ends.
The earlier inference that the portal requires public visibility immediately was wrong.
The owner's stricter public-first policy remains active in AGENTS.md and the package
configuration until explicitly changed. Neither publication nor sharing retired objects
is safe while GitHub still serves those objects. The owner reports Support ticket 4738585
and supplied Support's removal reply. Session-27 authenticated verification passes the
purge gate. Session 28 verifies PUBLIC visibility and anonymous checks; feat-007 is complete.

The official AI-use instructions require provider, plan/tier and data-handling setting.
The owner confirmed OpenAI/Codex **API tier** on 2026-09-06 and, on 2026-09-08,
confirmed that data is not used to train the provider's models and no other AI providers
were used. These owner attestations complete `notes/track1-submission-config.json`.
They are not independently verified account settings and do not imply zero retention,
a retention duration, or permission to transmit prohibited subject data.

Verified public source revision: `1c761cc23d90aebe6a011fd5b0b99517df42408c`.
Upload source SHA-256: `685a3b6d57ef3a1c49a8be47845b10d77cb576ed2d30b5a90879b09707659b86`.
The live preflight checks both the Space HEAD and this upload-code hash, failing closed
on changed/unavailable rules. It never downloads private ground truth.

## Reproducible local package

```bash
uv run python scripts/prepare_track1_package.py --self-check
uv run python scripts/track1_submission.py --self-check
# Commit reviewed code, template and config first; build requires a clean tree.
uv run python scripts/prepare_track1_package.py build --name jvv7_genomewide_mva_v4
uv run python scripts/prepare_track1_package.py verify results/feat008/jvv7_genomewide_mva_v4
uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v4
# Push the reviewed commits before this live check:
uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v4
```

Build refuses to overwrite an existing package. Changed evidence, code or disclosure
requires a reviewed commit and a new package name. The manifest hashes the CSV, report,
local-check JSON, relevant source files and local evidence inputs. Verification repeats
the exact schema, identity, ranking and reference-normalization checks, regenerates the
report against the CSV/config, verifies committed source provenance and scans both
deliverables for prohibited content without printing matching source text.

The ten pairs preserve the reviewed baseline: one pair per gene, BUB1B first, with
lower-ranked alternatives explicitly weaker. No trans phase is asserted. The report
explains HPO/family separation, methods, targeted recall, CN/BAF screening limitations,
uncalibrated EPCRs and the ClinVar population-frequency caveat. The local 100 rank points
and 1.0 F-max use assumed row-1 truth, not the private answer key.

## Actual upload procedure — not yet executed

1. Owner disclosure and feat-007 publication/purge gates are complete. Keep enforcing
   the live checks; a passing historical result is not a waiver for future changes.
2. Use unchanged v4 while its verification passes. Only configuration/report/evidence
   changes require a reviewed commit and a new immutable package. Verify, push any
   intended commits and run fresh preflight. Use the exact CSV/report in the manifest.
3. In the authenticated official portal, confirm identity `jvv7`, current quota and
   remaining attempts. No local score test consumes a submission; the real upload does.
4. Submit the paired files and configured GitHub URL once. Do not retry blindly after
   a timeout: inspect authenticated submission history first to avoid spending two slots.
5. Preserve the returned submission identifier, timestamp, official scores and quota in
   a local receipt; hash the submitted files again. Record only permitted derived facts
   in tracked notes. Do not claim success without a receipt/history confirmation.
6. Mark feat-008 done only after successful upload and receipt verification. Changing
   either deliverable after upload requires an explicit task from the owner.

The script intentionally does not automate uploads or pretend that live quota is known.
It can produce an offline-valid draft while required owner inputs remain unresolved;
such a draft is **not submission-ready**.

## Review corrections

The first local package (`v1`) is superseded, not an uploaded deliverable. Independent
specification and standards review identified a stale-upstream check, an upload-policy
dependency in the public-repository purge check, and imprecise missing-AF wording.
The revised preflight queries the actual configured origin branch and always requires
the purge gate when visibility is PUBLIC. Unknown visibility fails closed. Tests cover
18 policy/visibility/purge combinations, a moved remote despite matching cached refs,
an unavailable remote, and payload/manifest corruption. Named evidence paths replaced
positional dependencies. The report now states the actual +1 default for missing AF.

## Historical v2 result and live blocker

Package: `results/feat008/jvv7_genomewide_mva_v2/`, built at code revision
`c5bc2e0` (full SHA in its manifest). The CSV contains 10 ranked pairs and 20 alleles
that pass exact reference normalization. SHA-256:

- CSV: `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`
- Report: `e4df63305f7cdb3e3e6deb97a8366f859e6a08fa0dc58caefe0c33eb27d7a98f`

The live preflight run after pushing returned exit 1, with the three missing disclosure
fields and failed remote purge as blockers. The official contract and live origin checks
passed. **Unexpectedly, GitHub reported PUBLIC**, confirmed by a separate query at about
17:44 UTC on 2026-09-06; all 13 retired blobs remained retrievable with zero unknown
errors and a successful control. This session performed no visibility change. The owner
was asked to authorize restoration to PRIVATE. The object checker did not print blob
contents, and no submission was attempted.

### Standards review

The independent review found a conditional purge-gate violation and a low-priority
positional-evidence naming issue. Both were corrected in `c5bc2e0`; re-review identified
no residual standards violations or material heuristic findings.

### Specification review

The independent review found stale cached-upstream verification, conditional publication
safety and inaccurate missing-AF wording. All three were corrected in `c5bc2e0`;
re-review identified no residual specification issues. The actual upload and owner
inputs remain explicitly unfinished.

Review totals: Standards 2 findings resolved; Specification 3 findings resolved (the
purge issue appears in both axes). No remaining finding in either reviewed axis.

## Owner clarification (2026-09-06)

The owner confirmed that they deliberately made the repository public and that Codex
uses API tier. The configuration records the tier verbatim in meaning; it does not infer
account-specific retention, training or data-sharing settings. Two disclosure fields
remain unresolved: `ai_data_handling_setting` and `other_ai_providers`.

The PUBLIC state is therefore explained, not an unexplained repository change. It does
not establish that GitHub purged the retired objects or clear the confidentiality gate.
The most recent remote check still found all 13 retrievable. No visibility change or
upload is performed in response to this clarification.

The v2 package above is a historical validated draft bound to the previous configuration.
Its hashes remain unchanged, but verification against the updated configuration must
reject it. A refreshed v3 draft is documented below. After completing the remaining
disclosure, commit the configuration and build a new package name (next: v4); never edit
the old deliverables in place.

## Historical v3 draft (2026-09-06)

Built `results/feat008/jvv7_genomewide_mva_v3/` from `cdfb444` with the owner-confirmed
API-tier disclosure. This refresh changes the report, not the ranked candidates or
scientific interpretation. Trans phase remains unconfirmed. The CSV SHA-256 is unchanged:
`a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
The report SHA-256 is
`eb836b42dc8b10c3dc010384edd124bd8e3c02a738a9106e097c887de42d421f`.

Build, offline verification and package regression pass: 10 pairs, 20 normalized alleles,
18 publication-policy cases, three live-upstream cases, portable copying and nine
corruption rejections. The real preflight exits 1 with exactly these blockers:

- API account data-handling disclosure remains unconfirmed.
- Other AI providers used remain unconfirmed.
- The independent retired-object purge gate still fails.

The live repository is PUBLIC; the pinned official upload contract and origin
synchronization checks pass. No submission was attempted, quota remains unqueried, and
there is no official score or receipt. Repeatedly rebuilding an unchanged draft cannot
resolve these blockers: the next material work requires the missing owner disclosures
and resolution of the retained-object exposure. The request to ignore that gate was not
implemented because it conflicts with the non-negotiable data-access rules.

## Current v4 draft (2026-09-08)

Built `results/feat008/jvv7_genomewide_mva_v4/` from committed revision `13f06ad`.
The report now includes the owner's no-training and no-other-provider confirmations;
there are **zero unresolved disclosure fields**. This is an owner attestation, not an
account audit. Ranked candidates and scientific interpretation are unchanged, including
unconfirmed trans phase. V1/v2/v3 remain untouched historical artifacts; do not upload them.

- CSV SHA-256: `a1f9315e223a07914589ce6884a66702b80e587ec5b7ad67f2ca1213f6caa225`.
- Report SHA-256: `f36bacbc506d5a717ee7a55f174fed3f376ed7beacd83d11091e57d319d0d68b`.
- Build/verify pass: 10 pairs, 20 reference-normalized alleles, zero missing disclosures.
- Regression passes: 18 publication-policy cases, three live-upstream cases, portable
  copying and nine corruption rejections. Package and official-scorer self-checks pass.
- Live preflight exits 1 with exactly one blocker: GitHub removed-object purge has not
  passed. PUBLIC visibility, origin synchronization and the pinned official contract pass.

No upload, official score or receipt exists. Resolve the purge, then rerun verification
and live preflight on v4; do not create v5 unless configuration, code or evidence changes.
Confirm authenticated identity and remaining quota immediately before any real submission.

### Containment and Support ticket update

The owner reports Support ticket **4738585** and restored PRIVATE visibility on 2026-09-08;
GitHub API independently confirms PRIVATE. Ticket contents/status remain owner-reported,
not inspected by this workflow. The earlier v4 preflight above is a historical PUBLIC
snapshot. With private containment, public-first visibility is also an upload prerequisite;
do not republish until the authenticated purge check and audit pass. V4 files and config
are unchanged. Await the existing ticket response; no duplicate request is needed.

### Fresh execution attempt (session 25)

At clean, synchronized revision `8476cc2`, reran:

```bash
uv run python scripts/prepare_track1_package.py --self-check
uv run python scripts/track1_submission.py --self-check
uv run python scripts/test_track1_package.py results/feat008/jvv7_genomewide_mva_v4
uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v4
```

Both self-checks and all package regressions pass (18 policy cases, three upstream
cases, portable copy and nine corruption rejections). Preflight confirms offline validity,
10 pairs, 20 reference-normalized alleles, unchanged v4 hashes and complete disclosure.
Live origin synchronization, the reachable-history disclosure audit and pinned official
contract pass. Preflight exits 1 with exactly these blockers:

- `repository policy requires PUBLIC visibility before upload`
- `GitHub removed-object purge gate has not passed`

The nested remote check confirms PRIVATE, 13/13 retired objects retrievable under
authentication, zero unknown errors and a successful reachable-blob control. The existing
Support ticket remains owner-reported; no response or completion is inferred from it.
Feat-008 is explicitly blocked, not done. Keep PRIVATE until purge verification passes;
finish feat-007 and repeat live preflight before checking portal identity/quota and uploading.
No code/configuration/deliverable changes, new package, upload or submission attempt were
made. Trans phase remains unconfirmed. Fresh startup output is recorded in `progress.md`.

### Additional phase work (session 26)

Feat-005c found no direct or indirect eligible-SNV fragment connection between the
leading alleles. A separate WhatsHap run on recalled variants also leaves both
unphased. See [phase-connectivity.md](phase-connectivity.md). The existing v4 CSV
and report remain unchanged and pass verification and regressions. No uploaded
deliverable was edited. The owner's announced intention to publish/submit was not
verified as an external action or receipt in this analysis session; do not infer
an official score or available quota from the local checks.

### Support removal verified (session 27)

The owner supplied a Support reply dated 2026-09-08 10:41 UTC, associated with ticket
4738585. Independent authenticated checks confirm all 13 retired blobs unavailable,
with zero unknown errors and a successful live-object control. The all-ref audit
passes. Purge is no longer a blocker; see [publication-audit.md](publication-audit.md).

At synchronized `6d2d8d0`, a fresh
`uv run python scripts/prepare_track1_package.py preflight results/feat008/jvv7_genomewide_mva_v4`
confirms unchanged hashes, 10 pairs, 20 normalized alleles, complete disclosure, live
origin synchronization and the pinned official contract. Exit 1 now has exactly one
blocker: `repository policy requires PUBLIC visibility before upload`.

The repository remains PRIVATE. The owner had stated they would publish; this session
did not change visibility. Finish public visibility and anonymous-access checks, then
rerun preflight and verify authenticated identity/quota before any upload. No new
package, upload or deliverable modification was performed. Trans remains unconfirmed.

### Public preflight and authenticated browser handoff (session 28)

At synchronized `e8b9113`, fresh public preflight exits 0: no blockers, unchanged
hashes, 10 pairs, 20 normalized alleles, complete disclosure, public visibility,
successful purge, clean history, synchronized origin and unchanged official contract.
Anonymous requests independently confirm clean main access (200), a live-blob control
(200) and all 13 retired blobs unavailable (404). Feat-007 is complete.

`HfApi().whoami()["name"]` confirms **jvv7**, without emitting credentials or the full
identity response. This is HF API identity, not proof of portal login. The live Space
is RUNNING. Its public `/config` identifies Gradio 6.24.0 and the read-only quota
callback `_quota_status`. A normal Bearer-authenticated POST of `{"data": []}` to
`/gradio_api/call/_quota_status`, followed by retrieval of the returned event, returns
HTTP 200 and `event: complete` with `data: [""]`: **no authenticated quota**.
The official `utils.py`/`submit_track1.py` require an OAuthProfile or request username
and return empty quota when identity is absent. No identity override, fabricated
profile, header spoofing, upload endpoint or `_handle_submit` call was used.

The remaining action requires the owner's signed-in browser:

1. Open the [official portal](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/)
   and sign in as **jvv7**. Select **Submit - Track 1**.
2. Check submission history and the displayed quota. If this package was already
   submitted outside this workflow, retrieve its receipt rather than submit again.
   Continue only with at least one remaining attempt.
3. Leave Team / Display Name blank for the configured individual submission. Set
   GitHub URL to `https://github.com/Vijayavallabh/mva-hackathon-2026`.
4. Attach only these two files from `results/feat008/jvv7_genomewide_mva_v4/`:
   - Predictions: `jvv7_genomewide_mva_v4.csv`
   - Report: `jvv7_genomewide_mva_v4_report.md`
   Do not attach the raw VCF, phenotype document, result directory or recovery bundle.
5. Click **Submit & Score** once. On timeout, inspect history before retrying.
6. Preserve the displayed submission number, timestamp, scores and remaining quota;
   share that receipt without credentials. An official score has not yet been observed
   by this workflow. Trans phase remains unconfirmed regardless of format validation.

No upload was attempted and no attempt was spent by the quota check. The successful
preflight flag means the package is ready for an authenticated submission workflow,
not that browser authentication or quota was successfully checked.
