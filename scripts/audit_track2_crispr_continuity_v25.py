#!/usr/bin/env python3
"""Resolve renamed/reaggregated low-dose profiles by source wells, not sig IDs."""
import argparse
import json
from pathlib import Path
import pandas as pd
from track2_crispr_v25 import save, digest


def run(root):
    newfile=root/'outputs/prepared/everolimus-metadata.tsv'
    oldfile=Path('/home/prachh/v/mva-track2-transcriptome-20260927/outputs/phase2-prepared/signatures.tsv.gz')
    new=pd.read_csv(newfile,sep='\t',dtype=str,keep_default_na=False)
    old=pd.read_csv(oldfile,sep='\t',dtype=str,keep_default_na=False)
    wells={}
    for i,s in enumerate(old.distil_id):
        for well in s.split('|'):wells.setdefault(well,[]).append(i)
    rows=[]
    selected=new[new.pert_id.eq('BRD-K13514097')&pd.to_numeric(new.pert_dose).eq(.1)]
    for r in selected.itertuples():
        ids=set(r.distil_ids.split('|'))
        matched=sorted({i for well in ids for i in wells.get(well,[])})
        oldrows=[];oldw=set()
        for i in matched:
            o=old.iloc[i];oldw.update(o.distil_id.split('|'))
            oldrows.append(dict(signature_id=o.sig_id,compound_id=o.pert_id,
                                nsample=o.distil_nsample,cc_q75=o.distil_cc_q75,tas=o.tas,
                                shared_wells=len(ids&set(o.distil_id.split('|')))))
        rows.append(dict(signature_id=r.sig_id,cell=r.cell_iname,nominal_dose_uM=.1,
             quality_pass=r.quality_pass=='True',new_wells=len(ids),previous_profiles=oldrows,
             shared_wells=len(ids&oldw),added_wells=len(ids-oldw),exact_signature_match=bool(old.sig_id.eq(r.sig_id).any()),
             new_nsample=int(r.nsample),new_cc_q75=float(r.cc_q75),new_tas=float(r.tas),new_qc_pass=int(r.qc_pass)))
    out=dict(version=25,source='Public LINCS2020 vs frozen GSE70138',
       new_metadata_sha256=digest(newfile),old_metadata_sha256=digest(oldfile),
       comparison='All source wells audited, including changed signature identifiers',rows=rows,
       regrouped_profiles=sum(bool(r['shared_wells']) for r in rows),
       exact_signature_matches=sum(r['exact_signature_match'] for r in rows),
       interpretation='Different signature IDs can represent the same experimental wells. Improved aggregation/QC is retained; neither old failed QC nor new passing QC is overwritten or counted as independent replication.',
       scope='This audits regrouping against GSE70138. Preparation separately audits reuse against GSE92742. Neither covers all historical Broad experiments.')
    save(root/'outputs/continuity-final.json',out)
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);run(p.parse_args().root)
