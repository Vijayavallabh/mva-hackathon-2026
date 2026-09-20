# Track 2: public-reference ESM control pilot

2026-09-20 · Session 51 · Owner-authorized remote computation under `~/v`.

**Completed:** the prespecified primary control gate passed in all three windows,
then the candidate was scored. ESM-1v checkpoint 1 gave p.Asn1002Lys positive
alternate-versus-reference log scores in every window. This particular model
therefore supplies no sequence-incompatibility support for a damaging interpretation.
It does **not** establish normal BUBR1 function or clinical benignity. A secondary
control exposes a limitation of the passing primary gate. No drug, genetic
classification, phase or exposure conclusion was promoted.

## Results and decisions

Scores below are natural-log masked residue-probability differences, rounded to
three decimals. Higher means more sequence-compatible according to this model;
it does not mean better biological function. Full precision and input/runtime
provenance are in [the result record](track2-esm-pilot-results.json).

| Substitution | Role | 1–1022 | 29–1050 | 721–1044 |
| --- | --- | ---: | ---: | ---: |
| V793R | Primary impaired | -3.375 | -3.346 | -2.885 |
| K795R | Primary impaired | -2.050 | -2.178 | -2.597 |
| D911N | Primary impaired | -1.189 | -1.252 | -1.800 |
| D882N | Primary assay-retaining | -0.215 | 0.004 | -0.469 |
| K795A | Secondary impaired | -2.400 | -3.165 | -3.444 |
| D882A | Secondary assay-retaining | -1.555 | -1.247 | -2.727 |
| N1002K | Candidate, scored after gate | **0.709** | **0.586** | **0.483** |

The primary ordering margin was positive in each context: 0.974, 1.256 and
1.331 respectively. Repeated inference differed by 0.0 in the checked masked
distribution. These repeated/contextual comparisons are not independent
biological samples, and their count is not a probability of model correctness.

**The important countercheck is D882A.** Despite its reported retained function,
it scored below D911N in two windows and below K795R in the domain-only window.
It was prospectively secondary, so the registered primary gate correctly remains
"pass"; nevertheless, it limits any claim that scores discriminate BUBR1 functional
states reliably. Do not hide it, relabel the gate or derive a clinical threshold
from this small experiment.

For Track 2, the result strengthens the need to **measure** the missense allele's
abundance and function and maintain the separate allele/phase controls already
specified in v10. A sequence model can challenge an assumed mechanism without
establishing an alternative diagnosis. The stop-gain is not addressed by this
substitution model. Existing favorable or unfavorable predictors must remain
visible; this single model is not an independent clinical adjudicator. The
owner-reported Track 1 score and the submitted v4 files are unaffected.

No large screen or structural campaign was launched. Passing the minimal gate
allowed the declared candidate scoring, but the secondary discrepancy and lack
of a validated drug-response link do not justify eight-GPU expansion. A later
cross-check would need a new fixed question/design; do not change checkpoints
until they agree with a favored conclusion. Everolimus stays an optional
model-qualified mechanistic probe, HCQ reserve, with no rescue-priority drug.

The scoring process completed with exit 0. Timed model loading/scoring after the
initial checkpoint hash took **10.48 seconds**, with **2.72 GiB peak PyTorch tensor
allocation** (2.79 GiB reserved). These figures exclude installation, download,
initial checksum time and non-PyTorch memory; they are not a speedup benchmark.
GPU 4 returned to 1 MiB/0% utilization after completion. No GPU job from this
pilot remains running. Local checks matched seven preregistered input hashes,
recomputed the control gate and confirmed the candidate ran only after a pass.

## Question and prespecified design

Can a fixed protein-language-model baseline order experimentally impaired BUBR1
substitutions below an assay-retaining substitution, before we interpret a score
for p.Asn1002Lys? This tests whether the proposed computation deserves further
resources. It does not estimate drug response, clinical pathogenicity or phase.

The [fixed plan](track2-esm-pilot-plan.json) uses ESM-1v checkpoint 1, masked
alternate-minus-reference log probabilities and three predetermined contexts:
residues 1–1022, 29–1050 and the published recombinant-domain interval 721–1044.
The full reference is 1,050 residues; no silent truncation is allowed. Each
substitution is checked against public UniProt O60566 before inference.

The primary challenge compares V793R, K795R and D911N against D882N. The former
showed functional defects in the cited reconstitution experiments; D882N retained
the measured functions. K795A and D882A are additional contextual checks and do
not determine the gate. These are assay-specific labels, not clinical variant
classifications. Source: [Suijkerbuijk et al., 2012](https://doi.org/10.1016/j.devcel.2012.03.009),
main text around Figure 3 and its legend. D882A's supplementary result was read
through the main-text account; the supplement was not independently reviewed.

D882N must score strictly above all three primary impaired controls in **every**
window. A repeated inference must agree within 1e-6. This intentionally conservative
allocation rule was fixed before scores; it is not a validated diagnostic cutoff.
The code persists the control decision before allowing any candidate inference.
Failed controls stop candidate scoring and structure/model escalation. No checkpoint
or context substitution is permitted merely to obtain a pass.

The control set is small, selected and from one study, with one primary retaining
site. It is not a clinical validation set or a powered benchmark. Reconstitution
in cancer cell backgrounds does not model the selected pair in deficient normal
tissue. The same-site secondary substitutions are not independent evidence.
Agreement could reuse evolutionary information already reflected in other
predictors. Disagreement would disqualify this planned inference route, not prove
the candidate harmless, invalidate the experiments or rule out all useful models.

## Execution and provenance

Key-based SSH succeeded using the owner's supplied host. No password was saved.
All new remote files, managed Python, environment, model weights, compiler/cache
paths, temporary files and logs are confined to:

`PrakashDGX_H2:~/v/mva-track2-pilot-20260920/`

The host exposes eight H100 80 GB GPUs. At first inspection GPUs 0–3 were busy
and 4–7 idle. The runner requires GPU 4 to have at most 1,000 MiB occupied and
at most 5% utilization, then exposes only that GPU to PyTorch. No other job was
terminated or altered. Remote resource detection reported 192 logical CPUs,
about 982 GiB available RAM and 839 GiB available disk after environment setup.

Driver 555.42.02 does not meet the reviewed Anthropic kits' driver floors, so this
pilot uses **upstream fair-esm 2.0.0**, PyTorch 2.5.1+cu124 and a uv-managed Python
3.11 environment. No Anthropic optimization was installed or benchmarked; this is
not a stock-versus-exact comparison. No system package or driver was changed.
The [environment definition](../scripts/track2_esm_environment.toml) and
[resolved lock](../scripts/track2_esm_pilot.uv.lock) reproduce the package set.

The official full ESM checkpoint is 7,828,635,339 bytes. The first bounded fetch
stopped at an incorrectly small 3.5 GB cap. A read-only upstream HEAD established
the size; a separate `cache/weights-v2/` download then passed an exact size check.
The failed partial file and log remain recorded in the first directory. This was
an infrastructure correction before inference, not a changed scientific rule.
Checkpoint SHA-256:
`9519ee60f1cddad3c101afb1f42612499e188534969c3f682e94850870f70433`.
The checksum identifies received upstream bytes; it is not an independent signature.

Public reference FASTA SHA-256:
`4ac6895daf90501d8398d17ded42f46d78b9db777f5084facc875c2926496d1b`.
Plan SHA-256:
`fbd5d8dcdf51bc19b5f2735374dd66619fe1a1c7cac7b633330d77cde533d9e7`.
Inference script SHA-256:
`d2ed238d66d851f44ef5129ae9ad6b3f1e9a1de366f8ea8ce972950e2611715c`.
Lock SHA-256:
`2561e2223198cbd20df2f1bd0128d59b27c6166134efe598dce7ed7ed7611990`.
`outputs/preregistration.json` records the plan, reference, code, launcher,
environment and lock hashes before inference, alongside the GPU availability check.

Public reference/source retrievals are archived locally in
`results/feat009/model-pilot-public-v1/`, with URL/hash manifest `sources.json`.
The 2012 author-hosted PDF was retrieved successfully. An attempted Europe PMC
XML retrieval for the separate 2010 paper returned HTTP 500, while browser PMC
access hit a challenge page; it was not used to define the controls. No automated
access restriction was bypassed.

Only explicitly selected public code, a public reference FASTA and the permitted
derived candidate substitution were copied. No repository-wide synchronization,
raw subject file, VCF record, clinical narrative, project `.env` or API key was sent.
The inference is local to the owner-authorized SSH host using Meta's downloaded
ESM weights; no hosted inference provider was called. Future submission disclosure
must include this computation. The existing immutable v12 package is preserved.

## Reproduction and checks

Copy the environment TOML to `pyproject.toml`, its lock to `uv.lock`, and the three
pilot/launcher/environment scripts into `scripts/` in a fresh private directory
under `~/v/mva-track2-pilot-*`. Copy the fixed plan and the hash-verified public
[UniProt FASTA](https://rest.uniprot.org/uniprotkb/O60566.fasta) into `inputs/`.
Create `cache/`, `python/`, `tmp/`, `logs/` and `outputs/`, then run from that directory:

```bash
source scripts/track2_esm_remote_env.sh
/home/prachh/v/bin/uv sync --frozen --python 3.11.16 --managed-python
/home/prachh/v/bin/uv run --frozen python scripts/track2_esm_pilot.py fetch-model cache/weights-v2
nohup bash scripts/run_track2_esm_pilot.sh > logs/inference.log 2>&1 < /dev/null &
```

The runner is explicitly configured for physical GPU 4 on this host and refuses
an occupied device; do not silently change it during a running job. Fetching uses
the official upstream HTTPS checkpoint. Loading uses fair-esm's upstream loader
in the isolated environment. Inference itself uses local files. Preserve output
directories; each new attempt needs a new directory and its own preregistration.

Ten new tests cover reference-residue mismatches, numbering/BOS offsets, oversized
windows, missing/nonfinite controls, score direction, ties and stopping when any
window fails. The complete Track 2 suite passed 499 tests. Core checks and fresh
`./init.sh` passed. V12 verification confirms eight files/119 bound inputs and
preserves v1–v11. Tests establish implementation checks, not biological validity.

The remote directory and any local result copies belong in the project's deletion
inventory for 2026-11-24. Keep all source, failed-download, environment, runtime
and control-result records until then. No raw subject data is present on the host.
