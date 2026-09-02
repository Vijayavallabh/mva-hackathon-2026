"""Extract embedded HPO IDs from the phenotype DOCX and resolve their labels.

The protected clinical narrative is read locally but is never printed or written. The
only subject-derived values emitted by this program are standardized HPO IDs, which the
data-access rules explicitly permit as derived output.

Run the real extraction from the repository root:

    uv run python scripts/extract_hpo.py

Run the synthetic, data-free exercise:

    uv run python scripts/extract_hpo.py --self-check
"""

from __future__ import annotations

import argparse
import hashlib
import re
import tempfile
import zipfile
from collections.abc import Iterable
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCX = ROOT / "data" / "Challenge_Clinical_Phenotype_1.docx"
DEFAULT_ONTOLOGY = ROOT / "data" / "resources" / "hp.obo"
DEFAULT_OUTPUT = ROOT / "notes" / "phenotype.md"
HPO_SOURCE = "https://purl.obolibrary.org/obo/hp.obo"
HPO_ID = re.compile(rb"HP:\d{7}")


def extract_hpo_ids(docx: Path) -> list[str]:
    """Return unique HPO IDs in document order without returning narrative text."""
    with zipfile.ZipFile(docx) as archive:
        try:
            document_xml = archive.read("word/document.xml")
        except KeyError as error:
            raise ValueError("DOCX has no word/document.xml member") from error

    # Searching the XML bytes avoids storing or exposing the surrounding clinical text.
    found = (match.group().decode("ascii") for match in HPO_ID.finditer(document_xml))
    return list(dict.fromkeys(found))


def _finish_obo_term(fields: dict[str, object], labels: dict[str, str]) -> None:
    """Add one non-obsolete OBO term and its alternate IDs to ``labels``."""
    term_id = fields.get("id")
    name = fields.get("name")
    if not isinstance(term_id, str) or not isinstance(name, str):
        return
    if fields.get("is_obsolete") == "true":
        return
    labels[term_id] = name
    for alt_id in fields.get("alt_ids", []):
        if isinstance(alt_id, str):
            labels[alt_id] = name


def parse_obo(ontology: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return HPO ID-to-label mappings and public ontology header metadata."""
    labels: dict[str, str] = {}
    metadata: dict[str, str] = {}
    fields: dict[str, object] | None = None

    with ontology.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line == "[Term]":
                if fields is not None:
                    _finish_obo_term(fields, labels)
                fields = {"alt_ids": []}
                continue
            if line.startswith("["):
                if fields is not None:
                    _finish_obo_term(fields, labels)
                fields = None
                continue
            if ": " not in line:
                continue

            key, value = line.split(": ", 1)
            if fields is None:
                if key in {"format-version", "data-version", "ontology"}:
                    metadata[key] = value
            elif key == "alt_id":
                alt_ids = fields["alt_ids"]
                assert isinstance(alt_ids, list)
                alt_ids.append(value)
            elif key in {"id", "name", "is_obsolete"}:
                fields[key] = value

    if fields is not None:
        _finish_obo_term(fields, labels)
    return labels, metadata


def sha256(path: Path) -> str:
    """Calculate a resource checksum without loading the whole file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def render_markdown(
    ids: Iterable[str], labels: dict[str, str], metadata: dict[str, str], digest: str
) -> str:
    """Build the public-safe phenotype note from IDs and ontology labels only."""
    rows = []
    for hpo_id in ids:
        try:
            label = labels[hpo_id]
        except KeyError as error:
            raise ValueError(f"HPO ID is absent or obsolete in hp.obo: {hpo_id}") from error
        rows.append(f"| `{hpo_id}` | {label} |")

    table = "\n".join(rows)
    data_version = metadata.get("data-version", "not declared")
    return f"""# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only the standardized
HPO IDs embedded in it and their public ontology labels—no clinical narrative, dates,
places, ages, or identifying free text.

## HPO terms

| HPO ID | Label |
|---|---|
{table}

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`; no phenotype was inferred from prose. Labels came from the official
[Human Phenotype Ontology OBO file]({HPO_SOURCE}).

- Ontology version: `{data_version}`
- Local ontology SHA-256: `{digest}`
- Fetch ontology: `mkdir -p data/resources && curl --fail --location {HPO_SOURCE} --output data/resources/hp.obo`
- Reproduce: `uv run python scripts/extract_hpo.py`
- Data-free exercise: `uv run python scripts/extract_hpo.py --self-check`

## Scope of the search

The earlier structural keyword probe found no karyotype, prior genetic testing, or
candidate gene in the supplied material. The variant search therefore remains genome-wide;
known MVA genes are literature priors, not a hard shortlist.
"""


def run(docx: Path, ontology: Path, output: Path) -> list[str]:
    """Extract IDs, resolve labels, and write the safe derived-output note."""
    ids = extract_hpo_ids(docx)
    if not ids:
        raise ValueError("no embedded HPO IDs found")
    labels, metadata = parse_obo(ontology)
    output.write_text(render_markdown(ids, labels, metadata, sha256(ontology)))
    return ids


def self_check() -> None:
    """Exercise extraction, deduplication, label lookup, and disclosure boundaries."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        docx = root / "synthetic.docx"
        ontology = root / "hp.obo"
        output = root / "phenotype.md"

        with zipfile.ZipFile(docx, "w") as archive:
            archive.writestr(
                "word/document.xml",
                "<document>private example HP:0000001 repeated HP:0000001 "
                "and HP:0000002</document>",
            )
        ontology.write_text(
            "format-version: 1.2\n"
            "data-version: synthetic/test\n\n"
            "[Term]\n"
            "id: HP:0000001\n"
            "name: Synthetic term one\n\n"
            "[Term]\n"
            "id: HP:0000002\n"
            "name: Synthetic term two\n"
        )

        ids = run(docx, ontology, output)
        rendered = output.read_text()
        assert ids == ["HP:0000001", "HP:0000002"]
        assert "Synthetic term one" in rendered
        assert "Synthetic term two" in rendered
        assert "private example" not in rendered
    print("self-check ok: 2 synthetic HPO IDs resolved; narrative not emitted")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract embedded HPO IDs without exposing clinical narrative."
    )
    parser.add_argument("--docx", type=Path, default=DEFAULT_DOCX)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--self-check", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.self_check:
        self_check()
    else:
        extracted = run(arguments.docx, arguments.ontology, arguments.output)
        print(f"wrote {arguments.output} with {len(extracted)} HPO terms")
