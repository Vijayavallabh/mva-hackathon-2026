# Leading BUB1B pair: phase follow-up (feat-005c)

The owner requested additional trans-phase work on 2026-09-08. This follow-up uses
only the existing local all-lane BAM and variant calls. **Trans phase remains
unconfirmed.** No parental data, new sequencing, external data upload or family
contact is involved. No submitted deliverable is changed.

## Question and decision rule

Can the available reads connect the two submitted candidate alleles, directly or
through intermediate heterozygous markers? The candidate positions differ by
10,911 bases. Their presence as two heterozygotes does not establish which
chromosome carries each allele.

The new script is a connectivity audit, **not a phasing algorithm**. Each eligible
SNV is a node, and a fragment observing two nodes supplies an edge. It intentionally
does not infer allele orientation or calibrated phase confidence from graph
connectivity. Disconnection demonstrates missing links under the tested model;
connection would require further phase-consistency review, not an automatic trans call.
The official [WhatsHap guide](https://whatshap.readthedocs.io/en/latest/guide.html)
explains read-based reconstruction and why phase-set membership matters. Long-read
or pedigree evidence can improve phasing, but neither is newly available here.

## Audit method

- Fetch only the existing 100,154-base padded BUB1B interval, using indexed access.
- Require single-sample PROBAND01 marker inputs and BAM read groups matching PROBAND01.
- Original markers: explicit PASS, biallelic heterozygous A/C/G/T SNVs, DP >= 10,
  GQ >= 20. Exclude positions with conflicting eligible allele definitions.
- Exploratory union: add qualifying HaplotypeCaller SNVs, explicitly permitting its
  unfiltered `.` records through `--unfiltered-vcf`. These are not relabelled PASS
  and are not independent validation; they use the same underlying reads.
- Use primary, nonduplicate, QC-passing alignments. Exclude supplementary/secondary
  alignments. Main thresholds: MAPQ >= 30 and base quality >= 20; sensitivity:
  MAPQ >= 20 and base quality >= 13.
- Combine observations only across properly paired alignments with matching read
  name and read group on the same chromosome. Improper pairs contribute individual
  reads, not mate links. A mate's mapped position or template length alone is not
  an observation of a variant. Conflicting overlapping-mate calls are excluded.
- Test graph connections requiring at least one and at least three distinct
  fragment identities per edge. This is an operational support check, not a
  probability model or proof of molecular independence after duplicate marking.
- Output only counts, categorical conclusions and provenance. No read names,
  read bases, non-submission marker alleles, marker coordinates or graph edges
  are emitted. Input sizes/mtimes are recorded, not a full BAM content hash.

Pysam numeric fetch coordinates are zero-based, half-open; command-line target
positions are one-based and explicitly converted. FILTER membership is tested
through the explicit key set: in pysam 0.24.0, `"PASS" in record.filter` also
returns true for an empty filter, which must not silently erase that distinction.

## Initial measured result

Original calls supply 48 eligible SNVs; the union with HaplotypeCaller supplies 49.
The nearest other eligible SNVs are 6,769 and 809 bases from the respective targets.
At both quality settings and both edge-support thresholds:

- Zero fragments observe both candidate positions.
- Both targets are singleton components with zero neighboring SNVs.
- Candidate-specific fragment counts are 21 reference / 26 alternate and
  15 reference / 12 alternate. These support the individual calls, not their phase.

The region contains 32,844 fetched alignments; 32,541 and 32,572 pass the respective
alignment filters. Maximum observed read length is 149 bases. Among accepted
proper-pair read-1 alignments in the region, median absolute template length is
442 bases and maximum is 1,347 bases. These are local alignment summaries, not
global library statistics or evidence that an unsequenced insert covers a marker.

The original-marker graph has 366 fragments observing at least two markers;
the union has 367. Thus the audit detects local links elsewhere, but neither
target participates. The graph is SNV-only; the separate WhatsHap recall-locus
run below tests supported non-SNV types too. This does not exclude every possible
future variant-discovery, structural, long-read or pedigree approach.

## Reproduction

All outputs remain ignored under `results/feat005c/`. Do not overwrite a previous
run when preserving provenance; use a new output directory for revised analysis.

```bash
uv run python scripts/audit_phase_connectivity.py --self-check
uv run python scripts/test_phase_connectivity.py

uv run python scripts/audit_phase_connectivity.py \
  --bam results/feat005b/all-lanes.markdup.bam \
  --vcf results/feat005b/target-source.proband.vcf.gz \
  --bed results/feat005b/phase-target.bed \
  --left 40209701:T:G --right 40220612:T:G \
  > results/feat005c/source-connectivity.json

uv run python scripts/audit_phase_connectivity.py \
  --bam results/feat005b/all-lanes.markdup.bam \
  --vcf results/feat005b/target-source.proband.vcf.gz \
  --unfiltered-vcf results/feat005b/haplotypecaller.pass.normalized.vcf.gz \
  --bed results/feat005b/phase-target.bed \
  --left 40209701:T:G --right 40220612:T:G \
  > results/feat005c/union-connectivity.json

tools/install/bin/bcftools view -R results/feat005b/phase-target.bed \
  results/feat005b/haplotypecaller.pass.normalized.vcf.gz \
  -Oz -o results/feat005c/hc-locus.vcf.gz
tools/install/bin/tabix -p vcf results/feat005c/hc-locus.vcf.gz
uv run whatshap phase --sample PROBAND01 \
  --reference data/resources/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set_plus_hs38d1_maskedGRC_exclusions_v2_no_chr.fasta \
  -o results/feat005c/hc-locus.phased.vcf.gz \
  results/feat005c/hc-locus.vcf.gz results/feat005b/all-lanes.markdup.bam \
  > logs/feat005c-hc-phase.log 2>&1
tools/install/bin/tabix -p vcf results/feat005c/hc-locus.phased.vcf.gz
```

The WhatsHap 2.8 recall-locus run is in progress. Its phase result must be inspected
before treating this follow-up as complete. Neither original evidence nor the
connectivity audit currently establishes cis or trans.
