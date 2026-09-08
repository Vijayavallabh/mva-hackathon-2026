# Self-hosted Firecrawl: capability and disclosure review

Reviewed 2026-09-09 for feat-009. This is a read-only source review, not a claim
that the 26 tools have all succeeded in the present deployment. No `.env`, cookie
jar, credential value, subject file, or raw runtime configuration was read. No
live tool suite, external model job, monitor, feedback write, installation, or
sibling-repository mutation was performed by this review.

## Findings that affect the integration

The available integration is a **local STDIO MCP process backed by a local HTTP
API**, not an HTTP `/mcp` endpoint. Local transport does **not** mean that all
processing, logging, or model inference stays local. The documented default is
Fireworks-hosted GLM, and source code also contains explicit Google/Vertex model
routes. Use only public literature, public gene/mechanism queries, and permitted
derived summaries. No protected file may be submitted to any tool, including
`parse`, local browser interactions, feedback notes, or agent prompts.

Primary implementation sources inspected:

- Sibling `firecrawl-selfhost`, clean revision
  `081d6d0ef114c989198a8e1ab6b501d098ca426a`: [README](../../firecrawl-selfhost/README.md),
  [capability test](../../firecrawl-selfhost/tests/mcp-local-capabilities.mjs),
  [live-tool test](../../firecrawl-selfhost/tests/mcp-live-tools.mjs),
  [reliability patch](../../firecrawl-selfhost/scripts/patch-mcp-reliability.mjs),
  and [research proxy](../../firecrawl-selfhost/research-service/main.py).
- Actual sibling checkout `firecrawl`, revision
  `fe49e4c97b84b135f7aedc41c4cb61dd50ce611a`, **with local modifications**.
  This is not the absent `firecrawl-selfhost/firecrawl` directory described by
  the setup layout. The setup script's default upstream pin
  `7f1ecf3bd2eb92ad3fe560cc441421bf8a12b12e` is not a description of the actual
  checkout. HEAD alone cannot reproduce these patched files; selected hashes are
  recorded below. This review does not establish that running containers match
  this checkout.

## Transport and advertised surface

The capability test launches Node with the installed
`firecrawl-mcp/dist/index.js` as its entrypoint, using piped stdin/stdout and
newline-delimited JSON-RPC. It initializes protocol version `2025-06-18`, sends
`notifications/initialized`, then `tools/list`. README documents package version
`firecrawl-mcp@3.22.2`. Prefer an already installed, identified entrypoint over
unbounded `npx -y` installation during the evidence run. Preserve stderr separately
and never interpret it as an MCP result.

The local API setting is `FIRECRAWL_API_URL=http://127.0.0.1:3002`.
`FIRECRAWL_SELF_HOSTED_DB_ENABLED=true` advertises 26 tools; explicit `false`
advertises 14. The patch also enables the database-backed surface by default for
this local stack. Advertisement is therefore **a configuration assumption, not
a successful database health check**. Deprecated `firecrawl_extract` remains
hidden. [Capability test](../../firecrawl-selfhost/tests/mcp-local-capabilities.mjs),
[patch](../../firecrawl-selfhost/scripts/patch-mcp-reliability.mjs).

All 26 names are mapped below. “Read” means no deliberate target-site write; it
does not mean no local request/job logs, billing records, caches, or network
traffic. Conditional model use also depends on scrape options and engine
selection, so plain retrieval is not certified as universally LLM-free.

| Tool | Function and relevant boundary |
|---|---|
| `firecrawl_search` | Public web discovery; queries leave the machine through search backends. SearXNG aggregates external engines. Keep queries broad and non-identifying. |
| `firecrawl_scrape` | Retrieve a public URL; markdown/links are retrieval products, while `summary`/JSON and some processing paths can invoke a model. Page access may fail or return an interstitial. |
| `firecrawl_map` | Discover site URLs; broad limits can expand scope. Optional search/ranking can add model or search-backend dependencies. |
| `firecrawl_crawl` | Starts a persistent, potentially multi-page job. Bound pages, depth, domains, and formats explicitly. No crawl-cancel tool is in this 26-tool surface. |
| `firecrawl_check_crawl_status` | Read crawl state/results by owned job ID; inspect failed-page counts, not just the top-level success flag. |
| `firecrawl_parse` | Parse a file/URL; a local filename is an input transfer, not permission to upload protected data. Use a public fixture or public paper only. Requested output formats may add processing dependencies. |
| `firecrawl_research_search_papers` | External bibliographic discovery, chiefly OpenAlex with fallbacks. Metadata search is not exhaustive full-text retrieval. |
| `firecrawl_research_inspect_paper` | Resolve public identifiers and metadata through bibliographic services. Verify DOI/title/year and publication type. |
| `firecrawl_research_read_paper` | Fetch accessible public paper content and rank passages for a question. Scores are lexical retrieval scores, not model confidence. Missing passages do not prove the paper lacks the evidence. |
| `firecrawl_research_related_papers` | Citation/reference/recommendation retrieval using OpenAlex/Semantic Scholar, with local reranking. Ranking can favor the existing hypothesis. |
| `firecrawl_research_search_github` | Public repository/issue/README discovery through GitHub. Returns untrusted code/text, not permission to execute it. |
| `firecrawl_developer_search` | Public GitHub code/issues/repository search, with documented fallback paths. A fallback README hit is not an exact code-search match. |
| `firecrawl_agent` | Starts a model-backed scrape/search/synthesis job; sends collected content and prompt to the configured model provider and persists job data. |
| `firecrawl_agent_status` | Read that job's status/output; completion does not validate citations, scientific correctness, or cost accounting. |
| `firecrawl_feedback` | Writes endpoint feedback and related accounting to the configured database; only factual feedback on the actual owned retrieval job. |
| `firecrawl_search_feedback` | Same principle for search feedback; neither a retrieval tool nor scientific evidence. |
| `firecrawl_interact` | Opens/reuses an executable browser session. Deterministic read-only code can inspect a public page; natural-language instructions invoke an agent/model. No logins, submissions, cookies, or arbitrary downloaded code. |
| `firecrawl_interact_stop` | Stops the session identified by its scrape ID; cleanup does not erase all logs/history. |
| `firecrawl_monitor_create` | Creates persistent scheduled state. A nonempty goal implicitly enables LLM judging unless explicitly disabled. Do not leave a test monitor running. |
| `firecrawl_monitor_get` | Reads an owned monitor's configuration/state. |
| `firecrawl_monitor_list` | Lists available monitors; do not modify unrelated pre-existing monitors. |
| `firecrawl_monitor_update` | Mutates schedule, targets, retention, state, and/or notifications. Apply only to a monitor created for this task. |
| `firecrawl_monitor_run` | Enqueues a check with external retrieval and optional judging/notification effects. Rejects paused or already-running monitors. |
| `firecrawl_monitor_check` | Reads one check, pages, diffs and notification status; artifacts can involve configured object storage. |
| `firecrawl_monitor_checks` | Reads check history; inspect pagination and terminal status. |
| `firecrawl_monitor_delete` | Soft-deletes the owned monitor and clears the next scheduled run; not an immediate deletion of history, logs or retained artifacts. |

The exact names and intended request forms come from the sibling
[capability test](../../firecrawl-selfhost/tests/mcp-local-capabilities.mjs) and
[live-tool test](../../firecrawl-selfhost/tests/mcp-live-tools.mjs). Historical
`TOOL-COVERAGE.md` assertions are not fresh execution evidence. Its FireEngine
limitations and README's local-browser claims differ; determine support from the
actual bounded probe and returned errors, not by choosing the more optimistic
description.

## Model routing, evidence quality, and agent containment

README recommends the public model identifier
`accounts/fireworks/models/glm-5p3-flash` through the OpenAI-compatible
`https://api.fireworks.ai/inference/v1` endpoint. These are **documented defaults**,
not values read from the running service. `getModel()` substitutes `MODEL_NAME`;
`getModelFast()` prefers `MODEL_NAME_FAST`; an Ollama setting changes the default
provider. The provider argument can still explicitly select a different service.
[Routing implementation](../../firecrawl/apps/api/src/lib/generic-ai.ts).

The monitor judge is a concrete exception to “everything routes to GLM”: its
`googleModel()` calls `getModel(..., "vertex" | "google")`. The generic model-name
override does not turn that provider into Fireworks. An incompatible global model
name can therefore cause failure on this path. Do not enable judging merely to
exercise a tool, or report a failed judge as “no meaningful changes.”
[Monitor tuning](../../firecrawl/apps/api/src/services/monitoring/search/tuning.ts),
[judge](../../firecrawl/apps/api/src/services/monitoring/judgeChange.ts).

The patched research agent scrapes at most 10 supplied URLs and truncates
synthesis input at 400,000 characters. **If all those scrapes return no usable
content, it falls back to web search**, even if URLs were supplied: it searches
the first 200 prompt characters, then scrapes up to three results. There is no
domain allowlist in that fallback. A supplied-URL agent request is consequently
not a strict primary-source sandbox. It must return source references that are
checked independently; its generated summary cannot establish efficacy,
concentration equivalence, or the missing phase.
[Agent controller](../../firecrawl/apps/api/src/controllers/v2/agent.ts).

The research proxy's function named `similarity_semantic_score` uses token overlap
with title/abstract and bonuses for particular phrases including MVA, chromosome
missegregation, and spindle assembly checkpoint. Its passage ranker computes the
fraction of query words found in a passage. These are neither semantic embeddings
nor calibrated probabilities. It can omit short paragraphs, separate a table from
its explanatory text, or miss synonyms. Related-paper ranking is useful discovery,
but is not an independent test of the BUB1B/mechanism hypothesis. Search for
negative results, conflicting mechanisms, exposure limitations, and non-cancer
functional rescue separately. [Research proxy, ranking and passage extraction](../../firecrawl-selfhost/research-service/main.py).

The MCP output cap documented in README is 400,000 characters, with beginning/end
retention and a truncation notice. Missing middle content is not evidence of
absence. Archive the source identity and retrieval status, and inspect relevant
original sections/tables before updating a scientific ledger.

## Persistence, authentication, and lifecycle

The documented API binding is loopback because self-hosted mode disables hosted
database authentication. A reachable localhost API is not a user-authentication
boundary, and its internal `Bearer bypass` calls must not be copied into remote
authentication workarounds. Do not bind it publicly or change global MCP
configuration as part of this bounded integration. An API URL is not proof that
every downstream service is local. [README](../../firecrawl-selfhost/README.md),
[agent controller](../../firecrawl/apps/api/src/controllers/v2/agent.ts).

With `DATABASE_URL` configured, the patched database connection enables
persistence even when hosted authentication is off. Feedback writes
`search_feedback`, including notes, metadata, useful sources and query
suggestions. This is not intrinsically a message to Firecrawl support. However,
feedback also has conditional refund and error-reporting paths, so “local
feedback” is not a complete no-egress attestation. The configured database's
location was not read or independently verified by this source review.
[Database connection](../../firecrawl/apps/api/src/db/connection.ts),
[feedback storage](../../firecrawl/apps/api/src/controllers/v2/feedback/feedback-store.ts),
[feedback controller](../../firecrawl/apps/api/src/controllers/v2/feedback/record.ts).

Request metadata and query/options may persist. The local agent stores its prompt,
URLs, schema and output in `agent_jobs` and calls request logging with
`zeroDataRetention:false`. Browser-agent debug logs in non-production mode include
prompt, commands and outputs. Other source paths conditionally use GCS, PostHog,
Sentry and billing services. No claim of zero retention, absent telemetry, or
absence of other AI providers can be inferred from self-hosting. If this workflow
actually uses Fireworks or another model provider, update the **new Track 2 AI
disclosure** from execution evidence; do not retroactively alter the historical
Track 1 owner attestation.
[Agent](../../firecrawl/apps/api/src/controllers/v2/agent.ts),
[browser-agent logs](../../firecrawl/apps/api/src/lib/scrape-interact/browser-agent.ts),
[request/job logging](../../firecrawl/apps/api/src/services/logging/log_job.ts),
[PostHog](../../firecrawl/apps/api/src/services/posthog.ts),
[Sentry](../../firecrawl/apps/api/src/services/sentry.ts).

For a bounded monitor smoke test, use one public page, no webhook/email/Slack,
explicit `judgeEnabled:false` where supported, a distant valid schedule, a short
retention setting, and only the newly created ID. Poll the manual run to a terminal
state before deleting it. Deletion sets `status="deleted"` and `next_run_at=null`;
it does not itself demonstrate cancellation of already-dispatched work or physical
erasure of retained data. Verify the owned monitor is unavailable afterward and
record cleanup failures rather than swallowing them. The API rejects a manual run
while paused, so “create, pause, run” is not a valid sequence.
[Schema defaults](../../firecrawl/apps/api/src/services/monitoring/types.ts),
[controller](../../firecrawl/apps/api/src/controllers/v2/monitor.ts),
[store](../../firecrawl/apps/api/src/services/monitoring/store.ts).

For browser interactions use a literal, read-only inspection command, no
natural-language browsing agent, and an explicit stop in cleanup. For agents,
set a small public input and finite polling deadline; killing the MCP client is
not proof of cancelling an asynchronous server job. The 26-tool list has no agent
cancel tool, although the API checkout has a separate cancellation controller.

## Reproducibility and limits

Read-only review commands used `git rev-parse HEAD`, `git status --short`, `rg`,
`sed`, and `sha256sum` on the source paths above. No configuration execution was
needed. Selected SHA-256 fingerprints of inspected files:

| Relative source path | SHA-256 |
|---|---|
| `firecrawl-selfhost/tests/mcp-local-capabilities.mjs` | `33d5dbcaa565b687184b31e8ae1d8ea2ccb609621835fbc3eeeb08b142bf79e9` |
| `firecrawl-selfhost/tests/mcp-live-tools.mjs` | `19a890b7c7e07e262b315e90bd83387faed80f388c2672f41d924e554bdf31bc` |
| `firecrawl-selfhost/research-service/main.py` | `f218de3166af90ab7a866a1cd38d29d2f2a67fa955b5a7bc8f600d071dbb1524` |
| `firecrawl/apps/api/src/controllers/v2/agent.ts` | `fbd627bd64ed4aa6e79936f51f1a50f37decba1eb7fcec47a866cb54a6f01d4d` |
| `firecrawl/apps/api/src/lib/generic-ai.ts` | `b68726a8b0dbde4b8d4d64e89a0e3c0bd69932cc5eaa34682be10d0fd99dff55` |
| `firecrawl/apps/api/src/services/monitoring/search/tuning.ts` | `1e83489cc2b8055fac98ce6fa38b1894d5bb637edabe020e4f550a39501b79f5` |
| `firecrawl/apps/api/src/controllers/v2/feedback/record.ts` | `af779c9016f6478c2d840e9a92465e051d4527a974ede04c6051107027c8f787` |
| `firecrawl/apps/api/src/db/connection.ts` | `c3cf66cb37f31ec21d40800cf70cf5c68e109eb69a34ffacb3f42b7846932d19` |

This is a scoped capability/data-flow review, not a full security audit, provider
terms review, runtime packet capture, or verification of all model calls. The
main integration must record its own entrypoint/package hash, observed tool
schemas, actual results/errors, public input inventory, bounded costs and cleanup.
Using all tools is useful coverage only when each invocation has a legitimate,
bounded role; a successful smoke test is not new biological evidence.
