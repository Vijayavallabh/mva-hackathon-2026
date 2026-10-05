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
REVISION='c9b4a7e6247574124cd5bbfd249af9af6f1bbac3'
DISCUSSIONS=[1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
require=static.require

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(text):return ' '.join(text.split())
def acknowledgement():return normalized((ROOT/'notes/track2-report-v16.md').read_text().split('## Acknowledgement\n')[1])

class DeckParser(static.DeckParser):
    def validate(self):
        require(not self.stack and self.html_count==1 and self.csp_count==1,'Incomplete or unsafe HTML')
        require(self.sections==[f'slide-{n}' for n in range(1,10)],'Nine ordered slides required')
        require(self.svg_count==8 and self.section_vectors==[1]*8+[0],'Eight figures and full acknowledgement required')

def presentation_checks(deck):
    p=DeckParser();p.feed(deck);p.close();p.validate()
    c=Content();c.feed(deck);slides=[' '.join(s).lower() for s in c.sections]
    required={
        1:['everolimus','approved mtorc1 inhibitor','research hypothesis','no rescue-priority drug'],
        2:['p.leu737ter / p.asn1002lys','phase unconfirmed','endogenous effects unknown','neither branch established','does not replace bubr1','1/24','0/24','4 related checkpoints','6 wt backbones','candidate rank does not establish function','predicted backbone changes the score','stability retained','cenp-e phosphorylation lost','kard/scaffolding retained','separate stability, scaffolding and catalysis'],
        3:['0.3500','0.1223-0.1371','rnai 1-6 / crispr 1-3','715-781 / 276-340 references','1 guide / 31 total profiles','failed crispr profiles excluded','independent guides needed','tumour-line assay lead','rnai reused','repeated-partition range, not a ci','projection can remove real biology','evaluated genes held out of fitting','passing crispr profiles only'],
        4:['mcf7','reference-matching chemistry','0.1 µm nominal culture','1-3 → 204-308','787-920 held-out references','-0.2144','-0.0335','-0.0259','mtor stays rank 1','including qc-only views','drug qc passes','qualified bub1b query: missing','missing is not zero','ht29 drug profile fails qc','10 µm nominal culture','different cells and separate perturbations','joint functional rescue remains untested','not confidence intervals'],
        5:['rapa-ex-01 / 40 older adults','sirolimus − placebo / 13 weeks','both trial groups exercised','rapamycin models','−2.13','chair stands','primary itt difference','95% ci −4.61 to 0.34; p=0.089','no established functional benefit','young male rats','force impaired','adult female mice','exercise gains retained','grip strength / power','indirect for everolimus/mva'],
        6:['no wet-lab experiments','single / cis / trans','corrected controls','randomize + blind','independent replication','independent genetic control','drug + qualified deficit','every enrolled cell','function + daughter fate','exposure + recovery','no post-hoc switching','editing-stress controls'],
        7:['invalid assay','hold inference','unknown / imprecise','hold advancement','meaningful benefit excluded','stop the tested claim','failed safety','stop; review injury','preclinical review only','clinical exposure margin unknown','quarantined','valid, qualified tests required','47 claim records / five registers'],
        8:['impact','innovation','reuse','cpu','no subject files or gpus','fresh qualification','tumour killing','deficient-normal controls'],
    }
    for n,phrases in required.items():
        for phrase in phrases:require(phrase in slides[n-1],f'Slide {n} omits boundary: {phrase}')
    require(acknowledgement().lower() in slides[8],'Full acknowledgement required')
    require('https://github.com/Vijayavallabh/mva-hackathon-2026/blob/main/notes/track2-report-v30.md' in c.links,'Current report link required')
    for ident,label in {'invalid':'Invalid assay','inference':'Hold inference',
                        'unknown':'Unknown / imprecise','hold':'Hold advancement',
                        'futility':'Meaningful benefit excluded','claim':'Stop the tested claim',
                        'failed':'Failed safety','stop':'Stop; review injury',
                        'all':'All requirements met','review':'Preclinical review only'}.items():
        match=re.search(r'<text id="gate-'+ident+r'"[^>]*>([^<]+)</text>',deck)
        require(match is not None and match[1]==label,'Decision-row label drift: '+ident)
    return dict(slides=9,vector_figures=8,visible_words=[len(s) for s in c.sections])

def check_deck():
    p=ROOT/'notes/track2-slides-v30.html'
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
    for text in ['47 claim records','45/54','119,013','116,782','replicate-ID sets overlap','not independent biological replication','0.01422','0.08532','0.21276','5/36','0/36','No BUB1B CRISPR profile','14/297','21/297','not sample sizes','finite-reference','unknown','not our earlier','same-seed, different-target']:
        require(text.lower() in report.lower(),'RNAi qualification missing: '+text)
    for phrase in ['31 BUB1B CRISPR profiles','one guide ID','19 cell contexts','0.3712','0.3693','0.3594','One HT29 batch fails QC','8,623/57,044','7,983','271','82 pass','357','five pass','zero passing profiles','7 / 4,274','2,402 / 5,119','616 / 5,113','0.2836','10 µM','regroup three older singleton wells','cannot be combined into one experiment','2,474,445,074','285,488','1.231 seconds','8% GPU utilization','editing stress','survivor selection','same DNA-cutting event','not independent biological review']:
        require(phrase.lower() in report.lower(),'CRISPR qualification missing: '+phrase)
    for text in ['9,472','179,968','19,950','71.6%','89.8%','matched N→K','not p-values or pathogenicity probabilities','second-most',
                 'not a symmetrically held-out','attenuation does not prove','residual cosine is not a causal estimate','0.1510','7 → 8 → 78 → 125 → 1,184','0.2250',
                 'not a robust rescue rationale','918,999,010','1,004.196 seconds','not continuous eight-GPU saturation','no new biological observation']:
        require(text.lower() in report.lower(),'V27 qualification missing: '+text)
    for text in ['OpenAI','Fireworks','unverified','ColabFold','AlphaFold3','Evo2','not on-demand','raw subject','eight owner-host H100s','statistical reanalysis','brief, bursty','public NIH/Broad','local ESMC/ESM3 protein inference','executed ProteinMPNN','Four related checkpoint sets','FP32','no additional']:
        require(text.lower() in a['B9'].lower(),'Required provider disclosure missing: '+text)
    for text in ['67,584','528','1/24','0/24','four related','D882N','CENP-E','KARD','400 fits','820,147,416','715-781','276-340','204-308','787-920','not confidence intervals','missing evidence, not a zero score','endpoint-specific']:
        require(text.lower() in report.lower(),'V29 qualification missing: '+text)
    require(REVISION in report,'Stale official source revision')
    require('Distribution scope remains unresolved' in report,'Distribution uncertainty omitted')
    require(normalized(report.split('## Acknowledgement\n')[1])==acknowledgement(),'Acknowledgement drift')
    require(not re.search(r'\]\((?!https://)[^)]+\)',report),'Standalone report needs absolute public links')
    return a

def presentation_numbers(summary, report, deck):
    """Bind the four displayed held-out rows to the frozen numerical summaries."""
    rows=[r for r in summary['expression'] if r['cell']=='HT29' and r['representation'] in {'all978','residual_pc10'}]
    require(len(rows)==4,'Held-out display coverage')
    for r in rows:
        label=('All profiles' if r['quality']=='all_profiles' else 'Passing CRISPR profiles only')
        label+=(', unadjusted' if r['representation']=='all978' else ', mean + PC10 removed')
        values=[f"{v:.4f}" for v in r['correlation']]
        corr=values[0] if values[0]==values[1] else '-'.join(values)
        ranks=['-'.join(str(v) for v in r[k]) for k in ['rnai_rank','crispr_rank']]
        require('| '+label+' | '+corr+' | '+' | '.join(ranks)+' |' in report,'Held-out table differs from frozen results: '+label)
        if r['quality']=='crispr_quality_pass_only':
            require(corr in deck,'Slide correlation differs from QC-only results')
            if r['representation']=='residual_pc10':
                require('RNAi '+ranks[0]+' / CRISPR '+ranks[1] in deck,'Slide retrieval ranks differ from results')
    for r in summary['expression']:
        if r['cell']=='MCF7' and r['quality']=='crispr_quality_pass_only':
            require(r['available']==0 and r['correlation'] is None,'Missing MCF7 query was converted to a score')
    section=report.split('### Symmetric held-out expression tests')[1].split('## 4.')[0]
    for representation in ['all978','residual_pc10']:
        r=next(r for r in summary['drug'] if r['cell']=='MCF7' and r['quality']=='all_profiles' and r['gene']=='BUB1B' and r['representation']==representation)
        for value in r['correlation']:
            require(f'{value:.4f}' in section and f'{value:.4f}' in deck,'MCF7 drug correlation differs from results')
        require('-'.join(str(v) for v in r['reversal_rank']) in section,'MCF7 reversal range differs from results')
    return dict(heldout_table_rows=len(rows),source='notes/track2-orthogonal-summary-v29.json')


def requirements_checks(r,community):
    require(r['deadline_utc']=='2026-10-24T23:59:00Z' and r['data_deletion_deadline']=='2026-11-24','Deadline drift')
    require(r['winner_announcement_date']=='2026-12-18' and r['judging_end_date']=='2026-12-17','Judging schedule drift')
    require(r['requirements_review_independent'] is False and community['independent_review'] is False,'Unsupported independent review')
    require(r['revision']==REVISION,'Official revision drift')
    require(r['rubric_weights']==dict(scientific_rigor=35,potential_impact=25,innovation=25,scalability=15),'Rubric drift')
    require(r['submission_limit']==3 and r['only_latest_reviewed'] is True and r['quota_remaining'] is None,'Quota inference')
    require(r['report_extensions']==['.pdf','.md'] and r['video_duration_seconds']==180,'Submission format drift')
    require(r['required_ai_cell']=='B9' and r['abstract_word_limit']==500,'Methods requirement drift')
    require(len(r['sources'])==10 and all(x['http_status']==200 for x in r['sources']),'Incomplete source retrieval')
    require(all(v['exact_trimmed_match'] is True for v in r['live_source_comparison'].values()),'Live/source mismatch')
    require(r['licensing_scope_resolved'] is False and r['provider_settings_verified'] is False,'Unverified compliance promotion')
    require(community['listed_numbers']==DISCUSSIONS and community['listed_count']==26 and community['closed_count']==14,'Incomplete public community coverage')
    require(community['complete'] is True and len(community['threads'])==26,'Missing thread retrieval')
    require({t['num'] for t in community['threads']}==set(DISCUSSIONS) and all(t['status']=='ok' for t in community['threads']),'Wrong/failed thread')
    require(sum(t['comments'] for t in community['threads'])==community['visible_comments']==79,'Comment coverage drift')
    require(community['reviewed_admin_attachments']==3 and community['no_hidden_edit_history_review'] is True,'Reading depth drift')
    return dict(revision=REVISION,public_discussions=26,visible_comments=79,closed_discussions=14)

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

RNAI_AUDIT_SHA256='27bff5205ea443acdfe1dbb8863f21725af36af3e7400199bcea3345cdf9cb3c'

def rnai_checks():
    import check_track2_rnai_v23 as rnai
    path=ROOT/'notes/track2-rnai-audit-v23.json'
    require(digest(path)==RNAI_AUDIT_SHA256,'Frozen RNAi audit drift')
    result=rnai.check(ROOT)
    require(result['passed'] is True,'RNAi evidence check failed')
    return result

CRISPR_AUDIT_SHA256='264a46ecc491e0894d57f204c9d9739cb20494ca866bb6e73e3fdce5bd8e3ebb'

def crispr_checks():
    import check_track2_crispr_v25 as crispr
    path=ROOT/'notes/track2-crispr-audit-v25.json'
    require(digest(path)==CRISPR_AUDIT_SHA256,'Frozen CRISPR audit drift')
    result=crispr.check(ROOT)
    require(result['passed'] is True,'CRISPR evidence check failed')
    return result


FALSIFICATION_AUDIT_SHA256='690411890163add844aaa61aaf1a832b1447143341d67bdb34b45ec37128bd27'

def v27_checks():
    import check_track2_falsification_v27 as v27
    require(digest(ROOT/'notes/track2-falsification-audit-v27.json')==FALSIFICATION_AUDIT_SHA256,'Frozen v27 audit drift')
    result=v27.check(ROOT)
    require(result['passed'] is True,'V27 evidence check failed')
    return result


ORTHOGONAL_AUDIT_SHA256='c8499bbaa69f10884ec3fc43d95faf570bc97c379c5a2ef14bfbc08bc75d0e6f'

def v29_checks():
    import check_track2_orthogonal_v29 as v29
    require(digest(ROOT/'notes/track2-orthogonal-audit-v29.json')==ORTHOGONAL_AUDIT_SHA256,'Frozen v29 audit drift')
    result=v29.check(ROOT)
    require(result['passed'] is True,'V29 evidence check failed')
    return result


def check():
    deck=check_deck()
    r=json.loads((ROOT/'notes/track2-requirements-v30.json').read_text())
    community=json.loads((ROOT/'notes/track2-community-audit-v30.json').read_text())
    requirements=requirements_checks(r,community)
    methods=report_checks((ROOT/'notes/track2-report-v30.md').read_text())
    science=falsification.check()
    revised_science=amendment.check()
    require(json.loads((ROOT/'notes/track2-falsification-analysis-v21.json').read_text())==revised_science,
            'Recorded falsification analysis is stale')
    transcriptome=transcriptome_checks()
    rnai=rnai_checks()
    crispr=crispr_checks()
    v27=v27_checks()
    v29=v29_checks()
    numbers=presentation_numbers(json.loads((ROOT/'notes/track2-orthogonal-summary-v29.json').read_text()),(ROOT/'notes/track2-report-v30.md').read_text(),(ROOT/'notes/track2-slides-v30.html').read_text())
    claim_ids=[c['id'] for path in ['track2-falsification-register-v21.json','track2-rnai-register-v23.json','track2-crispr-register-v25.json','track2-falsification-register-v27.json','track2-orthogonal-register-v29.json']
               for c in json.loads((ROOT/'notes'/path).read_text())['claims']]
    require(len(claim_ids)==len(set(claim_ids))==47, 'Combined claim-register drift')
    ledger=json.loads((ROOT/'notes/track2-evidence-v15.json').read_text())
    baseline=json.loads((ROOT/'notes/track2-evidence-v10.json').read_text())
    require(len(ledger['sources'])==63 and len(ledger['decisions'])==11,'Evidence inventory drift')
    require({x['id']:x['decision'] for x in ledger['decisions']}=={x['id']:x['decision'] for x in baseline['decisions']},'Unreviewed drug promotion')
    pitch=(ROOT/'notes/track2-pitch-v30.md').read_text()
    spoken=pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows=re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)',spoken.strip(),re.S)
    require([head[0] for head,_ in rows]==list('123456789'),'Narration slide alignment')
    counts=[len(body.split()) for _,body in rows]
    require(sum(counts)==326 and 'Narration contains 326 whitespace-separated words' in pitch,'Narration count drift')
    for phrase in ['no drug earns rescue priority','phase and endogenous effects remain unresolved','expanded controls in all twenty-four comparisons','neither branch is established','held-out adjustment','one guide','removal of failed crispr profiles','independent perturbation and restoration','tumour context','rnai data are reused','no bub1b query passes quality checks','mtor stays first','nominal culture concentration','cannot qualify the query','ht29 drug quality also fails','different cells cannot supply a joint rescue result','whole blood is not free tissue','preclinical review only','no subject files or gpus','forty older adults','primary confidence interval includes no effect','adult female mice retained','invalid assays hold inference','benefit stops that tested claim','hcq remains reserve','nad findings do not establish niacin rescue','editing-stress controls','against each alone']:
        require(phrase in normalized(spoken).lower(),'Narration boundary missing: '+phrase)
    transcript='Track 2 v30 - read-aloud transcript\nRead the paragraphs; headings and times are cues, not narration.\n\n'
    for head,body in rows:transcript+='Slide '+head.replace(' / ',' | ')+'\n'+body.strip()+'\n\n'
    require((ROOT/'notes/track2-transcript-v30.txt').read_text()==transcript.rstrip()+'\n','Plain transcript drift')
    desc=(ROOT/'notes/track2-video-description-v30.md').read_text()
    require(normalized(desc.split('## Acknowledgement\n')[1])==acknowledgement(),'Video acknowledgement drift')
    require(methods['B9'] in desc,'Video disclosure differs from report')
    return dict(passed=True,presentation_version=30,drug_science_version=21,**deck,narration_words=sum(counts),words_per_slide=counts,
                requirements=requirements,transcriptome=transcriptome,rnai=rnai,crispr=crispr,v27=v27,v29=v29,presentation_numbers=numbers,claim_records=len(claim_ids),methods_fields=len(methods),abstract_words=len(methods['B17'].split()),falsification=science,
                falsification_amendment=revised_science,upload_ready=False,biological_validation=False,scope='Tracked-public consistency checks; no inference, clinical or eligibility certification')

if __name__=='__main__':print(json.dumps(check(),indent=2))
