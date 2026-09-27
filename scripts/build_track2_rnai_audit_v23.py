#!/usr/bin/env python3
"""Bind the v23 public addendum to its completed primary GPU evidence archive."""
import json
from pathlib import Path
import tarfile
from track2_rnai_v23 import digest,save
from verify_track2_rnai_archive_v23 import verify

root=Path(__file__).resolve().parents[1];local=root/'results/feat009/rnai-v23'
archive=json.loads((local/'archive.json').read_text())
verified=verify(local/archive['path'],archive)
with tarfile.open(local/archive['path'],'r:gz') as t:
 registrations=[json.load(t.extractfile(f'outputs/worker-{i}/registration.json')) for i in range(8)]
 resources=json.load(t.extractfile('outputs/resources.json'))
paths=[
 'notes/track2-rnai-plan-v23.json','notes/track2-rnai-results-v23.json','notes/track2-rnai-tail-sensitivity-v23.json',
 'notes/track2-rnai-register-v23.json','notes/track2-rnai-search-v23.json','notes/track2-rnai-sources-v23.md',
 'notes/track2-rnai-validation-v23.md','notes/track2-rnai-v23.md','notes/track2-rnai-v23.svg',
 'scripts/track2_rnai_v23.py','scripts/track2_rnai_tail_sensitivity_v23.py','scripts/audit_track2_rnai_v23.py',
 'scripts/verify_track2_rnai_archive_v23.py','scripts/plot_track2_rnai_v23.py','scripts/check_track2_rnai_v23.py',
 'scripts/test_track2_rnai_v23.py','scripts/test_track2_rnai_check_v23.py','scripts/build_track2_rnai_audit_v23.py',
 'scripts/run_track2_rnai_download_v23.sh','scripts/run_track2_rnai_v23.sh',
 'scripts/track2_transcriptome_environment.toml','scripts/track2_transcriptome.uv.lock',
]
save(root/'notes/track2-rnai-audit-v23.json',dict(version=23,public_input_sha256={p:digest(root/p) for p in paths},
 archive=archive,archive_verification=verified,preparation=json.loads((local/'preparation.json').read_text()),
 numerical=json.loads((local/'numerical-audit.json').read_text()),registrations=registrations,
 resources=resources,biological_validation=False,drug_ranking_changed=False,
 presentation='Frozen v22; v23 is a separate research addendum',independent_scientific_review=False))
