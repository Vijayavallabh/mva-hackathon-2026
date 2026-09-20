#!/usr/bin/env python3
"""Check observed coordinates, rather than deposited sequence length, in public PDBs."""
import argparse
import json
from pathlib import Path
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from track2_esm_pilot import digest, write_json


def audit(root):
    root=Path(root); output={}
    for pdb,chain in [('5KHU','Q'),('6TLJ','S')]:
        path=root/(pdb+'.cif');d=MMCIF2Dict(str(path))
        rows=zip(d['_atom_site.auth_asym_id'],d['_atom_site.label_seq_id'],
                 d['_atom_site.label_atom_id'],d['_atom_site.label_entity_id'])
        selected=[(int(pos),entity) for c,pos,atom,entity in rows if c==chain and atom=='CA']
        positions=sorted({p for p,e in selected});entities={e for p,e in selected}
        if len(entities)!=1:raise ValueError('Ambiguous chain/entity mapping')
        entity=next(iter(entities))
        sequences=dict(zip(d['_entity_poly.entity_id'],d['_entity_poly.pdbx_seq_one_letter_code_can']))
        sequence=''.join(sequences[entity].split())
        if len(sequence)!=1050 or sequence[1001]!='N':raise ValueError('Unexpected reference mapping')
        output[pdb]=dict(chain=chain,entity=entity,sha256=digest(path),deposited_sequence_length=len(sequence),
            observed_CA_count=len(positions),observed_label_min=min(positions),observed_label_max=max(positions),
            candidate_1002_observed=1002 in positions,domain_721_1044_CA=sum(721<=p<=1044 for p in positions))
    return output


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('out')
    a=p.parse_args();result=audit(a.root);write_json(a.out,result);print(json.dumps(result,indent=2))
