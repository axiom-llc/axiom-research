import json, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner
ROOT=Path(__file__).resolve().parents[1]
class PublicationRecordsTests(unittest.TestCase):
    def test_claims_validate_and_reference_retained_evidence(self):
        paths=sorted((ROOT/'claims').glob('*.json')); self.assertEqual(len(paths),4)
        for path in paths:
            claim=json.loads(path.read_text()); runner.validate('claim-record',claim)
            self.assertEqual(claim['evidence_classification'],'VALIDATED_EXECUTABLE_DEMO')
            for ref in claim['evidence_refs']:
                target=ROOT/ref; self.assertTrue(target.is_file(),ref)
                data=json.loads(target.read_text())
                if data.get('schema')=='axiom-simulation/evidence-v1': self.assertEqual(data.get('status'),'PASS')
                elif data.get('schema') in ('axiom-simulation/operational-reconstruction-v1','axiom-simulation/operational-cycle-reconstruction-v1'): self.assertEqual(data.get('result'),'ACCEPT')
                elif data.get('schema')=='axiom-simulation/operational-fidelity-acceptance-v1': self.assertEqual(data.get('status'),'ACCEPT')
                else: self.fail(f'unsupported evidence schema: {ref}: {data.get("schema")}')

    def test_high_fidelity_claims_bind_to_accepted_cycle_evidence(self):
        acceptance=json.loads((ROOT/'operational-fidelity/portfolio-acceptance.json').read_text())
        self.assertTrue(acceptance['milestone_accepted']); self.assertEqual(acceptance['status'],'ACCEPT')
        for name in ('high-fidelity-multiday-operations-20260917','high-fidelity-contention-ledger-20260917'):
            claim=json.loads((ROOT/'claims'/f'{name}.json').read_text()); runner.validate('claim-record',claim)
            self.assertEqual(claim['evidence_classification'],'VALIDATED_EXECUTABLE_DEMO')
            for ref in claim['evidence_refs']:
                target=ROOT/ref; self.assertTrue(target.is_file(),ref)
        for domain in ('software-development','logistics-supply-chain'):
            text=(ROOT/'case-studies'/f'{domain}.md').read_text()
            self.assertIn('High-fidelity multi-day evidence',text)
            self.assertIn('three-day synthetic operating cycle',text)
            self.assertIn('24/24 successful APEX effects/events',text)

    def test_case_studies_cover_portfolio_and_preserve_boundary(self):
        summary=json.loads((ROOT/'portfolio-summary.json').read_text())
        cases={p.stem:p.read_text() for p in (ROOT/'case-studies').glob('*.md')}
        self.assertEqual(set(cases),{row['domain'] for row in summary['domains']})
        for text in cases.values():
            self.assertIn('VALIDATED_EXECUTABLE_DEMO',text); self.assertIn('not a production deployment',text)
if __name__=='__main__': unittest.main()
