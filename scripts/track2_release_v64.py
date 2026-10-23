#!/usr/bin/env python3
"""Build a new reviewed v43 literature-integrated snapshot; preserve all earlier bound artifacts."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import track2_release_v40 as historical
import track2_public_review_v64 as review
import check_track2_optical_v36 as optical
import check_track2_literature_v45 as literature

ROOT=historical.ROOT
LITERATURE_AUDIT=json.loads((historical.ROOT/'notes/track2-literature-audit-v45.json').read_text())
require=historical.require
digest=historical.digest
OPTICAL_INPUTS=historical.OPTICAL_INPUTS
# Reuse source captures, adjudications, demo and all research without new copies.
PRESENTATION=['report','slides','pitch','transcript','video-description','reviewer-guide',
    'owner-readiness','reviewer-brief','competition-strategy','harness-review',
    'lab-handoff','community-kit','judge-questions','recording-guide','teleprompter',
    'external-review-packet','public-review','prompter-audit']
def new_route(source):
    for stem in PRESENTATION:
        source=source.replace('track2-'+stem+'-v39','track2-'+stem+'-v40')
    # Reuse historical editorial reviews; the current design note documents this revision.
    for stem in ['design','render-audit','documents-audit']:
        source=source.replace('track2-v39-'+stem,'track2-v40-'+stem)
    return source
FILES={(name.replace('v39','v40') if new_route(source)!=source else name):new_route(source)
       for name,source in historical.FILES.items()}
FILES['track2-narration-v40.json']='notes/track2-narration-v40.json'
for name in ['track2-literature-v45.md','track2-literature-audit-v45.json']:
    FILES[name]='notes/'+name
for source in LITERATURE_AUDIT['selected_sources']:
    if source['receipt']:
        receipt=Path(source['receipt'])
        FILES[receipt.name]=source['receipt']
FILES['track2-report-v49.md']='notes/track2-report-v64.md'
FILES['track2-slides-v49.html']='notes/track2-slides-v64.html'
FILES['track2-external-review-packet-v43.md']='notes/track2-external-review-packet-v43.md'
FILES['track2-reviewer-brief-v43.md']='notes/track2-reviewer-brief-v43.md'
FILES['track2-video-description-v47.md']='notes/track2-video-description-v47.md'
FILES['track2-judge-questions-v43.md']='notes/track2-judge-questions-v43.md'
FILES['track2-community-kit-v42.md']='notes/track2-community-kit-v42.md'
FILES['track2-community-kit-v37.md']='notes/track2-community-kit-v37.md'
FILES['track2-recording-guide-v46.md']='notes/track2-recording-guide-v46.md'
FILES['track2-competition-strategy-v42.md']='notes/track2-competition-strategy-v42.md'
FILES['track2-lab-handoff-v43.md']='notes/track2-lab-handoff-v43.md'
FILES['track2-candidate-comparison-v51.md']='notes/track2-candidate-comparison-v51.md'
SCRIPTS=['track2_release_v64.py','test_track2_release_v64.py',
    'track2_public_review_v64.py','test_track2_public_review_v64.py',
    'track2_export_documents_v64.py','render_track2_report_v64.mjs',
    'render_track2_slides_v64.mjs','track2_bundle_v64.py',
    'audit_track2_public_v43.py','audit_track2_exports_v43.py',
    'check_track2_requirements_v52.py','test_track2_requirements_v52.py',
    'check_track2_submission_prep_v3.py','test_track2_submission_prep_v3.py',
    'check_track2_literature_v45.py','test_track2_literature_v45.py']
# Harness check/audit/test scripts execute the snapshot, so binding their hashes here would make every current harness update invalidate the immediately preceding snapshot. They remain public and are bound by the v48 harness review/audit instead.
INPUTS=historical.INPUTS|set(FILES.values())|{'scripts/'+s for s in SCRIPTS}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v40_manifest',
        'optical_audit_sha256','presentation','upload_ready','upload_performed','video_url',
        'provider_settings_verified','licensing_scope_resolved','phase','clinical_exposure_margin'}


def audit_checks(render,documents,public):
    require(render['source_sha256']==digest(ROOT/'notes/track2-slides-v64.html')
        and render['renderer_sha256']==digest(ROOT/'scripts/render_track2_slides_v64.mjs'),'Slide audit drift')
    require(len(render['slides'])==9 and all(not s['outside'] and not s['overlaps'] and
        s['min_font_px']>=24 for s in render['slides']),'Slide geometry failed')
    require(render['minimum_checked_text_contrast']>=4.5 and render['pdf_pages']==9
        and render['fonts_embedded'] is True,'PDF/contrast check failed')
    require(render['narrow_screen']['width']==render['narrow_screen']['scrollWidth']==640,'Narrow layout failed')
    export,pdf=documents['export'],documents['pdf']
    require(export['report_sha256']==pdf['source_sha256']==digest(ROOT/'notes/track2-report-v64.md'),
            'Report audit drift')
    require(export['script_sha256']==pdf['exporter_sha256']==digest(ROOT/'scripts/track2_export_documents_v64.py')
        and pdf['renderer_sha256']==digest(ROOT/'scripts/render_track2_report_v64.mjs'),'Exporter audit drift')
    require(export['template_sha256']=='61aab080a2868a3b724e76692b83c24812112e305cd3a8b03f8f91a6b2414441'
        and export['answer_cells']==[f'B{n}' for n in range(7,18)],'Official workbook mapping differs')
    require(export['official_questions_unchanged'] is True and export['track1_values_and_cell_styles_preserved'] is True
        and export['formulas']==export['formula_errors']==0 and export['upload_ready'] is False,'Workbook/readiness changed')
    require(6<=documents['pages']<=19 and pdf['geometry']['width']==pdf['geometry']['scrollWidth'],
            'Report layout failed')
    require(documents['pdf_title']=='jvv7 · Track 2 report v64' and
            documents['title_independent_check_passed'] is True,
            'Uploaded-report title is stale or independently unverified')
    require(public['passed'] is True and public['presentation_version']==64,'Public review failed')
    return dict(report_pages=documents['pages'],report_pdf_title=documents['pdf_title'],methods_fields=11,
        render_pdf_pages=render['pdf_pages'],minimum_checked_text_contrast=render['minimum_checked_text_contrast'],
        independent_visual_review=False,clinical_validation=False)

def recording_checks(a):
    require(a['schema_version']==40 and a['passed'] is True,'Recording audit failed')
    required={'notes/track2-pitch-v46.md','notes/track2-transcript-v46.txt',
        'notes/track2-teleprompter-v46.html','scripts/build_track2_recording_v46.py',
        'scripts/review_track2_interactive_v46.mjs','scripts/audit_track2_recording_v46.py',
        'scripts/track2_narration_v46.py','notes/track2-recording-guide-v46.md','notes/track2-narration-v46.json'}
    require(set(a['public_input_sha256'])==required,'Recording inputs omitted or unexpected')
    for relative,sha in a['public_input_sha256'].items():
        require(digest(ROOT/relative)==sha,'Recording input drift: '+relative)
    browser=a['browser_checks']
    require(browser['passed'] is True and browser['network_blocked'] is True and
        browser['source_sha256']==digest(ROOT/'notes/track2-teleprompter-v46.html') and
        browser['renderer_sha256']==digest(ROOT/'scripts/review_track2_interactive_v46.mjs'),
        'Recording browser receipt drift')
    for viewport,width in [('desktop',1280),('mobile',390)]:
        g=browser['checks'][viewport]
        require(g['width']==g['scrollWidth']==width and g['labelledControls'] is True and
            g['networkResources']==0 and all(b['height']>=44 for b in g['buttons']),
            'Recording layout failed')
    for viewport in ['desktopCues','mobileCues']:
        rows=browser['checks'][viewport]
        require([r['seconds'] for r in rows]==[0,18,40,63,87,106,126,149,168] and
            all(r['top']>=r['headerBottom'] for r in rows),'Active cue hidden by header')
    timing=browser['checks']['timing']
    require([x['seconds'] for x in timing]==[0,18,40,63,87,106,126,149,168,180] and
        [x['slide'] for x in timing]==[1,2,3,4,5,6,7,8,9,9],'Recording cue drift')
    require(all(a[k] is False for k in ['recording_created','runtime_measured','independent_review']),
        'Rehearsal is not a measured recording or outside review')
    return dict(cues=9,allocation_seconds=180,recording_created=False,runtime_measured=False)


def scientific_checks():
    result=review.check()
    files=['track2-v64-render-audit-v1.json','track2-v64-documents-audit-v1.json','track2-public-review-v64.json']
    result['exports']=audit_checks(*[json.loads((ROOT/'notes'/n).read_text()) for n in files])
    result['interactive']=historical.historical.historical.interactive_checks(json.loads((ROOT/'notes/track2-demo-audit-v37.json').read_text()))
    result['recording']=recording_checks(json.loads((ROOT/'notes/track2-prompter-audit-v46.json').read_text()))
    result['literature_v45']=literature.check()
    return result


def inputs():return {p:digest(ROOT/p) for p in sorted(INPUTS)}


def history():
    path=ROOT/'results/feat009/jvv7_track2_research_v40'
    require(historical.verify(path)['integrity_verified'],'Historical snapshot changed')
    return digest(path/'manifest.json')


def location(path):
    path=historical.location(path)
    require(path.name not in {f'jvv7_track2_research_v{n}' for n in range(1,41)},'Historical snapshots protected')
    return path


def manifest_checks(m):
    require(set(m)==FIELDS and m['schema_version']==47,'Unexpected manifest/version')
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
    m=dict(schema_version=47,created_utc=datetime.now(timezone.utc).isoformat(),
        files={n:digest(path/n) for n in FILES},input_hashes=bound,historical_v40_manifest=old,
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
    require(m['historical_v40_manifest']==history(),'Historical drift')
    require(m['presentation']==scientific_checks(),'Presentation/science drift')
    return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),
        historical_v1_through_v40_preserved=True,upload_ready=False)


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
