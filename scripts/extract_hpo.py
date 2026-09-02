"""Extract public-safe phenotype features from the protected phenotype DOCX.

The protected clinical narrative is read locally but is never printed or written. The
program emits standardized HPO IDs plus broad, non-verbatim context signals; it never
emits the Presentation or Notes cell text, numbers, ages, or measurements.

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
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCX = ROOT / "data" / "Challenge_Clinical_Phenotype_1.docx"
DEFAULT_ONTOLOGY = ROOT / "data" / "resources" / "hp.obo"
DEFAULT_OUTPUT = ROOT / "notes" / "phenotype.md"
HPO_SOURCE = "https://purl.obolibrary.org/obo/hp.obo"
HPO_ID = re.compile(rb"HP:\d{7}")
WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD = {"w": WORD_NAMESPACE}

# These deliberately broad patterns produce lexical signals, not clinical conclusions.
SIGNAL_PATTERNS = {
    "proband context": re.compile(r"\b(?:patient|proband|child|boy|he|his)\b", re.I),
    "family context": re.compile(
        r"\b(?:family|mother|maternal|father|paternal|parent|sibling|brother|sister|"
        r"pregnan\w*|miscarri\w*)\b",
        re.I,
    ),
    "prenatal timing": re.compile(
        r"\b(?:prenatal|antenatal|fetal|foetal|pregnancy|gestation|in utero)\b", re.I
    ),
    "perinatal timing": re.compile(
        r"\b(?:birth|born|newborn|neonatal|prematur\w*|delivery)\b", re.I
    ),
    "postnatal timing": re.compile(
        r"\b(?:postnatal|infancy|infant|childhood|after birth|later in life)\b", re.I
    ),
    "quantitative detail": re.compile(
        r"\d|\b(?:cm|mm|kg|gram\w*|percentile|week\w*|month\w*|year\w*)\b", re.I
    ),
    "diagnostic detail": re.compile(
        r"\b(?:diagnos\w*|biops\w*|patholog\w*|histolog\w*|imaging|ultrasound|"
        r"scan|mri|ct|laboratory)\b",
        re.I,
    ),
    "treatment detail": re.compile(
        r"\b(?:treat\w*|therap\w*|chemotherap\w*|radiotherap\w*|surg\w*|"
        r"medication\w*)\b",
        re.I,
    ),
    "longitudinal detail": re.compile(
        r"\b(?:recurrent|progress\w*|follow-up|previous\w*|history|resolved|ongoing)\b",
        re.I,
    ),
}


ContextSignals = tuple[str, ...]


def _read_document_xml(docx: Path) -> bytes:
    """Read the sole protected DOCX member used by both extraction stages."""
    with zipfile.ZipFile(docx) as archive:
        try:
            return archive.read("word/document.xml")
        except KeyError as error:
            raise ValueError("DOCX has no word/document.xml member") from error


def extract_hpo_ids(docx: Path) -> list[str]:
    """Return unique HPO IDs in document order without returning narrative text."""
    document_xml = _read_document_xml(docx)
    # Searching the XML bytes avoids storing or exposing the surrounding clinical text.
    found = (match.group().decode("ascii") for match in HPO_ID.finditer(document_xml))
    return list(dict.fromkeys(found))


def _cell_text(cell: ElementTree.Element) -> str:
    """Join Word text runs for local classification; callers must not emit the result."""
    return "".join(node.text or "" for node in cell.findall(".//w:t", WORD)).strip()


def _signals(text: str) -> tuple[str, ...]:
    """Reduce protected text to a fixed vocabulary of broad lexical signals."""
    return tuple(name for name, pattern in SIGNAL_PATTERNS.items() if pattern.search(text))


def extract_context_signals(docx: Path) -> dict[str, ContextSignals]:
    """Classify the Presentation/Notes cell without returning its source text."""
    root = ElementTree.fromstring(_read_document_xml(docx))
    tables = root.findall(".//w:tbl", WORD)
    if len(tables) != 1:
        raise ValueError("expected exactly one phenotype table")
    rows = tables[0].findall("./w:tr", WORD)
    if not rows:
        raise ValueError("phenotype table has no rows")

    header_cells = rows[0].findall("./w:tc", WORD)
    headers = [_cell_text(cell).casefold() for cell in header_cells]
    context_indices = [
        index
        for index, header in enumerate(headers)
        if "present" in header and "note" in header
    ]
    if len(context_indices) != 1:
        raise ValueError("phenotype table lacks one combined Presentation/Notes column")
    context_index = context_indices[0]

    contexts: dict[str, ContextSignals] = {}
    for row in rows[1:]:
        cells = row.findall("./w:tc", WORD)
        if context_index >= len(cells):
            raise ValueError("phenotype table row has too few columns")
        row_ids = HPO_ID.findall(" ".join(_cell_text(cell) for cell in cells).encode())
        for raw_id in row_ids:
            hpo_id = raw_id.decode("ascii")
            contexts[hpo_id] = _signals(_cell_text(cells[context_index]))
    return contexts


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
    ids: Iterable[str],
    labels: dict[str, str],
    contexts: dict[str, ContextSignals],
    metadata: dict[str, str],
    digest: str,
) -> str:
    """Build the public-safe phenotype note without protected cell text."""
    rows = []
    for hpo_id in ids:
        try:
            label = labels[hpo_id]
        except KeyError as error:
            raise ValueError(f"HPO ID is absent or obsolete in hp.obo: {hpo_id}") from error
        context = contexts.get(hpo_id, ())
        signals = ", ".join(context) or "no broad signal"
        rows.append(f"| `{hpo_id}` | {label} | {signals} |")

    table = "\n".join(rows)
    data_version = metadata.get("data-version", "not declared")
    return f"""# Phenotype (feat-002)

The protected DOCX was processed locally. This tracked note contains only the standardized
HPO IDs embedded in it, their public ontology labels, and broad lexical context signals—no
clinical narrative, dates, places, ages, measurements, or identifying free text.

## HPO terms

| HPO ID | Label | Presentation/Notes signals |
|---|---|---|
{table}

The signal columns are conservative keyword matches, not clinical interpretation. “No
broad signal” means none of the fixed categories matched; it does not mean the cell was
empty or uninformative. Exact wording and quantitative values remain protected locally.
Mixed proband/family signals are deliberately left unresolved and must not be converted
into phenotype-ranking weights without authorized local human review.

## Method and provenance

The IDs were mechanically matched as `HP:` followed by seven digits in
`word/document.xml`. The combined Presentation/Notes column was reduced to a fixed
vocabulary covering subject context, broad timing, and information type. Labels came from
the official [Human Phenotype Ontology OBO file]({HPO_SOURCE}).

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
    contexts = extract_context_signals(docx)
    missing_context = [hpo_id for hpo_id in ids if hpo_id not in contexts]
    if missing_context:
        raise ValueError(f"HPO IDs have no Presentation/Notes row: {missing_context}")
    labels, metadata = parse_obo(ontology)
    output.write_text(render_markdown(ids, labels, contexts, metadata, sha256(ontology)))
    return ids


def self_check() -> None:
    """Exercise extraction, deduplication, label lookup, and disclosure boundaries."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        docx = root / "synthetic.docx"
        ontology = root / "hp.obo"
        output = root / "phenotype.md"

        xml = f"""<w:document xmlns:w="{WORD_NAMESPACE}"><w:body><w:tbl>
<w:tr><w:tc><w:p><w:r><w:t>Phenotype</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HPO ID</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>Clinical Presentations / Notes</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Example one</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HP:0000001</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>The child was diagnosed after birth; private measurement was 12 cm at 37 weeks on 2026-01-01 and treated surgically</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Example two</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>HP:0000002</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>Private family pregnancy history was recurrent</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl></w:body></w:document>"""
        with zipfile.ZipFile(docx, "w") as archive:
            archive.writestr("word/document.xml", xml)
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
        assert "Private measurement" not in rendered
        assert "Private pregnancy" not in rendered
        assert "12 cm" not in rendered
        assert "37 weeks" not in rendered
        assert "2026-01-01" not in rendered
        assert "diagnosed after birth" not in rendered
        assert "quantitative detail" in rendered
        assert "family context" in rendered
    print("self-check ok: IDs and context signals resolved; protected text not emitted")


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
