#!/usr/bin/env python3
"""Exhaustive public-reference BUBR1 masked scores; descriptive, not clinical labels."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import time

AA = 'ACDEFGHIKLMNPQRSTVWY'
OLD = Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(8 * 1024**2):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def jobs(plan, shard):
    require(type(shard) is int and 0 <= shard < 8, 'Invalid shard')
    return [(w, pos) for w in plan['windows']
            for pos in range(w['start'], w['end'] + 1)
            if (pos - w['start']) % 2 == shard % 2]


def worker(root, shard):
    import numpy as np
    import torch
    require(os.environ.get('CUDA_VISIBLE_DEVICES') == str(shard)
            and torch.cuda.device_count() == 1, 'Device assignment mismatch')
    require('H100' in torch.cuda.get_device_name(), 'Expected H100')
    plan = json.loads((root/'inputs/plan.json').read_text())
    item = plan['models'][shard // 2]
    repo = item['repository']
    label = repo.replace('/', '_')
    weights = OLD/'cache/models'/label
    manifest_path = OLD/'outputs'/(label+'-weights.json')
    manifest = json.loads(manifest_path.read_text())
    require(manifest['revision'] == item['revision'], 'Wrong model revision')
    for r in manifest['files']:
        require(digest(weights/r['name']) == r['sha256'], 'Changed model resource')
    fasta = root/'inputs/uniprot-O60566.fasta'
    require(digest(fasta) == plan['reference']['reference_fasta_sha256'], 'Changed reference')
    seq = ''.join(fasta.read_text().splitlines()[1:])
    require(len(seq) == 1050 and set(seq) <= set(AA), 'Invalid reference sequence')
    require(seq[1001] == 'N', 'Candidate reference mismatch')
    out = root/f'outputs/protein-{shard}'
    out.mkdir(exist_ok=False)
    torch.set_num_threads(4)
    torch.manual_seed(0)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    save(out/'registration.json', dict(created_utc=datetime.now(timezone.utc).isoformat(),
        plan_sha256=digest(root/'inputs/plan.json'), script_sha256=digest(__file__),
        model=repo, revision=item['revision'], weight_manifest_sha256=digest(manifest_path),
        reference_sha256=digest(fasta), environment_lock_sha256=digest(OLD/'envs/esm/uv.lock'),
        packages={p:importlib.metadata.version(p) for p in ['torch','esm','numpy','transformers']},
        cuda=torch.version.cuda, device=torch.cuda.get_device_name(),
        uuid=str(torch.cuda.get_device_properties(0).uuid), shard=shard,
        precision='float32; TF32 disabled; no autocast', batch_size=plan['batch_size']))
    started = time.monotonic()
    esm3 = repo == 'EvolutionaryScale/esm3-sm-open-v1'
    if esm3:
        import esm.pretrained
        import esm.utils.constants.esm3 as constants
        constants.data_root = lambda name: weights
        esm.pretrained.data_root = constants.data_root
        model = esm.pretrained.ESM3_sm_open_v0('cuda').float().eval()
        tokenizer = model.tokenizers.sequence
    else:
        from esm.models.esmc import EsmcForMaskedLM, EsmcTokenizer
        model = EsmcForMaskedLM.from_pretrained(weights, device='cuda', dtype=torch.float32,
                                               attn_implementation='sdpa').eval()
        tokenizer = EsmcTokenizer()
    aa_ids = [tokenizer.convert_tokens_to_ids(a) for a in AA]
    cache = {}
    gpu_seconds = 0.

    @torch.inference_mode()
    def predict(window, positions):
        nonlocal gpu_seconds
        key = window['name']
        if key not in cache:
            enc = tokenizer(seq[window['start']-1:window['end']], return_tensors='pt')
            cache[key] = (enc['input_ids'].cuda(), enc['attention_mask'].cuda())
        base, mask = cache[key]
        tokens = base.repeat(len(positions), 1)
        indices = torch.tensor([p-window['start']+1 for p in positions], device='cuda')
        rows = torch.arange(len(positions), device='cuda')
        for i, p in enumerate(positions):
            require(tokens[i, indices[i]].item() == tokenizer.convert_tokens_to_ids(seq[p-1]),
                    'Token coordinate mismatch')
        tokens[rows, indices] = tokenizer.mask_token_id
        before, after = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
        before.record()
        logits = (model(sequence_tokens=tokens).sequence_logits if esm3 else
                  model(input_ids=tokens, attention_mask=mask.repeat(len(positions), 1)).logits)
        values = torch.log_softmax(logits[rows, indices].float(), -1)[:, aa_ids]
        after.record(); torch.cuda.synchronize()
        gpu_seconds += before.elapsed_time(after)/1000
        require(torch.isfinite(values).all().item(), 'Nonfinite distribution')
        return values.cpu().numpy()

    # Verify batching against the original single-sequence scoring semantics.
    validations = []
    for w in plan['windows']:
        positions = [793, 795, 882, 911, 1002]
        batch = predict(w, positions)
        error = max(float(np.max(np.abs(batch[i]-predict(w, [p])[0]))) for i,p in enumerate(positions))
        require(error <= plan['numerical_tolerance'], 'Batch/single mismatch')
        repeat = float(np.max(np.abs(batch-predict(w, positions))))
        require(repeat <= plan['numerical_tolerance'], 'Repeat mismatch')
        validations.append(dict(window=w['name'], batch_single_max_abs_error=error,
                                repeat_max_abs_error=repeat))
    save(out/'numerical-validation.json', validations)
    count = 0
    with (out/'masked-log-probabilities.csv').open('x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['model','window','position','reference',*AA])
        for w in plan['windows']:
            positions = [p for ww,p in jobs(plan, shard) if ww['name'] == w['name']]
            for start in range(0, len(positions), plan['batch_size']):
                selected = positions[start:start+plan['batch_size']]
                values = predict(w, selected)
                for p,v in zip(selected,values):
                    writer.writerow([repo,w['name'],p,seq[p-1],*map(float,v)])
                count += len(selected)
                f.flush()
                if start % 128 == 0:
                    print(json.dumps(dict(shard=shard,window=w['name'],positions_complete=count,
                                          seconds=time.monotonic()-started)), flush=True)
    require(count == len(jobs(plan,shard)), 'Incomplete scan')
    save(out/'summary.json', dict(model=repo,shard=shard,masked_positions=count,
        substitution_scores=count*19,elapsed_seconds=time.monotonic()-started,
        cuda_forward_seconds=gpu_seconds,peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
        output_sha256=digest(out/'masked-log-probabilities.csv'),clinical_classification=False,
        phase_resolved=False,drug_ranking_changed=False,wet_lab_performed=False))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root',type=Path); p.add_argument('--shard',type=int,required=True)
    a=p.parse_args(); worker(a.root,a.shard)
