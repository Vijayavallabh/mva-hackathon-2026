#!/usr/bin/env python3
"""Recompute v27 descriptive summaries from complete, archived public outputs."""
import argparse
import csv
import itertools
import json
from pathlib import Path
import shutil
from track2_saturation_v27 import AA, digest, require, save

LABELS=['esmc300m','esmc600m','esmc6b','esm3']


def distribution(values,score):
    import numpy as np
    v=np.asarray(values,dtype=float)
    require(v.size>0 and np.isfinite(v).all(),'Invalid score distribution')
    return dict(n=int(v.size),negative=int((v<0).sum()),negative_fraction=float((v<0).mean()),
        at_or_below_candidate=int((v<=score).sum()),at_or_below_candidate_fraction=float((v<=score).mean()),
        quantiles=dict(zip(['min','q05','q25','median','q75','q95','max'],
                          map(float,np.quantile(v,[0,.05,.25,.5,.75,.95,1])))))


def analyze(root,old,output):
    import numpy as np
    from scipy.stats import spearmanr
    output.mkdir(exist_ok=False)
    plan=json.loads((root/'inputs/plan.json').read_text())
    oldscores=json.loads((old/'notes/track2-latest-protein-results.json').read_text())
    baseline={r['model']:r for r in oldscores['models'].values()}
    seq=''.join((root/'inputs/uniprot-O60566.fasta').read_text().splitlines()[1:])
    require(digest(root/'inputs/uniprot-O60566.fasta')==plan['reference']['reference_fasta_sha256'], 'Wrong reference')
    allmaps={};summaries=[];workers=[];max_old_error=0.
    for index,item in enumerate(plan['models']):
        rows=[];repo=item['repository']
        for shard in [index*2,index*2+1]:
            folder=root/f'outputs/protein-{shard}'
            s=json.loads((folder/'summary.json').read_text());workers.append(s)
            reg=json.loads((folder/'registration.json').read_text())
            require(reg['plan_sha256']==digest(root/'inputs/plan.json') and reg['script_sha256']==digest(root/'scripts/track2_saturation_v27.py'),'Plan/code drift')
            require(s['output_sha256']==digest(folder/'masked-log-probabilities.csv'),'Changed masked output')
            with (folder/'masked-log-probabilities.csv').open() as f: rows.extend(csv.DictReader(f))
        rows.sort(key=lambda r:([w['name'] for w in plan['windows']].index(r['window']),int(r['position'])))
        scores={}
        for r in rows:
            pos=int(r['position']);ref=r['reference']
            require(r['model']==repo and seq[pos-1]==ref,'Reference/model mismatch')
            for alt in AA:
                if alt==ref: continue
                key=(r['window'],pos,alt)
                require(key not in scores,'Duplicate masked coordinate')
                scores[key]=float(r[alt])-float(r[ref])
        expected={(w['name'],pos,a) for w in plan['windows'] for pos in range(w['start'],w['end']+1)
                  for a in AA if a!=seq[pos-1]}
        require(scores.keys()==expected,'Incomplete score landscape')
        name=f'track2-saturation-{LABELS[index]}-v27.tsv'
        with (output/name).open('x',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['model','window','position','reference',*AA],delimiter='\t',lineterminator='\n')
            writer.writeheader();writer.writerows(rows)
        olddiff=[]
        for r in baseline[repo]['rows']:
            variant=r['variant'];new=scores[r['window'],int(variant[1:-1]),variant[-1]]
            olddiff.append(abs(new-r['score']))
        error=max(olddiff);max_old_error=max(max_old_error,error)
        require(error<=2*plan['numerical_tolerance'],'Original 84 scores not reproduced')
        windows=[]
        for w in plan['windows']:
            wn=w['name'];score=scores[wn,1002,'K']
            samepos=[v for (win,p,a),v in scores.items() if win==wn and p==1002]
            contexts={
                'whole_window':[v for (win,p,a),v in scores.items() if win==wn],
                'common_domain':[v for (win,p,a),v in scores.items() if win==wn and 721<=p<=1044],
                'matched_N_to_K':[v for (win,p,a),v in scores.items() if win==wn and seq[p-1]=='N' and a=='K'],
                'position1002':samepos,
            }
            controls=[dict(c,score=scores[wn,int(c['variant'][1:-1]),c['variant'][-1]]) for c in plan['controls']]
            primary_retained=next(c['score'] for c in controls if c['group']=='primary_retained')
            primary_pass=all(primary_retained>c['score'] for c in controls if c['group']=='primary_impaired')
            all_retained=[c['score'] for c in controls if c['group'].endswith('retained')]
            all_impaired=[c['score'] for c in controls if c['group'].endswith('impaired')]
            windows.append(dict(window=wn,candidate_score=score,backgrounds={k:distribution(v,score) for k,v in contexts.items()},
                controls=controls,primary_gate=primary_pass,expanded_gate=min(all_retained)>max(all_impaired)))
        summaries.append(dict(model=repo,rows=len(rows),substitution_scores=len(scores),
            original_score_max_abs_error=error,windows=windows,public_matrix=name,public_matrix_sha256=digest(output/name)))
        allmaps[repo]=scores
    correlations=[]
    # All same-window cross-model and within-model cross-window comparisons.
    for repo,scores in allmaps.items():
        for wa,wb in itertools.combinations([w['name'] for w in plan['windows']],2):
            aa={(p,a):v for (w,p,a),v in scores.items() if w==wa}
            bb={(p,a):v for (w,p,a),v in scores.items() if w==wb}
            keys=sorted(aa.keys()&bb.keys())
            correlations.append(dict(kind='within_model_windows',model=repo,a=wa,b=wb,n=len(keys),
                 spearman=float(spearmanr([aa[k] for k in keys],[bb[k] for k in keys]).statistic)))
    for a,b in itertools.combinations(allmaps,2):
        for w in plan['windows']:
            keys=sorted(k for k in allmaps[a] if k[0]==w['name'])
            correlations.append(dict(kind='between_models',a=a,b=b,window=w['name'],n=len(keys),
                spearman=float(spearmanr([allmaps[a][k] for k in keys],[allmaps[b][k] for k in keys]).statistic)))
    save(output/'track2-saturation-results-v27.json',dict(version=27,complete=True,plan_sha256=digest(root/'inputs/plan.json'),
        models=summaries,workers=workers,correlations=correlations,masked_positions=sum(m['rows'] for m in summaries),
        substitution_scores=sum(m['substitution_scores'] for m in summaries),original_84_score_max_abs_error=max_old_error,
        unique_reference_positions=1050,unique_single_substitution_identities=19950,clinical_classification=False,
        drug_ranking_changed=False,biological_validation=False,neural_inference=True))
    specificity=[];specworkers=[]
    for shard in range(8):
        folder=root/f'outputs/specificity-{shard}'
        specworkers.append(json.loads((folder/'summary.json').read_text()))
        for p in sorted(folder.glob('*.json')):
            if p.name in ['summary.json','registration.json','feature-removal.json']: continue
            record=json.loads(p.read_text());specificity.append(record)
    require(len(specificity)==10 and len({(r['cell'],r['space']) for r in specificity})==10,'Missing specificity tasks')
    # Original frozen v25 shared-gene rows are the baseline numerical control.
    v25=json.loads((old/'notes/track2-crispr-results-v25.json').read_text())
    base={(r['cell'],r['space'],r['gene']):r for worker in v25['gpu_runs'] for c in worker['cells']
          for r in c['orthogonal_panel'] if r['features']=='all978'}
    baseline_checks=[]
    for record in specificity:
        for row in record['representations']['all978']['queries']:
            previous=base[record['cell'],record['space'],row['gene']]
            error=abs(row['correlation']-previous['correlation'])
            require(error<=2e-5 and row['rnai_rank']==previous['rnai_rank']
                    and row['crispr_rank']==previous['crispr_rank'],'v25 baseline mismatch')
            baseline_checks.append(dict(cell=record['cell'],space=record['space'],gene=row['gene'],max_abs_error=error))
    save(output/'track2-specificity-results-v27.json',dict(version=27,complete=True,
        plan_sha256=digest(root/'inputs/specificity-plan.json'),records=sorted(specificity,key=lambda r:(r['cell'],r['space'])),
        workers=specworkers,comparisons=sum(r['comparisons'] for r in specworkers),baseline_checks=baseline_checks,
        feature_removal=json.loads((root/'outputs/specificity-0/feature-removal.json').read_text()),
        drug_ranking_changed=False,biological_validation=False,post_hoc_sensitivity=True))
    shutil.copyfile(root/'inputs/uniprot-O60566.fasta',output/'track2-public-bubr1-v27.fasta')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('repository',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();analyze(a.root,a.repository,a.output)
