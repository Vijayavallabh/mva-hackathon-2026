#!/usr/bin/env python3
"""Synthetic public-interface regressions; no subject files or network required."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pysam

from audit_track1_evidence import native_phase, rank_sensitivity, score_scenarios
from track1_submission import SCHEMA


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="track1-evidence-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.csv = self.directory / "submission.csv"
        self.rows = []
        for i in range(4):
            row = {field: "" for field in SCHEMA}
            row.update(proband_id="PROBAND01", finding_type="primary", epcr=str(.9 - .1 * i))
            for suffix, pos in (("1", 10 + 20 * i), ("2", 20 + 20 * i)):
                row.update({f"chrom_{suffix}": "chr1", f"pos_{suffix}": str(pos),
                            f"ref_{suffix}": "A", f"alt_{suffix}": "T"})
            self.rows.append(row)
        self.write_csv()

    def write_csv(self):
        with self.csv.open("w") as handle:
            writer = csv.DictWriter(handle, fieldnames=SCHEMA)
            writer.writeheader()
            writer.writerows(self.rows)

    def test_scores_have_no_actual_result_and_include_failure_cases(self):
        report = score_scenarios(self.csv)
        self.assertIsNone(report["actual_competition_score"])
        self.assertFalse(report["guaranteed_perfect_score"])
        cases = report["scenarios"]
        self.assertEqual([c["rank_points"] for c in cases], [100, 50, 50, 25, 50, 50, 0])
        for case, expected in zip(cases, [1, 2/3, .5, .4, .5, .5, 0]):
            self.assertAlmostEqual(case["f_max"], expected)

    def test_monotonic_epcr_rescaling_does_not_change_scores(self):
        before = score_scenarios(self.csv)["scenarios"]
        for i, row in enumerate(self.rows):
            row["epcr"] = str(.04 - .01 * i)
        self.write_csv()
        after = score_scenarios(self.csv)["scenarios"]
        self.assertEqual([(r["rank_points"], r["f_max"]) for r in before],
                         [(r["rank_points"], r["f_max"]) for r in after])

    def test_schema_errors_cannot_get_successful_audit(self):
        self.rows[1]["epcr"] = self.rows[0]["epcr"]
        self.write_csv()
        with self.assertRaises(ValueError):
            score_scenarios(self.csv)

    def make_vcf(self, left=None, right=None, extra_samples=False, duplicate=False, omit_right=False):
        header = pysam.VariantHeader()
        header.contigs.add("1", length=1000)
        for key, number, dtype in (("GT", 1, "String"), ("PS", 1, "Integer"),
                                   ("PGT", 1, "String"), ("PID", 1, "String"),
                                   ("HP", ".", "String")):
            header.formats.add(key, number, dtype, "Synthetic fixture field")
        header.add_sample("TEST")
        if extra_samples:
            header.add_sample("OTHER")
        path = self.directory / "synthetic.vcf"
        with pysam.VariantFile(path, "w", header=header) as out:
            for pos, settings in ((10, left or {}), (20, right or {})):
                if pos == 20 and omit_right:
                    continue
                record = out.new_record(contig="1", start=pos - 1, alleles=("A", "T"))
                call = record.samples["TEST"]
                call["GT"] = settings.get("GT", (0, 1))
                call.phased = settings.get("phased", False)
                for key in ("PS", "PGT", "PID", "HP"):
                    if key in settings:
                        call[key] = settings[key]
                out.write(record)
                if duplicate and pos == 10:
                    out.write(record)
        return Path(pysam.tabix_index(str(path), preset="vcf", force=True))

    def phase(self, **kwargs):
        return native_phase(self.csv, self.make_vcf(**kwargs), "TEST")

    def test_absent_tags_are_unconfirmed(self):
        result = self.phase()
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")
        self.assertFalse(result["biological_phase_confirmed"])
        self.assertEqual([t["exact_match_count"] for t in result["targets"]], [1, 1])

    def test_gt_ps_trans_is_only_encoding(self):
        result = self.phase(left={"GT": (0, 1), "phased": True, "PS": 7},
                            right={"GT": (1, 0), "phased": True, "PS": 7})
        self.assertEqual(result["encoded_relations"]["GT_PS"], "trans")
        self.assertFalse(result["biological_phase_confirmed"])

    def test_gt_ps_cis(self):
        result = self.phase(left={"phased": True, "PS": 7}, right={"phased": True, "PS": 7})
        self.assertEqual(result["combined_encoding_status"], "cis")

    def test_separate_phase_sets_do_not_connect(self):
        result = self.phase(left={"phased": True, "PS": 7}, right={"phased": True, "PS": 8})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_phased_gt_without_explicit_group_is_not_assumed_connected(self):
        result = self.phase(left={"phased": True}, right={"phased": True})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_unphased_gt_with_ps_is_not_phase(self):
        result = self.phase(left={"PS": 7}, right={"PS": 7})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_native_pgt_pid_is_recognized_without_phased_gt(self):
        result = self.phase(left={"PGT": "0|1", "PID": "private_fixture_group"},
                            right={"PGT": "1|0", "PID": "private_fixture_group"})
        self.assertEqual(result["encoded_relations"]["PGT_PID"], "trans")
        self.assertNotIn("private_fixture_group", json.dumps(result))
        self.assertNotIn("0|1", json.dumps(result))

    def test_native_pid_groups_are_not_interchangeable(self):
        result = self.phase(left={"PGT": "0|1", "PID": "left"},
                            right={"PGT": "1|0", "PID": "right"})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_pgt_without_pid_is_not_connected(self):
        result = self.phase(left={"PGT": "0|1"}, right={"PGT": "1|0"})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_invalid_pgt_requires_review(self):
        result = self.phase(left={"PGT": "1|1", "PID": "same"},
                            right={"PGT": "0|1", "PID": "same"})
        self.assertEqual(result["combined_encoding_status"], "manual_review_required")

    def test_disagreeing_encodings_require_review(self):
        result = self.phase(left={"phased": True, "PS": 7, "PGT": "0|1", "PID": "same"},
                            right={"phased": True, "PS": 7, "PGT": "1|0", "PID": "same"})
        self.assertEqual(result["combined_encoding_status"], "conflicting_encodings")

    def test_homozygous_gt_cannot_establish_pair_phase(self):
        result = self.phase(left={"GT": (1, 1), "phased": True, "PS": 7},
                            right={"phased": True, "PS": 7})
        self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_hp_is_flagged_not_silently_ignored(self):
        result = self.phase(left={"HP": ("7-1", "7-2")})
        self.assertEqual(result["combined_encoding_status"], "manual_review_required")

    def test_duplicates_and_missing_targets_do_not_establish_phase(self):
        for kwargs in ({"duplicate": True}, {"omit_right": True}):
            with self.subTest(**kwargs):
                result = self.phase(**kwargs)
                self.assertEqual(result["combined_encoding_status"], "unconfirmed")

    def test_sample_identity_must_be_explicit_and_unique(self):
        path = self.make_vcf()
        with self.assertRaises(ValueError):
            native_phase(self.csv, path, "WRONG")
        path = self.make_vcf(extra_samples=True)
        with self.assertRaises(ValueError):
            native_phase(self.csv, path, "TEST")

    def make_candidates(self):
        records = []
        for i, row in enumerate(self.rows[:2]):
            record = dict(row, model="compound_heterozygous", gene=f"GENE_{i}",
                          proband_similarity=str(1 - i), family_history_similarity="0",
                          proband_coverage_of_7=str(7 * (1 - i)), total_score=str(20 - i))
            for suffix in ("1", "2"):
                record.update({f"max_af_{suffix}": "", f"sift_{suffix}": "",
                               f"polyphen_{suffix}": "", f"clinvar_{suffix}": ""})
            records.append(record)
        path = self.directory / "candidates.tsv"
        with path.open("w") as handle:
            writer = csv.DictWriter(handle, fieldnames=records[0], delimiter="\t")
            writer.writeheader()
            writer.writerows(records)
        return path

    def test_rank_sensitivity_can_displace_leader(self):
        result = rank_sensitivity(self.csv, self.make_candidates())
        self.assertEqual(result["scenario_count"], 34)
        self.assertEqual(result["leading_pair_best_rank"], 1)
        self.assertEqual(result["leading_pair_worst_rank"], 2)
        baseline = [s for s in result["scenarios"] if s["proband_weight"] == 8
                    and s["family_weight"] == .5 and s["missing_af_credit"] == 1
                    and s["prediction_bonus"] and s["clinvar_bonus"]][0]
        self.assertEqual(baseline["leading_pair_margin_over_best_other"], 1)

    def test_leading_pair_absent_from_candidate_universe_is_error(self):
        candidates = self.make_candidates()
        self.rows[0]["pos_1"] = "99"
        self.write_csv()
        with self.assertRaises(ValueError):
            rank_sensitivity(self.csv, candidates)

    def test_annotation_ablation_uses_pair_average_and_missingness(self):
        path = self.make_candidates()
        with path.open() as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        # Leader has two prediction points and two ClinVar points on one allele:
        # each contributes one point after averaging the pair. Only one AF missing.
        rows[0].update(sift_1="deleterious", polyphen_1="probably_damaging",
                       clinvar_1="Pathogenic", max_af_2="0.0001")
        rows[1].update(max_af_1="0.0001", max_af_2="0.0001")
        with path.open("w") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0], delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
        result = rank_sensitivity(self.csv, path)
        ablation = next(s for s in result["scenarios"] if not s["prediction_bonus"]
                        and not s["clinvar_bonus"] and s["missing_af_credit"] == 0)
        self.assertAlmostEqual(ablation["leading_pair_margin_over_best_other"], -1.5)
        self.assertEqual(ablation["leading_pair_rank"], 2)

    def test_cli_error_does_not_echo_subject_like_sample_or_phase_text(self):
        path = self.make_vcf(left={"PGT": "0|1", "PID": "private_fixture_group"})
        command = [sys.executable, str(Path(__file__).with_name("audit_track1_evidence.py")),
                   "phase", str(self.csv), "--vcf", str(path), "--sample", "PRIVATE_WRONG_SAMPLE"]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertNotIn("PRIVATE_WRONG_SAMPLE", run.stdout + run.stderr)
        self.assertNotIn("private_fixture_group", run.stdout + run.stderr)
        self.assertNotIn("0|1", run.stdout + run.stderr)

    def test_cli_scores_is_read_only_and_emits_json(self):
        before = self.csv.read_bytes()
        command = [sys.executable, str(Path(__file__).with_name("audit_track1_evidence.py")),
                   "scores", str(self.csv)]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIsNone(json.loads(run.stdout)["actual_competition_score"])
        self.assertEqual(self.csv.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
