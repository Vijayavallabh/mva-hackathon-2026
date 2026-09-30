#!/usr/bin/env python3
"""Verify a v25 local derived-evidence archive without extracting/executing it."""
import argparse
import json
from pathlib import Path
from verify_track2_rnai_archive_v23 import verify


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path)
    p.add_argument('--metadata',type=Path,required=True)
    a=p.parse_args()
    result=verify(a.archive,json.loads(a.metadata.read_text()))
    result['version']=25
    print(json.dumps(result,indent=2))
