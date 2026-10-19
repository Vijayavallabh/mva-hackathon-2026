#!/usr/bin/env python3
"""Encode the unchanged optical JSON below the public repository's blob limit."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('destination',type=Path)
    parser.add_argument('--receipt',type=Path,required=True)
    args=parser.parse_args()
    if args.destination.exists() or args.receipt.exists():
        raise ValueError('Use new paths; preserve existing artifacts first')
    source=args.source.read_bytes();value=json.loads(source)
    original=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    if original!=source:
        raise ValueError('Source is not the retained analysis serialization')
    compact=(json.dumps(value,separators=(',',':'),allow_nan=False)+'\n').encode()
    if len(compact)>5_000_000 or json.loads(compact)!=value:
        raise ValueError('Publication size or lossless round-trip check failed')
    args.destination.write_bytes(compact)
    record=dict(version=36,source_bytes=len(source),public_bytes=len(compact),
        source_sha256=digest(source),public_sha256=digest(compact),
        original_serialization_reconstructable=True,decoded_values_identical=True,
        archive_member='outputs/final-review-v36/results.json',
        script_sha256=digest(Path(__file__).read_bytes()),
        scientific_results_changed=False,biological_validation=False,
        reason='Whitespace-only encoding change to satisfy the 5,000,000-byte public blob limit.')
    args.receipt.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
