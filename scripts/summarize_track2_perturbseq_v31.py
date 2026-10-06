#!/usr/bin/env python3
"""Summarize all prespecified public Perturb-seq queries and cross-cell specificity."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from track2_perturbseq_v31 import CELLS, digest, require, save


def stats(values):
    a=np.asarray(values,dtype=float)
    return dict(n=len(a),minimum=float(a.min()),q025=float(np.quantile(a,.025)),
                median=float(np.median(a)),q975=float(np.quantile(a,.975)),maximum=float(a.max()))


def unit(x):
    x=np.asarray(x,dtype=np.float64);x=x-x.mean(1,keepdims=True)
    length=np.linalg.norm(x,axis=1,keepdims=True)
    require((length>1e-10).all(),'Degenerate vector')
    return x/length


def summarize(root, destination=None):
    out=destination or root/'outputs/analysis';out.mkdir(exist_ok=False)
    plan=json.loads((root/'inputs/plan.json').read_text());regs=[];completions=[]
    frames=[];nulls=[];logos=[];workers=[]
    for shard in range(8):
        d=root/'outputs'/f'worker-{shard}'
        reg=json.loads((d/'registration.json').read_text());comp=json.loads((d/'completion.json').read_text())
        require(comp['complete'] and comp['iterations']==256 and reg['iterations']==256,'Incomplete wave')
        require(reg['plan_sha256']==digest(root/'inputs/plan.json') and
                reg['amendment_sha256']==digest(root/'inputs/amendment.json'),'Plan drift')
        require(reg['script_sha256']==digest(root/'scripts/track2_perturbseq_v31.py'),'Executed code drift')
        frame=pd.read_csv(d/'split-query-records.tsv.gz',sep='\t');frame['shard']=shard;frame['cell']=reg['cell']
        frames.append(frame);regs.append(reg);completions.append(comp);workers.append(d)
        for r in json.loads((d/'matched-control-null.json').read_text()):nulls.append(r|dict(shard=shard,cell=reg['cell']))
        for r in json.loads((d/'leave-partition-out.json').read_text()):logos.append(r|dict(shard=shard,cell=reg['cell']))
    frame=pd.concat(frames,ignore_index=True);frame.to_csv(out/'all-split-query-records.tsv.gz',sep='\t',index=False)
    records=[]
    for (cell,gene,rep),f in frame.groupby(['cell','gene','representation']):
        require(len(f)==1024,'Missing/duplicate query repetitions')
        records.append(dict(cell=cell,gene=gene,representation=rep,
            correlation=stats(f.correlation),forward_rank=stats(f.forward_rank),reverse_rank=stats(f.reverse_rank),
            reference_constructs=sorted(f.reference_constructs.unique().astype(int).tolist()),
            forward_top1=int(f.forward_rank.eq(1).sum()),reverse_top1=int(f.reverse_rank.eq(1).sum()),
            forward_top10=int(f.forward_rank.le(10).sum()),reverse_top10=int(f.reverse_rank.le(10).sum())))
    grouped_null=[]
    for cell in CELLS:
        for gene in plan['queries']:
            for rep in ['all_features','no_queries','no_queries_or_cycle']:
                rows=[r for r in nulls if r['cell']==cell and r['gene']==gene and r.get('representation')==rep and r['evaluable']]
                if not rows:continue
                require(len(rows)==4,'Missing null shard')
                values=[v for r in rows for v in r['null_norms']]
                require(len(values)==1024,'Null draw mismatch')
                threshold=rows[0]['observed_norm']
                grouped_null.append(dict(cell=cell,gene=gene,representation=rep,observed_norm=threshold,
                    observed_norm_seed_max_difference=max(abs(r['observed_norm']-threshold) for r in rows),
                    null_norm=stats(values),greater_equal=sum(v>=threshold for v in values),
                    descriptive_tail=(1+sum(v>=threshold for v in values))/1025))
    batches=[]
    for cell in CELLS:
        for gene in plan['queries']:
            for rep in ['all_features','no_queries','no_queries_or_cycle']:
                # Full profiles do not depend on seed; retain the first shard only here.
                rows=[r for r in logos if r['cell']==cell and r['gene']==gene and r['representation']==rep and r['shard'] in [0,4]]
                if rows:batches.append(dict(cell=cell,gene=gene,representation=rep,partitions=len(rows),
                    correlation=stats([r['correlation'] for r in rows]),rank=stats([r['rank'] for r in rows]),
                    reference_includes_retained_cells=True))
    a=np.load(workers[0]/'full-profiles.npy');b=np.load(workers[4]/'full-profiles.npy')
    an,bn=regs[0]['names'],regs[4]['names'];duplicates=[]
    for i in range(8):
        base=0 if i<4 else 4
        require(regs[i]['names']==regs[base]['names'],'Reference order drift')
        v=np.load(workers[i]/'full-profiles.npy');z=np.load(workers[base]/'full-profiles.npy')
        error=float(np.max(np.abs(v-z)));require(error<=2e-5,'Seed-independent full profile drift')
        duplicates.append(dict(shard=i,reference_shard=base,max_error=error))
    var=pd.read_csv(root/'outputs/prepared/rpe1-features.tsv',sep='\t')
    other=pd.read_csv(root/'outputs/prepared/K562_essential-features.tsv',sep='\t')
    require(var.gene_id.tolist()==other.gene_id.tolist(),'Feature identity/order mismatch')
    cc=set((root/'inputs/cell-cycle.txt').read_text().split())
    masks={'all_features':np.ones(len(var),dtype=bool),
        'no_queries':~var.gene_name.isin(plan['queries']).to_numpy(),
        'no_queries_or_cycle':~var.gene_name.isin(set(plan['queries'])|cc).to_numpy()}
    crosses=[];within=[];full_panels=[]
    for key,mask in masks.items():
        aa,bb=unit(a[:,mask]),unit(b[:,mask]);sc=aa@bb.T
        np.save(out/(key+'-cross-cell-correlations.npy'),sc.astype(np.float32))
        bidx={g:i for i,g in enumerate(bn)};panel=[]
        for i,g in enumerate(an):
            if g not in bidx:continue
            j=bidx[g];v=float(sc[i,j])
            row=dict(construct=g,correlation=v,k562_rank=1+int((sc[i]>v+1e-6).sum()),
                rpe1_rank=1+int((sc[:,j]>v+1e-6).sum()),k562_denominator=len(bn),rpe1_denominator=len(an))
            panel.append(row)
            if any('_'+q+'_' in g for q in plan['queries']):crosses.append(row|dict(representation=key))
        pd.DataFrame(panel).to_csv(out/(key+'-all-shared-constructs.tsv.gz'),sep='\t',index=False)
        full_panels.append(dict(representation=key,shared_constructs=len(panel),
            k562_top1=sum(r['k562_rank']==1 for r in panel),rpe1_top1=sum(r['rpe1_rank']==1 for r in panel),
            limitation='General retrieval context; queried transcripts removed, not every reference target transcript.'))
        for cell,names,x in [(CELLS[0],an,aa),(CELLS[1],bn,bb)]:
            ids={q:[i for i,g in enumerate(names) if '_'+q+'_' in g] for q in plan['queries']}
            if not ids['BUB1B']:continue
            i=ids['BUB1B'][0];scores=x@x[i]
            order=np.argsort(-scores)
            top=[dict(construct=names[j],correlation=float(scores[j])) for j in order if j!=i][:20]
            pairs={q:float(scores[v[0]]) if v else None for q,v in ids.items()}
            within.append(dict(cell=cell,representation=key,bub1b_query_correlations=pairs,
                top20_other_constructs=top,drug_plus_deficit_measured=False))
    meta=json.loads((root/'outputs/prepared/manifest.json').read_text())
    output=dict(version=31,complete=True,plan_sha256=digest(root/'inputs/plan.json'),
        amendment_sha256=digest(root/'inputs/amendment.json'),query_metadata=meta['cells'],
        feature_counts=regs[0]['feature_counts'],split_results=records,null_results=grouped_null,
        partition_sensitivity=batches,cross_cell_queries=crosses,cross_cell_context=full_panels,
        within_cell_queries=within,full_profile_seed_checks=duplicates,
        missing_queries={c:json.loads((workers[0 if c==CELLS[0] else 4]/'missing-queries.json').read_text()) for c in CELLS},
        compute=dict(gpus=8,workers=8,split_repetitions=sum(r['iterations'] for r in completions),
            gpu_correlations=sum(r['comparisons'] for r in completions),
            cuda_product_seconds=sum(r['cuda_product_seconds'] for r in completions),
            max_dot_product_cpu_error=max(r['max_cpu_error'] for r in completions),
            worker_wall_seconds=[r['elapsed_seconds'] for r in completions],
            cpu_cross_cell_correlations=int(sc.size)*len(masks)),
        all_controls_sensitivity='unavailable; retained all-control and core-control membership is identical',
        drug_ranking_changed=False,biological_validation=False,phase_confirmed=False,clinical_exposure_margin=None,
        conditional_ranges_are_biological_confidence_intervals=False,neural_model_inference=False)
    save(out/'summary.json',output)
    print(json.dumps({'complete':True,'compute':output['compute'],'missing_queries':output['missing_queries']}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--output',type=Path);a=p.parse_args();summarize(a.root,a.output)
