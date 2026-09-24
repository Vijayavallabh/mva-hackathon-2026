# Track 2 reviewer guide — jvv7

Start with the [v17 report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v17.md)
and [eight-slide deck](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v17.html).
The proposal is a qualified everolimus experiment for non-cancer function, not a
rescue ranking or treatment recommendation. Its decisive feature is an outcome that
can fail on function, safety, mechanism or exposure rather than pass on a marker alone.

## Reproduce the public checks

From a checkout of this repository:

```bash
uv run --no-project python scripts/track2_public_review_v17.py
```

This standard-library command reads public tracked artifacts only. It needs no gated
subject data, API keys, network requests, SSH, GPUs, model weights, previous local
release directories or project `.env`. It checks source/requirement provenance,
24-discussion coverage, the actual retained-control sensitivity, the synthetic
selection example, conservative advancement gates, and current presentation alignment.
It does not rerun models, verify the truth of source adjudication, measure biological
benefit or certify clinical/competition readiness. A clean exported-copy test and
resource measurements are documented in the v17 design/review note.

The [63-source ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json),
[19-claim register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v15.json)
and [validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v15.md)
contain the scientific decisions. The [falsification review](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-review-v15.md)
retains positive and contrary results, reading limits and failed retrievals. Unknown
means hold; failed safety stops advancement; all-pass permits only preclinical review.

## Full research history and regeneration

Earlier model campaigns, complete public-reference matrices and runtime corrections
are indexed in `notes/track2-latest-models.md` and `notes/track2-model-expansion.md`.
Historical AF3/Atlas derivatives retain their applicable terms and notices. The
judge-facing v17 materials omit their numerical outputs and figures; distribution
scope for linked history remains unresolved. Do not present the repository as a
blanket relicence of third-party material.

To regenerate current documents and slides into new directories:

```bash
uv run scripts/track2_export_documents_v17.py new-v17-documents
uv run node scripts/render_track2_slides_v17.mjs new-v17-slides
uv run node scripts/render_track2_report_v17.mjs new-v17-documents
```

The document exporter uses pinned transient Python dependencies and downloads the
hash-verified public organizer template if it is absent locally. The renderers use
installed Node/Chrome and isolated network-blocked browser profiles; no external
assets or new image-model provider. Reports use absolute public evidence links so
uploaded PDF/Markdown files do not depend on local relative paths.

For the owner, `scripts/track2_release_v17.py` checks/builds/verifies a new immutable
research snapshot and recursively verifies locally retained earlier snapshots.
That stricter historical-integrity operation has extra local archive requirements;
it is separate from the public reviewer command. Submitted Track 1 and all previous
Track 2 releases remain unchanged. See `notes/track2-current.json` for current paths.
