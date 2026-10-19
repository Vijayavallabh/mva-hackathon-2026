#!/usr/bin/env python3
"""Resume v35 preparation with typed, audited empty-shard support.

Nonempty shards use the unchanged v35 implementation. Existing completed shards
are hash-checked; incomplete outputs are moved into a preserved failure directory.
No feature, cell, guide, threshold, split or sampling policy changes.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import shutil
import time

import numpy as np
import pyarrow.parquet as pq

import track2_optical_prepare_v35 as core
from track2_optical_fetch_v33 import hashes, selected_files, write_json, MIN_FREE_BYTES


def prepare_file(job):
    root_string, arm, row, features = job
    root = Path(root_string)
    source = root/'inputs'/arm/row['label']
    out = root/'prepared-v35'/arm/'shards'/str(row['dataFile']['id'])
    empty = pq.read_metadata(source).num_rows == 0
    if (out/'complete.json').is_file():
        if not empty:
            return core.prepare_file(job)
        receipt = json.loads((out/'complete.json').read_text())
        if receipt['script_sha256'] != hashes(Path(__file__))[1] or receipt['cells'] != 0:
            raise ValueError('Empty shard receipt changed')
        for name, digest in receipt['outputs'].items():
            if hashes(out/name)[1] != digest:
                raise ValueError('Empty shard output changed')
        return receipt
    if out.exists():
        preserved = root/'outputs/preparation-v36-preserved'/arm/str(row['dataFile']['id'])
        preserved.parent.mkdir(parents=True, exist_ok=True)
        if preserved.exists():
            raise ValueError('An earlier incomplete shard is already preserved')
        out.rename(preserved)
    if not empty:
        return core.prepare_file(job)
    if shutil.disk_usage(root).free < MIN_FREE_BYTES+2*1024**3:
        raise RuntimeError('Storage floor reached')
    start = time.monotonic()
    md5, sha = hashes(source)
    if md5 != row['dataFile']['checksum']['value'] or source.stat().st_size != row['dataFile']['filesize']:
        raise ValueError('Empty source checksum failure')
    table = pq.read_table(source, columns=core.META+features, use_threads=False)
    if table.num_rows != 0:
        raise ValueError('Source changed after footer inspection')
    out.mkdir(parents=True, exist_ok=False)
    width = len(features)
    np.savez(out/'summary.npz', sums=np.empty((0,width), dtype=np.float64),
             finite_counts=np.empty((0,width), dtype=np.int64),
             invalid_feature_counts=np.zeros(width, dtype=np.int64))
    np.save(out/'cell_hashes.npy', np.empty(0, dtype='V16'), allow_pickle=False)
    np.save(out/'sample_x.npy', np.empty((0,width), dtype=np.float32), allow_pickle=False)
    np.save(out/'sample_rank.npy', np.empty(0, dtype=np.uint64), allow_pickle=False)
    pq.write_table(table.select(core.META), out/'sample_meta.parquet')
    write_json(out/'guides.json', [])
    write_json(out/'guide_plates.json', [])
    np.savez(out/'plate_summary.npz', sums=np.empty((0,width), dtype=np.float64),
             finite_counts=np.empty((0,width), dtype=np.int64))
    receipt = dict(source_file=row['label'], source_id=row['dataFile']['id'], source_sha256=sha,
                   cells=0, sampled_cells=0, features=width, guides=0,
                   elapsed_seconds=time.monotonic()-start, script_sha256=hashes(Path(__file__))[1],
                   empty_source_verified=True,
                   outputs={p.name:hashes(p)[1] for p in sorted(out.iterdir()) if p.is_file()})
    write_json(out/'complete.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--arm', choices=['interphase'], required=True)
    parser.add_argument('--workers', type=int, choices=range(1,17), default=8)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):
        raise ValueError('All processing stays under v')
    for name, digest in [('plan.json',core.PLAN_SHA), ('amendment-v35.json',core.AMENDMENT_SHA)]:
        if hashes(root/'inputs'/name)[1] != digest:
            raise ValueError('Registered plan changed')
    d = json.loads((root/'outputs/download-interphase-complete.json').read_text())
    if d['errors'] or d['completed'] != 3029 or d['completed_bytes'] != 321585666869:
        raise ValueError('Complete source coverage required')
    target = root/'prepared-v35'/args.arm
    if (target/'complete.json').exists():
        raise ValueError('Completed preparation protected')
    rows = [r for r in selected_files(root/'inputs/dataverse-metadata.json',args.arm)
            if r['label'].startswith('part.')]
    features = core.phenotype_columns(pq.read_schema(root/'inputs'/args.arm/'_common_metadata'))
    if len(features) != 1064:
        raise ValueError('Corrected feature definition changed')
    jobs = [(str(root), args.arm, r, features) for r in rows]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        receipts = list(pool.map(prepare_file, jobs))
    core.merge(root, args.arm, features, receipts)
    complete = json.loads((target/'complete.json').read_text())
    complete['empty_shard_repair'] = dict(version=36, script_sha256=hashes(Path(__file__))[1],
        nonempty_script_sha256=hashes(Path(core.__file__))[1],
        empty_sources=[dict(source_id=r['source_id'],source_file=r['source_file'],source_sha256=r['source_sha256'])
                       for r in receipts if r['cells']==0],
        all_shard_receipts={str(r['source_id']):hashes(target/'shards'/str(r['source_id'])/'complete.json')[1]
                            for r in receipts},
        scientific_policy_changed=False, incomplete_outputs_preserved=True)
    write_json(target/'complete.json', complete)


if __name__ == '__main__':
    main()
