# Synthetic demonstration specification

- ID / version: `synthetic-accuracy-demo` / `1`.
- Scope: demonstrate artifact hashing and numeric evidence links, using four invented records.
- Input: the four IDs in `split.json`, with binary true and predicted labels in `predictions.json`.
- Evaluation: `evaluate.py` checks unique IDs, exact split membership and allowed labels, then computes accuracy as correct predictions / total records.
- Protocol: `synthetic-binary-accuracy` / `1`; split `synthetic-test-v1`; no model fitting, candidate selection or repeated trials.
- Completion: all four records pass the input checks and `metrics.json` is written.
- Budget: one local evaluation call. This example records counters; it provides no external execution limit.
- Scientific limits: invented data, no baseline, no uncertainty estimate, and no empirical research claim.
