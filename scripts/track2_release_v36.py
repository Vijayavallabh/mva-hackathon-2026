#!/usr/bin/env python3
"""Build a new reviewed v36 snapshot; preserve all earlier bound artifacts."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import track2_release_v34 as historical
import track2_public_review_v36 as review
import check_track2_optical_v36 as optical

ROOT=historical.ROOT
require=historical.require
digest=historical.digest
UPDATED={source:source.replace('v34','v36') for source in historical.FILES.values() if 'v34' in source}
FILES={(name.replace('v34','v36') if source in UPDATED else name):UPDATED.get(source,source)
       for name,source in historical.FILES.items()}
OPTICAL_INPUTS=set(json.loads((ROOT/'notes/track2-optical-audit-v36.json').read_text())['public_input_sha256']) | {
    'notes/track2-optical-audit-v36.json','scripts/check_track2_optical_v36.py',
    'scripts/test_track2_optical_v36.py','scripts/track2_optical_archive_review_v36.py'}
for source in sorted(p for p in OPTICAL_INPUTS if p.startswith('notes/')):
    name=Path(source).name
    require(name not in FILES or FILES[name]==source,'Output filename collision')
    FILES[name]=source
INPUTS=historical.INPUTS|OPTICAL_INPUTS|set(FILES.values())|{
    'scripts/track2_release_v36.py','scripts/test_track2_release_v36.py',
    'scripts/track2_public_review_v36.py','scripts/test_track2_public_review_v36.py',
    'scripts/track2_export_documents_v36.py','scripts/render_track2_report_v36.mjs',
    'scripts/render_track2_slides_v36.mjs','scripts/track2_bundle_v36.py',
    'scripts/audit_track2_public_v36.py','scripts/audit_track2_exports_v36.py'}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v34_manifest',
        'optical_audit_sha256','presentation','upload_ready','upload_performed','video_url',
        'provider_settings_verified','licensing_scope_resolved','phase','clinical_exposure_margin'}


def audit_checks(render,documents,public):
    require(render['source_sha256']==digest(ROOT/'notes/track2-slides-v36.html')
        and render['renderer_sha256']==digest(ROOT/'scripts/render_track2_slides_v36.mjs'),'Slide audit drift')
    require(len(render['slides'])==9 and all(not s['outside'] and not s['overlaps'] and
        s['min_font_px']>=24 for s in render['slides']),'Slide geometry failed')
    require(render['minimum_checked_text_contrast']>=4.5 and render['pdf_pages']==9
        and render['fonts_embedded'] is True,'PDF/contrast check failed')
    require(render['narrow_screen']['width']==render['narrow_screen']['scrollWidth']==640,'Narrow layout failed')
    export,pdf=documents['export'],documents['pdf']
    require(export['report_sha256']==pdf['source_sha256']==digest(ROOT/'notes/track2-report-v36.md'),
            'Report audit drift')
    require(export['script_sha256']==pdf['exporter_sha256']==digest(ROOT/'scripts/track2_export_documents_v36.py')
        and pdf['renderer_sha256']==digest(ROOT/'scripts/render_track2_report_v36.mjs'),'Exporter audit drift')
    require(export['template_sha256']=='61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441'
        and export['answer_cells']==[f'B{n}' for n in range(7,18)],'Official workbook mapping differs')
    require(export['official_questions_unchanged'] is True and export['track1_values_and_cell_styles_preserved'] is True
        and export['formulas']==export['formula_errors']==0 and export['upload_ready'] is False,'Workbook/readiness changed')
    require(6<=documents['pages']<=14 and pdf['geometry']['width']==pdf['geometry']['scrollWidth'],
            'Report layout failed')
    require(public['passed'] is True and public['network_forbidden_by_audit_hook'] is True
        and public['data_results_logs_env_forbidden_by_audit_hook'] is True
        and public['project_environment_used'] is False,'Public-only isolation failed')
    for key,source in [('script_sha256','scripts/track2_public_review_v36.py'),
                       ('report_sha256','notes/track2-report-v36.md'),('slide_sha256','notes/track2-slides-v36.html')]:
        require(public[key]==digest(ROOT/source),'Public audit input changed')
    return dict(report_pages=documents['pages'],methods_fields=11,public_review_isolated=True,
        independent_visual_review=False,clinical_validation=False)


def scientific_checks():
    result=review.check()
    files=['track2-v36-render-audit.json','track2-v36-documents-audit.json','track2-public-review-v36.json']
    result['exports']=audit_checks(*[json.loads((ROOT/'notes'/n).read_text()) for n in files])
    return result


def inputs():return {p:digest(ROOT/p) for p in sorted(INPUTS)}


def history():
    path=ROOT/'results/feat009/jvv7_track2_research_v34'
    require(historical.verify(path)['integrity_verified'],'Historical snapshot changed')
    return digest(path/'manifest.json')


def location(path):
    path=historical.location(path)
    require(path.name not in {f'jvv7_track2_research_v{n}' for n in range(1,36)},'Historical snapshots protected')
    return path


def manifest_checks(m):
    require(set(m)==FIELDS and m['schema_version']==36,'Unexpected manifest/version')
    stamp=datetime.fromisoformat(m['created_utc'])
    require(stamp.tzinfo is not None and stamp.utcoffset().total_seconds()==0,'UTC timestamp required')
    require(m['optical_audit_sha256']==optical.AUDIT_SHA256,'Optical audit differs')
    require(all(m[k] is False for k in ['upload_ready','upload_performed','provider_settings_verified','licensing_scope_resolved']),
            'Unsupported readiness promotion')
    require(m['video_url'] is None and m['clinical_exposure_margin'] is None and m['phase']=='unconfirmed',
            'Unsupported scientific/delivery promotion')


def build(path):
    path=location(path);require(not path.exists(),'Use a new snapshot directory')
    presentation,bound,old=scientific_checks(),inputs(),history()
    path.mkdir()
    for name,source in FILES.items():shutil.copyfile(ROOT/source,path/name)
    m=dict(schema_version=36,created_utc=datetime.now(timezone.utc).isoformat(),
        files={n:digest(path/n) for n in FILES},input_hashes=bound,historical_v34_manifest=old,
        optical_audit_sha256=optical.AUDIT_SHA256,presentation=presentation,upload_ready=False,
        upload_performed=False,video_url=None,provider_settings_verified=False,licensing_scope_resolved=False,
        phase='unconfirmed',clinical_exposure_margin=None)
    require(inputs()==bound and history()==old,'Inputs changed during snapshot')
    (path/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    return verify(path)


def verify(path):
    path=location(path);m=json.loads((path/'manifest.json').read_text());manifest_checks(m)
    require(m['input_hashes']==inputs(),'Bound input drift')
    require(set(m['files'])==set(FILES) and {p.name for p in path.iterdir()}==set(FILES)|{'manifest.json'},
            'Unexpected snapshot files')
    for name,source in FILES.items():
        require(digest(path/name)==m['files'][name]==m['input_hashes'][source],'Snapshot output drift')
    require(m['historical_v34_manifest']==history(),'Historical drift')
    require(m['presentation']==scientific_checks(),'Presentation/science drift')
    return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),
        historical_v1_through_v34_preserved=True,upload_ready=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check-deck','check','build','verify'])
    p.add_argument('output',type=Path,nargs='?');a=p.parse_args()
    if a.command in {'build','verify'}:
        if a.output is None:p.error('New output directory required')
        result={'build':build,'verify':verify}[a.command](a.output)
    else:
        if a.output is not None:p.error('Check takes no output')
        result={'check':scientific_checks,'check-deck':review.check_deck}[a.command]()
    print(json.dumps(result,indent=2))
