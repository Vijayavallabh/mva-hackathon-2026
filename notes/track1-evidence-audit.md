# Track 1 evidence audit (feat-006b)

## Scope and acceptance criteria

Requested 2026-09-08 after the owner asked whether local 100 rank points / 1.0
F-max guaranteed the competition result, then requested corrections including phase.
The review baseline is `608c1c6`. This is one bounded follow-up feature:

1. Provide a reproducible, prominently labelled score-scenario audit of the exact
   current submission. Actual competition scores must remain unknown without a
   receipt; assumed answers must never become evidence for causality.
2. Stress-test the existing genome-wide compound-pair ranking under declared
   phenotype/family weights and annotation ablations. Include every retained pair,
   not just the ten submitted genes. Report instability as well as stability.
   This is conditional sensitivity, not independent validation or probability.
3. Check native GT/PS and PGT/PID phase annotations in the original and recalled
   calls, with exact submitted-allele and sample matching. Do not emit records,
   phase-set identifiers, read names or non-submission variant details. A caller's
   encoded phase is not automatically verified biological phase.
4. Preserve existing package bytes. Do not submit, spend quota, invent a receipt,
   access the private key, contact the family, or upload raw data. Do not force a
   trans call or claim that all possible future phasing approaches are exhausted.
5. Add regression tests, run existing relevant checks and fresh `./init.sh`, record
   actual results, review the changes, and update the harness before handoff.

The current v4 CSV/report remain unchanged while owner-side upload status is unknown.
The public scorer is pinned; these checks do not replace live preflight or the
authenticated portal receipt.

## Phase interpretation references

GATK documents PGT as physical haplotype orientation and PID as a within-sample
phase-group identifier. They must be interpreted together, not compared across
samples or files. [GATK VCF documentation](https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format).

WhatsHap describes read-based phasing, disconnected phase sets, and long-read and
pedigree inputs. Existing disconnected evidence cannot be repaired by simply
relabelling two heterozygotes. [WhatsHap guide](https://whatshap.readthedocs.io/en/latest/guide.html).

## Results

### Score scenarios

`scripts/audit_track1_evidence.py scores` reports `actual_competition_score: null`,
`official_receipt_checked: false` and `guaranteed_perfect_score: false` before its
scenario list. These mean this audit has not established an actual score, not
that the owner has never submitted independently.

For the unchanged v4 CSV, 13 explicitly hypothetical cases include:

| Assumed private answer | Rank points | F-max |
|---|---:|---:|
| Submitted pair at rank 1 | 100 | 1.000 |
| Submitted pair at rank 2 | 50 | 0.667 |
| Submitted pair at rank 4 | 25 | 0.400 |
| Only one leading allele is true; its partner is not submitted | 50 | 0.500 |
| Neither true allele is submitted | 0 | 0.000 |

The audit uses the pinned scorer without accessing a private key. Unseen-truth
tokens exist only in memory and are explicitly non-genomic, not new variants.
The scenarios have no assigned probabilities. Strict CSV schema/EPCR validation
runs first; reference normalization remains the separate package check. Changing
EPCR magnitudes without changing order or ties cannot improve either metric.

### Ranking sensitivity

The input is **all 169 retained compound-pair hypotheses across 27 genes**, not
just the ten submitted rows or a BUB1B-only shortlist. This is the compound-pair
subset of feat-004's genome-wide filtered search, not an unfiltered whole-genome
reanalysis. All 169 pairs are reranked before reporting the leading pair's rank.

The declared grid contains 30 settings: proband weights 0/4/8/12/16, separate
family-history weights 0/0.5/2, and missing-frequency credit 0/1. Four additional
baseline-weight ablations remove computational-prediction bonuses, ClinVar
bonuses, both, or both plus missing-frequency credit. Other score components and
the retained variant universe are fixed. Pair-averaged bonuses follow the existing
ranker exactly; this does not reclassify ClinVar assertions.

- BUB1B's submitted pair ranks first in **26 of 34** settings, with no score tie.
- Its baseline margin over the best other pair is **1.405572 score units**.
- It remains first for proband weights 4–16 throughout the weight/missing-AF grid.
- At proband weight zero its rank becomes **13 or 17**, with ADAMTS1 first.
  Removing phenotype is an ablation control, not a recommended model.
- Removing only prediction bonuses or only ClinVar bonuses leaves BUB1B first,
  but reduces its margin to **0.405572**.
- Removing both makes its rank **12**; also removing missing-AF credit makes it
  **15**. HLA-DQA1 is first in those two settings, not thereby established causal.

Ranks are among pair hypotheses, not distinct genes. The grid is not randomly
sampled: **26/34 is not a probability or confidence estimate**. Scores derive
from rounded baseline output; ties within 1e-5 are exposed. This does not test
rejected variants, alternate transcripts, HPO annotation bias, new callers or
complete mechanism compatibility. No automatic reranking or EPCR recalibration
was justified by this conditional stress test.

### Additional phase evidence

The delivered source index had an older timestamp than its VCF. A fresh CSI was
generated under ignored `results/feat006b/` without changing the source or its
delivered index. All three checked files contain exactly one matching record for
each submitted allele:

| Input | Defined phase fields | Result for both submitted alleles |
|---|---|---|
| Original source VCF | GT, PGT, PID | Unphased; no populated PGT/PID pair |
| Raw HaplotypeCaller recall | GT | Unphased; no native phase-group annotation |
| Recalled-locus WhatsHap output | GT, PS | Unphased; no populated GT/PS pair |

Sample identity is explicit. Native group identifiers never leave the process.
Both GT/PS and PGT/PID require shared groups within one file/sample; conflicts are
flagged. HP is flagged for manual review rather than silently interpreted. The
audit conservatively does not assume shared chromosome-wide phase when PS is
absent. Even positive encoding requires caller/read evidence review before
biological confirmation. VCF provenance is size/mtime, not a full content hash;
the explicit fresh index and exact submitted CSV have SHA-256 provenance.

Together with feat-005c's zero connecting fragments and singleton target
components, native metadata supplies **no new cis or trans evidence**. Trans
remains unconfirmed; cis is not established either. Relabelling the same input
cannot manufacture missing linkage information.

## Reproduction

Run from the repository root. Outputs are aggregate JSON under ignored results.
Use a new output directory for a changed analysis; do not overwrite old evidence.

```bash
mkdir -p results/feat006b
task_csv_path=results/feat008/jvv7_genomewide_mva_v4/jvv7_genomewide_mva_v4.csv
uv run python scripts/test_track1_evidence.py
uv run python scripts/audit_track1_evidence.py scores "$task_csv_path" \
  > results/feat006b/score-scenarios.json
uv run python scripts/audit_track1_evidence.py ranking "$task_csv_path" \
  --candidates results/feat004/all_candidate_models.tsv \
  > results/feat006b/rank-sensitivity.json
tools/install/bin/bcftools index --csi \
  --output results/feat006b/source-fresh.csi data/WGS_EX2312012_HGWCNDSX7.vcf.gz
uv run python scripts/audit_track1_evidence.py phase "$task_csv_path" \
  --vcf data/WGS_EX2312012_HGWCNDSX7.vcf.gz --sample WGS_EX2312012 \
  --index results/feat006b/source-fresh.csi > results/feat006b/native-source-phase.json
uv run python scripts/audit_track1_evidence.py phase "$task_csv_path" \
  --vcf results/feat005b/haplotypecaller.raw.vcf.gz --sample PROBAND01 \
  > results/feat006b/native-recall-phase.json
uv run python scripts/audit_track1_evidence.py phase "$task_csv_path" \
  --vcf results/feat005c/hc-locus.phased.vcf.gz --sample PROBAND01 \
  > results/feat006b/whatshap-recall-phase.json
```

The index command refuses to overwrite an existing index. Reuse its recorded
artifact or choose a new output name on a later run.

## Next evidence needed, not promises

- **Actual score:** authenticated portal history/receipt for the exact file
  hashes. No upload or attempt was made by this audit. Obtain any existing receipt
  before considering another submission.
- **Phase:** additional authorized informative data, such as parental genotypes
  or long reads/linked observations connecting both sites directly or through
  a marker chain. Neither the recessive-disease prior nor statistical population
  phasing alone proves phase for this individual's rare pair. No family contact,
  specimen request, purchase or external transfer is authorized by this audit.
  A score matching the answer key is not experimental phase evidence from our work.
- **Biology:** independent evidence for the missense allele and mechanism-compatible
  alternatives. Not every possible existing-short-read analysis has been exhausted.

Implementation/harness guidance led to explicit unknown-score fields and a
reproducible companion command; critical-thinking guidance keeps sensitivity
distinct from calibration and confirmed phase. Existing v4 CSV/report hashes and
offline validity are unchanged. Verification/review evidence is in `progress.md`.
