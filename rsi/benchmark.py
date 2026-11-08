"""Independent synthetic queue validator before/after benchmark; no real queue data."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
import tempfile
import time

from rsi.native import generate

ROOT = Path(__file__).resolve().parents[1]


def load(source):
    namespace = {"__name__": "rsi_queue_validator"}
    exec(compile(source, "research_queue_check.py", "exec"), namespace)
    return namespace["validate"]


def fixture(count=300):
    return {
        "schema_version": 1,
        "policy": {
            "owner_repo": "axiom-llc/axiom-research",
            "ordering": ["priority asc", "value_score desc", "created_at asc", "id asc"],
            "statuses": ["QUEUED", "ISSUED", "COMPLETE", "BLOCKED", "REJECTED"],
            "researcher_targets": ["claude-manual", "gemini-manual", "chatgpt"],
            "manager_target": "chatgpt",
            "incremental_hosted_cost_usd": 0,
        },
        "items": [{
            "id": f"RQ-2026-11-08-{i:03d}", "priority": i % 7,
            "value_score": (i * 17) % 100, "status": "QUEUED",
            "target": "chatgpt", "created_at": "2026-11-08",
            "title": "Synthetic", "question": "Synthetic question",
            "objective": "Synthetic objective", "deliverable": ["fixture"],
            "constraints": [],
        } for i in range(count)],
    }


def measure(root=ROOT):
    report = generate(root)
    if len(report["candidates"]) != 1:
        return {"status": "NO_APPLICABLE_RULE"}
    rule = json.loads((root / "rsi/generators.json").read_text())["rules"][0]
    source = (root / rule["path"]).read_text()
    updated = source.replace(rule["before"], rule["after"], 1)
    before, after = load(source), load(updated)
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "synthetic.json"
        path.write_text(json.dumps(fixture()), encoding="utf-8")
        expected = before(path)
        if expected != after(path):
            raise ValueError("candidate changes queue-validation output")
        # Explicit negative holdout ensures malformed content remains rejected.
        bad = fixture(4)
        bad["items"][0].pop("title")
        path.write_text(json.dumps(bad), encoding="utf-8")
        errors = []
        for fn in (before, after):
            try:
                fn(path)
            except ValueError as exc:
                errors.append(str(exc))
        if len(errors) != 2 or errors[0] != errors[1]:
            raise ValueError("candidate changes failure semantics")
        path.write_text(json.dumps(fixture()), encoding="utf-8")
        samples = []
        for i in range(11):
            pairs = (("before", before), ("after", after)) if i % 2 == 0 else (
                ("after", after), ("before", before))
            sample = {}
            for key, fn in pairs:
                start = time.perf_counter_ns()
                for _ in range(35):
                    fn(path)
                sample[key] = (time.perf_counter_ns() - start) / 35
            samples.append(sample)
    b = median(s["before"] for s in samples)
    a = median(s["after"] for s in samples)
    return {
        "schema": "axiom-native-rsi/benchmark-v1",
        "source_revision": report["source_revision"],
        "candidate_id": report["candidates"][0]["candidate_id"],
        "source_sha256": sha256(source.encode()).hexdigest(),
        "candidate_sha256": sha256(updated.encode()).hexdigest(),
        "workload_provenance": "synthetic 300-record canonical-schema fixture",
        "paired_samples": 11, "operations_per_sample": 35,
        "baseline_median_ns_per_op": b, "candidate_median_ns_per_op": a,
        "paired_median_gain_ns_per_op": median(s["before"]-s["after"] for s in samples),
        "gain_percentage": (b-a)*100/b if b>0 else None,
        "quality_equivalent": True, "promotion_authorized": False,
        "status": "POSITIVE_MACHINE_MEASUREMENT" if a<b else "NONPOSITIVE_MEASUREMENT",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = measure()
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    print(json.dumps(result, sort_keys=True))
