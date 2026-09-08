#!/usr/bin/env python3
"""Synthetic-only release integrity tests; no actual packages or subject inputs."""
from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import track2_release as release


REPORT_WORDS = (
    "research draft 3", "trans phase remains unconfirmed", "Fireworks", "GLM",
    "Google DeepMind", "not used to train", "Acknowledgement", "pralatrexate",
    "0.08699", "0.04813", "mitotic slippage",
)
PITCH_WORDS = ("Fireworks", "Google DeepMind", "phase unconfirmed", "not a recorded")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReleaseFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="track2-release-offline-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.v2 = self.root / "results/feat009/jvv7_track2_research_v2"
        self.v2.mkdir(parents=True)
        write_json(self.v2 / "manifest.json", {"synthetic": "immutable historical v2"})
        (self.v2 / "sentinel.md").write_text("Historical bytes must not change.\n")
        self.v2_bytes = {p.name: p.read_bytes() for p in self.v2.iterdir()}
        self.out = self.root / "results/feat009/synthetic_v3"
        for name in release.INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Synthetic fixture for " + name + "\n")
        self.report = self.root / release.FILES["jvv7_track2_report_v3.md"]
        self.pitch = self.root / release.FILES["jvv7_track2_pitch_v3.md"]
        self.report.write_text("\n".join(REPORT_WORDS) + "\n")
        self.pitch.write_text("\n".join(PITCH_WORDS) + "\n")
        self.sources = {"schema_version": 1, "sources": [{
            "id": "synthetic_source", "title": "Synthetic public source",
            "url": "https://www.jci.org/articles/view/123", "kind": "primary",
            "model": "synthetic cells", "reading": "synthetic fixture",
            "claim": "No clinical efficacy", "limit": "Synthetic; not evidence",
        }]}
        candidate = {key: "synthetic fixture" for key in (
            "name", "role", "jurisdiction", "approved_use", "target_direction",
            "bridge", "normal_tissue_risk", "exposure_gap", "falsifier", "next_test",
        )}
        candidate.update(id="synthetic_candidate", approval="not_verified", decision="exclude",
                         evidence_level="mechanistic_tool", direct_pair_evidence=False,
                         clinical_efficacy="unestablished", support=["synthetic_source"],
                         counterevidence=["synthetic_source"], clinical_exposure_margin=None)
        self.candidates = {"schema_version": 1, "phase": "unconfirmed",
                           "clinical_use": "research_only", "candidates": [candidate]}
        write_json(self.root / "notes/track2-sources.json", self.sources)
        write_json(self.root / "notes/track2-candidates.json", self.candidates)
        write_json(self.root / "notes/track2-exposure.json", {"synthetic": "upstream audit mocked"})
        self.track1 = {"unchanged_local_v4_hashes": {"synthetic.csv": "a" * 64},
                       "uploaded_bytes_independently_verified": False}
        self.start_patch(patch.object(release, "ROOT", self.root))
        self.start_patch(patch.object(release, "V2", self.v2))
        # The real v2 and Track 1 packages are deliberately never opened.  This
        # stand-in checks v2's immutable tree; real ledger validation remains active.
        self.verify_v2 = self.start_patch(patch.object(release.base, "verify", side_effect=self.check_v2))
        self.track1_check = self.start_patch(patch.object(release.base, "check_track1", return_value=self.track1))
        self.load = self.start_patch(patch.object(release.base, "load_ledgers", side_effect=self.load_ledgers))

    def start_patch(self, patcher):
        value = patcher.start()
        self.addCleanup(patcher.stop)
        return value

    def check_v2(self, path):
        if path != self.v2 or {p.name for p in path.iterdir()} != set(self.v2_bytes):
            raise ValueError("historical package tree changed")
        if any((path / name).read_bytes() != value for name, value in self.v2_bytes.items()):
            raise ValueError("historical package bytes changed")
        return {"integrity_verified": True}

    def load_ledgers(self):
        sources = json.loads((self.root / "notes/track2-sources.json").read_text())
        candidates = json.loads((self.root / "notes/track2-candidates.json").read_text())
        release.base.validate(sources, candidates)
        return sources, candidates

    def build(self):
        result = release.build(self.out)
        self.assertTrue(result["integrity_verified"])
        return result

    def manifest(self):
        return json.loads((self.out / "manifest.json").read_text())

    def put_manifest(self, value):
        write_json(self.out / "manifest.json", value)


class BuildTests(ReleaseFixture):
    def test_exact_file_and_input_sets(self):
        self.build()
        expected = {
            "jvv7_track2_report_v3.md", "jvv7_track2_pitch_v3.md", "sources.json",
            "candidates.json", "exposure.json", "validation-plan.md", "validation-addendum.md",
            "scientific-exposure-review.md", "firecrawl-scientific-review.md",
            "firecrawl-capabilities.md", "firecrawl-run-review.md", "alphagenome-authenticated.md",
            "alphagenome-splicing.md", "alphagenome-score-semantics.md", "alphagenome-splicing-semantics.md",
        }
        self.assertEqual(set(release.FILES), expected)
        self.assertEqual({p.name for p in self.out.iterdir()}, expected | {"manifest.json"})
        manifest = self.manifest()
        self.assertEqual(set(manifest["files"]), expected)
        self.assertEqual(set(manifest["input_hashes"]), release.INPUTS)
        self.assertTrue({"scripts/track2_release.py", "scripts/test_track2_release.py",
                         "scripts/track2_firecrawl.py", "scripts/test_track2_firecrawl.py"} <= release.INPUTS)

    def test_copies_and_hashes_bind_exact_source_bytes(self):
        self.build()
        manifest = self.manifest()
        for name, source in release.FILES.items():
            self.assertEqual((self.out / name).read_bytes(), (self.root / source).read_bytes())
            self.assertEqual(manifest["files"][name], sha(self.out / name))
            self.assertEqual(manifest["files"][name], manifest["input_hashes"][source])
        self.assertEqual(manifest["historical_v2_manifest_sha256"], sha(self.v2 / "manifest.json"))
        self.assertEqual(manifest["track1"], self.track1)

    def test_build_preserves_v2_and_source_inputs(self):
        before = {name: (self.root / name).read_bytes() for name in release.INPUTS}
        self.build()
        self.check_v2(self.v2)
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in release.INPUTS})

    def test_draft_state_never_claims_upload_video_phase_or_margin(self):
        result = self.build()
        manifest = self.manifest()
        self.assertEqual(manifest["schema_version"], 3)
        self.assertEqual(manifest["stage"], "research_draft_not_submitted")
        self.assertIs(manifest["upload_performed"], False)
        self.assertIs(manifest["upload_ready"], False)
        self.assertIsNone(manifest["video_url"])
        self.assertIsNone(manifest["clinical_exposure_margin"])
        self.assertEqual(manifest["phase"], "unconfirmed")
        self.assertIs(result["upload_ready"], False)

    def test_rejects_existing_destination_without_overwrite(self):
        self.out.mkdir()
        sentinel = self.out / "sentinel"
        sentinel.write_text("retain exact bytes")
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.verify_v2.assert_not_called()
        self.assertEqual(list(self.out.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_text(), "retain exact bytes")

    def test_rejects_existing_file_destination(self):
        self.out.write_text("preserve file")
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertEqual(self.out.read_text(), "preserve file")

    def test_rejects_output_root_outside_and_v2(self):
        for path in (self.root / "outside", self.root / "results/feat009", self.v2):
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.build(path)
        self.check_v2(self.v2)

    def test_rejects_descendant_of_v2_before_any_write(self):
        nested = self.v2 / "new_snapshot"
        with self.assertRaises(ValueError):
            release.build(nested)
        self.assertFalse(nested.exists(), "must reject before mutating the historical package")
        self.check_v2(self.v2)

    def test_rejects_v1_and_descendants_before_any_write(self):
        v1 = self.root / "results/feat009/jvv7_track2_research_v1"
        v1.mkdir()
        (v1 / "sentinel").write_text("historical v1")
        for path in (v1, v1 / "nested_snapshot"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.build(path)
        self.assertEqual({p.name for p in v1.iterdir()}, {"sentinel"})
        self.assertEqual((v1 / "sentinel").read_text(), "historical v1")

    def test_parent_alias_cannot_bypass_historical_v2_gate(self):
        alias = self.root / "results/feat009/history_alias"
        alias.symlink_to(self.v2, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.build(alias / "nested_snapshot")
        self.check_v2(self.v2)

    def test_rejects_symlink_destination(self):
        self.out.symlink_to(self.v2, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertTrue(self.out.is_symlink())
        self.check_v2(self.v2)

    def test_resolved_parent_symlink_cannot_escape_output_root(self):
        outside = self.root / "outside"
        outside.mkdir()
        alias = self.root / "results/feat009/alias"
        alias.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.build(alias / "new")
        self.assertEqual(list(outside.iterdir()), [])

    def test_missing_and_symlinked_inputs_fail_before_build(self):
        name = "scripts/test_track2_release.py"
        path = self.root / name
        original = path.read_bytes()
        path.unlink()
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())
        target = self.root / "synthetic_target"
        target.write_bytes(original)
        path.symlink_to(target)
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_input_drift_during_build_does_not_produce_valid_manifest(self):
        real_copy = release.shutil.copyfile
        changed = False
        def copy_with_drift(source, target):
            nonlocal changed
            value = real_copy(source, target)
            if not changed:
                changed = True
                path = self.root / "scripts/track2_firecrawl.py"
                path.write_text("Changed during build")
            return value
        with patch.object(release.shutil, "copyfile", side_effect=copy_with_drift):
            with self.assertRaises(ValueError):
                release.build(self.out)
        self.assertFalse((self.out / "manifest.json").exists())
        self.check_v2(self.v2)

    def test_upstream_v2_failure_stops_before_output_creation(self):
        self.verify_v2.side_effect = ValueError("synthetic v2 failure")
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_track1_failure_does_not_create_verified_snapshot(self):
        self.track1_check.side_effect = ValueError("synthetic Track 1 drift")
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse((self.out / "manifest.json").exists())
        self.check_v2(self.v2)


class BoundaryTests(ReleaseFixture):
    def test_each_report_boundary_is_required(self):
        for word in REPORT_WORDS:
            with self.subTest(word=word):
                self.report.write_text("\n".join(x for x in REPORT_WORDS if x != word))
                with self.assertRaises(ValueError):
                    release.build(self.out)
                self.assertFalse(self.out.exists())

    def test_each_pitch_boundary_is_required(self):
        for word in PITCH_WORDS:
            with self.subTest(word=word):
                self.pitch.write_text("\n".join(x for x in PITCH_WORDS if x != word))
                with self.assertRaises(ValueError):
                    release.build(self.out)
                self.assertFalse(self.out.exists())

    def test_obsolete_provider_attestation_is_rejected(self):
        self.report.write_text(self.report.read_text() + "\nNo other AI providers have been used.\n")
        with self.assertRaises(ValueError):
            release.build(self.out)
        self.assertFalse(self.out.exists())

    def test_case_insensitive_boundaries(self):
        self.report.write_text(self.report.read_text().upper())
        self.pitch.write_text(self.pitch.read_text().upper())
        self.build()

    def test_candidate_phase_and_clinical_use_are_validated(self):
        for field, bad in (("phase", "confirmed_trans"), ("clinical_use", "clinical_treatment")):
            with self.subTest(field=field):
                altered = copy.deepcopy(self.candidates)
                altered[field] = bad
                write_json(self.root / "notes/track2-candidates.json", altered)
                with self.assertRaises(ValueError):
                    release.build(self.out)
                self.assertFalse(self.out.exists())

    def test_candidate_exposure_margin_must_be_explicit_null(self):
        for value in (1.5, 0, False, "unknown", "missing"):
            with self.subTest(value=value):
                altered = copy.deepcopy(self.candidates)
                if value == "missing":
                    del altered["candidates"][0]["clinical_exposure_margin"]
                else:
                    altered["candidates"][0]["clinical_exposure_margin"] = value
                write_json(self.root / "notes/track2-candidates.json", altered)
                with self.assertRaises(ValueError):
                    release.build(self.out)
                self.assertFalse(self.out.exists())

    def test_unestablished_efficacy_and_pair_intervention_evidence(self):
        for field, bad in (("direct_pair_evidence", True), ("clinical_efficacy", "established")):
            with self.subTest(field=field):
                altered = copy.deepcopy(self.candidates)
                altered["candidates"][0][field] = bad
                write_json(self.root / "notes/track2-candidates.json", altered)
                with self.assertRaises(ValueError):
                    release.build(self.out)
                self.assertFalse(self.out.exists())


class VerifyTests(ReleaseFixture):
    def setUp(self):
        super().setUp()
        self.build()

    def test_plain_package_tamper_is_rejected(self):
        (self.out / "validation-addendum.md").write_text("tampered")
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_updated_package_hash_cannot_hide_source_mismatch(self):
        path = self.out / "validation-addendum.md"
        path.write_text("tampered")
        manifest = self.manifest()
        manifest["files"][path.name] = sha(path)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_missing_file_or_extra_file_rejected(self):
        extra = self.out / "extra.txt"
        extra.write_text("unexpected")
        with self.assertRaises(ValueError):
            release.verify(self.out)
        extra.unlink()
        (self.out / "validation-addendum.md").unlink()
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_manifest_file_set_cannot_be_shortened(self):
        manifest = self.manifest()
        del manifest["files"]["validation-addendum.md"]
        self.put_manifest(manifest)
        (self.out / "validation-addendum.md").unlink()
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_manifest_input_set_cannot_be_shortened_or_expanded(self):
        original = self.manifest()
        for action in ("remove", "add"):
            with self.subTest(action=action):
                manifest = copy.deepcopy(original)
                if action == "remove":
                    del manifest["input_hashes"]["scripts/test_track2_release.py"]
                else:
                    manifest["input_hashes"]["notes/invented.md"] = "a" * 64
                self.put_manifest(manifest)
                with self.assertRaises(ValueError):
                    release.verify(self.out)

    def test_source_and_script_input_drift_rejected(self):
        for name in ("notes/track2-validation-v3.md", "scripts/test_track2_release.py"):
            path = self.root / name
            original = path.read_bytes()
            path.write_text("current input changed")
            with self.subTest(name=name), self.assertRaises(ValueError):
                release.verify(self.out)
            path.write_bytes(original)

    def test_symlink_package_file_rejected_even_for_identical_bytes(self):
        name = "validation-addendum.md"
        path = self.out / name
        path.unlink()
        path.symlink_to(self.root / release.FILES[name])
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_symlink_manifest_rejected_even_for_identical_bytes(self):
        target = self.root / "saved-manifest.json"
        target.write_bytes((self.out / "manifest.json").read_bytes())
        (self.out / "manifest.json").unlink()
        (self.out / "manifest.json").symlink_to(target)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_symlink_package_directory_rejected(self):
        alias = self.root / "results/feat009/package_alias"
        alias.symlink_to(self.out, target_is_directory=True)
        with self.assertRaises(ValueError):
            release.verify(alias)

    def test_invalid_stage_and_version_rejected(self):
        original = self.manifest()
        for key, value in (("schema_version", 2), ("stage", "submitted")):
            manifest = copy.deepcopy(original)
            manifest[key] = value
            self.put_manifest(manifest)
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_false_ready_upload_and_video_claims_rejected(self):
        original = self.manifest()
        for key, value in (("upload_ready", True), ("upload_ready", 0),
                           ("upload_performed", True), ("upload_performed", 0),
                           ("video_url", "https://example.org/video")):
            manifest = copy.deepcopy(original)
            manifest[key] = value
            self.put_manifest(manifest)
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_phase_and_explicit_null_margin_gates(self):
        original = self.manifest()
        for key, value in (("phase", "confirmed_trans"), ("clinical_exposure_margin", 0),
                           ("clinical_exposure_margin", False), ("clinical_exposure_margin", "unknown")):
            manifest = copy.deepcopy(original)
            manifest[key] = value
            self.put_manifest(manifest)
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                release.verify(self.out)
        manifest = copy.deepcopy(original)
        del manifest["clinical_exposure_margin"]
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_historical_hash_and_track1_attestation_tamper_rejected(self):
        original = self.manifest()
        for key, value in (("historical_v2_manifest_sha256", "0" * 64), ("track1", {})):
            manifest = copy.deepcopy(original)
            manifest[key] = value
            self.put_manifest(manifest)
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.verify(self.out)

    def test_historical_actual_drift_rejected(self):
        (self.v2 / "sentinel.md").write_text("changed historical bytes")
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_baseline_check_summary_tamper_rejected(self):
        manifest = self.manifest()
        manifest["base_ledger_checks"]["direct_pair_intervention_evidence"] = 1
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_revalidation_rejects_forged_candidate_even_with_matching_hashes(self):
        changed = copy.deepcopy(self.candidates)
        changed["phase"] = "confirmed_trans"
        source = self.root / "notes/track2-candidates.json"
        copied = self.out / "candidates.json"
        write_json(source, changed)
        write_json(copied, changed)
        manifest = self.manifest()
        manifest["files"]["candidates.json"] = sha(copied)
        manifest["input_hashes"]["notes/track2-candidates.json"] = sha(source)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_revalidation_rejects_missing_disclosure_with_matching_hashes(self):
        changed = self.report.read_text().replace("Fireworks", "")
        self.report.write_text(changed)
        copied = self.out / "jvv7_track2_report_v3.md"
        copied.write_text(changed)
        manifest = self.manifest()
        manifest["files"][copied.name] = sha(copied)
        manifest["input_hashes"][release.FILES[copied.name]] = sha(self.report)
        self.put_manifest(manifest)
        with self.assertRaises(ValueError):
            release.verify(self.out)

    def test_verify_cli_is_read_only(self):
        before = {p.name: p.read_bytes() for p in self.out.iterdir()}
        with patch("sys.argv", ["test", "verify", str(self.out)]), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            release.main()
        self.assertTrue(json.loads(stdout.getvalue())["integrity_verified"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.out.iterdir()})


if __name__ == "__main__":
    unittest.main()
