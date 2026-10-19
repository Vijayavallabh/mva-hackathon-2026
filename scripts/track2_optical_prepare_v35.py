#!/usr/bin/env python3
"""Correct optical coordinate exclusion; retain guide and plate summaries (v35).

The input export is already normalized by its authors. Preserve complete-guide
counts/sums and a deterministic, feature-independent sample for neural fitting.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from track2_optical_fetch_v33 import hashes, selected_files, write_json, MIN_FREE_BYTES

PLAN_SHA = 'f9e56533068de83eea12844a1d660252a4f18c2e0f6133a65bdb484ea773fa1d'
AMENDMENT_SHA = '4231bcb4055c5aaa9899a5d9a0503e140fadafe99dd42240b9693f3cd8116946'
META = ['plate', 'well', 'tile', 'label', 'gene_symbol_0', 'group_0', 'sgRNA_0']
QUERIES = ['BUB1B', 'BUB1', 'MAD2L1', 'CDC20', 'TTK', 'AURKB', 'PLK1', 'MTOR', 'RPTOR', 'RICTOR']


def phenotype_columns(schema):
    result = []
    for field in schema:
        n = field.name
        if not (n.startswith('nucleus_') or n.startswith('cell_')):
            continue
        if not (pa.types.is_floating(field.type) or pa.types.is_integer(field.type)):
            continue
        if n in ['cell_0', 'cell_1', 'cell_i', 'cell_j', 'nucleus_i', 'nucleus_j']:
            continue
        if 'bounds_' in n or re.search(r'_(center_mass|max_location|centroid)_[rc]$', n):
            continue
        result.append(n)
    return result


def gene_split(gene):
    if gene in QUERIES:
        return 'test'
    value = int(hashlib.sha256(('track2-v33|' + gene).encode()).hexdigest(), 16) % 10
    return 'test' if value < 2 else 'validation' if value == 2 else 'train'


def cell_hashes(frame):
    identities = [json.dumps([str(p), str(w), int(t), int(l)], separators=(',', ':'))
                  for p, w, t, l in frame[['plate', 'well', 'tile', 'label']].itertuples(index=False, name=None)]
    digests = [hashlib.blake2b(s.encode(), digest_size=16).digest() for s in identities]
    # Keep the entire digest for duplicate checks; first 64 bits define sampling order.
    full = np.asarray(digests, dtype='V16')
    rank = np.asarray([int.from_bytes(d[:8], 'little') for d in digests], dtype=np.uint64)
    if len(np.unique(full)) != len(full):
        raise ValueError('Duplicate full cell identity within a source shard')
    return full, rank


def sample_indices(rank, limit=128):
    return np.argsort(rank, kind='stable')[:limit]


def prepare_file(job):
    root_string, arm, row, features = job
    root = Path(root_string)
    source = root / 'inputs' / arm / row['label']
    out = root / 'prepared-v35' / arm / 'shards' / str(row['dataFile']['id'])
    if (out / 'complete.json').exists():
        receipt = json.loads((out / 'complete.json').read_text())
        if receipt['script_sha256'] != hashes(Path(__file__))[1]:
            raise ValueError('Prepared shard used a different script; preserve it and use a new output root')
        for name, digest in receipt['outputs'].items():
            if hashes(out / name)[1] != digest:
                raise ValueError('Prepared shard changed: ' + str(out / name))
        return receipt
    out.mkdir(parents=True, exist_ok=False)
    if shutil.disk_usage(root).free < MIN_FREE_BYTES + 2 * 1024**3:
        raise RuntimeError('Free-space floor reached; preserve outputs')
    start = time.monotonic()
    md5, sha = hashes(source)
    if md5 != row['dataFile']['checksum']['value'] or source.stat().st_size != row['dataFile']['filesize']:
        raise ValueError('Source checksum failure: ' + str(source))
    table = pq.read_table(source, columns=META + features, use_threads=False)
    meta = table.select(META).to_pandas(ignore_metadata=True)
    full, ranks = cell_hashes(meta)
    x = np.column_stack([table.column(f).to_numpy(zero_copy_only=False) for f in features]).astype(np.float32)
    finite = np.isfinite(x)
    invalid = (~finite).sum(axis=0)
    x[~finite] = np.nan
    np.clip(x, -10, 10, out=x)
    summaries, means, counts, samples, sample_meta, sample_rank = [], [], [], [], [], []
    for guide, indices in meta.groupby('sgRNA_0', sort=True, dropna=False).indices.items():
        if not isinstance(guide, str) or not guide:
            raise ValueError('Missing guide identity')
        sub = meta.iloc[indices]
        genes = sub['gene_symbol_0'].fillna('').unique().tolist()
        groups = sub['group_0'].fillna('').unique().tolist()
        if len(genes) != 1 or len(groups) != 1:
            raise ValueError('A guide maps to multiple genes/groups')
        values = x[indices]
        counts.append(np.isfinite(values).sum(axis=0))
        means.append(np.nansum(values, axis=0, dtype=np.float64))
        summaries.append(dict(guide=guide, gene=genes[0], group=groups[0], cells=len(indices),
                              plate_well_counts=dict(Counter(str(p)+'|'+str(w) for p,w in
                                  sub[['plate','well']].itertuples(index=False, name=None)))))
        chosen = indices[sample_indices(ranks[indices])]
        samples.append(x[chosen])
        sample_meta.append(meta.iloc[chosen])
        sample_rank.append(ranks[chosen])
    np.savez(out / 'summary.npz', sums=np.asarray(means), finite_counts=np.asarray(counts),
             invalid_feature_counts=invalid)
    np.save(out / 'cell_hashes.npy', full, allow_pickle=False)
    np.save(out / 'sample_x.npy', np.concatenate(samples), allow_pickle=False)
    np.save(out / 'sample_rank.npy', np.concatenate(sample_rank), allow_pickle=False)
    import pandas as pd
    pq.write_table(pa.Table.from_pandas(pd.concat(sample_meta, ignore_index=True), preserve_index=False),
                   out / 'sample_meta.parquet')
    write_json(out / 'guides.json', summaries)
    plate_rows, plate_sums, plate_counts = [], [], []
    for (guide, plate), indices in meta.groupby(['sgRNA_0', 'plate'], sort=True).indices.items():
        values = x[indices]
        plate_rows.append(dict(guide=guide, plate=str(plate), cells=len(indices)))
        plate_sums.append(np.nansum(values, axis=0, dtype=np.float64))
        plate_counts.append(np.isfinite(values).sum(axis=0))
    write_json(out / 'guide_plates.json', plate_rows)
    np.savez(out / 'plate_summary.npz', sums=np.asarray(plate_sums),
             finite_counts=np.asarray(plate_counts))
    receipt = dict(source_file=row['label'], source_id=row['dataFile']['id'], source_sha256=sha,
                   cells=len(meta), sampled_cells=sum(len(v) for v in samples), features=len(features),
                   guides=len(summaries), elapsed_seconds=time.monotonic()-start,
                   script_sha256=hashes(Path(__file__))[1])
    receipt['outputs'] = {p.name: hashes(p)[1] for p in sorted(out.iterdir()) if p.is_file()}
    write_json(out / 'complete.json', receipt)
    return receipt


def merge(root, arm, features, receipts):
    import pandas as pd
    target = root / 'prepared-v35' / arm
    paths = [target / 'shards' / str(r['source_id']) for r in receipts]
    all_hashes = np.concatenate([np.load(p / 'cell_hashes.npy', allow_pickle=False) for p in paths])
    if len(np.unique(all_hashes)) != len(all_hashes):
        raise ValueError('Duplicate full cell identity across source shards; inspect before proceeding')
    del all_hashes
    guides = {}
    for p in paths:
        rows = json.loads((p / 'guides.json').read_text())
        stats = np.load(p / 'summary.npz', allow_pickle=False)
        source_sums, source_counts = stats['sums'], stats['finite_counts']
        for i, row in enumerate(rows):
            guide = row['guide']
            if guide not in guides:
                guides[guide] = dict(**row, sums=source_sums[i].copy(),
                                    finite_counts=source_counts[i].copy())
            else:
                old = guides[guide]
                if (old['gene'], old['group']) != (row['gene'], row['group']):
                    raise ValueError('Inconsistent cross-shard guide attribution')
                old['cells'] += row['cells']
                old['sums'] += source_sums[i]
                old['finite_counts'] += source_counts[i]
                counts = Counter(old['plate_well_counts']); counts.update(row['plate_well_counts'])
                old['plate_well_counts'] = dict(counts)
        stats.close()
    guide_rows = [guides[k] for k in sorted(guides)]
    sums = np.asarray([r.pop('sums') for r in guide_rows])
    counts = np.asarray([r.pop('finite_counts') for r in guide_rows])
    means = np.divide(sums, counts, out=np.full(sums.shape, np.nan), where=counts > 0)
    np.savez(target / 'full_profiles.npz', means=means, sums=sums, finite_counts=counts)
    for r in guide_rows:
        r['split'] = gene_split(r['gene'])
    write_json(target / 'guides.json', guide_rows)
    # Aggregate complete cells by acquisition plate, never by selected effect.
    plate_groups = {}
    for p in paths:
        plate_rows = json.loads((p / 'guide_plates.json').read_text())
        with np.load(p / 'plate_summary.npz', allow_pickle=False) as stats:
            ps, pc = stats['sums'], stats['finite_counts']
            for i, row in enumerate(plate_rows):
                key = (row['guide'], row['plate'])
                if key not in plate_groups:
                    plate_groups[key] = dict(**row, sums=ps[i].copy(), finite_counts=pc[i].copy())
                else:
                    old = plate_groups[key]
                    old['cells'] += row['cells']; old['sums'] += ps[i]
                    old['finite_counts'] += pc[i]
    plate_rows = [plate_groups[k] for k in sorted(plate_groups)]
    ps = np.asarray([r.pop('sums') for r in plate_rows])
    pc = np.asarray([r.pop('finite_counts') for r in plate_rows])
    pm = np.divide(ps, pc, out=np.full(ps.shape, np.nan), where=pc > 0)
    np.savez(target / 'plate_profiles.npz', sums=ps, finite_counts=pc, means=pm)
    write_json(target / 'guide_plates.json', plate_rows)
    del ps, pc, pm, plate_groups, plate_rows
    # Metadata is small; only selected feature rows are read through memory maps.
    metadata = []
    for i, p in enumerate(paths):
        frame = pq.read_table(p / 'sample_meta.parquet').to_pandas()
        frame['sample_rank'] = np.load(p / 'sample_rank.npy', allow_pickle=False)
        frame['shard_index'] = i
        frame['shard_row'] = np.arange(len(frame))
        metadata.append(frame)
    combined = pd.concat(metadata, ignore_index=True)
    chosen = combined.sort_values(['sgRNA_0', 'sample_rank'], kind='stable').groupby('sgRNA_0', sort=False).head(128)
    chosen = chosen.sort_values(['sgRNA_0', 'sample_rank'], kind='stable').reset_index(drop=True)
    dest = np.lib.format.open_memmap(target / 'sample_x.npy', mode='w+', dtype=np.float32,
                                    shape=(len(chosen), len(features)))
    for i, positions in chosen.groupby('shard_index').indices.items():
        shard = np.load(paths[i] / 'sample_x.npy', mmap_mode='r', allow_pickle=False)
        dest[positions] = shard[chosen.iloc[positions]['shard_row'].to_numpy()]
    dest.flush(); del dest
    pq.write_table(pa.Table.from_pandas(chosen, preserve_index=False), target / 'sample_meta.parquet')
    write_json(target / 'features.json', features)
    queries = {gene: [dict(guide=r['guide'], cells=r['cells'],
                           meets_20_cell_minimum=r['cells'] >= 20) for r in guide_rows if r['gene'] == gene]
               for gene in QUERIES}
    summary = dict(arm=arm, cells=sum(r['cells'] for r in receipts), sampled_cells=len(chosen),
                   guides=len(guide_rows), genes=len({r['gene'] for r in guide_rows}),
                   features=len(features), query_coverage=queries, plan_sha256=PLAN_SHA,
                   biological_validation=False, source_normalization_reused=True,
                   script_sha256=hashes(Path(__file__))[1], coordinate_exclusion_corrected=True,
                   amendment_sha256=AMENDMENT_SHA)
    summary['outputs'] = {p.name: hashes(p)[1] for p in target.iterdir() if p.is_file() and p.name != 'complete.json'}
    write_json(target / 'complete.json', summary)
    print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--arm', choices=['interphase', 'mitotic'], required=True)
    parser.add_argument('--workers', type=int, choices=range(1, 17), default=8)
    args = parser.parse_args()
    root = args.root.resolve()
    if hashes(root / 'inputs/plan.json')[1] != PLAN_SHA:
        raise ValueError('Plan changed')
    if hashes(root / 'inputs/amendment-v35.json')[1] != AMENDMENT_SHA:
        raise ValueError('Correction amendment changed')
    if not (root / 'outputs' / f'download-{args.arm}-complete.json').exists():
        raise ValueError('Download incomplete; do not analyze partial coverage')
    target = root / 'prepared-v35' / args.arm
    if (target / 'complete.json').exists():
        raise ValueError('Preparation already complete; preserve outputs')
    rows = [r for r in selected_files(root / 'inputs/dataverse-metadata.json', args.arm)
            if r['label'].startswith('part.')]
    features = phenotype_columns(pq.read_schema(root / 'inputs' / args.arm / '_common_metadata'))
    if any('centroid' in name for name in features):
        raise ValueError('Absolute coordinates remain in model inputs')
    jobs = [(str(root), args.arm, r, features) for r in rows]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        receipts = list(pool.map(prepare_file, jobs))
    merge(root, args.arm, features, receipts)


if __name__ == '__main__':
    main()
