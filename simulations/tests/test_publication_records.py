import json, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner
ROOT=Path(__file__).resolve().parents[1]
class PublicationRecordsTests(unittest.TestCase):
    def test_claims_validate_and_reference_retained_evidence(self):
        paths=sorted((ROOT/'claims').glob('*.json')); self.assertEqual(len(paths),2)
        for path in paths:
            claim=json.loads(path.read_text()); runner.validate('claim-record',claim)
            self.assertEqual(claim['evidence_classification'],'VALIDATED_EXECUTABLE_DEMO')
            for ref in claim['evidence_refs']:
                target=ROOT/ref; self.assertTrue(target.is_file(),ref)
                self.assertEqual(json.loads(target.read_text())['status'],'PASS')
    def test_case_studies_cover_portfolio_and_preserve_boundary(self):
        summary=json.loads((ROOT/'portfolio-summary.json').read_text())
        cases={p.stem:p.read_text() for p in (ROOT/'case-studies').glob('*.md')}
        self.assertEqual(set(cases),{row['domain'] for row in summary['domains']})
        for text in cases.values():
            self.assertIn('VALIDATED_EXECUTABLE_DEMO',text); self.assertIn('not a production deployment',text)
if __name__=='__main__': unittest.main()
