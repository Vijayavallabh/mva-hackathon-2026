#!/usr/bin/env python3
"""Public-only v29 preparation, fixed-site ProteinMPNN execution and verification."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

OLD = Path('/home/prachh/v/mva-track2-expanded-latest-20260921')
PREP = Path('/home/prachh/v/mva-track2-crispr-20261001-v25/outputs/prepared')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def prepare(root):
    from Bio.PDB import MMCIFParser
    from Bio.SeqUtils import seq1
    plan = json.loads((root/'inputs/structural-plan.json').read_text())
    fasta = root/'inputs/public-reference.fasta'
    require(digest(fasta) == plan['reference']['reference_fasta_sha256'], 'Reference drift')
    seq = ''.join(fasta.read_text().splitlines()[1:])[720:1044]
    require(len(seq) == 324 and seq[281] == 'N', 'Reference indexing')
    structures = {}
    source_records = []
    for arm in plan['structure_sources']:
        expected = json.loads((root/'inputs'/('single-structures.json' if 'single' in arm else 'msa-structures.json')).read_text())
        byname = {Path(r['file']).name: r for r in expected['records']}
        for variant in plan['structure_variants']:
            for seed in plan['structure_seeds']:
                name = f'{variant}-seed{seed}.cif'
                src = OLD/'outputs'/arm/name
                require(digest(src) == byname[name]['sha256'], 'Changed original structure')
                dest = root/'inputs'/f'{arm}-{name}'
                shutil.copyfile(src, dest)
                model = MMCIFParser(QUIET=True).get_structure('public', dest)[0]
                chains = list(model)
                require(len(chains) == 1, 'Unexpected chains')
                residues = list(chains[0])
                observed = ''.join(seq1(r.resname) for r in residues)
                wanted = seq if variant == 'WT' else seq[:281]+'K'+seq[282:]
                require(observed == wanted, 'Backbone sequence mismatch')
                coords = {f'{a}_chain_A': [r[a].coord.astype(float).tolist() for r in residues]
                          for a in ['N', 'CA', 'C', 'O']}
                structures[arm, variant, seed] = coords
                source_records.append(dict(arm=arm,variant=variant,seed=seed,
                    file=str(dest.relative_to(root)),sha256=digest(dest),residues=len(residues),
                    confidence_at_1002=float(residues[281]['CA'].bfactor)))
    jobs = []
    for model_i, model in enumerate(plan['models']):
        for arm_i, arm in enumerate(plan['structure_sources']):
            shard = 2*model_i+arm_i
            rows, fixed, records = [], {}, []
            for variant in plan['structure_variants']:
                positions = plan['positions'] if variant == 'WT' else [1002]
                for seed in plan['structure_seeds']:
                    for position in positions:
                        name = f'{variant}_s{seed}_p{position}'
                        row = dict(name=name,seq=seq,seq_chain_A=seq,num_of_chains=1,
                                   coords_chain_A=structures[arm,variant,seed])
                        rows.append(row)
                        fixed[name] = {'A':[p for p in range(1,325) if p != position-720]}
                        records.append(dict(name=name,variant=variant,structure_seed=seed,
                            position=position,reference=seq[position-721]))
            jsonl = root/'inputs'/f'mpnn-{shard}.jsonl'
            with jsonl.open('x') as f:
                for row in rows:f.write(json.dumps(row,allow_nan=False)+'\n')
            with (root/'inputs'/f'fixed-{shard}.json').open('x') as f:
                f.write(json.dumps(fixed,allow_nan=False)+'\n')
            jobs.append(dict(shard=shard,model=model,arm=arm,contexts=records,
                             jsonl_sha256=digest(jsonl)))
    save(root/'inputs/mpnn-jobs.json',jobs)
    expression = json.loads((PREP/'manifest.json').read_text())
    for item in expression['matrices']:
        require(digest(PREP/(item['arm']+'.npy')) == item['sha256'], 'Expression matrix drift')
        require(digest(PREP/(item['arm']+'-metadata.tsv.gz')) == item['metadata_sha256'], 'Metadata drift')
    source_hashes = {str(p):digest(p) for p in sorted(PREP.iterdir()) if p.is_file()}
    weights = {str(p.relative_to(root)):digest(p) for p in sorted((root/'ProteinMPNN').glob('*model_weights/*.pt'))}
    versions = {}
    for name in ['toolkit','ProteinMPNN']:
        versions[name] = subprocess.check_output(['git','-C',str(root/name),'rev-parse','HEAD'],text=True).strip()
        require(not subprocess.check_output(['git','-C',str(root/name),'status','--porcelain','--untracked-files=no'],text=True).strip(), 'Modified upstream source')
    require(versions['toolkit']==plan['toolkit_revision'] and versions['ProteinMPNN']==plan['upstream_revision'],'Revision mismatch')
    for name in ['README.md','STOCK.md','CHANGES.md','stock/PINS.json']:
        shutil.copyfile(root/'toolkit/proteinmpnn'/name,root/'inputs'/('toolkit-'+name.replace('/','-')))
    shutil.copyfile(PREP/'manifest.json',root/'inputs/expression-manifest.json')
    shutil.copyfile(PREP.parent.parent/'inputs/plan.json',root/'inputs/v25-plan.json')
    save(root/'outputs/input-provenance.json',dict(structures=source_records,
        source_sha256=source_hashes,weights_sha256=weights,revisions=versions,
        subject_inputs_transferred=False,new_provider=False,
        generated_sequence_use='Fixed-site computational probability sampling only; no binder or therapeutic sequence selected.'))
    (root/'outputs/prepare-complete.txt').write_text(datetime.now(timezone.utc).isoformat()+'\n')


def command(root, shard, mode='exact', pilot=False):
    plan=json.loads((root/'inputs/structural-plan.json').read_text())
    job=json.loads((root/'inputs/mpnn-jobs.json').read_text())[shard]
    suffix=f'pilot-{mode}' if pilot else f'mpnn-{shard}'
    return [str(root/'../bin/uv'), 'run','--no-sync','--project',str(root),'bash',str(root/'toolkit/proteinmpnn/run.sh'),
        'design','--config','h100','--mode',mode,'--variant',job['model']['variant'],
        '--model_name',job['model']['name'],'--jsonl_path',str(root/'inputs'/('pilot.jsonl' if pilot else f'mpnn-{shard}.jsonl')),
        '--fixed_positions_jsonl',str(root/'inputs'/f'fixed-{shard}.json'),
        '--out',str(root/'outputs'/suffix),'--seed',str(plan['inference_seed']),
        '--num_seq_per_target',str(16 if pilot else plan['samples_per_context']),
        '--batch_size',str(plan['batch_size']),'--sampling_temp','1.0','--save_probs','1','--save_score','1']


def run(root,shard,pilot=False):
    require(os.environ.get('CUDA_VISIBLE_DEVICES')==str(shard),'GPU mapping mismatch')
    if pilot:
        rows=(root/'inputs/mpnn-0.jsonl').read_text().splitlines()
        selected=[row for row in rows if json.loads(row)['name']=='WT_s11_p1002']
        require(len(selected)==1,'Pilot missing')
        (root/'inputs/pilot.jsonl').write_text(selected[0]+'\n')
        for mode in ['off','exact']:subprocess.run(command(root,0,mode,True),check=True)
        import numpy as np
        off=root/'outputs/pilot-off';exact=root/'outputs/pilot-exact'
        require((off/'seqs/WT_s11_p1002.fa').read_bytes()==(exact/'seqs/WT_s11_p1002.fa').read_bytes(),'Exact mode sequence mismatch')
        results={}
        for folder in ['probs','scores']:
            a=np.load(off/folder/'WT_s11_p1002.npz');b=np.load(exact/folder/'WT_s11_p1002.npz')
            require(set(a.files)==set(b.files),'Exact keys mismatch')
            for key in a.files:
                require(np.array_equal(a[key],b[key]),f'Exact array mismatch: {folder}/{key}')
                results[f'{folder}/{key}']=True
        save(root/'outputs/exact-stock-control.json',dict(passed=True,sequence_bytes_identical=True,
            arrays_identical=results,scope='One backbone/site/checkpoint/batch/seed; not a global equivalence proof.'))
        direct_control(root)
        return
    start=time.monotonic()
    save(root/'outputs'/f'mpnn-registration-{shard}.json',dict(shard=shard,
        created_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=digest(root/'inputs/structural-plan.json'),
        jobs_sha256=digest(root/'inputs/mpnn-jobs.json'),script_sha256=digest(__file__),command=command(root,shard)))
    subprocess.run(command(root,shard),check=True)
    save(root/'outputs'/f'mpnn-completion-{shard}.json',dict(shard=shard,complete=True,
        elapsed_seconds=time.monotonic()-start))


def direct_control(root):
    """Compare upstream sampling and direct conditional inference at identical orders."""
    import copy
    import sys
    import numpy as np
    import torch
    sys.path.insert(0,str(root/'ProteinMPNN'))
    from protein_mpnn_utils import ProteinMPNN, tied_featurize
    torch.backends.cuda.matmul.allow_tf32=False
    torch.manual_seed(291006)
    protein=json.loads((root/'inputs/pilot.jsonl').read_text())
    fixed=json.loads((root/'inputs/fixed-0.json').read_text())
    tensors=tied_featurize([copy.deepcopy(protein) for _ in range(16)],torch.device('cuda'),
        None,fixed,None,None,None,None,ca_only=False)
    X,S,mask,_,chain_M,encoding,_,_,_,_,chain_pos,_,residue_idx,*_=tensors
    weight=root/'ProteinMPNN/vanilla_model_weights/v_48_010.pt'
    checkpoint=torch.load(weight,map_location='cuda',weights_only=False)
    model=ProteinMPNN(num_letters=21,node_features=128,edge_features=128,hidden_dim=128,
        num_encoder_layers=3,num_decoder_layers=3,augment_eps=0.,k_neighbors=checkpoint['num_edges']).to('cuda').eval()
    model.load_state_dict(checkpoint['model_state_dict'])
    randn=torch.randn(chain_M.shape,device='cuda');randn[:,281]=1.0
    omit=np.array([0.]*20+[1.]);bias=np.zeros(21)
    with torch.no_grad():
        sample=model.sample(X,randn,S,chain_M,encoding,residue_idx,mask=mask,temperature=1.,
            omit_AAs_np=omit,bias_AAs_np=bias,chain_M_pos=chain_pos,bias_by_res=torch.zeros(16,324,21,device='cuda'))
        direct=model.conditional_probs(X,S,mask,chain_M*chain_pos,residue_idx,encoding,randn)
        expected=torch.softmax(direct[:,281,:20],dim=-1)
        error=float((sample['probs'][:,281,:20]-expected).abs().max().cpu())
        require(bool((sample['decoding_order'][:,-1]==281).all()),'Control target not last')
    require(error<=2e-5,'Sampling/conditional API disagreement')
    save(root/'outputs/direct-conditional-control.json',dict(passed=True,max_abs_probability_error=error,
        samples=16,position=1002,weight_sha256=digest(weight),target_forced_last_in_control=True,
        scope='Paired upstream algorithms at identical orders; production uses upstream random ordering.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','pilot','run']);p.add_argument('root',type=Path)
    p.add_argument('--shard',type=int,default=0);a=p.parse_args()
    if a.action=='prepare':prepare(a.root)
    else:run(a.root,a.shard,a.action=='pilot')
