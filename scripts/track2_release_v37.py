#!/usr/bin/env python3
"""Build a new reviewed v37 snapshot; preserve all earlier bound artifacts."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import track2_release_v36 as historical
import track2_public_review_v37 as review
import check_track2_optical_v36 as optical

ROOT=historical.ROOT
require=historical.require
digest=historical.digest
PRESENTATION=['report','slides','pitch','transcript','video-description','reviewer-guide','owner-readiness','reviewer-brief','competition-strategy','harness-review','requirements','community-audit','source-review','public-review']
def new_route(source):
    for stem in PRESENTATION:
        source=source.replace('track2-'+stem+'-v36','track2-'+stem+'-v37')
    source=source.replace('track2-v36-','track2-v37-')
    return source
UPDATED={source:new_route(source) for source in historical.FILES.values() if new_route(source)!=source}
FILES={(name.replace('v36','v37') if source in UPDATED else name):UPDATED.get(source,source) for name,source in historical.FILES.items()}
EXTRA_NOTES=['competition-plan','requirements-review','lab-handoff','community-kit','judge-questions','recording-guide','demo-cases','demo-template','demo','teleprompter','demo-audit','dgx-cleanup']
for stem in EXTRA_NOTES:
    suffix='json' if stem in {'demo-cases','demo-audit'} else 'html' if stem in {'demo','demo-template','teleprompter'} else 'md'
    name='track2-'+stem+'-v37.'+suffix
    FILES[name]='notes/'+name
OPTICAL_INPUTS=set(json.loads((ROOT/'notes/track2-optical-audit-v36.json').read_text())['public_input_sha256']) | {
    'notes/track2-optical-audit-v36.json','scripts/check_track2_optical_v36.py',
    'scripts/test_track2_optical_v36.py','scripts/track2_optical_archive_review_v36.py'}
for source in sorted(p for p in OPTICAL_INPUTS if p.startswith('notes/')):
    name=Path(source).name
    require(name not in FILES or FILES[name]==source,'Output filename collision')
    FILES[name]=source
INPUTS=historical.INPUTS|OPTICAL_INPUTS|set(FILES.values())|{
    'scripts/track2_release_v37.py','scripts/test_track2_release_v37.py',
    'scripts/track2_public_review_v37.py','scripts/test_track2_public_review_v37.py',
    'scripts/track2_export_documents_v37.py','scripts/render_track2_report_v37.mjs',
    'scripts/render_track2_slides_v37.mjs','scripts/track2_bundle_v37.py',
    'scripts/audit_track2_public_v37.py','scripts/audit_track2_exports_v37.py',
    'scripts/track2_demo_v37.py','scripts/track2_demo_v37.js','scripts/test_track2_demo_v37.py',
    'scripts/build_track2_demo_v37.py','scripts/build_track2_recording_v37.py',
    'scripts/review_track2_interactive_v37.mjs','scripts/track2_community_kit_v37.py',
    'scripts/track2_dgx_cleanup_v37.py','scripts/audit_track2_demo_v37.py'}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v36_manifest',
        'optical_audit_sha256','presentation','upload_ready','upload_performed','video_url',
        'provider_settings_verified','licensing_scope_resolved','phase','clinical_exposure_margin'}


def audit_checks(render,documents,public):
    require(render['source_sha256']==digest(ROOT/'notes/track2-slides-v37.html')
        and render['renderer_sha256']==digest(ROOT/'scripts/render_track2_slides_v37.mjs'),'Slide audit drift')
    require(len(render['slides'])==9 and all(not s['outside'] and not s['overlaps'] and
        s['min_font_px']>=24 for s in render['slides']),'Slide geometry failed')
    require(render['minimum_checked_text_contrast']>=4.5 and render['pdf_pages']==9
        and render['fonts_embedded'] is True,'PDF/contrast check failed')
    require(render['narrow_screen']['width']==render['narrow_screen']['scrollWidth']==640,'Narrow layout failed')
    export,pdf=documents['export'],documents['pdf']
    require(export['report_sha256']==pdf['source_sha256']==digest(ROOT/'notes/track2-report-v37.md'),
            'Report audit drift')
    require(export['script_sha256']==pdf['exporter_sha256']==digest(ROOT/'scripts/track2_export_documents_v37.py')
        and pdf['renderer_sha256']==digest(ROOT/'scripts/render_track2_report_v37.mjs'),'Exporter audit drift')
    require(export['template_sha256']=='61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441'
        and export['answer_cells']==[f'B{n}' for n in range(7,18)],'Official workbook mapping differs')
    require(export['official_questions_unchanged'] is True and export['track1_values_and_cell_styles_preserved'] is True
        and export['formulas']==export['formula_errors']==0 and export['upload_ready'] is False,'Workbook/readiness changed')
    require(6<=documents['pages']<=14 and pdf['geometry']['width']==pdf['geometry']['scrollWidth'],
            'Report layout failed')
    require(public['passed'] is True and public['network_forbidden_by_audit_hook'] is True
        and public['data_results_logs_env_forbidden_by_audit_hook'] is True
        and public['project_environment_used'] is False,'Public-only isolation failed')
    for key,source in [('script_sha256','scripts/track2_public_review_v37.py'),
                       ('report_sha256','notes/track2-report-v37.md'),('slide_sha256','notes/track2-slides-v37.html')]:
        require(public[key]==digest(ROOT/source),'Public audit input changed')
    return dict(report_pages=documents['pages'],methods_fields=11,public_review_isolated=True,
        independent_visual_review=False,clinical_validation=False)


def interactive_checks(a):
    require(a['schema_version']==37 and a['passed'] is True,'Demo audit failed')
    for relative,sha in a['public_input_sha256'].items():
        p=Path(relative)
        require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in {'notes','scripts'},'Unsafe demo source')
        require(digest(ROOT/p)==sha,'Demo input drift: '+relative)
    required={'scripts/track2_demo_v37.py','scripts/track2_demo_v37.js',
              'scripts/track2_falsification_v21.py','notes/track2-demo-cases-v37.json',
              'notes/track2-decision-contract-v21.json','notes/track2-demo-v37.html',
              'notes/track2-teleprompter-v37.html','scripts/review_track2_interactive_v37.mjs'}
    require(required<=set(a['public_input_sha256']),'Demo audit omits required inputs')
    require(a['implementation_tests']==dict(passed=True,tests=6,
        valid_python_javascript_agreements=83,invalid_records_rejected_by_both=12),'Implementation receipt drift')
    for kind,source in [('demo','notes/track2-demo-v37.html'),('prompter','notes/track2-teleprompter-v37.html')]:
        browser=a['browser_checks'][kind]
        require(browser['passed'] is True and browser['network_blocked'] is True and
            browser['source_sha256']==digest(ROOT/source) and browser['renderer_sha256']==
            digest(ROOT/'scripts/review_track2_interactive_v37.mjs'),'Browser receipt drift')
        for viewport,width in [('desktop',1280),('mobile',390)]:
            g=browser['checks'][viewport]
            require(g['width']==g['scrollWidth']==width and g['labelledControls'] is True
                and g['networkResources']==0 and all(b['height']>=44 for b in g['buttons']),'Interactive layout failed')
    d=a['browser_checks']['demo']['checks']
    require(d['current']['decision']=='HOLD' and len(d['cases'])==18 and
            all(c['decision']==c['expected'] for c in d['cases']) and d['reset'] is True,'Teaching case drift')
    require(d['download']['decision']['clinical_recommendation'] is False,'Clinical demo promotion')
    timing=a['browser_checks']['prompter']['checks']['timing']
    require([x['seconds'] for x in timing]==[0,18,40,63,87,106,126,149,168,180] and
            [x['slide'] for x in timing]==[1,2,3,4,5,6,7,8,9,9],'Recording cue drift')
    r=a['community_kit']['isolated_replay']
    require(r['passed'] is True and r['project_environment_used'] is False and
            r['source_checkout_or_history_used'] is False and
            set(r['blocked_probes'])=={'network','process','protected_path','credentials','external_path','write'},'Kit isolation failed')
    require(all(a[k] is False for k in ['independent_review','clinical_validation','external_adoption_measured',
        'policy_validity_established','recording_created']),'Unsupported demo or delivery promotion')
    return dict(cases=18,synthetic_cases=17,current_decision='HOLD',isolated_small_kit_replay=True,
                clinical_validation=False,recording_created=False)


def scientific_checks():
    result=review.check()
    files=['track2-v37-render-audit.json','track2-v37-documents-audit.json','track2-public-review-v37.json']
    result['exports']=audit_checks(*[json.loads((ROOT/'notes'/n).read_text()) for n in files])
    result['interactive']=interactive_checks(json.loads((ROOT/'notes/track2-demo-audit-v37.json').read_text()))
    return result


def inputs():return {p:digest(ROOT/p) for p in sorted(INPUTS)}


def history():
    path=ROOT/'results/feat009/jvv7_track2_research_v36'
    require(historical.verify(path)['integrity_verified'],'Historical snapshot changed')
    return digest(path/'manifest.json')


def location(path):
    path=historical.location(path)
    require(path.name not in {f'jvv7_track2_research_v{n}' for n in range(1,37)},'Historical snapshots protected')
    return path


def manifest_checks(m):
    require(set(m)==FIELDS and m['schema_version']==37,'Unexpected manifest/version')
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
    m=dict(schema_version=37,created_utc=datetime.now(timezone.utc).isoformat(),
        files={n:digest(path/n) for n in FILES},input_hashes=bound,historical_v36_manifest=old,
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
    require(m['historical_v36_manifest']==history(),'Historical drift')
    require(m['presentation']==scientific_checks(),'Presentation/science drift')
    return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),
        historical_v1_through_v36_preserved=True,upload_ready=False)


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
