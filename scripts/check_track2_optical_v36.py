#!/usr/bin/env python3
"""Check completed optical evidence, missing states and conservative use on a CPU."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT_SHA256='05eaa24c5d929305b83228559cf8793a8a26662546378398fc814d2b37e0b6f7'
QUERIES=['BUB1B','BUB1','MAD2L1','CDC20','TTK','AURKB','PLK1','MTOR','RPTOR','RICTOR']


def require(condition,message):
    if not condition:raise ValueError(message)


def gain_check(gain,learned,baselines):
    best=max(x['macro_mrr'] for x in baselines.values())
    differences=[x['macro_mrr']-best for x in learned]
    require(len(differences)==4 and all(abs(a-b)<1e-12 for a,b in
        zip(differences,gain['point_difference'])),'Gain arithmetic differs')
    intervals=gain['paired_95_percent_intervals'];joint=gain['joint_minimum_seed_95_percent_interval']
    require(len(intervals)==4 and all(len(v)==2 and v[0]<=v[1] for v in intervals)
            and len(joint)==2 and joint[0]<=joint[1],'Invalid paired intervals')
    passed=all(v>=.02 for v in differences) and all(v[0]>0 for v in intervals) and joint[0]>0
    require(gain['practical_gain_gate_passed'] is passed,'Gain gate differs from its definition')
    require(gain['repetitions']==20000 and gain['seed']==3501 and gain['unit']=='held-out genes',
            'Bootstrap unit or prespecified settings changed')
    return passed


def validate(result):
    require(result['schema_version']==36 and result['status']=='complete','Incomplete optical comparison')
    require(result['excluded_original_v33_fits'] is True and result['corrected_features']==1064,
            'Coordinate correction missing')
    require((result['all_corrected_fits'],result['all_plate_workers'],result['all_median_workers'])==(16,16,16),
            'Incomplete declared work')
    for key,value in dict(phase='unconfirmed',clinical_exposure_margin=None,rescue_priority=None,
        everolimus='mechanistic_probe_only',hcq='reserve',wet_lab_performed=False,
        biological_validation=False,drug_ranking_changed=False).items():
        require(result[key]==value and type(result[key]) is type(value),'Unsupported promotion: '+key)
    require(set(result['arms'])=={'mitotic','interphase'},'Arm omitted')
    expected={'mitotic':(838224,832846,20404,[11,15,11,25]),
              'interphase':(31046046,2609447,20445,[859,1219,839,1435])}
    output={}
    original_names={'full_profile','full_correlation','basic_morphology','size_only','guide_abundance',
                    'pca_whiten_64','pca_whiten_128','pca_whiten_256'}
    extra_names={'mitotic_fraction','matched_sample_mean','full_median_shared_preprocessing','full_median_training_preprocessing'}
    for arm,(cells,sampled,guides,bub1b) in expected.items():
        r=result['arms'][arm]
        require((r['cells'],r['sampled_cells'],r['guides'],r['features'])==(cells,sampled,guides,1064),
                'Optical cohort differs')
        require([x['cells'] for x in r['query_coverage']['BUB1B']]==bub1b,'BUB1B source counts differ')
        require(set(r['query_status'])==set(QUERIES),'Fixed query family changed')
        require(set(r['baselines'])==original_names|extra_names,'Baseline omitted')
        for gene,state in r['query_status'].items():
            n=sum(x['cells']>=20 for x in r['query_coverage'][gene])
            require(state['eligible_guides']==n and state['rank_is_missing'] is (n<2)
                and state['status']==('evaluated' if n>=2 else 'insufficient_guide_coverage'),
                'Coverage missingness differs')
            for method in r['query_baselines'].values():
                value=method['mrr'][gene]
                require((value is None)==(n<2),'Missing query turned into a score')
                if value is not None:require(0<value<=1,'Invalid query MRR')
        for value in list(r['baselines'].values())+r['learned']+r['shuffled']:
            require(value['genes']==r['test_genes'] and 0<value['macro_mrr']<=1,'Unpaired retrieval cohort')
        for wave in r['waves'].values():
            require(wave['successful'] is True and len(wave['workers'])==8
                and all(w['returncode']==0 for w in wave['workers']),'Failed GPU worker promoted')
        require(len(r['models'])==8 and all(m['steps']==3000 for m in r['models']),
                'Smoke/incomplete training entered comparison')
        require(r['median_cpu_guides']==r['independent_cpu_guides']==40
            and r['median_cpu_max_error']<=2e-5 and r['independent_cpu_max_sum_error']<=1e-7
            and r['secondary_cpu_max_error']<=2e-5,'Numerical/source audit failed')
        require(len(r['plates'])==8 and all(len(w['plates'])==8 for w in r['plates']),
                'Plate worker/coverage omitted')
        require(r['unseen_acquisition_training'] is False and r['biological_validation'] is False
            and r['drug_ranking_changed'] is False,'Pooled acquisition or biological claim promoted')
        control=r['plate_control']
        require(control['post_hoc'] is True and control['full_profile_rank_replay'] is True
            and control['complete_count_conservation'] is True and len(control['within_plate'])==8,
            'Post-hoc plate-control provenance omitted')
        require(all(control[k] is False for k in ['original_gates_changed','unseen_acquisition_validation',
            'biological_validation','drug_ranking_changed']),'Post-hoc plate control promoted')
        require(control['plate_only']['genes']==r['test_genes'], 'Plate-only cohort differs')
        for plate in control['within_plate']:
            metric=plate['full_profile']
            require((metric is None)==(plate['status']=='insufficient_reference_coverage'),
                    'Missing within-plate result given a score')
            for gene,status in plate['query_status'].items():
                eligible=metric is not None and gene in metric['by_gene_mrr']
                require(eligible==(status=='evaluated'),'Within-plate query coverage differs')
        old={k:v for k,v in r['baselines'].items() if k in original_names}
        registered=dict(old,mitotic_fraction=r['baselines']['mitotic_fraction'])
        primary=gain_check(r['original_eight_baseline_gain'],r['learned'],old)
        full=gain_check(r['registered_nine_baseline_gain'],r['learned'],registered)
        exploratory=gain_check(r['exploratory_twelve_baseline_gain'],r['learned'],r['baselines'])
        require(not full or primary,'Added baseline rescued failed primary gate')
        require(not exploratory or full,'Exploratory baseline rescued failed registered gate')
        output[arm]=dict(cells=cells,test_genes=r['test_genes'],baseline_methods=12,
            primary_gain_gate_passed=primary,registered_gain_gate_passed=full,
            exploratory_gain_gate_passed=exploratory,bub1b=r['query_status']['BUB1B'])
    repair=result['arms']['interphase']['empty_shard_repair']
    require(repair['version']==36 and repair['scientific_policy_changed'] is False
            and len(repair['empty_sources'])==1 and repair['empty_sources'][0]['source_id']==6421679
            and len(repair['all_shard_receipts'])==3027,'Empty-shard provenance omitted')
    return dict(passed=True,version=36,status='complete',gpus=8,cells=sum(v[0] for v in expected.values()),
        corrected_fits=16,baseline_methods_per_arm=12,arms=output,biological_validation=False,drug_ranking_changed=False)


def check(root=ROOT):
    audit_path=root/'notes/track2-optical-audit-v36.json'
    require(hashlib.sha256(audit_path.read_bytes()).hexdigest()==AUDIT_SHA256,'Bound optical audit changed')
    audit=json.loads(audit_path.read_text())
    for relative,digest in audit['public_input_sha256'].items():
        p=Path(relative)
        require(not p.is_absolute() and '..' not in p.parts and not (root/p).is_symlink(),'Unsafe public path')
        require(hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,'Optical input changed: '+relative)
    replay=json.loads((root/'notes/track2-optical-local-replay-v36.json').read_text())
    require(replay['passed'] and replay['rank_to_mrr_recomputed'] and replay['all_archive_hashes_verified']
        and replay['paired_intervals_recomputed'] and replay['biological_validation'] is False,
        'Local numerical replay failed')
    require(replay['archive_sha256']==audit['archive']['sha256'],'Archive identity differs')
    r=json.loads((root/'notes/track2-optical-results-v36.json').read_text())
    encoding=json.loads((root/'notes/track2-optical-public-encoding-v36.json').read_text())
    original=(json.dumps(r,indent=2,allow_nan=False)+'\n').encode()
    require(encoding['decoded_values_identical'] is True
        and encoding['original_serialization_reconstructable'] is True
        and encoding['scientific_results_changed'] is False
        and hashlib.sha256(original).hexdigest()==encoding['source_sha256'],
        'Compact public results do not reconstruct the original analysis')
    public=(root/'notes/track2-optical-results-v36.json').read_bytes()
    require(len(public)==encoding['public_bytes']<=5_000_000
        and hashlib.sha256(public).hexdigest()==encoding['public_sha256'],
        'Compact public encoding differs')
    workbook=json.loads((root/'notes/track2-optical-workbook-v36.json').read_text())
    require(workbook['passed'] is True and workbook['biological_validation'] is False
        and workbook['results_sha256']==encoding['source_sha256'],
        'Public workbook count reconciliation failed')
    for arm in ['mitotic','interphase']:
        require(replay['arms'][arm]['post_hoc_plate_only_rank_metrics_recomputed'] is True,
                'Plate-control numerical replay missing')
        require(replay['arms'][arm]['cross_plate_metrics_recomputed']==
                {'mitotic':96,'interphase':384}[arm]
                and replay['arms'][arm]['within_plate_rank_metrics_recomputed']==0,
                'Cross-plate numerical replay coverage differs')
        require({row['guide']:row[arm+'_cells'] for row in workbook['counts']}==
            {row['guide']:row['cells'] for row in r['arms'][arm]['query_coverage']['BUB1B']},
            'Workbook and full export counts differ')
    return validate(r)


if __name__=='__main__':print(json.dumps(check(),indent=2))
