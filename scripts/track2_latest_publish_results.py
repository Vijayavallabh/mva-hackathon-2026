#!/usr/bin/env python3
"""Check remote/local agreement and export permitted derived newer-model results."""
import argparse
import json
import math
from pathlib import Path
import shutil
from track2_esm_pilot import digest, write_json


def compare(left, right, differences):
    if isinstance(left, dict):
        if left.keys() != right.keys(): raise ValueError('Analysis key mismatch')
        for key in left: compare(left[key], right[key], differences)
    elif isinstance(left, list):
        if len(left) != len(right): raise ValueError('Analysis length mismatch')
        for a, b in zip(left, right): compare(a, b, differences)
    elif isinstance(left, float):
        if not math.isclose(left, right, rel_tol=1e-10, abs_tol=1e-10):
            raise ValueError('Numerical reanalysis mismatch')
        differences.append(abs(left - right))
    elif left != right:
        raise ValueError('Analysis value mismatch')


def publish(root, analysis, destination, crc):
    root, analysis, destination = map(Path, [root, analysis, destination])
    load = lambda p: json.loads(p.read_text())
    differences = []
    for path in sorted(analysis.glob('*.json')):
        local, remote = load(path), load(root/'outputs/final-audit'/path.name)
        if path.name == 'protein-scores.json':
            for document in [local, remote]:
                for row in document['bound_results']:
                    row['file'] = 'outputs/' + row['file'].split('outputs/', 1)[1]
        compare(local, remote, differences)
    plan = load(root/'inputs/latest-plan.json')
    if digest(Path('notes/track2-latest-model-plan.json')) != digest(root/'inputs/latest-plan.json'):
        raise ValueError('Public and executed plan differ')
    registrations = {}
    for label in ['ESMC-300M-score', 'ESMC-600M-score', 'ESMC-6B-score', 'ESM3-score',
                  'ESM3-fold', 'ESMFold2-single_sequence-retry', 'ESMFold2-shared_msa']:
        registration = load(root/'outputs'/label/'preregistration.json')
        item = next(m for m in plan['models'] if m['repository'] == registration['repository'])
        manifest = root/'outputs'/(item['repository'].replace('/', '_')+'-weights.json')
        if registration['revision'] != item['revision'] or load(manifest)['revision'] != item['revision']:
            raise ValueError('Model revision mismatch')
        for actual, expected in [
            (digest(manifest), registration['checkpoint_manifest_sha256']),
            (digest(root/'inputs/runtime/esm-uv.lock'), registration['lock_sha256']),
            (digest(root/'inputs/latest-plan.json'), registration['plan_sha256']),
            (digest(root/'inputs/uniprot-O60566.fasta'), registration['reference_sha256']),
            (plan['source_revisions']['Biohub/esm'], registration['source_revision'])]:
            if actual != expected: raise ValueError('Protein provenance mismatch')
        if registration['script_sha256'] not in {digest(p) for p in (root/'scripts').glob('track2_latest_protein*.py')}:
            raise ValueError('Scoring source missing')
        registrations[label] = registration
    registrations['Evo2-20B'] = load(root/'outputs/Evo2-20B/preregistration.json')
    evo = registrations['Evo2-20B']
    for name, local in [('pyproject.toml', 'track2_evo2_fp8_environment.toml'),
                        ('uv.lock', 'track2_evo2_fp8.uv.lock')]:
        if digest(Path('scripts')/local) != evo['environment_hashes'][name]:
            raise ValueError('Historical Evo runtime manifest mismatch')
    if evo['checkpoint_repository_revision'] != next(m['revision'] for m in plan['models'] if m['repository']=='arcinstitute/evo2_20b'):
        raise ValueError('Evo checkpoint revision mismatch')
    af3 = load(root/'outputs/af3-input-provenance.json')
    for name, expected in af3['files'].items():
        if digest(root/'inputs/af3'/name) != expected: raise ValueError('AF3 input mismatch')
    if af3['plan_sha256'] != digest(root/'inputs/latest-plan.json'):
        raise ValueError('AF3 plan mismatch')
    sources = load(root/'inputs/runtime/source-revisions.json')
    for alias, repo in [('esm','Biohub/esm'), ('alphafold3','google-deepmind/alphafold3'), ('evo2','ArcInstitute/evo2')]:
        if sources[alias]['revision'] != plan['source_revisions'][repo] or not sources[alias]['tracked_source_pristine']:
            raise ValueError('Upstream source mismatch')
    # Preserve exact executed versions; historical helpers already exist unchanged.
    for p in (root/'scripts').glob('*'):
        local = Path('scripts')/p.name
        if p.is_file() and local.exists() and digest(p) != digest(local):
            raise ValueError('Public/archived source mismatch: ' + p.name)
    for env in ['esm', 'af3']:
        if digest(root/'inputs/runtime'/(env+'-pyproject.toml')) != digest(Path('scripts')/('track2_latest_'+env+'_environment.toml')):
            raise ValueError('Environment specification mismatch')
        target = Path('scripts')/('track2_latest_'+env+'.uv.lock')
        source = root/'inputs/runtime'/(env+'-uv.lock')
        if target.exists():
            if digest(target) != digest(source): raise ValueError('Existing lock differs')
        else: shutil.copyfile(source, target)
    destination.mkdir(parents=True, exist_ok=True)
    write_json(destination/'track2-latest-protein-results.json', dict(
        models={label:load(root/'outputs'/label/'summary.json') for label in
                ['ESMC-300M-score','ESMC-600M-score','ESMC-6B-score','ESM3-score']},
        audit=load(analysis/'protein-scores.json')))
    exports = {
        'AlphaFold3-structures.json':'track2-alphafold3-results.json',
        'ESM3-fold-structures.json':'track2-esm3-structure-results.json',
        'ESMFold2-single_sequence-structures.json':'track2-esmfold2-single-results.json',
        'ESMFold2-shared_msa-structures.json':'track2-esmfold2-msa-results.json'}
    for source, target in exports.items(): write_json(destination/target, load(analysis/source))
    write_json(destination/'track2-evo2-20b-results.json', load(root/'outputs/Evo2-20B/summary.json'))
    audit = dict(load(analysis/'audit.json'), local_remote_max_abs_difference=max(differences),
                 comparison_absolute_and_relative_tolerance=1e-10,
                 additional_provenance_checks_passed=True,
                 archive=load(Path('results/feat009/latest-model-archive-verification-v1.json')))
    write_json(destination/'track2-latest-model-audit.json', audit)
    files = {str(p.relative_to(root)):load(p) for p in (root/'outputs').glob('*weights.json')}
    provenance = dict(sources=sources, registrations=registrations, resources=files,
        alphafold3_inputs=af3, alphafold3_postrun_crc32c=load(Path(crc)),
        archive_manifest=load(root/'archive-manifest.json'),
        corrections='See track2-latest-models.md: inherited plan prose, first device omission, failed CCD path, and environment-mutation flag. Original bytes retained.',
        output_terms='See alphafold3-output-terms.md and alphafold3-Legally-Binding-Terms-of-Use.txt')
    write_json(destination/'track2-latest-model-provenance.json', provenance)
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['root', 'analysis', 'destination', 'crc']: parser.add_argument(name)
    args = parser.parse_args()
    publish(args.root, args.analysis, args.destination, args.crc)
