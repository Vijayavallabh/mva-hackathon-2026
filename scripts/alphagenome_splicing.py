#!/usr/bin/env python3
"""Offline public Atlas archive validation and fixed submission-derived lookups.

Never reads a subject VCF, sequences, narrative or .env; never makes a network call.
ZIP members are copied explicitly, not extractall(), and no existing output is reused.
"""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import shutil
import stat
import struct
import subprocess
import tempfile
import zipfile
import zlib

from alphagenome_atlas import ROOT, CONTROL, SUBMITTED, submitted_preflight

DATA = "combined_alphagenome_splicing_snvs.tsv.gz"
INDEX = DATA + ".tbi"
MEMBERS = (DATA, INDEX)
HEADER = "#CHROM\tPOS\tREF\tALT\talphagenome_splicing"
BGZF_EOF = bytes.fromhex("1f8b08040000000000ff0600424302001b0003000000000000000000")
TABIX = ROOT / "tools/install/bin/tabix"
LIMITS = {DATA: 30_000_000_000, INDEX: 10_000_000}
CHUNK = 8 * 1024 * 1024


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write("\n")
    temporary.replace(path)


def identity(path):
    s = path.stat()
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def validate_members(infos):
    require(len(infos) == 2 and {i.filename for i in infos} == set(MEMBERS), "ZIP member set mismatch")
    for i in infos:
        mode = i.external_attr >> 16
        require(not stat.S_ISLNK(mode) and not i.is_dir(), "ZIP non-regular member")
        require(stat.S_IFMT(mode) in (0, stat.S_IFREG), "ZIP special member")
        require(i.flag_bits & 1 == 0, "encrypted ZIP member")
        require(i.compress_type == zipfile.ZIP_STORED and i.compress_size == i.file_size,
                "unexpected ZIP compression; inspect new artifact explicitly")
        require(0 < i.file_size <= LIMITS[i.filename], "ZIP member size outside declared bounds")


def bgzf_check(path):
    with path.open("rb") as f:
        prefix = f.read(18)
        require(prefix[:4] == b"\x1f\x8b\x08\x04" and prefix[12:16] == b"BC\x02\x00", "BGZF header mismatch")
        f.seek(-28, os.SEEK_END)
        require(f.read() == BGZF_EOF, "BGZF EOF marker missing")


def index_header(path):
    bgzf_check(path)
    with gzip.open(path, "rb") as f:
        header = f.read(36)
        require(len(header) == 36 and header[:4] == b"TBI\x01", "invalid Tabix magic")
        n_ref, fmt, seq, begin, end, meta, skip, n_names = struct.unpack("<8i", header[4:])
        require(0 < n_ref < 10000 and 0 < n_names < 1000000, "Tabix name table bounds")
        raw = f.read(n_names)
    require(len(raw) == n_names and raw.endswith(b"\0"), "Tabix name table truncated")
    names = raw[:-1].decode("ascii").split("\0")
    require(len(names) == n_ref and len(set(names)) == n_ref, "Tabix contig names mismatch")
    # Provider used Tabix's VCF preset (2), despite this being a five-column
    # reference-prediction TSV, not a subject VCF. SNVs remain 1-based points.
    require((fmt, seq, begin, end, meta, skip) == (2, 1, 2, 0, 35, 0), "Tabix coordinate/schema mismatch")
    return {"format": fmt, "coordinate_convention": "1-based point", "sequence_column": seq,
            "begin_column": begin, "end_column": end, "meta_character": "#", "contigs": names}


def prepare(archive, output):
    require(archive.is_file() and not archive.is_symlink(), "ZIP must be a regular non-symlink file")
    require(not output.exists(), "prepare output already exists")
    original = identity(archive)
    with zipfile.ZipFile(archive) as z:
        validate_members(z.infolist())
        required = sum(i.file_size for i in z.infolist()) + 1024**3
    require(shutil.disk_usage(output.parent).free > required, "insufficient extraction headroom")
    output.mkdir()
    manifest = {"state": "started", "created_at": now(), "archive_path": str(archive),
                "archive_size": original[2], "publisher_checksum_verified": False,
                "script_sha256": digest(Path(__file__)), "members": {}}
    save(output / "manifest.json", manifest)
    try:
        manifest["archive_sha256"] = digest(archive)
        save(output / "manifest.json", manifest)
        with zipfile.ZipFile(archive) as z:
            validate_members(z.infolist())
            for info in z.infolist():
                sha, crc, total = hashlib.sha256(), 0, 0
                partial = output / (info.filename + ".partial")
                with z.open(info) as source, partial.open("xb") as target:
                    while block := source.read(CHUNK):
                        total += len(block)
                        require(total <= info.file_size, "ZIP expanded beyond declared size")
                        target.write(block)
                        sha.update(block)
                        crc = zlib.crc32(block, crc)
                require(total == info.file_size and crc == info.CRC, "ZIP member size/CRC mismatch")
                partial.rename(output / info.filename)
                manifest["members"][info.filename] = {"size": total, "sha256": sha.hexdigest(),
                    "zip_crc32": f"{crc:08x}", "crc_verified": True}
                save(output / "manifest.json", manifest)
        require(identity(archive) == original, "ZIP changed during verification")
        bgzf_check(output / DATA)
        with gzip.open(output / DATA, "rt", encoding="ascii") as f:
            require(f.readline(4096).rstrip("\n") == HEADER, "TSV header mismatch")
        manifest["index"] = index_header(output / INDEX)
        manifest.update(state="prepared", completed_at=now(),
            integrity_scope="Full ZIP SHA-256 and both member CRC/SHA-256; BGZF endpoints; no whole-table inflation")
        save(output / "manifest.json", manifest)
        return manifest
    except Exception as error:
        manifest.update(state="failed", completed_at=now(), error_type=type(error).__name__)
        save(output / "manifest.json", manifest)
        raise


def verify_prepared(cache):
    manifest = json.loads((cache / "manifest.json").read_text())
    require(manifest.get("state") == "prepared", "cache is not prepared")
    require(set(manifest["members"]) == set(MEMBERS), "manifest member set mismatch")
    for name in MEMBERS:
        p = cache / name
        item = manifest["members"][name]
        require(p.is_file() and not p.is_symlink(), "cache member missing or symlink")
        before = identity(p)
        require(before[2] == item["size"] and digest(p) == item["sha256"], "cache hash mismatch")
        require(identity(p) == before, "cache changed during verification")
    require(index_header(cache / INDEX) == manifest["index"], "cache index metadata changed")
    return manifest


def parse_rows(text, variant):
    chrom, pos, ref, alt = variant
    lines = text.splitlines()
    require(lines and lines[0] == HEADER, "query header missing or changed")
    require(len(lines) <= 4, "too many records for an SNV position")
    rows, seen = [], set()
    for line in lines[1:]:
        cells = line.split("\t")
        require(len(cells) == 5, "row field count mismatch")
        c, p, r, a, score_text = cells
        require(c == chrom and p == str(pos) and r == ref, "row identity/coordinate/REF mismatch")
        require(a in "ACGT" and len(a) == 1 and a != ref and a not in seen, "ALT invalid or duplicate")
        seen.add(a)
        score = float(score_text)
        require(math.isfinite(score) and score >= 0, "merged score invalid; missing is not zero")
        rows.append({"chromosome": c, "position": pos, "reference": r, "alternate": a,
                     "merged_splicing_score": score, "score_text": score_text})
    chosen = next((r for r in rows if r["alternate"] == alt), None)
    return {"variant": variant, "state": "found" if chosen else "missing",
            "merged_splicing_score": None if chosen is None else chosen["merged_splicing_score"],
            "score_text": None if chosen is None else chosen["score_text"],
            "all_alternate_rows": rows, "all_three_alternates_present": len(rows) == 3,
            "interpretation": "Uncalibrated aggregate model score; not AVI, PHRED, disease probability or phase"}


def run_tabix(command, limit=65536, timeout=30):
    """Bound native output before buffering it; this CLI runs on Linux, one thread."""
    def child_limits():
        resource.setrlimit(resource.RLIMIT_FSIZE, (limit + 1, limit + 1))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        run = subprocess.run(command, stdout=out, stderr=err, timeout=timeout,
                             preexec_fn=child_limits)
        out.seek(0)
        err.seek(0)
        body, errors = out.read(limit + 1), err.read(limit + 1)
    require(run.returncode == 0 and not errors.strip(), "Tabix failed or emitted a warning")
    require(len(body) <= limit, "Tabix output exceeds point-query bound")
    return body.decode("ascii")


def query(cache, output):
    require(not output.exists(), "query output already exists")
    output.mkdir()
    result = {"state": "started", "created_at": now(), "script_sha256": digest(Path(__file__)),
              "request_scope": [CONTROL, *SUBMITTED], "rows": [], "network_calls": 0,
              "source_vcf_read": False, "phase": "unconfirmed"}
    save(output / "scores.json", result)
    try:
        manifest = verify_prepared(cache)
        result["preflight"] = submitted_preflight()
        result["source"] = {"cache_manifest_sha256": digest(cache / "manifest.json"),
                            "archive_sha256": manifest["archive_sha256"], "members": manifest["members"]}
        result["tabix_version"] = subprocess.check_output([str(TABIX), "--version"], text=True).strip()
        for variant in (CONTROL, *SUBMITTED):
            chrom, pos, _, _ = variant
            require(chrom in manifest["index"]["contigs"], "query contig absent from index")
            command = [str(TABIX), "-h", str(cache / DATA), f"{chrom}:{pos}-{pos}"]
            row = parse_rows(run_tabix(command), variant)
            row["command"] = command
            result["rows"].append(row)
            save(output / "scores.json", result)
        result.update(state="complete" if all(r["state"] == "found" for r in result["rows"]) else "partial",
                      completed_at=now())
        save(output / "scores.json", result)
        return result
    except Exception as error:
        result.update(state="failed", completed_at=now(), error_type=type(error).__name__)
        save(output / "scores.json", result)
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("prepare", "query", "verify"))
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path, nargs="?")
    args = p.parse_args()
    source = args.input.absolute()
    require(not source.is_symlink(), "input symlink refused")
    source = source.resolve()
    require(source.is_relative_to(ROOT / "data/resources"), "input must be under local data/resources")
    if args.command == "verify":
        require(args.output is None, "verify takes no output")
        result = verify_prepared(source)
    else:
        require(args.output is not None, "output required")
        output = args.output.resolve()
        base = ROOT / ("data/resources" if args.command == "prepare" else "results/feat009")
        require(output.is_relative_to(base) and output != base, "output outside allowed directory")
        result = prepare(source, output) if args.command == "prepare" else query(source, output)
    print(json.dumps({k: result[k] for k in ("state", "archive_sha256", "rows") if k in result}, indent=2))
    return 0 if result["state"] in ("complete", "prepared") else 2


if __name__ == "__main__":
    raise SystemExit(main())
