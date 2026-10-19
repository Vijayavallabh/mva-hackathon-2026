#!/usr/bin/env python3
"""Cross-guide contrastive learning with gene-held-out optical validation.

Only the coordinate-corrected public v35 preparation is accepted. Query genes never participate
in training or checkpoint selection. Model performance is not drug efficacy.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq
import torch
from torch import nn
from torch.nn import functional as F

from track2_optical_fetch_v33 import hashes, write_json
from track2_optical_prepare_v35 import PLAN_SHA, QUERIES

BASIC = ['nucleus_area', 'cell_area', 'nucleus_dapi_int', 'nucleus_dapi_mean',
         'nucleus_eccentricity', 'nucleus_form_factor', 'nucleus_solidity',
         'cell_eccentricity', 'cell_form_factor', 'cell_solidity']
AMENDMENT_SHA = '4231bcb4055c5aaa9899a5d9a0503e140fadafe99dd42240b9693f3cd8116946'


def eligible_groups(rows, split, minimum_guides=2):
    groups = {}
    for i, row in enumerate(rows):
        # The source encodes controls as individual gene labels starting with nontargeting.
        gene = row['gene']
        if (row['split'] != split or row['cells'] < 20 or not gene or
                'targeting' in gene.lower() or gene.lower().startswith('control')):
            continue
        groups.setdefault(gene, []).append(i)
    return {g: ix for g, ix in sorted(groups.items()) if len(ix) >= minimum_guides}


@torch.no_grad()
def retrieve(vectors, groups, distance='cosine'):
    """Every query guide is excluded from its own gene's reference profile.

    Other references aggregate their eligible guides. This unequal reference size
    is shared by all methods and retained as a limitation, not hidden replication.
    """
    names = list(groups)
    if len(names) < 2:
        raise ValueError('Insufficient reference genes')
    query_indices, true_index, ref_vectors, reference_counts = [], [], [], []
    for i, name in enumerate(names):
        ix = groups[name]
        query_indices.extend(ix)
        true_index.extend([i]*len(ix))
        ref_vectors.append(vectors[ix].mean(0))
        reference_counts.extend([len(ix)]*len(ix))
    q = vectors[query_indices]
    r = torch.stack(ref_vectors)
    truth = torch.tensor(true_index, device=vectors.device)
    count = torch.tensor(reference_counts, device=vectors.device).unsqueeze(1)
    own = (r[truth]*count-q)/(count-1)
    if distance == 'cosine':
        score = F.normalize(q, dim=1) @ F.normalize(r, dim=1).T
        own_score = (F.normalize(q, dim=1)*F.normalize(own, dim=1)).sum(1)
    elif distance == 'absolute':
        score = -(q[:,None,:]-r[None,:,:]).abs().mean(2)
        own_score = -(q-own).abs().mean(1)
    else:
        raise ValueError('Unknown distance')
    score[torch.arange(len(q), device=q.device), truth] = own_score
    if not torch.isfinite(score).all():
        raise ValueError('Nonfinite retrieval scores')
    # Explicit average ranks for exact ties, including constant/zero-vector baselines.
    ranks = 1 + (score > own_score[:,None]).sum(1) + ((score == own_score[:,None]).sum(1)-1)*0.5
    ranks = ranks.cpu().numpy()
    own_scores = own_score.cpu().numpy()
    best = score.argmax(1).cpu().numpy()
    rows = []
    for k, guide_index in enumerate(query_indices):
        rows.append(dict(gene=names[true_index[k]], guide_index=guide_index,
                         rank=float(ranks[k]), reference_genes=len(names),
                         own_score=float(own_scores[k]), best_gene=names[best[k]]))
    by_gene = {}
    for row in rows:
        by_gene.setdefault(row['gene'], []).append(row['rank'])
    mrr = {g: float(np.mean(1/np.asarray(values))) for g, values in by_gene.items()}
    return dict(macro_mrr=float(np.mean(list(mrr.values()))), genes=len(names),
                guide_queries=len(rows), by_gene_mrr=mrr, rows=rows,
                reference_policy='Other guides of own gene; all eligible guides of alternative genes')


class Encoder(nn.Module):
    def __init__(self, features):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(features,512), nn.GELU(),
                                    nn.Linear(512,256), nn.GELU(), nn.Linear(256,128))

    def forward(self, x):
        return self.layers(x)


def bag_loss(model, x, a, b):
    av = F.normalize(model(x[a]).mean(1).float(), dim=1)
    bv = F.normalize(model(x[b]).mean(1).float(), dim=1)
    logits = av @ bv.T / 0.1
    labels = torch.arange(len(a), device=x.device)
    return (F.cross_entropy(logits, labels)+F.cross_entropy(logits.T, labels))/2


@torch.no_grad()
def encode_guides(model, x, guide_index, number):
    sums = torch.zeros((number,128), device=x.device)
    # Use deterministic segmented sums after concatenation, avoiding CUDA index_add atomics.
    encoded = []
    for start in range(0,len(x),4096):
        with torch.autocast('cuda', dtype=torch.bfloat16):
            encoded.append(model(x[start:start+4096]).float())
    encoded = torch.cat(encoded)
    for g, indices in guide_index.items():
        sums[g] = encoded[indices].mean(0)
    if not torch.isfinite(sums).all():
        raise ValueError('Nonfinite learned profiles')
    return sums


@torch.no_grad()
def encode_plates(model, x, meta, guide_lookup, out):
    """Retain plate-separated means from the exact registered global cell sample."""
    encoded=[]
    for start in range(0,len(x),4096):
        with torch.autocast('cuda',dtype=torch.bfloat16):
            encoded.append(model(x[start:start+4096]).float().cpu().numpy())
    encoded=np.concatenate(encoded)
    rows,profiles=[],[]
    for (guide,plate),indices in meta.groupby(['sgRNA_0','plate'],sort=True).indices.items():
        rows.append(dict(guide_index=guide_lookup[guide],plate=str(plate),sampled_cells=len(indices)))
        profiles.append(encoded[indices].mean(0,dtype=np.float64).astype(np.float32))
    profiles=np.asarray(profiles)
    if not np.isfinite(profiles).all():
        raise ValueError('Nonfinite plate profiles')
    np.save(out/'learned_plate_profiles.npy',profiles,allow_pickle=False)
    write_json(out/'learned_plate_rows.json',rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    p.add_argument('--arm', choices=['mitotic','interphase'], required=True)
    p.add_argument('--seed', type=int, choices=[3301,3302,3303,3304], required=True)
    p.add_argument('--shuffled', action='store_true')
    p.add_argument('--smoke', action='store_true', help='Separate two-step engineering check, never a scientific result')
    args = p.parse_args()
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise ValueError('Expose exactly one idle GPU per worker')
    root = args.root.resolve()
    if hashes(root / 'inputs/plan.json')[1] != PLAN_SHA:
        raise ValueError('Plan changed')
    if hashes(root / 'inputs/amendment-v35.json')[1] != AMENDMENT_SHA:
        raise ValueError('Amendment changed')
    source = root / 'prepared-v35' / args.arm
    complete = json.loads((source/'complete.json').read_text())
    for name, digest in complete['outputs'].items():
        if hashes(source/name)[1] != digest:
            raise ValueError('Prepared input changed: '+name)
    label = f"{args.arm}-{args.seed}-{'shuffled' if args.shuffled else 'real'}" + ('-smoke' if args.smoke else '')
    out = root / 'models-v35' / label
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)
    rng = np.random.default_rng(args.seed)
    rows = json.loads((source/'guides.json').read_text())
    features = json.loads((source/'features.json').read_text())
    if any('centroid' in n or 'bounds_' in n or '_center_mass_' in n or
           '_max_location_' in n for n in features):
        raise ValueError('Absolute image coordinates in model inputs')
    if not set(BASIC).issubset(features):
        raise ValueError('Declared basic baseline features are absent')
    meta = pq.read_table(source/'sample_meta.parquet').to_pandas()
    data = np.load(source/'sample_x.npy', mmap_mode='r', allow_pickle=False)
    full = np.load(source/'full_profiles.npz', allow_pickle=False)
    training = eligible_groups(rows, 'train', minimum_guides=3)
    validation = eligible_groups(rows, 'validation')
    test = eligible_groups(rows, 'test')
    if set(QUERIES) & (training.keys() | validation.keys()):
        raise ValueError('Query leakage')
    if min(len(training),len(validation),len(test)) < 128:
        raise ValueError('Insufficient held-out gene coverage')
    fit_indices = [i for values in training.values() for i in values]
    fit_means = full['means'][fit_indices]
    finite_fraction = full['finite_counts'][fit_indices].sum(0) / sum(rows[i]['cells'] for i in fit_indices)
    center = np.nanmean(fit_means,axis=0)
    scale = np.nanstd(fit_means,axis=0)
    keep = (finite_fraction >= 0.95) & np.isfinite(center) & np.isfinite(scale) & (scale > 1e-6)
    if keep.sum() < 50:
        raise ValueError('Insufficient finite, variable features')
    center, scale = center[keep], scale[keep]
    def transform(values):
        v = np.asarray(values[:,keep], dtype=np.float32).copy()
        v = (v-center)/scale
        v[~np.isfinite(v)] = 0
        return np.clip(v,-10,10).astype(np.float32)
    x = torch.tensor(transform(data),device='cuda')
    profile = torch.tensor(transform(full['means']),device='cuda')
    guide_lookup = {r['guide']:i for i,r in enumerate(rows)}
    guide_index = {guide_lookup[g]:torch.tensor(indices,device='cuda') for g,indices in
                   meta.groupby('sgRNA_0',sort=True).indices.items()}
    # Store preprocessing and exact split membership for independent replay.
    np.savez(out/'preprocessing.npz', keep=keep, center=center, scale=scale)
    write_json(out/'split.json',dict(training=training, validation=validation, test=test))
    fit_groups = [list(v) for v in training.values()]
    if args.shuffled:
        pool = np.array([i for v in fit_groups for i in v]);rng.shuffle(pool)
        cursor = 0
        for j, original in enumerate(fit_groups):
            fit_groups[j] = pool[cursor:cursor+len(original)].tolist();cursor += len(original)
    write_json(out/'training-groups.json', fit_groups)
    model = Encoder(int(keep.sum())).cuda()
    optimizer = torch.optim.AdamW(model.parameters(),lr=0.0003,weight_decay=0.01)
    best, trace = -float('inf'), []
    steps = 2 if args.smoke else 3000
    registration = dict(arm=args.arm,seed=args.seed,shuffled=args.shuffled,smoke=args.smoke,
                        plan_sha256=PLAN_SHA,script_sha256=hashes(Path(__file__))[1],
                        amendment_sha256=AMENDMENT_SHA,
                        prepared_sha256=hashes(source/'complete.json')[1],
                        device=torch.cuda.get_device_name(0),torch_version=torch.__version__,
                        started_utc=datetime.now(timezone.utc).isoformat(),precision='BF16 autocast; FP32 parameters and scores; TF32 disabled',
                        features=int(keep.sum()),training_genes=len(training),validation_genes=len(validation),
                        test_genes=len(test),no_query_training=True,clinical_validation=False)
    write_json(out/'registration.json',registration)
    for step in range(1,steps+1):
        chosen = rng.choice(len(fit_groups),128,replace=False)
        aa,bb = [],[]
        for g in chosen:
            ga,gb = rng.choice(fit_groups[g],2,replace=False)
            ia,ib = guide_index[int(ga)],guide_index[int(gb)]
            aa.append(ia[torch.randint(len(ia),(32,),device='cuda')])
            bb.append(ib[torch.randint(len(ib),(32,),device='cuda')])
        a,b = torch.stack(aa),torch.stack(bb)
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast('cuda',dtype=torch.bfloat16):
            loss = bag_loss(model,x,a,b)
        if not torch.isfinite(loss):
            raise ValueError('Nonfinite training loss')
        loss.backward();optimizer.step()
        if step % 100 == 0 or step == steps:
            model.eval()
            learned = encode_guides(model,x,guide_index,len(rows))
            val = retrieve(learned,validation)
            record = dict(step=step,loss=float(loss.detach()),validation_mrr=val['macro_mrr'],
                          elapsed_seconds=time.monotonic()-started)
            trace.append(record);write_json(out/'trace.json',trace)
            if val['macro_mrr'] > best:
                best = val['macro_mrr'];torch.save(model.state_dict(),out/'best.pt')
                write_json(out/'best-validation.json',record)
            print(json.dumps(record),flush=True)
            model.train()
    model.load_state_dict(torch.load(out/'best.pt',map_location='cuda',weights_only=True));model.eval()
    learned = encode_guides(model,x,guide_index,len(rows))
    np.save(out/'learned_profiles.npy',learned.cpu().numpy(),allow_pickle=False)
    encode_plates(model,x,meta,guide_lookup,out)
    baseline_results = dict(full_profile=retrieve(profile,test))
    baseline_results['full_correlation'] = retrieve(profile-profile.mean(1,keepdim=True),test)
    kept_names = [n for n,k in zip(features,keep) if k]
    basic = [i for i,n in enumerate(kept_names) if n in BASIC]
    size = [i for i,n in enumerate(kept_names) if n in ['nucleus_area','cell_area']]
    if len(basic) < 2 or len(size) != 2:
        raise ValueError('Insufficient variable basic/size baseline features')
    baseline_results['basic_morphology'] = retrieve(profile[:,basic],test)
    baseline_results['size_only'] = retrieve(profile[:,size],test)
    abundance = torch.tensor([[np.log1p(r['cells'])] for r in rows],dtype=torch.float32,device='cuda')
    baseline_results['guide_abundance'] = retrieve(abundance,test,distance='absolute')
    # All dimensions are declared implementation sensitivities, not target-tuned choices.
    _, singular, vh = torch.linalg.svd(profile[fit_indices],full_matrices=False)
    for dim in [64,128,256]:
        if dim <= len(singular):
            white = (profile @ vh[:dim].T) / singular[:dim].clamp_min(1e-6)
            baseline_results['pca_whiten_'+str(dim)] = retrieve(white,test)
    result = dict(**registration, baseline_results=baseline_results, learned=retrieve(learned,test),
                  best_validation=json.loads((out/'best-validation.json').read_text()),
                  elapsed_seconds=time.monotonic()-started,
                  peak_gpu_bytes=torch.cuda.max_memory_allocated(),no_drug_promotion=True)
    result['baseline_feature_audit'] = dict(basic_retained=[kept_names[i] for i in basic],
        basic_excluded=[n for n in BASIC if n not in kept_names],
        size_retained=[kept_names[i] for i in size], coordinate_features=[])
    result['query_status'] = {gene: dict(
        eligible_guides=sum(r['gene']==gene and r['cells']>=20 for r in rows),
        status='evaluated' if gene in test else 'insufficient_guide_coverage',
        rank_is_missing=gene not in test) for gene in QUERIES}
    cpu_vectors = profile[:32].cpu().double().numpy()
    denom = np.linalg.norm(cpu_vectors,axis=1,keepdims=True)
    cpu_normal = cpu_vectors / np.maximum(denom,1e-12)
    cpu_dot = cpu_normal @ cpu_normal.T
    gpu_dot = (F.normalize(profile[:32],dim=1) @ F.normalize(profile[:32],dim=1).T).cpu().numpy()
    error = float(np.max(np.abs(cpu_dot-gpu_dot)))
    if error > 2e-5:
        raise ValueError('CPU/GPU similarity audit failed')
    result['numerical_audit'] = dict(cpu_float64_cuda_float32_max_absolute_error=error,
                                    tolerance=2e-5,rows=32,biological_validation=False)
    write_json(out/'results.json',result)
    write_json(out/'complete.json',dict(files={p.name:hashes(p)[1] for p in out.iterdir() if p.is_file()},
                                       elapsed_seconds=result['elapsed_seconds'],smoke=args.smoke))
    print(json.dumps(dict(label=label,elapsed_seconds=result['elapsed_seconds'],
                          learned_mrr=result['learned']['macro_mrr'])),flush=True)


if __name__ == '__main__':
    main()
