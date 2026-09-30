# New CRISPR evidence strengthens the HT29 qualification lead

The new analysis supports **HT29 as a place to qualify a BUB1B assay**. It does not
qualify HT29 as a non-cancer MVA model or establish a rescue drug. Everolimus remains
an optional model-qualified mechanistic probe; HCQ remains reserve. Phase, endogenous
allele effects and clinical exposure margins remain unresolved.

All eight owner-host H100s completed the [fixed-plan campaign](track2-crispr-plan-v25.json).
It closes a specific gap in the older v23 panel: newer public data contain BUB1B
CRISPR profiles. The [source review](track2-crispr-sources-v25.json) records discovery,
contrary evidence and reading limits. This is GPU-accelerated statistics, not new
neural inference or an experiment performed by this project.

## What changed

The Broad LINCS2020 files contain 140,945 CRISPR treatment profiles, 1,956 controls
and 720,216 compound profiles. Exact-ID joins leave no unannotated matrix columns.
We used 978 directly measured genes. The 31 BUB1B profiles span 19 cell contexts but
use **one guide ID, BRDN0001148077**. Their underlying wells do not overlap one another
or the frozen v23 dataset. Different batches still repeat the same guide, and the
RNAi side reuses v23 experiments.

HT29 is the strongest BUB1B concordance result among the five shared RNAi/CRISPR
contexts. Both retrieval directions matter: finding BUB1B among RNAi targets does
not guarantee that the RNAi profile identifies BUB1B among CRISPR targets.

| Cell | Raw RNAi–CRISPR correlation | PRIME RNAi–CRISPR correlation | PRIME rank among RNAi targets | PRIME rank among CRISPR targets |
|---|---:|---:|---:|---:|
| A375 | 0.3430 | 0.2144 | 159 / 3,826 | 827 / 5,119 |
| A549 | 0.2063 | 0.2084 | 74 / 3,724 | 443 / 5,137 |
| **HT29** | **0.3539** | **0.3712** | **4 / 3,665** | **4 / 5,113** |
| MCF7 | −0.0974 | −0.0887 | 2,860 / 3,471 | 3,839 / 4,274 |
| PC3 | −0.0356 | −0.0293 | 3,525 / 3,822 | 4,032 / 5,113 |

Removing the measured BUB1B transcript leaves HT29's PRIME correlation at 0.3693
and both ranks at fourth. Its two CRISPR batches correlate at 0.3594 and retrieve
the same guide first in both directions. Across all nine repeat-batch BUB1B contexts,
only 2/30 directed retrievals rank first; both are this HT29 pair. Those 30 retrievals
reuse 15 pairwise correlations. One of the two HT29 profiles fails the declared
quality filter, and both use the same guide. This is a **qualification lead**, not
independent-guide validation. The distinct v19 five-reagent and v23 six-reagent
RNAi findings remain unchanged.

The genome-wide benchmark prevents reporting only the favorable target: 8,623/57,044
directed cross-batch queries retrieve their guide first. For the 7,983 overlapping
gene/context records, PRIME retrieves the intended RNAi target first in 72 cases and
the intended CRISPR target first in 94. These are selected, dependent observations;
neither fraction is a population accuracy estimate or a p-value.

## Everolimus: favorable connections survive, but the model does not qualify

Of 628 everolimus-labelled profiles, 271 use the reference-matching InChIKey;
82 of those pass the specified drug-quality filter across the whole release.
The other 357 retain unresolved stereochemical identity and are kept separate.
Among reference-matching profiles in the BUB1B contexts, 5/15 pass drug QC. All
five have negative BUB1B correlations, unchanged in sign by either sensitivity.

Three passing profiles are at **0.1 µM nominal culture concentration**:

| Cell | BUB1B correlation | Reversal rank among CRISPR targets | BUB1B query profiles passing QC |
|---|---:|---:|---:|
| A375 | −0.0043 | 2,402 / 5,119 | 0 |
| YAPC | −0.0261 | 616 / 5,113 | 0 |
| MCF7 | −0.2144 | 7 / 4,274 | 0 |

MCF7 also retrieves MTOR first among 4,274 targets with a positive correlation of
0.2836. This is favorable mechanism evidence. However, its BUB1B query fails QC and
disagrees with RNAi. HT29's available reference-matching everolimus profile is at
10 µM, fails drug QC and correlates positively with BUB1B loss. No context combines
independent-guide qualification with a qualified drug-rescue result.

The improved low-dose coverage does not erase the older QC result. The detailed
[source-well audit](track2-crispr-continuity-v25.json) shows that the newer A375 and
NPC 0.1 µM signatures regroup the three earlier singleton wells per cell under new
IDs. A375's regrouped signature now passes the filter. The first exact-ID comparison
missed this continuity; the well-level audit resolves it. Neither regrouping nor
new processing creates an independent experiment. Nominal culture concentrations
still cannot establish free tissue exposure or a child's dose.

## Consequences for the proposal

Advance **HT29 assay qualification**, with independent perturbation/restoration and
endogenous protein/function measurements. Retain MCF7's favorable drug/MTOR result
as a separate mechanism check, with its failed BUB1B model qualification visible.
Do not combine the best model result in one cell with the best drug result in another
as though they were a joint rescue experiment.

The [revised validation requirements](track2-crispr-validation-v25.md) add explicit
editing-stress, guide-independence, source-well and cross-context safeguards to v21/v23.
Expression reversal might suppress a harmful response, a protective response or
general proliferation. Direct useful function, daughter fate, recovery and injury
must decide between those explanations. Favorable human T-cell mTOR findings and
contrary developmental/CRISPR evidence are retained with their limits in the source
review. No drug disposition is promoted.

## Compute and verification

The campaign scored 285,488 compound profiles in matched contexts and completed
**2,474,445,074 comparisons**: 700,767,475 cross-batch, 367,326,268 orthogonal and
1,406,351,331 CRISPR–compound comparisons. These counts reuse profiles and include
prespecified sensitivities; they are not independent experiments.

Eight workers ran for 17.6–179.5 seconds each. Timed CUDA matrix products totalled
1.231 seconds across workers; preprocessing, CPU summaries and I/O dominated.
One-second monitoring peaked at 8% GPU utilization. All eight GPUs executed products,
but this was **brief GPU work, not sustained saturation**. We did not add redundant
model runs to inflate utilization.

All six source files passed source ETag/length verification and received SHA256
records. Separate CPU checks compare original GCTX coordinates and all 141
BUB1B/everolimus comparisons across the three identifiers; maximum error is
2.83 × 10⁻⁷, below 2 × 10⁻⁵. This is internal numerical verification, not independent
scientific review. See the [complete results](track2-crispr-results-v25.json),
[summary](track2-crispr-summary-v25.json), [audit](track2-crispr-audit-v25.json) and
[reproduction instructions](track2-crispr-reproduction-v25.md).

Only public data and code were used under the owner host's `~/v` folder. No subject
data transfer, hosted model inference, wet-lab intervention or submission occurred.
Presentation v24 remains frozen; this v25 addendum must accompany it until a future
presentation revision integrates these findings.
