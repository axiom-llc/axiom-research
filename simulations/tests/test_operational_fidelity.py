import json, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import runner

class OperationalFidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=runner.load(ROOT/'robotics-production/high-fidelity/operating-day.json')
        cls.schema=runner.load(ROOT/'schemas/operational-fidelity.schema.json')
    def test_record_validates_and_is_complete(self):
        import jsonschema
        jsonschema.validate(self.record,self.schema)
        self.assertEqual(len(self.record['operations']),28)
        self.assertTrue(all(self.record['completeness'].values()))
    def test_reference_closure_causality_and_state_chain(self):
        ids=set()
        for key in ('actors','resources','schedules','queues','decisions','communications','transactions','inventory_movements','documents','events','situations','issues','approvals','state_transitions','outcomes'):
            vals=[x['id'] for x in self.record[key]]; self.assertEqual(len(vals),len(set(vals)),key); ids.update(vals)
        actor_ids={x['id'] for x in self.record['actors']}; seen=set(); last=''
        for op in self.record['operations']:
            self.assertIn(op['actor_ref'],actor_ids); self.assertTrue(set(op['refs']) <= ids); self.assertIn(op['result_ref'],ids)
            self.assertTrue(set(op['causes']) <= seen); self.assertGreaterEqual(op['at'],last); last=op['at']; seen.add(op['id'])
        transitions=self.record['state_transitions']; self.assertEqual(transitions[0]['from'],'NEW')
        for a,b in zip(transitions,transitions[1:]): self.assertEqual(a['to'],b['from'])
    def test_financial_inventory_and_authority_records_are_queryable(self):
        self.assertEqual(sum(x['amount_usd'] for x in self.record['transactions']),21390.0)
        for m in self.record['inventory_movements']:
            for key in ('sku','lot','from','to','quantity'): self.assertIn(key,m)
            self.assertGreater(m['quantity'],0)
        actors={x['id'] for x in self.record['actors']}
        self.assertTrue(all(a['actor'] in actors for a in self.record['approvals']))
if __name__=='__main__': unittest.main()
