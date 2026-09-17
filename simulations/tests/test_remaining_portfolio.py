import hashlib, json, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner
ROOT=Path(__file__).resolve().parents[1]
DOMAINS={
 'software-development': {'steps':15,'effects':15,'failures':{'retry_safe','non_retry_safe'}},
 'specialty-care-administration': {'steps':12,'effects':13,'failures':{'dependency_unavailable'}},
 'soc-operations': {'steps':12,'effects':13,'failures':{'retry_safe','approval_denied'}},
 'logistics-supply-chain': {'steps':13,'effects':14,'failures':{'dependency_unavailable','retry_safe'}},
}
class RemainingPortfolioTests(unittest.TestCase):
    def test_contracts_authority_and_failure_paths(self):
        for slug,expect in DOMAINS.items():
            with self.subTest(slug=slug):
                d=ROOT/slug; org=runner.load(d/'organization.json'); sc=runner.load(d/'scenarios/end-to-end.json'); fx=runner.load(d/'fixture-manifest.json')
                for kind,value in [('organization-model',org),('scenario-spec',sc),('fixture-manifest',fx)]: runner.validate(kind,value)
                actors={a['id']:a for a in org['actors']}; steps={s['id']:s for s in sc['steps']}
                self.assertEqual(len(steps),expect['steps']); self.assertTrue(all(s['actor'] in actors for s in sc['steps']))
                self.assertTrue(all(dep in steps for s in sc['steps'] for dep in s['depends_on']))
                self.assertTrue(all(s['approval_ref'] is None or s['approval_ref'] in actors[s['actor']]['authority'] for s in sc['steps']))
                self.assertTrue(expect['failures'].issubset({f['failure_class'] for f in sc['failure_injections']}))
    def test_fixture_hashes_and_synthetic_boundary(self):
        for slug in DOMAINS:
            with self.subTest(slug=slug):
                d=ROOT/slug; fx=runner.load(d/'fixture-manifest.json'); self.assertTrue(fx['synthetic']); self.assertFalse(fx['contains_private_data'])
                for name,expected in fx['artifact_hashes'].items(): self.assertEqual(hashlib.sha256((d/'fixtures'/name).read_bytes()).hexdigest(),expected,name)
    def test_execution_requests_are_local_and_bounded(self):
        for slug in DOMAINS:
            with self.subTest(slug=slug):
                d=ROOT/slug; req=runner.load(d/'execution-request.json'); steps=req['plan']['steps']; prefix=f'/tmp/axiom-{slug}-001/'
                self.assertLessEqual(len(steps),req['policy']['max_steps']); self.assertEqual(set(req['policy']['allowed_tools']),{'write_file','read_file'}); self.assertEqual(req['policy']['blast_radius'],'local')
                self.assertTrue(all(s['tool'] in {'write_file','read_file'} for s in steps)); self.assertTrue(all(str(s['args']['path']).startswith(prefix) for s in steps))

    def test_retained_evidence_is_accepted_and_bounded(self):
        for slug,expect in DOMAINS.items():
            with self.subTest(slug=slug):
                d=ROOT/slug/'evidence'/'accepted-20260916'; evidence=runner.load(d/'evidence.json'); evaluation=runner.load(d/'evaluation.json')
                runner.validate('simulation-evidence',evidence); runner.validate('evaluation-record',evaluation)
                self.assertEqual(evidence['status'],'PASS'); self.assertEqual(evaluation['result'],'ACCEPT'); self.assertTrue(all(c['passed'] for c in evaluation['checks']))
                self.assertEqual(len(evidence['effect_evidence']),expect['effects']); self.assertTrue(all(e['state']=='SUCCEEDED' for e in evidence['effect_evidence']))
                self.assertEqual(evidence['limitations'],[]); self.assertEqual(evidence['failures'],[])
                self.assertEqual(len(evidence['recovery']),1); self.assertTrue(evidence['recovery'][0]['effect_files_unchanged'])
                self.assertIsNone(evidence['outputs']['authority_gate_negative_control']['apex_response'])
                self.assertEqual(evidence['repository_revisions']['axiom-research'],'8519fcbb3e9e9c299d854e009bd4daed8c17b4d9')

if __name__=='__main__': unittest.main()
