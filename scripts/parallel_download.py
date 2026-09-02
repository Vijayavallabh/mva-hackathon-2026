#!/usr/bin/env python3
"""Resumable bounded-range downloader for large public reference archives."""

from __future__ import annotations

import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import urllib.request


def remote_size(url: str) -> int:
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request) as response:
        return int(response.headers["Content-Length"])


def fetch_part(url: str, path: Path, start: int, end: int) -> None:
    expected = end - start + 1
    current = path.stat().st_size if path.exists() else 0
    if current == expected:
        return
    if current > expected:
        raise RuntimeError(f"oversized partial chunk: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as output:
        subprocess.run(
            [
                "curl",
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--retry",
                "8",
                "--range",
                f"{start + current}-{end}",
                url,
            ],
            check=True,
            stdout=output,
        )
    actual = path.stat().st_size
    if actual != expected:
        raise RuntimeError(f"chunk size mismatch for {path}: {actual}/{expected}")


def download(url: str, destination: Path, workers: int, chunk_size: int) -> None:
    size = remote_size(url)
    if destination.exists() and destination.stat().st_size == size:
        return
    parts = destination.with_name(destination.name + ".parts")
    parts.mkdir(parents=True, exist_ok=True)
    first_part = parts / "00000.part"
    if destination.exists() and not first_part.exists():
        if destination.stat().st_size > chunk_size:
            raise RuntimeError("existing partial is larger than one chunk")
        destination.replace(first_part)
    ranges = [
        (index, start, min(start + chunk_size, size) - 1)
        for index, start in enumerate(range(0, size, chunk_size))
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(fetch_part, url, parts / f"{index:05d}.part", start, end)
            for index, start, end in ranges
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    assembling = destination.with_name(destination.name + ".assembling")
    with assembling.open("wb") as output:
        for index, start, end in ranges:
            part = parts / f"{index:05d}.part"
            with part.open("rb") as source:
                while block := source.read(16 * 1024 * 1024):
                    output.write(block)
    if assembling.stat().st_size != size:
        raise RuntimeError("assembled download has the wrong size")
    os.replace(assembling, destination)
    for part in parts.iterdir():
        part.unlink()
    parts.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("destination", type=Path)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--chunk-size", type=int, default=1024**3)
    args = parser.parse_args()
    download(args.url, args.destination, args.workers, args.chunk_size)


if __name__ == "__main__":
    main()
