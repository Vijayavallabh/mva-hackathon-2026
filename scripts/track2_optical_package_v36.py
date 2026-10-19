#!/usr/bin/env python3
"""Collect completed public optical comparisons and their bounded review archive.

Model checkpoints, source parquet and prepared numeric matrices remain on the
owner host. This archive contains review records, code, logs and provenance.
"""
import argparse
import json
from pathlib import Path
import tarfile

from track2_optical_fetch_v33 import hashes, write_json
from track2_optical_audit_v35 import metric_summary
from track2_optical_prepare_v35 import QUERIES


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    args=parser.parse_args();root=args.root.resolve()
    if not root.is_relative_to('/home/prachh/v'):
        raise ValueError('All work must stay under v')
    out=root/'outputs/final-review-v36';out.mkdir(exist_ok=False)
    paths=set()
    def read(relative):
        path=root/relative
        if not path.is_file() or path.is_symlink():raise ValueError('Missing/unsafe input: '+relative)
        paths.add(relative)
        return json.loads(path.read_text())
    for directory in ['interphase-v36-pipeline','secondary-v35-pipeline']:
        if read('outputs/'+directory+'/finished.json')['successful'] is not True:
            raise ValueError('Pipeline incomplete')
    arms={}
    for arm in ['mitotic','interphase']:
        source='prepared-v35/'+arm
        prepared=read(source+'/complete.json')
        shard_receipts=[read(str(p.relative_to(root))) for p in (root/source/'shards').glob('*/complete.json')]
        if sum(r['cells'] for r in shard_receipts)!=prepared['cells']:
            raise ValueError('Prepared shard cell conservation failed')
        for name in ['guides.json','features.json','guide_plates.json']:
            if hashes(root/source/name)[1]!=prepared['outputs'][name]:raise ValueError('Preparation changed')
            read(source+'/'+name)
        summary=read('outputs/audit-v35-'+arm+'.json')
        independent=read('outputs/audit-independent-v35-'+arm+'.json')
        plates=read('outputs/plate-summary-v35-'+arm+'.json')
        plate_control=read('plate-control-v36/'+arm+'/results.json')
        control_receipt=read('plate-control-v36/'+arm+'/complete.json')
        if hashes(root/'plate-control-v36'/arm/'results.json')[1]!=control_receipt['files']['results.json']:
            raise ValueError('Plate-control artifact changed')
        if not plate_control['full_profile_rank_replay'] or not plate_control['complete_count_conservation']:
            raise ValueError('Plate-control replay failed')
        secondary=read('secondary-v35/'+arm+'/results.json')
        complete=read('secondary-v35/'+arm+'/complete.json')
        for name,digest in complete['files'].items():
            if hashes(root/'secondary-v35'/arm/name)[1]!=digest:raise ValueError('Secondary artifact changed')
        med=read('median-v35/'+arm+'/complete.json')
        medaudit=read('median-v35/'+arm+'/cpu_audit.json')
        if (med['cells'],med['guides'],med['features'])!=(prepared['cells'],prepared['guides'],1064):
            raise ValueError('Median/preparation cohort differs')
        if len(medaudit)!=40 or max(v['maximum_absolute_error'] for v in medaudit)>2e-5:
            raise ValueError('Median CPU audit failed')
        if not independent['passed'] or len(independent['guides'])!=40:
            raise ValueError('Independent query reductions incomplete')
        metrics=dict(summary['baselines'])
        for name,result in secondary['secondary_results'].items():metrics[name]=metric_summary(result)
        if len(metrics)!=12:raise ValueError('A declared baseline is missing')
        model_rows=[];query_results=[]
        for label in ['real','shuffled']:
            for seed in [3301,3302,3303,3304]:
                folder=f'models-v35/{arm}-{seed}-{label}'
                r=read(folder+'/results.json');c=read(folder+'/complete.json')
                if hashes(root/folder/'results.json')[1]!=c['files']['results.json']:
                    raise ValueError('Model result changed')
                split=read(folder+'/split.json')
                if set(split['training'])&set(split['test']) or set(QUERIES)&set(split['training']):
                    raise ValueError('Evaluated/query genes entered fitting')
                model_rows.append(dict(seed=seed,shuffled=r['shuffled'],steps=read(folder+'/trace.json')[-1]['step'],
                    elapsed_seconds=r['elapsed_seconds'],peak_gpu_bytes=r['peak_gpu_bytes'],
                    numerical_audit=r['numerical_audit'],best_validation=r['best_validation']))
                query_results.append(dict(seed=seed,shuffled=r['shuffled'],
                    mrr={g:r['learned']['by_gene_mrr'].get(g) for g in QUERIES},
                    rows=[x for x in r['learned']['rows'] if x['gene'] in QUERIES]))
                for f in (root/folder).glob('*.json'):paths.add(str(f.relative_to(root)))
        waves={}
        for kind,folder in [('models','outputs/wave-v35-'+arm),('plates','outputs/wave-plates-v35-'+arm),
                            ('medians','median-v35/'+arm)]:
            wave=read(folder+'/finished.json')
            if not wave['successful'] or len(wave['workers'])!=8 or any(w['returncode']!=0 for w in wave['workers']):
                raise ValueError('Eight-worker wave did not complete: '+folder)
            waves[kind]=wave
            for suffix in ['*.json','*.jsonl']:
                for f in (root/folder).glob(suffix):paths.add(str(f.relative_to(root)))
        for f in (root/'median-v35'/arm/'workers').rglob('*.json'):paths.add(str(f.relative_to(root)))
        for f in (root/'plate-v35').glob(arm+'-*/*.json'):paths.add(str(f.relative_to(root)))
        query_baselines={}
        first=read(f'models-v35/{arm}-3301-real/results.json')
        for name,result in dict(first['baseline_results'],**secondary['secondary_results']).items():
            query_baselines[name]=dict(mrr={g:result['by_gene_mrr'].get(g) for g in QUERIES},
                rows=[x for x in result['rows'] if x['gene'] in QUERIES])
        arms[arm]=dict(cells=prepared['cells'],sampled_cells=prepared['sampled_cells'],guides=prepared['guides'],
            genes=prepared['genes'],features=prepared['features'],test_genes=summary['genes'],
            query_coverage=prepared['query_coverage'],query_status=summary['query_status'],
            baselines=metrics,learned=summary['learned'],shuffled=summary['shuffled'],
            original_eight_baseline_gain=summary['real_gain'],
            registered_nine_baseline_gain=secondary['registered_gain_with_cross_arm'],
            exploratory_twelve_baseline_gain=secondary['exploratory_gain_with_all_baselines'],
            exploratory_shuffled_gain=secondary['exploratory_shuffled_with_all_baselines'],
            query_baselines=query_baselines,query_learned=query_results,
            query_cross_arm_counts=secondary['query_counts'],
            median_cpu_guides=len(medaudit),median_cpu_max_error=max(v['maximum_absolute_error'] for v in medaudit),
            independent_cpu_guides=len(independent['guides']),
            independent_cpu_max_sum_error=max(v['maximum_sum_error'] for v in independent['guides']),
            secondary_cpu_max_error=secondary['cpu_float64_cuda_float32_max_absolute_error'],
            models=model_rows,waves=waves,plates=plates['workers'],plate_control=plate_control,
            empty_shard_repair=prepared.get('empty_shard_repair'),
            unseen_acquisition_training=False,biological_validation=False,drug_ranking_changed=False)
    for relative in ['inputs/plan.json','inputs/amendment.json','inputs/amendment-v35.json',
                     'inputs/secondary-plan-v35.json','inputs/median-plan-v35.json','inputs/plate-control-plan-v36.json',
                     'inputs/dataverse-metadata.json','outputs/audit-v35-equivalence.json',
                     'outputs/download-mitotic-complete.json','outputs/download-interphase-complete.json']:
        read(relative)
    for directory in ['interphase-v35-pipeline','interphase-v36-pipeline','secondary-v35-pipeline']:
        for f in (root/'outputs'/directory).glob('*.json'):paths.add(str(f.relative_to(root)))
    for f in (root/'scripts').glob('*optical*.py'):paths.add(str(f.relative_to(root)))
    for name in ['pyproject.toml','uv.lock']:
        if (root/name).is_file():paths.add(name)
    for pattern in ['*v35*.log','*v36*.log']:
        for f in (root/'logs').glob(pattern):
            if f.name not in {'package-optical-v36.log','finalize-v36-pipeline.log'}:
                paths.add(str(f.relative_to(root)))
    result=dict(schema_version=36,status='complete',source_doi='10.7910/DVN/VYKTI5',
        source_version='2.0',source_license='CC BY 4.0',corrected_features=1064,
        excluded_original_v33_fits=True,arms=arms,all_corrected_fits=16,
        all_plate_workers=16,all_median_workers=16,original_model_steps=3000,
        phase='unconfirmed',clinical_exposure_margin=None,rescue_priority=None,
        everolimus='mechanistic_probe_only',hcq='reserve',wet_lab_performed=False,
        biological_validation=False,drug_ranking_changed=False,
        script_sha256=hashes(Path(__file__))[1],
        bindings={name:hashes(root/name)[1] for name in sorted(paths)},
        limitations=['Gene retrieval is an engineering benchmark, not functional rescue.',
            'HeLa is transformed and p53-defective; fixed classes do not measure longitudinal fate.',
            'Median and matched-sample sensitivities are exploratory; original gates are preserved.',
            'Seeds, guides and resamples do not create independent biological replications.',
            'The plate comparison reuses a pooled encoder; reference cohorts vary by plate.'])
    write_json(out/'results.json',result);paths.add('outputs/final-review-v36/results.json')
    archive=out/'optical-v36-review.tar.gz'
    with tarfile.open(archive,'w:gz') as tar:
        for relative in sorted(paths):
            p=root/relative
            if p.is_symlink() or not p.is_file():raise ValueError('Unsafe archive input')
            tar.add(p,arcname=relative,recursive=False)
    manifest=dict(files=len(paths),bytes=archive.stat().st_size,sha256=hashes(archive)[1],
        content_sha256={n:hashes(root/n)[1] for n in sorted(paths)},
        scope='Public review records, code and provenance; excludes source parquet, checkpoints and prepared numeric matrices')
    write_json(out/'manifest.json',manifest)
    print(json.dumps(dict(archive=str(archive),files=len(paths),bytes=manifest['bytes'],sha256=manifest['sha256']),indent=2))


if __name__=='__main__':main()
