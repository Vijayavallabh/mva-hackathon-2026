#!/usr/bin/env python3
"""Integrated v22 presentation and frozen v19 research; preserve every earlier release."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import track2_release_v21 as historical
import track2_public_review_v22 as review

ROOT = historical.ROOT
require = historical.require
digest = historical.digest
UPDATED_SOURCES = {
    'notes/track2-'+name+'-v21.'+suffix:'notes/track2-'+name+'-v22.'+suffix
    for name,suffix in [('report','md'),('slides','html'),('pitch','md'),('transcript','txt'),
                        ('video-description','md'),('requirements','json'),('community-audit','json'),
                        ('public-review','json'),('reviewer-guide','md'),('owner-readiness','md'),('harness-review','md')]
}
UPDATED_SOURCES.update({f'notes/track2-v21-{kind}':f'notes/track2-v22-{kind}'
                        for kind in ['render-audit.json','documents-audit.json','editorial-review.md']})
FILES = {(name.replace('v21','v22') if source in UPDATED_SOURCES else name):
         UPDATED_SOURCES.get(source,source) for name,source in historical.FILES.items()}
for source in ['notes/track2-v22-design.md','notes/track2-v22-integration-review.md']:
    name=Path(source).name
    require(name not in FILES, 'Presentation output name collision')
    FILES[name]=source

INPUTS = historical.INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v22.py','scripts/test_track2_release_v22.py',
    'scripts/track2_public_review_v22.py','scripts/test_track2_public_review_v22.py',
    'scripts/track2_export_documents_v22.py','scripts/render_track2_report_v22.mjs',
    'scripts/render_track2_slides_v22.mjs','scripts/track2_bundle_v22.py',
    'scripts/audit_track2_public_v22.py',
}

FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes',
          'historical_v21_manifest', 'presentation', 'upload_ready', 'upload_performed',
          'video_url', 'provider_settings_verified', 'licensing_scope_resolved',
          'phase', 'clinical_exposure_margin'}


def audit_checks(render, documents, public_run):
    require(render['source_sha256'] == digest(ROOT/'notes/track2-slides-v22.html'), 'Audited deck changed')
    require(render['renderer_sha256'] == digest(ROOT/'scripts/render_track2_slides_v22.mjs'), 'Slide renderer changed')
    require(len(render['slides']) == 8 and all(not s['outside'] and not s['overlaps'] and
            s['min_font_px'] >= 24 for s in render['slides']), 'Slide geometry failed')
    require(render['minimum_checked_text_contrast'] >= 4.5, 'Text contrast failed')
    require(render['narrow_screen']['width'] == render['narrow_screen']['scrollWidth'] == 640,
            'Narrow layout failed')
    export, pdf = documents['export'], documents['pdf']
    require(export['report_sha256'] == pdf['source_sha256'] == digest(ROOT/'notes/track2-report-v22.md'),
            'Exported report changed')
    require(export['script_sha256'] == pdf['exporter_sha256'] == digest(ROOT/'scripts/track2_export_documents_v22.py'),
            'Document exporter changed')
    require(pdf['renderer_sha256'] == digest(ROOT/'scripts/render_track2_report_v22.mjs'), 'Report renderer changed')
    require(export['template_sha256'] == '61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441',
            'Official workbook changed')
    require(export['answer_cells'] == [f'B{n}' for n in range(7,18)] and export['abstract_words'] == 215,
            'Incomplete methods export')
    require(export['official_questions_unchanged'] is True and export['track1_values_and_cell_styles_preserved'] is True,
            'Official template altered')
    require(export['formulas'] == export['formula_errors'] == 0 and export['upload_ready'] is False,
            'Unsupported workbook/readiness change')
    require(documents['pages'] == 8 and pdf['geometry']['width'] == pdf['geometry']['scrollWidth'],
            'Report layout changed')
    require(public_run['passed'] is True and public_run['network_forbidden_by_audit_hook'] is True and
            public_run['data_results_logs_env_forbidden_by_audit_hook'] is True and
            public_run['project_environment_used'] is False, 'Isolated public review not verified')
    for key, source in [('script_sha256','scripts/track2_public_review_v22.py'),
                        ('report_sha256','notes/track2-report-v22.md'),
                        ('slide_sha256','notes/track2-slides-v22.html')]:
        require(public_run[key] == digest(ROOT/source), 'Public review input changed')
    return dict(report_pages=8, methods_fields=11, independent_visual_review=False,
                public_review_isolated=True, clinical_validation=False)


def scientific_checks():
    result = review.check()
    audits = [json.loads((ROOT/f'notes/{name}').read_text()) for name in
              ['track2-v22-render-audit.json','track2-v22-documents-audit.json','track2-public-review-v22.json']]
    result['exports'] = audit_checks(*audits)
    result['runtime_measured'] = False
    return result


def inputs():
    return {source:digest(ROOT/source) for source in sorted(INPUTS)}


def history():
    path = ROOT/'results/feat009/jvv7_track2_research_v21'
    require(historical.verify(path)['integrity_verified'], 'Historical verification failed')
    return digest(path/'manifest.json')


def location(path):
    path = historical.location(path)
    require(path.name not in {f'jvv7_track2_research_v{n}' for n in range(1,22)}, 'Historical versions protected')
    return path


def manifest_checks(m):
    require(set(m) == FIELDS, 'Unexpected manifest fields')
    stamp = datetime.fromisoformat(m['created_utc'])
    require(stamp.tzinfo is not None and stamp.utcoffset().total_seconds() == 0, 'UTC timestamp required')
    require(m['schema_version'] == 22, 'Wrong release version')
    require(all(m[k] is False for k in ['upload_ready','upload_performed',
            'provider_settings_verified','licensing_scope_resolved']), 'Unsupported readiness promotion')
    require(m['video_url'] is None and m['clinical_exposure_margin'] is None and
            m['phase'] == 'unconfirmed', 'Unsupported scientific/delivery change')


def build(path):
    path = location(path)
    require(not path.exists(), 'Use a new directory')
    presentation, bound, old = scientific_checks(), inputs(), history()
    path.mkdir()
    for name, source in FILES.items():
        shutil.copyfile(ROOT/source, path/name)
    m = dict(schema_version=22, created_utc=datetime.now(timezone.utc).isoformat(),
             files={name:digest(path/name) for name in FILES}, input_hashes=bound,
             historical_v21_manifest=old, presentation=presentation,
             upload_ready=False, upload_performed=False, video_url=None,
             provider_settings_verified=False, licensing_scope_resolved=False,
             phase='unconfirmed', clinical_exposure_margin=None)
    require(inputs() == bound and history() == old, 'Inputs changed during copy')
    (path/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    return verify(path)


def verify(path):
    path = location(path)
    m = json.loads((path/'manifest.json').read_text())
    manifest_checks(m)
    require(m['input_hashes'] == inputs(), 'Input drift')
    require(set(m['files']) == set(FILES) and {p.name for p in path.iterdir()} == set(FILES)|{'manifest.json'},
            'Unexpected snapshot file set')
    for name, source in FILES.items():
        require(digest(path/name) == m['files'][name] == m['input_hashes'][source], 'Output drift')
    require(m['historical_v21_manifest'] == history(), 'Historical drift')
    require(m['presentation'] == scientific_checks(), 'Presentation/evidence drift')
    return dict(integrity_verified=True, files=len(FILES), bound_inputs=len(INPUTS),
                historical_v1_through_v21_preserved=True, upload_ready=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['check-deck','check','build','verify'])
    p.add_argument('output', type=Path, nargs='?')
    a = p.parse_args()
    if a.command in {'build','verify'}:
        if a.output is None: p.error('Output directory required')
        result = {'build':build,'verify':verify}[a.command](a.output)
    else:
        if a.output is not None: p.error('Check takes no output')
        result = {'check':scientific_checks,'check-deck':review.check_deck}[a.command]()
    print(json.dumps(result,indent=2))
