import json, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import runner
DOMAINS={
 'specialty-care-administration':{'ops':14,'cost':525.0,'final':'CLOSED','forbidden':['diagnosis','prescription','treatment_order','real_patient']},
 'soc-operations':{'ops':12,'cost':615.0,'final':'CLOSED','forbidden':['live_probe','credential_use','real_endpoint_mutation','network_scan']},
}
class FinalDomainFidelityTests(unittest.TestCase):
 def test_records_validate_and_reconcile(self):
  for d,e in DOMAINS.items():
   r=runner.load(ROOT/d/'high-fidelity/operating-day.json'); runner.validate('operational-fidelity',r)
   self.assertEqual(len(r['operations']),e['ops']); self.assertEqual(sum(x['amount_usd'] for x in r['transactions']),e['cost']); self.assertTrue(all(r['completeness'].values()))
 def test_reference_closure_and_state_continuity(self):
  for d in DOMAINS:
   r=runner.load(ROOT/d/'high-fidelity/operating-day.json'); ids=set(); actors={x['id'] for x in r['actors']}
   for k in ('actors','resources','schedules','queues','decisions','communications','transactions','inventory_movements','documents','events','situations','issues','approvals','state_transitions','outcomes'): ids.update(x['id'] for x in r[k])
   seen=set(); last=''
   for op in r['operations']:
    self.assertIn(op['actor_ref'],actors); self.assertTrue(set(op['refs'])<=ids); self.assertIn(op['result_ref'],ids); self.assertTrue(set(op['causes'])<=seen); self.assertGreaterEqual(op['at'],last); seen.add(op['id']); last=op['at']
   st=r['state_transitions']; self.assertEqual(st[0]['from'],'NEW')
   for a,b in zip(st,st[1:]): self.assertEqual(a['to'],b['from'])
 def test_sensitive_effect_boundaries_are_synthetic(self):
  care=(ROOT/'specialty-care-administration/high-fidelity/operating-day.json').read_text().lower()
  soc=(ROOT/'soc-operations/high-fidelity/operating-day.json').read_text().lower()
  self.assertIn('clinical judgment remains human-controlled',care); self.assertIn('synthetic-patient',care)
  self.assertIn('all endpoint/network effects simulated only',soc); self.assertIn('synthetic-endpoint',soc)
  care_record=runner.load(ROOT/'specialty-care-administration/high-fidelity/operating-day.json')
  soc_record=runner.load(ROOT/'soc-operations/high-fidelity/operating-day.json')
  care_actions=' '.join([x['kind'] for x in care_record['operations']]+[x.get('kind','') for x in care_record['resources']]).lower()
  soc_actions=' '.join([x['kind'] for x in soc_record['operations']]+[x.get('kind','') for x in soc_record['resources']]).lower()
  for term in DOMAINS['specialty-care-administration']['forbidden']: self.assertNotIn(term,care_actions)
  for term in DOMAINS['soc-operations']['forbidden']: self.assertNotIn(term,soc_actions)

class RetainedFinalDomainFidelityTests(unittest.TestCase):
 def test_retained_evidence_is_bound_and_accepted(self):
  for d,e in DOMAINS.items():
   base=ROOT/d/'high-fidelity/evidence/accepted-20260917'
   report=json.loads((base/'reconstruction.json').read_text()); evidence=json.loads((base/'execution-evidence.json').read_text())
   self.assertEqual(report['result'],'ACCEPT'); self.assertEqual(report['repository_revisions']['axiom-research'],'96a572f869e506f90e4985187abc25d72e3c0cd1')
   self.assertEqual(report['audit']['operations'],e['ops']); self.assertEqual(report['audit']['synthetic_cost_usd'],e['cost'])
   self.assertEqual(report['phase_count'],4); self.assertEqual(len(report['harness_receipts']),4); self.assertEqual(report['effect_count'],16); self.assertEqual(report['event_count'],16)
   self.assertTrue(report['authority_gate_ok']); self.assertTrue(report['authorization_bindings_ok']); self.assertEqual(report['final_state'],e['final'])
   self.assertTrue(all(x['outcome']=='ACCEPTED' for x in report['harness_receipts']))
   self.assertTrue(all(effect.get('state')=='SUCCEEDED' for phase in evidence for effect in phase['effects']))
   self.assertTrue(all(phase['authorization_binding'] for phase in evidence))

if __name__=='__main__': unittest.main()
