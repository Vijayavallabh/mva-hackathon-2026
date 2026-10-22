#!/usr/bin/env python3
"""Review the rubric-directed v41 proposal, literature addendum, demo and retained v36 science offline."""
import json
from pathlib import Path
import re
import track2_public_review_v39 as previous
import track2_narration_v46 as timing
import build_track2_recording_v50 as recording
import track2_public_review_v36 as prior
import track2_demo_v37 as demo
import build_track2_demo_v37 as builder
import check_track2_literature_v45 as literature

ROOT=prior.ROOT
REVISION=prior.REVISION
require=prior.require
digest=prior.digest
normalized=prior.normalized
methods_answers=prior.methods_answers
acknowledgement=prior.acknowledgement
repository_links=prior.repository_links


def presentation_checks(deck):
    """Static/semantic checks; final numerical integration is checked by check()."""
    parser=prior.historical.DeckParser();parser.feed(deck);parser.close();parser.validate()
    content=prior.Content();content.feed(deck)
    slides=[' '.join(s).lower() for s in content.sections]
    required={
        1:['everolimus','mtorc1 inhibitor','on hold','research hypothesis','no rescue-priority drug'],
        2:['p.leu737ter / p.asn1002lys','phase unconfirmed','endogenous effects','neither route established',
           'does not replace bubr1','first qualify function','independent restoration','carrier skeletal muscle','bubr1+/x753; sarcopenia',
           '1. first qualify function','2. qualify a separate hypothesis','nad/sirt2',
           'male-biased genetic survival','opposing site/context evidence'],
        3:['no wet-lab measurements','single / cis / trans','perturbation + restoration','deficient baseline','four arms','corrected reference','vehicle','everolimus','randomize cultures','blind scoring','confirm independently'],
        4:['synthetic example, not experimental data','25%','20 / 80','11.1%','5 / 45','60 / 100','40 / 100',
           'daughter fate','prespecified window','missing observations','deficient + vehicle','deficient + probe','founder cells'],
        5:['0 / 24 pass','one shared guide pair','selected controls','40 older adults','−2.13',
           '95% ci −4.61 to 0.34','p=0.089','indirect for mva','separate drug profiles cannot establish rescue'],
        6:['hela lacks functional p53','retrieval does not establish non-cancer rescue'],
        7:['invalid assay','hold inference','unknown / imprecise','hold advancement','meaningful benefit excluded',
           'stop the tested claim','failed safety','stop; review injury','preclinical review',
           'software verification only','biological thresholds need fresh qualified evidence','exposure margins remain unknown'],
        8:['cpu','no subject files or gpus','fresh qualification','hcq reserve','deficient-normal controls'],
    }
    for number,phrases in required.items():
        for phrase in phrases:require(phrase in slides[number-1],f'Slide {number} boundary missing: '+phrase)
    require(acknowledgement().lower() in slides[-1],'Full acknowledgement required')
    require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v53.md' in content.links,
            'Current report link missing')
    return dict(slides=9,vector_figures=8,visible_words=[len(s) for s in content.sections])


def check_deck():
    path=ROOT/'notes/track2-slides-v53.html'
    return dict(static_deck_verified=True,source_sha256=digest(path),**presentation_checks(path.read_text()))


def command_paths(document):
    for relative in re.findall(r'\bscripts/[A-Za-z0-9_.-]+\.(?:py|mjs|sh)\b',document):
        require((ROOT/relative).is_file(),'Missing documented command: '+relative)


def report_checks(report):
    text=normalized(report).lower()
    for phrase in ['targeted contrary-evidence refreshes','checkpoint-architecture readouts',
                   'mitochondrial integrity and proteostasis/ubiquitin-proteasome injury markers','k250/s16/s39',
                   'no drug disposition changed','everolimus remains a mechanistic probe on hold','hcq remains reserve',
                   '2026 fission-yeast torc1-segregation study','direct mtorc1 engagement',
                   'lagging-dna/anaphase-bridge counts','fission-yeast, not mammalian mva',
                   'rapamycin and everolimus are not interchangeable']:
        require(phrase in text,'Literature integration drift: '+phrase)
    for route in ['https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-v45.md',
                 'https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-literature-audit-v43.json']:
        require(route in report,'Missing literature route')
    command_paths(report)
    answers=previous.report_checks(report)
    text=normalized(report).lower()
    for phrase in ['first qualification question','separately justified alternative','four separate links',
                   '17 synthetic cases and one actual unmeasured state','benefit-only rule advances 11',
                   'viability still advances 9','83 valid checks','12 invalid records',
                   'not a representative','not been co-developed with the family',
                   'heterozygous bubr1+/x753','females had no median-lifespan',
                   'mouse k243 corresponds to human k250','spontaneous tumors',
                   'proposed first comparator is engineered htert-rpe1',
                   'availability, clone feasibility and functional qualification remain unconfirmed',
                   'synthetic margins cannot qualify','diagnostic use would still require',
                   'why everolimus is eligible but not superior.','the first experiment is model qualification',
                   'two downstream mtor-related hypotheses','changes readout design, not any drug disposition']:
        require(phrase in text,'Rubric/limitations drift: '+phrase)
    return answers


def requirements_checks(r,c):
    require(r['revision']==REVISION and r['schema_version']==39,'Wrong current source revision')
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


def optical_report_numbers(results,report):
    """The v50 pitch no longer displays optical statistics; verify the report numbers only."""
    for arm,r in results['arms'].items():
        require(f"{r['cells']:,}" in report,'Report cell count differs: '+arm)
        for field in ['full_profile','full_median_training_preprocessing']:
            require(f"{r['baselines'][field]['macro_mrr']:.6f}" in report,'Report baseline differs: '+arm+'/'+field)

def narration(pitch):
    cues=timing.parse(pitch)
    rows=[(c['head'],c['body']) for c in cues]
    spoken=' '.join(c['body'] for c in cues)
    counts=[c['words'] for c in cues]
    require(300<=sum(counts)<=400 and f'Narration contains {sum(counts)} whitespace-separated words' in pitch,'Narration word drift')
    for phrase in ['no drug earns rescue priority','phase and endogenous effects remain unresolved','neither route is established',
                   'independent perturbation and restoration','this example is synthetic','track every cell',
                   'early relative sensitivity can reverse','whole blood is not free tissue','preclinical review',
                   'invalid assays hold inference','injury stops advancement','no wet-lab experiment has been performed',
                   'hcq remains reserve','without requesting another family sample']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    transcript='Track 2 v50 - read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for h,b in rows:transcript+='Slide '+h.replace(' / ',' | ')+'\n'+b.strip()+'\n\n'
    return counts,transcript.rstrip()+'\n'


def v50_checks(report, deck):
    report_text=normalized(report).lower(); deck_text=normalized(deck).lower()
    for phrase in ['track 2 research proposal | jvv7 | 23 october 2026 | v53',
                   'pooled agreement as uniform stability',
                   '## candidate proposal and mechanism in brief','**everolimus** as the conditional approved candidate',
                   'variant | bub1b p.leu737ter / p.asn1002lys',
                   'direction of effect','gene-level mechanism','downstream pathway','repurposing rationale',
                   'deficient + vehicle, deficient + everolimus, corrected + vehicle, corrected + everolimus',
                   'selected-pair efficacy, trans phase, and clinical exposure',
                   'alternatives considered and not advanced',
                   'dasatinib + quercetin senolysis',
                   'a viability endpoint cannot distinguish these directions']:
        require(phrase in report_text,'V48 report hierarchy missing: '+phrase)
    for banned in ['delve','foster','leverage','utilize','facilitate','empower','streamline',
                   'cutting-edge','paradigm shift','game changer','tapestry','realm','beacon',
                   'multifaceted','meticulous','intricate','paramount','transformative','elevate',
                   'embark','supercharge','ever-evolving','seamless','holistic','pivotal',
                   'underscores','underscoring','testament','unprecedented','invaluable']:
        if banned=='beacon': continue  # BEACON consortium acknowledgement is required text, not slop

        require(banned not in report_text and banned not in deck_text,'Slop wording retained: '+banned)
    for phrase in ['qualify function first.','on hold','first experiment: endogenous function, not exposure','no rescue-priority drug; no clinical consideration','a staged experiment. an inspectable tool.','reusable now','qualify next']:
        require(phrase in deck_text,'V48 deck improvement missing: '+phrase)
    require('track2-report-v53.md' in deck and 'track2-report-v48.md' not in deck,'V48 route drift')
    require('v53' in deck and 'v52' not in deck.lower(),'V53 title drift')
    return dict(report_revision='v51',slop_scan_passed=True,route='notes/track2-report-v53.md')

def check():
    old=prior.check()
    visual=check_deck()
    literature_result=literature.check()
    report=(ROOT/'notes/track2-report-v53.md').read_text();answers=report_checks(report)
    deck=(ROOT/'notes/track2-slides-v53.html').read_text();v50_result=v50_checks(report,deck)
    optical_report_numbers(json.loads((ROOT/'notes/track2-optical-results-v36.json').read_text()),report)
    requirements=requirements_checks(*[json.loads((ROOT/f'notes/track2-{n}-v39.json').read_text()) for n in ['requirements','community-audit']])
    counts,transcript=narration((ROOT/'notes/track2-pitch-v50.md').read_text())
    require((ROOT/'notes/track2-transcript-v50.txt').read_text()==transcript,'Transcript differs')
    pitch=(ROOT/'notes/track2-pitch-v50.md').read_text()
    require(json.loads((ROOT/'notes/track2-narration-v50.json').read_text())==timing.summary(pitch),'Narration metrics differ')
    require(timing.guide_metrics(pitch) in (ROOT/'notes/track2-recording-guide-v50.md').read_text(),'Recording guide rates differ')
    require(recording.rendered()==(ROOT/'notes/track2-teleprompter-v50.html').read_text(),'Teleprompter differs')
    description=(ROOT/'notes/track2-video-description-v50.md').read_text()
    require(f'{sum(counts)} narration words' in description and normalized(answers['B9']) in normalized(description),'Video disclosure/count differs')
    require(acknowledgement() in normalized(description),'Video acknowledgement missing')
    require(builder.rendered()==(ROOT/'notes/track2-demo-v37.html').read_text(),'Generated demo differs')
    teaching=demo.run();teaching.pop('seconds')
    for name in ['report','slides']:
        suffix='html' if name=='slides' else 'md'
        document=(ROOT/f'notes/track2-{name}-v48.{suffix}').read_text()
        repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-pitch-v50.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-lab-handoff-v43.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-candidate-comparison-v42.md').read_text()
    repository_links(document);command_paths(document)
    for name in ['judge-questions']:
        document=(ROOT/f'notes/track2-{name}-v43.md').read_text()
        repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-community-kit-v42.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-recording-guide-v42.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-video-description-v50.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-external-review-packet-v43.md').read_text()
    repository_links(document);command_paths(document)
    document=(ROOT/'notes/track2-reviewer-brief-v43.md').read_text()
    repository_links(document);command_paths(document)
    for name in ['reviewer-guide','owner-readiness']:
        document=(ROOT/f'notes/track2-{name}-v43.md').read_text()
        repository_links(document);command_paths(document)
    return dict(old,passed=True,presentation_version=53,report_revision='v53',v50_checks=v50_result,literature_refresh=literature_result,**visual,narration_words=sum(counts),words_per_slide=counts,planned_recording=timing.summary(pitch),
        abstract_words=len(answers['B17'].split()),requirements=requirements,teaching_demo=teaching,
        historical_v36_checks_preserved=True,upload_ready=False,runtime_measured=False,biological_validation=False,
        scope='Public consistency, literature provenance and educational implementation checks; not biological or clinical validation')


if __name__=='__main__':print(json.dumps(check(),indent=2))
