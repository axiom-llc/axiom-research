import json,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import runner
CASES={
 'software-development':{'ops':18,'cost':1018.0,'approvals':4,'final':'CLOSED'},
 'logistics-supply-chain':{'ops':13,'cost':692.0,'approvals':3,'final':'CLOSED'},
}
class OperationalFidelityPortfolioTests(unittest.TestCase):
    def load(self,d): return runner.load(ROOT/d/'high-fidelity/operating-day.json')
    def test_records_validate_and_reconcile(self):
        import jsonschema
        schema=runner.load(ROOT/'schemas/operational-fidelity.schema.json')
        for d,e in CASES.items():
            r=self.load(d); jsonschema.validate(r,schema); self.assertTrue(all(r['completeness'].values()),d)
            self.assertEqual(len(r['operations']),e['ops']); self.assertEqual(sum(x['amount_usd'] for x in r['transactions']),e['cost']); self.assertEqual(len(r['approvals']),e['approvals'])
    def test_reference_closure_causality_and_state_continuity(self):
        for d in CASES:
            r=self.load(d); ids=set(); actors={x['id'] for x in r['actors']}
            for key in ('actors','resources','schedules','queues','decisions','communications','transactions','inventory_movements','documents','events','situations','issues','approvals','state_transitions','outcomes'):
                vals=[x['id'] for x in r[key]]; self.assertEqual(len(vals),len(set(vals)),(d,key)); ids.update(vals)
            seen=set(); last=''
            for op in r['operations']:
                self.assertIn(op['actor_ref'],actors); self.assertTrue(set(op['refs'])<=ids); self.assertIn(op['result_ref'],ids); self.assertTrue(set(op['causes'])<=seen); self.assertGreaterEqual(op['at'],last); seen.add(op['id']); last=op['at']
            t=r['state_transitions']; self.assertEqual(t[0]['from'],'NEW'); self.assertEqual(t[-1]['to'],CASES[d]['final'])
            for a,b in zip(t,t[1:]): self.assertEqual(a['to'],b['from'])
    def test_inventory_and_authority_are_explicit(self):
        for d in CASES:
            r=self.load(d); actors={x['id'] for x in r['actors']}
            for m in r['inventory_movements']:
                for k in ('sku','lot','from','to','quantity'): self.assertIn(k,m)
                self.assertGreater(m['quantity'],0)
            self.assertTrue(all(a['actor'] in actors and a['authority'] for a in r['approvals']))
if __name__=='__main__': unittest.main()
