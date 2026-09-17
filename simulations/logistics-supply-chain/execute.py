#!/usr/bin/env python3
"""Reproduce the domain simulation simulation with isolated local APEX state."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
SIMULATIONS=HERE.parent
ECOSYSTEM=HERE.parents[2]
sys.path.insert(0,str(SIMULATIONS))
import runner

RUN_ROOT=Path('/tmp/axiom-logistics-supply-chain-001')

def load(name): return json.loads((HERE/name).read_text())
def post(url, body, key):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-Apex-Key':key},method='POST')
    with urllib.request.urlopen(req,timeout=60) as r: return json.load(r)
def wait_health(url,key,proc):
    for _ in range(100):
        if proc.poll() is not None: raise RuntimeError('APEX server exited before health check')
        try:
            req=urllib.request.Request(url+'/health',headers={'X-Apex-Key':key})
            with urllib.request.urlopen(req,timeout=1) as r:
                if r.status==200:return
        except Exception: time.sleep(.05)
    raise RuntimeError('APEX health check timed out')
def snapshot_mtimes():
    return {p.name:p.stat().st_mtime_ns for p in RUN_ROOT.glob('*.json')}
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',type=Path,default=HERE/'evidence'/'latest'); a=ap.parse_args(argv)
    shutil.rmtree(RUN_ROOT,ignore_errors=True); a.out_dir.mkdir(parents=True,exist_ok=True)
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    apex_url=f'http://127.0.0.1:{port}'; key='logistics-supply-chain-simulation-local-key'
    with tempfile.TemporaryDirectory(prefix='axiom-robotics-apex-') as td:
        env=os.environ.copy(); env.update({'PYTHONPATH':str(ECOSYSTEM/'axiom-apex'),'APEX_API_KEY':key,'APEX_HISTORY_DB_PATH':str(Path(td)/'runs.db'),'GEMINI_API_KEY':'offline-exact-plan-only'})
        proc=subprocess.Popen([sys.executable,'-m','apex','serve','--host','127.0.0.1','--port',str(port)],cwd=ECOSYSTEM/'axiom-apex',env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        try:
            wait_health(apex_url,key,proc)
            org=load('organization.json'); scenario=load('scenarios/end-to-end.json'); fixture=load('fixture-manifest.json'); request=load('execution-request.json')
            denied,denied_meta=runner.ason_submit(request,apex_url,'',key)
            authority_gate_ok=bool(denied) and denied.get('accepted') is True and denied.get('apex_response') is None and 'authority_ref is required' in str(denied.get('error','')) and denied_meta.get('exit_code') != 0
            evidence,evaluation=runner.run(org,scenario,fixture,request,RUN_ROOT/'terminal-state.json',apex_url=apex_url,authority_ref='operations-manager:synthetic-approved',api_key=key)
            evidence['outputs']['authority_gate_negative_control']=denied
            evaluation['checks'].append({'id':'missing-authority-blocks-before-apex','passed':authority_gate_ok,'observed':{'exit_code':denied_meta.get('exit_code'),'apex_response':None if not denied else denied.get('apex_response'),'error':None if not denied else denied.get('error')}})
            before=snapshot_mtimes(); run_id=int((evidence['outputs']['apex_response'] or {})['run_id'])
            replay=post(apex_url+'/replay',{'run_id':run_id,'mode':'live'},key); after=snapshot_mtimes()
            recovery_ok=replay.get('exit_code')==0 and before==after and len(before)>0
            evidence['recovery'].append({'mode':'live','run_ref':f'apex:{run_id}','exit_code':replay.get('exit_code'),'effect_files_unchanged':before==after,'observed_file_count':len(before),'output_sha256':hashlib.sha256(str(replay.get('output','')).encode()).hexdigest()})
            evaluation['checks'].append({'id':'live-recovery-reuses-completed-effects','passed':recovery_ok,'observed':{'exit_code':replay.get('exit_code'),'effect_files_unchanged':before==after,'observed_file_count':len(before)}})
            evaluation['result']='ACCEPT' if evaluation['result']=='ACCEPT' and recovery_ok and authority_gate_ok else 'REJECT'; evidence['status']='PASS' if evaluation['result']=='ACCEPT' else 'FAIL'
            runner.validate('simulation-evidence',evidence); runner.validate('evaluation-record',evaluation)
            (a.out_dir/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n'); (a.out_dir/'evaluation.json').write_text(json.dumps(evaluation,indent=2)+'\n')
            summary={'result':evaluation['result'],'run_id':run_id,'modeled_steps':len(scenario['steps']),'effects':len(evidence['effect_evidence']),'events':len(evidence['events']),'authority_gate_ok':authority_gate_ok,'recovery_ok':recovery_ok,'out_dir':str(a.out_dir)}
            (a.out_dir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print(json.dumps(summary))
            return 0 if evaluation['result']=='ACCEPT' else 1
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait()
if __name__=='__main__': raise SystemExit(main())
