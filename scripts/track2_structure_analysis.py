#!/usr/bin/env python3
"""All-seed structural comparisons; RMSD and confidence are not functional assays."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
from track2_esm_pilot import digest, write_json


def aligned_distances(fixed, moving):
    import numpy as np
    fixed, moving = np.asarray(fixed, dtype=float), np.asarray(moving, dtype=float)
    if fixed.shape != moving.shape or fixed.ndim != 2 or fixed.shape[1] != 3 or len(fixed) < 3:
        raise ValueError('Require matching nontrivial CA coordinate arrays')
    if not np.isfinite(fixed).all() or not np.isfinite(moving).all():
        raise ValueError('Nonfinite coordinates')
    a, b = fixed-fixed.mean(0), moving-moving.mean(0)
    u, _, vt = np.linalg.svd(b.T@a)
    correction = np.diag([1,1,np.linalg.det(u@vt)])
    rotated = b@(u@correction@vt)
    return np.linalg.norm(rotated-a,axis=1)


def summarize(root, output):
    import numpy as np
    from Bio.PDB import MMCIFParser
    from Bio.SeqUtils import seq1
    root = Path(root)
    plan = json.loads((root/'inputs/plan.json').read_text())
    prereg = json.loads((root/'outputs/boltz-preregistration.json').read_text())
    if prereg['plan_sha256'] != digest(root/'inputs/plan.json'):
        raise ValueError('Plan changed after registration')
    sequence = ''.join((root/'inputs/uniprot-O60566.fasta').read_text().splitlines()[1:])[720:1044]
    records, coords = [], {}
    for job in prereg['schedule']:
        variant, seed = job['variant'],job['seed']
        name = f'{variant}-seed{seed}'
        run = root/f'outputs/boltz/{name}'
        cifs = list(run.glob('**/predictions/*/*_model_0.cif'))
        confs = list(run.glob('**/predictions/*/confidence_*_model_0.json'))
        if len(cifs) != 1 or len(confs) != 1:
            raise ValueError(f'Missing/ambiguous output for {name}')
        structure = MMCIFParser(QUIET=True).get_structure(name,str(cifs[0]))
        residues = [r for r in structure[0]['A'] if 'CA' in r]
        if [r.id[1] for r in residues] != list(range(1,325)):
            raise ValueError('Unexpected domain residue mapping')
        expected = sequence
        if variant != 'WT':
            index = int(variant[1:-1])-721
            if expected[index] != variant[0]: raise ValueError('Reference mismatch')
            expected = expected[:index]+variant[-1]+expected[index+1:]
        if ''.join(seq1(r.resname) for r in residues) != expected:
            raise ValueError('Structure sequence differs from prescribed input')
        xyz = np.array([r['CA'].coord for r in residues])
        coords[(variant,seed)] = xyz
        confidence = json.loads(confs[0].read_text())
        records.append(dict(**job,cif_sha256=digest(cifs[0]),confidence_sha256=digest(confs[0]),
            confidence={k:confidence[k] for k in ['confidence_score','ptm','complex_plddt','complex_pde']},
            CA_count=len(residues)))
    seeds = plan['structural_comparison']['seeds']
    comparisons = []
    for variant in plan['structural_comparison']['variants']:
        pairs = list(itertools.combinations(seeds,2)) if variant=='WT' else list(itertools.product(seeds,seeds))
        for wt_seed,other_seed in pairs:
            distances = aligned_distances(coords[('WT',wt_seed)],coords[(variant,other_seed)])
            row=dict(variant=variant,wt_seed=wt_seed,other_seed=other_seed,
                     CA_rmsd_angstrom=float(np.sqrt(np.mean(distances**2))))
            if variant!='WT':
                pos=int(variant[1:-1]);mask=np.abs(np.arange(721,1045)-pos)<=10
                row['local_CA_rmsd_after_global_fit_angstrom']=float(np.sqrt(np.mean(distances[mask]**2)))
            comparisons.append(row)
    ranges={}
    for variant in plan['structural_comparison']['variants']:
        subset=[x for x in comparisons if x['variant']==variant]
        conf=[r['confidence']['complex_plddt'] for r in records if r['variant']==variant]
        rmsd=[r['CA_rmsd_angstrom'] for r in subset]
        ranges[variant]=dict(plddt_range=[min(conf),max(conf)],CA_rmsd_range_angstrom=[min(rmsd),max(rmsd)])
    write_json(output,dict(plan_sha256=digest(root/'inputs/plan.json'),records=records,
        comparisons=comparisons,ranges=ranges,analysis_script_sha256=digest(__file__),
        model='boltz 2.2.1',single_sequence=prereg.get('arm') != 'shared WT-derived MSA',
        msa_records=prereg.get('msa_records'),
        interpretation='All comparisons retained. Seeds and pairwise combinations are correlated sampling diagnostics, not independent biological replicates. Confidence/RMSD cannot establish stability, abundance, pathogenicity or rescue.',
        clinical_classification=False,drug_ranking_changed=False,phase_resolved=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('output')
    a=p.parse_args();summarize(a.root,a.output)
