#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,shutil,socket,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
SIMULATIONS=Path(__file__).resolve().parents[1]
ECOSYSTEM=SIMULATIONS.parents[1]
sys.path.insert(0,str(SIMULATIONS)); sys.path.insert(0,str(ECOSYSTEM/'axiom-harness'))
import runner
from axiom_harness import HarnessStore, LeaseError, ResourceSpec, TaskSpec

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

def validate_cycle(cycle):
    import jsonschema
    schema=json.loads((SIMULATIONS/'operational-fidelity/operational-cycle.schema.json').read_text())
    jsonschema.validate(cycle,schema)
    assert all(cycle['completeness'].values())
    entities={x['id'] for x in cycle['entities']}; resources={x['id'] for x in cycle['resources']}
    assert {x['entity'] for x in cycle['arrivals']}<=entities
    assert {x['id'] for x in cycle['work_items']}==entities
    assert {x['execution_resource'] for x in cycle['work_items']}<=resources
    assert any(x.get('carryover') for x in cycle['work_items'])
    assert len(cycle['days'])>=3 and len(cycle['resource_contention'])>=2
    assert cycle['queue_snapshots'][1].get('open',0)>cycle['queue_snapshots'][0].get('open',0)
    amount=sum(float(x['amount_usd']) for x in cycle['ledger_entries'])
    return {'work_items':len(cycle['work_items']),'days':len(cycle['days']),'contention_cases':len(cycle['resource_contention']),'ledger_entries':len(cycle['ledger_entries']),'ledger_debits_usd':amount,'ledger_credits_usd':amount,'carryover_items':sum(bool(x.get('carryover')) for x in cycle['work_items']),'queue_peak_open':max(x.get('open',0) for x in cycle['queue_snapshots'])}

def execute(*,cycle_path:Path,out_dir:Path,authority_prefix:str,run_root:Path,api_key:str):
    cycle=json.loads(cycle_path.read_text()); audit=validate_cycle(cycle); domain=cycle['domain']
    revisions={n:runner.git_revision(n) for n in ('axiom-research','axiom-ason','axiom-apex','axiom-harness')}; revisions={k:v for k,v in revisions.items() if v}
    shutil.rmtree(run_root,ignore_errors=True); run_root.mkdir(parents=True); out_dir.mkdir(parents=True,exist_ok=True)
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    apex_url=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix=f'axiom-{domain}-cycle-') as td:
        env=os.environ.copy(); env.update({'PYTHONPATH':str(ECOSYSTEM/'axiom-apex'),'APEX_API_KEY':api_key,'APEX_HISTORY_DB_PATH':str(Path(td)/'apex.db'),'GEMINI_API_KEY':'offline-exact-plan-only'})
        proc=subprocess.Popen([sys.executable,'-m','apex','serve','--host','127.0.0.1','--port',str(port)],cwd=ECOSYSTEM/'axiom-apex',env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        try:
            wait_health(apex_url,api_key,proc); evidence=[]; receipts=[]; contention=[]; authority_gate_ok=False
            items={x['id']:x for x in cycle['work_items']}
            with HarnessStore(Path(td)/'harness.db') as store:
                for r in cycle['resources']:
                    store.register_resource(ResourceSpec(resource_id=r['id'],capabilities=('filesystem','simulation'),maximum_mutation_class='M1',hard_zero_spend_eligible=True,context_limit=32768),now=90)
                for idx,item in enumerate(cycle['work_items'],1):
                    result={'work_item':item['id'],'status':item['result'],'day_completed':item['day_completed']}; rb=canonical(result)
                    store.submit_task(TaskSpec(task_id=f"{cycle['cycle_id']}:{item['id']}",intent_ref=cycle['cycle_id'],domain=domain,capabilities=('filesystem','simulation'),expected_result_sha256=hashlib.sha256(rb).hexdigest(),mutation_class='M1',cash_ceiling=0.0,context_budget=32768,retry_budget=0),now=100+idx)
                for idx,item in enumerate(cycle['work_items'],1):
                    task_id=f"{cycle['cycle_id']}:{item['id']}"; context=canonical({'cycle_id':cycle['cycle_id'],'work_item':item,'queue_snapshots':cycle['queue_snapshots'],'staffing_events':cycle['staffing_events'],'calendar_events':cycle['calendar_events']})
                    lease=store.acquire_lease(task_id,item['execution_resource'],context,ttl_seconds=300,now=200+idx*10,lease_id=f"lease-{item['id']}")
                    target=item.get('contention_probe')
                    if target:
                        blocked=False
                        try: store.acquire_lease(f"{cycle['cycle_id']}:{target}",items[target]['execution_resource'],canonical({'probe':target}),ttl_seconds=30,now=201+idx*10,lease_id=f"probe-{target}")
                        except LeaseError: blocked=True
                        contention.append({'holder':item['id'],'blocked':target,'resource':item['execution_resource'],'exclusive_lease_blocked':blocked})
                    wd=run_root/item['id']; wd.mkdir(parents=True,exist_ok=True); result_path=wd/'result.json'; context_path=wd/'context.json'; ledger_path=wd/'ledger.json'
                    result={'work_item':item['id'],'status':item['result'],'day_completed':item['day_completed']}; rb=canonical(result)
                    request={'plan':{'steps':[{'tool':'write_file','args':{'path':str(context_path),'content':context.decode()}},{'tool':'write_file','args':{'path':str(ledger_path),'content':json.dumps(cycle['ledger_entries'],indent=2)+'\n'}},{'tool':'write_file','args':{'path':str(result_path),'content':rb.decode()}},{'tool':'read_file','args':{'path':str(result_path)}}]},'policy':{'max_steps':8,'allowed_tools':['write_file','read_file'],'blast_radius':'local','rollback_on_failure':False}}
                    if idx==1:
                        denied,m0=runner.ason_submit(request,apex_url,'',api_key); authority_gate_ok=bool(denied) and denied.get('apex_response') is None and m0.get('exit_code')!=0
                    submitted,meta=runner.ason_submit(request,apex_url,f'{authority_prefix}:{item["id"]}:synthetic-approved',api_key); response=(submitted or {}).get('apex_response') or {}
                    if meta['exit_code']!=0 or response.get('exit_code')!=0: raise RuntimeError(f'work item failed: {item["id"]}')
                    detail=runner.apex_detail(apex_url,int(response['run_id']),api_key); attempt=store.record_attempt(lease.lease_id,result=result_path.read_bytes(),result_ref=str(result_path),started_at=205+idx*10,completed_at=206+idx*10,attempt_id=f"attempt-{item['id']}"); receipt=store.commit_accepted(attempt.attempt_id,now=207+idx*10); receipts.append(receipt)
                    auth=submitted['authorization']; bound=detail.get('authorization')==auth and detail.get('ledger',{}).get('plan_digest')==auth.get('approved_plan_digest')
                    evidence.append({'work_item':item['id'],'run_id':response['run_id'],'authorization_binding':bound,'authorization':auth,'effects':detail.get('effects',[]),'events':detail.get('events',[]),'receipt':receipt})
                assert store.check()=={'ok':True,'schema_version':1}
            report={'schema':'axiom-simulation/operational-cycle-reconstruction-v1','cycle_id':cycle['cycle_id'],'domain':domain,'result':'ACCEPT' if authority_gate_ok and all(x['exclusive_lease_blocked'] for x in contention) and all(x['authorization_binding'] for x in evidence) else 'FAIL','repository_revisions':revisions,'source_sha256':hashlib.sha256(cycle_path.read_bytes()).hexdigest(),'audit':audit,'authority_gate_ok':authority_gate_ok,'contention':contention,'contention_ok':all(x['exclusive_lease_blocked'] for x in contention),'harness_receipts':receipts,'authorization_bindings_ok':all(x['authorization_binding'] for x in evidence),'effect_count':sum(len(x['effects']) for x in evidence),'event_count':sum(len(x['events']) for x in evidence),'all_effects_succeeded':all(e.get('state')=='SUCCEEDED' for x in evidence for e in x['effects']),'outcomes':cycle['outcomes']}
            (out_dir/'cycle-reconstruction.json').write_text(json.dumps(report,indent=2)+'\n'); (out_dir/'cycle-execution-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n'); print(json.dumps(report)); return report
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait()
