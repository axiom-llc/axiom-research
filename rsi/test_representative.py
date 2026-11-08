"""Independently check source scope, live canonical queue semantics and no promotion."""
from pathlib import Path
import json
import unittest

from rsi.representative import workload

ROOT = Path(__file__).resolve().parents[1]


class CurrentQueueAcceptance(unittest.TestCase):
    def test_matched_current_queue_and_negative_holdouts(self):
        raw = (ROOT / "research-queue.json").read_bytes()
        receipt = workload(ROOT, samples=11, operations=10)
        self.assertEqual(receipt["canonical_items"],
                         len(json.loads(raw)["items"]))
        self.assertEqual(receipt["repository"], "axiom-llc/axiom-research")
        self.assertEqual(receipt["status"], "MEASURED_CURRENT_CANONICAL_QUEUE")
        self.assertEqual(len(receipt["negative_holdouts"]), 4)
        self.assertTrue(receipt["behavior_equivalent"])
        self.assertEqual(len(receipt["samples"]), 11)
        self.assertEqual(receipt["positive_pairs"] +
                         sum(row["candidate"] >= row["baseline"]
                             for row in receipt["samples"]), 11)
        self.assertFalse(receipt["production_distribution_covered"])
        self.assertFalse(receipt["independent_implementation_review"])
        self.assertFalse(receipt["promotion_authorized"])
        self.assertEqual(raw, (ROOT / "research-queue.json").read_bytes())

    def test_insufficient_workload_samples_fail_closed(self):
        with self.assertRaises(ValueError):
            workload(ROOT, samples=3)
        with self.assertRaises(ValueError):
            workload(ROOT, operations=0)


if __name__ == "__main__":
    unittest.main()
