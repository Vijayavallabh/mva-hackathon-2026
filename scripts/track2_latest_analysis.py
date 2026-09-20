#!/usr/bin/env python3
"""Recheck complete newer-model matrices and all structures; no clinical classifier."""
import argparse
import itertools
import json
import math
from pathlib import Path
import re
from track2_esm_pilot import control_gate,digest,write_json
from track2_evo2_comparison import functional_gate,validate_inputs
from track2_model_result_audit import same
from track2_structure_analysis import aligned_distances


def sequence_check(result,plan):
    variants=plan['protein_controls']+[dict(variant=plan['protein_candidate'],group='candidate')]
    expected={(w['name'],v['variant'],v['group']) for w in plan['protein_windows'] for v in variants}
    rows=result['rows']
    if len(rows)!=21 or {(r['window'],r['variant'],r['group']) for r in rows}!=expected:
        raise ValueError('Missing, duplicated or relabelled protein score')
    if not all(math.isfinite(r['score']) for r in rows):raise ValueError('Nonfinite protein score')
    actual=control_gate([r for r in rows if r['group']!='candidate'])
    same(actual['windows'],result['gate']['windows'])
    repeat=result['gate']['repeat_max_abs_difference']
    numeric=math.isfinite(repeat) and 0<=repeat<=1e-6
    if result['gate']['numerical_pass']!=numeric or result['gate']['pass']!=(actual['pass'] and numeric):
        raise ValueError('Incorrect control/repeat disposition')
    for key in ['clinical_classification','drug_ranking_changed','phase_resolved']:
        if result[key] is not False:raise ValueError('Unsupported scientific promotion')
    return dict(model=result['model'],gate=result['gate'],candidate=[r for r in rows if r['group']=='candidate'])


def evo_check(result,document,plan):
    benchmark,candidates=validate_inputs(document,plan)
    expected={(r['id'],r['window']):r for r in benchmark+candidates}
    rows=result['benchmark']+result['candidate_scores']
    if len(rows)!=100 or len({(r['id'],r['window']) for r in rows})!=100:raise ValueError('Incomplete/duplicated DNA matrix')
    for row in rows:
        source=expected[(row['id'],row['window'])]
        for key in ['pos','ref','alt','group','assembly','window']:
            if row[key]!=source[key]:raise ValueError('DNA result/input mismatch')
        values=[row[k] for k in ['reference_forward','alternate_forward','reference_reverse_complement','alternate_reverse_complement']]
        if not all(map(math.isfinite,values)):raise ValueError('Nonfinite DNA likelihood')
        f,b=values[1]-values[0],values[3]-values[2]
        same([f,b,(f+b)/2],[row['delta_forward'],row['delta_reverse_complement'],row['delta_mean_strands']])
    same(functional_gate(result['benchmark']),result['benchmark_gate'])
    numeric=result['numerical_gate']
    if result['model']!='evo2_20b' or numeric['pass'] is not True or not math.isfinite(numeric['mean_loss']) or abs(numeric['mean_loss']-0.2166748046875)>=0.001 or not 0<=numeric['reference_repeat_abs_difference']<=1e-6:
        raise ValueError('DNA numerical qualification failed')
    for key in ['clinical_classification','drug_ranking_changed','phase_resolved']:
        if result[key] is not False:raise ValueError('Unsupported DNA scientific promotion')
    return dict(rows=100,benchmark_gate=result['benchmark_gate'],numerical_gate=numeric,candidate_scores=result['candidate_scores'])


def structures(root,label,plan):
    import numpy as np
    from Bio.PDB import MMCIFParser,PDBParser
    from Bio.SeqUtils import seq1
    folder=root/'outputs'/label
    if label=='ESMFold2-single_sequence':folder=root/'outputs/ESMFold2-single_sequence-retry'
    expected_sequence=''.join((root/'inputs/uniprot-O60566.fasta').read_text().splitlines()[1:])[720:1044]
    coords={};records=[]
    seeds=plan['structures']['seeds'];variants=plan['structures']['variants']
    af3=label=='AlphaFold3'
    files=folder.glob('*/seed-*_sample-*/*_model.cif') if af3 else list(folder.glob('*.pdb'))+list(folder.glob('*.cif'))
    for path in sorted(files):
        if af3:
            variant=path.parent.parent.name.upper()
            match=re.fullmatch(r'seed-(\d+)_sample-(\d+)',path.parent.name)
            seed,sample=map(int,match.groups())
        else:
            match=re.fullmatch(r'(WT|V793R|K795R|D911N|D882N|K795A|D882A|N1002K)-seed(\d+)',path.stem)
            if not match:raise ValueError('Unexpected structure name')
            variant,seed,sample=match.group(1),int(match.group(2)),0
        key=(variant,seed,sample)
        if key in coords:raise ValueError('Duplicate structure')
        parser=MMCIFParser(QUIET=True) if path.suffix=='.cif' else PDBParser(QUIET=True)
        chain=parser.get_structure('prediction',str(path))[0]['A']
        residues=[r for r in chain if 'CA' in r]
        if len(residues)!=324 or [r.id[1] for r in residues]!=list(range(1,325)):
            raise ValueError('Incomplete structure coordinates')
        expected=expected_sequence
        if variant!='WT':
            i=int(variant[1:-1])-721
            if expected[i]!=variant[0]:raise ValueError('Reference mismatch')
            expected=expected[:i]+variant[-1]+expected[i+1:]
        if ''.join(seq1(r.resname) for r in residues)!=expected:raise ValueError('Structure sequence mismatch')
        xyz=np.array([r['CA'].coord for r in residues]);coords[key]=xyz
        if not np.isfinite(xyz).all():raise ValueError('Nonfinite coordinates')
        confidence=np.array([r['CA'].bfactor for r in residues])
        if not np.isfinite(confidence).all():raise ValueError('Nonfinite CA confidence')
        records.append(dict(variant=variant,seed=seed,sample=sample,CA_count=324,mean_CA_bfactor=float(confidence.mean()),
            file=str(path.relative_to(root)),sha256=digest(path)))
    sample_ids=range(5) if af3 else [0]
    expected={(v,s,i) for v in variants for s in seeds for i in sample_ids}
    if set(coords)!=expected:raise ValueError(f'Incomplete {label} matrix: {len(coords)}/{len(expected)}')
    wt=[k for k in coords if k[0]=='WT'];comparisons=[]
    for variant in variants:
        pairs=itertools.combinations(wt,2) if variant=='WT' else itertools.product(wt,[k for k in coords if k[0]==variant])
        for a,b in pairs:
            distances=aligned_distances(coords[a],coords[b])
            row=dict(variant=variant,wt_seed=a[1],wt_sample=a[2],other_seed=b[1],other_sample=b[2],CA_rmsd_angstrom=float(np.sqrt(np.mean(distances**2))))
            if variant!='WT':
                mask=np.abs(np.arange(721,1045)-int(variant[1:-1]))<=10
                row['local_CA_rmsd_after_global_fit_angstrom']=float(np.sqrt(np.mean(distances[mask]**2)))
            comparisons.append(row)
    ranges={}
    for variant in variants:
        confidence=[r['mean_CA_bfactor'] for r in records if r['variant']==variant]
        rmsd=[r['CA_rmsd_angstrom'] for r in comparisons if r['variant']==variant]
        ranges[variant]=dict(mean_CA_bfactor_range=[min(confidence),max(confidence)],CA_rmsd_range_angstrom=[min(rmsd),max(rmsd)])
    return dict(model=label,structures=len(records),records=records,comparisons=comparisons,ranges=ranges,
        confidence_note='Raw CA B-factor field; check model export scaling before cross-model comparison.',
        interpretation='All samples retained. Seeds/samples/pairs are correlated computations, not biological replicates; confidence and RMSD do not measure function or rescue.',
        output_terms='https://github.com/google-deepmind/alphafold3/blob/main/OUTPUT_TERMS_OF_USE.md' if af3 else None)


def analyze(root,output):
    root=Path(root);out=Path(output);out.mkdir(exist_ok=False,parents=True)
    plan=json.loads((root/'inputs/latest-plan.json').read_text())
    sequence=[];bound=[]
    expected_repos=['biohub/ESMC-300M','biohub/ESMC-600M','biohub/ESMC-6B','EvolutionaryScale/esm3-sm-open-v1']
    for label,repo in zip(['ESMC-300M-score','ESMC-600M-score','ESMC-6B-score','ESM3-score'],expected_repos):
        folder=root/'outputs'/label
        result=json.loads((folder/'summary.json').read_text());registration=json.loads((folder/'preregistration.json').read_text())
        if result['model']!=repo or registration['repository']!=repo:raise ValueError('Model identity mismatch')
        if registration['plan_sha256']!=digest(root/'inputs/latest-plan.json'):raise ValueError('Protein plan drift')
        if registration['reference_sha256']!=digest(root/'inputs/uniprot-O60566.fasta'):raise ValueError('Reference drift')
        scripts=list((root/'scripts').glob('track2_latest_protein*.py'))
        if registration['script_sha256'] not in {digest(p) for p in scripts}:raise ValueError('Unbound scoring source')
        sequence.append(sequence_check(result,plan));bound.append(dict(file=str(folder/'summary.json'),sha256=digest(folder/'summary.json')))
    write_json(out/'protein-scores.json',dict(models=sequence,bound_results=bound))
    for label in ['AlphaFold3','ESM3-fold','ESMFold2-single_sequence','ESMFold2-shared_msa']:
        write_json(out/(label+'-structures.json'),structures(root,label,plan))
    result=json.loads((root/'outputs/Evo2-20B/summary.json').read_text())
    document=json.loads((root/'inputs/evo2-inputs.json').read_text())
    registration=json.loads((root/'outputs/Evo2-20B/preregistration.json').read_text())
    if document['plan_sha256']!=digest(root/'inputs/evo2-plan.json') or registration['inputs_sha256']!=digest(root/'inputs/evo2-inputs.json'):
        raise ValueError('DNA input provenance drift')
    if registration['script_sha256']!=digest(root/'scripts/track2_evo2_20b_comparison.py'):
        raise ValueError('DNA runner drift')
    write_json(out/'Evo2-20B-audit.json',evo_check(result,document,plan['evo2']))
    write_json(out/'audit.json',dict(passed=True,protein_models=4,structures=192,dna_rows=100,
        plan_sha256=digest(root/'inputs/latest-plan.json'),analysis_sha256=digest(__file__),
        protected_subject_inputs_used=False,clinical_validation=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('output');a=p.parse_args();analyze(a.root,a.output)
