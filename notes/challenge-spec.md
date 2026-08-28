# Challenge specification — read off the published code, 2026-08-28

Everything here comes from **public** sources: the challenge Space's own source at
`SageBio/rare-disease-real-kid-mva-hackathon-2026` (`evaluation.py`, `groundtruth.py`,
`config.py`, `tabs/submit_track1.py`, `tabs/rules.py`, `tabs/faq.py`, `tabs/about.py`) and
the public dataset README. No subject data is involved and this file is safe to publish.

The point of writing it down: two of these details silently score **zero** if got wrong,
and there are only 6 attempts.

---

## 1. Two traps that cost the entire score

**Contig naming.** The submission template is `chr1,100000,A,T`. `evaluation.py` matches
with exact tuple equality on `(chrom, pos, ref, alt)` and only `.strip()`s `chrom` — it
never normalizes it. **Our VCF is unprefixed (`1`, `2`, `X`).** Submitting VCF coordinates
straight through matches nothing and scores 0 while looking perfectly well-formed.

**Proband ID.** Must be exactly **`PROBAND01`**. The app rejects anything else with
"Unknown proband_id … Only PROBAND01 is accepted in this challenge". It is *not* the sample
name `WGS_EX2312012` that appears throughout the data files.

Also normalized by the scorer: `pos` → `int`, `ref`/`alt` → `.strip().upper()`.
Indel representation is **not** normalized — left-alignment must match the answer key.

## 2. Submission schema

`proband_id, chrom_1, pos_1, ref_1, alt_1, chrom_2, pos_2, ref_2, alt_2, epcr, finding_type, notes`

- One row per proposed causal variant **or compound-het pair**. `*_2` blank for singles.
- `epcr` ∈ (0, 1] — validated, out-of-range raises.
- `finding_type` ∈ {`primary`, `secondary`} — validated but **informational only**, it does
  not enter the score.
- `notes` is free text and is not read by the scorer.
- **Maximum 10 rows** per proband; more raises.
- GRCh38 coordinates.
- Filename should carry the HF username and a short method name,
  e.g. `jvv7_vep-comphet.csv`.

## 3. The answer key is a compound-heterozygous pair

`evaluation.py`'s own docstring: *"simplified for a single proband ('N-of-1') with a
**clinically validated compound-heterozygous answer key**"*. The FAQ and the About page
both describe half credit "if you recover only one of two compound-heterozygous variants",
and `groundtruth.py`'s dev fallback holds two variants.

Combined with the measured absence of any ROH (`data-profile.md` §2), the working model is
**two different rare damaging alleles in one gene**, not a homozygote.

## 4. How the two metrics actually behave

**Rank points.** Rows are sorted by `epcr` descending (ties broken by file order) before
scoring. Points come from the rank of the *first row whose variant set exactly equals* the
true set:

| rank | 1 | 2–3 | 4–5 | 6–10 | >10 |
|---|---|---|---|---|---|
| points | 100 | 50 | 25 | 10 | 0 |

If no row matches fully, a row sharing **one** of the two true variants scores
`0.5 ×` the tier for its rank.

**F-max.** Sweeps every distinct `epcr` value as a threshold. At threshold `t`, the
prediction set is the **union of variants across all rows with `epcr ≥ t`**; precision and
recall are computed against the true set at the level of individual variants, and F-max is
the best F over all thresholds.

**Strategy that falls out of this:**

- Put the best compound-het **pair in a single row at the top**. A row holding exactly the
  two true variants gives F = 1.0 at its own threshold. Splitting the pair across two rows
  can only reach F = 1.0 if nothing false outranks them.
- **Rows with `epcr` below the true row are free.** F-max is a maximum, so they cannot lower
  it, and rank points depend only on position. Confirmed by the FAQ: secondary and
  incidental findings "won't hurt your automated score". **Fill all 10 rows.**
- **Rows with `epcr` above the true row are the only thing that costs points** — each one
  pushes the true row down a tier.
- **Use strictly distinct `epcr` values.** Ties collapse thresholds and remove sweep points
  that F-max could otherwise have used.

## 5. Submission logistics

- **Track 1: 6 submissions** per participant; highest score counts. Each upload requires
  **all three** of: the CSV, a report file (`.pdf` or `.md`), and a GitHub URL that starts
  with `https://github.com/`. → the repo must be public before the first submission (feat-007).
- **Track 2: 1 submission**, no re-submissions. Report + GitHub link + 3-minute recorded
  pitch video. Judged on rigor 35% / impact 25% / innovation 25% / scalability 15%.
- Teams: each member registers individually and gets their own Track 1 quota; one Track 2
  submission per team.
- Judging runs ~2–3 months after the 2026-10-24 close.
- Prize pool $50,000 (AWS Imagine Grant + Anthropic).

## 6. Rules that bind our working practice

- *"You will not release or otherwise grant data access to anyone, and you will establish
  appropriate safeguards to prevent unauthorized data use."*
- *"No data may be reshared through any channel."*
- *"All data must be deleted within 30 days of Hackathon close from all environments (local
  machines, cloud instances, notebooks, private repos, and any intermediate or derived
  datasets)"*, then confirmed by email.
- *"Participants are free to publicly share their code, models, and derived outputs at any
  time."* — this is the basis for what `AGENTS.md` rule 1 permits.
- Embargo on peer-reviewed manuscripts until the organizers publish their summary report.
- Submissions are CC-BY 4.0 and may be rerun by the organizers.
- Publications must not include information that could re-identify the subject or family
  "beyond what redacted redacted redacted redacted redacted redacted redacted'redacted own blog posts".

## 7. Publicly stated clinical context

From the About page: the child lives with Mosaic Variegated Aneuploidy, there is no
established treatment, and **"Care today means managing symptoms and fighting cancer cells."**

Cancer predisposition is therefore part of the stated presentation. That is the canonical
BUB1B/MVA1 phenotype and should anchor the Track 2 mechanism argument — but see
`prior-knowledge.md`: it is a prior, not a finding, and the phenotype document itself names
no gene.

The rules also say raw data is available "optionally in BAM/CRAM" — **none was shipped**.
We have FASTQ and a germline VCF only.
