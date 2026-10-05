#!/usr/bin/env python3
"""Recompute v29 summaries from complete model and held-out expression outputs."""
import argparse
import csv
import json
from pathlib import Path
from track2_orthogonal_v29 import digest, require, save

AA='ACDEFGHIKLMNPQRSTVWY'


def structural(root, out):
    import numpy as np
    jobs=json.loads((root/'inputs/mpnn-jobs.json').read_text())
    plan=json.loads((root/'inputs/structural-plan.json').read_text())
    seq=''.join((root/'inputs/public-reference.fasta').read_text().splitlines()[1:])[720:1044]
    rows=[];draws=[];sample_count=0;completion=[]
    for job in jobs:
        shard=job['shard'];folder=root/'outputs'/f'mpnn-{shard}'
        done=json.loads((root/'outputs'/f'mpnn-completion-{shard}.json').read_text());require(done['complete'],'Incomplete inference')
        completion.append(done)
        expected={c['name']+'.npz' for c in job['contexts']}
        require({p.name for p in (folder/'probs').glob('*.npz')}==expected,'Probability output coverage')
        for context in job['contexts']:
            pos=context['position'];index=pos-721;name=context['name']
            z=np.load(folder/'probs'/(name+'.npz'),allow_pickle=False)
            prob=z['probs'][:,index,:20].astype(np.float64)
            require(prob.shape==(plan['samples_per_context'],20),'Probability shape')
            require(np.isfinite(prob).all() and (prob>0).all(),'Invalid probabilities')
            require(np.max(np.abs(prob.sum(1)-1))<=2e-5,'Probability normalization')
            lines=(folder/'seqs'/(name+'.fa')).read_text().splitlines()
            sequences=[line for line in lines if line and not line.startswith('>')]
            require(len(sequences)==plan['samples_per_context']+1,'Sample membership')
            require(sequences[0]==seq,'Native sequence drift')
            for sample in sequences[1:]:
                require(len(sample)==len(seq) and all(a==b for i,(a,b) in enumerate(zip(sample,seq)) if i!=index),'Fixed residue changed')
            sample_count+=len(sequences)-1
            ref=AA.index(context['reference']);logodds=np.log(prob)-np.log(prob[:,ref,None])
            base=dict(shard=shard,model=job['model']['variant']+'/'+job['model']['name'],arm=job['arm'],**context)
            mean_prob=prob.mean(0)
            for k,aa in enumerate(AA):
                rows.append(base|dict(alt=aa,mean_probability=float(mean_prob[k]),
                    mean_log_odds=float(logodds[:,k].mean()),min_log_odds=float(logodds[:,k].min()),
                    max_log_odds=float(logodds[:,k].max()),sd_log_odds=float(logodds[:,k].std()),
                    log_odds_of_mean_probabilities=float(np.log(mean_prob[k]/mean_prob[ref]))))
            alts=['K'] if pos!=793 and pos!=795 and pos!=882 and pos!=911 else {793:['R'],795:['R','A'],882:['N','A'],911:['N']}[pos]
            for aa in alts:
                for i,value in enumerate(logodds[:,AA.index(aa)]):draws.append(base|dict(alt=aa,draw=i,log_odds=float(value)))
    require(len(rows)==(plan['primary_contexts']+plan['sensitivity_contexts'])*20 and sample_count==plan['expected_samples'],'Structural count mismatch')
    with (out/'track2-structural-probabilities-v29.tsv').open('x') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
    # Complete draw-level site probabilities are in the archive; selected log-odds trajectories retained there too.
    with (out/'structural-draws-v29.tsv').open('x') as f:
        w=csv.DictWriter(f,fieldnames=list(draws[0]),delimiter='\t');w.writeheader();w.writerows(draws)
    summaries=[]
    for model in sorted({r['model'] for r in rows}):
        for arm in plan['structure_sources']:
            for seed in plan['structure_seeds']:
                group=[r for r in rows if r['model']==model and r['arm']==arm and r['structure_seed']==seed and r['variant']=='WT']
                scores={f"{r['reference']}{r['position']}{r['alt']}":r['mean_log_odds'] for r in group}
                primary_i=[scores[c['variant']] for c in plan['controls'] if c['group']=='primary_impaired']
                primary_r=[scores[c['variant']] for c in plan['controls'] if c['group']=='primary_retained']
                expanded_i=[scores[c['variant']] for c in plan['controls'] if c['group'].endswith('_impaired')]
                expanded_r=[scores[c['variant']] for c in plan['controls'] if c['group'].endswith('_retained')]
                candidate=scores['N1002K'];background=[r['mean_log_odds'] for r in group if r['reference']=='N' and r['alt']=='K']
                alternatives=[r['mean_log_odds'] for r in group if r['position']==1002 and r['alt']!='N']
                sens=[r['mean_log_odds'] for r in rows if r['model']==model and r['arm']==arm and r['structure_seed']==seed and r['variant']=='N1002K' and r['alt']=='K']
                require(len(sens)==1 and len(background)==17,'Background/sensitivity coverage')
                summaries.append(dict(model=model,arm=arm,structure_seed=seed,primary_controls_pass=max(primary_i)<min(primary_r),
                    expanded_controls_pass=max(expanded_i)<min(expanded_r),control_scores={c['variant']:scores[c['variant']] for c in plan['controls']},
                    candidate_log_odds=candidate,candidate_backbone_log_odds=sens[0],
                    matched_NK_count=len(background),matched_NK_at_or_below=sum(v<=candidate+1e-9 for v in background),
                    alternate_rank_most_compatible_first=1+sum(v>candidate+1e-9 for v in alternatives)))
    result=dict(version=29,complete=True,gpus=8,contexts=plan['primary_contexts']+plan['sensitivity_contexts'],
        primary_contexts=plan['primary_contexts'],sensitivity_contexts=plan['sensitivity_contexts'],
        sample_count=sample_count,site_amino_acid_records=len(rows),comparisons=summaries,
        primary_controls_pass=sum(r['primary_controls_pass'] for r in summaries),expanded_controls_pass=sum(r['expanded_controls_pass'] for r in summaries),
        completion=completion,exact_stock_control=json.loads((root/'outputs/exact-stock-control.json').read_text()),
        direct_conditional_control=json.loads((root/'outputs/direct-conditional-control.json').read_text()),
        functional_validation=False,drug_ranking_changed=False)
    save(out/'track2-structural-results-v29.json',result)
    return result


def crossfit(root,out,repo):
    plan=json.loads((root/'inputs/crossfit-plan.json').read_text());rows=[];runs=[]
    for shard in range(8):
        folder=root/'outputs'/f'crossfit-{shard}'
        run=json.loads((folder/'completion.json').read_text());require(run['complete'],'Incomplete expression worker');runs.append(run)
        rows.extend(json.loads(p.read_text()) for p in sorted(folder.glob('task-*.json')))
    rows.sort(key=lambda r:r['task'])
    require([r['task'] for r in rows]==list(range(plan['expected_tasks'])),'Expression task coverage')
    require(sum(len(r['folds']) for r in rows)==plan['expected_fits'],'Fit coverage')
    previous=json.loads((repo/'notes/track2-specificity-results-v27.json').read_text())
    # Versioned v27 document's task records are located under `records`.
    old_records=previous.get('records',previous.get('tasks',[]))
    if not isinstance(old_records,list):old_records=[]
    diffs=[]
    for row in rows:
        for control in row['full_unadjusted_control']:
            old=next(r for r in old_records if r['cell']==row['cell'] and r['space']==row['space'])
            candidate=next(r for r in old['representations']['all978']['queries'] if r['gene']==control['gene'])
            diffs.append(abs(control['correlation']-candidate['correlation']))
            require(control['rnai_rank']==candidate['rnai_rank'] and control['crispr_rank']==candidate['crispr_rank'],'Original retrieval rank drift')
    require(len(diffs)==20 and max(diffs)<=plan['numerical_tolerance'],'Original correlation drift')
    result=dict(version=29,complete=True,gpus=8,tasks=len(rows),fits=sum(r['fits'] for r in runs),
        comparisons=sum(r['comparisons'] for r in runs),max_cpu_error=max(r['max_cpu_error'] for r in runs),
        full_unadjusted_control_count=len(diffs),max_v27_difference=max(diffs),runs=runs,records=rows,
        biological_validation=False,drug_ranking_changed=False)
    save(out/'track2-crossfit-results-v29.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('repo',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--only',choices=['structural','crossfit','both'],default='both');a=p.parse_args()
    a.output.mkdir(exist_ok=False)
    if a.only in ['structural','both']:structural(a.root,a.output)
    if a.only in ['crossfit','both']:crossfit(a.root,a.output,a.repo)
