#!/usr/bin/env python3
"""Standard-library check of complete v31 research; consistency is not biology."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT='notes/track2-perturbseq-audit-v31.json'


def require(condition,message):
    if not condition:raise ValueError(message)


def validate_results(j):
    require(j['version']==31 and j['complete'] is True,'Incomplete/wrong version')
    for flag in ['drug_ranking_changed','biological_validation','phase_confirmed',
                 'conditional_ranges_are_biological_confidence_intervals','neural_model_inference']:
        require(j[flag] is False,'Unsupported promotion: '+flag)
    require(j['clinical_exposure_margin'] is None,'Unsupported exposure margin')
    require('unavailable' in j['all_controls_sensitivity'] and 'identical' in j['all_controls_sensitivity'],
            'Missing selected-control limitation')
    cells=['rpe1','K562_essential'];queries=['BUB1B','BUB1','MAD2L1','CDC20','TTK','AURKB','PLK1','MTOR','RPTOR','RICTOR']
    reps=['all_features','no_queries','no_queries_or_cycle']
    require(j['feature_counts']==dict(all_features=4861,no_queries=4852,no_queries_or_cycle=4773),'Feature mask drift')
    expected_missing={'rpe1':['CDC20','AURKB','RICTOR'],'K562_essential':['RICTOR']}
    require(j['missing_queries']==expected_missing,'Missing query represented incorrectly')
    seen=set();reference={};expected_gpu=0
    for r in j['split_results']:
        key=(r['cell'],r['gene'],r['representation'])
        require(key not in seen,'Duplicate query result');seen.add(key)
        require(len(r['reference_constructs'])==1 and type(r['reference_constructs'][0]) is int,'Reference denominator')
        reference[r['cell']]=r['reference_constructs'][0]
        for role in ['correlation','forward_rank','reverse_rank']:
            s=r[role];require(s['n']==1024 and type(s['n']) is int,'Wrong resampling count')
            values=[s[k] for k in ['minimum','q025','median','q975','maximum']]
            require(all(math.isfinite(v) for v in values) and sorted(values)==values,'Invalid resampling range')
            if role=='correlation':require(-1<=values[0]<=values[-1]<=1,'Invalid correlation')
            else:require(1<=values[0]<=values[-1]<=reference[r['cell']],'Rank outside denominator')
        for direction in ['forward','reverse']:
            a,b=r[direction+'_top1'],r[direction+'_top10']
            require(type(a) is int and type(b) is int and 0<=a<=b<=1024,'Invalid retrieval counts')
    wanted={(c,q,r) for c in cells for q in queries if q not in expected_missing[c] for r in reps}
    require(seen==wanted,'Incomplete prespecified query/feature matrix')
    for cell,ncells,nbub,ncontrols in [('rpe1',247914,106,11485),('K562_essential',310385,141,10691)]:
        meta=j['query_metadata'][cell]
        require(meta['cells']==ncells and meta['core_control_cells']==meta['all_control_cells']==ncontrols,'Control/cell coverage drift')
        q={r['gene']:r for r in meta['query_metadata']};require(set(q)==set(queries),'Query metadata missing')
        require(q['BUB1B']['cells']==nbub and len(q['BUB1B']['constructs'])==len(q['BUB1B']['guide_pairs'])==1,'False guide replication')
        require(q['RICTOR']['cells']==0,'Absent query treated as measurement')
        if cell=='rpe1':require(q['RPTOR']['measured_gene_ids']==[] and q['CDC20']['cells']==15 and q['AURKB']['cells']==5,'Missing versus low coverage drift')
        for r in q.values():
            if 'cp10k_ratio' in r and r['cp10k_ratio'] is not None:
                require(abs(r['mean_target_cp10k']/r['matched_control_cp10k']-r['cp10k_ratio'])<1e-12,'Target ratio arithmetic')
        partitions=sum(r['partitions'] for r in j['partition_sensitivity'] if r['cell']==cell)
        expected_gpu+=4*(3*reference[cell]**2*257+reference[cell]*partitions)
    pair_a=j['query_metadata']['rpe1']['query_metadata'][0]['guide_pairs']
    pair_b=j['query_metadata']['K562_essential']['query_metadata'][0]['guide_pairs']
    require(pair_a==pair_b,'Shared guide identity changed')
    comp=j['compute']
    require(comp['gpus']==8 and comp['workers']==8 and comp['split_repetitions']==2048,'Compute coverage mismatch')
    require(comp['gpu_correlations']==expected_gpu and expected_gpu==27628823832,'Correlations do not follow declared workload')
    require(comp['cpu_cross_cell_correlations']==3*reference['rpe1']*reference['K562_essential'],'Cross-cell count mismatch')
    require(comp['max_dot_product_cpu_error']<=2e-5,'Numerical check failed')
    for row in j['null_results']:
        require(row['null_norm']['n']==1024 and abs(row['descriptive_tail']-(1+row['greater_equal'])/1025)<1e-15,'Finite null arithmetic')
    require(all(r['reference_includes_retained_cells'] is True for r in j['partition_sensitivity']),
            'Partition influence mislabeled held-out validation')
    require(len(j['cross_cell_queries'])==21,'Cross-cell query coverage')
    for r in j['cross_cell_queries']:
        require(r['k562_denominator']==2077 and r['rpe1_denominator']==2154,'Cross-cell denominator drift')
        require(1<=r['k562_rank']<=2077 and 1<=r['rpe1_rank']<=2154,'Invalid cross-cell rank')
    return dict(passed=True,version=31,gpus=8,gpu_correlations=expected_gpu,split_repetitions=2048,
                public_cells=558299,drug_ranking_changed=False,biological_validation=False)


def check(root=ROOT):
    audit=json.loads((root/AUDIT).read_text())
    require(audit['version']==31 and audit['archive_verification']['passed'],'Archive not verified')
    replay=audit['reanalysis']
    require(replay['passed'] and replay['numeric_fields']==2705 and
            replay['max_absolute_difference']<=2e-5,'Local reanalysis incomplete')
    require(len(replay['complete_output_comparisons'])==7 and
            all(r.get('max_absolute_difference',0)<=2e-5 for r in replay['complete_output_comparisons'].values()),
            'Incomplete full-output reanalysis')
    for rel,sha in audit['public_input_sha256'].items():
        p=Path(rel);require(not p.is_absolute() and '..' not in p.parts and p.parts[0] in ['notes','scripts'],'Unsafe audit path')
        require(not (root/p).is_symlink() and (root/p).is_file(),'Missing/unsafe bound input: '+rel)
        require(hashlib.sha256((root/p).read_bytes()).hexdigest()==sha,'Changed bound input: '+rel)
    results=json.loads((root/'notes/track2-perturbseq-results-v31.json').read_text())
    summary=validate_results(results)
    claims=json.loads((root/'notes/track2-perturbseq-register-v31.json').read_text())
    require([c['id'] for c in claims['claims']]==['R48','R49','R50','R51','R52'],'Missing falsification challenges')
    for c in claims['claims']:
        require(all(c.get(k) for k in ['claim','support','challenge','falsifier','decision','next_discriminating_action','reopening_criteria']),'Incomplete claim challenge')
    require(claims['unknown_means_hold'] and claims['safety_overrides_benefit'] and
            claims['all_pass_means']=='further_preclinical_review_only','Changed biological gates')
    sources=json.loads((root/'notes/track2-perturbseq-sources-v31.json').read_text())
    require(len(sources['queries'])==8 and sum(q['retained_records'] for q in sources['queries'])==98,'Source coverage mismatch')
    return summary|dict(claim_records=5,all_control_sensitivity_available=False,
        scope='Public computation consistency; not biological qualification or submission readiness')


if __name__=='__main__':print(json.dumps(check(),indent=2))
