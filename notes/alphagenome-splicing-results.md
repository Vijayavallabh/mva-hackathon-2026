# AlphaGenome merged splicing: verified local results

2026-09-09 IST, session 36, feat-009; baseline `25d8488`. The recorded processing
timestamps are 2026-09-08 UTC. Research only; no clinical recommendations.

## Outcome

**The owner-supplied ZIP is readable, its internal integrity checks pass, and all
three exact lookups succeeded.** Both selected BUB1B alleles have small predicted
merged-splicing effects in this resource. This fills the previously missing
**aggregate splicing-score** lookup, not the missing tissue/junction-resolved
molecular analysis. No change to the drug shortlist or phase conclusion follows.

| Role | GRCh38, 1-based forward-strand allele | Merged-splicing score |
|---|---|---:|
| Documented public DNM1 comparison | `chr9:128225994 G>A` | 2.522 |
| Submitted BUB1B p.Leu737Ter candidate | `chr15:40209701 T>G` | 0.08699 |
| Submitted BUB1B p.Asn1002Lys candidate | `chr15:40220612 T>G` | 0.04813 |

These are the archive's decimal values, not AVI scores, PHRED ranks, SHAP values,
pathogenicity probabilities or measured percentages of abnormal transcripts. The
public comparison provides transport and scale context; it does not validate an
assay or establish a clinical sensitivity/negative predictive value.

## Meaning and next scientific decision

The merged score is the maximum splice-site effect plus the maximum splice-usage
effect plus one-fifth of the maximum junction effect. These maxima may come from
different genes, tissues or junctions. It is an unsigned, nonnegative and theoretically
unbounded aggregate. The official tutorial's observation that values above 1 often
have large effects is **not a validated clinical cutoff**. Neither result establishes
benignity or experimentally normal splicing.
[Official scoring tutorial](https://www.alphagenomedocs.com/colabs/splicing_variant_scoring.html),
[detailed source review](alphagenome-splicing-semantics.md)

The defensible inference is that **this resource does not add strong predicted
splicing support for either selected allele**. It does not exclude coding/protein
damage, transcript decay, an effect in an unrepresented biological context or a
model false negative. In particular, a small splice-effect prediction does not
contradict a stop-gain mechanism or demonstrate that the missense protein is functional.

The aggregate is itself an input to AVI; the earlier AVI and this download are not
independent biological replications. Previously obtained `MERGED_SPLICING` SHAP
contributions quantify influence on AVI, not these raw splice-effect magnitudes.
Do not compare their numeric scales or count them as separate functional experiments.
[Atlas methods](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

For Track 2, retain RNA abundance/splicing, protein and checkpoint/function assays in
the proposed validation plan. Do not add a splice-targeted intervention on these
scalars alone, or remove RNA checks because the values are small. Everolimus remains
one conditional phenotype-first research priority; HCQ remains reserve. Clinical
efficacy and exposure margins remain unknown. **Trans phase remains unconfirmed.**
No wet-lab experiment, treatment, contact or submission upload occurred.

## Exact scope and retained contrasts

The three query positions were declared in code before reading their scores: the
same public DNM1 example used in session 35, plus the two permitted submission-derived
candidate tuples. No source VCF, clinical narrative, subject sequence or `.env` was
read. This session made **no AlphaGenome API requests** and ran no model inference.
The public archive contains reference predictions, not observations of this subject.

At each position, all three alternate-allele rows returned by Tabix were retained,
including those not selected in the submission:

| Position / REF | Alternate-score contrasts |
|---|---|
| `chr9:128225994 G` | A: 2.522; C: 0.08013; T: 0.06606 |
| `chr15:40209701 T` | A: 0.04022; C: 0.07947; G: 0.08699 |
| `chr15:40220612 T` | A: 0.03854; C: 0.1073; G: 0.04813 |

These other alternates are **public-reference allele contrasts, not additional
subject variants or clinically validated benign controls**. Nine rows total were
retained; zero requested alleles were missing. A missing row would remain unavailable,
not become a zero score. No full-genome score distribution or dataset-wide coverage
was inferred from these three positions.

## Archive, index and integrity evidence

Original, unchanged file:
`data/resources/combined_splicing_snvs_tabix.zip` — **20,637,482,323 bytes**.
SHA-256: `21011fe376455c7692f7f8f24ae9898d8f758060a91a24b15c35ac1c6cffa7a3`.
The owner identified it as the official merged-splicing download; the archive did
not supply an independently authenticated publisher checksum to compare against.
Our SHA-256 pins these local bytes; CRC checks establish internal consistency, not
publisher authenticity or biological correctness.

The ZIP has exactly two stored, unencrypted, regular-file members. The complete bytes
of both were copied in bounded chunks and checked against ZIP sizes/CRCs, with member
SHA-256 hashes calculated. No archive path was used with `extractall()`.

| Member | Bytes | ZIP CRC-32, verified | SHA-256 |
|---|---:|---|---|
| `combined_alphagenome_splicing_snvs.tsv.gz` | 20,635,924,975 | `0d5fd842` | `4e0d617655044e8301416104a82685be69638071cc6be8a1f4e42c5e3443e594` |
| `combined_alphagenome_splicing_snvs.tsv.gz.tbi` | 1,556,770 | `a953ad14` | `f6af28d74315fde560cb16e8b14411ba4776b83f96b613e2edb19d3e2d0e8f2c` |

The usable cache is `data/resources/alphagenome-splicing-v2/`. Both members pass BGZF
header and canonical 28-byte EOF checks. The score-table header is exactly:

```text
#CHROM	POS	REF	ALT	alphagenome_splicing
```

The TBI header has 24 `chr`-prefixed contigs, format 2 (VCF preset), sequence column 1,
start column 2, end column 0, comment `#`, skip 0 and no zero-based flag. This is still
a **five-column TSV, not a valid VCF**. Local Tabix 1.24 requests `chr:POS-POS` and an
explicit text parser checks chromosome, position, REF, ALT, uniqueness and a finite
nonnegative score. Candidate REF bases and immutable submission/report hashes are
checked locally before interpretation. No arbitrary raw genomic input is accepted.

The query step rehashed both cached members before using the index. It verified the
same index metadata and retained exact decimal strings. Native query stdout/stderr
are bounded before buffering, with a 30-second timeout and no core dumps. ZIP CRCs
cover all compressed member bytes, but we did **not** inflate the entire genomic
table or validate every inner BGZF block/record/index entry. The blocks traversed
by the header and point queries were decoded by gzip/HTSlib. Preserve this distinction.

The cache manifest SHA-256 is
`c91370a246d79d7ba2e480cb33c76005ef964ceb10d7274b8dfd6c4737a4567d`.
The query result `results/feat009/alphagenome-splicing-v1/scores.json` has SHA-256
`d61e58f771d64037f08de283e0ce34bf42f84e6077e0732ce869ef7154ac19cb`.
Successful preparation took 19:03:51–19:04:51 UTC; query/rehashing took
19:05:07–19:05:23 UTC on 8 September. Exact producer/model revision remains unknown;
neither the download filename, ZIP timestamps nor SDK pin supplies it.

## Reproduce and test

```bash
uv run python /home/sports/.agents/skills/get-available-resources/scripts/detect_resources.py --output results/feat009/alphagenome-session36-resources.json
uv run python scripts/alphagenome_splicing.py prepare data/resources/combined_splicing_snvs_tabix.zip data/resources/alphagenome-splicing-v2
uv run python scripts/alphagenome_splicing.py query data/resources/alphagenome-splicing-v2 results/feat009/alphagenome-splicing-v1
uv run python scripts/alphagenome_splicing.py verify data/resources/alphagenome-splicing-v2
uv run python scripts/test_alphagenome_splicing.py
uv run python scripts/track2_evidence.py verify results/feat009/jvv7_track2_research_v2
uv run python scripts/track2_evidence.py track1
```

`prepare` and `query` require new output directories; choose new suffixes when
repeating. `verify` is read-only and checks the prepared cache, not a fresh download
against an independently published checksum. The external resource-skill script is
optional for reproduction of scores; `psutil` was added with `uv add` and locked after
the first resource-helper call reported its missing dependency.

Resource snapshot: 64 CPU cores, approximately 456 GiB available RAM and 3.2 TiB disk
free; GPUs were busy. Although the helper suggested broad parallelism from hardware
counts, the actual job used one streaming CPU process, 8 MiB chunks and no GPU.
The original ZIP and BGZF compression were retained; no whole-table inflation or
genome-wide annotation job was performed.

## Adversarial corrections and output conditions

The initial `alphagenome-splicing-v1` **cache** attempt passed both full-member
CRCs/hashes but failed our end-marker check because the local validator mistakenly
encoded 30 bytes instead of the canonical 28. The constant was corrected; an
independently constructed BGZF test fixture guards against recurrence. That failed
cache/manifest remains historical; use cache v2, not a manually relabelled success.
This was not evidence of a defective user download. The similarly named **result**
directory `results/feat009/alphagenome-splicing-v1/` is the successful query output.

Standards review also identified a post-buffer output limit; child file-size limits
now enforce the bound before native output enters Python memory. Synthetic tests
cover archive traversal/types/compression/corruption, size/hash/index drift, canonical
BGZF structure, coordinate/allele matching, missing versus zero, nonfinite scores,
no-overwrite behavior and fixed query scope. Their manufactured scores are tests,
not extra patient or Atlas findings.

This addendum uses Google DeepMind precomputed output under the non-commercial
download conditions and [AlphaGenome Output Terms of Use](https://deepmind.google.com/science/alphagenome/output-terms).
The output-derived values and descriptions here remain subject to those terms;
no additional output licence is granted. Modifications: exact allele selection,
JSON serialization, tabular presentation and explanatory interpretation. The original
archive is unchanged. This extends the session-35 Google DeepMind disclosure; it is
not a fresh hosted inference run. Preserve the uploaded Track 1 v4 and reviewed
Track 2 v2 snapshots. A future Track 2 release needs the Atlas addenda and updated
disclosure; this note is not a new submitted entry or evidence of upload readiness.
