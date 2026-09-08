#!/usr/bin/env python3
"""Offline synthetic ZIP/BGZF/TBI checks; no public bulk archive or subject reads."""
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
import zlib

import alphagenome_splicing as s


def bgzf_block(payload):
    compressor = zlib.compressobj(wbits=-15)
    compressed = compressor.compress(payload) + compressor.flush()
    header = bytes.fromhex("1f8b08040000000000ff060042430200")
    size = len(header) + 2 + len(compressed) + 8
    return (header + struct.pack("<H", size - 1) + compressed
        + struct.pack("<II", zlib.crc32(payload), len(payload)))


def bgzf(payload):
    return bgzf_block(payload) + bgzf_block(b"")


def tbi_bytes(names=("chr9", "chr15"), fields=None, raw_names=None):
    encoded = raw_names if raw_names is not None else b"\0".join(n.encode() for n in names) + b"\0"
    integers = [len(names), 2, 1, 2, 0, 35, 0, len(encoded)]
    if fields:
        for offset, value in fields.items():
            integers[offset] = value
    # Empty bins/linear intervals are sufficient for header validation only.
    return bgzf(b"TBI\x01" + struct.pack("<8i", *integers) + encoded
        + b"\0" * (8 * len(names)) + struct.pack("<Q", 0))


def point_text(variant=s.CONTROL, omit=None):
    chrom, pos, ref, alt = variant
    lines = [s.HEADER]
    for base in "ACGT":
        if base != ref and base != omit:
            value = "0" if base == alt else "0.125"
            lines.append(f"{chrom}\t{pos}\t{ref}\t{base}\t{value}")
    return "\n".join(lines) + "\n"


class Fixture(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="atlas-splicing-synthetic-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def archive(self, data=None, index=None):
        path = self.root / "synthetic.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.writestr(s.DATA, bgzf(point_text().encode()) if data is None else data)
            archive.writestr(s.INDEX, tbi_bytes() if index is None else index)
        return path

    def prepared(self):
        cache = self.root / "cache"
        s.prepare(self.archive(), cache)
        return cache

    def index(self, data):
        path = self.root / "synthetic.tbi"
        path.write_bytes(data)
        return path


class MemberTests(unittest.TestCase):
    def members(self):
        infos = []
        for name in s.MEMBERS:
            item = zipfile.ZipInfo(name)
            item.file_size = item.compress_size = 100
            item.compress_type = zipfile.ZIP_STORED
            item.external_attr = (stat.S_IFREG | 0o600) << 16
            infos.append(item)
        return infos

    def test_exact_regular_stored_members(self):
        s.validate_members(self.members())

    def test_path_absolute_traversal_or_nested_rejected(self):
        for name in ("../" + s.DATA, "/" + s.DATA, "nested/" + s.DATA, "..\\" + s.DATA):
            with self.subTest(name=name), self.assertRaises(ValueError):
                infos = self.members()
                infos[0].filename = name
                s.validate_members(infos)

    def test_missing_extra_and_duplicate_members_rejected(self):
        for kind in ("missing", "extra", "duplicate"):
            infos = self.members()
            if kind == "missing":
                infos.pop()
            elif kind == "extra":
                infos.append(zipfile.ZipInfo("extra"))
            else:
                infos[1].filename = s.DATA
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                s.validate_members(infos)

    def test_symlink_directory_and_special_modes_rejected(self):
        for mode in (stat.S_IFLNK, stat.S_IFDIR, stat.S_IFIFO, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFSOCK):
            infos = self.members()
            infos[0].external_attr = (mode | 0o600) << 16
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                s.validate_members(infos)

    def test_encrypted_members_rejected(self):
        infos = self.members()
        infos[0].flag_bits |= 1
        with self.assertRaises(ValueError):
            s.validate_members(infos)

    def test_other_compression_and_inconsistent_sizes_rejected(self):
        for change in ("compression", "size"):
            infos = self.members()
            if change == "compression":
                infos[0].compress_type = zipfile.ZIP_DEFLATED
            else:
                infos[0].compress_size -= 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                s.validate_members(infos)

    def test_empty_negative_and_oversized_members_rejected(self):
        for index, name in enumerate(s.MEMBERS):
            for size in (0, -1, s.LIMITS[name] + 1):
                infos = self.members()
                infos[index].file_size = infos[index].compress_size = size
                with self.subTest(name=name, size=size), self.assertRaises(ValueError):
                    s.validate_members(infos)


class StructureTests(Fixture):
    def test_canonical_eof_constructed_independently(self):
        eof = bgzf_block(b"")
        self.assertEqual(len(eof), 28)
        self.assertEqual(s.BGZF_EOF, eof)
        s.bgzf_check(self.index(bgzf(b"synthetic")))

    def test_non_bgzf_and_missing_or_corrupt_eof_rejected(self):
        good = bgzf(b"synthetic")
        for data in (gzip.compress(b"synthetic"), good[:-28], good[:-1] + b"x", b"short"):
            with self.subTest(data=data[:12]), self.assertRaises((ValueError, OSError)):
                s.bgzf_check(self.index(data))

    def test_valid_vcf_preset_index_semantics(self):
        result = s.index_header(self.index(tbi_bytes()))
        self.assertEqual(result["format"], 2)
        self.assertEqual(result["coordinate_convention"], "1-based point")
        self.assertEqual(result["contigs"], ["chr9", "chr15"])

    def test_zero_based_flag_and_schema_columns_rejected(self):
        for fields in ({1: 2 | 0x10000}, {1: 0}, {2: 2}, {3: 3}, {4: 2}, {5: 0}, {6: 1}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                s.index_header(self.index(tbi_bytes(fields=fields)))

    def test_name_table_bounds_and_count_rejected(self):
        for fields in ({0: 0}, {0: 10000}, {7: 0}, {7: 1000000}, {0: 3}, {7: 999999}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                s.index_header(self.index(tbi_bytes(fields=fields)))

    def test_duplicate_and_unterminated_names_rejected(self):
        for data in (tbi_bytes(names=("chr9", "chr9")), tbi_bytes(raw_names=b"chr9\0chr15")):
            with self.subTest(), self.assertRaises(ValueError):
                s.index_header(self.index(data))

    def test_wrong_magic_and_short_index_rejected(self):
        raw = gzip.decompress(tbi_bytes())
        for data in (bgzf(b"CSI\x01" + raw[4:]), bgzf(b"TBI\x01")):
            with self.subTest(), self.assertRaises(ValueError):
                s.index_header(self.index(data))


class PreparationTests(Fixture):
    def test_prepared_integrity_and_provenance(self):
        archive = self.archive()
        manifest = s.prepare(archive, self.root / "cache")
        self.assertEqual(manifest["state"], "prepared")
        self.assertEqual(manifest["archive_sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())
        self.assertFalse(manifest["publisher_checksum_verified"])
        self.assertEqual(set(manifest["members"]), set(s.MEMBERS))
        for name, item in manifest["members"].items():
            payload = (self.root / "cache" / name).read_bytes()
            self.assertEqual(item["size"], len(payload))
            self.assertEqual(item["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(item["zip_crc32"], f"{zlib.crc32(payload):08x}")
            self.assertTrue(item["crc_verified"])
        self.assertEqual(s.verify_prepared(self.root / "cache"), manifest)

    def test_archive_symlink_rejected(self):
        archive = self.archive()
        link = self.root / "link.zip"
        link.symlink_to(archive)
        with self.assertRaises(ValueError):
            s.prepare(link, self.root / "cache")

    def test_existing_output_not_overwritten(self):
        cache = self.prepared()
        before = (cache / "manifest.json").read_bytes()
        with self.assertRaises(ValueError):
            s.prepare(self.root / "synthetic.zip", cache)
        self.assertEqual((cache / "manifest.json").read_bytes(), before)

    def test_crc_corruption_records_failure(self):
        archive = self.archive()
        with zipfile.ZipFile(archive) as zipped:
            item = zipped.getinfo(s.DATA)
            offset = item.header_offset + 30 + len(item.filename.encode()) + len(item.extra)
        content = bytearray(archive.read_bytes())
        content[offset + 20] ^= 1
        archive.write_bytes(content)
        output = self.root / "cache"
        with self.assertRaises((zipfile.BadZipFile, ValueError)):
            s.prepare(archive, output)
        result = json.loads((output / "manifest.json").read_text())
        self.assertEqual(result["state"], "failed")
        self.assertIn("archive_sha256", result)
        self.assertFalse((output / s.DATA).exists())

    def test_bad_header_or_eof_cannot_be_prepared(self):
        for label, data in (("header", bgzf(b"#wrong\n")), ("EOF", bgzf_block(point_text().encode()))):
            with self.subTest(label=label):
                output = self.root / label
                with self.assertRaises(ValueError):
                    s.prepare(self.archive(data=data), output)
                self.assertEqual(json.loads((output / "manifest.json").read_text())["state"], "failed")

    def test_archive_change_during_prepare_rejected(self):
        archive = self.archive()
        original = s.identity(archive)
        changed = [*original[:-1], original[-1] + 1]
        with mock.patch.object(s, "identity", side_effect=[original, changed]), self.assertRaises(ValueError):
            s.prepare(archive, self.root / "cache")
        self.assertEqual(json.loads((self.root / "cache/manifest.json").read_text())["state"], "failed")

    def test_cache_hash_drift_rejected(self):
        cache = self.prepared()
        target = cache / s.DATA
        content = bytearray(target.read_bytes())
        content[20] ^= 1
        target.write_bytes(content)
        with self.assertRaises(ValueError):
            s.verify_prepared(cache)

    def test_cache_member_symlink_rejected(self):
        cache = self.prepared()
        target = cache / s.DATA
        replacement = self.root / "same-synthetic-bytes.gz"
        target.rename(replacement)
        target.symlink_to(replacement)
        with self.assertRaises(ValueError):
            s.verify_prepared(cache)

    def test_stale_manifest_state_and_index_rejected(self):
        cache = self.prepared()
        path = cache / "manifest.json"
        original = json.loads(path.read_text())
        for kind in ("state", "index"):
            changed = json.loads(json.dumps(original))
            if kind == "state":
                changed["state"] = "started"
            else:
                changed["index"]["contigs"] = ["changed"]
            path.write_text(json.dumps(changed))
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                s.verify_prepared(cache)


class RowTests(unittest.TestCase):
    def test_zero_is_found_and_all_alternates_retained(self):
        result = s.parse_rows(point_text(), s.CONTROL)
        self.assertEqual(result["state"], "found")
        self.assertEqual(result["merged_splicing_score"], 0)
        self.assertEqual(result["score_text"], "0")
        self.assertEqual(len(result["all_alternate_rows"]), 3)
        self.assertTrue(result["all_three_alternates_present"])

    def test_absent_alternate_and_empty_position_are_missing(self):
        for text in (s.HEADER + "\n", point_text(omit=s.CONTROL[3])):
            with self.subTest(text=text):
                result = s.parse_rows(text, s.CONTROL)
                self.assertEqual(result["state"], "missing")
                self.assertIsNone(result["merged_splicing_score"])
                self.assertIsNone(result["score_text"])

    def test_header_identity_coordinate_and_ref_fail_closed(self):
        chrom, pos, ref, alt = s.CONTROL
        valid = [chrom, str(pos), ref, alt, "0.25"]
        texts = ["", "#wrong\n", point_text().replace(s.HEADER, s.HEADER + "\textra", 1)]
        for offset, value in ((0, "chr1"), (1, str(pos - 1)), (2, "C")):
            cells = valid.copy()
            cells[offset] = value
            texts.append(s.HEADER + "\n" + "\t".join(cells) + "\n")
        for text in texts:
            with self.subTest(text=text), self.assertRaises(ValueError):
                s.parse_rows(text, s.CONTROL)

    def test_invalid_alt_and_nonfinite_or_negative_score_rejected(self):
        chrom, pos, ref, alt = s.CONTROL
        for alternate in ("", "N", "AA", "a", ref):
            text = s.HEADER + f"\n{chrom}\t{pos}\t{ref}\t{alternate}\t0.25\n"
            with self.subTest(alternate=alternate), self.assertRaises(ValueError):
                s.parse_rows(text, s.CONTROL)
        for score in ("NaN", "inf", "-inf", "-0.1", ".", "", "NA"):
            text = s.HEADER + f"\n{chrom}\t{pos}\t{ref}\t{alt}\t{score}\n"
            with self.subTest(score=score), self.assertRaises(ValueError):
                s.parse_rows(text, s.CONTROL)

    def test_duplicate_extra_or_bad_width_rows_rejected(self):
        text = point_text()
        first = text.splitlines()[1]
        for changed in (s.HEADER + "\n" + first + "\n" + first + "\n", text + first + "\n", text.replace(first, first + "\textra")):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                s.parse_rows(changed, s.CONTROL)

    def test_aggregate_is_not_bounded_to_probability(self):
        text = point_text().replace("\t0\n", "\t4.125\n")
        self.assertEqual(s.parse_rows(text, s.CONTROL)["merged_splicing_score"], 4.125)


class ProcessTests(unittest.TestCase):
    def test_bounded_process_returns_ascii(self):
        self.assertEqual(s.run_tabix([sys.executable, "-c", "print('synthetic')"], limit=128), "synthetic\n")

    def test_stdout_and_stderr_limits_enforced_in_child(self):
        for descriptor in (1, 2):
            command = [sys.executable, "-c", f"import os; os.write({descriptor}, b'x' * 1000000)"]
            with self.subTest(descriptor=descriptor), self.assertRaises(ValueError):
                s.run_tabix(command, limit=128)

    def test_warnings_or_nonzero_exit_rejected(self):
        for program in ("import sys; print('warning', file=sys.stderr)", "raise SystemExit(3)"):
            with self.subTest(program=program), self.assertRaises(ValueError):
                s.run_tabix([sys.executable, "-c", program])

    def test_process_timeout_propagates(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            s.run_tabix([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.05)

    def test_non_ascii_output_rejected(self):
        with self.assertRaises(UnicodeError):
            s.run_tabix([sys.executable, "-c", "import os; os.write(1, bytes([255]))"])


class QueryTests(Fixture):
    def lookup(self, cache, output, responses):
        with mock.patch.object(s, "submitted_preflight", return_value={"synthetic": True}), \
                mock.patch.object(s.subprocess, "check_output", return_value="synthetic tabix version"), \
                mock.patch.object(s, "run_tabix", side_effect=responses) as tabix:
            result = s.query(cache, output)
        return result, tabix

    def test_fixed_scope_success_preserves_rows_and_source_hashes(self):
        cache = self.prepared()
        variants = (s.CONTROL, *s.SUBMITTED)
        output = self.root / "results"
        result, tabix = self.lookup(cache, output, [point_text(v) for v in variants])
        self.assertEqual(result["state"], "complete")
        self.assertEqual([r["variant"] for r in result["rows"]], list(variants))
        self.assertEqual(result["network_calls"], 0)
        self.assertFalse(result["source_vcf_read"])
        self.assertEqual(result["phase"], "unconfirmed")
        self.assertEqual(result["source"]["cache_manifest_sha256"], s.digest(cache / "manifest.json"))
        self.assertEqual(result["source"]["archive_sha256"], s.digest(self.root / "synthetic.zip"))
        for call, variant in zip(tabix.call_args_list, variants):
            chrom, position, _, _ = variant
            self.assertEqual(call.args[0], [str(s.TABIX), "-h", str(cache / s.DATA), f"{chrom}:{position}-{position}"])
        self.assertEqual(json.loads((output / "scores.json").read_text())["state"], "complete")

    def test_missing_target_is_partial_and_not_zero(self):
        variants = (s.CONTROL, *s.SUBMITTED)
        responses = [point_text(v, omit=v[3] if i == 1 else None) for i, v in enumerate(variants)]
        result, _ = self.lookup(self.prepared(), self.root / "results", responses)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["rows"][0]["merged_splicing_score"], 0)
        self.assertIsNone(result["rows"][1]["merged_splicing_score"])
        self.assertEqual(result["rows"][1]["state"], "missing")

    def test_later_failure_keeps_prior_success_and_provenance(self):
        cache = self.prepared()
        output = self.root / "results"
        with self.assertRaises(ValueError):
            self.lookup(cache, output, [point_text(), ValueError("synthetic failure")])
        result = json.loads((output / "scores.json").read_text())
        self.assertEqual(result["state"], "failed")
        self.assertEqual(len(result["rows"]), 1)
        self.assertEqual(result["rows"][0]["variant"], list(s.CONTROL))
        self.assertEqual(result["source"]["cache_manifest_sha256"], s.digest(cache / "manifest.json"))

    def test_failed_preflight_makes_no_point_queries(self):
        cache = self.prepared()
        output = self.root / "results"
        with mock.patch.object(s, "submitted_preflight", side_effect=ValueError("synthetic")), \
                mock.patch.object(s, "run_tabix") as tabix, self.assertRaises(ValueError):
            s.query(cache, output)
        tabix.assert_not_called()
        self.assertEqual(json.loads((output / "scores.json").read_text())["state"], "failed")

    def test_corrupt_cache_stops_before_preflight_or_queries(self):
        cache = self.prepared()
        (cache / s.DATA).write_bytes(b"synthetic corruption")
        with mock.patch.object(s, "submitted_preflight") as preflight, \
                mock.patch.object(s, "run_tabix") as tabix, self.assertRaises(ValueError):
            s.query(cache, self.root / "results")
        preflight.assert_not_called()
        tabix.assert_not_called()

    def test_existing_query_output_not_overwritten(self):
        cache = self.prepared()
        output = self.root / "results"
        self.lookup(cache, output, [point_text(v) for v in (s.CONTROL, *s.SUBMITTED)])
        before = (output / "scores.json").read_bytes()
        with self.assertRaises(ValueError):
            s.query(cache, output)
        self.assertEqual((output / "scores.json").read_bytes(), before)

    def test_cli_partial_is_nonzero(self):
        source = self.root / "data/resources/cache"
        output = self.root / "results/feat009/new"
        with mock.patch.object(s, "ROOT", self.root), \
                mock.patch.object(sys, "argv", ["splicing", "query", str(source), str(output)]), \
                mock.patch.object(s, "query", return_value={"state": "partial", "rows": []}), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(s.main(), 2)

    def test_cli_rejects_wrong_input_or_output_scope(self):
        for source, output in ((self.root / "outside", self.root / "results/feat009/new"),
                (self.root / "data/resources/cache", self.root / "outside")):
            with self.subTest(source=source, output=output), mock.patch.object(s, "ROOT", self.root), \
                    mock.patch.object(sys, "argv", ["splicing", "query", str(source), str(output)]), \
                    mock.patch.object(s, "query") as query, self.assertRaises(ValueError):
                s.main()
            query.assert_not_called()

    @unittest.skipUnless(s.TABIX.is_file(), "repository-local Tabix required")
    def test_real_pinned_tabix_roundtrip_on_tiny_bgzf(self):
        source = self.root / s.DATA
        variants = (s.CONTROL, *s.SUBMITTED)
        text = s.HEADER + "\n" + "".join("\n".join(point_text(v).splitlines()[1:]) + "\n" for v in variants)
        source.write_bytes(bgzf(text.encode()))
        subprocess.run([str(s.TABIX), "-p", "vcf", str(source)],
            check=True, capture_output=True, timeout=5)
        archive = self.root / "real-tabix-synthetic.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as zipped:
            zipped.write(source, s.DATA)
            zipped.write(Path(str(source) + ".tbi"), s.INDEX)
        cache = self.root / "cache"
        s.prepare(archive, cache)
        with mock.patch.object(s, "submitted_preflight", return_value={"synthetic": True}):
            result = s.query(cache, self.root / "results")
        self.assertEqual(result["state"], "complete")
        self.assertEqual(len(result["rows"]), 3)
        self.assertTrue(all(r["all_three_alternates_present"] for r in result["rows"]))
        self.assertTrue(all(r["merged_splicing_score"] == 0 for r in result["rows"]))


if __name__ == "__main__":
    unittest.main()
