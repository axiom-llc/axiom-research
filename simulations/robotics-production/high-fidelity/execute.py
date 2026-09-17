#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
SIMULATIONS=HERE.parents[1]
ECOSYSTEM=HERE.parents[3]
sys.path.insert(0,str(SIMULATIONS)); sys.path.insert(0,str(ECOSYSTEM/'axiom-harness'))
import runner
from axiom_harness import HarnessStore, ResourceSpec, TaskSpec

RUN_ROOT=Path('/tmp/axiom-robotics-hifi-day-001')
PHASES=[('engineering-procurement',1,8,'buyer-desk'),('production-test',9,16,'build-cell'),('quality-release',17,22,'quality-desk'),('field-close',23,28,'field-ops')]

def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()+b'\n'
def wait_health(url,key,proc):
    for _ in range(100):
        if proc.poll() is not None: raise RuntimeError('APEX exited before health')
        try:
            req=urllib.request.Request(url+'/health',headers={'X-Apex-Key':key})
            with urllib.request.urlopen(req,timeout=1) as r:
                if r.status==200:return
        except Exception: time.sleep(.05)
    raise RuntimeError('APEX health timeout')
def verify_record(record):
    runner.validate('operational-fidelity',record)
    ids=set(); actors={x['id'] for x in record['actors']}
    for key in ('actors','resources','schedules','queues','decisions','communications','transactions','inventory_movements','documents','events','situations','issues','approvals','state_transitions','outcomes'):
        vals=[x['id'] for x in record[key]]
        if len(vals)!=len(set(vals)): raise ValueError(f'duplicate ids in {key}')
        ids.update(vals)
    seen=set(); last=''
    for op in record['operations']:
        if op['actor_ref'] not in actors or not set(op['refs'])<=ids or op['result_ref'] not in ids: raise ValueError('unresolved operation reference')
        if not set(op['causes'])<=seen or op['at']<last: raise ValueError('causal or chronological violation')
        seen.add(op['id']); last=op['at']
    chain=record['state_transitions']
    if chain[0]['from']!='NEW' or any(a['to']!=b['from'] for a,b in zip(chain,chain[1:])): raise ValueError('state chain discontinuity')
    return {'operations':len(record['operations']),'synthetic_cost_usd':sum(x['amount_usd'] for x in record['transactions']),'inventory_movements':len(record['inventory_movements']),'documents':len(record['documents']),'communications':len(record['communications']),'approvals':len(record['approvals'])}
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); a=ap.parse_args(argv)
    record=runner.load(HERE/'operating-day.json'); audit=verify_record(record)
    revisions={n:runner.git_revision(n) for n in ('axiom-research','axiom-ason','axiom-apex','axiom-harness')}
    revisions={k:v for k,v in revisions.items() if v}
    shutil.rmtree(RUN_ROOT,ignore_errors=True); RUN_ROOT.mkdir(parents=True); a.out_dir.mkdir(parents=True,exist_ok=True)
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    apex_url=f'http://127.0.0.1:{port}'; key='robotics-hifi-local-key'
    with tempfile.TemporaryDirectory(prefix='axiom-robotics-hifi-') as td:
        env=os.environ.copy(); env.update({'PYTHONPATH':str(ECOSYSTEM/'axiom-apex'),'APEX_API_KEY':key,'APEX_HISTORY_DB_PATH':str(Path(td)/'apex.db'),'GEMINI_API_KEY':'offline-exact-plan-only'})
        proc=subprocess.Popen([sys.executable,'-m','apex','serve','--host','127.0.0.1','--port',str(port)],cwd=ECOSYSTEM/'axiom-apex',env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        try:
            wait_health(apex_url,key,proc); phase_evidence=[]; receipts=[]; authority_gate_ok=False
            with HarnessStore(Path(td)/'harness.db') as store:
                for phase,start,end,resource_id in PHASES:
                    ops=record['operations'][start-1:end]
                    result={'phase':phase,'status':'COMPLETE','operation_ids':[o['id'] for o in ops]}
                    result_bytes=canonical(result); task_id=f'robotics-day:{phase}'
                    store.submit_task(TaskSpec(task_id=task_id,intent_ref=record['record_id'],domain='robotics-production',capabilities=('filesystem','simulation'),expected_result_sha256=hashlib.sha256(result_bytes).hexdigest(),mutation_class='M1',cash_ceiling=0.0,context_budget=32768,retry_budget=0),now=100+start)
                    store.register_resource(ResourceSpec(resource_id=resource_id,capabilities=('filesystem','simulation'),maximum_mutation_class='M1',hard_zero_spend_eligible=True,context_limit=32768),now=100+start)
                    context=canonical({'record_id':record['record_id'],'phase':phase,'operations':ops})
                    lease=store.acquire_lease(task_id,resource_id,context,ttl_seconds=300,now=200+start,lease_id=f'lease-{phase}')
                    phase_dir=RUN_ROOT/phase; phase_dir.mkdir(parents=True,exist_ok=True)
                    ops_path=phase_dir/'operations.json'; result_path=phase_dir/'result.json'; snapshot_path=phase_dir/'snapshot.json'
                    snapshot={'phase':phase,'last_operation':ops[-1]['id'],'terminal_transition':record['state_transitions'][min(end-1,len(record['state_transitions'])-1)]['to']}
                    request={'plan':{'steps':[{'tool':'write_file','args':{'path':str(ops_path),'content':json.dumps(ops,indent=2)+'\n'}},{'tool':'write_file','args':{'path':str(snapshot_path),'content':json.dumps(snapshot,indent=2)+'\n'}},{'tool':'write_file','args':{'path':str(result_path),'content':result_bytes.decode()}},{'tool':'read_file','args':{'path':str(result_path)}}]},'policy':{'max_steps':8,'allowed_tools':['write_file','read_file'],'blast_radius':'local','rollback_on_failure':False}}
                    
                    if phase==PHASES[0][0]:
                        denied,denied_meta=runner.ason_submit(request,apex_url,'',key)
                        authority_gate_ok=bool(denied) and denied.get('apex_response') is None and denied_meta.get('exit_code')!=0
                    submitted,meta=runner.ason_submit(request,apex_url,f'robotics-operations:{phase}:synthetic-approved',key)
                    response=(submitted or {}).get('apex_response') or {}
                    if meta['exit_code']!=0 or response.get('exit_code')!=0: raise RuntimeError(f'phase execution failed: {phase}: {submitted}')
                    detail=runner.apex_detail(apex_url,int(response['run_id']),key)
                    actual=result_path.read_bytes(); attempt=store.record_attempt(lease.lease_id,result=actual,result_ref=str(result_path),started_at=250+start,completed_at=251+start,attempt_id=f'attempt-{phase}')
                    receipt=store.commit_accepted(attempt.attempt_id,now=252+start); receipts.append(receipt)
                    auth=submitted['authorization']; bound=detail.get('authorization')==auth and detail.get('ledger',{}).get('plan_digest')==auth.get('approved_plan_digest')
                    phase_evidence.append({'phase':phase,'run_id':response['run_id'],'authorization':auth,'authorization_binding':bound,'ledger':detail.get('ledger',{}),'effects':detail.get('effects',[]),'events':detail.get('events',[]),'harness_receipt':receipt})
                if store.check()!={'ok':True,'schema_version':1}: raise RuntimeError('Harness check failed')
            report={'schema':'axiom-simulation/operational-reconstruction-v1','repository_revisions':revisions,'authority_gate_ok':authority_gate_ok,'authorization_bindings_ok':all(x['authorization_binding'] for x in phase_evidence),'record_id':record['record_id'],'result':'ACCEPT','audit':audit,'phase_count':len(PHASES),'harness_receipts':receipts,'apex_runs':[x['run_id'] for x in phase_evidence],'effect_count':sum(len(x['effects']) for x in phase_evidence),'event_count':sum(len(x['events']) for x in phase_evidence),'final_state':record['state_transitions'][-1]['to'],'source_sha256':hashlib.sha256((HERE/'operating-day.json').read_bytes()).hexdigest()}
            (a.out_dir/'reconstruction.json').write_text(json.dumps(report,indent=2)+'\n'); (a.out_dir/'execution-evidence.json').write_text(json.dumps(phase_evidence,indent=2)+'\n')
            print(json.dumps(report)); return 0
        finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
if __name__=='__main__': raise SystemExit(main())
