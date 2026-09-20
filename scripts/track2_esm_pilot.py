#!/usr/bin/env python3
"""Bounded public-reference ESM-1v pilot. Run from an isolated uv environment."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import time
import urllib.request

MODEL = "esm1v_t33_650M_UR90S_1"
URL = f"https://dl.fbaipublicfiles.com/fair-esm/models/{MODEL}.pt"
EXPECTED_BYTES = 7_828_635_339  # Official upstream HEAD, 2026-09-20; full checkpoint.


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    with Path(path).open("x") as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write("\n")


def parse_variant(variant, sequence):
    m = re.fullmatch(r"([ACDEFGHIKLMNPQRSTVWY])([1-9][0-9]*)([ACDEFGHIKLMNPQRSTVWY])", variant)
    if not m:
        raise ValueError("Expected a single amino-acid substitution")
    ref, pos, alt = m.group(1), int(m.group(2)), m.group(3)
    if pos > len(sequence) or sequence[pos - 1] != ref or ref == alt:
        raise ValueError("Reference residue mismatch, position out of range, or identity substitution")
    return ref, pos, alt


def token_position(pos, start, end):
    if not 1 <= start <= pos <= end or end - start + 1 > 1022:
        raise ValueError("Position outside the bounded window")
    return pos - start + 1  # ESM prepends BOS; full protein positions are one-based.


def control_gate(rows):
    windows = sorted({r["window"] for r in rows})
    result = {}
    for window in windows:
        selected = [r for r in rows if r["window"] == window]
        retained = [r["score"] for r in selected if r["group"] == "primary_retained"]
        impaired = [r["score"] for r in selected if r["group"] == "primary_impaired"]
        if len(retained) != 1 or len(impaired) != 3 or not all(map(math.isfinite, retained + impaired)):
            raise ValueError("Incomplete or nonfinite primary controls")
        gap = retained[0] - max(impaired)
        result[window] = {"retained_minus_highest_impaired": gap, "pass": gap > 0,
                          "correct_pairwise_orderings": sum(retained[0] > x for x in impaired),
                          "comparisons": len(impaired)}
    if len(windows) != 3:
        raise ValueError("Expected all three prespecified windows")
    return {"windows": result, "pass": all(x["pass"] for x in result.values())}


def fetch_model(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    checkpoint = directory / f"{MODEL}.pt"
    manifest = directory / "model.json"
    if manifest.exists():
        metadata = json.loads(manifest.read_text())
        if metadata["url"] != URL or metadata["sha256"] != digest(checkpoint):
            raise ValueError("Existing checkpoint does not match retrieval manifest")
        print(json.dumps(metadata), flush=True)
        return
    partial = checkpoint.with_suffix(".part")
    started = time.monotonic()
    size = 0
    with urllib.request.urlopen(URL, timeout=90) as response, partial.open("xb") as out:
        if int(response.headers.get("Content-Length", "0")) != EXPECTED_BYTES:
            raise ValueError("Official checkpoint size changed; review before fetching")
        while chunk := response.read(8 * 1024 * 1024):
            size += len(chunk)
            if size > EXPECTED_BYTES or time.monotonic() - started > 1200:
                raise ValueError("Checkpoint download exceeded bounded size or time")
            out.write(chunk)
    if size != EXPECTED_BYTES:
        raise ValueError("Unexpected checkpoint size")
    if checkpoint.exists():
        raise FileExistsError(checkpoint)
    partial.rename(checkpoint)
    metadata = {"model": MODEL, "url": URL, "bytes": size, "sha256": digest(checkpoint),
                "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                "trust": "Official upstream HTTPS checkpoint; digest records received bytes, not an independent signature"}
    write_json(manifest, metadata)
    print(json.dumps(metadata), flush=True)


def run(plan_path, fasta_path, weights, out_path):
    import os
    import platform
    import subprocess
    import esm
    import numpy as np
    import torch

    plan_path, fasta_path, weights, out_path = map(Path, (plan_path, fasta_path, weights, out_path))
    plan = json.loads(plan_path.read_text())
    text = fasta_path.read_text()
    if not text.startswith(">sp|O60566|") or text.count(">") != 1:
        raise ValueError("Expected the single public UniProt reference record")
    sequence = "".join(text.splitlines()[1:]).strip()
    if len(sequence) != plan["reference_length"] or plan["model"] != MODEL:
        raise ValueError("Unexpected reference length or model")
    if digest(fasta_path) != plan["reference_fasta_sha256"]:
        raise ValueError("Public reference does not match the prespecified digest")
    metadata = json.loads((weights / "model.json").read_text())
    checkpoint = weights / f"{MODEL}.pt"
    if metadata["url"] != URL or digest(checkpoint) != metadata["sha256"]:
        raise ValueError("Checkpoint integrity mismatch")
    for row in plan["controls"]:
        parse_variant(row["variant"], sequence)
    parse_variant(plan["candidate"], sequence)
    if len(plan["windows"]) != 3:
        raise ValueError("Expected three windows")
    if torch.cuda.device_count() != 1:
        raise ValueError("Expose exactly one selected GPU")
    out_path.mkdir(exist_ok=False)
    started = time.monotonic()
    torch.manual_seed(0)
    np.random.seed(0)
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model, alphabet = esm.pretrained.load_model_and_alphabet_local(str(checkpoint))
    model.eval().cuda()
    converter = alphabet.get_batch_converter()
    cached = {}

    @torch.inference_mode()
    def distribution(window, pos, repeat=False):
        start, end = window["start"], window["end"]
        index = token_position(pos, start, end)
        key = (start, end, pos)
        if repeat or key not in cached:
            _, _, tokens = converter([("public_BUBR1", sequence[start - 1:end])])
            tokens[0, index] = alphabet.mask_idx
            logits = model(tokens.cuda(), return_contacts=False)["logits"]
            values = torch.log_softmax(logits[0, index].float(), dim=-1).cpu()
            if repeat:
                return values
            cached[key] = values
        return cached[key]

    def score_variant(window, variant, group):
        ref, pos, alt = parse_variant(variant, sequence)
        values = distribution(window, pos)
        return {"window": window["name"], "variant": variant, "group": group,
                "score": float(values[alphabet.get_idx(alt)] - values[alphabet.get_idx(ref)])}

    rows = [score_variant(w, c["variant"], c["group"])
            for w in plan["windows"] for c in plan["controls"]]
    repeat = distribution(plan["windows"][0], 882, repeat=True)
    difference = float((repeat - distribution(plan["windows"][0], 882)).abs().max())
    gate = control_gate(rows)
    gate["repeat_max_abs_difference"] = difference
    gate["numerical_pass"] = math.isfinite(difference) and difference <= 1e-6
    gate["pass"] = gate["pass"] and gate["numerical_pass"]
    # Persist the control adjudication before any candidate inference.
    write_json(out_path / "controls.json", {"rows": rows, "gate": gate})
    candidate = ([score_variant(w, plan["candidate"], "candidate") for w in plan["windows"]]
                 if gate["pass"] else [])
    torch.cuda.synchronize()
    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "model": MODEL,
        "plan_sha256": digest(plan_path), "script_sha256": digest(__file__),
        "reference_sha256": digest(fasta_path), "reference_length": len(sequence),
        "checkpoint": metadata, "gate": gate,
        "candidate_inference_performed": bool(candidate), "candidate_scores": candidate,
        "decision": "exploratory_candidate_scores_only" if gate["pass"] else "stop_unqualified_model",
        "elapsed_seconds": time.monotonic() - started,
        "peak_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
        "peak_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
        "gpu": torch.cuda.get_device_name(0), "visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "python": platform.python_version(), "torch": torch.__version__, "esm": esm.__version__,
        "cuda_runtime": torch.version.cuda, "cwd": str(Path.cwd()),
        "driver": subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"], text=True).splitlines()[0],
        "clinical_inference": False, "drug_ranking_changed": False, "phase_resolved": False,
        "limitations": plan["limitations"],
    }
    write_json(out_path / "summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch-model")
    fetch.add_argument("directory")
    score = sub.add_parser("run")
    score.add_argument("--plan", required=True)
    score.add_argument("--fasta", required=True)
    score.add_argument("--weights", required=True)
    score.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.command == "fetch-model":
        fetch_model(args.directory)
    else:
        run(args.plan, args.fasta, args.weights, args.out)


if __name__ == "__main__":
    main()
