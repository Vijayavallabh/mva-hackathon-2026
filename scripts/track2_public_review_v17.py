#!/usr/bin/env python3
"""Review tracked public Track 2 artifacts using the standard library only."""
from pathlib import Path
import hashlib
import json
import math
import re
import track2_release_v5 as static
from track2_release_v7 import Content
import track2_falsification_v15 as falsification

ROOT=Path(__file__).resolve().parents[1]
REVISION='aeeef5ad49f51204a7439352e59e9d310aee5e9e'
DISCUSSIONS=[1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
require=static.require

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(text):return ' '.join(text.split())
def acknowledgement():return normalized((ROOT/'notes/track2-report-v16.md').read_text().split('## Acknowledgement\n')[1])

class DeckParser(static.DeckParser):
    def validate(self):
        require(not self.stack and self.html_count==1 and self.csp_count==1,'Incomplete or unsafe HTML')
        require(self.sections==[f'slide-{n}' for n in range(1,9)],'Eight ordered slides required')
        require(self.svg_count==7 and self.section_vectors==[1]*7+[0],'Seven figures and full acknowledgement required')

def presentation_checks(deck):
    p=DeckParser();p.feed(deck);p.close();p.validate()
    c=Content();c.feed(deck);slides=[' '.join(s).lower() for s in c.sections]
    required={
        1:['everolimus','approved mtorc1 inhibitor','research hypothesis','no rescue-priority drug'],
        2:['p.leu737ter / p.asn1002lys','phase unconfirmed','allele effects unknown','neither branch established','does not replace bubr1'],
        3:['force benefit not established','late passage','hr 0.86','95% ci 0.58–1.26','p=0.44','297 evaluable','not non-cancer everolimus rescue'],
        4:['no wet-lab experiments','single / cis / trans','corrected controls','randomize + blind','independent replication','no post-hoc branch switching'],
        5:['synthetic example','not data','100 enrolled','25%','11.1%','60%','40%','not rescue','deficient-normal controls'],
        6:['unknown evidence','hold','failed safety','stop','preclinical review only','clinical exposure margin unknown','quarantined'],
        7:['impact','innovation','reuse','cpu','no subject files or gpus','fresh qualification'],
    }
    for n,phrases in required.items():
        for phrase in phrases:require(phrase in slides[n-1],f'Slide {n} omits boundary: {phrase}')
    require(acknowledgement().lower() in slides[7],'Full acknowledgement required')
    require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v17.md' in c.links,'Current report link required')
    # Common 400-pixel 0-to-100% scale for both synthetic panels.
    expected={'control-errors':100,'treated-errors':400*5/45,'control-output':240,'treated-output':160}
    for name,width in expected.items():
        match=re.search(r'<rect id="synthetic-'+name+r'"[^>]*width="([0-9.]+)"',deck)
        require(match is not None and math.isclose(float(match[1]),width,abs_tol=1e-6),'Synthetic bar or denominator drift')
    for ident,label in {'unknown':'Unknown evidence','hold':'Hold','failed':'Failed safety','stop':'Stop','all':'All requirements met','review':'Preclinical review only'}.items():
        match=re.search(r'<text id="gate-'+ident+r'"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==label,'Decision-row label drift: '+ident)
    return dict(slides=8,vector_figures=7,visible_words=[len(s) for s in c.sections])

def check_deck():
    p=ROOT/'notes/track2-slides-v17.html'
    return dict(static_deck_verified=True,source_sha256=digest(p),**presentation_checks(p.read_text()))

def methods_answers(report):
    answers={}
    for n in range(7,18):
        match=re.search(rf'\*\*B{n} — [^\n]+?\*\*\s*(.*?)(?=\n\n\*\*B\d+|\n\n## Acknowledgement)',report,re.S)
        require(match is not None,f'Missing methods B{n}')
        answers[f'B{n}']=match[1].strip()
    require(0<len(answers['B17'].split())<=500,'Abstract exceeds official limit')
    return answers

def report_checks(report):
    a=methods_answers(report)
    for text in ['no rescue-priority drug','trans phase','1,000-fold','8/12','11/24','12/12','post-hoc','0.58–1.26','p=0.44','63-source','19 claims']:
        require(text.lower() in report.lower(),'Report omits evidence qualification: '+text)
    for text in ['OpenAI','Fireworks','unverified','ColabFold','AlphaFold3','Evo2','not on-demand','raw subject']:
        require(text.lower() in a['B9'].lower(),'Required provider disclosure missing: '+text)
    require(REVISION in report,'Stale official source revision')
    require('Distribution scope remains unresolved' in report,'Distribution uncertainty omitted')
    require(normalized(report.split('## Acknowledgement\n')[1])==acknowledgement(),'Acknowledgement drift')
    require(not re.search(r'\]\((?!https://)[^)]+\)',report),'Standalone report needs absolute public links')
    return a

def requirements_checks(r,community):
    require(r['revision']==REVISION,'Official revision drift')
    require(r['rubric_weights']==dict(scientific_rigor=35,potential_impact=25,innovation=25,scalability=15),'Rubric drift')
    require(r['submission_limit']==3 and r['only_latest_reviewed'] is True and r['quota_remaining'] is None,'Quota inference')
    require(r['report_extensions']==['.pdf','.md'] and r['video_duration_seconds']==180,'Submission format drift')
    require(r['required_ai_cell']=='B9' and r['abstract_word_limit']==500,'Methods requirement drift')
    require(len(r['sources'])==10 and all(x['http_status']==200 for x in r['sources']),'Incomplete source retrieval')
    require(all(v['exact_trimmed_match'] is True for v in r['live_source_comparison'].values()),'Live/source mismatch')
    require(r['licensing_scope_resolved'] is False and r['provider_settings_verified'] is False,'Unverified compliance promotion')
    require(community['listed_numbers']==DISCUSSIONS and community['listed_count']==24 and community['closed_count']==12,'Incomplete public community coverage')
    require(community['complete'] is True and len(community['threads'])==24,'Missing thread retrieval')
    require({t['num'] for t in community['threads']}==set(DISCUSSIONS) and all(t['status']=='ok' for t in community['threads']),'Wrong/failed thread')
    require(sum(t['comments'] for t in community['threads'])==community['visible_comments']==68,'Comment coverage drift')
    require(community['reviewed_admin_attachments']==3 and community['no_hidden_edit_history_review'] is True,'Reading depth drift')
    return dict(revision=REVISION,public_discussions=24,visible_comments=68,closed_discussions=12)

def check():
    deck=check_deck()
    r=json.loads((ROOT/'notes/track2-requirements-v17.json').read_text())
    community=json.loads((ROOT/'notes/track2-community-audit-v17.json').read_text())
    requirements=requirements_checks(r,community)
    methods=report_checks((ROOT/'notes/track2-report-v17.md').read_text())
    science=falsification.check()
    ledger=json.loads((ROOT/'notes/track2-evidence-v15.json').read_text())
    baseline=json.loads((ROOT/'notes/track2-evidence-v10.json').read_text())
    require(len(ledger['sources'])==63 and len(ledger['decisions'])==11,'Evidence inventory drift')
    require({x['id']:x['decision'] for x in ledger['decisions']}=={x['id']:x['decision'] for x in baseline['decisions']},'Unreviewed drug promotion')
    pitch=(ROOT/'notes/track2-pitch-v17.md').read_text()
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    require([head[0] for head,_ in rows]==list('12345678'),'Narration slide alignment')
    counts=[len(body.split()) for _,body in rows]
    require(sum(counts)==342 and 'Narration contains 342 whitespace-separated words' in pitch,'Narration count drift')
    for phrase in ['no drug currently earns rescue priority','phase and endogenous effects remain unresolved','synthetic example','whole blood is not free tissue','preclinical review, not treatment','no subject files or gpus']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    transcript='Track 2 v17 — read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for head,body in rows:transcript+='Slide '+head.replace(' / ',' | ')+'\n'+body.strip()+'\n\n'
    require((ROOT/'notes/track2-transcript-v17.txt').read_text()==transcript.rstrip()+'\n','Plain transcript drift')
    desc=(ROOT/'notes/track2-video-description-v17.md').read_text()
    require(normalized(desc.split('## Acknowledgement\n')[1])==acknowledgement(),'Video acknowledgement drift')
    require(methods['B9'] in desc,'Video disclosure differs from report')
    return dict(passed=True,presentation_version=17,drug_science_version=15,**deck,narration_words=sum(counts),words_per_slide=counts,
                requirements=requirements,methods_fields=len(methods),abstract_words=len(methods['B17'].split()),falsification=science,
                upload_ready=False,biological_validation=False,scope='Tracked-public consistency checks; no inference, clinical or eligibility certification')

if __name__=='__main__':print(json.dumps(check(),indent=2))
