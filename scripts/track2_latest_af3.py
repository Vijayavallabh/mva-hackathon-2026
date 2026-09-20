#!/usr/bin/env python3
"""Prepare public-domain AlphaFold3 inputs and retrieve Google-origin parameters."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
from track2_esm_pilot import digest, write_json, parse_variant

ROOT=Path('/home/prachh/v/mva-track2-expanded-latest-20260921')


def prepare():
    plan=json.loads((ROOT/'inputs/latest-plan.json').read_text())
    fasta=ROOT/'inputs/uniprot-O60566.fasta'
    if digest(fasta)!=plan['protein_reference']['reference_fasta_sha256']:
        raise ValueError('Reference hash mismatch')
    sequence=''.join(fasta.read_text().splitlines()[1:])
    dest=ROOT/'inputs/af3';dest.mkdir(exist_ok=False)
    paths={}
    for variant in plan['structures']['variants']:
        seq=sequence
        if variant!='WT':
            ref,pos,alt=parse_variant(variant,sequence)
            seq=sequence[:pos-1]+alt+sequence[pos:]
        seq=seq[720:1044]
        msa=(ROOT/f'inputs/msa/{variant}.a3m').read_text()
        if msa.splitlines()[1]!=seq or sum(line.startswith('>') for line in msa.splitlines())!=623:
            raise ValueError('Shared MSA query/count mismatch')
        data=dict(name=variant,modelSeeds=plan['structures']['seeds'],dialect='alphafold3',version=3,
            sequences=[dict(protein=dict(id='A',sequence=seq,unpairedMsa=msa,pairedMsa='',templates=[]))])
        path=dest/(variant+'.json');write_json(path,data);paths[path.name]=digest(path)
    write_json(ROOT/'outputs/af3-input-provenance.json',dict(files=paths,
        plan_sha256=digest(ROOT/'inputs/latest-plan.json'),script_sha256=digest(__file__),
        msa_origin='Previously retrieved public WT ColabFold alignment; only query row changed for registered substitutions'))


def weights():
    import zstandard
    url='https://storage.googleapis.com/alphafold3/af3.bin.zst'
    dest=ROOT/'cache/alphafold3';dest.mkdir(exist_ok=True)
    path=dest/'af3.bin.zst'
    with urllib.request.urlopen(url,timeout=120) as response,path.open('xb') as out:
        size=int(response.headers['Content-Length'])
        if not 100_000_000<size<5_000_000_000:
            raise ValueError('Unexpected parameter size')
        md5=hashlib.md5();received=0;headers=dict(response.headers)
        while block:=response.read(8*1024*1024):
            received+=len(block)
            if received>size:raise ValueError('Oversized parameter stream')
            md5.update(block);out.write(block)
    expected=headers.get('x-goog-hash',headers.get('X-Goog-Hash',''))
    if received!=size or ('md5=' in expected and base64.b64encode(md5.digest()).decode()!=expected.split('md5=')[1].split(',')[0]):
        raise ValueError('Google transport size/hash mismatch')
    decoded=dest/'af3.bin'
    with path.open('rb') as source,decoded.open('xb') as out:
        zstandard.ZstdDecompressor().copy_stream(source,out)
    write_json(ROOT/'outputs/af3-weights.json',dict(url=url,created_utc=datetime.now(timezone.utc).isoformat(),
        compressed=dict(bytes=size,sha256=digest(path),google_hash_header=expected),
        decoded=dict(bytes=decoded.stat().st_size,sha256=digest(decoded)),
        terms='Noncommercial academic theoretical research; no clinical decision or model training. Weights not redistributed. Outputs subject to AlphaFold3 Output Terms.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prepare','weights']);a=p.parse_args()
    {'prepare':prepare,'weights':weights}[a.command]()
