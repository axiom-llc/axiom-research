import json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OperationalFidelityMilestoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.p=json.loads((ROOT/'operational-fidelity/portfolio-validation.json').read_text())
    def test_all_five_domains_pass_common_evidence_checks(self):
        self.assertEqual(len(self.p['domains']),5)
        for d in self.p['domains']:
            self.assertTrue(all(d['checks'].values()),d['domain'])
            self.assertEqual(d['harness_receipts'],4); self.assertEqual(d['effects'],16); self.assertEqual(d['events'],16)
    def test_aggregate_metrics_match_retained_artifacts(self):
        t=self.p['totals']; self.assertEqual(t['operations'],85); self.assertEqual(t['synthetic_cost_usd'],24240.0)
        self.assertEqual(t['inventory_movements'],19); self.assertEqual(t['documents'],39); self.assertEqual(t['communications'],24); self.assertEqual(t['approvals'],18)
        self.assertEqual(t['harness_receipts'],20); self.assertEqual(t['effects'],80); self.assertEqual(t['events'],80)
    def test_source_hashes_match_operating_days(self):
        for d in self.p['domains']:
            path=ROOT/d['domain']/'high-fidelity/operating-day.json'
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),d['operating_day_sha256'])
    def test_milestone_fails_closed_on_material_gaps(self):
        self.assertEqual(self.p['validation_status'],'PASS_WITH_LIMITS'); self.assertFalse(self.p['milestone_accepted'])
        self.assertGreaterEqual(len(self.p['remaining_material_gaps']),6)
if __name__=='__main__': unittest.main()
