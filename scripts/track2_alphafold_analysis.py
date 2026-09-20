#!/usr/bin/env python3
"""Retain every AlphaFold2 parameter set/seed and compare matched-model structures."""
import argparse
import itertools
import json
from pathlib import Path
import re
from track2_esm_pilot import digest,write_json
from track2_structure_analysis import aligned_distances


def analyze(root,output):
    import numpy as np
    from Bio.PDB import PDBParser
    from Bio.SeqUtils import seq1
    root=Path(root);plan=json.loads((root/'inputs/alphafold-plan.json').read_text())
    registration=json.loads((root/'outputs/alphafold-preregistration.json').read_text())
    if registration['plan_sha256']!=digest(root/'inputs/alphafold-plan.json'):
        raise ValueError('Plan changed after registration')
    pattern=re.compile(r'^(WT|V793R|K795R|D911N|D882N|K795A|D882A|N1002K)_unrelaxed_rank_\d+_alphafold2_ptm_model_([1-5])_seed_(\d+)\.pdb$')
    xyz={};records=[]
    for path in sorted((root/'outputs/alphafold').glob('*/*_unrelaxed_*.pdb')):
        match=pattern.fullmatch(path.name)
        if not match:raise ValueError('Unexpected prediction identity')
        variant,model,seed=match.group(1),int(match.group(2)),int(match.group(3))
        key=(variant,model,seed)
        if key in xyz:raise ValueError('Duplicate prediction')
        residues=[r for r in PDBParser(QUIET=True).get_structure('prediction',str(path))[0]['A'] if 'CA' in r]
        if [r.id[1] for r in residues]!=list(range(1,325)):
            raise ValueError('Unexpected coordinate mapping')
        expected=json.loads((root/f'inputs/boltz/{variant}.yaml').read_text())['sequences'][0]['protein']['sequence']
        if ''.join(seq1(r.resname) for r in residues)!=expected:raise ValueError('Structure/input sequence mismatch')
        xyz[key]=np.array([r['CA'].coord for r in residues])
        score=path.with_name(path.name.replace('_unrelaxed_','_scores_').replace('.pdb','.json'))
        scores=json.loads(score.read_text())
        if len(scores['plddt'])!=324:raise ValueError('Incomplete residue confidence')
        records.append(dict(variant=variant,model=model,seed=seed,pdb_sha256=digest(path),
            score_sha256=digest(score),mean_plddt=float(np.mean(scores['plddt'])),ptm=scores['ptm'],CA_count=324))
    expected={(v,m,s) for v in plan['variants'] for m in range(1,6) for s in plan['seeds']}
    if set(xyz)!=expected or len(records)!=120:
        raise ValueError(f'Incomplete prespecified matrix: {len(records)}/120 structures')
    comparisons=[]
    for model in range(1,6):
        for variant in plan['variants']:
            pairs=(itertools.combinations(plan['seeds'],2) if variant=='WT'
                   else itertools.product(plan['seeds'],plan['seeds']))
            for wt_seed,other_seed in pairs:
                distances=aligned_distances(xyz[('WT',model,wt_seed)],xyz[(variant,model,other_seed)])
                result=dict(variant=variant,model=model,wt_seed=wt_seed,other_seed=other_seed,
                    CA_rmsd_angstrom=float(np.sqrt(np.mean(distances**2))))
                if variant=='WT':
                    result['local_reference_CA_rmsd_angstrom']={str(pos):float(np.sqrt(np.mean(distances[np.abs(np.arange(721,1045)-pos)<=10]**2))) for pos in [793,795,882,911,1002]}
                else:
                    pos=int(variant[1:-1]);mask=np.abs(np.arange(721,1045)-pos)<=10
                    result['local_CA_rmsd_after_global_fit_angstrom']=float(np.sqrt(np.mean(distances[mask]**2)))
                comparisons.append(result)
    ranges={}
    for variant in plan['variants']:
        confidence=[r['mean_plddt'] for r in records if r['variant']==variant]
        rmsd=[r['CA_rmsd_angstrom'] for r in comparisons if r['variant']==variant]
        ranges[variant]=dict(plddt_range_0_100=[min(confidence),max(confidence)],
            matched_model_CA_rmsd_range_angstrom=[min(rmsd),max(rmsd)])
    write_json(output,dict(plan_sha256=digest(root/'inputs/alphafold-plan.json'),
        analysis_script_sha256=digest(__file__),records=records,comparisons=comparisons,ranges=ranges,
        models=5,seeds=plan['seeds'],structures=120,clinical_classification=False,drug_ranking_changed=False,
        interpretation='All five parameter sets and all seeds retained; matching is within model. These are correlated computational sensitivities, not independent biological replication or a stability/function assay.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('output')
    a=p.parse_args();analyze(a.root,a.output)
