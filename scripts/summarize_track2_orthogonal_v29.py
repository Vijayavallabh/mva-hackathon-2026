#!/usr/bin/env python3
"""Small public summaries derived from the complete v29 numerical records."""
import csv
import json
from pathlib import Path


def span(rows,key):
    return [min(r[key] for r in rows),max(r[key] for r in rows)] if rows else None


def summarize(structural,expression):
    protein=structural['comparisons']
    result=dict(version=29,structural=dict(
        primary_control_passes=sum(r['primary_controls_pass'] for r in protein),
        expanded_control_passes=sum(r['expanded_controls_pass'] for r in protein),
        comparisons=len(protein),candidate_WT_backbone_log_odds=span(protein,'candidate_log_odds'),
        candidate_mutant_backbone_log_odds=span(protein,'candidate_backbone_log_odds'),
        matched_NK_at_or_below=span(protein,'matched_NK_at_or_below'),matched_NK_count=17,
        candidate_alternate_rank=span(protein,'alternate_rank_most_compatible_first')),
        expression=[],drug=[],panel=[])
    for cell in ['HT29','MCF7']:
        for qc in ['all_profiles','crispr_quality_pass_only']:
            for rep in ['all978','residual_pc1','residual_pc3','residual_pc10']:
                fs=[f['representations'][rep] for r in expression['records'] if r['cell']==cell and r['space']=='prime' and r['quality']==qc for f in r['folds']]
                qs=[q for f in fs for q in f['queries'] if q['gene']=='BUB1B']
                base=dict(cell=cell,quality=qc,representation=rep,partitions=len(fs))
                result['expression'].append(base|dict(available=len(qs),missing=len(fs)-len(qs),
                    correlation=span(qs,'correlation'),rnai_rank=span(qs,'rnai_rank'),crispr_rank=span(qs,'crispr_rank'),
                    rnai_reference_genes=span(fs,'rnai_reference_genes'),crispr_reference_genes=span(fs,'crispr_reference_genes')))
                n=sum(f['heldout_shared_genes'] for f in fs)
                result['panel'].append(base|dict(repeated_heldout_gene_records=n,
                    **{k:sum(f[k] for f in fs)/n for k in ['heldout_rnai_top1','heldout_crispr_top1','heldout_rnai_top10','heldout_crispr_top10']}))
                if cell=='MCF7':
                    for gene in ['BUB1B','MTOR']:
                        ds=[d for f in fs for d in f['drugs'] if d['gene']==gene and d['dose']=='0.1']
                        result['drug'].append(base|dict(gene=gene,available=len(ds),
                            correlation=span(ds,'correlation'),reversal_rank=span(ds,'reversal_rank'),mimic_rank=span(ds,'mimic_rank'),
                            reference_genes=span(ds,'reference_genes')))
    return result


def compute(root):
    from track2_orthogonal_v29 import digest
    models=[];expressions=[]
    for gpu in range(8):
        log=root/'logs'/f'mpnn-{gpu}.log'
        timings=[json.loads(s) for s in log.read_text().splitlines() if s.startswith('{') and '"n_backbones"' in s]
        if len(timings)!=1:raise ValueError('Missing model timing')
        done=json.loads((root/'outputs'/f'mpnn-completion-{gpu}.json').read_text())
        models.append(done|dict(worker_timings=timings[0],log_sha256=digest(log)))
        expressions.append(json.loads((root/'outputs'/f'crossfit-{gpu}/completion.json').read_text()))
    monitors={}
    for name,file in [('model','gpu-monitor.csv'),('expression','crossfit-gpu-monitor.csv')]:
        rows=[{k.strip():v.strip() for k,v in r.items()} for r in csv.DictReader((root/'logs'/file).open())]
        stats=[]
        for gpu in range(8):
            rs=[r for r in rows if int(r['index'])==gpu]
            values=[float(r['utilization.gpu [%]'].split()[0]) for r in rs]
            stats.append(dict(gpu=gpu,samples=len(rs),peak_utilization_percent=max(values),
                mean_sampled_utilization_percent=sum(values)/len(values),
                nonzero_samples=sum(v>0 for v in values),
                peak_memory_MiB=max(float(r['memory.used [MiB]'].split()[0]) for r in rs)))
        monitors[name]=dict(file=file,sha256=digest(root/'logs'/file),by_gpu=stats,
            interpretation='One-second whole-launch samples; model monitor includes pilot and startup. Not continuous kernel instrumentation.')
    return dict(version=29,all_owned_jobs_complete=True,gpus=8,new_neural_inference=True,
        toolkit_executed=True,toolkit_revision='f4f62fa6592ae4938d49b1757bea0cfeff9f468e',
        model_workers=models,expression_workers=expressions,monitoring=monitors,
        scope='Worker and sampled-device measurements; no claim of uninterrupted eight-GPU saturation.',
        subject_data_transferred=False,new_hosted_model_provider=False)


if __name__=='__main__':
    import argparse
    from track2_orthogonal_v29 import save
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('analysis',type=Path);a=p.parse_args()
    s=json.loads((a.analysis/'track2-structural-results-v29.json').read_text())
    e=json.loads((a.analysis/'track2-crossfit-results-v29.json').read_text())
    save(a.analysis/'track2-orthogonal-summary-v29.json',summarize(s,e))
    save(a.analysis/'track2-orthogonal-compute-v29.json',compute(a.root))
