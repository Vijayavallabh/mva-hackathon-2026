#!/usr/bin/env python3
"""Derive complete, versioned summaries without promoting expression to efficacy."""
import argparse
import json
from pathlib import Path
import pandas as pd
from track2_crispr_v25 import save, digest


def summarize(root):
    out=root/'outputs';prep=out/'prepared'
    result=json.loads((out/'results.json').read_text())
    cross=pd.read_csv(out/'cross-batch.tsv.gz',sep='\t')
    orth=pd.read_csv(out/'orthogonal.tsv.gz',sep='\t')
    named=pd.read_csv(out/'named-drugs.tsv.gz',sep='\t')
    meta=pd.read_csv(prep/'everolimus-metadata.tsv',sep='\t')
    xm=pd.read_csv(prep/'xpr-metadata.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    labels=pd.read_csv(prep/'everolimus-identity.tsv',sep='\t',dtype=str)
    reference='BRD-K13514097'
    assert labels[labels.pert_id.eq(reference)].inchi_key.tolist()==['HKVAMNSJSFKALM-GKUWKFKPSA-N']
    def records(df):return json.loads(df.to_json(orient='records',double_precision=15))
    def drug_stats(df):
        return dict(n=len(df),positive=int(df.correlation.gt(0).sum()),negative=int(df.correlation.lt(0).sum()),
             median=float(df.correlation.median()) if len(df) else None,
             min=float(df.correlation.min()) if len(df) else None,max=float(df.correlation.max()) if len(df) else None,
             sign_changes_without_target=int((df.correlation*df.exclude_BUB1B_correlation<0).sum()),
             sign_changes_common_response=int((df.correlation*df.common_response_removed_correlation<0).sum()))
    ev=named[named.compound.str.lower().eq('everolimus')]
    strata=[]
    for keys,group in ev.groupby(['gene','compound_id'],sort=True):
        for mode,part in [('all',group),('drug_qc_pass',group[group.quality_pass])]:
            strata.append(dict(gene=keys[0],compound_id=keys[1],filter=mode,**drug_stats(part)))
    orth_summary=[]
    for (space,features),group in orth.groupby(['space','features']):
        orth_summary.append(dict(space=space,features=features,n=len(group),
            rnai_top1=int(group.rnai_rank.eq(1).sum()),
            rnai_top5percent=int((group.rnai_rank/group.rnai_candidates<=.05).sum()),
            crispr_top1=int(group.crispr_rank.eq(1).sum()),
            crispr_top5percent=int((group.crispr_rank/group.crispr_candidates<=.05).sum())))
    by_dose=meta.groupby(['pert_id','pert_dose','pert_dose_unit']).agg(profiles=('sig_id','size'),quality_passes=('quality_pass','sum')).reset_index()
    # Investigate changed 0.1-uM QC in the newer aggregation; preserve each old result.
    old=pd.read_csv('/home/prachh/v/mva-track2-transcriptome-20260927/outputs/phase2-prepared/signatures.tsv.gz',sep='\t',dtype=str,keep_default_na=False)
    newer=meta[meta.pert_id.eq(reference)&meta.pert_dose.eq(.1)]
    continuity=[]
    for row in newer.itertuples():
        neww=set(row.distil_ids.split('|'))
        matches=old[old.sig_id.eq(row.sig_id)]
        for previous in matches.to_dict('records'):
            oldw=set(previous.get('distil_id','').split('|'))-{''}
            continuity.append(dict(signature_id=row.sig_id,
                 old_metrics={k:previous.get(k) for k in ['distil_nsample','distil_cc_q75','tas']},
                 new_metrics=dict(nsample=int(row.nsample),cc_q75=float(row.cc_q75),tas=float(row.tas),qc_pass=int(row.qc_pass)),
                 new_quality_pass=bool(row.quality_pass),old_wells=len(oldw),new_wells=len(neww),
                 shared_wells=len(oldw&neww),added_wells=len(neww-oldw),removed_wells=len(oldw-neww),same_well_set=oldw==neww))
    resource=json.loads((out/'resources.json').read_text())
    monitor=pd.read_csv(root/'logs/gpu-monitor.csv',skipinitialspace=True)
    monitor.columns=monitor.columns.str.strip()
    utilization=[]
    for index,group in monitor.groupby('index'):
        col=next(c for c in group if c.startswith('utilization.gpu'))
        mem=next(c for c in group if c.startswith('memory.used'))
        u=pd.to_numeric(group[col].astype(str).str.replace(' %','',regex=False).str.strip())
        m=pd.to_numeric(group[mem].astype(str).str.replace(' MiB','',regex=False).str.strip())
        utilization.append(dict(index=int(index),samples=len(group),max_gpu_percent=int(u.max()),mean_sampled_gpu_percent=float(u.mean()),
                                nonzero_samples=int(u.gt(0).sum()),max_memory_mib=int(m.max())))
    b=cross[cross.gene.eq('BUB1B')]
    borth=orth[orth.gene.eq('BUB1B')]
    target=ev[ev.gene.eq('BUB1B')&ev.compound_id.eq(reference)]
    low=target[target.quality_pass&target.dose.le(.1)]
    output=dict(version=25,plan_sha256=result['plan_sha256'],complete=True,
         source_profiles=dict(compound=720216,crispr_matrix=142901,crispr_treatments=140945),
         crispr_types=xm.pert_type.value_counts().to_dict(),bub1b=dict(profiles=31,cells=19,guides=1,guide_id='BRDN0001148077',
               cross_batch_queries=len(b),cross_batch_top1=int(b.top_one.sum()),cross_batch_top5percent=int(b.top_five_percent.sum()),
               cross_batch_positive=int(b.correlation.gt(0).sum()),cross_batch_records=records(b),
               orthogonal_records=records(borth),independent_guide_qualified_contexts=0),
         genome_benchmark=dict(cross_batch_queries=len(cross),cross_batch_top1=int(cross.top_one.sum()),
                               cross_batch_top5percent=int(cross.top_five_percent.sum()),orthogonal=orth_summary),
         comparisons=result['comparisons'],total_comparisons=sum(result['comparisons'].values()),
         matched_compound_profiles=sum(c['compound_profiles'] for r in result['gpu_runs'] for c in r['cells']),
         everolimus=dict(labelled_profiles=len(meta),reference_matching_profiles=int(meta.pert_id.eq(reference).sum()),
             reference_matching_quality_passes=int(meta[meta.pert_id.eq(reference)].quality_pass.sum()),
             unresolved_identity_profiles=int(meta.pert_id.ne(reference).sum()),by_id_dose=records(by_dose),
             identity=records(labels[['pert_id','inchi_key']]),strata=strata,
             matched_reference_bub1b=drug_stats(target),matched_reference_bub1b_quality=drug_stats(target[target.quality_pass]),
             matched_reference_bub1b_low_dose_quality=drug_stats(low),low_dose_records=records(low),
             reaggregation_01uM=continuity),
         resources=dict(gpus=8,utilization=utilization),
         worker_seconds=[r['wall_seconds'] for r in result['gpu_runs']],
         timed_gpu_product_seconds=[r['timed_gpu_product_seconds'] for r in result['gpu_runs']],
         peak_allocated_bytes=[r['peak_allocated_bytes'] for r in result['gpu_runs']],
         public_table_hashes=result['tables'],drug_ranking_changed=False,clinical_exposure_margin=None,
         biological_validation=False,new_neural_inference=False,wet_lab_performed=False)
    save(out/'summary.json',output)
    ev[ev.gene.isin(['BUB1B','MTOR','RPTOR'])].to_csv(out/'everolimus-panel.tsv',sep='\t',index=False)
    print(json.dumps({k:output[k] for k in ['total_comparisons','matched_compound_profiles','worker_seconds','timed_gpu_product_seconds']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);summarize(p.parse_args().root)
