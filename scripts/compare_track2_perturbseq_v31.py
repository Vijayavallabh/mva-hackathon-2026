#!/usr/bin/env python3
"""Compare every archived summary/table/matrix with a separate local reanalysis."""
import argparse
import gzip
import json
from pathlib import Path


def compare(original, replay):
    import numpy as np
    import pandas as pd
    errors = []
    numeric_fields = 0

    def walk(a, b, path=''):
        nonlocal numeric_fields
        if isinstance(a, dict):
            assert a.keys() == b.keys(), path
            for key in a:
                walk(a[key], b[key], path + '/' + key)
        elif isinstance(a, list):
            assert len(a) == len(b), path
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, path + '/' + str(i))
        elif isinstance(a, (int, float)) and not isinstance(a, bool):
            numeric_fields += 1
            assert type(a) is type(b), path
            if isinstance(a, int):
                assert a == b, path
            else:
                assert np.isfinite(a) and np.isfinite(b), path
                errors.append(abs(a - b))
        else:
            assert a == b, path

    walk(json.loads((original/'summary.json').read_text()), json.loads((replay/'summary.json').read_text()))
    records = {}
    assert {p.name for p in original.iterdir()} == {p.name for p in replay.iterdir()}
    for source in sorted(original.iterdir()):
        other = replay/source.name
        if source.suffix == '.npy':
            a, b = np.load(source), np.load(other)
            assert a.shape == b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
            error = float(np.max(np.abs(a-b)))
            assert error <= 2e-5
            records[source.name] = dict(shape=list(a.shape), max_absolute_difference=error)
        elif source.suffix == '.gz':
            a, b = pd.read_csv(source, sep='\t'), pd.read_csv(other, sep='\t')
            assert list(a.columns) == list(b.columns) and a.shape == b.shape
            maximum = 0.0
            for column in a:
                x, y = a[column], b[column]
                assert x.isna().equals(y.isna())
                if pd.api.types.is_numeric_dtype(x):
                    delta = np.abs(x.dropna().to_numpy()-y.dropna().to_numpy())
                    error = float(delta.max()) if len(delta) else 0.0
                    if pd.api.types.is_integer_dtype(x):
                        assert error == 0
                    maximum = max(maximum, error)
                else:
                    assert x.equals(y), column
            assert maximum <= 2e-5
            records[source.name] = dict(rows=len(a), max_absolute_difference=maximum,
                decompressed_byte_identical=gzip.decompress(source.read_bytes()) == gzip.decompress(other.read_bytes()))
    maximum = max(errors, default=0)
    assert maximum <= 2e-5
    return dict(passed=True, summary_byte_identical=(original/'summary.json').read_bytes()==(replay/'summary.json').read_bytes(),
        numeric_fields=numeric_fields, differing_numeric_fields=sum(x != 0 for x in errors),
        max_absolute_difference=maximum, tolerance=2e-5, complete_output_comparisons=records,
        scope='Numerical reproduction of archived analysis; not independent biological validation')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('original',type=Path);p.add_argument('replay',type=Path)
    a=p.parse_args()
    print(json.dumps(compare(a.original,a.replay),indent=2))
