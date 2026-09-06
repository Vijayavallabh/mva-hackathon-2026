# Prepared GitHub Support request — not sent

Submit through [GitHub Support](https://support.github.com/contact) while authenticated as
the repository owner. Keep the repository private until the removal checks pass.

Subject: Purge retained objects after sensitive-text history rewrite in a private repository

Repository: `Vijayavallabh/mva-hackathon-2026`

We are preparing this private repository for public release. A local audit found short
overlaps with restricted clinical source wording in historical Markdown/Python files.
We rewrote all reachable history and force-pushed the cleaned main branch. No raw sequence
or variant files or phenotype documents were committed. This request contains no protected text.

The cleaned branch initially pointed at `5581dfd84f7ab81bb5b341bf4a7cb1475970e99c`, replacing
`65ad73d4545974c1afa8d8ac5c21ca7aa74f3214`. The originally identified affected commit was
`05ed1ccd8ff67dd93a34cc8d56e228276d05a7ab`. Subsequent normal commits preserve the clean
history. The full rewrite changed 22 commits; its earliest changed original commit is
`119577d2977e30abd6c3783aa2e2963f03b26a23`. There are no pull requests, forks or extra
branches in our inventory.

After the force-push, authenticated lookups to the repository's Git blobs endpoint still
return all 13 retired objects listed below. Please purge the obsolete objects and cached
views/references, including original affected commits, or advise the exact remaining steps
needed so changing this repository to public cannot expose the retired content.

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
