#!/usr/bin/env python3
"""Review the concise v36 proposal and completed optical evidence on public files."""
import json
from pathlib import Path
import re
import track2_public_review_v34 as historical
import check_track2_optical_v36 as optical
from track2_release_v7 import Content

ROOT=Path(__file__).resolve().parents[1]
REVISION=historical.REVISION
require=historical.require
digest=historical.digest
normalized=historical.normalized
methods_answers=historical.methods_answers
acknowledgement=historical.acknowledgement
repository_links=historical.repository_links
requirements_checks=historical.requirements_checks


def presentation_checks(deck):
    """Static/semantic checks; final numerical integration is checked by check()."""
    parser=historical.DeckParser();parser.feed(deck);parser.close();parser.validate()
    content=Content();content.feed(deck)
    slides=[' '.join(s).lower() for s in content.sections]
    required={
        1:['everolimus','approved mtorc1 inhibitor','research hypothesis','no rescue-priority drug'],
        2:['p.leu737ter / p.asn1002lys','phase unconfirmed','endogenous effects','neither branch established',
           'does not replace bubr1','excess mtor activity','impaired dynamic flux'],
        3:['no wet-lab measurements','single / cis / trans','perturbation + restoration','deficit alone',
           'joint treatment','corrected','drug alone','randomize cultures','blind scoring','confirm independently'],
        4:['synthetic example, not experimental data','25%','20 / 80','11.1%','5 / 45','60 / 100','40 / 100',
           'daughter fate','prespecified recovery','missing observations'],
        5:['0 / 24 pass','one shared guide pair','selected controls','40 older adults','−2.13',
           '95% ci −4.61 to 0.34','p=0.089','indirect for mva','separate drug profiles cannot establish rescue'],
        6:['hela lacks functional p53','retrieval does not establish non-cancer rescue'],
        7:['invalid assay','hold inference','unknown / imprecise','hold advancement','meaningful benefit excluded',
           'stop the tested claim','failed safety','stop; review injury','preclinical review only',
           'clinical exposure margin unknown'],
        8:['cpu','no subject files or gpus','fresh qualification','hcq reserve','deficient-normal controls'],
    }
    for number,phrases in required.items():
        for phrase in phrases:require(phrase in slides[number-1],f'Slide {number} boundary missing: '+phrase)
    require(acknowledgement().lower() in slides[-1],'Full acknowledgement required')
    require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v36.md' in content.links,
            'Current report link missing')
    return dict(slides=9,vector_figures=8,visible_words=[len(s) for s in content.sections])


def check_deck():
    path=ROOT/'notes/track2-slides-v36.html'
    return dict(static_deck_verified=True,source_sha256=digest(path),**presentation_checks(path.read_text()))


def report_checks(report):
    require('PENDING' not in report,'Unfinished report integration')
    answers=methods_answers(report);text=normalized(report).lower()
    for phrase in ['no rescue-priority drug','trans phase','1,000-fold','both values remain quarantined',
                   'neither branch is established','0/24','1/24','12/12','8/12','11/24','67,584','528',
                   '0/14','uncalibrated','0.1223-0.1371','0.6572','171.5/2,154','0.1043','0.5836',
                   'one shared guide pair','selected controls','repeated splits reuse cells',
                   'no qc-qualified bub1b query','0.1 µm nominal culture','related models',
                   'failed assay controls hold inference','genotype-specific claim needs an interaction contrast',
                   'nonsignificance is not safety','all clinical exposure margins','returns hold',
                   'synthetic example, not experimental data','20/80','5/45','60/100','40/100',
                   'cnb@sagebase.org by november 23','distribution scope remains unresolved',
                   'rereads funk methods','reading depth','not systematic',REVISION]:
        require(phrase in text,'Report boundary missing: '+phrase)
    disclosure=normalized(answers['B9']).lower()
    for phrase in ['openai','fireworks-hosted','unverified','colabfold','alphafold3','evo2','not on-demand',
                   'raw subject','eight owner-host h100s','executed proteinmpnn','carbon annotation',
                   'no additional hosted model provider','precomputed','four image-position features']:
        require(phrase in disclosure,'Provider/model disclosure missing: '+phrase)
    require(normalized(report.split('## Acknowledgement\n')[1])==acknowledgement(),'Acknowledgement changed')
    require(not re.search(r'\]\((?!https://)[^)]+\)',report),'Standalone report needs absolute public links')
    return answers


def optical_numbers(results,report,deck):
    """Numbers shown in final prose/figures must match the retained comparison."""
    for arm,r in results['arms'].items():
        require(f"{r['cells']:,}" in report,'Report cell count differs: '+arm)
        for field in ['full_profile','full_median_training_preprocessing']:
            require(f"{r['baselines'][field]['macro_mrr']:.6f}" in report,'Report baseline differs: '+arm+'/'+field)
        values=[seed['macro_mrr'] for seed in r['learned']]
        match=re.search(r'<text id="'+arm+r'-neural-range"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==f'{min(values):.4f}–{max(values):.4f}',
                'Slide learned MRR range differs')
        best=max(v['macro_mrr'] for v in r['baselines'].values())
        match=re.search(r'<text id="'+arm+r'-baseline"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==f'{best:.4f}','Slide strongest baseline differs')
    ranks=[row['rank'] for row in results['arms']['interphase']['query_baselines']['full_profile']['rows']
           if row['gene']=='BUB1B']
    for i,rank in enumerate(ranks,1):
        match=re.search(r'<text id="bub1b-rank-'+str(i)+r'"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==f'{rank:g}','Slide BUB1B rank differs')
    require('0.02' in deck and 'insufficient' in deck.lower(),'Threshold/coverage qualification omitted')


def narration(pitch):
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    require([h[0] for h,_ in rows]==list('123456789'),'Narration alignment differs')
    counts=[len(body.split()) for _,body in rows]
    require(300<=sum(counts)<=400 and f'Narration contains {sum(counts)} whitespace-separated words' in pitch,
            'Narration word count differs')
    for phrase in ['no drug earns rescue priority','phase and endogenous effects remain unresolved',
                   'neither branch is established','this example is synthetic','track every cell',
                   'early relative sensitivity can reverse','independent perturbation and restoration',
                   'whole blood is not free tissue','preclinical review only','invalid assays hold inference',
                   'injury stops advancement','no wet-lab experiment has been performed','hcq remains reserve']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    require('PENDING' not in pitch,'Unfinished narration')
    transcript='Track 2 v36 - read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for head,body in rows:transcript+='Slide '+head.replace(' / ',' | ')+'\n'+body.strip()+'\n\n'
    return counts,transcript.rstrip()+'\n'


def check():
    old=historical.check()
    study=optical.check()
    deck=(ROOT/'notes/track2-slides-v36.html').read_text()
    require('PENDING' not in deck,'Unfinished optical slide')
    visual=check_deck()
    report=(ROOT/'notes/track2-report-v36.md').read_text();answers=report_checks(report)
    optical_numbers(json.loads((ROOT/'notes/track2-optical-results-v36.json').read_text()),report,deck)
    requirements=requirements_checks(json.loads((ROOT/'notes/track2-requirements-v36.json').read_text()),
        json.loads((ROOT/'notes/track2-community-audit-v36.json').read_text()))
    counts,transcript=narration((ROOT/'notes/track2-pitch-v36.md').read_text())
    require((ROOT/'notes/track2-transcript-v36.txt').read_text()==transcript,'Plain transcript differs')
    description=(ROOT/'notes/track2-video-description-v36.md').read_text()
    require(f'{sum(counts)} narration words' in description,'Video-description word count differs')
    require(normalized(answers['B9']) in normalized(description),'Video disclosure differs from methods B9')
    require(acknowledgement() in normalized(description),'Video acknowledgement missing')
    for name in ['report','slides','pitch','reviewer-guide','owner-readiness','video-description']:
        suffix='html' if name=='slides' else 'md'
        repository_links((ROOT/f'notes/track2-{name}-v36.{suffix}').read_text())
    register=json.loads((ROOT/'notes/track2-optical-register-v36.json').read_text())
    ids=[x['id'] for x in register['claims']]
    require(len(ids)==len(set(ids))==6 and all(x['drug_ranking_changed'] is False for x in register['claims']),
            'Optical falsification record differs')
    return dict(passed=True,presentation_version=36,drug_science_version=21,**visual,
        narration_words=sum(counts),words_per_slide=counts,methods_fields=len(answers),
        abstract_words=len(answers['B17'].split()),requirements=requirements,optical=study,
        claim_records=old['claim_records']+len(ids),historical_v34_checks_preserved=True,
        transcriptome=old['transcriptome'],falsification_amendment=old['falsification_amendment'],
        upload_ready=False,biological_validation=False,runtime_measured=False,
        scope='Public consistency and arithmetic provenance; not biological validation or delivery approval')


if __name__=='__main__':print(json.dumps(check(),indent=2))
