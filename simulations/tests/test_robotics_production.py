import hashlib, json, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner

ROOT=Path(__file__).resolve().parents[1]/'robotics-production'
class RoboticsProductionTests(unittest.TestCase):
    def setUp(self):
        self.org=runner.load(ROOT/'organization.json'); self.scenario=runner.load(ROOT/'scenarios/end-to-end.json'); self.fixture=runner.load(ROOT/'fixture-manifest.json')
    def test_flagship_contracts_and_references(self):
        for kind,value in [('organization-model',self.org),('scenario-spec',self.scenario),('fixture-manifest',self.fixture)]: runner.validate(kind,value)
        actors={a['id']:a for a in self.org['actors']}; steps={s['id']:s for s in self.scenario['steps']}
        self.assertEqual(len(steps),22); self.assertTrue(all(s['actor'] in actors for s in self.scenario['steps']))
        self.assertTrue(all(dep in steps for s in self.scenario['steps'] for dep in s['depends_on']))
        self.assertTrue(all(s['approval_ref'] is None or s['approval_ref'] in actors[s['actor']]['authority'] for s in self.scenario['steps']))
    def test_fixture_hashes_match_retained_inputs(self):
        for name,expected in self.fixture['artifact_hashes'].items():
            actual=hashlib.sha256((ROOT/'fixtures'/name).read_bytes()).hexdigest(); self.assertEqual(actual,expected,name)
    def test_execution_request_is_bounded_and_local(self):
        req=json.loads((ROOT/'execution-request.json').read_text()); steps=req['plan']['steps']
        self.assertLessEqual(len(steps),req['policy']['max_steps']); self.assertEqual(set(req['policy']['allowed_tools']),{'write_file','read_file'})
        self.assertTrue(all(s['tool'] in {'write_file','read_file'} for s in steps)); self.assertTrue(all(str(s['args']['path']).startswith('/tmp/axiom-robotics-production-sr1-001/') for s in steps))
        self.assertEqual(req['policy']['blast_radius'],'local')
    def test_retained_evidence_is_accepted_and_bounded(self):
        evidence=runner.load(ROOT/'evidence/accepted-20260916/evidence.json'); evaluation=runner.load(ROOT/'evidence/accepted-20260916/evaluation.json')
        runner.validate('simulation-evidence',evidence); runner.validate('evaluation-record',evaluation)
        self.assertEqual(evidence['status'],'PASS'); self.assertEqual(evaluation['result'],'ACCEPT'); self.assertTrue(all(c['passed'] for c in evaluation['checks']))
        self.assertEqual(len(evidence['effect_evidence']),19); self.assertTrue(all(e['state']=='SUCCEEDED' for e in evidence['effect_evidence']))
        self.assertEqual(evidence['limitations'],[]); self.assertEqual(evidence['failures'],[])
        self.assertEqual(len(evidence['recovery']),1); self.assertTrue(evidence['recovery'][0]['effect_files_unchanged'])
        self.assertEqual(evidence['outputs']['authority_gate_negative_control']['apex_response'],None)
if __name__=='__main__': unittest.main()
