# Prepared GitHub Support request — not sent

Updated 2026-09-08. Submit through [GitHub Support](https://support.github.com/contact)
while signed in as the repository owner. Choose sensitive-data removal/security and
paste the request below; do not attach original history, raw data or clinical wording.
No ticket has been sent and no ticket identifier exists in this workflow. GitHub CLI
repository authentication is available, but an authenticated Support portal session is not.
The owner has already made the repository PUBLIC; temporary PRIVATE visibility is
recommended containment, not proof of purge, and requires the owner's direction.

Subject: Sensitive-data removal: server-side GC and cached-view purge after completed history rewrite

Repository: `Vijayavallabh/mva-hackathon-2026`

Repository URL: https://github.com/Vijayavallabh/mva-hackathon-2026

The repository is currently PUBLIC. A local audit found short overlaps with restricted
clinical source wording in historical Markdown/Python files.
We rewrote all reachable history and force-pushed the cleaned main branch. No raw sequence
or variant files or phenotype documents were committed. This request contains no protected text.
The removed wording derives from a restricted clinical document under data-access terms;
this is a sensitive-data exposure, not a credential that can be rotated. Some other
matches were conservatively included by the local lexical audit, as explained below.

The cleaned branch initially pointed at `5581dfd84f7ab81bb5b341bf4a7cb1475970e99c`, replacing
`65ad73d4545974c1afa8d8ac5c21ca7aa74f3214`. The originally identified affected commit was
`05ed1ccd8ff67dd93a34cc8d56e228276d05a7ab`. Subsequent normal commits preserve the clean
history. The full rewrite changed 22 commits; its earliest changed original commit,
derived from the rewrite commit map, is `119577d2977e30abd6c3783aa2e2963f03b26a23`.
The regular git-filter-repo blob-callback rewrite was used; this identifier is not
claimed to be output from its optional sensitive-data-removal mode.

Fresh inventory on 2026-09-08:

- Affected pull requests: 0; no open or closed pull requests exist.
- Forks: 0. Advertised refs: only `refs/heads/main` and symbolic HEAD.
- Actions runs, releases and issues: 0 each.
- No Git LFS objects were involved in the rewrite.
- Audited clean HEAD: `3c64b87b9837a97a183424b188457a98d86900ab`; subsequent documentation
  commits may advance main without restoring old history.
- All reachable local history: 34 commits, 251 unique blobs, zero audit findings.
- Authenticated retired-object lookup: 13/13 retrievable; zero unknown errors;
  a known current reachable blob succeeds as a positive access control.
- Independent unauthenticated Git blobs API requests also returned HTTP 200 for all
  13 retired objects and the reachable control. Response bodies were not displayed.
  Exposure is therefore confirmed for anonymous access, not only repository administrators.

After the force-push, authenticated lookups to the repository's Git blobs endpoint still
return all 13 retired objects listed below. Please run server-side garbage collection
and purge cached views/references, including original affected commits and these retired
blobs. Please confirm completion, or identify any remaining references preventing removal.
Local garbage collection or another push cannot remove GitHub's retained storage.

```text
09ef9dd25f68503360220c9903c1632c7906adaf
1389a463d29667565bcf35daa594b3fd57c60c49
2b1fd04d6931072ea5c363ecf80c0483deaae661
322367e82ea2a239a2547a4368b32da6eee0fba2
421bbf3b5127aafff97698cc20f436612921800a
78b3348b44e0ed7d73b9df70f1f49f78102427ed
7db139a120a20681c739bbd517a61620abd0e47f
8ef7b7e4704a2be8e5cb0c6e1d29c09ae4c80b77
99238d188e0f185450cb35fbd6643f1afea64a97
a8c3e60b4a2ccdf2a79cb649ba94f8ea1fbc4d11
bd4452b3a9b6a53ad4a527adf75e394806e007d5
cff4aca847dab73ee5fc9fcc009672cc732a28bd
d9b1661f3915e1fc1c9953241c2656e54d39fc67
```

Some additional matches were conservatively removed even where wording overlaps public
competition rules. We request purge of the entire retired-object inventory. We can provide
non-content rewrite metadata if required, but cannot reshare clinical source text or a
bundle of the original history.
