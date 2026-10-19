#!/usr/bin/env python3
"""Recompute public mitotic metrics from the retained review archive, locally."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import numpy as np
from track2_optical_audit_v35 import paired_gain


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path)
    p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise ValueError('Preserve prior replay')
    m=json.loads(a.manifest.read_text());raw=a.archive.read_bytes()
    if len(raw)!=m['bytes'] or hashlib.sha256(raw).hexdigest()!=m['sha256']:
        raise ValueError('Archive digest mismatch')
    with tarfile.open(a.archive) as t:
        members=t.getmembers()
        if len(members)!=m['files'] or any(not x.isfile() or Path(x.name).is_absolute() or '..' in Path(x.name).parts for x in members):
            raise ValueError('Unsafe or incomplete archive')
        def read(name):return json.load(t.extractfile(name))
        summary=read('outputs/audit-v35-mitotic.json');results=[]
        for label in ['real','shuffled']:
            for seed in [3301,3302,3303,3304]:
                r=read(f'models-v35/mitotic-{seed}-{label}/results.json')
                for obj in list(r['baseline_results'].values())+[r['learned']]:
                    grouped={}
                    for row in obj['rows']:
                        grouped.setdefault(row['gene'],[]).append(1/row['rank'])
                    recalculated={g:float(np.mean(v)) for g,v in grouped.items()}
                    if set(recalculated)!=set(obj['by_gene_mrr']):raise ValueError('Gene set changed')
                    np.testing.assert_allclose([recalculated[g] for g in sorted(recalculated)],
                                               [obj['by_gene_mrr'][g] for g in sorted(recalculated)],rtol=0,atol=1e-12)
                    np.testing.assert_allclose(np.mean(list(recalculated.values())),obj['macro_mrr'],rtol=0,atol=1e-12)
                results.append(r)
        genes=sorted(results[0]['learned']['by_gene_mrr'])
        baselines=[[obj['by_gene_mrr'][g] for g in genes] for _,obj in sorted(results[0]['baseline_results'].items())]
        real=[[r['learned']['by_gene_mrr'][g] for g in genes] for r in results[:4]]
        negative=[[r['learned']['by_gene_mrr'][g] for g in genes] for r in results[4:]]
        for values,key in [(real,'real_gain'),(negative,'shuffled_gain')]:
            replay=paired_gain(baselines,values)
            for field in ['point_difference','paired_95_percent_intervals','joint_minimum_seed_95_percent_interval']:
                np.testing.assert_allclose(replay[field],summary[key][field],rtol=0,atol=1e-12)
            if replay['practical_gain_gate_passed']!=summary[key]['practical_gain_gate_passed']:
                raise ValueError('Gain gate differs')
    result=dict(passed=True,archive_sha256=m['sha256'],files=m['files'],models=8,
        held_out_genes=len(genes),baseline_methods=len(baselines),bootstrap_repetitions=20000,
        rank_to_gene_and_macro_metrics_recomputed=True,paired_intervals_recomputed=True,
        tolerance=1e-12,practical_gain_gate_passed=summary['real_gain']['practical_gain_gate_passed'],biological_validation=False,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
