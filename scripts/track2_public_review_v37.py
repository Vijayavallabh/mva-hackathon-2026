#!/usr/bin/env python3
"""Review the rubric-directed v37 proposal, demo and retained v36 science offline."""
import json
from pathlib import Path
import re
import track2_public_review_v36 as prior
import track2_demo_v37 as demo
import build_track2_demo_v37 as builder

ROOT=prior.ROOT
REVISION=prior.REVISION
require=prior.require
digest=prior.digest
normalized=prior.normalized
methods_answers=prior.methods_answers
acknowledgement=prior.acknowledgement
repository_links=prior.repository_links


def presentation_checks(deck):
    result=prior.presentation_checks(deck.replace('track2-report-v37','track2-report-v36'))
    for phrase in ['18 evidence cases','17 synthetic cases','actual unmeasured','no new family sample','fresh qualification','offline examples']:
        require(phrase in deck.lower(),'Contribution boundary missing: '+phrase)
    return result


def check_deck():
    path=ROOT/'notes/track2-slides-v37.html'
    return dict(static_deck_verified=True,source_sha256=digest(path),**presentation_checks(path.read_text()))


def report_checks(report):
    answers=prior.report_checks(report)
    text=normalized(report).lower()
    for phrase in ['first qualification question','separately justified alternative','four separate links',
                   '17 synthetic cases and one actual unmeasured state','benefit-only rule advances 11',
                   'viability still advances 9','83 valid checks','12 invalid records',
                   'not a representative','not been co-developed with the family',
                   'synthetic margins cannot qualify','diagnostic use would still require']:
        require(phrase in text,'Rubric/limitations drift: '+phrase)
    return answers


def requirements_checks(r,c):
    require(r['revision']==REVISION and r['schema_version']==37,'Wrong current source revision')
    require(r['rubric_weights']==dict(scientific_rigor=35,potential_impact=25,innovation=25,scalability=15),'Rubric drift')
    require(r['submission_limit']==3 and r['only_latest_reviewed'] and r['quota_remaining'] is None,'Quota inference')
    require(r['deadline_utc']=='2026-10-24T23:59:00Z' and r['data_deletion_deadline']=='2026-11-23','Deadline drift')
    require(r['video_duration_seconds']==180 and r['required_ai_cell']=='B9' and r['abstract_word_limit']==500,'Deliverable drift')
    require(len(r['sources'])==7 and all(s['http_status']==200 and s['unchanged'] for s in r['sources']),'Source retrieval drift')
    require(c['listed_count']==len(c['threads'])==30 and c['closed_count']==14 and c['complete'],'Thread coverage drift')
    require(c['listed_numbers']==list(range(1,9))+list(range(10,32)),'Missing public thread')
    require(sum(x['comments'] for x in c['threads'])==c['visible_comments']==84 and all(x['status']=='ok' for x in c['threads']),'Comment/fetch drift')
    require(c['new_or_edited_comments']==1 and c['independent_review'] is False,'Reading-depth drift')
    require(r['licensing_scope_resolved'] is False and r['provider_settings_verified'] is False,'Unsupported readiness')
    return dict(revision=REVISION,public_discussions=30,visible_comments=84,closed_discussions=14)


def narration(pitch):
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    require([h[0] for h,_ in rows]==list('123456789'),'Narration alignment drift')
    counts=[len(b.split()) for _,b in rows]
    require(300<=sum(counts)<=400 and f'Narration contains {sum(counts)} whitespace-separated words' in pitch,'Narration word drift')
    times=[re.search(r'/ (\d+):(\d+)-(\d+):(\d+) /',h).groups() for h,_ in rows]
    ranges=[(60*int(a)+int(b),60*int(c)+int(d)) for a,b,c,d in times]
    require(ranges[0][0]==0 and ranges[-1][1]==180 and all(ranges[i][1]==ranges[i+1][0] for i in range(8)),'Noncontiguous timing')
    for phrase in ['no drug earns rescue priority','phase and endogenous effects remain unresolved','neither branch is established',
                   'independent perturbation and restoration','this example is synthetic','track every cell',
                   'early relative sensitivity can reverse','whole blood is not free tissue','preclinical review only',
                   'invalid assays hold inference','injury stops advancement','no wet-lab experiment has been performed',
                   'hcq remains reserve','eighteen evidence cases','without requesting another family sample']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    transcript='Track 2 v37 - read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for h,b in rows:transcript+='Slide '+h.replace(' / ',' | ')+'\n'+b.strip()+'\n\n'
    return counts,transcript.rstrip()+'\n'


def check():
    old=prior.check()
    visual=check_deck()
    report=(ROOT/'notes/track2-report-v37.md').read_text();answers=report_checks(report)
    prior.optical_numbers(json.loads((ROOT/'notes/track2-optical-results-v36.json').read_text()),report,(ROOT/'notes/track2-slides-v37.html').read_text())
    requirements=requirements_checks(*[json.loads((ROOT/f'notes/track2-{n}-v37.json').read_text()) for n in ['requirements','community-audit']])
    counts,transcript=narration((ROOT/'notes/track2-pitch-v37.md').read_text())
    require((ROOT/'notes/track2-transcript-v37.txt').read_text()==transcript,'Transcript differs')
    description=(ROOT/'notes/track2-video-description-v37.md').read_text()
    require(f'{sum(counts)} narration words' in description and normalized(answers['B9']) in normalized(description),'Video disclosure/count differs')
    require(acknowledgement() in normalized(description),'Video acknowledgement missing')
    require(builder.rendered()==(ROOT/'notes/track2-demo-v37.html').read_text(),'Generated demo differs')
    teaching=demo.run();teaching.pop('seconds')
    for name in ['report','slides','pitch','reviewer-guide','owner-readiness','video-description','lab-handoff','community-kit','judge-questions']:
        suffix='html' if name=='slides' else 'md';repository_links((ROOT/f'notes/track2-{name}-v37.{suffix}').read_text())
    return dict(old,passed=True,presentation_version=37,**visual,narration_words=sum(counts),words_per_slide=counts,
        abstract_words=len(answers['B17'].split()),requirements=requirements,teaching_demo=teaching,
        historical_v36_checks_preserved=True,upload_ready=False,runtime_measured=False,biological_validation=False,
        scope='Public consistency and educational implementation checks; not biological or clinical validation')


if __name__=='__main__':print(json.dumps(check(),indent=2))
