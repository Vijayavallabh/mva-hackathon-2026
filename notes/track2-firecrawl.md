# Track 2: self-hosted Firecrawl MCP run and integration

2026-09-09 IST, session 37, baseline `42171c0`. Feat-009 only. This extends the
scientific/exposure and Atlas reviews; it does not change Track 1 files, establish
trans phase, perform laboratory experiments or upload a Track 2 entry.

## Outcome

Connected through a real newline-delimited JSON-RPC **STDIO MCP** process to the
owner's local Firecrawl API at `http://127.0.0.1:3002`. All **26 advertised tools**
were exercised across **84 calls** in three bounded runs. There were **79 non-error
responses, three no-passage reads and two tool errors**. Every tool had at least
one non-error response; this is tool coverage, not proof that every call or scientific
claim succeeded. The deprecated `firecrawl_extract` was not advertised or invoked.
No native Codex tool registration/global configuration was changed; the reproducible
workspace bridge is [track2_firecrawl.py](../scripts/track2_firecrawl.py).

The substantive result is [research draft 3](track2-report-v3.md), an updated
[pitch](track2-pitch-v3.md) and [validation addendum](track2-validation-v3.md).
An independent [scientific supplement](track2-firecrawl-scientific-review.md)
checks six additional primary papers at selected-section depth, another paper's
abstract and one official label. These eight documents supplement, rather than
silently alter, the preserved 53-source/12-candidate baseline ledgers.

Everolimus remains a conditional pathway experiment; HCQ remains reserve. Pralatrexate
is a new fusion-positive RMS tumour-only horizon, with recurrence and schedule toxicity
explicit. Rapamycin/slippage evidence adds a cell-fate safety requirement. An engineered
rapamycin dimerizer is excluded from therapeutic rescue support. No clinical exposure
margin, phase confirmation, efficacy probability or winning-score guarantee follows.

## Transport and source provenance

The active entry was:

```text
/home/sports/.npm/_npx/12b05d58670d8359/node_modules/firecrawl-mcp/dist/index.js
package version: 3.24.0
entry SHA256: a227fb070b4e21605925896273bfb05381df8810fda8b781606cd28567dd5846
```

This observed version supersedes the sibling README's installation example, not the
entire deployment's version history. The existing package was used without installing
or executing an unpinned download. MCP protocol `2025-06-18` initialization, server
information and the actual tool schemas are retained in each run directory.

The [capability/source review](firecrawl-capability-review.md) records the clean
self-host setup revision, dirty underlying Firecrawl checkout, selected file hashes,
all tool names and downstream service boundaries. Those fingerprints are not a
cryptographic attestation of the running container build or every dependency. Repeating
the live workflow requires a compatible owner-managed service and public network access;
it is not an offline-only reproduction or a vendored full Firecrawl deployment.

The client runs Node in an empty temporary directory with only a small non-secret
environment. This prevents the server's dotenv loader from reading the project `.env`
and avoids inheriting API keys, proxy settings or `NODE_OPTIONS`. Native stderr is
discarded because upstream error strings can contain credentials. Structured tool
errors are sanitized, not printed verbatim. No account settings/keys were read.

## What each tool group contributed

| MCP tools | Bounded use and observed result |
|---|---|
| `search` | Twelve broad queries, six focused compound queries and one public-gene control query; 122 returned web rows/106 distinct URLs. One broad correction query failed. |
| `research_search_papers` | Four supplementary bibliographic queries, at most 12 results each; discovery, not full-paper screening. |
| `research_inspect_paper` | Two baseline and five new DOI metadata lookups; identity is distinct from claim support. |
| `research_related_papers` | Citers and references for two public seed papers, at most 12 results each; ranking is lexical, not biological confidence. |
| `research_read_paper` | Four baseline and five follow-up passage requests. Six returned text; three baseline reads returned no passages. |
| `research_search_github`, `developer_search` | Public reproducibility/implementation discovery; no downloaded repository code was executed. |
| `scrape`, `map` | Public source/correction/FP-RMS retrieval and bounded gene-site mapping. Statin publisher scrape failed, while passage retrieval and independent primary XML checking succeeded. |
| `crawl`, `check_crawl_status` | One public MedlinePlus BUB1B page; completed with one page, not an unrestricted site crawl. |
| `parse` | Parsed only the HTML returned from that public gene page; never the protected clinical DOCX or local subject files. |
| `agent`, `agent_status` | Completed public JCI-paper synthesis on the model identifier below; checked against primary text and not treated as independent experimental evidence. |
| `feedback`, `search_feedback` | Factual retrieval feedback for the newly created public jobs; no publisher/support messages or efficacy endorsements. |
| `interact`, `interact_stop` | Literal read-only title inspection of the public gene page; successful explicit stop. No login, target-site write or downloaded code execution. |
| All eight `monitor_*` tools | Owned one-page temporary monitor: create/list/get/update/run/check/checks/delete. One baseline page completed, zero page errors; no email, Slack or webhook was attempted. List output was projected to the owned ID before persistence. |

Operational counters, search result rows and bibliographic hits are overlapping units.
Do not sum them into a count of screened studies. Broad multi-compound queries had
poor precision; focused per-compound queries were an explicit adaptive correction.
No dual independent full-text screening, exhaustive citation census, unpublished-data
search or complete systematic review was performed.

## Failures, truncation and cleanup

The two sanitized tool errors were `search_bubr1_correction` and `scrape_statin`.
The three empty reads were the DOI requests for ARST1431, the secukinumab combination
paper and North's SIRT2 paper. A request returning no passages is not evidence that
the paper contains no relevant result or that accessible text exists nowhere. Direct
correction-page retrieval and independent primary-source checking supplied alternatives.

The first decoder flagged any occurrence of “truncat”, including a paper's biological
truncation terminology. Thus its `read_bubr1` flag does **not** establish transport
truncation. The final decoder recognises explicit output-truncation notices/fields.
Regardless of that flag, passage retrieval is not full-paper reading and can omit
tables, limitations and neighboring context. MCP/server output limits remain finite.

The temporary monitor's manual check completed with one new baseline page, no changed
page and no page errors. This cannot test longitudinal change sensitivity. Its initial
nonempty goal implicitly enabled judging in the server schema, although a new baseline
does not demonstrate a change-judge call. The final client explicitly sets
`judgeEnabled:false` for future capability probes. Conditional Google/Vertex paths
exist in source; no blanket “all processing was Fireworks/local” claim is made.

Deletion returned `success:true` after the terminal check. Source code implements this
as **soft deletion and schedule removal**, not immediate erasure of public check history,
logs or feedback. No unrelated monitor was changed. Browser stop also returned success;
all MCP child processes exited. No recurring task or intentionally unfinished job was
left running. A successful deletion acknowledgement is not a retention/account audit.

## Exact run pins and reproduction

All run artifacts are ignored local public-literature outputs. Each manifest records
arguments, timestamps, per-call status and result SHA256; schemas and executing script
snapshots are retained. All recorded result hashes and three executing-script hashes
were rechecked after completion. Hashes detect byte drift, not publisher authenticity.

| Directory under `results/feat009/` | Calls | Manifest SHA256 |
|---|---:|---|
| `firecrawl-research-v1` | 30 | `1f23e8a75787c9e162d157e28a2dad2894622234e3d81ab50c82db4a6db3b7a4` |
| `firecrawl-capabilities-v1` | 36 | `ba4e05c09be35a85c337cce6219508b7742e11ede07b35ac4ae5301b897a77ef` |
| `firecrawl-followup-v1` | 18 | `9e5e31dcc2499d161c0120a410486091edefe7572aae2d7b901cde0b74736e18` |

The first two runs used script SHA256
`618ce6ca841bf0e49290cf6ad2d9d924c6f1c84e1527a93370a53e58a0079a29`;
the follow-up used `a98fbdc0e59182c5fbe3e7a3461023c3fb5b09be5163fbe7361c5f765b891b70`.
Final source includes subsequent guard fixes; do not pretend those source hashes are
identical. Initial scripts returned exit 0 despite per-call failures; the final CLI
returns 2 for any non-ok call, including no-passage results, preserving earlier successes.
Failure details in the manifests—not the old exit code—govern the review.

```bash
# Each live mode requires a new output directory; no overwrite or automatic retry.
uv run python scripts/track2_firecrawl.py discover results/feat009/firecrawl-discovery-new
uv run python scripts/track2_firecrawl.py research results/feat009/firecrawl-research-new
uv run python scripts/track2_firecrawl.py capabilities results/feat009/firecrawl-capabilities-new
uv run python scripts/track2_firecrawl.py followup results/feat009/firecrawl-followup-new
uv run python scripts/test_track2_firecrawl.py
uv run python scripts/test_track2_release.py
uv run python scripts/track2_release.py build results/feat009/jvv7_track2_research_v3
uv run python scripts/track2_release.py verify results/feat009/jvv7_track2_research_v3
uv run python scripts/track2_evidence.py verify results/feat009/jvv7_track2_research_v2
uv run python scripts/track2_evidence.py track1
```

Use `--entry` to identify a compatible installed MCP entry on another machine; this
does not install/start the service or alter global Codex configuration. Re-running
`capabilities` creates a temporary local monitor and feedback records and uses an
external model for the public-paper audit; it is not a purely read-only smoke test.

## Adversarial revisions and delivery boundary

Independent standards tests exposed failure-classification, truncation, full-stdin
deadline, malformed-response, metadata-startup, cleanup, duplicate-tool and exit-code
defects. Fixes enforce bounded writes/reads, preserve errors as errors, project unrelated
monitor records before persistence, require deletion acknowledgement, and keep monitor
cleanup independent from browser cleanup. Unsupported non-text tool envelopes fail
closed. Startup prepares artifacts before spawning and closes the child if registration
fails. The advanced monitor body is complete because it replaces, rather than merges,
shorthand fields. Both cases have regressions. The final bridge has 44 tests, the v3
release checker 41; with 215 existing tests, all 300 pass. Final-source MCP discovery
also succeeds in `results/feat009/firecrawl-final-discovery-v2/`. These tests and discovery
are not additional literature calls or scientific successes.

The new release checker preserves v2 and Track 1, binds an exact 15-file v3 package to
current tracked inputs, rejects symlinks/historical-directory descendants, checks phase,
explicit null exposure and current AI disclosure, and refuses overwrite. Its hashes are
not signatures or scientific validation. V3 is a research draft; recorded/hosted video,
final owner review, live rules/disclosure/quota and upload receipt remain outstanding.

Fireworks-hosted `accounts/fireworks/models/glm-5p3-flash` was observed in the completed
agent response. This adds to OpenAI/Codex and Google DeepMind Atlas use. The owner-attested
OpenAI no-training setting is not extended to this additional route without evidence.
Self-hosting is not zero retention. The v3 report and pitch carry the updated disclosure
and Atlas output notice; historical uploaded/reviewed files remain byte-for-byte intact.
