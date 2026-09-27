#!/usr/bin/env python3
"""Read-only, standard-library audit of the complete v23 public RNAi addendum."""
import hashlib
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def require(ok,msg):
    if not ok:raise ValueError(msg)


def bh(values):
    order=sorted(range(len(values)),key=values.__getitem__);out=[None]*len(values);running=1.
    for rank in range(len(order)-1,-1,-1):
        i=order[rank];running=min(running,values[i]*len(values)/(rank+1));out[i]=running
    return out


def validate(data,sensitivity,register):
    require(data['complete'] is True and data['version']==23,'Incomplete RNAi analysis')
    require(data['drug_ranking_changed'] is False and data['biological_validation'] is False and data['independent_experiments_added']==0,'Unsupported scientific promotion')
    require(data['status']==dict(rescue_priority=None,everolimus='mechanistic_probe_only',hcq='reserve',clinical_exposure_margin=None,phase='unconfirmed',wet_lab_performed=False),'Status drift')
    runs=data['gpu_runs'];require([r['shard'] for r in runs]==list(range(8)) and all(r['complete'] for r in runs),'Incomplete eight-GPU coverage')
    rows=data['rows'];cells=['A375','A549','HA1E','HCC515','HEPG2','HT29','MCF7','PC3','VCAP']
    require(sorted((r['cell'],r['space']) for r in rows)==sorted((c,s) for c in cells for s in ['raw','prime']),'Cell/space coverage drift')
    require(sorted(x for r in runs for x in r['completed'])==sorted(r['cell']+'-'+r['space'] for r in rows),'GPU output coverage drift')
    require(all(r['cpu_gpu_max_difference']<=2e-5 for r in runs),'Numeric tolerance failed')
    require(all(not r['crispr_bub1b_present'] for r in rows),'Unsupported BUB1B CRISPR evidence')
    pairs=sum(r['rnai_reagents']*(r['rnai_reagents']-1)//2 for r in rows)
    require(pairs==sum(r['unordered_pairs'] for r in rows)==sum(r['unordered_pairs'] for r in runs),'Pair count drift')
    records=[];seed_greater={};ortho={}
    for row in rows:
        b=row['bub1b'];reagents=b['reagents']
        require(len(reagents)==b['n_reagents']==len({r['seed6'] for r in reagents})==len({r['seed7'] for r in reagents}),'Seed/reagent drift')
        require(row['classes']['different_gene_same_seed6']['mean']>row['classes']['same_gene_different_seed6']['mean'],'Global seed comparison changed')
        for r in b['nulls']:
            require(r['arm'] in ['seed6','batch_replicates'] and r['observed_mean_pair']==b['mean_pair'],'Conditional comparison drift')
            if r['status']=='complete':
                n=r['draws'];k=r['at_or_above'];require(type(n) is int and 0<=k<=n,'Invalid reference count')
                p=k/n if r['kind']=='exact_enumeration' else (k+1)/(n+1)
                require(p==r['tail'] and len(r['pool_sizes'])==len(reagents),'Tail/count mismatch')
            else:require(r['tail'] is None and any(v==0 for v in r['pool_sizes']),'Missing comparison promoted')
            records.append((row,r))
    require(len(records)==36,'Multiplicity family drift')
    for (_,r),q in zip(records,bh([r['tail'] if r['tail'] is not None else 1 for _,r in records])):
        require(abs(q-r['BH_q'])<1e-12,'Primary multiplicity drift')
        require(r['excess_coherence_under_null']==(r['tail'] is not None and q<=.05 and r['observed_mean_pair']>0),'Primary threshold drift')
    for space in ['raw','prime']:
        rr=[r for r in rows if r['space']==space]
        comp=[v for r in rr for v in r['bub1b']['reagents'] if v['seed_peers']['mean'] is not None]
        seed_greater[space]=dict(available=len(comp),seed_greater=sum(v['seed_peers']['mean']>v['gene_peers']['mean'] for v in comp))
        cc=[v for r in rr for v in r['orthogonal'] if v['status']=='complete']
        ortho[space]=dict(comparisons=len(cc),top1=sum(v['rank_worst']==1 for v in cc),top5percent=sum(v['rank_worst']/v['reference_genes']<=.05 for v in cc))
    require(seed_greater==dict(raw=dict(available=54,seed_greater=45),prime=dict(available=54,seed_greater=45)),'BUB1B seed summary drift')
    require(ortho==dict(raw=dict(comparisons=297,top1=14,top5percent=84),prime=dict(comparisons=297,top1=21,top5percent=93)),'Orthogonal summary drift')
    require(sensitivity['post_hoc'] is True and sensitivity['primary_replaced'] is False,'Sensitivity scope drift')
    sr=sensitivity['rows'];require(len(sr)==36,'Sensitivity family drift')
    slookup={(r['cell'],r['space'],r['arm']):r for r in sr};finite=[]
    for row,r in records:
        t=slookup[(row['cell'],row['space'],r['arm'])];p=(r['at_or_above']+1)/(r['draws']+1) if r['status']=='complete' else 1
        require(t['finite_reference_tail']==p and t['primary_tail']==r['tail'],'Sensitivity tail drift');finite.append(p)
    require(min(bh(finite))>.05 and sensitivity['primary_excess_count']==5 and sensitivity['finite_reference_BH_excess_count']==0 and sensitivity['finite_reference_BY_excess_count']==0,'Finite-reference counterweight lost')
    for (row,r),q in zip(records,bh(finite)):
        t=slookup[(row['cell'],row['space'],r['arm'])]
        require(abs(t['finite_reference_BH_q']-q)<1e-12 and abs(t['finite_reference_BY_q']-min(1,q*sum(1/i for i in range(1,37))))<1e-12,'Sensitivity adjustment drift')
    summary=data['summary']
    require(summary['unordered_pair_comparisons']==pairs==1536619950,'Comparison total drift')
    require(summary['null_sets']==sum(r.get('draws',0) for _,r in records)==sum(r['null_sets'] for r in runs)==5843968,'Null total drift')
    require(summary['orthogonal_comparisons']==sum(r['orthogonal_comparisons'] for r in rows)==2364754,'Orthogonal total drift')
    require(summary['v19_exact_signature_overlap']==summary['v19_same_distil_id_sets']==116782,'Overlap missing')
    require(summary['unknown_conditional_tests']==sum(r['tail'] is None for _,r in records)==2,'Unknown count drift')
    require(register['drug_dispositions_changed'] is False and register['biological_validation'] is False,'Register promotion')
    require([r['id'] for r in register['claims']]==['R28','R29','R30','R31','R32'],'Missing falsification claim')
    for r in register['claims']:
        require(all(r.get(k) for k in ['claim','support','challenge','falsifier','stop','reopen','next_action']),'Incomplete falsification record')
    return dict(passed=True,version=23,gpus=8,unordered_pair_comparisons=pairs,null_sets=5843968,orthogonal_comparisons=2364754,
        primary_threshold_crossings=5,finite_reference_threshold_crossings=0,unknown_comparisons=2,
        seed_comparison=seed_greater,orthogonal_reference=ortho,independent_bub1b_experiment=False,drug_ranking_changed=False,biological_validation=False)


def check(root=ROOT):
    audit=json.loads((root/'notes/track2-rnai-audit-v23.json').read_text())
    for name,expected in audit['public_input_sha256'].items():
        p=Path(name);require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in ['notes','scripts'],'Unsafe bound path')
        require(not any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)),'Symlinked bound path')
        require(hashlib.sha256((root/p).read_bytes()).hexdigest()==expected,'Bound RNAi input changed: '+name)
    data=json.loads((root/'notes/track2-rnai-results-v23.json').read_text())
    sensitivity=json.loads((root/'notes/track2-rnai-tail-sensitivity-v23.json').read_text())
    register=json.loads((root/'notes/track2-rnai-register-v23.json').read_text())
    require(sensitivity['primary_results_sha256']==hashlib.sha256((root/'notes/track2-rnai-results-v23.json').read_bytes()).hexdigest(),'Sensitivity provenance drift')
    require(data['plan_sha256']==audit['public_input_sha256']['notes/track2-rnai-plan-v23.json'],'Plan changed after run')
    require(audit['numerical']['passed'] and audit['archive_verification']['passed'],'Numerical/archive audit failed')
    require(audit['numerical']['retained_null_statistics']==data['summary']['null_sets'],'Retained controls drift')
    require(audit['numerical']['maximum_original_coordinate_error']<2e-5,'Original-coordinate check failed')
    require(len({r['device_uuid'] for r in audit['registrations']})==8,'Distinct GPU registration missing')
    for r in audit['registrations']:
        require(r['script_sha256']==audit['public_input_sha256']['scripts/track2_rnai_v23.py'] and r['plan_sha256']==data['plan_sha256'],'Worker code/plan drift')
    return validate(data,sensitivity,register)

if __name__=='__main__':print(json.dumps(check(),indent=2))
