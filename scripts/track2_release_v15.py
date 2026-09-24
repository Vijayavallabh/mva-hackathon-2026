#!/usr/bin/env python3
"""Falsification v15 release; retain all v1-v14 bound inputs and snapshots."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import track2_release_v14 as historical
from track2_release_v7 import Content
import track2_falsification_v15 as falsification

ROOT=historical.ROOT
require=historical.require
digest=historical.digest
previous=historical.previous

def current_path(value):
    value=value.replace('v14','v15')
    if value in {'notes/track2-evidence-v10.json','notes/track2-validation-v10.md'}:
        value=value.replace('v10','v15')
    return value

FILES={name.replace('v14','v15').replace('v10','v15') if 'v10' in source else name.replace('v14','v15'):current_path(source)
       for name,source in historical.FILES.items()}
for name in ['falsification-review','falsification-register','falsification-analysis','falsification-source-audit',
             'falsification-search','falsification-followup']:
    suffix='md' if name=='falsification-review' else 'json'
    FILES[f'{name}-v15.{suffix}']=f'notes/track2-{name}-v15.{suffix}'
INPUTS=historical.INPUTS | set(FILES.values()) | {
    'notes/track2-v15-design.md','scripts/track2_release_v15.py',
    'scripts/render_track2_slides_v15.mjs','scripts/track2_falsification_v15.py',
    'scripts/track2_falsification_retrieve_v15.py','scripts/test_track2_falsification_v15.py',
    'scripts/test_track2_release_v15.py'}
FIELDS={'schema_version','created_utc','files','input_hashes','historical_v14_manifest',
        'presentation','falsification','upload_ready','upload_performed','video_url',
        'provider_settings_verified','phase','clinical_exposure_margin'}

def presentation_checks(deck):
    parser=historical.DeckParser();parser.feed(deck);parser.close();parser.validate()
    c=Content();c.feed(deck);slides=[' '.join(x).lower() for x in c.sections]
    required={
        1:['mechanistic probe','endogenous allele effects','phase unconfirmed'],
        2:['84 archived scores','12/12 pass','8/12 fail separation','post-hoc sensitivity',
           '11/24 retained scores negative','earlier esm failures remain','no clinical classification or drug ranking'],
        3:['192 new structures','impaired controls also fold','7.10–9.10 å','auroc 0.920',
           'brca1 benchmark does not validate bub1b','alphafold3 output terms','terms notice'],
        4:['force benefit not established','loss alone does not prove harm','none establishes benefit or harm'],
        5:['excess mtor activity','impaired flux + regeneration','no post-hoc switching','units unresolved'],
        6:['hr 0.86','95% ci 0.58-1.26','p = 0.44','does not test non-cancer everolimus rescue'],
        7:['useful output / enrolled culture','pH controls'.lower(),'tracking loss separately','growth-rate artifacts'],
        8:['unknown: hold','failed: stop','preclinical review','no rescue priority','no wet-lab experiments',
           'exposure margin unknown','policies unverified'],
    }
    for n,phrases in required.items():
        for phrase in phrases:
            require(phrase in slides[n-1],f'Missing slide {n} boundary: {phrase}')
    old=(ROOT/'notes/track2-slides-v14.html').read_text()
    pattern=r'<svg id="arst1431-plot".*?</svg>'
    require(re.findall(pattern,deck,re.S)==re.findall(pattern,old,re.S),'Trial figure changed')
    require(previous.normalized(previous.acknowledgement()).lower() in slides[8],'Full acknowledgement required')
    for path in ['track2-report-v15.md','alphafold3-output-terms.md','alphafold3-Legally-Binding-Terms-of-Use.txt']:
        require(f'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/{path}' in c.links,'Missing current disclosure/terms')
    require('https://doi.org/10.1038/s41586-024-07487-w' in c.links,'Missing AF3 citation')
    require(previous.previous.previous.REMOVED_LINE not in slides[0],'Removed cover line restored')
    return dict(slides=9,vector_figures=8,visible_words=[len(x) for x in c.sections])

def check_deck():
    path=ROOT/'notes/track2-slides-v15.html'
    return dict(static_deck_verified=True,source_sha256=digest(path),**presentation_checks(path.read_text()))

def evidence_checks():
    checked=falsification.check()
    require(checked['advancement']['decision']=='hold_unresolved','Unreviewed advancement')
    ledger=json.loads((ROOT/'notes/track2-evidence-v15.json').read_text())
    old=json.loads((ROOT/'notes/track2-evidence-v10.json').read_text())
    require(ledger['schema_version']==15 and ledger['baseline_science_version']==10,'Ledger version drift')
    require({x['id']:x['decision'] for x in ledger['decisions']}=={x['id']:x['decision'] for x in old['decisions']},'Unreviewed drug promotion')
    require(len(ledger['sources'])==63 and len({x['id'] for x in ledger['sources']})==63,'Source count/identity drift')
    for name in ['phase','clinical_use','clinical_exposure_margin','direct_pair_intervention_evidence','clinical_efficacy']:
        require(ledger[name]==old[name],'Unsupported scientific change: '+name)
    model=historical.model_evidence_checks()
    report=(ROOT/'notes/track2-report-v15.md').read_text()
    for phrase in ['8/12','11/24','post-hoc sensitivity','10 mM','10 μM','1,000-fold','no rescue-priority drug',
                   'hold','growth-rate','19-claim','no independent agent or specialist review']:
        require(phrase.lower() in report.lower(),'Missing report qualification: '+phrase)
    for filename in ['track2-report-v15.md','track2-video-description-v15.md']:
        text=(ROOT/'notes'/filename).read_text()
        for phrase in ['AlphaFold3 Output Terms','Legally','modifications','10.1038/s41586-024-07487-w','Fireworks','unverified']:
            require(phrase in text,'Missing terms/disclosure')
        require(previous.normalized(text.split('## Acknowledgement\n')[1])==previous.normalized(previous.acknowledgement()),'Acknowledgement drift')
    return dict(**checked,models=model)

def scientific_checks():
    deck=check_deck();evidence_checks()
    pitch=(ROOT/'notes/track2-pitch-v15.md').read_text()
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    require(re.findall(r'### Slide (\d+) /',spoken)==list('123456789'),'Nine narration sections required')
    paragraphs=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    counts=[len(p.split()) for _,p in paragraphs]
    require(310<=sum(counts)<=375,'Narration planning budget exceeded')
    require(f'Narration contains {sum(counts)} whitespace-separated words' in pitch,'Narration count drift')
    for phrase in ['small fixed control challenge','eight of twelve','retained-function controls',
                   'conflicting ex vivo units','unknown evidence means hold','whole blood is not free tissue',
                   'not validate bub1b','no rescue priority, clinical margin or wet-lab result']:
        require(phrase in ' '.join(pitch.lower().split()),'Narration omits boundary: '+phrase)
    transcript='Track 2 v15 — read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for header,paragraph in paragraphs:
        transcript+='Slide '+header.replace(' / ',' | ')+'\n'+paragraph.strip()+'\n\n'
    require((ROOT/'notes/track2-transcript-v15.txt').read_text()==transcript,'Plain transcript drift')
    review=json.loads((ROOT/'notes/track2-v15-render-audit.json').read_text())
    require(review['source_sha256']==deck['source_sha256'],'Audited deck hash drift')
    require(review['renderer_sha256']==digest(ROOT/'scripts/render_track2_slides_v15.mjs'),'Renderer hash drift')
    require(len(review['slides'])==9 and all(not x['outside'] and not x['overlaps'] and x['min_font_px']>=24 for x in review['slides']),'Visual geometry failed')
    for output,source in [('AlphaFold3-Output-Terms.md','notes/alphafold3-output-terms.md'),
                          ('Legally-Binding-Terms-of-Use.txt','notes/alphafold3-Legally-Binding-Terms-of-Use.txt')]:
        require(review['files'][output]==digest(ROOT/source),'Rendered terms drift')
    return dict(**deck,narration_words=sum(counts),words_per_slide=counts,runtime_measured=False)

def inputs():return {s:digest(ROOT/s) for s in sorted(INPUTS)}
def history():
    p=ROOT/'results/feat009/jvv7_track2_research_v14'
    require(historical.verify(p)['integrity_verified'],'Historical verification failed')
    return digest(p/'manifest.json')
def location(path):
    path=historical.location(path)
    require(path.name!='jvv7_track2_research_v14','Historical v14 protected')
    return path

def build(path):
    path=location(path);require(not path.exists(),'Use a new directory')
    presentation=scientific_checks();evidence=evidence_checks();bound=inputs();old=history();path.mkdir()
    for name,source in FILES.items():shutil.copyfile(ROOT/source,path/name)
    manifest=dict(schema_version=15,created_utc=datetime.now(timezone.utc).isoformat(),
        files={name:digest(path/name) for name in FILES},input_hashes=bound,historical_v14_manifest=old,
        presentation=presentation,falsification=evidence,upload_ready=False,upload_performed=False,
        video_url=None,provider_settings_verified=False,phase='unconfirmed',clinical_exposure_margin=None)
    require(inputs()==bound and history()==old,'Inputs changed during copy')
    (path/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return verify(path)

def verify(path):
    path=location(path);m=json.loads((path/'manifest.json').read_text())
    previous.foundation.exact_keys(m,FIELDS,'manifest')
    timestamp=datetime.fromisoformat(m['created_utc'])
    require(timestamp.tzinfo is not None and timestamp.utcoffset().total_seconds()==0,'UTC timestamp required')
    require(m['schema_version']==15 and m['input_hashes']==inputs(),'Input/schema drift')
    require(set(m['files'])==set(FILES) and {p.name for p in path.iterdir()}==set(FILES)|{'manifest.json'},'Unexpected file set')
    for name,source in FILES.items():require(digest(path/name)==m['files'][name]==m['input_hashes'][source],'Output drift')
    require(m['historical_v14_manifest']==history(),'Historical drift')
    require(m['presentation']==scientific_checks() and m['falsification']==evidence_checks(),'Evidence/presentation drift')
    require(all(m[k] is False for k in ['upload_ready','upload_performed','provider_settings_verified']),'Readiness changed')
    require(m['video_url'] is None and m['clinical_exposure_margin'] is None and m['phase']=='unconfirmed','Scientific status changed')
    return dict(integrity_verified=True,files=len(FILES),bound_inputs=len(INPUTS),historical_v1_through_v14_preserved=True,upload_ready=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['check-deck','check','build','verify'])
    p.add_argument('output',type=Path,nargs='?');a=p.parse_args()
    if a.command in {'build','verify'}:
        if a.output is None:p.error('Output directory required')
        result={'build':build,'verify':verify}[a.command](a.output)
    else:
        if a.output is not None:p.error('Check takes no output')
        result={'check':scientific_checks,'check-deck':check_deck}[a.command]()
    print(json.dumps(result,indent=2))
