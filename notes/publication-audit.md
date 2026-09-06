# Publication audit — feat-007

As of 2026-09-06, the cleaned `main` branch is pushed, but the repository remains private.
GitHub still returns all 13 retired blob objects by their identifiers after the rewrite.
Changing visibility now could expose those objects. Feat-007 is therefore incomplete
pending GitHub Support's removal of the retained objects and a successful remote recheck.

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

## Remaining publication gate

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
clinical text. It has not been sent. Do not upload the recovery bundle or protected source
to Support.

After Support confirms removal, rerun the remote checker and the full local audit, verify
all advertised remote refs and any newly created remote surfaces, then change visibility:

```bash
gh repo edit Vijayavallabh/mva-hackathon-2026 \
  --visibility public --accept-visibility-change-consequences
gh repo view Vijayavallabh/mva-hackathon-2026 --json visibility,url
```

Finally verify anonymous access to the clean branch and failure to retrieve each removed
object, record the public URL, and only then mark feat-007 done and feat-008 next. No Track 1
submission has been uploaded by this work; trans phase remains unconfirmed.
