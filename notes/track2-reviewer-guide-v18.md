# Track 2 reviewer guide

Start with the [v18 report](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v18.md)
and [eight-slide deck](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-slides-v18.html).
This is a qualified everolimus experiment for non-cancer function. Function, safety,
mechanism and exposure can each stop advancement. No rescue-priority drug is supported.

## Public checks

```bash
uv run --no-project python scripts/track2_public_review_v18.py
```

The standard-library command checks public tracked artifacts: source/requirement
records, archived discussion coverage, retained-control sensitivity, synthetic
denominators, decision rules, methods answers and slide/script alignment. It needs
no subject data, keys, network, SSH, GPUs, model weights or earlier release folders.
It does not establish biological efficacy or eligibility.

The [63-source ledger](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-evidence-v15.json),
[19-claim register](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-falsification-register-v15.json)
and [validation plan](https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-validation-v15.md)
retain the scientific decisions. The v18 changes are visual and editorial. The
September 24 community review is retained; the official brief was rechecked September 25.

## Regenerate the materials

```bash
uv run scripts/track2_export_documents_v18.py new-v18-documents
uv run node scripts/render_track2_report_v18.mjs new-v18-documents
uv run node scripts/render_track2_slides_v18.mjs new-v18-slides
```

Use new directory names; exports cannot overwrite earlier versions. The document
exporter uses pinned transient dependencies and a hash-verified official workbook.
Renderers require Node/Chrome and use isolated, network-blocked profiles. Ubuntu is
the local slide/report typeface; the PDFs embed fonts, while HTML falls back to
sans-serif on hosts without Ubuntu. No image-model provider or remote assets are used.

`scripts/track2_release_v18.py` separately verifies the new research snapshot and
all locally retained historical snapshots. `scripts/track2_bundle_v18.py` packages
the deck, report, workbook, script and recording notes with hashes. Neither operation
records or submits a video. Current paths are in `notes/track2-current.json`.

Earlier model matrices, failed runs and corrections remain in the technical history.
Historical AF3/Atlas materials retain applicable notices. Their numerical outputs and
figures are omitted from the pitch/report; linked-history distribution scope remains
unresolved. No blanket relicence or provider attestation is implied.
