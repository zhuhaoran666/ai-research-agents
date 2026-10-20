#!/usr/bin/env python3
"""Recompute accuracy from four invented predictions; no experiment is launched."""

import json
from pathlib import Path
import sys


def evaluate(directory):
    def load(name):
        return json.loads((directory / name).read_text(encoding="utf-8"))

    predictions = load("predictions.json")
    split = load("split.json")
    config = load("config.json")
    if not isinstance(predictions, list) or len(predictions) != 4:
        raise ValueError("the synthetic demonstration requires exactly four records")
    allowed = config["labels"]
    expected_ids = split["test_ids"]
    ids = []
    correct = 0
    for row in predictions:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError("each prediction must have a string id")
        ids.append(row["id"])
        for field in ("true_label", "predicted_label"):
            if type(row.get(field)) is not int or row[field] not in allowed:
                raise ValueError("prediction labels must be allowed integer classes")
        correct += int(row["true_label"] == row["predicted_label"])
    if len(set(ids)) != len(ids):
        raise ValueError("prediction ids must be unique")
    if len(expected_ids) != len(set(expected_ids)) or set(ids) != set(expected_ids):
        raise ValueError("predictions must match the declared split exactly")
    metrics = {
        "accuracy": correct / len(predictions),
        "correct": correct,
        "total": len(predictions),
        "checks": {"unique_ids": True, "exact_split_membership": True, "allowed_labels": True},
    }
    (directory / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def main():
    try:
        metrics = evaluate(Path(__file__).resolve().parent)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Synthetic evaluation failed: " + str(exc), file=sys.stderr)
        return 1
    print("Synthetic demonstration only: accuracy = {} ({}/{})".format(
        metrics["accuracy"], metrics["correct"], metrics["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
