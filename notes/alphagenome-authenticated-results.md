# AlphaGenome Atlas authenticated follow-up

2026-09-08, session 35, feat-009; baseline `6aa9d96`. Research only.

## Outcome

**The owner-configured key works. Both submitted BUB1B candidates now have validated
precomputed AVI scores and all 18 feature attributions.** Detailed molecular-scorer
retrieval remains incomplete after service failures. No on-demand model inference,
raw genomic-file transfer, clinical narrative upload or phase experiment occurred.

These additional computational annotations do **not** change the drug shortlist,
establish causality, confirm trans, or supply a clinical exposure margin. They mainly
reuse evidence already in the variant assessment. The Track 1 v4 files and reviewed
Track 2 v2 snapshot remain unchanged; this is a separate research addendum.

## Output notice and disclosure

AlphaGenome-derived values, feature summaries and interpretations here are subject to
the [AlphaGenome Output Terms of Use](https://deepmind.google.com/science/alphagenome/output-terms),
with the AVI-score exception described in the
[Services Additional Terms](https://deepmind.google.com/science/alphagenome/terms).
No additional output licence is granted here. Modifications: JSON serialization,
CDF-to-PHRED calculation, rounding, selection of largest attributions and explanatory
interpretation. Predictions are not clinically validated measurements.

**AI-use update:** Google DeepMind AlphaGenome Atlas's authenticated API was used to
retrieve precomputed public-reference predictions on 2026-09-08. This is additional
to OpenAI/Codex, not another language-model literature-review service or a newly run
AlphaGenome inference. The owner's earlier no-other-provider attestation remains a
historical statement for the already-submitted Track 1 package. A future Track 2
release should include this updated disclosure and notice; do not silently reuse the
historical statement as a description of the entire current workflow. No independent
account-retention/training-policy audit was performed for Google.

## Actual results

Source: `results/feat009/alphagenome-auth-composites-v1/scores.json`, acquired
16:24:44–16:24:50 UTC on 2026-09-08. All variants are GRCh38, 1-based, forward-strand
REF/ALT. The two candidate tuples came from the permitted submission-derived report,
not VCF extraction. The public DNM1 example is a transport/parser control only.

| Variant | Raw AVI | API CDF | PHRED | Largest feature attribution |
|---|---:|---:|---:|---|
| Public DNM1 `chr9:128225994 G>A` | 1.061495 | 0.996578634 | 24.6580 | Merged splicing: 0.769922 |
| BUB1B `chr15:40209701 T>G`, p.Leu737Ter | 1.872790 | 0.999579668 | 33.7641 | Protein termination: 1.484070 |
| BUB1B `chr15:40220612 T>G`, p.Asn1002Lys | 1.216326 | 0.997251093 | 25.6084 | AlphaMissense: 0.760741 |

All displayed PHRED values are `-10*log10(1-CDF)` and none required the helper's
`1e-7` tail floor. The two candidate tails are approximately **0.0420%** and
**0.2749%** of the calibration distribution, respectively—not patient disease risks
or probabilities of pathogenicity. The full-precision values and named attributions
are retained in the JSON. [Score definitions and validation](alphagenome-score-semantics.md)

Interpretation:

- For p.Leu737Ter, termination dominates, followed by PhastCons and Cactus conservation
  contributions of 0.221275 and 0.151699. This is consistent with an established
  stop-gain annotation; it does not measure nonsense-mediated decay or residual protein.
- For p.Asn1002Lys, AlphaMissense dominates, followed by PhastCons and Cactus contributions
  of 0.234708 and 0.221295. **0.760741 is an attribution to AVI, not the original
  AlphaMissense pathogenicity score.** It does not establish a reversible folding defect.
- Small splicing/RNA attributions are contributions to the composite, not measured
  molecular effects and not evidence of no splice or expression effect. No usable
  detailed molecular matrix was retained from the attempted all-scorer lookup.
- Raw-minus-sum-of-attribution residuals are −0.049199554 (control), −0.045775602
  (stop-gain), and −0.049405229 (missense). The Methods' baseline and approximation
  are unresolved; do not force exact additivity or infer a universal offset.

AVI combines AlphaMissense, consequences and conservation with AlphaGenome molecular
features; it is not independent validation of those existing inputs. Chromosome 15
was a training chromosome; exact candidate training overlap remains unknown. Do not
turn two composite scores into evidence of trans or genotype-specific drug rescue.
[Primary-source assessment](alphagenome-primary-review.md)

## Request scope and reproducibility

The key was read only inside the local process from the ignored, owner-only `.env`;
it was not printed, included in a command argument, hashed, or written into results.
The parser does not execute shell syntax or expand environment variables. Requests
go only to the pinned client's official `gdmscience.googleapis.com:443` TLS endpoint,
with a 20-second connection timeout, 45-second per-RPC deadline and retries disabled.
Python/native diagnostics are muted, including client cleanup on failure. Error
records contain only allowlisted local codes or gRPC status, not service error text.

Before candidate calls, the script verifies the immutable local Track 1 v4 hashes,
the derived report SHA-256 and both REF bases against the local GRCh38 reference.
Then live public metadata and the documented DNM1 control must pass. Exact outgoing
variant protos are restricted to that control and the two submitted tuples. There
is no arbitrary variant, interval, VCF, sequence, clinical-context or endpoint input.
No sample identifier, genotype, phase, phenotype or transcript narrative is sent.

The initial full candidate plan requested AVI and feature importance separately from
all twelve molecular scorers, without gene/tissue filters. That would retain all
returned genes/tracks, not just favourable or BUB1B-associated values. After actual
molecular service failure, the declared `submitted-composites` fallback deliberately
requests only AVI and feature importance for both candidates. It must not be described
as successful detailed molecular analysis. HPO terms are not biosample identifiers.

```bash
uv run python scripts/alphagenome_atlas.py results/feat009/alphagenome-auth-v1
uv run python scripts/alphagenome_atlas.py results/feat009/alphagenome-auth-control-v1 --mode control
uv run python scripts/alphagenome_atlas.py results/feat009/alphagenome-auth-pair-v1 --mode submitted-pair
# Pair v2/v3/v4 use new directories after documented parser/reliability changes.
uv run python scripts/alphagenome_atlas.py results/feat009/alphagenome-auth-composites-v1 --mode submitted-composites
uv run python scripts/test_alphagenome_atlas.py
uv run python scripts/track2_evidence.py verify results/feat009/jvv7_track2_research_v2
uv run python scripts/track2_evidence.py track1
```

Existing output directories are never overwritten; choose a new suffix if explicitly
repeating a lookup. `uv.lock` pins the SDK and dependencies; the SDK source revision
is `aa6fc8f6faadcb8c910fa2b85b57386fbd5c7b5d`, checked against installed package metadata.
This is **not** an immutable server model/dataset version. The API provides no such
version field in the inspected schema, so the manifest keeps it null. Later API
responses need not be bit-identical. Manifests record executing-script hashes, UTC
times, exact request scope and hashes of normalized returned metadata/score JSON;
these are not hashes of raw gRPC wire bytes. Early attempts used earlier working
versions of this script; their failed manifests remain historical, not current reruns.

Successful composite-run hashes:

- `scorers.json`: `1a3e31f14291d838f2db5eeec136f34e338770732fc8fd71d410f48680ae396f`
- `scores.json`: `a0e7fdf692b630ff65dd5ed73778bb6fb78236504fc939eb4151815ab3583dc5`
- Executing script: `ca134712935c4619775bb59714d5094795be7990143587c0bdc27a8242b4b43d`

## Failure record and adversarial corrections

| Snapshot suffix | Result | What may be concluded |
|---|---|---|
| `auth-v1` | Metadata success, 22 scorers | Credential/API access works |
| `auth-control-v1` | Metadata + public control pass | Transport, identity and shape checks work for this example |
| `auth-pair-v1` | Local gate failure after control; no candidate retained | Failure cause not localized; no accepted candidate score |
| `auth-pair-v2` | gRPC `UNAVAILABLE` at control | Temporary request failure, not invalid key or biological absence |
| `auth-pair-v3` | gRPC `UNAVAILABLE` at first candidate composite | No retained candidate result |
| `auth-pair-v4` | First candidate composite retained; molecular RPC `UNAVAILABLE` | Partial success only; second candidate not yet requested in this run |
| `auth-composites-v1` | Control + both candidate composites pass | Both AVI/attribution lookups available; no detailed molecular results |

Independent standards review identified loss of successful composite results after a
later molecular failure and cleanup diagnostics outside the muted boundary. Both
were corrected and regression-tested. Independent scientific review identified the
incorrect universal `[0,1]` molecular calibration gate; signed molecular calibration
uses `[-1,1]`, while AVI retains its own CDF interpretation. Tests now cover both,
identity/shape/name validation, secret redaction, native finalizer diagnostics,
partial preservation, exact request allowlist and composite-only scope. The older
exact-SHAP-sum statement was also corrected. These fixes do not retroactively diagnose
the insufficiently instrumented first live failure.

Next useful Atlas work, if resumed, is a bounded RNA/splicing retrieval with explicit
gene/tissue coverage and negative results retained. It is optional for the existing
Track 2 hypothesis and cannot replace RNA/protein experiments, segregation or measured
normal/tumour exposure. No automatic retries or scheduled monitoring remain running.
