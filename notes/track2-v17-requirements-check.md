# Track 2 v17: independent requirements and editorial check

2026-09-24 · feat-009 · pre-freeze report review.

Reviewed `notes/track2-report-v17.md`, SHA-256
`12539a2b86150d8dc4da0d2b13c66363942744e0eaa825e2e692316d38828f7b`,
against the [independent official-source audit](track2-official-requirements-review-20260924.md),
the retained [v15 decisions](track2-evidence-v15.json),
[validation plan](track2-validation-v15.md), and
[falsification analysis](track2-falsification-analysis-v15.json).
No new external request, model inference, protected-data access or submission was
performed. This check evaluates the stated requirements, internal consistency and
presentation. It does not independently replicate the science, establish clinical
suitability, resolve distribution rights or predict the judges' decision.

## Finding

The draft is materially clearer for Track 2 review. It proposes an existing approved
medicine and a mechanism-grounded experiment without promoting everolimus beyond the
preserved optional mechanistic-probe disposition. Its opening makes the candidate,
question, first decision and current limits apparent before the computational history.
The current report text passes this bounded scope/content review, subject to the
delivery and integration items below; this is not an upload-readiness sign-off.

| Check | Result in the reviewed draft |
| --- | --- |
| Approved-drug task | Everolimus is explicitly the candidate. Existing approval and mTORC1 pharmacology are separated from MVA efficacy, safety and chromosome repair. Investigational tools are not presented as approved candidates. |
| No unsupported promotion | No rescue priority, unconfirmed phase, unmeasured endogenous function, no wet-lab experiment and null clinical exposure margin are retained. HCQ is reserve; pralatrexate is a conditional tumour-only horizon; other named dispositions match all eleven v15 decisions. |
| Scientific rigor, 35% | The variant-to-mechanism chain, indirect mouse bridge, separately qualified A/B hypotheses, positive and contrary drug findings, exposure distinctions and independent confirmation are explicit. The Balnis concentrations remain quarantined. |
| Potential impact, 25% | Both a useful positive result and a well-measured negative/harmful result have a stated research consequence. Neither is converted to promised clinical benefit. |
| Innovation, 25% | The contribution is the integration of genotype alternatives, falsification, complete fate accounting and decision rules. It avoids first-ever novelty and demonstrated-superiority claims. |
| Scalability, 15% | A proposed CPU review route is distinguished from optional heavy-model reproduction. Biological transfer requires fresh qualification. The 126-allocation illustration is explicitly not power, capacity or a laboratory quote. |
| Falsification accounting | The 12/12 primary ordering, 8/12 expanded-control failures and 11/24 negative retained-control scores agree with the retained analysis. The post-hoc and dependence qualifications remain. No software/model success substitutes for experimental evidence. |
| Synthetic illustration | The 20/80 versus 5/45 error fractions and 60/100 versus 40/100 useful-output fractions match the v15 counterexample and are explicitly labelled synthetic. Missingness bounds are distinguished from sampling uncertainty. |
| Template coverage | All eleven answers B7–B17 are present. Required B9 identifies providers/routes and distinguishes owner attestations from unverified handling settings. B17 has 249 whitespace-delimited words, below 500. |
| Acknowledgement and delivery | Full prescribed acknowledgement is present. Required report/GitHub/video deliverables, three-entry/latest-reviewed policy and remaining unknown quota are described accurately. A script is not called a recording. |
| Distribution wording | Omission of AF3/Atlas-derived numerical results and figures from this entry is described as a packaging choice, not a licence cure. Historical use is disclosed; notices remain; linked-history scope and eligibility are explicitly unresolved. |

Official basis: [Track 2 rubric](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/about.py),
[submission instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/submit_track2.py),
[rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/aeeef5ad49f51204a7439352e59e9d310aee5e9e/tabs/rules.py),
[methods workbook](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/resolve/aeeef5ad49f51204a7439352e59e9d310aee5e9e/static/templates/methods_description_form.xlsx).
The complete discussion-review counts are the main author's documented audit; this
second check did not independently reread the entire community archive.

## Actionable delivery findings

1. **Make evidence links portable.** Ten links in the reviewed report use relative
   filenames: ledger, validation, exposure, falsification review/register,
   website/discussion review, readiness note and two AF3 terms/notice files.
   A downloaded or portal-hosted Markdown/PDF report may resolve these against the
   wrong directory. Use absolute public GitHub URLs in the judge-facing report and
   exported PDF, preferably pinned to the final reviewed revision where practical.
   Local filesystem paths can remain in reproduction instructions.
2. **Verify the promised public route on its final files.** At this review's time,
   `scripts/track2_public_review_v17.py` and
   `notes/track2-owner-readiness-v17.md` had not yet been created. The main author is
   implementing them. Before freezing the report, run the documented CPU command
   from a public-data-only context and check every claim about what it validates.
   Do not confuse a current public evidence check with historical release-integrity
   checks or model inference. Confirm all promised links/files exist.
3. **Check the complete exported set.** This review did not inspect the unfinished
   eight-slide deck, workbook, PDF, narration or final release. Verify B7–B17 answers
   agree across report and workbook; the exported report contains the full methods
   disclosure and acknowledgement; the final deck/script preserve the same candidate,
   limits and decision rules; and measured recording duration includes the full
   acknowledgement. Passing text review does not establish rendering or runtime.
4. **Keep real delivery gaps explicit.** B9 honestly states unresolved provider
   handling settings. That is a transparent draft answer, not evidence that the
   required conditions are verified. Distribution scope, recorded/hosted video,
   owner review, live authenticated checks and submission receipt also remain open.
   Neither this review nor the shorter report resolves them.

No new factual contradiction with the retained v15 science was identified in this
bounded comparison. Primary-paper accuracy, legal compatibility, final file identity
and experimental feasibility still require their respective evidence; this review
does not replace them.
