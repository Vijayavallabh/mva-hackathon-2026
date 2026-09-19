# Track 2 v4: integration, adversarial review and delivery gates

2026-09-19 · Session 40 · feat-009 · baseline `e7aee96`.
The owner authorized the recommended next step: integrate reviewed evidence, sharpen
validation, and prepare matching pitch materials. This is not authorization to upload,
treat, acquire samples, contact the family or send protected subject content externally.

## Outcome and artifacts

- `track2-report-v4.md`: standalone synthesis with explicit positive/negative evidence.
- `track2-evidence-v4.json`: 32 source records, 11 fixed research decisions. This is a
  focused integration layer, not 32 new papers or an exhaustive replacement for the
  historical 53-source/12-candidate ledger. Reading depth is cumulative archived review;
  the separate primary-review note records September 19 rechecks specifically.
- `track2-validation-v4.md`: consolidated proposed assays, endpoints, statistical units,
  exposure requirements and stop rules. No assay has been performed.
- `track2-pitch-v4.md`: five-part narration, recording instructions, description/credits
  and expected questions. **336 words / 112 words per minute** is a planning estimate,
  not a recording or a measured three-minute duration.
- `track2-slides-v4.html`: five static, locally rendered 16:9 slides; no external assets,
  fonts, image-generation calls or additional model provider.
- `track2-v4-primary-review.md`: independent bounded primary-source/content review.
- `scripts/track2_release_v4.py` and its tests: separate offline v4 snapshot checks,
  preserving current-input-bound v2/v3 and the existing Track 1 files.
- `scripts/render_track2_slides.mjs`: local fixed-deck preview, source/code hashes,
  explicit browser viewport, text-boundary checks and owned-browser cleanup.

The research and scientific-critical-thinking skills prompted independent primary checks
and a distinction between evidence and interpretation. Scientific-slides guidance prompted
the timed outline and image-based visual review. Its optional remote generation/lookup
routes were not used: no extra provider was authorized or needed. Existing archived
sources plus bounded built-in web checks supplied the citations.

## Scientific devil's-advocate revisions

| Challenge | Resolution carried into v4 |
|---|---|
| Is the mouse pathway result pair-specific drug rescue? | No. Original p70S6K/4EBP1 readouts, different alleles, depicted two-animal blot groups, lack of randomization/blinding and absence of rapalog intervention are explicit. Proposed pS6 is labelled future work. |
| Does PP2A recruitment prove a chemical treatment? | No. MVA-cell engineered alignment rescue and HeLa pharmacological perturbation remain separate. Faithful completed division is not inferred from metaphase alignment. |
| Does the new PR65 paper lack binding data? | No. The independent rereview verifies ensemble binding as well as stabilization. This still does not settle DT-061 specificity or establish MVA rescue. |
| Must downstream mTOR mitigation repair chromosomes? | Not necessarily. A qualified lineage-function endpoint can be selected before screening; unchanged segregation with useful downstream improvement is not called chromosome repair. Segregation and division remain safety guardrails. |
| Do first-event categories omit daughters that later die? | Corrected. First accurate/error division is classified separately from subsequent daughter survival; the composite useful-division endpoint retains late death and missing tracks. |
| Is a limited alignment control useless without complete rescue? | No. It can qualify the alignment endpoint; a stronger segregation-rescue claim needs completed divisions and viable daughters. |
| Does China approval make entinostat an RMS lead? | No. Its actual jurisdiction-specific approval is retained alongside model, schedule, multiplicity and exposure gaps. No blanket worldwide nonapproval claim. |
| Do positive model summaries resolve uncertainty? | No. Archived GLM completions remain proposals; rejected claims and retrieval limits are preserved. No new paid/model run was launched to force agreement. |

The independent scientific agent reviewed the report, validation, ledger, pitch and HTML
content, found no remaining material source-number contradiction or unsupported promotion,
and documented its scope. Main author applied the recommended citations/provenance polish.
This is a bounded review, not universal proof that every sentence or source is error-free.

Everolimus remains the sole conditional constitutional priority, HCQ reserve, pralatrexate
an optional tumour-only horizon. No exact-pair efficacy, clinical exposure margin or
phase confirmation follows. Engineered cis/trans controls do not resolve subject phase.

## Independent implementation/standards review

The second reviewer inspected the additive release implementation and new content against
the baseline and repository rules. Findings corrected before freeze:

1. Python `False == 0 == 0.0` could hide forged manifest-summary types. Strict JSON
   comparisons now distinguish them.
2. A static-deck guard initially rejected the deliberately restrictive CSP and missed
   entity-encoded CSS resource loads. It now permits only the exact conservative policy
   and rejects active/resource-loading constructs, duplicate attributes and redirects.
3. The initial pivotal-role rule incorrectly scoped the HCQ reserve as constitutional.
   The validator follows the scientific decision: tumour reserve. All eleven IDs,
   scopes and decisions are now frozen; omission/addition/promotion requires a new design.
4. Renderer DNS blocking alone was not a network prohibition. A dead loopback proxy,
   target HTTP(S)/WebSocket blocking, script disabling and restrictive CSP now supplement
   a minimal browser environment and fixed local file.
5. Renderer shutdown now targets only its own detached process group with bounded
   termination/kill and direct-child wait. Protocol decode/shape failures propagate through
   awaited errors. Start/end source and renderer hashes detect drift during execution.

The renderer records its isolated retained temporary profile in `render.json`; it contains
only public-deck browser state, not credentials or subject inputs. No unrelated browser
profile/process is touched. These controls do not turn a browser into a general-purpose
security sandbox for arbitrary protected input.

## Verification and visual review

The existing eight relevant test suites pass **367 tests**. The new v4 suite passes
**72 tests**, for **439 total**. Tests cover structural/semantic guards and synthetic
tampering, not biological efficacy. Renderer syntax checks and five actual local captures
supplement them. Exact logs and final build/verification results are in `progress.md`.

The first direct Chrome CLI previews were clipped/blank because of viewport/fragment
capture behavior; they were not accepted as slide validation. The explicit-viewport CDP
renderer produced all five complete 1280×720 screenshots with zero text-boundary violations.
Manual inspection still caught a slide-3 content/reference overlap: shortening the title
fixed it. Slide-4 spacing was also improved. This illustrates why geometric checks alone
are insufficient. Main author inspected every slide and the corrected slides again.

Final source-matched captures and renderer/browser hashes are in
`results/feat009/v4-slide-review-audited-20260919/`; earlier preview attempts remain historical.
The text palette's calculated WCAG contrast ratios are **at least 8.49:1** on both used
backgrounds; body/support text is at least 24 CSS pixels. Runtime, voice clarity, projector
behavior and hosted playback require an actual recording and owner review.

Fresh `./init.sh` passed. An earlier sandboxed repeat failed DNS during remote manifest
lookup; the network-enabled rerun succeeded. This was not evidence of corrupted subject
data and did not trigger a redownload. Actual output is in
`logs/track2-v4-final-init-network.log` and copied into the session log.

V4 snapshot commands (a new directory only; do not rebuild over existing output):

```bash
uv run python scripts/test_track2_release_v4.py
node --check scripts/render_track2_slides.mjs
node scripts/render_track2_slides.mjs NEW-REVIEW-NAME
uv run python scripts/track2_release_v4.py build results/feat009/jvv7_track2_research_v4
uv run python scripts/track2_release_v4.py verify results/feat009/jvv7_track2_research_v4
```

The snapshot contains 25 copied support/delivery files plus its manifest and binds 44
inputs. It includes historical v3 support for provenance; **the intended new report is
`jvv7_track2_report_v4.md`**, not the older report also present in the archive. The directory
is a research snapshot, not a request to upload all its files. PNG previews are separately
hashed review artifacts. Hash checks are not signatures, truth checks or clinical clearance.

## Provider and submission gates

The owner answered the Fireworks disclosure question with “just api credits.” Record
**owner-confirmed credit-based API usage**, not an inferred paid tier, no-training policy
or zero-retention promise. Training and retention settings remain unverified; no key was
requested or printed. OpenAI's earlier owner-attested no-training setting does not extend
to Fireworks. Atlas precomputed-output use/terms remain disclosed. K-Dense installation
alone did not add inference evidence.

The official public Track 2 submission-tab source was re-opened on September 19: report,
GitHub URL and a three-minute YouTube/Vimeo pitch are required, with provider/tier/data
handling in methods. Only the latest entry is reviewed. The current config endpoint was
unavailable to the web tool; the previously verified three-entry limit is historical,
not a newly verified remaining quota. No login, submit callback, upload or receipt occurred.
[Official tab](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/raw/main/tabs/submit_track2.py)

Remaining gates: actual video/hosted playback; Fireworks settings verification; owner
review; live rules/public visibility/purge/disclosure and authenticated quota checks;
authorized portal submission and receipt archival. The package deliberately reports
`upload_ready: false`, `provider_settings_verified: false`, `video_url: null` and
`upload_performed: false`. Scientific unknowns are openly stated proposal limitations,
not reasons to fabricate experiments or repeatedly rerun computational phase work.
