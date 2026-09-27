#!/usr/bin/env python3
"""Post-hoc finite-reference/dependence sensitivity; never replace fixed v23 tails."""
import argparse
import json
import math
from pathlib import Path
from track2_rnai_v23 import bh, save, digest


def analyze(path):
    data=json.loads(Path(path).read_text());rows=[]
    for row in data['rows']:
        for null in row['bub1b']['nulls']:
            count=null.get('at_or_above');n=null.get('draws')
            p=(count+1)/(n+1) if n is not None else 1.0
            rows.append(dict(cell=row['cell'],space=row['space'],arm=null['arm'],status=null['status'],
                positive_mean=row['bub1b']['mean_pair']>0,reference_sets=n,at_or_above=count,
                primary_tail=null.get('tail'),primary_BH_q=null['BH_q'],finite_reference_tail=p,
                primary_excess_coherence=null['excess_coherence_under_null']))
    factor=sum(1/i for i in range(1,len(rows)+1))
    for row,q in zip(rows,bh([r['finite_reference_tail'] for r in rows])):
        row['finite_reference_BH_q']=q
        row['finite_reference_BY_q']=min(1,q*factor)
        row['finite_reference_BH_excess']=row['status']=='complete' and row['positive_mean'] and q<=.05
    return dict(post_hoc=True,reason='Exact reference sets as small as four give zero observed tail counts. These are conditional controls, not exhaustive assignments of the observed BUB1B reagent identity. Tails and BH values are not calibrated probabilities/FDR. Apply add-one to every finite set and a dependence-conservative BY sensitivity; neither creates exchangeability.',
        primary_results_sha256=digest(path),family_size=len(rows),missing_as_one=True,rows=rows,
        primary_excess_count=sum(r['primary_excess_coherence'] for r in rows),
        finite_reference_BH_excess_count=sum(r['finite_reference_BH_excess'] for r in rows),
        finite_reference_BY_excess_count=sum(r['status']=='complete' and r['positive_mean'] and r['finite_reference_BY_q']<=.05 for r in rows),
        primary_replaced=False,drug_ranking_changed=False,biological_validation=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);p.add_argument('output',type=Path);a=p.parse_args();save(a.output,analyze(a.results))
