#!/usr/bin/env python3
"""Review tracked public Track 2 artifacts using the standard library only."""
from pathlib import Path
import hashlib
import json
import re
import track2_release_v5 as static
from track2_release_v7 import Content
import track2_falsification_v15 as falsification
import track2_falsification_v21 as amendment

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
        3:['0/14','primary query filter','operational; uncalibrated','favourable ht29','post-hoc / shared-pattern removal','adjusted tail 0.042','5 reagents; minimum 6','does not pass the full filter','does not disprove biology','180 everolimus-labelled profiles','174 unresolved stereochemistry','reference-matching','0.1 µm nominal culture','all 6 fail drug qc','single sample; low activity','replicate correlation missing','neither benefit nor harm'],
        4:['rapa-ex-01 / 40 older adults','sirolimus − placebo / 13 weeks','both trial groups exercised','rapamycin models','−2.13','chair stands','primary itt difference','95% ci −4.61 to 0.34; p=0.089','no established functional benefit','young male rats','force impaired','adult female mice','exercise gains retained','grip strength / power','indirect for everolimus/mva'],
        5:['no wet-lab experiments','single / cis / trans','corrected controls','randomize + blind','independent replication','independent genetic control','drug + qualified deficit','every enrolled cell','function + daughter fate','exposure + recovery','no post-hoc switching'],
        6:['invalid assay','hold inference','unknown / imprecise','hold advancement','meaningful benefit excluded','stop the tested claim','failed safety','stop; review injury','preclinical review only','clinical exposure margin unknown','quarantined','valid, qualified tests required'],
        7:['impact','innovation','reuse','cpu','no subject files or gpus','fresh qualification','tumour killing','deficient-normal controls'],
    }
    for n,phrases in required.items():
        for phrase in phrases:require(phrase in slides[n-1],f'Slide {n} omits boundary: {phrase}')
    require(acknowledgement().lower() in slides[7],'Full acknowledgement required')
    require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v22.md' in c.links,'Current report link required')
    for ident,label in {'invalid':'Invalid assay','inference':'Hold inference',
                        'unknown':'Unknown / imprecise','hold':'Hold advancement',
                        'futility':'Meaningful benefit excluded','claim':'Stop the tested claim',
                        'failed':'Failed safety','stop':'Stop; review injury',
                        'all':'All requirements met','review':'Preclinical review only'}.items():
        match=re.search(r'<text id="gate-'+ident+r'"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==label,'Decision-row label drift: '+ident)
    return dict(slides=8,vector_figures=7,visible_words=[len(s) for s in c.sections])

def check_deck():
    p=ROOT/'notes/track2-slides-v22.html'
    return dict(static_deck_verified=True,source_sha256=digest(p),**presentation_checks(p.read_text()))

def methods_answers(report):
    answers={}
    for n in range(7,18):
        match=re.search(rf'\*\*B{n}: [^\n]+?\*\*\s*(.*?)(?=\n\n\*\*B\d+|\n\n## Acknowledgement)',report,re.S)
        require(match is not None,f'Missing methods B{n}')
        answers[f'B{n}']=match[1].strip()
    require(0<len(answers['B17'].split())<=500,'Abstract exceeds official limit')
    return answers

def report_checks(report):
    a=methods_answers(report)
    for phrase in ['27 claims','unknown sensitivity and specificity','RAPA-EX-01','p=0.089','PoWeR','SIRT2',
                   'Nonsignificance is not safety','interaction contrast','Failed assay controls','sixteen failed Europe PMC']:
        require(phrase.lower() in report.lower(),'Falsification amendment missing: '+phrase)
    for text in ['no rescue-priority drug','trans phase','1,000-fold','8/12','11/24','12/12','post-hoc','0.58-1.26','p=0.44','63-source','19 claims','312,438','not distinct drugs or independent experiments','12,185,082','560,000','0/14','0/42','0.042','six-reagent requirement','13/19','19 comparisons reuse 14','174/180','all six','0.1 µM','uncalibrated','does not match shRNA seed','does not prove','not new neural-model inference','drug-plus-deficit']:
        require(text.lower() in report.lower(),'Report omits evidence qualification: '+text)
    for text in ['OpenAI','Fireworks','unverified','ColabFold','AlphaFold3','Evo2','not on-demand','raw subject','eight owner-host H100s','statistical reanalysis','brief, bursty','public NIH']:
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

def research_summary(first, second, followup, identity, audit):
    """Derive current claims from completed outputs; no new biological inference."""
    primary = [r for q in first['queries'] for s in q['spaces'] if s['name'] == 'raw'
               for r in s['named_compounds'] if r['compound'] == 'everolimus']
    proper = {r['signature_id']: r for q in second['queries'] for s in q['spaces'] if s['name'] == 'raw'
              for r in s['named_compounds'] if r['compound'] == 'everolimus' and
              r['compound_id'] == identity['eligible_identity_id']}
    ht29 = [r for r in followup['rows'] if r['cell_id'] == 'HT29' and
            r['arm'] == 'provider_members_shared_pc1_removed']
    require(len(ht29) == 1, 'Missing HT29 counterweight')
    waves = [first, second, followup]
    for wave in waves:
        runs = wave['gpu_runs']
        require([r['shard'] for r in runs] == list(range(8)) and
                all(r['complete'] is True for r in runs), 'Incomplete GPU wave')
        require(sorted(q for r in runs for q in r['query_ids']) == sorted(q['query_id'] for q in first['queries']),
                'GPU query coverage drift')
    vectors = audit['score_vectors']
    require(len(vectors) == 2 and {r['wave'] for r in vectors} == {'shard-', 'phase2-shard-'},
            'Missing expression release')
    for record, result in zip(vectors, [first, second]):
        require(record['vectors'] == sum(len(q['spaces']) for q in result['queries']) and
                record['comparisons'] == record['vectors'] * record['profiles'], 'Comparison count drift')
    summary = dict(
        gpus=len(first['gpu_runs']), completed_gpu_waves=len(waves),
        compound_profiles=sum(r['profiles'] for r in vectors),
        query_compound_comparisons=sum(r['comparisons'] for r in vectors),
        resampled_reagent_sets=sum(q['null_draws'] for q in first['queries']) + sum(r['null_draws'] for r in followup['rows']),
        primary_contexts=len(first['queries']),
        primary_query_gates_passed=sum(q['operational_query_gate'] for q in first['queries']),
        post_hoc_comparisons=len(followup['rows']),
        post_hoc_full_filters_passed=sum(r['same_operational_filter'] for r in followup['rows']),
        primary_everolimus_comparisons=len(primary),
        primary_everolimus_profiles=len({r['signature_id'] for r in primary}),
        primary_everolimus_positive_correlations=sum(r['correlation'] > 0 for r in primary),
        phase2_unresolved_labelled_profiles=sum(identity['phase2_profile_counts_by_id'][i] for i in identity['unresolved_ids']),
        phase2_reference_matching_profiles=len(proper),
        phase2_reference_matching_qc_passes=sum(r['quality_pass'] for r in proper.values()),
        ht29_post_hoc_reagents=ht29[0]['n_reagents'],
        ht29_post_hoc_adjusted_tail=ht29[0]['split_null_BH_q'],
        ht29_full_filter_passed=ht29[0]['same_operational_filter'],
        drug_ranking_changed=first['drug_ranking_changed'],
    )
    expected = dict(gpus=8, completed_gpu_waves=3, compound_profiles=312438,
        query_compound_comparisons=12185082, resampled_reagent_sets=560000,
        primary_contexts=14, primary_query_gates_passed=0, post_hoc_comparisons=42,
        post_hoc_full_filters_passed=0, primary_everolimus_comparisons=19,
        primary_everolimus_profiles=14, primary_everolimus_positive_correlations=13,
        phase2_unresolved_labelled_profiles=174, phase2_reference_matching_profiles=6,
        phase2_reference_matching_qc_passes=0, ht29_post_hoc_reagents=5,
        ht29_post_hoc_adjusted_tail=0.041995800419958006,
        ht29_full_filter_passed=False, drug_ranking_changed=False)
    require(summary == expected, 'Unreviewed research-summary change')
    require(audit['retained_null_draws_rechecked'] == summary['resampled_reagent_sets'], 'Null archive count drift')
    return summary



def transcriptome_checks():
    import check_track2_transcriptome as campaign
    audit_path=ROOT/'notes/track2-transcriptome-audit-v19.json'
    require(digest(audit_path)=='a2ab0132f37a2fdce4f5e2c0efbe468da525ee8d12125e3d4b8baf7b22cb7ca1','Frozen transcriptome audit drift')
    audit=json.loads(audit_path.read_text())
    for path,expected in audit['public_input_sha256'].items():
        relative=Path(path)
        require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe campaign input')
        require(not any((ROOT/Path(*relative.parts[:i])).is_symlink() for i in range(1,len(relative.parts)+1)), 'Symlinked campaign input')
        require(digest(ROOT/path)==expected,'Frozen campaign input changed: '+path)
    first,second,identity,followup=[json.loads((ROOT/'notes'/n).read_text()) for n in [
        'track2-transcriptome-results-v19.json','track2-transcriptome-phase2-results-v19.json',
        'track2-transcriptome-identity-v19.json','track2-transcriptome-followup-results-v19.json']]
    campaign.validate(first,second,identity)
    campaign.validate_followup(followup,first)
    return research_summary(first,second,followup,identity,audit)

def check():
    deck=check_deck()
    r=json.loads((ROOT/'notes/track2-requirements-v22.json').read_text())
    community=json.loads((ROOT/'notes/track2-community-audit-v22.json').read_text())
    requirements=requirements_checks(r,community)
    methods=report_checks((ROOT/'notes/track2-report-v22.md').read_text())
    science=falsification.check()
    revised_science=amendment.check()
    require(json.loads((ROOT/'notes/track2-falsification-analysis-v21.json').read_text())==revised_science,
            'Recorded falsification analysis is stale')
    transcriptome=transcriptome_checks()
    ledger=json.loads((ROOT/'notes/track2-evidence-v15.json').read_text())
    baseline=json.loads((ROOT/'notes/track2-evidence-v10.json').read_text())
    require(len(ledger['sources'])==63 and len(ledger['decisions'])==11,'Evidence inventory drift')
    require({x['id']:x['decision'] for x in ledger['decisions']}=={x['id']:x['decision'] for x in baseline['decisions']},'Unreviewed drug promotion')
    pitch=(ROOT/'notes/track2-pitch-v22.md').read_text()
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    require([head[0] for head,_ in rows]==list('12345678'),'Narration slide alignment')
    counts=[len(body.split()) for _,body in rows]
    require(sum(counts)==337 and 'Narration contains 337 whitespace-separated words' in pitch,'Narration count drift')
    for phrase in ['no drug earns rescue priority','phase and endogenous effects remain unresolved','filter is uncalibrated','post-hoc ht29','five reagents against our six-reagent requirement','unresolved stereochemical metadata','nominal culture concentration','neither benefit nor harm','whole blood is not free tissue','preclinical review only','no subject files or gpus','forty older adults','primary confidence interval includes no effect','adult female mice retained','invalid assays hold inference','meaningful benefit stops that tested claim','hcq remains reserve','nad findings do not establish niacin rescue']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    transcript='Track 2 v22 - read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for head,body in rows:transcript+='Slide '+head.replace(' / ',' | ')+'\n'+body.strip()+'\n\n'
    require((ROOT/'notes/track2-transcript-v22.txt').read_text()==transcript.rstrip()+'\n','Plain transcript drift')
    desc=(ROOT/'notes/track2-video-description-v22.md').read_text()
    require(normalized(desc.split('## Acknowledgement\n')[1])==acknowledgement(),'Video acknowledgement drift')
    require(methods['B9'] in desc,'Video disclosure differs from report')
    return dict(passed=True,presentation_version=22,drug_science_version=21,**deck,narration_words=sum(counts),words_per_slide=counts,
                requirements=requirements,transcriptome=transcriptome,methods_fields=len(methods),abstract_words=len(methods['B17'].split()),falsification=science,
                falsification_amendment=revised_science,upload_ready=False,biological_validation=False,scope='Tracked-public consistency checks; no inference, clinical or eligibility certification')

if __name__=='__main__':print(json.dumps(check(),indent=2))
