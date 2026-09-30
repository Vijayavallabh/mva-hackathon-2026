#!/usr/bin/env python3
"""Bind the complete v25 public findings to the verified local evidence archive."""
import hashlib
import json
from pathlib import Path
import tarfile
from verify_track2_rnai_archive_v23 import verify

ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build():
    local=ROOT/'results/feat009/crispr-v25'
    expected=json.loads((local/'archive.json').read_text())
    checked=verify(local/expected['path'],expected)
    with tarfile.open(local/expected['path'],'r:gz') as tar:
        for remote,public in [('outputs/results.json','notes/track2-crispr-results-v25.json'),
                              ('outputs/summary.json','notes/track2-crispr-summary-v25.json'),
                              ('outputs/continuity-final.json','notes/track2-crispr-continuity-v25.json'),
                              ('outputs/everolimus-panel.tsv','notes/track2-crispr-everolimus-v25.tsv'),
                              ('outputs/source-manifest.json','notes/track2-crispr-source-manifest-v25.json')]:
            assert hashlib.sha256(tar.extractfile(remote).read()).hexdigest()==sha(ROOT/public),public
        for name in ['track2_crispr_v25.py','download_track2_crispr_v25.py','run_track2_crispr_v25.sh',
                     'audit_track2_crispr_v25.py','summarize_track2_crispr_v25.py',
                     'audit_track2_crispr_continuity_v25.py','archive_track2_crispr_v25.py']:
            assert hashlib.sha256(tar.extractfile('scripts/'+name).read()).hexdigest()==sha(ROOT/'scripts'/name),name
        registration=dict(plan_sha256=tar.extractfile('outputs/plan-registration.sha256').read().decode().split()[0],
                          registered_utc=tar.extractfile('outputs/plan-registration-time.txt').read().decode().strip(),
                          nonfinite_guard_fixed_utc=tar.extractfile('outputs/nonfinite-guard-fix-time.txt').read().decode().strip(),
                          completed_utc=tar.extractfile('outputs/complete.txt').read().decode().strip())
        numerical=json.load(tar.extractfile('outputs/audit.json'))
        numerical.pop('direct_everolimus_checks')
    paths=sorted(str(p.relative_to(ROOT)) for pattern in [
        'notes/track2-crispr-*-v25.*','notes/track2-crispr-v25.md',
        'scripts/*track2_crispr*v25*',
    ] for p in ROOT.glob(pattern) if p.is_file() and p.name!='track2-crispr-audit-v25.json')
    paths += ['scripts/verify_track2_rnai_archive_v23.py','scripts/track2_transcriptome_environment.toml','scripts/track2_transcriptome.uv.lock']
    result=dict(version=25,public_input_sha256={p:sha(ROOT/p) for p in sorted(set(paths))},
                archive=expected,archive_verification=checked,numerical=numerical,registration=registration,
                independent_scientific_review=False,biological_validation=False,drug_ranking_changed=False,
                presentation='Frozen v24; v25 is a separate completed research addendum',
                source_files_redistributed=False)
    with (ROOT/'notes/track2-crispr-audit-v25.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(passed=True,bound_inputs=len(result['public_input_sha256']),archive=checked),indent=2))


if __name__=='__main__':build()
