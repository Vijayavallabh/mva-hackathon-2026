#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf==1.26.4"]
# ///
"""Bind completed local v28 exports after manual visual inspection; never overwrite audits."""
import hashlib
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / 'results/feat009/v28-slides-final-20261001'
DOCS = ROOT / 'results/feat009/v28-documents-final-20261001'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def luminance(color):
    channels = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4 for v in channels]
    return sum(a*b for a, b in zip(linear, (0.2126, 0.7152, 0.0722)))


def main():
    destinations = [ROOT/f'notes/track2-v28-{kind}-audit.json' for kind in ('render', 'documents')]
    if any(p.exists() or p.is_symlink() for p in destinations):
        raise ValueError('Existing audits are protected')
    render = json.loads((SLIDES/'render.json').read_text())
    export = json.loads((DOCS/'documents.json').read_text())
    pdf = json.loads((DOCS/'report-render.json').read_text())
    for folder, files in [(SLIDES, render['files']), (DOCS, export['files']), (DOCS, pdf['files'])]:
        for name, sha in files.items():
            if Path(name).name != name or (folder/name).is_symlink() or digest(folder/name) != sha:
                raise ValueError('Export changed: '+name)
    if render['source_sha256'] != digest(ROOT/'notes/track2-slides-v28.html'):
        raise ValueError('Deck source changed')
    if export['report_sha256'] != pdf['source_sha256'] or pdf['source_sha256'] != digest(ROOT/'notes/track2-report-v28.md'):
        raise ValueError('Report source changed')
    for recorded, path in [(render['renderer_sha256'], 'scripts/render_track2_slides_v28.mjs'),
                           (pdf['renderer_sha256'], 'scripts/render_track2_report_v28.mjs'),
                           (export['script_sha256'], 'scripts/track2_export_documents_v28.py')]:
        if recorded != digest(ROOT/path):
            raise ValueError('Exporter/renderer changed')
    with fitz.open(SLIDES/'track2-slides-v28.pdf') as deck:
        if len(deck) != 9:
            raise ValueError('Slide PDF page count')
        fonts = {f[0] for page in deck for f in page.get_fonts()}
        if not fonts or any(not deck.extract_font(x)[3] for x in fonts):
            raise ValueError('Unembedded PDF font')
        render.update(pdf_pages=len(deck), fonts_embedded=True)
    # Actual palette pairs used by this static deck; no claim to a general CSS accessibility audit.
    pairs = [(fg, '#f7fafc') for fg in ['#142c3c', '#4c6370', '#176359', '#48419d']]
    pairs += [('#ffffff', '#123a40'), ('#d8eee5', '#123a40'),
              ('#ffffff', '#176359'), ('#ffffff', '#48419d'),
              ('#48419d', '#eae9f6'), ('#142c3c', '#eae9f6'), ('#4c6370', '#eae9f6'),
              ('#176359', '#d8eee5')]
    contrasts = []
    for fg, bg in pairs:
        a, b = sorted([luminance(fg), luminance(bg)])
        contrasts.append(dict(foreground=fg, background=bg, ratio=(b+0.05)/(a+0.05)))
    render['contrast_checks'] = contrasts
    render['minimum_checked_text_contrast'] = min(p['ratio'] for p in contrasts)
    if render['minimum_checked_text_contrast'] < 4.5:
        raise ValueError('Palette contrast')
    if len(render['slides']) != 9 or any(s['outside'] or s['overlaps'] or s['min_font_px'] < 24 for s in render['slides']):
        raise ValueError('Slide geometry')
    with fitz.open(DOCS/'jvv7_track2_report_v28.pdf') as report:
        text = ' '.join(' '.join(p.get_text().split()) for p in report)
        if len(report) != 12 or any(term not in text for term in ['1,184', '0.1510', '179,968', '42 claim records', 'We acknowledge their trust']):
            raise ValueError('Report page/text integrity')
        pages = len(report)
    render['author_visual_review'] = 'All nine final slides inspected in a contact sheet; changed result slides also inspected at full resolution. No independent reviewer.'
    documents = dict(document_directory=str(DOCS.relative_to(ROOT)), export=export, pdf=pdf, pages=pages,
        author_visual_review='All twelve final report pages inspected in contact sheets; new sensitivity table and protein background text inspected at full resolution. Seven tables and full acknowledgement retained. Workbook values/styles round-trip checked; workbook appearance not rendered.',
        independent_visual_review=False, clinical_validation=False)
    for path, content in zip(destinations, [render, documents]):
        with path.open('x') as f:
            f.write(json.dumps(content, indent=2)+'\n')
    print(json.dumps(dict(slides=9, report_pages=pages, minimum_checked_text_contrast=render['minimum_checked_text_contrast'],
                         output=[str(p.relative_to(ROOT)) for p in destinations]), indent=2))


if __name__ == '__main__':
    main()
