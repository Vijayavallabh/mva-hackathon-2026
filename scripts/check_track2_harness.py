#!/usr/bin/env python3
"""Check the current public Track 2 state without GPUs, SSH, keys or subject inputs."""
import importlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = {
    'rescue_priority': None, 'everolimus': 'mechanistic_probe_only', 'hcq': 'reserve',
    'phase': 'unconfirmed', 'clinical_exposure_margin': None, 'wet_lab_performed': False,
    'video_recorded': False, 'video_url': None, 'runtime_measured': False,
    'upload_performed': False, 'upload_ready': False, 'provider_settings_verified': False,
    'licensing_scope_resolved': False,
}


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
    require(state['drug_science_version'] == 15, 'Drug science changed without a reviewed harness update')
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
        'evidence':'notes/track2-evidence-v15.json', 'validation':'notes/track2-validation-v15.md',
        'falsification_register':'notes/track2-falsification-register-v15.json',
        'falsification_review':'notes/track2-falsification-review-v15.md',
        'falsification_analysis':'notes/track2-falsification-analysis-v15.json',
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
    require(state['harness_review'] == f'notes/track2-harness-review-v{version}.md', 'Stale harness review')
    for name in ['AGENTS.md', 'session-handoff.md', 'README.md']:
        require('notes/track2-current.json' in documents[name], 'Missing state-record route: '+name)
        require(f'v{version}' in documents[name].lower(), 'Stale current revision: '+name)
        for found, role in re.findall(r'\bcurrent\s+v(\d+)\s+(\w+)', documents[name],re.I):
            expected = state['drug_science_version'] if role.lower() in {'ledger','evidence','validation'} else version
            require(int(found)==expected, 'Historical version mislabeled current: '+name)
    require(f'notes/track2-pitch-v{version}.md' in documents['session-handoff.md'], 'Stale transcript handoff')
    require(f'scripts/track2_release_v{version}.py' in documents['AGENTS.md'], 'Stale release entry point')
    return roles


def check(root=ROOT):
    state = json.loads((root/'notes/track2-current.json').read_text())
    features = json.loads((root/'feature_list.json').read_text())['features']
    documents = {name:(root/name).read_text() for name in ['AGENTS.md','session-handoff.md','README.md']}
    roles = validate(state, features, documents)
    for relative in roles.values():
        path = root/relative
        require(path.is_file() and not path.is_symlink(), 'Missing/symlinked current artifact: '+relative)
        require(path.resolve().is_relative_to(root.resolve()), 'Artifact leaves repository')
    release = importlib.import_module(f"track2_release_v{state['presentation_version']}")
    presentation = release.scientific_checks()
    return dict(passed=True, active_feature='feat-009', presentation_version=state['presentation_version'],
                drug_science_version=15, slides=presentation['slides'],
                narration_words=presentation['narration_words'], upload_ready=False,
                scope='Public artifact/state consistency; not biological validation or submission preflight')


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
