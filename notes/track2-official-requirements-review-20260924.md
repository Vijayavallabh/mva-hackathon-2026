# Track 2: independent official-requirements review

2026-09-24 · feat-009 · requirements and presentation audit of the v16 baseline.
This bounded review read primary public materials independently of the main author's
discussion audit. It is not an organizer decision, scientific replication, legal
opinion, account audit or prediction of a judging score. It changed no submitted or
historically bound artifact.

## What was actually checked

Anonymous public Space metadata and the running Gradio `/config` were retrieved on
September 24. Both metadata and runtime identify revision
`aeeef5ad49f51204a7439352e59e9d310aee5e9e`, last modified September 22 at 05:10:02 UTC.
The running app was `RUNNING`. Read `README.md`, `app.py`, `config.py`, About, FAQ,
rules, Track 2 submission code, and the Track 2 methods worksheet at that revision.
No downloaded Python was imported or executed; workbook strings and layout were
read from ZIP/XML without evaluating formulas. Live rules and submission instructions
match their pinned source strings exactly after trimming surrounding whitespace.
[Space metadata](https://huggingface.co/api/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026),
[running public configuration](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/config),
[pinned app](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/app.py).

Compared with the earlier `1c761cc23d90aebe6a011fd5b0b99517df42408c` cache, About,
FAQ, Track 2 submission code, configuration, README and workbook have identical
hashes. The inspected rules change corrects a spelling error in the public-sharing
paragraph; it does not change these requirements. This is a comparison of the named
files, not a claim to have audited every changed file in the repository.

The main author separately reviewed the complete current discussion listing and
threads. This note does not claim an independent reread of every discussion and
does not turn participant suggestions into organizer requirements.

## Requirements that affect the entry

The official task is an approved-medication hypothesis grounded in the disrupted
mechanism. It expressly permits proposals for investigation without demonstrated
efficacy. A cautious everolimus hypothesis can therefore fit the task; the panel
still has to find its indirect mechanistic bridge persuasive. No wet-lab result or
fixed slide count is required in the inspected materials. [About](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py),
[rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/rules.py).

| Item | Verified requirement or distinction | Consequence for this revision |
| --- | --- | --- |
| Scientific rigor | 35%; sound variant mechanism and a drug rationale supported by it. | Put the mechanism-to-intervention chain and its weakest link before the model inventory. |
| Potential impact | 25%; conditional contribution to MVA understanding or diagnosis for this child or others. | Explain what a positive or negative experiment would change. Do not substitute a promised clinical response. |
| Innovation | 25%; creative angle, method or tool. | Explain the contribution of complete cell-fate accounting and falsifiable advancement decisions. Model size is not itself demonstrated innovation. |
| Scalability | 15%; realistic applicability beyond the single case. | Show the portable evidence/gate workflow and the model-specific work that must be repeated. |

Rubric source: [About, Track 2 scoring](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py).
The presentation consequences above are reviewer recommendations, not extra official
conditions or a self-score.

The portal requires a report, a GitHub URL and a recorded pitch. The report is PDF
or Markdown and should contain participant/team identity in its filename. The
instructions specify a three-minute YouTube or Vimeo video. The callback checks
the report suffix, GitHub prefix and presence of a video URL; these limited software
checks do not validate recording length, access permissions, scientific quality or
compliance with the written instructions. The repository must contain reproducible
scripts/configuration. Methods details are recommended; AI provider, plan/tier and
handling-setting disclosure is required when applicable. Team/display name and
notes for judges are optional. [Submission instructions and callback](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/submit_track2.py).

Three Track 2 entries are allowed and only the latest is reviewed. One designated
team member should submit. Remaining quota was not queried. The FAQ permits a
private repository during the competition but requires public access afterwards;
this project's stricter public-first policy remains in force. [FAQ](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/faq.py),
[quota constant](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/config.py).

The full prescribed acknowledgement applies to public communications. Retain it
legibly inside the video and in report/description, rather than relying on a link
to its text. There is no live Q&A, so the recording and report need to stand alone.
The data restrictions, deletion requirement and publication embargo are unchanged.
[Rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/rules.py).

## Template details and inconsistent wording

The Track 2 worksheet spans `A1:B17`. Prompts are `A7:A17`; answer cells are
`B7:B17`, without merged answer cells. They cover team name, approach, AI disclosure,
automation, manual curation, public/proprietary source scope, source descriptions,
variant mechanism, time/effort and a method abstract of at most 500 words. The AI
answer belongs in `B9`; the abstract belongs in `B17`. A completed workbook is a
useful working artifact, but the current uploader accepts the exported PDF/Markdown
report rather than an `.xlsx` upload. [Methods workbook](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/resolve/aeeef5ad49f51204a7439352e59e9d310aee5e9e/static/templates/methods_description_form.xlsx),
[accepted report extensions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/submit_track2.py).

The workbook retains older one-final-entry wording. The FAQ's team paragraph also
uses singular wording, while its dedicated quota paragraph, current instructions
and configuration specify three updates with the latest reviewed. Treat one team
submitter and one finally reviewed entry as distinct from three permitted uploads.
Do not create additional accounts or infer unused quota from this review.

The About timeline closes submissions on **24 October 2026 at 23:59 UTC**, gives
October 24–November 24 as judging, and lists November 25 for winners. Rules,
submission text and FAQ instead describe roughly two to three months of judging
and a later announcement. Preserve the closing deadline; describe the announcement
timing as inconsistent rather than promising November 25. [About timeline](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py),
[FAQ](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/faq.py).

## Changes that improve the v16 presentation

These are editorial and implementation recommendations. They do not promote a
candidate, replace the v15 scientific decisions, or weaken the falsification rules.

1. **Make the proposed medication and decision easy to find.** Lead with the
   approved everolimus hypothesis, its mTORC1 target, and the conditional question of
   useful non-cancer function. Explicitly show which arrows from BUB1B dysfunction
   to pathway phenotype are established at gene level, indirect, or unmeasured for
   this pair. An honest optional probe is stronger than a framework that appears
   to avoid proposing any medication.
2. **Condense computational history.** The v16 pitch spends 44 planned seconds on
   sequence/structure/DNA caveats before the drug evidence. A single evidence-limit
   panel can explain why models cannot select treatment, while the full primary
   and secondary control results remain in a linked technical appendix. Preserve
   the 8/12 expanded-control failures, 11/24 negative retained-control scores and
   post-hoc qualification wherever that analysis is summarized. Do not imply an
   independent model consensus or hide earlier failed controls.
3. **Show balanced evidence as a decision.** Pair the motivating observations
   with the strongest contrary studies and state exactly how they changed the
   plan. Keep compounds, tissues, doses and outcomes separate. The disputed Balnis
   concentration remains quarantined. A tumour trial cannot settle constitutional
   rescue, and a smaller abnormal-survivor fraction cannot establish benefit.
4. **Spend the recovered pitch time on the experiment.** Show model qualification,
   one prospectively selected mechanistic branch, function and complete cell-fate
   outcomes, matched deficient-normal safety, exposure and independent confirmation.
   Unknown means hold; demonstrated safety failure stops that tested context; all
   requirements passing permits further preclinical review. Use one readable
   decision diagram rather than narrating every assay.
5. **Make feasibility and scalability concrete.** Separate ordinary offline
   evidence/gate verification from optional heavy model reproduction. Demonstrate
   reuse on explicitly synthetic counterexamples without calling them experiments.
   Bring the existing validation plan's staged resource arithmetic into the main
   report: seven groups × three clones × three days × two conditions is 126 culture
   allocations before dose expansion and extra controls. This is an illustrative
   workload, not a powered sample size, available cell collection, cost quote or
   promised timeline. New diseases still need new biological qualification.
6. **Give judges a short entry point.** Put candidate, rationale, strongest
   challenge, decisive experiment and four rubric contributions in the report's
   opening pages. Keep an evidence index and technical appendix for auditability;
   do not bury the proposal beneath the history of tool execution. The methods
   answers and full disclosure must remain readily accessible.
7. **Align every current artifact.** V16 section 8 still labels itself a v15
   report and its linked deck as v15. Correct these in a new version, preserve
   historical files, use participant-named exports, and check report/deck/transcript/
   workbook/description links and narration together. A script is still not a
   recording, and planned timings are not measured video duration.

Baseline inspected: [v16 report](track2-report-v16.md),
[v16 slides](track2-slides-v16.html), [v16 narration](track2-pitch-v16.md),
[v15 validation](track2-validation-v15.md). The existing rubric table and extensive
falsification are strengths; this revision should improve their visibility and
decision value rather than manufacture stronger efficacy evidence.

## Submission reuse and model-output terms: a concrete scope ambiguity

The About page includes submissions, code and reports in its CC BY 4.0 statement;
the FAQ includes predictions/code/reports, and the rules permit organizer reruns
and describe submissions as CC-BY. The linked repository is a required deliverable.
The inspected materials do **not** define whether every historical or unrelated
file in that repository is part of the submitted entry, or describe a specific
exception for third-party model-output restrictions. The Space README's own licence
metadata does not by itself resolve that question. [About](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py),
[FAQ](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/faq.py),
[rules, Submission Reuse](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/rules.py).

AlphaFold3's current published Output Terms include substantially derived
descriptions and summaries in their scope, impose use restrictions, require
notices and citation, and prohibit conflicting additional terms. The local
[notice](alphafold3-Legally-Binding-Terms-of-Use.txt) already identifies confidence
summaries, RMSDs and explanatory text as derived analyses. This is directly relevant
to the v16 report and deck; deleting coordinate files alone would not remove all
material identified by those terms. Model-parameter recipients' use is governed by
the parameter terms, while the distributed output notice remains relevant to
recipients. [Official AlphaFold3 Output Terms](https://github.com/google-deepmind/alphafold3/blob/main/OUTPUT_TERMS_OF_USE.md),
[preserved local terms](alphafold3-output-terms.md).

AlphaGenome is also directly implicated: v16 contains merged-splicing values and
feature-attribution interpretation. Current rendered service terms distinguish the
permissive **AVI Score** from the **AVI Score Feature Breakdown**, and cover
precomputed datasets. Other output/derivative restrictions and notice obligations
remain. The output terms require retaining use restrictions when additional terms
are supplied. Do not treat every Atlas result as unrestricted merely because AVI
scores have a stated exception. [AlphaGenome service terms](https://deepmind.google.com/science/alphagenome/terms),
[output terms](https://deepmind.google.com/science/alphagenome/output-terms).

**Factual conclusion and bounded recommendation:** do not label the entire mixed
package as newly relicensed, unrestricted CC BY. Preserve the existing output
notices and clearly identify the exact proposed submission files and their source
conditions. A new entry can technically omit AF3/Atlas-derived results while
preserving labelled historical work, but that alone does not establish that the
organizers exclude linked history from their reuse requirement. Nor has this
review established that a mixed-terms entry is rejected. The inspected sources
leave that scope unresolved; this note makes no legal eligibility determination
and authorizes no organizer contact or acceptance of new terms.

## Provenance and reproduction

Independent raw responses and per-file URLs, response status, byte counts and
SHA-256 values are in
`results/feat009/official-requirements-independent-20260924/manifest.json`.
All ten public GETs succeeded: metadata, live configuration and eight pinned files.
`live-source-comparison.json` records the two exact source/component comparisons.
The live config contains 86 components and ten dependencies; none of the callbacks
was invoked. `track2-template-extracted.txt` records all Track 2 worksheet prompts.
A separate bounded duplicate source fetch is retained at
`results/feat009/official-requirements-bounded-20260924/`; its eight files agree.

| Artifact | SHA-256 |
| --- | --- |
| Space metadata | `d60b1bd4abf23e63aac56bd8c819a8e68a928ba134c0a50780193b0a6a4da30f` |
| Live configuration | `d725d66194ae9ae98621d194b2fcf126e1545e1cc1e3d2b9be2dda1554eaa261` |
| About | `1867b07f24d987fbb728c756c2d2bc4ab5f302d7c7804f53fe7b6a8b4c83ae43` |
| Rules | `0031b61f710ce5bcc686a88e4fcd470b165f25ed103f970827b6ebfed097ab12` |
| Track 2 submission code | `f48d576ab052df34527222b7693f956e15e5376ef68eddedcf0c4f04736bf65c` |
| Methods workbook | `61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441` |

The existing read-only public-page collector can reproduce the source/configuration
part in a fresh directory without modifying a historical release:

```bash
uv run python scripts/track2_challenge_review.py results/feat009/new-official-page-review
```

Text-only web access returned the Gradio shell or failed on API URLs; direct
anonymous GETs supplied complete public responses. AlphaGenome's text-only pages
likewise showed an application shell. Separate isolated temporary Chrome profiles
rendered the two official terms pages without login, agreement acceptance or API
inference; those browser processes exited. Their current DOM/text and manifests
are in the independent cache. Output-terms DOM SHA-256 is
`84f7df3bb31201a9455c637edcda21eed8d69554281e6725b3aa1e3a9a116a5c`;
service-terms DOM SHA-256 is
`336043054319dace149e77f8a897703328ed62769abd81554c72835d000ecea8`.
Current operative terms were read; older rendered caches were used only to locate
the relevant clauses. No protected files, `.env`, account authentication, model
inference, upload, submission or family contact were involved.
