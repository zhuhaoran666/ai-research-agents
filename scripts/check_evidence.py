#!/usr/bin/env python3
"""Check a local run manifest's artifact integrity and recorded evidence chain.

Python 3.9+, standard library only. This never executes experiments, reads network
resources, judges scientific validity, or enforces a running job's budget.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys


RUN_STATUSES = {"planned", "running", "completed", "failed", "cancelled"}
CHECK_STATUSES = {"unreviewed", "passed", "failed"}
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def is_number(value):
    try:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:
        return False


def within_root(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {!r}".format(key))
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number: " + value)


def read_json(path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=unique_object, parse_constant=reject_constant)


def json_pointer(document, pointer):
    """Resolve RFC 6901 syntax, rejecting ambiguous or invalid array indices."""
    if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
        raise ValueError("must be an RFC 6901 JSON pointer (empty or beginning with '/')")
    current = document
    if pointer == "":
        return current
    for encoded in pointer[1:].split("/"):
        if re.search(r"~(?![01])", encoded):
            raise ValueError("invalid '~' escape in JSON pointer")
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise ValueError("JSON pointer key {!r} is absent".format(token))
            current = current[token]
        elif isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("JSON pointer array index must be a non-negative integer")
            index = int(token)
            if index >= len(current):
                raise ValueError("JSON pointer array index is out of bounds")
            current = current[index]
        else:
            raise ValueError("JSON pointer traverses a scalar")
    return current


class CheckResult:
    def __init__(self, manifest_path, root):
        self.path = manifest_path
        self.root = root
        self.data = {}
        self.artifacts = {}
        self.files = {}
        self.errors = []

    def error(self, location, message):
        self.errors.append("{}: {}".format(location, message))

    def text(self, value, location, nullable=False):
        if nullable and value is None:
            return True
        if not isinstance(value, str) or not value.strip():
            self.error(location, "must be a non-empty string" + (" or null" if nullable else ""))
            return False
        return True

    def object(self, value, location):
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return {}
        return value

    def fields(self, value, names, location):
        for name in names:
            if name not in value:
                self.error(location + "." + name, "required field is absent (use null when unknown and allowed)")

    def array(self, value, location):
        if not isinstance(value, list):
            self.error(location, "must be an array")
            return []
        return value

    def number(self, value, location, nullable=False, integer=False):
        if nullable and value is None:
            return True
        if not is_number(value) or (integer and not isinstance(value, int)):
            self.error(location, "must be a finite {}{}".format(
                "integer" if integer else "number", " or null" if nullable else ""))
            return False
        return True

    def enum(self, value, allowed, location):
        if not isinstance(value, str) or value not in allowed:
            self.error(location, "must be one of " + ", ".join(sorted(allowed)))

    def ref(self, value, location):
        if self.text(value, location) and value not in self.artifacts:
            self.error(location, "unknown artifact id {!r}".format(value))


def check_manifest(manifest_path, root=None):
    """Return all discoverable errors without executing artifact contents."""
    requested = Path(manifest_path)
    try:
        resolved = requested.resolve()
        artifact_root = Path(root).resolve() if root is not None else requested.absolute().parent.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        result = CheckResult(requested, Path("."))
        result.error("manifest", "cannot resolve path: " + str(exc))
        return result
    result = CheckResult(resolved, artifact_root)
    if not within_root(resolved, artifact_root):
        result.error("manifest", "path is outside --root or the containing directory (including symlinks)")
        return result
    try:
        data = read_json(resolved)
    except (OSError, ValueError, RecursionError) as exc:
        result.error("manifest", "cannot read JSON: " + str(exc))
        return result
    result.data = result.object(data, "manifest")
    data = result.data
    result.fields(data, ("schema_version", "run_id", "spec", "parent_run_id", "reason", "status",
                         "validity", "provenance", "evaluation", "job", "budget", "artifacts", "metrics", "claims"), "manifest")
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        result.error("schema_version", "must be integer 1")
    result.text(data.get("run_id"), "run_id")
    result.text(data.get("parent_run_id"), "parent_run_id", nullable=True)
    result.text(data.get("reason"), "reason")
    result.enum(data.get("status"), RUN_STATUSES, "status")

    for index, item in enumerate(result.array(data.get("artifacts"), "artifacts")):
        location = "artifacts[{}]".format(index)
        artifact = result.object(item, location)
        artifact_id = artifact.get("id")
        valid_id = result.text(artifact_id, location + ".id")
        if valid_id and artifact_id in result.artifacts:
            result.error(location + ".id", "duplicate artifact id")
            continue
        if valid_id:
            result.artifacts[artifact_id] = artifact
        expected_hash = artifact.get("sha256")
        if not isinstance(expected_hash, str) or not SHA256.fullmatch(expected_hash):
            result.error(location + ".sha256", "must contain 64 hexadecimal characters")
        artifact_path = artifact.get("path")
        if not result.text(artifact_path, location + ".path"):
            continue
        try:
            relative = Path(artifact_path)
            if relative.is_absolute():
                result.error(location + ".path", "must be relative to the artifact root")
                continue
            actual_path = (artifact_root / relative).resolve()
            if not within_root(actual_path, artifact_root):
                result.error(location + ".path", "escapes the artifact root (including symlinks)")
                continue
            if not actual_path.is_file():
                result.error(location + ".path", "file does not exist or is not a regular file")
                continue
            digest = hashlib.sha256()
            with actual_path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            if isinstance(expected_hash, str) and digest.hexdigest() != expected_hash.lower():
                result.error(location + ".sha256", "file content differs from the recorded hash")
            if valid_id:
                result.files[artifact_id] = actual_path
        except (OSError, RuntimeError, ValueError) as exc:
            result.error(location + ".path", "cannot inspect file: " + str(exc))

    spec = result.object(data.get("spec"), "spec")
    for field in ("id", "version"):
        result.text(spec.get(field), "spec." + field)
    result.ref(spec.get("artifact"), "spec.artifact")
    provenance = result.object(data.get("provenance"), "provenance")
    for field in ("code_revision", "data_id", "data_version"):
        result.text(provenance.get(field), "provenance." + field)
    for field in ("code_artifact", "config_artifact", "split_artifact", "environment_artifact"):
        result.ref(provenance.get(field), "provenance." + field)
    evaluation = result.object(data.get("evaluation"), "evaluation")
    for field in ("protocol_id", "protocol_version", "split_id", "selection_scope", "aggregation"):
        result.text(evaluation.get(field), "evaluation." + field)
    job = result.object(data.get("job"), "job")
    result.fields(job, ("id", "backend", "last_checked_at"), "job")
    for field in ("id", "backend", "last_checked_at"):
        result.text(job.get(field), "job." + field, nullable=True)
    budget = result.object(data.get("budget"), "budget")
    result.fields(budget, ("unit", "limit", "used", "remaining", "max_attempts", "attempt", "stop_reason"), "budget")
    result.text(budget.get("unit"), "budget.unit")
    result.text(budget.get("stop_reason"), "budget.stop_reason", nullable=True)
    for field in ("limit", "used", "remaining", "max_attempts", "attempt"):
        value = budget.get(field)
        if result.number(value, "budget." + field, nullable=True,
                         integer=field in ("max_attempts", "attempt")) and value is not None and value < 0:
            result.error("budget." + field, "must be non-negative")
    limit, used, remaining = (budget.get(field) for field in ("limit", "used", "remaining"))
    if all(is_number(value) and value >= 0 for value in (limit, used, remaining)):
        if not math.isclose(remaining, max(0, limit - used), rel_tol=1e-9, abs_tol=1e-9):
            result.error("budget.remaining", "must equal max(0, limit - used) for supplied counters")

    validity = result.object(data.get("validity"), "validity")
    result.enum(validity.get("status"), CHECK_STATUSES, "validity.status")
    checks = result.array(validity.get("checks"), "validity.checks")
    for index, item in enumerate(checks):
        location = "validity.checks[{}]".format(index)
        check = result.object(item, location)
        result.text(check.get("name"), location + ".name")
        result.enum(check.get("status"), CHECK_STATUSES, location + ".status")
        evidence = result.array(check.get("evidence"), location + ".evidence")
        if check.get("status") == "passed" and not evidence:
            result.error(location + ".evidence", "a passed check requires at least one artifact reference")
        for ref_index, artifact_id in enumerate(evidence):
            result.ref(artifact_id, "{}.evidence[{}]".format(location, ref_index))
    if validity.get("status") == "passed":
        if not checks or any(not isinstance(check, dict) or check.get("status") != "passed" for check in checks):
            result.error("validity.checks", "passed validity requires at least one check and all checks passed")

    metrics = result.object(data.get("metrics"), "metrics")
    sources = {}
    for name, item in metrics.items():
        location = "metrics." + str(name)
        result.text(name, location + " (name)")
        metric = result.object(item, location)
        result.number(metric.get("value"), location + ".value")
        for field in ("definition", "unit"):
            result.text(metric.get(field), location + "." + field)
        result.enum(metric.get("direction"), {"higher", "lower", "target"}, location + ".direction")
        source_id = metric.get("source_artifact")
        result.ref(source_id, location + ".source_artifact")
        pointer = metric.get("pointer")
        try:
            # Validate syntax even if the source is missing, so both errors are reported.
            if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
                raise ValueError("must be an RFC 6901 JSON pointer")
            if re.search(r"~(?![01])", pointer):
                raise ValueError("invalid '~' escape in JSON pointer")
            if isinstance(source_id, str) and source_id in result.files:
                if source_id not in sources:
                    sources[source_id] = read_json(result.files[source_id])
                recorded = json_pointer(sources[source_id], pointer)
                if not is_number(recorded):
                    result.error(location + ".pointer", "source value must be a finite number (not a boolean)")
                elif is_number(metric.get("value")) and recorded != metric["value"]:
                    result.error(location + ".value", "does not equal the JSON source value")
        except (OSError, ValueError, RecursionError, OverflowError) as exc:
            result.error(location + ".pointer", "cannot read source value: " + str(exc))

    claims = result.array(data.get("claims"), "claims")
    if claims and (data.get("status") != "completed" or validity.get("status") != "passed"):
        result.error("claims", "evidence claims require status=completed and validity.status=passed")
    claim_ids = set()
    for index, item in enumerate(claims):
        location = "claims[{}]".format(index)
        claim = result.object(item, location)
        claim_id = claim.get("id")
        if result.text(claim_id, location + ".id"):
            if claim_id in claim_ids:
                result.error(location + ".id", "duplicate claim id")
            claim_ids.add(claim_id)
        for field in ("text", "location"):
            result.text(claim.get(field), location + "." + field)
        result.ref(claim.get("artifact"), location + ".artifact")
        metric_name = claim.get("metric")
        if result.text(metric_name, location + ".metric") and metric_name not in metrics:
            result.error(location + ".metric", "unknown metric name {!r}".format(metric_name))
        reported = claim.get("reported_value")
        tolerance = claim.get("absolute_tolerance")
        reported_valid = result.number(reported, location + ".reported_value")
        tolerance_valid = result.number(tolerance, location + ".absolute_tolerance")
        if tolerance_valid and tolerance < 0:
            result.error(location + ".absolute_tolerance", "must be non-negative")
        metric = metrics.get(metric_name) if isinstance(metric_name, str) else None
        if isinstance(metric, dict) and is_number(metric.get("value")) and reported_valid and tolerance_valid and tolerance >= 0:
            if abs(reported - metric["value"]) > tolerance:
                result.error(location + ".reported_value", "differs from the metric beyond absolute_tolerance")
    return result


def compare_results(current, baseline):
    """Check recorded comparability, not whether the study design is fair."""
    errors = []
    for section, fields in (
        ("evaluation", ("protocol_id", "protocol_version", "split_id", "selection_scope", "aggregation")),
        ("provenance", ("data_id", "data_version")),
    ):
        left, right = current.data.get(section), baseline.data.get(section)
        if not isinstance(left, dict) or not isinstance(right, dict):
            continue
        for field in fields:
            if left.get(field) != right.get(field):
                errors.append("{}.{} differs from baseline".format(section, field))
    hashes = []
    for result in (current, baseline):
        provenance = result.data.get("provenance")
        reference = provenance.get("split_artifact") if isinstance(provenance, dict) else None
        artifact = result.artifacts.get(reference) if isinstance(reference, str) else None
        hashes.append(artifact.get("sha256", "").lower() if isinstance(artifact, dict) else None)
    if all(hashes) and hashes[0] != hashes[1]:
        errors.append("provenance.split_artifact content hash differs from baseline")
    left, right = current.data.get("metrics"), baseline.data.get("metrics")
    if isinstance(left, dict) and isinstance(right, dict):
        shared = set(left).intersection(right)
        if not shared:
            errors.append("no shared metric names to compare with baseline")
        for name in sorted(shared):
            if not isinstance(left[name], dict) or not isinstance(right[name], dict):
                continue
            for field in ("definition", "unit", "direction"):
                if left[name].get(field) != right[name].get(field):
                    errors.append("metrics.{}.{} differs from baseline".format(name, field))
    for label, result in (("current", current), ("baseline", baseline)):
        validity = result.data.get("validity")
        if result.data.get("status") != "completed" or not isinstance(validity, dict) or validity.get("status") != "passed":
            errors.append(label + " comparison run must be completed with passed validity")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="path to a schema_version=1 JSON run manifest")
    parser.add_argument("--root", help="artifact root for both manifests (default: each manifest's directory)")
    parser.add_argument("--compare", metavar="BASELINE", help="also check a baseline and recorded comparability")
    args = parser.parse_args(argv)
    current = check_manifest(args.manifest, args.root)
    errors = [("current", error) for error in current.errors]
    if args.compare:
        baseline = check_manifest(args.compare, args.root)
        errors.extend(("baseline", error) for error in baseline.errors)
        # Only compare valid structures, avoiding misleading errors caused by malformed input.
        if not current.errors and not baseline.errors:
            errors.extend(("comparison", error) for error in compare_results(current, baseline))
    if errors:
        print("FAIL: {} evidence check error(s).".format(len(errors)), file=sys.stderr)
        for label, error in errors:
            print("- [{}] {}".format(label, error), file=sys.stderr)
        return 1
    print("PASS: artifact integrity and recorded source-value checks passed ({} claim record(s)).".format(
        len(current.data.get("claims", []))))
    if args.compare:
        print("PASS: recorded evaluation, data/split and shared metric definitions match the baseline.")
    print("This does not establish scientific validity, parse manuscript prose, or enforce runtime budgets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
