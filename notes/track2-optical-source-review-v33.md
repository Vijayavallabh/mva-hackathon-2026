# Optical phenotype source review

19 October 2026. Eight bounded Europe PMC searches returned 177 records representing
156 distinct source IDs. Titles and selected primary abstracts/methods passages were
screened. This is not a systematic review or a full-paper review of every result.
Requests, failures and exact response hashes are retained under
`results/feat009/optical-v33/discovery`, `discovery-followup`, `coverage` and `schema`.

| Source and reading depth | What it supports | What could invalidate the proposed use |
|---|---|---|
| [Funk et al., Cell 2022](https://doi.org/10.1016/j.cell.2022.10.017); dataset metadata, workbook and selected methods/supplement passages | Public optical measurements with four guide designs per gene offer a modality distinct from expression. | HeLa is transformed, aneuploid and p53 deficient. Fixed-cell counts reflect survival, sampling and classification. They cannot establish fidelity or non-cancer rescue. |
| [Counting cells can accurately predict small-molecule bioactivity benchmarks](https://doi.org/10.1038/s41467-026-68725-5); selected abstract, results and methods | Abundance is a strong competing explanation on several benchmarks. Full morphology retains an advantage on the curated 24-target subset. | An apparent neural gain over a weak baseline can overstate biological information. Retain count/basic-feature controls and held-out genes. The paper does not show all morphology is useless. |
| [Carbon blog](https://huggingface.co/blog/HuggingFaceBio/carbon-annotator-genbank-genome-annotation), requested collection and model card | The 1.2B model annotates protein-coding regions from sequence. Its decoder produces a consensus path; multiple isoforms are future work. | It does not answer the present questions about BUB1B functional rescue, phase or drug response. No Carbon inference was run; a technical-report bucket listing is not a technical-report review. |
| [Anthropic modeling toolkit](https://github.com/anthropics/uplifting-biomolecular-modeling/tree/f4f62fa6592ae4938d49b1757bea0cfeff9f468e); live revision/README compared | The available revision matches the toolkit already used for the completed ProteinMPNN analysis. | Repeating structural scoring cannot repair its failed functional controls or answer the imaging question. Existing execution and limitations remain preserved in v29. |

The Funk paper describes a live-cell sub-screen with 24-hour tracking. Incomplete
lineages are excluded, mitotic/apoptotic classes are combined in later analysis,
and a figure uses the stronger of two collection days. Its event definitions and
censoring differ from our required all-enrolled cell-fate analysis. Public duration
summaries must not be described as unbiased daughter survival. Raw trajectories have
not been obtained or reanalyzed here.

Retrieval failures remain visible: Europe PMC full-text retrieval failed; the PMC
web/PDF requests returned browser-challenge HTML with HTTP 200. Those are not full
papers. Selected source methods were read from the published PDF mirrored at
[STAT](https://www.statnews.com/wp-content/uploads/2023/02/MADNESS-23-49.pdf).
The first Dataverse request had a mistyped DOI and returned 404; the corrected
DOI ends in **VYKTI5**, and its metadata passed validation. The 2019 reduced-intensity
RMS case report, [10.1111/ped.13849](https://doi.org/10.1111/ped.13849), remains a
title/metadata lead; no full-text dosing or toxicity claim was verified from it.

The practical changes are to compare neural learning with strong simple baselines,
hold out all evaluated genes, retain shuffled training controls and plate sensitivity,
and keep low guide coverage as missing evidence. Neither favorable retrieval nor
training success qualifies an endogenous model or changes the drug ranking.
