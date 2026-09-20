#!/usr/bin/env python3
"""Pinned local ESMC/ESM3 control scoring and ESM3/ESMFold2 structure comparisons."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import math
import os
from pathlib import Path
import time
from track2_esm_pilot import digest, write_json, parse_variant, control_gate

ROOT = Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def setup(repo, label):
    import torch
    if torch.cuda.device_count()!=1 or os.environ.get('CUDA_VISIBLE_DEVICES') not in ['2','3','6','7']:
        raise ValueError('Expose exactly one explicitly selected available GPU')
    plan_path = ROOT / 'inputs/latest-plan.json'
    plan = json.loads(plan_path.read_text())
    item = next(x for x in plan['models'] if x['repository'] == repo)
    weight_root = ROOT / 'cache/models' / repo.replace('/', '_')
    manifest = json.loads((ROOT / 'outputs' / (repo.replace('/', '_') + '-weights.json')).read_text())
    if manifest['revision'] != item['revision']:
        raise ValueError('Checkpoint revision differs from fixed plan')
    for row in manifest['files']:
        if digest(weight_root / row['name']) != row['sha256']:
            raise ValueError('Checkpoint/resource integrity mismatch')
    fasta = ROOT / 'inputs/uniprot-O60566.fasta'
    if digest(fasta) != plan['protein_reference']['reference_fasta_sha256']:
        raise ValueError('Reference integrity mismatch')
    sequence = ''.join(fasta.read_text().splitlines()[1:])
    if len(sequence) != 1050:
        raise ValueError('Reference length mismatch')
    out = ROOT / 'outputs' / label
    out.mkdir(exist_ok=False)
    torch.set_num_threads(4)
    torch.manual_seed(0)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    registration = dict(created_utc=datetime.now(timezone.utc).isoformat(), repository=repo,
        revision=item['revision'], plan_sha256=digest(plan_path), script_sha256=digest(__file__),
        checkpoint_manifest_sha256=digest(ROOT/'outputs'/(repo.replace('/', '_')+'-weights.json')),
        reference_sha256=digest(fasta), lock_sha256=digest(ROOT/'envs/esm/uv.lock'),
        packages={p:importlib.metadata.version(p) for p in ['esm','torch','numpy','transformers']},
        cuda=torch.version.cuda, cudnn=torch.backends.cudnn.version(),
        devices=os.environ.get('CUDA_VISIBLE_DEVICES'), source_revision=plan['source_revisions']['Biohub/esm'])
    write_json(out/'preregistration.json', registration)
    return plan, sequence, weight_root, out


def load_esm3(weight_root):
    # Bind both official resource-resolver references to the checked local snapshot.
    # This changes only resource location, not model code, weights or inference.
    import esm.pretrained
    import esm.utils.constants.esm3 as constants
    constants.data_root = lambda name: weight_root
    esm.pretrained.data_root = constants.data_root
    return esm.pretrained.ESM3_sm_open_v0('cuda').float().eval()


def score(repo, label):
    import torch
    plan, sequence, weights, out = setup(repo, label)
    started = time.monotonic()
    esm3 = repo == 'EvolutionaryScale/esm3-sm-open-v1'
    if esm3:
        model = load_esm3(weights)
        tokenizer = model.tokenizers.sequence
    else:
        from esm.models.esmc import EsmcForMaskedLM, EsmcTokenizer
        model = EsmcForMaskedLM.from_pretrained(weights, device='cuda', dtype=torch.float32,
                                                attn_implementation='sdpa').eval()
        tokenizer = EsmcTokenizer()
    variants = plan['protein_controls'] + [dict(variant=plan['protein_candidate'], group='candidate')]
    cache = {}

    @torch.inference_mode()
    def distribution(window, pos, repeat=False):
        start, end = window['start'], window['end']
        index = pos-start+1
        key = (start,end,pos)
        if key not in cache or repeat:
            inputs = tokenizer(sequence[start-1:end], return_tensors='pt')
            tokens = inputs['input_ids'].cuda()
            if tokens.shape[1] != end-start+3 or tokens[0,index].item() != tokenizer.convert_tokens_to_ids(sequence[pos-1]):
                raise ValueError('Token/reference coordinate mismatch')
            tokens[0,index] = tokenizer.mask_token_id
            logits = (model(sequence_tokens=tokens).sequence_logits if esm3
                      else model(input_ids=tokens, attention_mask=inputs['attention_mask'].cuda()).logits)
            values = torch.log_softmax(logits[0,index].float(), -1).cpu()
            if not torch.isfinite(values).all():
                raise ValueError('Nonfinite masked distribution')
            if repeat:
                return values
            cache[key] = values
        return cache[key]

    rows = []
    for window in plan['protein_windows']:
        for row in variants:
            ref,pos,alt = parse_variant(row['variant'],sequence)
            values = distribution(window,pos)
            rows.append(dict(window=window['name'],variant=row['variant'],group=row['group'],
                score=float(values[tokenizer.convert_tokens_to_ids(alt)]-values[tokenizer.convert_tokens_to_ids(ref)])))
    repeat = float((distribution(plan['protein_windows'][0],882,True)-distribution(plan['protein_windows'][0],882)).abs().max())
    gate = control_gate([r for r in rows if r['group'] != 'candidate'])
    gate.update(repeat_max_abs_difference=repeat,numerical_pass=math.isfinite(repeat) and repeat<=1e-6)
    gate['pass'] = gate['pass'] and gate['numerical_pass']
    write_json(out/'summary.json',dict(model=repo,rows=rows,gate=gate,elapsed_seconds=time.monotonic()-started,
        peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,precision='float32; TF32 disabled; no autocast',
        clinical_classification=False,drug_ranking_changed=False,phase_resolved=False))
    print(json.dumps(dict(model=repo,gate=gate)),flush=True)


def fold(repo,label,arm):
    import torch
    plan,sequence,weights,out = setup(repo,label)
    started = time.monotonic()
    esm3 = repo == 'EvolutionaryScale/esm3-sm-open-v1'
    if esm3:
        from esm.sdk.api import ESMProtein, GenerationConfig
        model = load_esm3(weights)
    else:
        from esm.models.esmfold2 import EsmFold2Model, ESMFold2InputBuilder, ProteinInput, StructurePredictionInput
        from esm.utils.msa import MSA
        model = EsmFold2Model.from_pretrained(weights,device='cuda').eval()
        model.set_kernel_backend(None)
        builder = ESMFold2InputBuilder(ccd_cache=weights)
    records=[]
    for variant in plan['structures']['variants']:
        seq=sequence
        if variant!='WT':
            ref,pos,alt=parse_variant(variant,sequence)
            seq=sequence[:pos-1]+alt+sequence[pos:]
        seq=seq[720:1044]
        for seed in plan['structures']['seeds']:
            torch.manual_seed(seed);torch.cuda.manual_seed_all(seed)
            name=f'{variant}-seed{seed}'
            if esm3:
                result=model.generate(ESMProtein(sequence=seq),GenerationConfig(track='structure',num_steps=64,temperature=0.0))
                if not isinstance(result,ESMProtein) or result.sequence!=seq or result.coordinates is None:
                    raise ValueError(f'ESM3 returned no valid structure: {result}')
                path=out/(name+'.pdb');result.to_pdb(str(path))
                confidence=result.plddt
                record=dict(variant=variant,seed=seed,mean_plddt=float(confidence.float().mean()) if confidence is not None else None,
                    ptm=float(result.ptm) if result.ptm is not None else None)
            else:
                msa = MSA.from_a3m(ROOT/f'inputs/msa/{variant}.a3m',remove_insertions=True) if arm=='shared_msa' else None
                inp=StructurePredictionInput(sequences=[ProteinInput(id='A',sequence=seq,msa=msa)])
                result=builder.fold(model,inp,num_loops=20,num_sampling_steps=100,num_diffusion_samples=1,seed=seed)
                path=out/(name+'.cif');path.write_text(result.complex.to_mmcif())
                record=dict(variant=variant,seed=seed,mean_plddt=float(result.plddt.mean()),ptm=float(result.ptm),iptm=float(result.iptm))
            record.update(path=path.name,sha256=digest(path))
            write_json(out/(name+'.json'),record);records.append(record)
            print(json.dumps(record),flush=True)
    write_json(out/'summary.json',dict(model=repo,arm=arm,records=records,elapsed_seconds=time.monotonic()-started,
        peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
        precision='ESM3 SDK generation uses BF16 autocast; ESMFold2 uses its upstream folding precision/default sampler; no opt-in fused kernels',
        clinical_classification=False,drug_ranking_changed=False,phase_resolved=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['score','fold']);p.add_argument('repo');p.add_argument('label');p.add_argument('--arm',choices=['single_sequence','shared_msa'],default='single_sequence')
    a=p.parse_args()
    if a.command=='score':score(a.repo,a.label)
    else:fold(a.repo,a.label,a.arm)
