#!/usr/bin/env python3
"""Synthetic-only integration tests for the local phase-connectivity audit."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import pysam

from audit_phase_connectivity import audit_reads, load_markers, phase_status, self_check


class PhaseConnectivityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="phase-connectivity-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def vcf(self, name, records, sample="PROBAND01"):
        header = pysam.VariantHeader()
        header.contigs.add("1", length=1000)
        header.filters.add("LowQual", None, None, "Synthetic failing site")
        header.formats.add("GT", 1, "String", "Genotype")
        header.formats.add("DP", 1, "Integer", "Depth")
        header.formats.add("GQ", 1, "Integer", "Quality")
        header.add_sample(sample)
        path = self.root / f"{name}.vcf.gz"
        with pysam.VariantFile(path, "wz", header=header) as out:
            for pos, alt, status, gq in records:
                rec = out.new_record(contig="1", start=pos, alleles=("A", alt))
                if status:
                    rec.filter.add(status)
                rec.samples[sample]["GT"] = (0, 1)
                rec.samples[sample]["DP"] = 30
                rec.samples[sample]["GQ"] = gq
                out.write(rec)
        pysam.tabix_index(str(path), preset="vcf")
        return path

    def bam(self, *, proper=True, duplicate=False, mapq=60, baseq=30,
            different_groups=False, bad_sample=False, missing_group=False):
        path = self.root / "synthetic.bam"
        header = {"HD": {"SO": "coordinate"}, "SQ": [{"SN": "1", "LN": 1000}],
                  "RG": [{"ID": g, "SM": "wrong" if bad_sample else "PROBAND01"}
                         for g in ("a", "b")]}
        with pysam.AlignmentFile(path, "wb", header=header) as out:
            for index, (pos, base) in enumerate(((10, "A"), (30, "G"))):
                read = pysam.AlignedSegment()
                read.query_name = "synthetic-pair"
                read.query_sequence = base
                read.query_qualities = [baseq]
                read.reference_id = 0
                read.reference_start = pos
                read.next_reference_id = 0
                read.next_reference_start = 30 if index == 0 else 10
                read.template_length = 21 if index == 0 else -21
                read.cigarstring = "1M"
                read.mapping_quality = mapq
                read.flag = (99 if index == 0 else 147)
                if not proper:
                    read.flag &= ~2
                if duplicate:
                    read.flag |= 1024
                if not missing_group:
                    read.set_tag("RG", "b" if different_groups and index else "a")
                out.write(read)
        pysam.index(str(path))
        return path

    def audit(self, **kwargs):
        return audit_reads(self.bam(**kwargs), "1", 0, 100,
                           {10: ("A", "G"), 30: ("A", "G")}, [10, 30], 30, 20)

    def test_algorithm_cases(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self_check()

    def test_proper_mates_join_once(self):
        result = self.audit()
        self.assertEqual(result["direct_target_pair_fragments"]["RA"], 1)
        self.assertEqual(result["fragments_with_marker_observations"], 1)

    def test_improper_mates_do_not_join(self):
        self.assertEqual(sum(self.audit(proper=False)["direct_target_pair_fragments"].values()), 0)

    def test_same_name_different_read_groups_do_not_join(self):
        self.assertEqual(sum(self.audit(different_groups=True)["direct_target_pair_fragments"].values()), 0)

    def test_duplicates_excluded(self):
        self.assertEqual(self.audit(duplicate=True)["fragments_with_marker_observations"], 0)

    def test_low_mapq_excluded(self):
        self.assertEqual(self.audit(mapq=10)["fragments_with_marker_observations"], 0)

    def test_low_baseq_excluded(self):
        self.assertEqual(self.audit(baseq=5)["fragments_with_marker_observations"], 0)

    def test_bam_wrong_sample_rejected(self):
        with self.assertRaises(ValueError):
            self.audit(bad_sample=True)

    def test_missing_read_group_rejected(self):
        with self.assertRaises(ValueError):
            self.audit(missing_group=True)

    def test_unfiltered_records_require_explicit_permission(self):
        path = self.vcf("markers", [(10, "G", "PASS", 30), (20, "G", None, 30),
                                    (30, "G", "PASS", 30), (40, "G", "LowQual", 30),
                                    (50, "G", "PASS", 5)])
        targets = [(10, ("A", "G")), (30, ("A", "G"))]
        strict, _, _ = load_markers([(path, False)], "1", 0, 100, targets)
        relaxed, counts, _ = load_markers([(path, True)], "1", 0, 100, targets)
        self.assertEqual(set(strict), {10, 30})
        self.assertEqual(set(relaxed), {10, 20, 30})
        self.assertEqual(counts[0]["unfiltered_heterozygous_records"], 1)

    def test_conflicting_marker_removed_and_target_conflict_rejected(self):
        first = self.vcf("first", [(10, "G", "PASS", 30), (20, "G", "PASS", 30),
                                   (30, "G", "PASS", 30)])
        second = self.vcf("second", [(20, "T", "PASS", 30)])
        inputs = [(first, False), (second, False)]
        markers, _, ambiguous = load_markers(inputs, "1", 0, 100,
                                              [(10, ("A", "G")), (30, ("A", "G"))])
        self.assertEqual(set(markers), {10, 30})
        self.assertEqual(ambiguous, 1)
        with self.assertRaises(ValueError):
            load_markers(inputs, "1", 0, 100, [(20, ("A", "G"))])

    def test_vcf_wrong_sample_rejected(self):
        path = self.vcf("wrong", [(10, "G", "PASS", 30)], sample="wrong")
        with self.assertRaises(ValueError):
            load_markers([(path, False)], "1", 0, 100, [(10, ("A", "G"))])

    def test_phase_requires_matching_heterozygotes_and_phase_set(self):
        for case, genotypes, sets, expected in (
            ("cis", [(0, 1), (0, 1)], [10, 10], "cis"),
            ("trans", [(0, 1), (1, 0)], [10, 10], "trans"),
            ("separate", [(0, 1), (1, 0)], [10, 30], "unconfirmed"),
            ("missing", [(0, 1), (1, 0)], [None, None], "unconfirmed"),
            ("homozygous", [(0, 0), (1, 0)], [10, 10], "unconfirmed"),
        ):
            with self.subTest(case=case):
                source = self.vcf(case, [(10, "G", "PASS", 30), (30, "G", "PASS", 30)])
                dest = self.root / f"{case}-phased.vcf.gz"
                with pysam.VariantFile(source) as vcf:
                    vcf.header.formats.add("PS", 1, "Integer", "Phase set")
                    with pysam.VariantFile(dest, "wz", header=vcf.header) as out:
                        for index, rec in enumerate(vcf):
                            rec.samples["PROBAND01"]["GT"] = genotypes[index]
                            rec.samples["PROBAND01"].phased = True
                            rec.samples["PROBAND01"]["PS"] = sets[index]
                            out.write(rec)
                pysam.tabix_index(str(dest), preset="vcf")
                result = phase_status(dest, "1", [(10, ("A", "G")), (30, ("A", "G"))])
                self.assertEqual(result["encoded_phase_relation"], expected)


if __name__ == "__main__":
    unittest.main()
