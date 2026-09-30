#!/usr/bin/env python3
"""Check the current public Track 2 state without GPUs, SSH, keys or subject inputs."""
import hashlib
import importlib
import json
import re
from pathlib import Path

RNAI_STATE = {'version': 23, 'status': 'complete', 'report': 'notes/track2-rnai-v23.md', 'plan': 'notes/track2-rnai-plan-v23.json', 'results': 'notes/track2-rnai-results-v23.json', 'sensitivity': 'notes/track2-rnai-tail-sensitivity-v23.json', 'audit': 'notes/track2-rnai-audit-v23.json', 'validation': 'notes/track2-rnai-validation-v23.md', 'register': 'notes/track2-rnai-register-v23.json', 'check': 'scripts/check_track2_rnai_v23.py', 'figure': 'notes/track2-rnai-v23.svg', 'archive': 'results/feat009/rnai-v23/rnai-v23-audit.tar.gz', 'gpus': 8, 'unordered_pair_comparisons': 1536619950, 'conditional_control_sets': 5843968, 'orthogonal_comparisons': 2364754, 'drug_ranking_changed': False, 'presentation_integration': 'integrated_in_v26_preserves_v23'}
RNAI_AUDIT_SHA256 = '27bff5205ea443acdfe1dbb8863f21725af36af3e7400199bcea3345cdf9cb3c'
CRISPR_STATE = {
    'version':25, 'status':'complete', 'report':'notes/track2-crispr-v25.md',
    'plan':'notes/track2-crispr-plan-v25.json','results':'notes/track2-crispr-results-v25.json',
    'summary':'notes/track2-crispr-summary-v25.json','audit':'notes/track2-crispr-audit-v25.json',
    'continuity':'notes/track2-crispr-continuity-v25.json','validation':'notes/track2-crispr-validation-v25.md',
    'register':'notes/track2-crispr-register-v25.json','check':'scripts/check_track2_crispr_v25.py',
    'reproduction':'notes/track2-crispr-reproduction-v25.md',
    'archive':'results/feat009/crispr-v25/crispr-v25-audit.tar.gz',
    'gpus':8,'comparisons':2474445074,'bub1b_profiles':31,'bub1b_guides':1,
    'matched_compound_profiles':285488,'drug_ranking_changed':False,
    'presentation_integration':'integrated_in_v26_preserves_v25',
}
CRISPR_AUDIT_SHA256 = '264a46ecc491e0894d57f204c9d9739cb20494ca866bb6e73e3fdce5bd8e3ebb'

ROOT = Path(__file__).resolve().parents[1]
STATUS = {
    'rescue_priority': None, 'everolimus': 'mechanistic_probe_only', 'hcq': 'reserve',
    'phase': 'unconfirmed', 'clinical_exposure_margin': None, 'wet_lab_performed': False,
    'video_recorded': False, 'video_url': None, 'runtime_measured': False,
    'upload_performed': False, 'upload_ready': False, 'provider_settings_verified': False,
    'licensing_scope_resolved': False,
}
CURRENT_REVIEW = {
    'script': 'scripts/check_track2_harness.py',
    'isolation_audit': 'scripts/audit_track2_harness.py',
    'guide': 'notes/track2-reviewer-guide-v26.md',
    'readiness': 'notes/track2-owner-readiness-v26.md',
}
RESEARCH_PATHS = {
    'plan': 'notes/track2-transcriptome-plan-v19.json',
    'phase2_plan': 'notes/track2-transcriptome-phase2-plan-v19.json',
    'source_review': 'notes/track2-transcriptome-source-review-v19.md',
    'identity_audit': 'notes/track2-transcriptome-identity-v19.json',
    'check': 'scripts/check_track2_transcriptome.py',
    'report': 'notes/track2-transcriptome-v19.md',
    'reproduction': 'notes/track2-transcriptome-reproduction-v19.md',
    'audit': 'notes/track2-transcriptome-audit-v19.json',
    'followup_plan': 'notes/track2-transcriptome-followup-plan-v19.json',
    'primary_results': 'notes/track2-transcriptome-results-v19.json',
    'phase2_results': 'notes/track2-transcriptome-phase2-results-v19.json',
    'followup_results': 'notes/track2-transcriptome-followup-results-v19.json',
    'figure': 'notes/track2-transcriptome-v19.svg',
}
RESEARCH_STATE = {
    'version': 19, 'kind': 'public_perturbation_transcriptome', 'status': 'complete',
    'report_integration': 'integrated_in_v26_preserves_v19_through_v25',
    'gpus': 8, 'compound_profiles': 312438, 'query_compound_comparisons': 12185082,
    'resampled_reagent_sets': 560000, 'primary_query_gates_passed': 0,
    'drug_ranking_changed': False,
    'archive': 'results/feat009/transcriptome-remote-v19/transcriptome-v19-audit.tar.gz',
}
# Frozen campaign manifest from commit 71488a7; new science needs a new reviewed version.
CAMPAIGN_AUDIT_SHA256 = 'a2ab0132f37a2fdce4f5e2c0efbe468da525ee8d12125e3d4b8baf7b22cb7ca1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(state, features, documents):
    require(state['schema_version'] == 1, 'Unsupported current-state schema')
    version = state['presentation_version']
    require(type(version) is int and version >= 14, 'Stale presentation revision')
    require(state['active_feature'] == 'feat-009', 'Wrong active feature')
    require([f['id'] for f in features if f['status'] == 'in_progress'] == ['feat-009'],
            'Exactly one active feature is required')
    current = next(f for f in features if f['id'] == 'feat-009')
    require('notes/track2-current.json' in current['evidence'] and f'v{version}' in current['evidence'],
            'Feature evidence points to stale artifacts')
    require(state['drug_science_version'] == 21, 'Drug science changed without a reviewed harness update')
    require(state['status'] == STATUS, 'Unsupported scientific/delivery promotion; review evidence before updating the harness')
    require(state['model_campaign'] == dict(protein_scores=84, structures=192, dna_comparisons=100,
                                          inference_complete=True), 'Model completion/count drift')
    roles = {
        'report':f'notes/track2-report-v{version}.md',
        'slides':f'notes/track2-slides-v{version}.html',
        'pitch':f'notes/track2-pitch-v{version}.md',
        'transcript':f'notes/track2-transcript-v{version}.txt',
        'video_description':f'notes/track2-video-description-v{version}.md',
        'design_review':f'notes/track2-v{version}-design.md',
        'evidence':'notes/track2-evidence-v21.json', 'validation':'notes/track2-validation-v21.md',
        'falsification_register':'notes/track2-falsification-register-v21.json',
        'falsification_review':'notes/track2-falsification-review-v21.md',
        'falsification_analysis':'notes/track2-falsification-analysis-v21.json',
        'latest_model_findings':'notes/track2-latest-models.md',
        'latest_model_audit':'notes/track2-latest-model-audit.json',
        'release_script':f'scripts/track2_release_v{version}.py',
        'renderer':f'scripts/render_track2_slides_v{version}.mjs',
        'af3_terms':'notes/alphafold3-output-terms.md',
        'af3_notice':'notes/alphafold3-Legally-Binding-Terms-of-Use.txt',
        'official_requirements':f'notes/track2-requirements-v{version}.json',
        'community_review':'notes/track2-community-review-20260924.md',
        'reviewer_guide':f'notes/track2-reviewer-guide-v{version}.md',
        'owner_readiness':f'notes/track2-owner-readiness-v{version}.md',
        'public_review_script':f'scripts/track2_public_review_v{version}.py',
        'document_exporter':f'scripts/track2_export_documents_v{version}.py',
        'report_renderer':f'scripts/render_track2_report_v{version}.mjs',
        'bundle_script':f'scripts/track2_bundle_v{version}.py',
    }
    require(state['artifacts'] == roles, 'Mixed, missing or unsafe artifact paths')
    require(state['snapshot'] == f'results/feat009/jvv7_track2_research_v{version}', 'Stale snapshot path')
    require(state['video_materials_bundle'] == f'results/feat009/jvv7_track2_video_materials_v{version}.zip',
            'Stale recording-materials bundle path')
    require(re.fullmatch(rf'results/feat009/v{version}-[a-z0-9-]+',state['render_directory']),
            'Stale or unsafe render-directory path')
    require(re.fullmatch(rf'results/feat009/v{version}-[a-z0-9-]+',state['document_directory']),
            'Stale or unsafe document-directory path')
    require(state.get('harness_version') == 26 and
            state['harness_review'] == 'notes/track2-harness-review-v26.md', 'Stale harness review')
    require(state.get('current_review') == CURRENT_REVIEW, 'Missing or stale combined review route')
    require(state.get('rnai_addendum') == RNAI_STATE, 'Missing or inconsistent RNAi addendum')
    require(state.get('crispr_addendum') == CRISPR_STATE and
            all(type(state['crispr_addendum'][k]) is type(v) for k,v in CRISPR_STATE.items()),
            'Missing or inconsistent CRISPR addendum')
    addendum = state.get('research_addendum')
    expected = RESEARCH_PATHS | RESEARCH_STATE
    require(isinstance(addendum, dict) and addendum == expected and
            all(type(addendum[k]) is type(v) for k, v in expected.items()),
            'Missing, unsafe or inconsistent research addendum')
    for name in ['AGENTS.md', 'session-handoff.md', 'README.md']:
        require('notes/track2-current.json' in documents[name], 'Missing state-record route: '+name)
        require(f'v{version}' in documents[name].lower(), 'Stale current revision: '+name)
        for found, role in re.findall(r'\bcurrent\s+v(\d+)\s+(\w+)', documents[name],re.I):
            role_versions = {
                'ledger': state['drug_science_version'], 'evidence': state['drug_science_version'],
                'validation': state['drug_science_version'], 'harness': state['harness_version'],
                'research': addendum['version'], 'addendum': addendum['version'],
                'transcriptome': addendum['version'], 'rnai': 23, 'crispr':25,
            }
            expected = role_versions.get(role.lower(), version)
            require(int(found)==expected, 'Historical version mislabeled current: '+name)
    require(f'notes/track2-pitch-v{version}.md' in documents['session-handoff.md'], 'Stale transcript handoff')
    require(f'scripts/track2_release_v{version}.py' in documents['AGENTS.md'], 'Stale release entry point')
    for name, document in documents.items():
        for route in [CURRENT_REVIEW['script'], CURRENT_REVIEW['guide'], RESEARCH_PATHS['report']]:
            require(route in document, 'Missing combined research route: '+name+' / '+route)
    return roles


def public_path(root, relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts, 'Unsafe public artifact path')
    path = root / p
    require(path.is_file(), 'Missing public artifact: '+relative)
    require(not any((root / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts)+1)),
            'Symlinked public artifact: '+relative)
    require(path.resolve().is_relative_to(root.resolve()), 'Artifact leaves repository')
    return path


def campaign_audit(root):
    audit_bytes = public_path(root, RESEARCH_PATHS['audit']).read_bytes()
    require(hashlib.sha256(audit_bytes).hexdigest() == CAMPAIGN_AUDIT_SHA256, 'Frozen campaign audit changed')
    audit = json.loads(audit_bytes)
    for relative in audit['public_input_sha256']:
        public_path(root, relative)
    return audit


def research_summary(first, second, followup, identity, audit):
    """Derive current claims from completed outputs; no new biological inference."""
    primary = [r for q in first['queries'] for s in q['spaces'] if s['name'] == 'raw'
               for r in s['named_compounds'] if r['compound'] == 'everolimus']
    proper = {r['signature_id']: r for q in second['queries'] for s in q['spaces'] if s['name'] == 'raw'
              for r in s['named_compounds'] if r['compound'] == 'everolimus' and
              r['compound_id'] == identity['eligible_identity_id']}
    ht29 = [r for r in followup['rows'] if r['cell_id'] == 'HT29' and
            r['arm'] == 'provider_members_shared_pc1_removed']
    require(len(ht29) == 1, 'Missing HT29 counterweight')
    waves = [first, second, followup]
    for wave in waves:
        runs = wave['gpu_runs']
        require([r['shard'] for r in runs] == list(range(8)) and
                all(r['complete'] is True for r in runs), 'Incomplete GPU wave')
        require(sorted(q for r in runs for q in r['query_ids']) == sorted(q['query_id'] for q in first['queries']),
                'GPU query coverage drift')
    vectors = audit['score_vectors']
    require(len(vectors) == 2 and {r['wave'] for r in vectors} == {'shard-', 'phase2-shard-'},
            'Missing expression release')
    for record, result in zip(vectors, [first, second]):
        require(record['vectors'] == sum(len(q['spaces']) for q in result['queries']) and
                record['comparisons'] == record['vectors'] * record['profiles'], 'Comparison count drift')
    summary = dict(
        gpus=len(first['gpu_runs']), completed_gpu_waves=len(waves),
        compound_profiles=sum(r['profiles'] for r in vectors),
        query_compound_comparisons=sum(r['comparisons'] for r in vectors),
        resampled_reagent_sets=sum(q['null_draws'] for q in first['queries']) + sum(r['null_draws'] for r in followup['rows']),
        primary_contexts=len(first['queries']),
        primary_query_gates_passed=sum(q['operational_query_gate'] for q in first['queries']),
        post_hoc_comparisons=len(followup['rows']),
        post_hoc_full_filters_passed=sum(r['same_operational_filter'] for r in followup['rows']),
        primary_everolimus_comparisons=len(primary),
        primary_everolimus_profiles=len({r['signature_id'] for r in primary}),
        primary_everolimus_positive_correlations=sum(r['correlation'] > 0 for r in primary),
        phase2_unresolved_labelled_profiles=sum(identity['phase2_profile_counts_by_id'][i] for i in identity['unresolved_ids']),
        phase2_reference_matching_profiles=len(proper),
        phase2_reference_matching_qc_passes=sum(r['quality_pass'] for r in proper.values()),
        ht29_post_hoc_reagents=ht29[0]['n_reagents'],
        ht29_post_hoc_adjusted_tail=ht29[0]['split_null_BH_q'],
        ht29_full_filter_passed=ht29[0]['same_operational_filter'],
        drug_ranking_changed=first['drug_ranking_changed'],
    )
    expected = dict(gpus=8, completed_gpu_waves=3, compound_profiles=312438,
        query_compound_comparisons=12185082, resampled_reagent_sets=560000,
        primary_contexts=14, primary_query_gates_passed=0, post_hoc_comparisons=42,
        post_hoc_full_filters_passed=0, primary_everolimus_comparisons=19,
        primary_everolimus_profiles=14, primary_everolimus_positive_correlations=13,
        phase2_unresolved_labelled_profiles=174, phase2_reference_matching_profiles=6,
        phase2_reference_matching_qc_passes=0, ht29_post_hoc_reagents=5,
        ht29_post_hoc_adjusted_tail=0.041995800419958006,
        ht29_full_filter_passed=False, drug_ranking_changed=False)
    require(summary == expected, 'Unreviewed research-summary change')
    require(audit['retained_null_draws_rechecked'] == summary['resampled_reagent_sets'], 'Null archive count drift')
    return summary


def check(root=ROOT):
    require(root.resolve() == ROOT, 'Run this checker from the target checkout')
    state = json.loads(public_path(root, 'notes/track2-current.json').read_text())
    features = json.loads(public_path(root, 'feature_list.json').read_text())['features']
    documents = {name:public_path(root, name).read_text() for name in ['AGENTS.md','session-handoff.md','README.md']}
    roles = validate(state, features, documents)
    for relative in set(roles.values()) | set(CURRENT_REVIEW.values()) | set(RESEARCH_PATHS.values()) | {state['harness_review']}:
        public_path(root, relative)
    audit = campaign_audit(root)
    release = importlib.import_module(f"track2_release_v{state['presentation_version']}")
    presentation = release.scientific_checks()
    transcriptome = importlib.import_module('check_track2_transcriptome')
    require(transcriptome.check(root)['passed'], 'Public transcriptome check failed')
    first, second, followup, identity = [json.loads(public_path(root, RESEARCH_PATHS[k]).read_text())
        for k in ['primary_results', 'phase2_results', 'followup_results', 'identity_audit']]
    summary = research_summary(first, second, followup, identity, audit)
    for field in ['gpus', 'compound_profiles', 'query_compound_comparisons', 'resampled_reagent_sets',
                  'primary_query_gates_passed', 'drug_ranking_changed']:
        require(state['research_addendum'][field] == summary[field], 'Current research summary drift: '+field)
    rnai_audit = public_path(root, RNAI_STATE['audit']).read_bytes()
    require(hashlib.sha256(rnai_audit).hexdigest() == RNAI_AUDIT_SHA256, 'Frozen RNAi audit changed')
    rnai = importlib.import_module('check_track2_rnai_v23').check(root)
    require(rnai['passed'], 'RNAi review failed')
    crispr_bytes=public_path(root,CRISPR_STATE['audit']).read_bytes()
    require(hashlib.sha256(crispr_bytes).hexdigest()==CRISPR_AUDIT_SHA256,'Frozen CRISPR audit changed')
    crispr=importlib.import_module('check_track2_crispr_v25').check(root)
    require(crispr['passed'],'CRISPR review failed')
    for key in ['gpus','comparisons','bub1b_profiles','bub1b_guides','matched_compound_profiles','drug_ranking_changed']:
        require(state['crispr_addendum'][key]==crispr[key],'Current CRISPR summary drift: '+key)
    return dict(passed=True, active_feature='feat-009', harness_version=26,
                presentation_version=state['presentation_version'],
                drug_science_version=21, slides=presentation['slides'],
                narration_words=presentation['narration_words'], falsification_amendment=presentation['falsification_amendment'], upload_ready=False,
                research_addendum=dict(version=19, status='complete', **summary),
                rnai_addendum=rnai, crispr_addendum=crispr, biological_validation=False,
                scope='Combined public presentation/research consistency; not biological validation or submission preflight')


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
