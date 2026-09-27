# Public RNAi falsification: source and design review

27 September 2026. This is a targeted follow-up to v19, not a systematic review.
Expression results were not opened before the v23 plan was written and staged.
Only public sources were queried; no subject records or clinical narrative were used.

The primary [Smith et al. study](https://doi.org/10.1371/journal.pbio.2003213)
examines seed effects, consensus signatures and RNAi/CRISPR comparisons. The results,
discussion and methods sections were read, particularly the seed definition,
holdout limitations, data processing and selected CRISPR panel. Its caveat matters:
a failed group holdout need not invalidate every reagent or the full consensus.
The new analysis therefore tests specific competing explanations, rather than treating
v19's failed operational filter as biological disproof. The study also supports
retaining successful cross-technology comparisons as a counterweight. Those controls
are selected genes and use Cas9-expressing derivatives, not identical parental cells.

[GSE106127](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106127) supplies
raw and PRIME Level-5 matrices, 978 measured genes and annotated 6-mer/7-mer seeds.
The [NIH directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE106nnn/GSE106127/suppl/)
was read directly after the web-tool directory request failed. Its README redirects
to the GEO guide and supplies no additional protocol detail. Metadata has 119,013
signatures: 116,782 RNAi, 2,117 CRISPR and 114 vector controls. BUB1B has 55 RNAi
signatures across nine cell lines, ten distinct reagents overall and no CRISPR record.
This is a curated reuse of Connectivity Map experiments; overlap with v19 is measured
explicitly. A new accession does not establish an independent experiment.

The authors' [public code](https://github.com/iamsinht/rnaicrispr/tree/b30494958464142d0ff6985fceff2e374069ad25)
was inspected at commit `b30494958464142d0ff6985fceff2e374069ad25` (`tools/get_data.m`
and `util/modzs.m`). It was not executed. The new analysis uses an explicit equal-weight
mean for orthogonal reference comparisons and pairwise means for conditional tests;
it does not claim to reproduce the authors' weighted consensus or published FDRs.
Deposited PRIME is also distinct from v19's local, uncentered rank-space projection.

Targeted web searches also sought contrary findings about signature reversal,
proliferation, toxicity and reproducibility. Search-returned primary-study abstracts
include [Szalai et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6821211/) on viability
confounding, [Lim and Pavlidis](https://doi.org/10.1038/s41598-021-97005-z) on limited
CMap reproducibility, and [Chen et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5510182/)
on cancer signature reversal. These were discovery/abstract checks, not full-paper
reviews. They justify retaining functional and safety endpoints and separating tumour
killing from non-cancer rescue. None supplies MVA efficacy or a clinical exposure margin.
The earlier v21 searches and source adjudications continue to govern the drug,
functional, exposure and injury claims; this computation addresses only assay attribution.

Exact queries and retrieval outcomes are recorded in `track2-rnai-search-v23.json`.
No inference is drawn from search rank, inaccessible pages or absence of a hit.
