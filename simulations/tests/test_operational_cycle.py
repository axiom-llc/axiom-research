import json,unittest
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/'operational-fidelity/operational-cycle.schema.json').read_text())
DOMAINS=['software-development','logistics-supply-chain']
class OperationalCycleTests(unittest.TestCase):
 def records(self):
  for d in DOMAINS:
   yield d,json.loads((ROOT/d/'high-fidelity/cycle/operational-cycle.json').read_text())
 def test_cycles_close_all_gap_dimensions(self):
  for d,r in self.records():
   jsonschema.validate(r,SCHEMA); self.assertTrue(all(r['completeness'].values()),d); self.assertGreaterEqual(len(r['days']),3); self.assertGreaterEqual(len(r['entities']),6); self.assertTrue(any(x['carryover'] for x in r['work_items'])); self.assertGreaterEqual(len(r['resource_contention']),2)
 def test_backpressure_arrivals_and_schedule_changes_are_material(self):
  for d,r in self.records():
   opens=[x.get('open',0) for x in r['queue_snapshots']]; self.assertGreater(max(opens),opens[0]); self.assertEqual(opens[-1],0); self.assertGreaterEqual(len(r['arrivals']),6); self.assertGreaterEqual(len(r['staffing_events']),2); self.assertGreaterEqual(len(r['calendar_events']),2)
 def test_financial_cycles_are_double_entry_and_settle_liabilities(self):
  for d,r in self.records():
   self.assertTrue(all(x['amount_usd']>0 and x['debit_account']!=x['credit_account'] for x in r['ledger_entries']))
   debit=sum(x['amount_usd'] for x in r['ledger_entries']); credit=sum(x['amount_usd'] for x in r['ledger_entries']); self.assertEqual(debit,credit)
   credits={x['credit_account'] for x in r['ledger_entries']}; debits={x['debit_account'] for x in r['ledger_entries']}; self.assertTrue(any('payable' in x or 'accrued' in x for x in credits & debits))
if __name__=='__main__': unittest.main()
