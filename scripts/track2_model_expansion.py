#!/usr/bin/env python3
"""Fixed public-reference ESM ensemble/scale comparison; no clinical classifier."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics
import time
import urllib.request
from track2_esm_pilot import digest, parse_variant, token_position, control_gate, write_json

MODELS = [f"esm1v_t33_650M_UR90S_{n}" for n in range(1, 6)] + [
    "esm2_t36_3B_UR50D", "esm2_t48_15B_UR50D"]


def fetch(name, root):
    if name not in MODELS:
        raise ValueError("Unregistered model")
    root = Path(root) / name
    root.mkdir(parents=True, exist_ok=True)
    url = f"https://dl.fbaipublicfiles.com/fair-esm/models/{name}.pt"
    checkpoint = root / f"{name}.pt"
    if (root / "model.json").exists():
        manifest = json.loads((root / "model.json").read_text())
        if manifest["url"] != url or digest(checkpoint) != manifest["sha256"]:
            raise ValueError("Existing weight integrity mismatch")
        return
    with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=90) as r:
        size = int(r.headers["Content-Length"])
    if not 1_000_000_000 < size < 85_000_000_000:
        raise ValueError("Weight size outside the prespecified bound")
    started, received = time.monotonic(), 0
    partial = checkpoint.with_suffix(".part")
    with urllib.request.urlopen(url, timeout=120) as r, partial.open("xb") as f:
        if int(r.headers["Content-Length"]) != size:
            raise ValueError("HEAD/GET size mismatch")
        while chunk := r.read(8 * 1024 * 1024):
            received += len(chunk)
            if received > size or time.monotonic() - started > 7200:
                raise ValueError("Bounded download exceeded")
            f.write(chunk)
    if received != size or checkpoint.exists():
        raise ValueError("Incomplete download or existing destination")
    partial.rename(checkpoint)
    write_json(root / "model.json", dict(model=name, url=url, bytes=size,
        sha256=digest(checkpoint), retrieved_utc=datetime.now(timezone.utc).isoformat(),
        trust="Official HTTPS origin; digest describes received bytes, not an independent signature"))
    print(json.dumps({"downloaded": name, "bytes": size}), flush=True)


def run(name, plan_path, fasta_path, weight_root, out):
    import os
    import platform
    import esm
    import torch
    if name not in MODELS:
        raise ValueError("Unregistered model")
    plan = json.loads(Path(plan_path).read_text())
    fasta = Path(fasta_path).read_text()
    seq = "".join(fasta.splitlines()[1:]).strip()
    if (not fasta.startswith(">sp|O60566|") or fasta.count(">") != 1 or len(seq) != 1050
        or digest(fasta_path) != plan["reference_fasta_sha256"] or plan["models"] != MODELS):
        raise ValueError("Reference or fixed model list mismatch")
    weights = Path(weight_root) / name
    metadata = json.loads((weights / "model.json").read_text())
    checkpoint = weights / f"{name}.pt"
    if metadata["model"] != name or digest(checkpoint) != metadata["sha256"]:
        raise ValueError("Checkpoint integrity mismatch")
    variants = plan["controls"] + [{"variant": plan["candidate"], "group": "candidate"}]
    for row in variants:
        parse_variant(row["variant"], seq)
    if torch.cuda.device_count() != 1:
        raise ValueError("Expose one selected GPU per worker")
    out = Path(out); out.mkdir(exist_ok=False, parents=True)
    started = time.monotonic()
    torch.manual_seed(0); torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model, alphabet = esm.pretrained.load_model_and_alphabet_local(str(checkpoint))
    model.eval().cuda()  # All seven models use float32; no precision selection by result.
    converter = alphabet.get_batch_converter()
    cache = {}

    @torch.inference_mode()
    def distribution(window, pos, repeat=False):
        start, end = window["start"], window["end"]
        index = token_position(pos, start, end)
        key = (start, end, pos)
        if key not in cache or repeat:
            _, _, tokens = converter([("public_reference", seq[start-1:end])])
            if tokens[0, index].item() != alphabet.get_idx(seq[pos-1]):
                raise ValueError("Actual tokenizer reference coordinate mismatch")
            tokens[0, index] = alphabet.mask_idx
            logits = model(tokens.cuda(), return_contacts=False)["logits"]
            values = torch.log_softmax(logits[0, index].float(), -1).cpu()
            if repeat:
                return values
            cache[key] = values
        return cache[key]

    rows = []
    for window in plan["windows"]:
        for row in variants:
            ref, pos, alt = parse_variant(row["variant"], seq)
            values = distribution(window, pos)
            rows.append(dict(window=window["name"], variant=row["variant"], group=row["group"],
                score=float(values[alphabet.get_idx(alt)] - values[alphabet.get_idx(ref)])))
    repeat_delta = float((distribution(plan["windows"][0], 882, True) -
                          distribution(plan["windows"][0], 882)).abs().max())
    gate = control_gate([r for r in rows if r["group"] != "candidate"])
    gate["repeat_max_abs_difference"] = repeat_delta
    gate["numerical_pass"] = math.isfinite(repeat_delta) and repeat_delta <= 1e-6
    gate["pass"] = gate["pass"] and gate["numerical_pass"]
    torch.cuda.synchronize()
    result = dict(model=name, rows=rows, gate=gate, plan_sha256=digest(plan_path),
        script_sha256=digest(__file__), pilot_helpers_sha256=digest(Path(__file__).with_name("track2_esm_pilot.py")),
        fasta_sha256=digest(fasta_path), checkpoint=metadata,
        created_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-started,
        peak_allocated_gib=torch.cuda.max_memory_allocated()/1024**3,
        peak_reserved_gib=torch.cuda.max_memory_reserved()/1024**3,
        gpu=torch.cuda.get_device_name(0), visible_devices=os.environ.get("CUDA_VISIBLE_DEVICES"),
        python=platform.python_version(), torch=torch.__version__, esm=esm.__version__,
        precision="float32; TF32 disabled", candidate_is_diagnostic_even_if_gate_fails=True,
        clinical_classification=False, phase_resolved=False, drug_ranking_changed=False)
    write_json(out / "summary.json", result)
    print(json.dumps({k: result[k] for k in ["model", "gate", "elapsed_seconds", "peak_allocated_gib"]}), flush=True)


def aggregate(paths):
    runs = [json.loads(Path(p).read_text()) for p in paths]
    if sorted(r["model"] for r in runs) != sorted(MODELS):
        raise ValueError("Require exactly all seven registered models, including failures of the scientific gate")
    if len({r["plan_sha256"] for r in runs}) != 1 or len({r["script_sha256"] for r in runs}) != 1:
        raise ValueError("Mismatched plans or implementations")
    required = {(r["window"], r["variant"], r["group"]) for r in runs[0]["rows"]}
    if len(required) != 21:
        raise ValueError("Incomplete variant/window matrix")
    for run in runs:
        keys = [(r["window"], r["variant"], r["group"]) for r in run["rows"]]
        if len(keys) != 21 or set(keys) != required or not all(math.isfinite(r["score"]) for r in run["rows"]):
            raise ValueError("Missing, duplicated or nonfinite scores")
    ensemble = []
    for key in sorted(required):
        values = [r["score"] for run in runs if run["model"].startswith("esm1v_")
                  for r in run["rows"] if (r["window"], r["variant"], r["group"]) == key]
        ensemble.append(dict(window=key[0], variant=key[1], group=key[2], mean=statistics.mean(values),
            min=min(values), max=max(values), checkpoint_values=values))
    return dict(models=runs, esm1v_five_checkpoint_ensemble=ensemble,
        interpretation="Checkpoint ranges describe model sensitivity, not confidence intervals or independent biological replication",
        clinical_classification=False, drug_ranking_changed=False, phase_resolved=False)


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("model"); f.add_argument("root")
    r = sub.add_parser("run"); r.add_argument("model")
    for name in ["plan", "fasta", "weights", "out"]: r.add_argument("--"+name, required=True)
    a = sub.add_parser("aggregate"); a.add_argument("out"); a.add_argument("summaries", nargs="+")
    args = p.parse_args()
    if args.cmd == "fetch": fetch(args.model, args.root)
    elif args.cmd == "run": run(args.model, args.plan, args.fasta, args.weights, args.out)
    else: write_json(args.out, aggregate(args.summaries))


if __name__ == "__main__": main()
