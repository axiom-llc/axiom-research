#!/usr/bin/env python3
"""Run one canonical synthetic scenario through ASON→APEX and emit evidence."""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ECOSYSTEM = REPO.parent
SCHEMAS = HERE / 'schemas'


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(kind: str, value) -> None:
    import jsonschema
    schema = load(SCHEMAS / f'{kind}.schema.json')
    jsonschema.validators.validator_for(schema)(schema).validate(value)


def git_revision(name: str) -> str | None:
    path = ECOSYSTEM / name
    if not (path / '.git').exists():
        return None
    cp = subprocess.run(['git','-C',str(path),'rev-parse','HEAD'], text=True, capture_output=True)
    return cp.stdout.strip() if cp.returncode == 0 else None


def ason_submit(request: dict, apex_url: str, authority_ref: str, api_key: str | None) -> tuple[dict | None, dict]:
    env = os.environ.copy()
    if api_key: env['APEX_API_KEY'] = api_key
    cp = subprocess.run(
        [sys.executable, '-m', 'ason', 'submit', '-', '--apex-url', apex_url, '--authority-ref', authority_ref],
        cwd=ECOSYSTEM / 'axiom-ason', input=json.dumps(request), text=True, capture_output=True, env=env,
    )
    meta = {'command':['python','-m','ason','submit','-'],'exit_code':cp.returncode,'stderr':cp.stderr[-2000:]}
    try: return json.loads(cp.stdout), meta
    except json.JSONDecodeError: return None, {**meta, 'stdout':cp.stdout[-2000:]}


def apex_detail(apex_url: str, run_id: int, api_key: str | None) -> dict:
    headers = {'X-Apex-Key': api_key} if api_key else {}
    req = urllib.request.Request(f'{apex_url.rstrip("/")}/runs/{run_id}', headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp: return json.load(resp)


def evaluate(scenario: dict, evidence: dict) -> dict:
    contract = scenario['acceptance_contract']; checks=[]
    response = evidence['outputs'].get('apex_response') or {}
    detail = evidence['outputs'].get('apex_run_detail') or {}
    auth = evidence['outputs'].get('authorization') or {}
    if contract['require_apex_success']:
        observed = response.get('exit_code')
        checks.append({'id':'apex-success','passed':observed == 0,'observed':observed})
    if contract['require_authorization_binding']:
        bound = bool(auth) and detail.get('authorization') == auth and detail.get('ledger',{}).get('plan_digest') == auth.get('approved_plan_digest')
        checks.append({'id':'authorization-binding','passed':bound,'observed':bound})
    expected = contract['terminal_state_equals']; actual = evidence['terminal_state']
    checks.append({'id':'terminal-state','passed':actual == expected,'observed':actual})
    for requirement in scenario['evidence_requirements']:
        if requirement == 'effect-ledger': present = bool(detail.get('ledger')) and isinstance(detail.get('effects'), list)
        elif requirement == 'authorization': present = bool(detail.get('authorization'))
        else: present = False
        checks.append({'id':f'evidence:{requirement}','passed':present,'observed':present})
    submission = evidence['outputs'].get('ason_submission')
    infrastructure_unknown = submission is None or (submission.get('accepted') is True and submission.get('error') and submission.get('apex_response') is None)
    result = 'INCONCLUSIVE' if infrastructure_unknown else ('ACCEPT' if checks and all(c['passed'] for c in checks) else 'REJECT')
    return {'schema':'axiom-simulation/evaluation-record-v1','evaluation_id':evidence['evidence_id']+':evaluation','evidence_ref':evidence['evidence_id'],'acceptance_contract':contract,'checks':checks,'result':result,'limitations':list(evidence['limitations'])}


def run(org: dict, scenario: dict, fixture: dict, request: dict, terminal_path: Path, *, apex_url: str, authority_ref: str, api_key: str | None) -> tuple[dict,dict]:
    for kind,value in [('organization-model',org),('scenario-spec',scenario),('fixture-manifest',fixture)]: validate(kind,value)
    if scenario['organization_ref'] == '' or fixture['scenario_id'] != scenario['scenario_id'] or org['domain'] != scenario['domain']:
        raise ValueError('scenario, organization, and fixture identity mismatch')
    submitted, submit_meta = ason_submit(request, apex_url, authority_ref, api_key)
    detail={}; limitations=[]; failures=[]
    if submitted and (submitted.get('apex_response') or {}).get('run_id') is not None:
        try: detail=apex_detail(apex_url, int(submitted['apex_response']['run_id']), api_key)
        except Exception as exc: limitations.append(f'APEX run detail unavailable: {exc}')
    elif not submitted: limitations.append('ASON output was not valid JSON')
    if submit_meta['exit_code'] != 0: failures.append({'stage':'ason-submit','detail':submit_meta})
    terminal = load(terminal_path) if terminal_path.exists() else {}
    revisions={}
    for name in ('axiom-research','axiom-ason','axiom-apex'):
        rev=git_revision(name)
        if rev: revisions[name]=rev
    auth=(submitted or {}).get('authorization') or {}
    run_id=((submitted or {}).get('apex_response') or {}).get('run_id')
    evidence={
      'schema':'axiom-simulation/evidence-v1','evidence_id':scenario['scenario_id']+':run','scenario_id':scenario['scenario_id'],
      'classification':scenario['classification'],'status':'INCONCLUSIVE','repository_revisions':revisions,
      'scenario_sha256':digest(scenario),'fixture_sha256':digest(fixture),
      'configuration':{'execution_request_sha256':digest(request),'apex_url':apex_url,'authority_ref':authority_ref},
      'axiom_components':['axiom-ason','axiom-apex'],'run_refs':([f'apex:{run_id}'] if run_id is not None else []),
      'authorization_refs':([auth.get('authorization_id')] if auth.get('authorization_id') else []),
      'effect_evidence':detail.get('effects',[]),'events':detail.get('events',[]),
      'outputs':{'ason_submission':submitted,'apex_response':(submitted or {}).get('apex_response'),'authorization':auth,'apex_run_detail':detail},
      'terminal_state':terminal,'failures':failures,'recovery':[],
      'metrics':{'modeled_steps':len(scenario['steps']),'effect_count':len(detail.get('effects',[])),'event_count':len(detail.get('events',[]))},
      'limitations':limitations,
    }
    evaluation=evaluate(scenario,evidence); evidence['status']={'ACCEPT':'PASS','REJECT':'FAIL','INCONCLUSIVE':'INCONCLUSIVE'}[evaluation['result']]
    validate('simulation-evidence',evidence); validate('evaluation-record',evaluation)
    return evidence,evaluation


def main(argv=None) -> int:
    ap=argparse.ArgumentParser()
    for flag in ('organization','scenario','fixture','request','terminal-state'): ap.add_argument('--'+flag, type=Path, required=True)
    ap.add_argument('--apex-url',default=os.environ.get('APEX_URL','http://127.0.0.1:8080')); ap.add_argument('--authority-ref',required=True)
    ap.add_argument('--evidence-out',type=Path,required=True); ap.add_argument('--evaluation-out',type=Path,required=True)
    a=ap.parse_args(argv)
    evidence,evaluation=run(load(a.organization),load(a.scenario),load(a.fixture),load(a.request),a.terminal_state,apex_url=a.apex_url,authority_ref=a.authority_ref,api_key=os.environ.get('APEX_API_KEY'))
    a.evidence_out.write_text(json.dumps(evidence,indent=2)+'\n'); a.evaluation_out.write_text(json.dumps(evaluation,indent=2)+'\n')
    print(json.dumps({'evidence':str(a.evidence_out),'evaluation':str(a.evaluation_out),'result':evaluation['result']}))
    return 0 if evaluation['result']=='ACCEPT' else 1
if __name__=='__main__': raise SystemExit(main())
