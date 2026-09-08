# Publication audit — feat-007

As of 2026-09-08 session 28, **feat-007 is complete**. The owner made the repository
PUBLIC after Support removal on ticket **4738585**. Authenticated and anonymous
checks reject all 13 retired blobs, live-object controls succeed, and reachable
history passes the disclosure audit. Earlier private/failed-purge snapshots below
are historical. No agent changed visibility or uploaded submission files.

## Public verification (session 28)

Verified public URL: [Vijayavallabh/mva-hackathon-2026](https://github.com/Vijayavallabh/mva-hackathon-2026).

- `gh repo view Vijayavallabh/mva-hackathon-2026 --json visibility,url,forkCount`
  confirms PUBLIC and zero forks. All-state PR count is zero.
- Anonymous standard-library `urllib.request` GETs, with no Authorization header,
  return HTTP 200 for `raw.githubusercontent.com/Vijayavallabh/mva-hackathon-2026/main/README.md`
  and the current README Git blob. Each of the 13 IDs from
  `notes/publication-removed-objects.json` returns HTTP 404 from the GitHub Git blobs
  API. The helper emits only status counts; bodies are not displayed.
- Authenticated `scripts/check_publication_remote.py` passes inside live preflight.
- `uv run python scripts/audit_publication.py --output results/feat007/public-history.json`
  at `e8b9113` passes all refs: 40 commits, 289 unique blobs, zero findings.
- `git ls-remote origin` shows only synchronized HEAD/main.
- Fresh v4 package preflight exits 0 with no blockers, PUBLIC visibility and
  `ready_for_authenticated_submission=true`. This flag does not establish portal
  login or quota. The signed-in browser handoff is in `track1-submission.md`.

The publication feature is complete; continue enforcing data gates and live purge
checks. Removal cannot revoke copies previously downloaded by third parties.

## Post-Support verification (session 27)

At synchronized HEAD `6d2d8d0`:

- `uv run python scripts/check_publication_remote.py`: exit 0; 13 objects checked,
  zero retrievable, zero unknown errors, successful current-README control.
- Authenticated `gh api --silent repos/Vijayavallabh/mva-hackathon-2026/git/commits/<id>`
  checks return 404 for `05ed1ccd8ff67dd93a34cc8d56e228276d05a7ab`,
  `65ad73d4545974c1afa8d8ac5c21ca7aa74f3214` and
  `119577d2977e30abd6c3783aa2e2963f03b26a23`; the same endpoint succeeds for current
  HEAD `6d2d8d0ca00b2b5be0b128367bdcf1d91a7ae5fe`. Bodies are suppressed.
- `uv run python scripts/audit_publication.py --output results/feat007/post-support-history.json`:
  all refs pass, 39 commits and 281 unique blobs, zero findings.
- `git ls-remote origin`: only HEAD/main at the synchronized commit. Fresh GitHub
  metadata queries find zero forks, PRs (all states), Actions runs, releases and issues.
- Remote-check self-check and `scripts/test_publication_hooks.py` pass.
- Fresh v4 preflight passes offline validity, live origin synchronization, disclosure
  audit, purge and the pinned official contract. It exits 1 with just
  `repository policy requires PUBLIC visibility before upload`.

The owner previously stated they would make the repository public. That action has
not yet occurred according to the current API check. After publication, verify
anonymous clean-branch access and retired-object rejection, then rerun live preflight.
Do not count a private-repository anonymous 404 as purge evidence or claim an upload
receipt from these checks. The independent authenticated results above establish the
tracked purge gate's success; they cannot recover copies previously downloaded by others.

## Work completed

The user explicitly requested feat-007 on 2026-09-06, authorizing its defined history
cleanup, force-push and eventual visibility change. The implementation prepared an isolated
mirror before touching the active branch and kept a local recovery bundle under ignored
`results/feat007/`. No subject file or protected matching text was printed or uploaded.

The new audit checks every reachable commit and unique file blob across all refs, annotated
tag metadata, filenames and ref names. It rejects noncommit ref targets, binary/oversized
blobs, prohibited file paths, recognizable credentials and literal VCF record patterns.
Names containing protected patterns are replaced by hashes in reports. Local comparison
uses three-word sequences from the two narrative-bearing phenotype table columns, with
the supplied HPO labels exempted, and eight-word sequences from the full document. This
is a conservative lexical detector: shared generic phrases and public rules can match,
and the absence of a match is not a proof against every possible disclosure.

The broader audit found 13 matching historical blob versions across seven paths. This
includes the previously known protected overlaps and conservative additional matches;
it does not mean every matched phrase was confidential. For the historical copies,
matched words were replaced with `redacted`, retaining punctuation and Python syntax.
The current two affected notes were then paraphrased for readability. Every modified
historical Python blob was parsed successfully before filtering.

`git-filter-repo==2.47.0` performed the rewrite in a fresh packed mirror made with
`git clone --mirror --no-local`. The installed Git is 2.34.1; its lack of
`cat-file --batch-command` prevents filter-repo's optional sensitive-data-removal mode.
The regular blob callback rewrite was used, followed by our independent all-ref audit.
There were no Git LFS files, alternate branches, pull requests or forks to migrate.

The prepared mirror passed with 26 commits and 188 unique blobs; the filter-repo commit
map records 22 rewritten commits, starting at original commit
`119577d2977e30abd6c3783aa2e2963f03b26a23`. Its head was
`5581dfd84f7ab81bb5b341bf4a7cb1475970e99c`. The configured origin previously pointed at
`65ad73d4545974c1afa8d8ac5c21ca7aa74f3214`. The push used that exact expected old value
as its lease, so a concurrent update would have stopped the operation. Local and remote
`main` matched immediately afterward. Further normal commits contain the gate and handoff.

## Reproduce the checks

Run from the repository root with the gated document present locally:

```bash
uv run python scripts/audit_publication.py --self-check
uv run python scripts/prepare_publication_history.py --self-check
uv run python scripts/check_publication_remote.py --self-check
uv run python scripts/test_publication_hooks.py
uv run python scripts/audit_publication.py --staged
uv run python scripts/audit_publication.py --output results/feat007/current-history.json
git log --all --pretty=format: --name-only
./scripts/no_data_in_git.sh
uv run python scripts/check_publication_remote.py
./init.sh
```

The staged phrase check also runs through the existing pre-commit gate whenever the
protected source is available. Public clones do not download that source; their path gate
still operates. `init.sh` installs the pre-commit hook when absent and requires it to
resolve to the executable repository gate. An incompatible hook is preserved and startup
fails with integration guidance. Local audit fixtures test old content removed from HEAD, annotated
tags, direct blob refs and protected filenames/ref names without using patient data.

The exact preparation command was:

```bash
uv run python scripts/prepare_publication_history.py \
  --destination results/feat007/final-mirror.git
git bundle create results/feat007/pre-publication-recovery.bundle --all
git fetch --no-tags results/feat007/final-mirror.git refs/heads/main
git read-tree -m -u 97e6eede0f8a958f2c090458aadcdcbb11f5cf8d 5581dfd84f7ab81bb5b341bf4a7cb1475970e99c
git update-ref refs/heads/main 5581dfd84f7ab81bb5b341bf4a7cb1475970e99c 97e6eede0f8a958f2c090458aadcdcbb11f5cf8d
git push --force-with-lease=refs/heads/main:65ad73d4545974c1afa8d8ac5c21ca7aa74f3214 origin main
```

Those mutation commands are an execution record, not instructions to replay on the
already-cleaned branch. Recovery bundles and failed/prepared mirrors remain local under
the deletion plan; do not push their obsolete refs or share them.

## Historical failed purge gate (before Support's response)

At this earlier snapshot, owner-reported ticket **4738585** was pending and PRIVATE
visibility was independently confirmed. The authenticated checker returned 13/13 retired objects, zero
unknown errors and a successful reachable-object control. Session 27 above supersedes
this result. Private-repository anonymous 404s alone never demonstrate purge.

The remote checker makes authenticated, silent GitHub blob lookups using the fixed IDs in
`publication-removed-objects.json`. It records availability only. All 13 objects returned
success after the cleaned branch was pushed. A known reachable README blob must succeed
through the same API as a positive access control; permission-related 404s therefore cannot
produce a passing purge check. Metadata checks also found zero Actions runs,
releases, issues, pull requests, forks and Pages deployments; Discussions are disabled.
No content was sent to a new third party by these checks.

GitHub documents that rewriting history does not remove all cached views and references;
Support may need to purge them. See [GitHub's sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
The request is prepared in `github-support-request.md`; it contains identifiers and no
clinical text. The owner now reports submitting ticket 4738585. Do not upload the recovery bundle or protected source
to Support.

After Support confirms removal, rerun the remote checker and the full local audit, and
verify all advertised remote refs and any newly created remote surfaces. Keep visibility
PRIVATE during these authenticated checks; anonymous 404s alone do not demonstrate purge:

```bash
uv run python scripts/check_publication_remote.py
uv run python scripts/audit_publication.py --output results/feat007/current-history.json
git ls-remote origin
gh repo view Vijayavallabh/mva-hackathon-2026 --json visibility,url
```

Finally verify anonymous access to the clean branch and failure to retrieve each removed
object, record the public URL, and only then mark feat-007 done and feat-008 next. No Track 1
submission has been uploaded by this work; trans phase remains unconfirmed.

## Earlier resolution attempt, 2026-09-08 (before ticket and containment)

The owner explicitly requested resolution of the purge gate. Fresh checks found the
remote main at `3c64b87b9837a97a183424b188457a98d86900ab`, no extra advertised refs,
zero forks and pull requests, and zero Actions runs, releases and issues. Commands:

```bash
gh repo view Vijayavallabh/mva-hackathon-2026 --json nameWithOwner,visibility,url,viewerPermission,forkCount
git ls-remote origin
gh api --paginate 'repos/Vijayavallabh/mva-hackathon-2026/pulls?state=all' --jq 'length'
gh api repos/Vijayavallabh/mva-hackathon-2026/actions/runs --jq '.total_count'
gh api repos/Vijayavallabh/mva-hackathon-2026/releases --jq 'length'
gh api 'repos/Vijayavallabh/mva-hackathon-2026/issues?state=all&per_page=100' --jq 'length'
```

The all-ref audit passed: 34 commits, 251 unique blobs, zero findings. The authenticated
remote checker still failed: 13/13 retired objects retrievable, zero unknown errors and
a successful reachable-blob control. There is no additional advertised ref to remove.
An independent standard-library `urllib.request` check, with no Authorization header,
requested `/repos/Vijayavallabh/mva-hackathon-2026/git/blobs/{id}` for the fixed inventory
and current README control. It emitted status counts only: retired objects HTTP 200 = 13,
control HTTP 200, no response bodies displayed. Anonymous exposure is confirmed.

[GitHub's removal procedure](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository#fully-removing-the-data-from-github),
checked today, assigns server-side garbage collection and cached-view removal to Support.
Another local rewrite, force-push or local GC does not perform that server-side step.
Deleting/recreating the repository is not authorized or an established purge guarantee.

The refreshed `github-support-request.md` now accurately states PUBLIC visibility,
the sensitive-data context without source wording, zero affected PRs, the earliest changed
commit from the commit map, no LFS involvement, and fresh availability evidence. It asks
Support to perform server-side GC and remove cached references.

**Remaining handoff:** sign into the [Support portal](https://support.github.com/contact)
as the owner and send that request. The available GitHub CLI session has repository ADMIN
access, but no authenticated Support browser session or ticket-submission integration is
available here. [GitHub documents portal sign-in and submission](https://docs.github.com/en/support/contacting-github-support/creating-a-support-ticket);
security reports remain supported on GitHub Free. No request was sent and no ticket ID is
claimed. Do not ask the owner to supply a password, token, cookie or protected attachment.
Temporary PRIVATE visibility is recommended containment, not purge; no visibility change
was made against the owner's previously stated public-repository preference.
