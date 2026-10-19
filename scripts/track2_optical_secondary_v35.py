#!/usr/bin/env python3
"""Cross-arm count control and declared exploratory matched-sample baseline.

Run only after both complete public exports and all corrected fits. No refitting,
checkpoint selection, threshold changes or retrospective primary-gate rescue.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq

from track2_optical_fetch_v33 import hashes, write_json
from track2_optical_audit_v35 import paired_gain

SECONDARY_PLAN_SHA = 'fa09d60b1536d958a7cfa72df9553c04af43c47d7dfca1f2e4f42dd857febc23'
MEDIAN_PLAN_SHA = '533e75e8e8f3e122d102e8ef9b3628ecbb169d777a8f083e129196a1305f83b9'


def matched_fraction(rows, other_rows, arm):
    """A missing row means zero observed cells only after complete-export checks."""
    own={r['guide']:r for r in rows};other={r['guide']:r for r in other_rows}
    if len(own)!=len(rows) or len(other)!=len(other_rows):
        raise ValueError('Duplicate guide attribution')
    fractions=[];records=[]
    for row in rows:
        mate=other.get(row['guide'])
        if mate is not None and (mate['gene'],mate['group'])!=(row['gene'],row['group']):
            raise ValueError('Conflicting cross-arm guide attribution')
        n=int(row['cells']);m=int(mate['cells']) if mate else 0
        if n<=0 or m<0:raise ValueError('Invalid observed cell counts')
        mitotic=n if arm=='mitotic' else m
        interphase=m if arm=='mitotic' else n
        fractions.append(mitotic/(mitotic+interphase))
        records.append(dict(guide=row['guide'],gene=row['gene'],mitotic_cells=mitotic,
            interphase_cells=interphase,other_arm_zero_observed=mate is None))
    return np.asarray(fractions,dtype=np.float32)[:,None],records


def sampled_means(data,meta,rows):
    indices=meta.groupby('sgRNA_0',sort=True).indices
    if set(indices)!={r['guide'] for r in rows}:raise ValueError('Sample guide set differs')
    means=np.empty((len(rows),data.shape[1]),dtype=np.float64)
    finite_counts=np.empty_like(means,dtype=np.int64);sample_counts=[]
    for i,row in enumerate(rows):
        ix=indices[row['guide']]
        if not 1<=len(ix)<=min(128,row['cells']):raise ValueError('Sample count outside fixed cap')
        genes=set(meta.iloc[ix]['gene_symbol_0'].fillna(''))
        if genes!={row['gene']}:raise ValueError('Sample guide/gene attribution mismatch')
        values=np.asarray(data[ix],dtype=np.float32)
        finite=np.isfinite(values)
        if np.isinf(values).any() or (np.abs(values[finite])>10).any():
            raise ValueError('Prepared sample violates source clipping')
        counts=finite.sum(0);sums=np.where(finite,values,0).sum(0,dtype=np.float64)
        means[i]=np.divide(sums,counts,out=np.full(len(counts),np.nan),where=counts>0)
        finite_counts[i]=counts;sample_counts.append(len(ix))
    return means,finite_counts,np.asarray(sample_counts,dtype=np.int64)


def main():
    import torch
    from torch.nn import functional as F
    from track2_optical_model_v35 import eligible_groups,retrieve
    from track2_optical_prepare_v35 import QUERIES
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--arm',choices=['mitotic','interphase'],required=True);a=p.parse_args();root=a.root.resolve()
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1:
        raise ValueError('Expose exactly one idle GPU')
    if hashes(root/'inputs/secondary-plan-v35.json')[1]!=SECONDARY_PLAN_SHA:
        raise ValueError('Secondary plan changed')
    if hashes(root/'inputs/median-plan-v35.json')[1]!=MEDIAN_PLAN_SHA:
        raise ValueError('Median sensitivity plan changed')
    torch.backends.cuda.matmul.allow_tf32=False;torch.use_deterministic_algorithms(True)
    expected={'mitotic':(97,8399967217),'interphase':(3029,321585666869)}
    arm_rows={};bindings={}
    for arm,(files,byte_count) in expected.items():
        download=root/'outputs'/f'download-{arm}-complete.json'
        d=json.loads(download.read_text())
        if d['errors'] or d['completed']!=files or d['completed_bytes']!=byte_count:
            raise ValueError('Complete export coverage required')
        source=root/'prepared-v35'/arm
        complete=json.loads((source/'complete.json').read_text())
        if not complete['coordinate_exclusion_corrected'] or complete['features']!=1064:
            raise ValueError('Wrong preparation')
        if hashes(source/'guides.json')[1]!=complete['outputs']['guides.json']:
            raise ValueError('Prepared guide file changed')
        arm_rows[arm]=json.loads((source/'guides.json').read_text())
        bindings[str(download.relative_to(root))]=hashes(download)[1]
        bindings[str((source/'complete.json').relative_to(root))]=hashes(source/'complete.json')[1]
    source=root/'prepared-v35'/a.arm;rows=arm_rows[a.arm]
    complete=json.loads((source/'complete.json').read_text())
    for name in ['sample_x.npy','sample_meta.parquet','features.json','full_profiles.npz']:
        if hashes(source/name)[1]!=complete['outputs'][name]:raise ValueError('Prepared sample changed')
    out=root/'secondary-v35'/a.arm;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    meta=pq.read_table(source/'sample_meta.parquet').to_pandas()
    data=np.load(source/'sample_x.npy',mmap_mode='r',allow_pickle=False)
    means,finite_counts,sample_counts=sampled_means(data,meta,rows)
    np.savez(out/'sample_profiles.npz',means=means,finite_counts=finite_counts,sample_counts=sample_counts)
    del data,meta,finite_counts
    other='interphase' if a.arm=='mitotic' else 'mitotic'
    fractions,count_records=matched_fraction(rows,arm_rows[other],a.arm)
    write_json(out/'matched_counts.json',count_records)
    results=[];preprocess=None
    for shuffled in [False,True]:
        for seed in [3301,3302,3303,3304]:
            folder=root/'models-v35'/f"{a.arm}-{seed}-{'shuffled' if shuffled else 'real'}"
            done=json.loads((folder/'complete.json').read_text())
            if done['smoke']:raise ValueError('Smoke result excluded')
            for name in ['results.json','preprocessing.npz']:
                if hashes(folder/name)[1]!=done['files'][name]:raise ValueError('Model input changed')
            r=json.loads((folder/'results.json').read_text())
            if (r['arm'],r['seed'],r['shuffled'],r['smoke'])!=(a.arm,seed,shuffled,False):
                raise ValueError('Model identity mismatch')
            with np.load(folder/'preprocessing.npz') as pre:
                current={k:pre[k] for k in ['keep','center','scale']}
            if preprocess is None:preprocess=current
            elif any(not np.array_equal(preprocess[k],current[k]) for k in current):
                raise ValueError('Preprocessing differs between workers')
            results.append(r);bindings[str((folder/'complete.json').relative_to(root))]=hashes(folder/'complete.json')[1]
    groups=eligible_groups(rows,'test');genes=sorted(groups)
    for r in results:
        if sorted(r['learned']['by_gene_mrr'])!=genes:raise ValueError('Test cohort changed')
    v=np.asarray(means[:,preprocess['keep']],dtype=np.float32)
    v=(v-preprocess['center'])/preprocess['scale'];v[~np.isfinite(v)]=0
    v=np.clip(v,-10,10).astype(np.float32)
    vectors=torch.tensor(v,device='cuda')
    secondary=dict(mitotic_fraction=retrieve(torch.tensor(fractions,device='cuda'),groups,distance='absolute'),
                   matched_sample_mean=retrieve(vectors,groups))
    median_root=root/'median-v35'/a.arm
    median_complete=json.loads((median_root/'complete.json').read_text())
    if median_complete['plan_sha256']!=MEDIAN_PLAN_SHA:raise ValueError('Median result used another plan')
    for name in ['profiles.npz','guides.json','cpu_audit.json','features.json']:
        if hashes(median_root/name)[1]!=median_complete['outputs'][name]:
            raise ValueError('Median artifact changed')
    median_rows=json.loads((median_root/'guides.json').read_text())
    fields=['guide','gene','group','cells']
    if [[r[k] for k in fields] for r in median_rows]!=[[r[k] for k in fields] for r in rows]:
        raise ValueError('Median/prepared guide identity or counts differ')
    if (json.loads((median_root/'features.json').read_text())!=
            json.loads((source/'features.json').read_text())):raise ValueError('Median feature order differs')
    with np.load(median_root/'profiles.npz') as med:
        medians,median_finite=med['medians'],med['finite_counts']
    with np.load(source/'full_profiles.npz') as full:
        if not np.array_equal(median_finite,full['finite_counts']):raise ValueError('Median/source finite counts differ')
    if not np.array_equal(median_finite>0,np.isfinite(medians)):raise ValueError('Median missingness inconsistent')
    def standardize(values,mask,center,scale):
        transformed=(values[:,mask].astype(np.float32)-center)/scale
        transformed[~np.isfinite(transformed)]=0
        return torch.tensor(np.clip(transformed,-10,10).astype(np.float32),device='cuda')
    shared=standardize(medians,preprocess['keep'],preprocess['center'],preprocess['scale'])
    training=eligible_groups(rows,'train',minimum_guides=3)
    if set(QUERIES)&set(training):raise ValueError('Query leakage into median preprocessing')
    fit=medians[[i for ix in training.values() for i in ix]].astype(np.float64)
    center=np.nanmean(fit,axis=0);scale=np.nanstd(fit,axis=0)
    median_keep=preprocess['keep']&np.isfinite(center)&np.isfinite(scale)&(scale>1e-6)
    if median_keep.sum()<50:raise ValueError('Insufficient variable median features')
    median_fit=standardize(medians,median_keep,center[median_keep],scale[median_keep])
    secondary['full_median_shared_preprocessing']=retrieve(shared,groups)
    secondary['full_median_training_preprocessing']=retrieve(median_fit,groups)
    np.savez(out/'median_preprocessing.npz',keep=median_keep,center=center[median_keep],scale=scale[median_keep])
    bindings[str((median_root/'complete.json').relative_to(root))]=hashes(median_root/'complete.json')[1]
    cpu=v[:32].astype(np.float64);cpu/=np.maximum(np.linalg.norm(cpu,axis=1,keepdims=True),1e-12)
    gpu=(F.normalize(vectors[:32],dim=1)@F.normalize(vectors[:32],dim=1).T).cpu().numpy()
    error=float(np.max(np.abs(cpu@cpu.T-gpu)))
    if error>2e-5:raise ValueError('Secondary CPU/CUDA numerical check failed')
    baseline_names=sorted(results[0]['baseline_results'])
    baseline=np.array([[results[0]['baseline_results'][n]['by_gene_mrr'][g] for g in genes] for n in baseline_names])
    learned=np.array([[r['learned']['by_gene_mrr'][g] for g in genes] for r in results])
    fraction=np.array([secondary['mitotic_fraction']['by_gene_mrr'][g] for g in genes])
    sampled=np.array([secondary['matched_sample_mean']['by_gene_mrr'][g] for g in genes])
    registered=np.vstack([baseline,fraction]);exploratory=np.vstack([registered,sampled])
    med_matrix=np.array([[secondary[n]['by_gene_mrr'][g] for g in genes] for n in
                        ['full_median_shared_preprocessing','full_median_training_preprocessing']])
    all_baselines=np.vstack([exploratory,med_matrix])
    result=dict(arm=a.arm,plan_sha256=SECONDARY_PLAN_SHA,median_plan_sha256=MEDIAN_PLAN_SHA,
        bindings=bindings,secondary_results=secondary,
        test_genes=len(genes),original_baseline_names=baseline_names,original_primary_results_preserved=True,
        registered_gain_with_cross_arm=paired_gain(registered,learned[:4]),
        registered_shuffled_with_cross_arm=paired_gain(registered,learned[4:]),
        exploratory_gain_with_sampled_mean=paired_gain(exploratory,learned[:4]),
        exploratory_gain_with_all_baselines=paired_gain(all_baselines,learned[:4]),
        exploratory_shuffled_with_all_baselines=paired_gain(all_baselines,learned[4:]),
        median_variance_retained_features=int(median_keep.sum()),median_cell_counts_verified=True,
        sampled_cells=int(sample_counts.sum()),full_cells=sum(r['cells'] for r in rows),
        query_counts={g:[dict(r,sampled_cells=int(sample_counts[i])) for i,r in enumerate(count_records) if r['gene']==g] for g in QUERIES},
        cpu_float64_cuda_float32_max_absolute_error=error,numerical_tolerance=2e-5,
        script_sha256=hashes(Path(__file__))[1],elapsed_seconds=time.monotonic()-start,
        biological_validation=False,drug_ranking_changed=False,
        interpretation='Observed fixed-cell fractions are not viability. Matched-sample comparison was declared after mitotic results; it cannot replace the original full-data baseline or rescue a failed primary gate.')
    write_json(out/'results.json',result)
    write_json(out/'complete.json',dict(files={p.name:hashes(p)[1] for p in out.iterdir() if p.is_file()}))
    print(json.dumps(dict(arm=a.arm,test_genes=len(genes),sampled_cells=result['sampled_cells'],
        fraction_mrr=secondary['mitotic_fraction']['macro_mrr'],sample_mean_mrr=secondary['matched_sample_mean']['macro_mrr'],
        registered_gate=result['registered_gain_with_cross_arm']['practical_gain_gate_passed'])),flush=True)


if __name__=='__main__':main()
