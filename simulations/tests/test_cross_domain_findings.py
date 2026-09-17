import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOMAINS=['robotics-production','software-development','specialty-care-administration','soc-operations','logistics-supply-chain']
class CrossDomainFindingsTests(unittest.TestCase):
    def test_portfolio_summary_matches_retained_evidence(self):
        summary=json.loads((ROOT/'portfolio-summary.json').read_text()); rows={r['domain']:r for r in summary['domains']}
        self.assertEqual(set(rows),set(DOMAINS)); totals={k:0 for k in ('modeled_steps','departments','actors','approval_steps','failure_injections','effects','events','recovery_observed_files')}
        for d in DOMAINS:
            p=ROOT/d; sc=json.loads((p/'scenarios/end-to-end.json').read_text()); org=json.loads((p/'organization.json').read_text()); evp=p/'evidence/accepted-20260916/evidence.json'; erp=p/'evidence/accepted-20260916/evaluation.json'; ev=json.loads(evp.read_text()); er=json.loads(erp.read_text()); row=rows[d]
            observed={'modeled_steps':len(sc['steps']),'departments':len(org['departments']),'actors':len(org['actors']),'approval_steps':sum(s['approval_ref'] is not None for s in sc['steps']),'failure_injections':len(sc['failure_injections']),'effects':len(ev['effect_evidence']),'events':len(ev['events']),'recovery_observed_files':ev['recovery'][0]['observed_file_count']}
            self.assertEqual(row['result'],'ACCEPT'); self.assertEqual(ev['status'],'PASS'); self.assertTrue(all(c['passed'] for c in er['checks']))
            self.assertEqual(row['evidence_sha256'],hashlib.sha256(evp.read_bytes()).hexdigest()); self.assertEqual(row['evaluation_sha256'],hashlib.sha256(erp.read_bytes()).hexdigest())
            for k,v in observed.items(): self.assertEqual(row[k],v); totals[k]+=v
        self.assertEqual(summary['aggregate'],{'domain_count':5,**totals})
    def test_common_checks_are_present_in_every_evaluation(self):
        summary=json.loads((ROOT/'portfolio-summary.json').read_text()); expected=set(summary['common_validated_checks'])
        for d in DOMAINS:
            er=json.loads((ROOT/d/'evidence/accepted-20260916/evaluation.json').read_text()); passed={c['id'] for c in er['checks'] if c['passed']}
            self.assertTrue(expected <= passed,d)
if __name__=='__main__': unittest.main()
