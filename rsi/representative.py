"""Independent read-only acceptance on the current canonical research queue."""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
import tempfile
import time

from rsi.benchmark import load
from rsi.native import generate

ROOT = Path(__file__).resolve().parents[1]


def workload(root: Path = ROOT, *, samples: int = 15, operations: int = 75) -> dict:
    if samples < 11 or operations < 1:
        raise ValueError("insufficient matched samples")
    proposal = generate(root)
    if proposal.get("status") != "GENERATED" or len(proposal["candidates"]) != 1:
        raise ValueError("source-pinned proposal missing")
    rule = json.loads((root / "rsi/generators.json").read_text())["rules"][0]
    if rule["path"] != "research_queue_check.py":
        raise ValueError("unapproved acceptance target")
    source = (root / rule["path"]).read_text()
    updated = source.replace(rule["before"], rule["after"], 1)
    if source == updated or source.count(rule["before"]) != 1:
        raise ValueError("ambiguous source transformation")
    baseline, candidate = load(source), load(updated)
    queue_path = root / "research-queue.json"
    original_bytes = queue_path.read_bytes()
    canonical = json.loads(original_bytes)
    if not canonical.get("items"):
        raise ValueError("current canonical queue has no representative items")
    expected = baseline(queue_path)
    if expected != candidate(queue_path):
        raise ValueError("canonical queue behavior is not equivalent")

    holdouts = []
    cases = [
        ("missing-required-title", lambda data: data["items"][0].pop("title")),
        ("invalid-target", lambda data: data["items"][0].__setitem__("target", "invalid")),
        ("duplicate-id", lambda data: data["items"].append(deepcopy(data["items"][0]))),
        ("invalid-policy", lambda data: data["policy"].__setitem__("manager_target", "invalid")),
    ]
    with tempfile.TemporaryDirectory() as temp:
        inp = Path(temp) / "invalid-queue.json"
        for label, change in cases:
            corrupted = deepcopy(canonical)
            change(corrupted)
            inp.write_text(json.dumps(corrupted, sort_keys=True))
            exceptions = []
            for fn in (baseline, candidate):
                try:
                    fn(inp)
                except ValueError as exc:
                    exceptions.append((type(exc).__name__, str(exc)))
            if len(exceptions) != 2 or exceptions[0] != exceptions[1]:
                raise ValueError("negative holdout behavior differs: " + label)
            holdouts.append(label)

    # Warm real-current-queue filesystem/cache path equally before alternating.
    for _ in range(5):
        baseline(queue_path)
        candidate(queue_path)
    readings = []
    for n in range(samples):
        order = (("baseline", baseline), ("candidate", candidate)) if n % 2 == 0 else (
            ("candidate", candidate), ("baseline", baseline))
        result = {}
        for label, fn in order:
            start = time.perf_counter_ns()
            for _ in range(operations):
                if fn(queue_path) != expected:
                    raise ValueError("read-only canonical result changed during measurement")
            result[label] = (time.perf_counter_ns() - start) / operations
        readings.append(result)

    if queue_path.read_bytes() != original_bytes:
        raise ValueError("canonical source queue was modified")
    before = median(row["baseline"] for row in readings)
    after = median(row["candidate"] for row in readings)
    gain = (before - after) * 100 / before
    return {
        "schema": "axiom-research/rsi-representative-acceptance-v1",
        "repository": "axiom-llc/axiom-research",
        "source_revision": proposal["source_revision"],
        "candidate_id": proposal["candidates"][0]["candidate_id"],
        "source_sha256": proposal["candidates"][0]["source_sha256"],
        "candidate_sha256": proposal["candidates"][0]["candidate_sha256"],
        "canonical_queue_sha256": sha256(original_bytes).hexdigest(),
        "canonical_items": len(canonical["items"]),
        "canonical_result": expected,
        "negative_holdouts": holdouts,
        "behavior_equivalent": True,
        "paired_samples": len(readings),
        "operations_per_sample": operations,
        "baseline_median_ns_per_op": before,
        "candidate_median_ns_per_op": after,
        "paired_median_gain_ns_per_op": median(
            row["baseline"] - row["candidate"] for row in readings),
        "positive_pairs": sum(row["candidate"] < row["baseline"] for row in readings),
        "gain_percentage": gain,
        "samples": readings,
        "scope": "real current public canonical research-queue.json, local CI runner; not forecast load, field telemetry or universal production distribution",
        "independent_implementation_review": False,
        "production_distribution_covered": False,
        "mutation_authority": False,
        "promotion_authorized": False,
        "status": "MEASURED_CURRENT_CANONICAL_QUEUE",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = workload()
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
                      ("status", "source_revision", "canonical_items",
                       "paired_samples", "gain_percentage", "promotion_authorized")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
