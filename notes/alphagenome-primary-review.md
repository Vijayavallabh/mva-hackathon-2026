# AlphaGenome Atlas: primary-source relevance review

Reviewed 2026-09-08 for feat-009. This is a public-resource review, not a patient
prediction run. No subject file, sequence, genotype record or clinical narrative was
submitted to a remote service. Existing Track 1 submissions remain immutable.

## Decision

Atlas is relevant as an **optional molecular-interpretation check**, not a drug-ranking
or exposure model. The selected pair contains a stop-gain SNV and a missense SNV, so
the released variant class is potentially applicable. However, a high composite score
could simply repeat consequences already used in our analysis. Added value requires
examining the underlying regulatory/splicing predictions and feature contributions,
not collecting another favourable score. See the existing
[allele interpretation](track2-report.md).

No BUB1B-specific Atlas result was obtained in this review. Everolimus's conditional
priority and HCQ's reserve status therefore do not change. All clinical exposure
margins remain unknown; trans phase remains unconfirmed.

## Identity, release and reproducibility

| Resource | Verified primary evidence | Important distinction |
|---|---|---|
| AlphaGenome Atlas | DeepMind's announcement is dated **8 September 2026**. It describes precomputed effects for approximately nine billion SNVs, AVI scores, feature attributions and motif maps. [Launch announcement](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/) | This is an official new resource, not a third-party tool with a similar name. |
| API client | The official changelog's **0.9.0** section adds the Atlas API. Inspected commit: `aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d`, committed `2026-09-08T10:35:56Z`. [Pinned changelog](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/CHANGELOG.md) | Older cached documentation can omit Atlas. This client revision is not a verified Atlas dataset/model version. |
| Atlas manuscript | The launch links an 83-page primary manuscript. SHA-256: `07011853872613cb7bd3ce8ca62cd2621ad50b0a16e6f5dec3e480b3d190af2c`. [Manuscript](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf) | Do not cite the earlier Nature paper as peer review of AVI. No final journal publication/DOI for this Atlas manuscript was verified here. |
| Base AlphaGenome model | The earlier model has a peer-reviewed Nature article and separate research-code/weights release. [Nature article](https://www.nature.com/articles/s41586-025-10014-0), [research repository](https://github.com/google-deepmind/alphagenome_research) | Local base-model inference is not equivalent to reproducing the new AVI model. |

## What an AVI result would mean

The manuscript describes 18 features: ten aggregated AlphaGenome modalities plus
AlphaMissense, consequence, conservation and indel indicators. Regulatory features
take maxima across tissues and other dimensions. Training uses gnomAD v4.1 frequency
proxies, not individual clinical outcomes. Chromosome 15 is among training chromosomes;
exact overlap with our selected alleles is unknown. PHRED 20 means the top 1% of the
SNV score distribution, **not 99% pathogenicity**. The overview describes SHAP
contributions against raw AVI, not its PHRED transformation, but the Methods use
approximate baseline-relative attributions. The baseline is not supplied by the
inspected API; do not impose exact equality to raw AVI. See the
[score-semantics clarification](alphagenome-score-semantics.md). The study includes observed indels, but the initial
public datasets are restricted to valid hg38 SNVs. AVI code/weights are promised upon
final publication. [Manuscript, methods and data/code availability](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

Review inference: compare any eventual score with the evidence already available.
Termination-driven evidence does not measure transcript decay. Protein-impact-driven
evidence does not demonstrate a reversible folding defect. A maximum-across-contexts
result should not be labelled a measurement from the relevant normal or tumour cells.
An ensemble built partly from existing annotations is not an independent experiment.

## Access, terms and execution boundaries

The official client README distinguishes the API's non-commercial research use from
explicit permissive downloadable-artifact exceptions; it also restricts training other
machine-learning models on outputs. Predictions are not for clinical decisions.
An Apache-2.0 client-code licence does **not** remove restrictions on hosted outputs.
[Pinned README and terms links](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/README.md)

The initial unauthenticated [portal](https://deepmind.google.com/science/alphagenome/atlas)
and [terms page](https://deepmind.google.com/science/alphagenome/terms) inspection returned an
application/sign-in shell. Its public configuration advertised an 88.5 GB AVI-SNV
Tabix ZIP as permissive for commercial/non-commercial use, while splicing (20.6 GB)
and feature-importance (283.9 GB) downloads were labelled non-commercial. These labels
are not a full review or acceptance of the service's legal terms; the complete terms
were not available as readable text in that initial inspection. The continuation
below resolves text access through normal browser rendering. A public
download link is also not evidence that its bytes can currently be retrieved.

The separate base-model repository offers weights through gated Hugging Face/Kaggle
downloads requiring acceptance of non-commercial model terms. It recommends at least
an H100 for inference. Downloading weights does not authorize sending subject data to
hosted inference or moving it to another machine.
[Research-code requirements and licence](https://github.com/google-deepmind/alphagenome_research)

This review did not authenticate, accept new terms, request a key, install a provider
client, run Google-hosted model inference, or download the large Atlas archives.
Public reference-resource acquisition followed by an entirely local lookup is the
preferred next route if access becomes available and applicable terms are confirmed.
Failure to retrieve a resource is **missing evidence**, not a zero score or a benign
prediction. Execution/access-audit results belong in the companion session evidence.

## What it cannot establish, and the better experiment

Base AlphaGenome predicts DNA-dependent molecular readouts. Its authors report
limitations in condition specificity, distal regulation and personal-genome prediction;
sequence-to-function predictions do not directly establish disease-level outcomes.
[Base-model limitations](https://www.nature.com/articles/s41586-025-10014-0)

Accordingly, the following are review conclusions rather than Atlas measurements:

- **Phase:** two independent variant predictions cannot show which chromosome carries
  either allele. Simulated cis/trans sequences assume arrangements; they do not observe
  inheritance. Our linkage evidence remains unchanged.
- **Drug benefit:** predicted expression/splicing does not test everolimus or HCQ,
  demonstrate functional rescue, or establish preferential tumour killing.
- **Exposure:** there are no administered-drug concentration, protein-binding,
  pharmacokinetic or deficient-normal safety measurements in a variant-impact score.
- **Mechanism:** a regulatory hypothesis should lead to allele-aware RNA/splicing or
  protein/function assays, with relevant cell context and suitable controls. Drug
  hypotheses still require the phenotype-first gates in the
  [validation plan](track2-validation.md).

The highest-value eventual Atlas result would be an unexpected, reproducible splicing
or regulatory hypothesis that changes a specific validation experiment. A favourable
composite score alone would not justify changing the drug proposal, claiming confirmed
trans, modifying the uploaded Track 1 files, or promising a competition outcome.

## Review method and limits

The research skill directed this independent primary-source review; the PDF skill
was used to extract the large public launch manuscript locally when the browsing tool
could not load it. The abstract, model construction, training/overlap filtering,
interpretation limitations and data/code availability were examined. This was not
an exhaustive audit of every benchmark or supplementary table, and no BUB1B-specific
Atlas benchmark was identified. No contact with authors, organizers or family occurred.

Reproduction of the public-paper inspection uses `curl --fail --location` on the
manuscript link above, followed by `pdftotext -layout`, `pdfinfo`, and `sha256sum`.
Release identity was cross-checked against
`https://api.github.com/repos/google-deepmind/alphagenome/commits/main` and the pinned
changelog. Preserve the recorded PDF hash and client commit when repeating the review;
do not silently substitute future releases.

## Continuation: documented alternative access, 2026-09-08

After the owner's request to continue despite the failed download, the independent
research check revisited official release metadata, Atlas client documentation and
documented terms links. The live GitHub `commits/main` response still identified
`aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d`; no newer client revision was found.
The [pinned Atlas API documentation](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/docs/source/api/atlas.md)
and [client implementation](https://github.com/google-deepmind/alphagenome/blob/aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d/src/alphagenome/atlas/atlas.py)
document keyed API access, not an alternative unauthenticated static-data location.
Bounded primary-domain searches found no documented alternative bulk endpoint. This
is an access-search result, not proof that none exists.

A new readable first-party terms artifact was found and independently retrieved:
[AlphaGenome Model Parameters Terms of Use](https://storage.googleapis.com/alphagenome/terms/AlphaGenome-Model-Terms-of-Use.pdf).
Its text is dated **10 December 2025**; HTTP metadata reports modification on
23 January 2026. The complete 161,773-byte PDF was extracted locally and read;
SHA-256 is `0c7115b38e801c54b3b8b523abe4478ec3216bd8291a769c8bd5e3a504c030f3`.
It restricts base-model assets to eligible non-commercial use, requires notices for
redistributed output and model derivatives, prohibits clinical use and bypassing model
access controls, and links the separate output terms. **This is not the operative
Atlas service/permissive-download agreement**, so it does not independently establish
the current Atlas terms or authorize an alternative download path.

The main session subsequently rendered the complete first-party service and output
terms without login; this reviewer also read both complete rendered texts. The
[Services Additional Terms](https://deepmind.google.com/science/alphagenome/terms),
modified **8 September 2026**, distinguish the permissive downloadable AVI score from
its feature breakdown. The permissive exception does not waive all other provisions.
The service retains eligibility requirements, personal/non-shareable credentials,
nonclinical restrictions and a prohibition on processing HIPAA-regulated health data.
It incorporates other Google terms and policies. The
[Output Terms](https://deepmind.google.com/science/alphagenome/output-terms), effective
**25 June 2025**, describe redistribution notices and a specific exception for training
similar models subject to model-parameter terms; a blanket claim that all possible
output-based model training is prohibited would be too broad. This is a scoped
research review, not a legal opinion or verification of account eligibility. No
account registration or agreement-acceptance button was used.

Reproducible rendered evidence is in
`results/feat009/alphagenome-browser-v2/terms-rendered.html` and
`results/feat009/alphagenome-browser-v1/output-terms-rendered.html`. The published
[service-terms PDF](https://storage.googleapis.com/alphagenome/terms/20260908/AlphaGenome%20Services%20Additional%20Terms%20of%20Service%20-%20English.pdf)
is a documented direct route to that document, not to prediction data.

The newly linked official `science-skills` repository was inspected as source material,
not executed or adopted as instructions. At commit
`28b8482603a420708c8896f6fe5e06c276d9933d` (8 September, 12:12:22 UTC), its
[AVI helper](https://github.com/google-deepmind/science-skills/blob/28b8482603a420708c8896f6fe5e06c276d9933d/skills/alphagenome_variant_impact_score/scripts/alphagenome_atlas_avi.py)
requires a key for scores and experimental metadata. Its `AviFeature` enum and
`metadata --features` branch provide **18 static feature definitions without a
client**, not predictions. Public GENCODE reference annotations and URL construction
are also available, but neither supplies AVI results. Inspecting these definitions
can support an offline dependency checklist. Avoid executing the foreign CLI just to
read them: its entry point also loads a home-directory environment file.

This continuation did not repeat the scientific paper review or run variant queries.
No authentication, agreement acceptance, inference, author contact, untrusted mirror,
or access-control workaround was used. Normal browser rendering resolved the document
access problem, but no alternative working score-download route was found by this
independent review. Repeat checks of the published download remain separate,
auditable access tests by the main session.
