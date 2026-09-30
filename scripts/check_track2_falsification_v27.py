#!/usr/bin/env python3
"""Public-only v27 consistency review; standard library, no GPU/network/subject inputs."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AA='ACDEFGHIKLMNPQRSTVWY'
REPRESENTATIONS=['all978','without_selected_cycle_stress_features','residual_pc1','residual_pc3','residual_pc10']


def require(ok,message):
    if not ok:raise ValueError(message)


def close(a,b,tol=1e-12):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b)<=tol


def path(root,relative):
    p=Path(relative)
    require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in ['notes','scripts'],'Unsafe public path')
    require(not any((root/Path(*p.parts[:i])).is_symlink() for i in range(1,len(p.parts)+1)),'Symlinked input')
    return root/p


def validate(protein,specificity,compute,register,report):
    require(protein['version']==specificity['version']==compute['version']==register['version']==27,'Wrong version')
    require(protein['complete'] is True and specificity['complete'] is True and compute['all_owned_jobs_complete'] is True,'Incomplete campaign')
    require(protein['masked_positions']==9472 and protein['substitution_scores']==179968,'Inflated model count')
    require(protein['unique_single_substitution_identities']==19950,'Model/window duplicates treated as unique variants')
    require(len(protein['workers'])==8 and {w['shard'] for w in protein['workers']}==set(range(8))
            and len(compute['gpu_uuids'])==len(set(compute['gpu_uuids']))==8,'Missing/distorted GPU evidence')
    require(sum(w['masked_positions'] for w in protein['workers'])==9472,'Incomplete workers')
    require(close(sum(w['cuda_forward_seconds'] for w in protein['workers']),compute['protein_cuda_forward_seconds'],1e-8),'CUDA time drift')
    require(compute['max_batch_single_abs_error']<=1e-4 and compute['max_repeat_abs_error']<=1e-4
            and protein['original_84_score_max_abs_error']<=2e-4,'Failed numerical controls')
    windows=[w for m in protein['models'] for w in m['windows']]
    require(len(windows)==12 and sum(w['primary_gate'] for w in windows)==12
            and sum(w['expanded_gate'] for w in windows)==4,'Lost control sensitivity')
    require(all(w['candidate_score']<0 for w in windows),'Candidate sign changed')
    require(all(.7<w['backgrounds']['whole_window']['negative_fraction']<.91 for w in windows),'Negative background erased')
    require(specificity['comparisons']==sum(w['comparisons'] for w in specificity['workers'])==918999010,'Inflated expression count')
    require(len(specificity['records'])==10 and len({(r['cell'],r['space']) for r in specificity['records']})==10,'Missing cell/space')
    require(len(specificity['baseline_checks'])==20 and all(r['max_abs_error']<=2e-5 for r in specificity['baseline_checks']),'Baseline not reproduced')
    require(all(w['max_cpu_error']<=2e-5 for w in specificity['workers']),'CUDA/CPU mismatch')
    require(specificity['feature_removal']['kept']==965 and len(specificity['feature_removal']['removed'])==13,'Feature removal drift')
    for r in specificity['records']:
        require(list(r['representations'])==REPRESENTATIONS,'Missing or selected sensitivity')
        for v in r['representations'].values():
            require({q['gene'] for q in v['queries']}=={'BUB1B','MTOR'},'Missing target/control')
            for q in v['queries']:
                require(len(q['rnai_top20'])==len(q['crispr_top20'])==20,'Selected neighbors')
            for d in v['drug_rows']:
                require(type(d['drug_qc']) is bool and type(d['query_qc_pass']) is int,'QC conflation')
    ht=next(r for r in specificity['records'] if r['cell']=='HT29' and r['space']=='prime')
    for v in ht['representations'].values():
        q=next(q for q in v['queries'] if q['gene']=='BUB1B')
        require(q['correlation']>0 and 2<=q['rnai_rank']<=5 and 2<=q['crispr_rank']<=5,'Lost favorable HT29 counterevidence')
        require(all(not d['drug_qc'] and float(d['dose'])==10 for d in v['drug_rows']),'HT29 drug/QC promotion')
    mc=next(r for r in specificity['records'] if r['cell']=='MCF7' and r['space']=='prime')
    for i,v in enumerate(mc['representations'].values()):
        low=[d for d in v['drug_rows'] if float(d['dose'])==.1]
        require(len(low)==2,'Lost MCF7 low-dose records')
        b=next(d for d in low if d['gene']=='BUB1B');m=next(d for d in low if d['gene']=='MTOR')
        require(b['reversal_rank']==[7,8,78,125,1184][i] and b['query_qc_pass']==0 and b['drug_qc'],'BUB1B reversal/QC overstated')
        require(m['mimic_rank']==1 and m['correlation']>0 and m['query_qc_pass']==1,'Lost stable MTOR control')
    require([r['id'] for r in register['claims']]==['R38','R39','R40','R41','R42'],'Missing claim challenges')
    for r in register['claims']:
        require(all(r.get(k) for k in ['support','challenge','falsifier','stop','reopen','next_action']),'Missing falsification action')
    for obj in [protein,specificity,register]:
        require(obj['drug_ranking_changed'] is False,'Unsupported drug promotion')
    require(register['phase']=='unconfirmed' and register['clinical_exposure_margin'] is None
            and register['rescue_priority'] is None and register['wet_lab_performed'] is False
            and register['independent_guide_qualified_contexts']==0,'Biological/clinical promotion')
    require(compute['uplifting_toolkit_executed'] is False and compute['subject_inputs_transferred'] is False
            and compute['new_provider'] is False,'Tool/provider scope drift')
    normalized=' '.join(report.lower().split())
    for phrase in ['not probabilities of pathogenicity','one guide','post-hoc sensitivity tests',
                   'not a causal effect','1,184','second-most compatible','8/12','no wet-lab',
                   'presentation v26','not executed','clinical exposure','internal numerical checks']:
        require(phrase in normalized,'Lost limitation/counterweight: '+phrase)
    return dict(passed=True,version=27,gpus=8,masked_positions=9472,substitution_scores=179968,
        expression_comparisons=918999010,claim_records=5,new_neural_inference=True,
        drug_ranking_changed=False,biological_validation=False,independent_guide_qualified_contexts=0)


def check(root=ROOT):
    root=Path(root)
    audit=json.loads(path(root,'notes/track2-falsification-audit-v27.json').read_text())
    for relative,expected in audit['public_input_sha256'].items():
        require(hashlib.sha256(path(root,relative).read_bytes()).hexdigest()==expected,'Changed bound input: '+relative)
    load=lambda name:json.loads(path(root,'notes/'+name).read_text())
    p=load('track2-saturation-results-v27.json');s=load('track2-specificity-results-v27.json')
    c=load('track2-falsification-compute-v27.json');r=load('track2-falsification-register-v27.json')
    plan=load('track2-saturation-plan-v27.json')
    sequence=''.join(path(root,'notes/track2-public-bubr1-v27.fasta').read_text().splitlines()[1:])
    require(len(sequence)==1050 and sequence[1001]=='N','Reference drift')
    for model in p['models']:
        with path(root,'notes/'+model['public_matrix']).open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
        require(len(rows)==2368,'Missing masked positions')
        seen=set();scores={}
        for row in rows:
            pos=int(row['position']);ref=row['reference'];wn=row['window']
            require(row['model']==model['model'] and 1<=pos<=1050 and ref==sequence[pos-1],'Reference/model mismatch')
            require((wn,pos) not in seen,'Duplicate position');seen.add((wn,pos))
            values={a:float(row[a]) for a in AA}
            require(all(math.isfinite(v) and v<=0 for v in values.values()) and sum(math.exp(v) for v in values.values())<=1.00001,'Invalid probability vector')
            for a in AA:
                if a!=ref:scores[wn,pos,a]=values[a]-values[ref]
        expected={(w['name'],pos) for w in plan['windows'] for pos in range(w['start'],w['end']+1)}
        require(seen==expected,'Coordinate coverage mismatch')
        for w in model['windows']:
            wn=w['window'];v=scores[wn,1002,'K']
            require(close(v,w['candidate_score']),'Candidate arithmetic mismatch')
            contexts={
                'whole_window':[x for (win,pos,a),x in scores.items() if win==wn],
                'common_domain':[x for (win,pos,a),x in scores.items() if win==wn and 721<=pos<=1044],
                'matched_N_to_K':[x for (win,pos,a),x in scores.items() if win==wn and sequence[pos-1]=='N' and a=='K'],
                'position1002':[x for (win,pos,a),x in scores.items() if win==wn and pos==1002],
            }
            for key,values in contexts.items():
                d=w['backgrounds'][key];n=len(values);negative=sum(x<0 for x in values);below=sum(x<=v for x in values)
                require(d['n']==n and d['negative']==negative and d['at_or_below_candidate']==below
                        and close(d['negative_fraction'],negative/n) and close(d['at_or_below_candidate_fraction'],below/n),'Background arithmetic mismatch')
            for control in w['controls']:
                variant=control['variant']
                require(close(control['score'],scores[wn,int(variant[1:-1]),variant[-1]]),'Control arithmetic mismatch')
    return validate(p,s,c,r,path(root,'notes/track2-falsification-v27.md').read_text())


if __name__=='__main__':print(json.dumps(check(),indent=2))
