#!/usr/bin/env python3
"""Integrated v32 presentation and frozen v19/v23/v25/v27/v29 research; preserve every earlier release."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import track2_release_v30 as historical
import track2_public_review_v32 as review

ROOT = historical.ROOT
require = historical.require
digest = historical.digest
UPDATED_SOURCES = {
    'notes/track2-'+name+'-v30.'+suffix:'notes/track2-'+name+'-v32.'+suffix
    for name,suffix in [('report','md'),('slides','html'),('pitch','md'),('transcript','txt'),
                        ('video-description','md'),('requirements','json'),('community-audit','json'),
                        ('public-review','json'),('reviewer-guide','md'),('owner-readiness','md'),('harness-review','md')]
}
UPDATED_SOURCES.update({f'notes/track2-v30-{kind}':f'notes/track2-v32-{kind}'
                        for kind in ['render-audit.json','documents-audit.json','editorial-review.md','design.md','integration-review.md']})
FILES = {(name.replace('v30','v32') if source in UPDATED_SOURCES else name):
         UPDATED_SOURCES.get(source,source) for name,source in historical.FILES.items()}
RNAI_INPUTS=historical.RNAI_INPUTS
CRISPR_INPUTS=set(json.loads((ROOT/'notes/track2-crispr-audit-v25.json').read_text())['public_input_sha256']) | {'notes/track2-crispr-audit-v25.json'}
FALSIFICATION_INPUTS=set(json.loads((ROOT/'notes/track2-falsification-audit-v27.json').read_text())['public_input_sha256']) | {'notes/track2-falsification-audit-v27.json'}
ORTHOGONAL_INPUTS=set(json.loads((ROOT/'notes/track2-orthogonal-audit-v29.json').read_text())['public_input_sha256']) | {'notes/track2-orthogonal-audit-v29.json'}
FILES['track2-source-review-v32.md']='notes/track2-source-review-v32.md'
PERTURBSEQ_INPUTS=set(json.loads((ROOT/'notes/track2-perturbseq-audit-v31.json').read_text())['public_input_sha256']) | {'notes/track2-perturbseq-audit-v31.json'}
for source in sorted(p for p in PERTURBSEQ_INPUTS if p.startswith('notes/')):
    name=Path(source).name
    require(name not in FILES, 'Presentation output name collision')
    FILES[name]=source

INPUTS = historical.INPUTS | RNAI_INPUTS | CRISPR_INPUTS | FALSIFICATION_INPUTS | ORTHOGONAL_INPUTS | PERTURBSEQ_INPUTS | set(FILES.values()) | {
    'scripts/track2_release_v32.py','scripts/test_track2_release_v32.py',
    'scripts/track2_public_review_v32.py','scripts/test_track2_public_review_v32.py',
    'scripts/track2_export_documents_v32.py','scripts/render_track2_report_v32.mjs',
    'scripts/render_track2_slides_v32.mjs','scripts/track2_bundle_v32.py',
    'scripts/audit_track2_public_v32.py','scripts/audit_track2_exports_v32.py',
}

FIELDS = {'schema_version', 'created_utc', 'files', 'input_hashes',
          'historical_v30_manifest', 'rnai_audit_sha256', 'crispr_audit_sha256', 'falsification_audit_sha256', 'orthogonal_audit_sha256', 'perturbseq_audit_sha256', 'presentation', 'upload_ready', 'upload_performed',
          'video_url', 'provider_settings_verified', 'licensing_scope_resolved',
          'phase', 'clinical_exposure_margin'}


def audit_checks(render, documents, public_run):
    require(render['source_sha256'] == digest(ROOT/'notes/track2-slides-v32.html'), 'Audited deck changed')
    require(render['renderer_sha256'] == digest(ROOT/'scripts/render_track2_slides_v32.mjs'), 'Slide renderer changed')
    require(len(render['slides']) == 9 and all(not s['outside'] and not s['overlaps'] and
            s['min_font_px'] >= 24 for s in render['slides']), 'Slide geometry failed')
    require(render['minimum_checked_text_contrast'] >= 4.5, 'Text contrast failed')
    require(render['narrow_screen']['width'] == render['narrow_screen']['scrollWidth'] == 640,
            'Narrow layout failed')
    export, pdf = documents['export'], documents['pdf']
    require(export['report_sha256'] == pdf['source_sha256'] == digest(ROOT/'notes/track2-report-v32.md'),
            'Exported report changed')
    require(export['script_sha256'] == pdf['exporter_sha256'] == digest(ROOT/'scripts/track2_export_documents_v32.py'),
            'Document exporter changed')
    require(pdf['renderer_sha256'] == digest(ROOT/'scripts/render_track2_report_v32.mjs'), 'Report renderer changed')
    require(export['template_sha256'] == '61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441',
            'Official workbook changed')
    require(export['answer_cells'] == [f'B{n}' for n in range(7,18)] and export['abstract_words'] == len(review.methods_answers((ROOT/'notes/track2-report-v32.md').read_text())['B17'].split()),
            'Incomplete methods export')
    require(export['official_questions_unchanged'] is True and export['track1_values_and_cell_styles_preserved'] is True,
            'Official template altered')
    require(export['formulas'] == export['formula_errors'] == 0 and export['upload_ready'] is False,
            'Unsupported workbook/readiness change')
    require(documents['pages'] == 16 and pdf['geometry']['width'] == pdf['geometry']['scrollWidth'],
            'Report layout changed')
    require(public_run['passed'] is True and public_run['network_forbidden_by_audit_hook'] is True and
            public_run['data_results_logs_env_forbidden_by_audit_hook'] is True and
            public_run['project_environment_used'] is False, 'Isolated public review not verified')
    for key, source in [('script_sha256','scripts/track2_public_review_v32.py'),
                        ('report_sha256','notes/track2-report-v32.md'),
                        ('slide_sha256','notes/track2-slides-v32.html')]:
        require(public_run[key] == digest(ROOT/source), 'Public review input changed')
    return dict(report_pages=16, methods_fields=11, independent_visual_review=False,
                public_review_isolated=True, clinical_validation=False)


def scientific_checks():
    result = review.check()
    audits = [json.loads((ROOT/f'notes/{name}').read_text()) for name in
              ['track2-v32-render-audit.json','track2-v32-documents-audit.json','track2-public-review-v32.json']]
    result['exports'] = audit_checks(*audits)
    result['runtime_measured'] = False
    return result


def inputs():
    return {source:digest(ROOT/source) for source in sorted(INPUTS)}


def history():
    path = ROOT/'results/feat009/jvv7_track2_research_v30'
    require(historical.verify(path)['integrity_verified'], 'Historical verification failed')
    return digest(path/'manifest.json')


def location(path):
    path = historical.location(path)
    require(path.name not in {f'jvv7_track2_research_v{n}' for n in range(1,32)}, 'Historical versions protected')
    return path


def manifest_checks(m):
    require(set(m) == FIELDS, 'Unexpected manifest fields')
    stamp = datetime.fromisoformat(m['created_utc'])
    require(stamp.tzinfo is not None and stamp.utcoffset().total_seconds() == 0, 'UTC timestamp required')
    require(m['schema_version'] == 32, 'Wrong release version')
    require(m['perturbseq_audit_sha256']==review.PERTURBSEQ_AUDIT_SHA256, 'V31 audit drift')
    require(m['orthogonal_audit_sha256']==review.ORTHOGONAL_AUDIT_SHA256, 'V29 audit drift')
    require(m['rnai_audit_sha256']==review.RNAI_AUDIT_SHA256, 'RNAi audit drift')
    require(m['crispr_audit_sha256']==review.CRISPR_AUDIT_SHA256, 'CRISPR audit drift')
    require(m['falsification_audit_sha256']==review.FALSIFICATION_AUDIT_SHA256, 'V27 audit drift')
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
    m = dict(schema_version=32, created_utc=datetime.now(timezone.utc).isoformat(),
             files={name:digest(path/name) for name in FILES}, input_hashes=bound,
             historical_v30_manifest=old, rnai_audit_sha256=review.RNAI_AUDIT_SHA256, crispr_audit_sha256=review.CRISPR_AUDIT_SHA256, falsification_audit_sha256=review.FALSIFICATION_AUDIT_SHA256, orthogonal_audit_sha256=review.ORTHOGONAL_AUDIT_SHA256, perturbseq_audit_sha256=review.PERTURBSEQ_AUDIT_SHA256, presentation=presentation,
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
    require(m['historical_v30_manifest'] == history(), 'Historical drift')
    require(m['presentation'] == scientific_checks(), 'Presentation/evidence drift')
    return dict(integrity_verified=True, files=len(FILES), bound_inputs=len(INPUTS),
                historical_v1_through_v30_preserved=True, upload_ready=False)


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
