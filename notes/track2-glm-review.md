# Track 2: expanded GLM literature review and adjudication

2026-09-09, session 38, feat-009; baseline `8efde23`. The request was more substantive
GLM research through Firecrawl, not another capability demonstration. The research and
scientific-critical-thinking skills shaped a two-layer workflow: model comparisons and
adversarial rereads, followed by independent checks against primary evidence. This is
a focused scoping review, not an exhaustive systematic review or clinical advice.

## What changes scientifically

The additional literature strengthens falsification and exposure checks; it does not
establish a treatment. Everolimus remains a conditional constitutional/pathway-first
research hypothesis and HCQ a reserve. Pralatrexate remains a fusion-positive RMS
tumour-only horizon. There is no new phase evidence, measured patient drug response,
clinical exposure margin, laboratory experiment or submission change.

| Research direction | Useful addition | Constraint that must survive into any later report |
|---|---|---|
| PP2A-B56 recruitment | An engineered localization rescue can be a mechanistic positive control. | Fixed-cell alignment under MG132 arrest is not proof of faithful daughter divisions. Proposed chemical PP2A mechanisms are disputed; isolated PR65 stabilization does not settle DT-061 specificity. |
| Senescence/proteostasis | Preserve cell-type, tissue and genotype effects rather than a generic anti-ageing label. | p21 protects muscle/fat but promotes the lens phenotype in the reported BubR1 model. Ercc1 senolysis is not BUBR1 rescue; HSP90 inhibition can oppose mutant-BUBR1 stability. |
| Readthrough | Compare positive insertion/function evidence with negative, sequence-dependent contexts. | Reporter activity, full-length protein and checkpoint/segregation function are separate gates. A barcode needs a translation-coupled readout; barcode abundance alone is not readthrough. |
| TBX compounds/niclosamide | Endogenous-target validation and two formulation-specific clinical exposure studies improve screening interpretation. | RMS potencies are micromolar, some EC50 estimates extrapolate beyond tested maxima, and sampled total plasma levels are not a matched unbound RMS exposure margin. |
| Hedgehog/azoles | Retain genuine tumour-growth inhibition and distinguish pathway position and tumour subtype. | Do not import medulloblastoma responses into RMS or repeat broad low-toxicity claims despite liver findings and official interaction warnings. |
| HDAC inhibitors | Preserve transient vorinostat case benefit, negative PDX endpoints, and model-dependent entinostat combinations. | Necrosis is not growth control; daily mouse and weekly human exposure profiles differ; unadjusted comparisons are not universal synergy. Entinostat has a specific Chinese approval, not a pediatric RMS indication. |

Exact sources, reading depths, favorable findings and contrary evidence are in the
[constitutional review](track2-glm-constitutional-review.md) and
[oncology review](track2-glm-oncology-review.md). Those independent reviews began with
ten primary-paper seeds each; oncology added two parent-selected follow-ups. These
are not twenty-two new discoveries or twenty-two completely read full texts. TBX
upgrades a previous abstract-only entry; posaconazole deepens a prior horizon.
Official labels/notices are separate documents, not additional experiments.

The jurisdiction correction is consequential: the NMPA announced entinostat approval
with an aromatase inhibitor for a defined adult breast-cancer setting in April 2024.
A blanket worldwide “unapproved” exclusion is wrong. RMS eligibility, exposure and
benefit still need separate evaluation. [Official NMPA notice](https://english.nmpa.gov.cn/2024-04/30/c_1049690.htm)

## What GLM does—and does not—establish

The actual returned model is `accounts/fireworks/models/glm-5p3-flash`, accessed by
`firecrawl_agent` / `firecrawl_agent_status` over the existing STDIO MCP connection.
Ten fixed dossiers cover PP2A, senescence, readthrough, SIRT2, mTOR, TBX, azoles, HDAC,
antifolates and redox interventions; six originally included an adversarial pass,
with a seventh mTOR repair pass added after the failed DOI lookup. Search
results are archived discovery leads, not automatically added evidence.

Local Firecrawl source inspection shows the agent scrapes up to ten URLs, concatenates
up to 400,000 characters, and makes one model call. It is not an iterative autonomous
literature-search agent. If all supplied scrapes fail it may search elsewhere; the
client cannot claim strict source containment or proof that each supplied source was
consumed. Multiple passes of the same model are not independent replication.

The first full-text-URL PP2A answer explicitly relied on training memory, misidentified
the structural method, and overclaimed completed division rescue. It is retained for
audit but rejected as a source-grounded synthesis. A completed transport job is not a
successful scientific review. The initial senescence job failed retrieval. Neither
failure was hidden or treated as negative biological evidence.

The recovery route uses Europe PMC **indexed primary abstracts/metadata**, mapping
the same paper by PMCID, PMID or DOI. Official label/notice URLs are retained. A
successful XML scrape separately demonstrated public text availability, but did not
make the model's abstract-only analyses full-text reviews. No CAPTCHA was bypassed.
An unavailable source in one run is not proof that it is paywalled or nonexistent.

An unquoted parenthesized DOI returned zero records for ARST1431. The corrected
quoted DOI query resolves PMID38936378/PMC11550893. This was a query defect, not
missing clinical evidence; the independently verified baseline already included
the negative randomized comparison. The fixed runner quotes DOI field values.

### Additional mTOR adjudication

The first abstract-based mTOR answer appropriately withheld invented trial numbers
but proposed the wrong genotype comparison and overstrong exclusion criteria. Its
`H/L1002P` animals are not monoallelic carriers; the published mTOR-positive muscle
comparison was `+/X753` versus `+/L1002P` and wild-type. The paper did not test
rapalog rescue. A pathway can be a modifiable secondary driver, so late emergence
or non-exclusive activation is not by itself an automatic rejection of intervention.
Function, exposure, injury and completed cell-fate outcomes remain the decisive
proposed gates. [JCI primary study](https://www.jci.org/articles/view/126863)

The slippage signal must retain its human tumour-cell/mitotic-arrest context and
denominator; it does not measure patient or deficient-normal risk. ARST1431 found
no significant EFS improvement with added temsirolimus; that limits a tumour claim
but does not directly test everolimus constitutional rescue. The corrective GLM pass
is checked against these independently established facts, not counted as new evidence.
[Slippage primary Results](https://www.sciencedirect.com/science/article/pii/S258900422101645X),
[ARST1431 primary trial](https://www.sciencedirect.com/science/article/pii/S1470204524002559)

The completed mTOR challenge recovered the correct trial identity and main comparison,
corrected the carrier/disease-model distinction, and retained the explicit abstract
versus secondary-reviewer boundaries. It still needs narrowing before reuse:

- Calling temsirolimus simply an IV prodrug is incomplete: the parent inhibits mTOR
  through FKBP12, while sirolimus is an active metabolite. Preserve parent/metabolite
  exposures rather than treating the parent as inactive. [Official TORISEL label, sections 12.1/12.3](https://labeling.pfizer.com/showlabeling.aspx?id=490)
- The nonsignificant trial result is not proof of exact zero effect; adverse-event
  percentages are descriptive, and missing abstract biomarkers do not prove no
  biomarker substudy exists. Its chemotherapy context is not a direct estimate of
  constitutional-treatment safety.
- Static metaphase cytogenetics cannot identify a slippage history. Live cell-fate
  tracking is a separate measurement; absence of detected injury needs an explicit
  detection limit and precision, not a claim of absolute zero risk. Mouse experiments
  do not inherit human toxicity-grade thresholds without a species-appropriate plan.
- directSLiMS remains an engineered perturbation, not evidence of therapeutic rescue.
  Source-index MeSH annotations are not reliable substitutes for its construct or
  inducer Methods. The prior selected-section review already establishes the inducer
  and orthogonal dimerizer control; the model's abstract-access gap does not erase it.

No additional reruns are needed to force model agreement. The reviewed corrections,
not the raw proposals or a majority vote, govern any future report integration.

Independent reviewers inspected available primary sections/abstracts separately and
recorded exact retained, narrowed, corrected or rejected model claims. Adversarial
prompts include clearly labeled secondary reviewer counterchecks, not an assertion
that the model personally read those full-text sections. Some prior answers exceed
the MCP's 10,000-character prompt limit: revised challenges use explicitly marked
head/tail excerpts and archive the full prior hash, selected length and omission flag.
Those are partial prior-answer audits, not complete line-by-line rereviews.

## Reproducible workflow and preservation

The fixed public plan is [track2-glm-plan.json](track2-glm-plan.json); the runner is
[track2_glm_review.py](../scripts/track2_glm_review.py), importing the unchanged,
previously reviewed MCP bridge. Each normal CLI run records its executed runner, original
and effective plans, hashes, prompts, URLs, job IDs, expected/returned model, terminal
state and proposals. Raw model proposals stay in ignored `results/`, not the report.
The old full-text run, diagnostic/recovery artifacts and rejected prompts remain
available locally; repeated queries are not counted as independent papers.

## Final execution and verification record

The live final status audit found **19 unique accepted service jobs: 18 completed
with the expected GLM model and one failed with `no_content`; all are terminal**.
The eighteen completions comprise ten abstract-based topic reviews, seven
adversarial/corrective passes, and the initial rejected PP2A training-memory answer.
Completion is not scientific acceptance. Six overlong prompts were rejected by the
MCP's pre-execution 10,000-character schema and created no job IDs; their conservative
historical `unknown_start` records are clarified by that schema audit, not erased.

The current plan contains 35 distinct source URLs (31 paper/locator records and
four official labels/notices). Those are supplied sources, not proof of successful
reading or thirty-five newly discovered studies. Independent follow-ups also checked
a PLOS correction, EMA's status page and the TORISEL label; these are not new trials.

All paths below are under ignored `results/feat009/`:

| Artifact | Outcome |
|---|---|
| `glm-literature-v1/` and `glm-literature-pp2a-recovery/` | First full-text-URL attempt interrupted after identifying a failed-state polling defect; same PP2A job recovered without a duplicate start. Its answer is rejected as source-grounded evidence. |
| `glm-literature-abstracts-v2/` | Nine completed reviews; CLI exit 2 because five original long challenges failed schema validation. Do not relabel this run entirely successful. |
| `glm-literature-pp2a-abstract-v3/` | PP2A abstract comparison plus bounded challenge; exit 0. |
| `glm-literature-constitutional-challenges-v3/` | Senescence/readthrough counterchecks; exit 0. |
| `glm-literature-mtor-challenge-v3/` | Quoted-DOI clinical-trial repair and genotype correction; exit 0. |
| `glm-literature-oncology-challenges-v3/` | TBX/azole counterchecks; exit 0. |
| `glm-literature-hdac-challenge-v3/` | HDAC countercheck; exit 0. |
| `glm-literature-final-job-audit/audit.json` | Live terminal-state audit of all nineteen identified jobs and six schema rejections. |
| `glm-literature-final-job-audit/proposal-inventory.json` | Final eighteen proposal paths/hashes; 32,437 generated words, not 32,437 verified words. The earlier audit captured seventeen files before waiting for the final job; this later inventory closes that timing gap. |

Executed runner/plan snapshots are retained because fixes and reviewer counterchecks
were added during the session; the final source is not claimed to be the exact version
that produced every earlier artifact. One-off status/recovery checks use the unchanged
bridge and `agent_round(existing_job_id=...)`; the original creation runner remains
in `glm-literature-v1/executed-runner.py`. No model agreement was forced by unlimited
reruns. Independent notes adjudicate five constitutional reviews/three challenges
and five oncology reviews/three challenges; the two mTOR outputs are adjudicated here.

The mTOR proposal hashes are `45b365e66d179a7b1f776c5f9e27f8d80e3fbd78499c82df5c35c3a6936f0b0b`
(initial abstract review) and `fa08562b5aa98452cfc8e6ace47da48413532f6a000b9e2b3bbc91148d1c1d0c`
(repair pass). Remaining proposal hashes are in the independent notes and final inventory.

The 67 new offline tests and 300 existing tests pass (367 total). Fresh no-argument
`./init.sh` exits 0; real output is recorded in `progress.md` and
`logs/track2-glm-final-init.log`. Track 1 v4, Track 2 v2 and Track 2 v3 preservation
checks pass. No live literature/model job or MCP child remains. Publication audit
results and final commit/push verification are recorded in the session log.

```bash
# Use NEW output names; existing run directories are never overwritten.
uv run python scripts/track2_glm_review.py results/feat009/glm-literature-new-run --abstract-records
uv run python scripts/test_track2_glm_review.py
uv run python scripts/track2_evidence.py track1
uv run python scripts/track2_evidence.py verify results/feat009/jvv7_track2_research_v2
uv run python scripts/track2_release.py verify results/feat009/jvv7_track2_research_v3
./init.sh
```

The `--challenge-only` recovery mode accepts only this session's fixed own public
`glm-literature-abstracts-v2` review directory, checks proposal hash/model/completion,
and requires explicit challenge-enabled dossier IDs with `--abstract-records`.
It does not accept arbitrary files or prompts. Running it invokes an external model;
tests are offline and invoke no service. A polling timeout does not cancel a server
job; two local workers do not guarantee at most two outstanding server jobs after
timeouts or across separately launched recovery runs.

No `.env`, API key, raw subject record, protected narrative or exact patient query was
used. Self-hosting does not imply local inference or zero retention: public prompts
and outputs may persist in the local service and be processed by Fireworks. No new
monitor, browser session, global configuration, unrelated service or repository
visibility change was needed. No statement extends the owner's OpenAI settings
attestation to Fireworks. Existing v3 disclosure already names this provider.

Track 1 v4 and Track 2 v2/v3 report/pitch/packages and their current-input-bound files
remain unchanged. This supplement must be reviewed before any later v4 integration;
it is not a replacement upload. Feat-009 remains in progress for the recorded/hosted
pitch, final live submission checks and receipt. Trans phase remains unconfirmed.
