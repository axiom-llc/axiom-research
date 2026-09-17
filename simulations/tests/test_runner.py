import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner

FIX=Path(__file__).resolve().parent/'fixtures'/'valid'
class RunnerTests(unittest.TestCase):
    def inputs(self):
        org=runner.load(FIX/'organization-model.json'); scenario=runner.load(FIX/'scenario-spec.json'); fixture=runner.load(FIX/'fixture-manifest.json')
        request={'plan':{'steps':[{'tool':'write_file','args':{'path':'/tmp/state.json','content':'{}'}}]},'policy':{'max_steps':4,'allowed_tools':['write_file'],'blast_radius':'local','rollback_on_failure':False}}
        return org,scenario,fixture,request
    def test_accepts_bound_success_and_terminal_state(self):
        org,scenario,fixture,request=self.inputs(); auth={'authorization_id':'a1','approved_plan_digest':'d','policy_digest_or_ref':'p','authority_ref':'test','decision':True}
        submitted={'accepted':True,'authorization':auth,'apex_response':{'run_id':7,'exit_code':0}}
        detail={'authorization':auth,'ledger':{'plan_digest':'d'},'effects':[{'step':0,'state':'SUCCEEDED'}],'events':[]}
        with tempfile.TemporaryDirectory() as td:
            term=Path(td)/'terminal.json'; term.write_text(json.dumps(scenario['expected_terminal_state']))
            with patch.object(runner,'ason_submit',return_value=(submitted,{'exit_code':0,'command':[]})),patch.object(runner,'apex_detail',return_value=detail),patch.object(runner,'git_revision',return_value='a'*40):
                ev,evaluation=runner.run(org,scenario,fixture,request,term,apex_url='http://apex',authority_ref='test',api_key='k')
        self.assertEqual(ev['status'],'PASS'); self.assertEqual(evaluation['result'],'ACCEPT'); self.assertTrue(all(c['passed'] for c in evaluation['checks']))
    def test_rejects_authorization_mismatch(self):
        org,scenario,fixture,request=self.inputs(); auth={'authorization_id':'a1','approved_plan_digest':'d','policy_digest_or_ref':'p','authority_ref':'test','decision':True}
        submitted={'accepted':True,'authorization':auth,'apex_response':{'run_id':7,'exit_code':0}}
        detail={'authorization':dict(auth,authority_ref='other'),'ledger':{'plan_digest':'d'},'effects':[],'events':[]}
        with tempfile.TemporaryDirectory() as td:
            term=Path(td)/'terminal.json'; term.write_text(json.dumps(scenario['expected_terminal_state']))
            with patch.object(runner,'ason_submit',return_value=(submitted,{'exit_code':0,'command':[]})),patch.object(runner,'apex_detail',return_value=detail),patch.object(runner,'git_revision',return_value='a'*40):
                ev,evaluation=runner.run(org,scenario,fixture,request,term,apex_url='http://apex',authority_ref='test',api_key=None)
        self.assertEqual(ev['status'],'FAIL'); self.assertEqual(evaluation['result'],'REJECT')
    def test_transport_failure_is_inconclusive(self):
        org,scenario,fixture,request=self.inputs(); auth={'authorization_id':'a1','approved_plan_digest':'d','policy_digest_or_ref':'p','authority_ref':'test','decision':True}
        submitted={'accepted':True,'authorization':auth,'apex_response':None,'error':'connection refused'}
        with tempfile.TemporaryDirectory() as td:
            with patch.object(runner,'ason_submit',return_value=(submitted,{'exit_code':1,'command':[]})),patch.object(runner,'git_revision',return_value='a'*40):
                ev,evaluation=runner.run(org,scenario,fixture,request,Path(td)/'missing.json',apex_url='http://apex',authority_ref='test',api_key=None)
        self.assertEqual(ev['status'],'INCONCLUSIVE'); self.assertEqual(evaluation['result'],'INCONCLUSIVE')

    def test_missing_terminal_state_rejects(self):
        org,scenario,fixture,request=self.inputs(); submitted={'accepted':False,'violations':['blocked'],'apex_response':None}
        with tempfile.TemporaryDirectory() as td:
            with patch.object(runner,'ason_submit',return_value=(submitted,{'exit_code':1,'command':[]})),patch.object(runner,'git_revision',return_value='a'*40):
                ev,evaluation=runner.run(org,scenario,fixture,request,Path(td)/'missing.json',apex_url='http://apex',authority_ref='test',api_key=None)
        self.assertEqual(evaluation['result'],'REJECT'); self.assertTrue(ev['failures'])
if __name__=='__main__': unittest.main()
