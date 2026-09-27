#!/usr/bin/env python3
"""Bind completed public v19 outputs and locally recheck retained score/null arrays.

Requires the already safely extracted, hash-verified archive. Never reads subject data.
Refuses to overwrite an existing audit. This is a packaging audit, not a new analysis.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def require(value, message):
    if not value:
        raise ValueError(message)


def build(campaign, output):
    import numpy as np
    from verify_track2_transcriptome_archive import verify
    require(not output.exists(), 'Audit already exists')
    extracted = campaign / 'verified'
    archive = campaign / 'transcriptome-v19-audit.tar.gz'
    archive_record = dict(
        sha256='2a5749f0cffaedce2eb68bba7a5b99ad5478dce57879808011ba168d67c56272',
        bytes=117668567, files=457,
        manifest_sha256=digest(extracted / 'archive-manifest.json'))
    archive_verification = verify(archive, archive_record)
    manifest = json.loads((extracted / 'archive-manifest.json').read_text())['files']
    for name, expected in manifest.items():
        p = extracted / name
        require(p.is_file() and not p.is_symlink() and p.stat().st_size == expected['bytes'] and
                digest(p) == expected['sha256'], 'Extracted member mismatch: ' + name)

    public = lambda name: json.loads((ROOT / 'notes' / name).read_text())
    first = public('track2-transcriptome-results-v19.json')
    second = public('track2-transcriptome-phase2-results-v19.json')
    followup = public('track2-transcriptome-followup-results-v19.json')
    pairs = {
        'scripts/track2_transcriptome.py': 'scripts/track2_transcriptome.py',
        'scripts/track2_transcriptome_phase2.py': 'scripts/track2_transcriptome_phase2.py',
        'scripts/track2_transcriptome_followup.py': 'scripts/track2_transcriptome_followup.py',
        'scripts/track2_transcriptome_audit.py': 'scripts/track2_transcriptome_audit.py',
        'scripts/track2_transcriptome_environment.toml': 'pyproject.toml',
        'scripts/track2_transcriptome.uv.lock': 'uv.lock',
        'notes/track2-transcriptome-plan-v19.json': 'inputs/plan.json',
        'notes/track2-transcriptome-phase2-plan-v19.json': 'inputs/phase2-plan.json',
        'notes/track2-transcriptome-followup-plan-v19.json': 'inputs/followup-plan.json',
        'notes/track2-transcriptome-results-v19.json': 'outputs/transcriptome-results.json',
        'notes/track2-transcriptome-phase2-results-v19.json': 'outputs/phase2-results.json',
        'notes/track2-transcriptome-followup-results-v19.json': 'outputs/followup-results.json',
    }
    for local, remote in pairs.items():
        require(digest(ROOT / local) == digest(extracted / remote), 'Changed executed input/result: ' + local)

    vector_summary = []
    registrations = {}
    for prefix, count, result in [('shard-', 205034, first), ('phase2-shard-', 107404, second)]:
        vector_count = 0
        for p in sorted(extracted.glob(f'outputs/{prefix}*/query-*-all-compounds.npy')):
            x = np.load(p, allow_pickle=False)
            require(x.shape == (count,) and np.isfinite(x).all(), 'Invalid complete score vector')
            vector_count += 1
        require(vector_count == sum(len(q['spaces']) for q in result['queries']) == 39, 'Missing score vector')
        vector_summary.append(dict(wave=prefix, vectors=vector_count, profiles=count, comparisons=count*vector_count))
    for prefix in ['shard-', 'phase2-shard-', 'followup-shard-']:
        rows = [json.loads((extracted / f'outputs/{prefix}{i}/registration.json').read_text()) for i in range(8)]
        require([r['shard'] for r in rows] == list(range(8)), 'Missing device registration')
        require(all('H100' in r['device'] for r in rows), 'Unexpected device')
        registrations[prefix] = rows

    null_count = 0
    for result, posthoc in [(first, False), (followup, True)]:
        for q in result['rows' if posthoc else 'queries']:
            qi = q['query_index']
            prefix = 'followup-shard-' if posthoc else 'shard-'
            suffix = q['arm'] + '-null' if posthoc else 'reagent-checks'
            matches = list(extracted.glob(f'outputs/{prefix}*/query-{qi}-{suffix}.npz'))
            require(len(matches) == 1, 'Missing/duplicate null archive')
            data = np.load(matches[0], allow_pickle=False)
            null = data['null_statistics' if posthoc else 'null_median_split_scores']
            observed = data['observed_splits' if posthoc else 'split_scores']
            require(null.shape == (10000,) and np.isfinite(null).all() and np.isfinite(observed).all(), 'Invalid null array')
            statistic = float(np.median(observed))
            require(abs(statistic - q['split_median']) < 1e-12, 'Observed-statistic mismatch')
            tail = (1 + int(np.count_nonzero(null >= statistic))) / (1 + len(null))
            require(abs(tail - q['split_null_tail']) < 1e-12, 'Empirical-tail mismatch')
            null_count += len(null)
    require(null_count == 560000, 'Missing null draws')

    monitor = list(csv.reader((extracted / 'logs/gpu-monitor.csv').open()))[1:]
    monitoring = []
    for i in range(8):
        rows = [r for r in monitor if int(r[1]) == i]
        monitoring.append(dict(gpu=i, samples=len(rows),
            max_sampled_utilization_percent=max(int(r[2].strip().split()[0]) for r in rows),
            max_sampled_memory_mib=max(int(r[3].strip().split()[0]) for r in rows)))
    old_check = json.loads((campaign / 'local-archive-verification.json').read_text())
    require(old_check['passed'] and old_check['archive_sha256'] == archive_record['sha256'], 'Missing earlier local archive check')
    original = json.loads((extracted / 'outputs/original-gctx-audit.json').read_text())
    require(original['passed'] and original['comparisons'] == 139 and original['maximum_absolute_error'] < 2e-5,
            'Original-GCTX numerical audit failed')

    files = set(ROOT.glob('notes/track2-transcriptome*v19.*'))
    files.update(ROOT.glob('scripts/*track2_transcriptome*'))
    files.discard(output.resolve())
    require(all(p.is_file() and not p.is_symlink() for p in files), 'Unsafe public input')
    result = dict(schema_version=1, date='2026-09-27', data_origin='public_NIH_GEO_only',
        subject_inputs_transferred=False, inference_complete=True,
        computation_type='CUDA statistical reanalysis; no new neural-model inference',
        remote_root='/home/prachh/v/mva-track2-transcriptome-20260927',
        archive=archive_record, archive_verification=archive_verification,
        extracted_members_verified=len(manifest), source_and_result_byte_identity=pairs,
        source_manifests=[json.loads((extracted / p).read_text()) for p in
            ['outputs/prepared/manifest.json', 'outputs/phase2-prepared/manifest.json']],
        registrations=registrations, score_vectors=vector_summary,
        retained_null_draws_rechecked=null_count,
        original_gctx_audit={k:v for k,v in original.items() if k != 'checks'},
        original_gctx_audit_sha256=digest(extracted / 'outputs/original-gctx-audit.json'),
        output_inventory_sha256=digest(extracted / 'outputs/output-inventory.json'),
        output_inventory_files=len(json.loads((extracted / 'outputs/output-inventory.json').read_text())['files']),
        monitoring=monitoring,
        monitoring_limits='Five-second samples can miss short kernels; wall time is not GPU time; no sustained-saturation claim.',
        public_input_sha256={str(p.relative_to(ROOT)):digest(p) for p in sorted(files)})
    with output.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(dict(passed=True, public_files=len(files), archive_files=457, null_draws_rechecked=null_count), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('campaign', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    build(args.campaign, args.output)
