#!/usr/bin/env python3
"""Bind the new v27 research files; never edits historical inputs or archives."""
import json
from pathlib import Path
from track2_saturation_v27 import digest

ROOT=Path(__file__).resolve().parents[1]


def build():
    archive=ROOT/'results/feat009/falsification-v27/archive'
    excluded={'notes/track2-falsification-audit-v27.json'}
    paths=sorted([p for folder,pattern in [('notes','*v27*'),('scripts','*v27*')]
                  for p in (ROOT/folder).glob(pattern) if p.is_file() and str(p.relative_to(ROOT)) not in excluded])
    manifest=json.loads((archive/'archive-manifest.json').read_text())
    for name in ['scripts/track2_saturation_v27.py','scripts/track2_specificity_v27.py',
                 'scripts/run_track2_saturation_v27.sh','scripts/run_track2_specificity_v27.sh',
                 'scripts/provenance_track2_falsification_v27.py']:
        assert digest(ROOT/name)==manifest['files'][name], 'Executed code differs from public source'
    for public,original in [('notes/track2-saturation-plan-v27.json','inputs/plan.json'),
                            ('notes/track2-specificity-plan-v27.json','inputs/specificity-plan.json')]:
        assert digest(ROOT/public)==manifest['files'][original], 'Fixed plan changed'
    verification=json.loads((ROOT/'results/feat009/falsification-v27/archive-verification.json').read_text())
    result=dict(version=27,archive=verification,archive_member_sha256=manifest['files'],
        public_input_sha256={str(p.relative_to(ROOT)):digest(p) for p in paths},
        source_snapshots=json.loads((ROOT/'results/feat009/v27-source-review-20261001/manifest.json').read_text()),
        v26_preservation=json.loads((ROOT/'results/feat009/v27-preservation-20261001.json').read_text()),
        scope='Source/plan/output bindings and internal numerical checks; not biological validation')
    out=ROOT/'notes/track2-falsification-audit-v27.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(public_files=len(paths),archive_files=verification['files'],sha256=digest(out))))


if __name__=='__main__':build()
