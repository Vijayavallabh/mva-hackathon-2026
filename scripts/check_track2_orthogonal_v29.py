#!/usr/bin/env python3
"""Offline public consistency check for v29; no subject input, GPU or network."""
import csv
import hashlib
import json
import math
from pathlib import Path
from summarize_track2_orthogonal_v29 import summarize

ROOT=Path(__file__).resolve().parents[1]


def require(condition,message):
    if not condition:raise ValueError(message)


def safe_file(root,name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in {'notes','scripts'},'Unsafe public path')
    require(not any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)),'Symlinked public path')
    full=root/p;require(full.is_file(),'Missing public file: '+name)
    return full


def validate_structural(plan,result,rows):
    require(result['complete'] is True and result['gpus']==8 and result['functional_validation'] is False,'Structural completion/promotion')
    require(result['drug_ranking_changed'] is False,'Drug promotion')
    expected_contexts=plan['primary_contexts']+plan['sensitivity_contexts']
    require(result['contexts']==expected_contexts==528 and result['sample_count']==plan['expected_samples']==67584,'Structural count drift')
    require(len(rows)==result['site_amino_acid_records']==10560,'Missing site distributions')
    groups={}
    for row in rows:
        key=(int(row['shard']),row['variant'],int(row['structure_seed']),int(row['position']))
        groups.setdefault(key,[]).append(row)
        require(row['alt'] in 'ACDEFGHIKLMNPQRSTVWY','Unexpected amino acid')
        for field in ['mean_probability','mean_log_odds','min_log_odds','max_log_odds','sd_log_odds']:
            require(math.isfinite(float(row[field])),'Nonfinite structural score')
    require(len(groups)==528,'Missing backbone/site context')
    for (shard,variant,seed,pos),group in groups.items():
        require(0<=shard<8 and seed in [11,12,13] and variant in ['WT','N1002K'],'Structural context drift')
        require(pos in (plan['positions'] if variant=='WT' else [1002]),'Wrong scored position')
        require(len(group)==20 and {r['alt'] for r in group}==set('ACDEFGHIKLMNPQRSTVWY'),'Incomplete amino acid distribution')
        require(abs(sum(float(r['mean_probability']) for r in group)-1)<2e-5,'Probability normalization')
        reference=[r for r in group if r['alt']==r['reference']]
        require(len(reference)==1 and abs(float(reference[0]['mean_log_odds']))<1e-12,'Reference score not zero')
    comparisons=result['comparisons'];require(len(comparisons)==24,'Comparison coverage')
    seen=set()
    for row in comparisons:
        model=plan['models'].index(dict(zip(['variant','name'],row['model'].split('/'))))
        shard=2*model+plan['structure_sources'].index(row['arm']);seed=row['structure_seed']
        require((shard,seed) not in seen,'Duplicate comparison');seen.add((shard,seed))
        def score(variant,backbone='WT'):
            ref,alt=variant[0],variant[-1];pos=int(variant[1:-1])
            item=next(r for r in groups[shard,backbone,seed,pos] if r['alt']==alt)
            require(item['reference']==ref,'Reference identity drift')
            return float(item['mean_log_odds'])
        controls={c['variant']:score(c['variant']) for c in plan['controls']}
        require(controls==row['control_scores'],'Control summary drift')
        impaired=[controls[c['variant']] for c in plan['controls'] if c['group']=='primary_impaired']
        retained=[controls[c['variant']] for c in plan['controls'] if c['group']=='primary_retained']
        ei=[controls[c['variant']] for c in plan['controls'] if c['group'].endswith('_impaired')]
        er=[controls[c['variant']] for c in plan['controls'] if c['group'].endswith('_retained')]
        require(row['primary_controls_pass'] is (max(impaired)<min(retained)),'Primary gate drift')
        require(row['expanded_controls_pass'] is (max(ei)<min(er)),'Expanded gate drift')
        candidate=score('N1002K');require(row['candidate_log_odds']==candidate,'Candidate drift')
        require(row['candidate_backbone_log_odds']==score('N1002K','N1002K'),'Backbone sensitivity drift')
        background=[float(r['mean_log_odds']) for (sh,b,se,p),g in groups.items() if sh==shard and b=='WT' and se==seed for r in g if r['reference']=='N' and r['alt']=='K']
        require(row['matched_NK_count']==len(background)==17 and row['matched_NK_at_or_below']==sum(v<=candidate+1e-9 for v in background),'Matched background drift')
        alternatives=[float(r['mean_log_odds']) for r in groups[shard,'WT',seed,1002] if r['alt']!='N']
        require(row['alternate_rank_most_compatible_first']==1+sum(v>candidate+1e-9 for v in alternatives),'Alternate rank drift')
    require(result['primary_controls_pass']==sum(r['primary_controls_pass'] for r in comparisons)==1,'Primary failures suppressed')
    require(result['expanded_controls_pass']==sum(r['expanded_controls_pass'] for r in comparisons)==0,'Expanded failures suppressed')
    for name in ['exact_stock_control','direct_conditional_control']:require(result[name]['passed'] is True,'Numerical control failed')
    require(result['direct_conditional_control']['max_abs_probability_error']<=plan['numerical_tolerance'],'Conditional error')
    require([r['shard'] for r in result['completion']]==list(range(8)) and all(r['complete'] is True for r in result['completion']),'Worker coverage')


def validate_expression(plan,result):
    require(result['complete'] is True and result['biological_validation'] is False and result['drug_ranking_changed'] is False,'Expression promotion/completion')
    expected=[(c,s,q,z) for c in plan['cells'] for s in plan['spaces'] for q in plan['quality_views'] for z in plan['partition_seeds']]
    require(len(result['records'])==result['tasks']==80,'Missing expression tasks')
    fits=0
    for i,row in enumerate(result['records']):
        require(row['task']==i and (row['cell'],row['space'],row['quality'],row['partition_seed'])==expected[i],'Task membership drift')
        require(row['each_reference_evaluated_once'] is True,'Reference coverage failed')
        require([f['fold'] for f in row['folds']]==list(range(5)),'Fold coverage')
        for fold in row['folds']:
            fits+=1
            require(fold['train_test_disjoint'] is True and fold['orthogonality_error']<=1e-8,'Projection validity failed')
            require(set(fold['representations'])==set(plan['representations']),'Missing representation')
            for rep in fold['representations'].values():
                genes=[q['gene'] for q in rep['queries']]+[m['gene'] for m in rep['missing']]
                require(sorted(genes)==sorted(plan['query_genes']),'Missing or duplicated query')
                for q in rep['queries']:
                    require(math.isfinite(q['correlation']) and -1.000001<=q['correlation']<=1.000001,'Invalid correlation')
                    require(1<=q['rnai_rank']<=rep['rnai_reference_genes'] and 1<=q['crispr_rank']<=rep['crispr_reference_genes'],'Rank denominator drift')
                    if row['quality']=='crispr_quality_pass_only':require(q['crispr_quality_pass']==q['crispr_profiles']>0,'QC leakage')
                if row['cell']=='MCF7' and row['quality']=='crispr_quality_pass_only':
                    require('BUB1B' in [m['gene'] for m in rep['missing']] and all(d['gene']!='BUB1B' for d in rep['drugs']),'Missing MCF7 query fabricated')
                for d in rep['drugs']:
                    require(d['reference_genes']==rep['crispr_reference_genes'] and 1<=d['reversal_rank']<=d['reference_genes'] and 1<=d['mimic_rank']<=d['reference_genes'],'Drug rank drift')
    require(fits==result['fits']==plan['expected_fits']==400,'Fit count drift')
    require(result['comparisons']==sum(r['comparisons'] for r in result['runs'])==820147416,'Comparison count drift')
    require(result['max_cpu_error']<=plan['numerical_tolerance'] and result['max_v27_difference']<=plan['numerical_tolerance'] and result['full_unadjusted_control_count']==20,'Numerical continuity failure')
    require([r['shard'] for r in result['runs']]==list(range(8)) and sorted(t for r in result['runs'] for t in r['tasks'])==list(range(80)),'Worker task coverage')


def check(root=ROOT):
    audit=json.loads(safe_file(root,'notes/track2-orthogonal-audit-v29.json').read_text())
    for name,expected in audit['public_input_sha256'].items():
        require(hashlib.sha256(safe_file(root,name).read_bytes()).hexdigest()==expected,'Bound file changed: '+name)
    read=lambda name:json.loads(safe_file(root,'notes/'+name).read_text())
    sp=read('track2-structural-plan-v29.json');ep=read('track2-crossfit-plan-v29.json')
    s=read('track2-structural-results-v29.json');e=read('track2-crossfit-results-v29.json')
    with safe_file(root,'notes/track2-structural-probabilities-v29.tsv').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    validate_structural(sp,s,rows);validate_expression(ep,e)
    require(summarize(s,e)==read('track2-orthogonal-summary-v29.json'),'Derived summary drift')
    register=read('track2-orthogonal-register-v29.json')
    require([r['id'] for r in register['claims']]==[f'R{i}' for i in range(43,48)] and register['total_claim_records']==47,'Claim coverage')
    require(all(all(r.get(k) for k in ['support','challenge','falsifier','stop','reopen','next_action']) for r in register['claims']),'Missing falsification action')
    compute=read('track2-orthogonal-compute-v29.json')
    require(compute['all_owned_jobs_complete'] is True and compute['toolkit_executed'] is True and compute['gpus']==8,'Compute provenance drift')
    require(compute['subject_data_transferred'] is False and compute['new_hosted_model_provider'] is False,'Provider/data provenance drift')
    return dict(passed=True,version=29,gpus=8,structural_contexts=528,fixed_site_samples=67584,
        expression_fits=400,expression_comparisons=820147416,primary_control_passes=1,expanded_control_passes=0,
        claim_records=5,total_claim_records=47,new_neural_inference=True,toolkit_executed=True,
        biological_validation=False,drug_ranking_changed=False)


if __name__=='__main__':print(json.dumps(check(),indent=2))
