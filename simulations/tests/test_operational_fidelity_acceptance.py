import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OperationalFidelityAcceptanceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.r=json.loads((ROOT/'operational-fidelity/portfolio-acceptance.json').read_text())
 def test_milestone_is_accepted_on_closed_material_gaps(self):
  self.assertEqual(self.r['status'],'ACCEPT'); self.assertTrue(self.r['milestone_accepted']); self.assertEqual(len(self.r['gap_closure_domains']),2); self.assertGreaterEqual(len(self.r['closed_material_gaps']),7)
  for d in self.r['gap_closure_domains']: self.assertTrue(all(d['checks'].values()),d['domain'])
 def test_retained_cycle_hashes_and_source_binding(self):
  for row in self.r['gap_closure_domains']:
   b=ROOT/row['domain']/'high-fidelity/cycle/evidence/accepted-20260917'; cycle=ROOT/row['domain']/'high-fidelity/cycle/operational-cycle.json'
   self.assertEqual(hashlib.sha256(cycle.read_bytes()).hexdigest(),row['source_sha256'])
   self.assertEqual(hashlib.sha256((b/'cycle-reconstruction.json').read_bytes()).hexdigest(),row['reconstruction_sha256'])
   self.assertEqual(hashlib.sha256((b/'cycle-execution-evidence.json').read_bytes()).hexdigest(),row['execution_evidence_sha256'])
 def test_runtime_evidence_is_complete(self):
  for row in self.r['gap_closure_domains']:
   b=ROOT/row['domain']/'high-fidelity/cycle/evidence/accepted-20260917'; rec=json.loads((b/'cycle-reconstruction.json').read_text()); ev=json.loads((b/'cycle-execution-evidence.json').read_text())
   self.assertEqual(rec['repository_revisions']['axiom-research'],'7fd0df13bb8d7e43b92dfead337f4ca145f0e1de'); self.assertEqual(len(rec['harness_receipts']),6); self.assertEqual(rec['effect_count'],24); self.assertEqual(rec['event_count'],24); self.assertTrue(rec['contention_ok']); self.assertTrue(rec['authority_gate_ok']); self.assertTrue(rec['authorization_bindings_ok']); self.assertTrue(rec['all_effects_succeeded']); self.assertTrue(all(x['receipt']['outcome']=='ACCEPTED' and x['authorization_binding'] for x in ev))
if __name__=='__main__': unittest.main()
