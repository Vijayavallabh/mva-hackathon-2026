#!/usr/bin/env python3
"""Validate the machine-readable four-arm protocol schema and an example instance."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check():
    import jsonschema
    schema = json.loads((ROOT / 'notes/track2-four-arm-protocol-schema-v57.json').read_text())
    example = json.loads((ROOT / 'notes/track2-four-arm-protocol-example-v57.json').read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(example, schema)
    require_unique_arms = len({(a['genetic_state'], a['intervention']) for a in example['arms']}) == len(example['arms'])
    if not require_unique_arms:
        raise ValueError('Duplicate four-arm definition')
    if example['model']['qualification_status'] != 'unqualified':
        raise ValueError('Example must not claim model qualification')
    return {
        'passed': True,
        'schema': 'notes/track2-four-arm-protocol-schema-v57.json',
        'example': 'notes/track2-four-arm-protocol-example-v57.json',
        'example_valid': True,
        'biological_validation': False,
        'clinical_authorization': False,
        'scope': 'Structural schema validation only; no biological or clinical validation.'
    }

if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
