"""Behavior tests for the optional, offline evidence checker (stdlib only)."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location("check_evidence", REPO / "scripts/check_evidence.py")
CHECKER = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(CHECKER)


class EvidenceCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.directory = self.workspace / "case"
        shutil.copytree(REPO / "examples/evidence-demo", self.directory)
        self.path = self.directory / "manifest.json"
        self.manifest = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(json.dumps(self.manifest, indent=2) + "\n", encoding="utf-8")

    def errors(self):
        self.save()
        return "\n".join(CHECKER.check_manifest(self.path).errors)

    def refresh_hash(self, artifact_id):
        import hashlib
        artifact = next(item for item in self.manifest["artifacts"] if item["id"] == artifact_id)
        artifact["sha256"] = hashlib.sha256((self.directory / artifact["path"]).read_bytes()).hexdigest()

    def baseline(self):
        path = self.workspace / "baseline"
        shutil.copytree(REPO / "examples/evidence-demo", path)
        return CHECKER.check_manifest(path / "manifest.json")

    def test_complete_demo_passes_and_evaluator_recomputes_predictions(self):
        self.assertEqual(self.errors(), "")
        result = subprocess.run([sys.executable, str(self.directory / "evaluate.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        metrics = json.loads((self.directory / "metrics.json").read_text(encoding="utf-8"))
        self.assertEqual((metrics["accuracy"], metrics["correct"], metrics["total"]), (0.75, 3, 4))
        # Re-evaluation is deterministic, including the hashed output bytes.
        self.assertEqual(self.errors(), "")

    def test_evaluator_rejects_duplicate_prediction_ids(self):
        path = self.directory / "predictions.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[1]["id"] = records[0]["id"]
        path.write_text(json.dumps(records), encoding="utf-8")
        result = subprocess.run([sys.executable, str(self.directory / "evaluate.py")], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unique", result.stderr)

    def test_artifact_tampering_is_detected(self):
        with (self.directory / "report.md").open("a", encoding="utf-8") as stream:
            stream.write("Unrecorded change.\n")
        self.assertIn("recorded hash", self.errors())

    def test_missing_file_is_detected(self):
        (self.directory / "metrics.json").unlink()
        self.assertIn("file does not exist", self.errors())

    def test_running_or_failed_run_cannot_support_claims(self):
        for state in ("planned", "running", "failed", "cancelled"):
            with self.subTest(state=state):
                self.manifest["status"] = state
                self.assertIn("evidence claims require", self.errors())
        self.manifest["status"] = "running"
        self.manifest["claims"] = []
        self.manifest["validity"] = {"status": "unreviewed", "checks": []}
        for key in ("limit", "used", "remaining", "max_attempts", "attempt"):
            self.manifest["budget"][key] = None
        self.assertEqual(self.errors(), "")

    def test_passed_validity_requires_nonempty_passed_evidence_checks(self):
        self.manifest["validity"]["checks"] = []
        self.assertIn("at least one check", self.errors())
        self.manifest["validity"]["checks"] = [{"name": "empty", "status": "passed", "evidence": []}]
        self.assertIn("artifact reference", self.errors())
        self.manifest["validity"] = {"status": "failed", "checks": []}
        self.assertIn("evidence claims require", self.errors())

    def test_forged_metric_and_claim_numbers_are_detected(self):
        self.manifest["claims"][0]["reported_value"] = 0.99
        self.assertIn("beyond absolute_tolerance", self.errors())
        self.manifest["metrics"]["accuracy"]["value"] = 0.99
        self.assertIn("does not equal the JSON source value", self.errors())

    def test_explicit_claim_rounding_tolerance(self):
        self.manifest["claims"][0]["reported_value"] = 0.8
        self.manifest["claims"][0]["absolute_tolerance"] = 0.051
        self.assertEqual(self.errors(), "")
        self.manifest["claims"][0]["absolute_tolerance"] = -1
        self.assertIn("non-negative", self.errors())

    def test_matching_baseline_passes(self):
        self.save()
        current = CHECKER.check_manifest(self.path)
        self.assertEqual(CHECKER.compare_results(current, self.baseline()), [])

    def test_changed_split_id_and_changed_split_bytes_are_detected(self):
        baseline = self.baseline()
        self.manifest["evaluation"]["split_id"] = "different-split"
        self.save()
        self.assertIn("evaluation.split_id", "\n".join(CHECKER.compare_results(CHECKER.check_manifest(self.path), baseline)))
        self.manifest["evaluation"]["split_id"] = "synthetic-test-v1"
        path = self.directory / "split.json"
        split = json.loads(path.read_text(encoding="utf-8"))
        split["test_ids"][0] = "different-record"
        path.write_text(json.dumps(split), encoding="utf-8")
        self.refresh_hash("split")
        self.save()
        current = CHECKER.check_manifest(self.path)
        self.assertEqual(current.errors, [])
        self.assertIn("split_artifact content hash", "\n".join(CHECKER.compare_results(current, baseline)))

    def test_changed_protocol_data_or_metric_definition_is_detected(self):
        baseline = self.baseline()
        for section, key in (("evaluation", "protocol_version"), ("evaluation", "selection_scope"),
                             ("evaluation", "aggregation"), ("provenance", "data_version")):
            with self.subTest(section=section, key=key):
                original = self.manifest[section][key]
                self.manifest[section][key] = "different"
                self.save()
                errors = CHECKER.compare_results(CHECKER.check_manifest(self.path), baseline)
                self.assertIn(section + "." + key, "\n".join(errors))
                self.manifest[section][key] = original
        for key, value in (("definition", "balanced accuracy"), ("unit", "percent"), ("direction", "lower")):
            with self.subTest(metric_field=key):
                original = self.manifest["metrics"]["accuracy"][key]
                self.manifest["metrics"]["accuracy"][key] = value
                self.save()
                errors = CHECKER.compare_results(CHECKER.check_manifest(self.path), baseline)
                self.assertIn("metrics.accuracy." + key, "\n".join(errors))
                self.manifest["metrics"]["accuracy"][key] = original

    def test_parent_path_absolute_path_and_symlink_escape_are_rejected(self):
        artifact = self.manifest["artifacts"][0]
        outside = self.workspace / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        artifact["path"] = "../outside.md"
        self.assertIn("escapes the artifact root", self.errors())
        artifact["path"] = str(outside)
        self.assertIn("must be relative", self.errors())
        (self.directory / "escape.md").symlink_to(outside)
        artifact["path"] = "escape.md"
        self.assertIn("including symlinks", self.errors())

    def test_explicit_root_changes_relative_path_resolution(self):
        for artifact in self.manifest["artifacts"]:
            artifact["path"] = "case/" + artifact["path"]
        self.save()
        self.assertEqual(CHECKER.check_manifest(self.path, self.workspace).errors, [])
        self.assertIn("outside --root", "\n".join(CHECKER.check_manifest(self.path, self.directory / "nested").errors))

    def test_manifest_symlink_cannot_silently_change_the_default_root(self):
        link = self.workspace / "manifest-link.json"
        link.symlink_to(self.path)
        # The containing directory is the explicit artifact root here, so this is allowed.
        self.assertNotIn("outside --root", "\n".join(CHECKER.check_manifest(link).errors))
        nested = self.workspace / "nested"
        nested.mkdir()
        (nested / "escape.json").symlink_to(self.path)
        self.assertIn("including symlinks", "\n".join(CHECKER.check_manifest(nested / "escape.json").errors))

    def test_nonfinite_and_wrong_numeric_types_report_errors_without_crashing(self):
        for value in (True, "0.75", [], {}, None, float("inf"), float("nan"), 10 ** 400):
            with self.subTest(value_type=type(value).__name__):
                self.manifest["metrics"]["accuracy"]["value"] = value
                self.assertNotEqual(self.errors(), "")
        self.manifest["metrics"]["accuracy"]["value"] = 0.75
        for value in (True, "0.75", [], {}, None, 1e309):
            with self.subTest(source_type=type(value).__name__):
                (self.directory / "metrics.json").write_text(json.dumps({"accuracy": value}), encoding="utf-8")
                self.refresh_hash("metrics")
                self.assertNotEqual(self.errors(), "")

    def test_invalid_containers_and_references_report_errors_without_crashing(self):
        for key, value in (("artifacts", {}), ("metrics", []), ("claims", {}), ("validity", []),
                           ("budget", False), ("job", "local"), ("spec", None), ("provenance", []), ("evaluation", [])):
            with self.subTest(field=key):
                original = self.manifest[key]
                self.manifest[key] = value
                self.assertNotEqual(self.errors(), "")
                self.manifest[key] = original
        self.manifest["metrics"]["accuracy"]["source_artifact"] = ["not-a-string"]
        self.assertNotEqual(self.errors(), "")

    def test_rfc6901_escaping_and_invalid_pointers(self):
        (self.directory / "metrics.json").write_text(json.dumps({"a/b": {"m~n": [0.75]}}), encoding="utf-8")
        self.refresh_hash("metrics")
        metric = self.manifest["metrics"]["accuracy"]
        metric["pointer"] = "/a~1b/m~0n/0"
        self.assertEqual(self.errors(), "")
        for pointer in ("a/b", "/a~2b", "/a~1b/m~0n/01", "/absent", [], None):
            with self.subTest(pointer=pointer):
                metric["pointer"] = pointer
                self.assertNotEqual(self.errors(), "")

    def test_malformed_json_missing_schema_and_duplicate_ids_are_rejected(self):
        self.path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
        self.assertIn("duplicate JSON key", "\n".join(CHECKER.check_manifest(self.path).errors))
        self.path.write_text("[", encoding="utf-8")
        self.assertIn("cannot read JSON", "\n".join(CHECKER.check_manifest(self.path).errors))
        self.manifest.pop("schema_version")
        self.assertIn("schema_version", self.errors())
        self.manifest["artifacts"].append(dict(self.manifest["artifacts"][0]))
        self.assertIn("duplicate artifact id", self.errors())

    def test_cli_returns_nonzero_for_invalid_current_and_baseline(self):
        command = [sys.executable, str(REPO / "scripts/check_evidence.py"), str(self.path)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        baseline_path = self.workspace / "baseline"
        shutil.copytree(REPO / "examples/evidence-demo", baseline_path)
        (baseline_path / "report.md").write_text("tampered", encoding="utf-8")
        result = subprocess.run(command + ["--compare", str(baseline_path / "manifest.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("[baseline]", result.stderr)
        self.manifest["claims"][0]["reported_value"] = 1.0
        self.save()
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("[current]", result.stderr)


if __name__ == "__main__":
    unittest.main()
