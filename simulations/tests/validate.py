#!/usr/bin/env python3
"""Validate simulation contracts and paired deterministic fixtures."""
from __future__ import annotations
import json, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1]; SCHEMAS=ROOT/'schemas'; FIXTURES=Path(__file__).resolve().parent/'fixtures'

def semantic_checks(fixtures):
    org=fixtures['organization-model']; scenario=fixtures['scenario-spec']; manifest=fixtures['fixture-manifest']
    departments={d['id'] for d in org['departments']}; actors={a['id']:a for a in org['actors']}
    if any(a['department'] not in departments for a in org['actors']): return 'actor references unknown department'
    steps={s['id']:s for s in scenario['steps']}
    if len(steps)!=len(scenario['steps']): return 'duplicate scenario step id'
    if any(s['actor'] not in actors for s in scenario['steps']): return 'scenario step references unknown actor'
    if any(dep not in steps for s in scenario['steps'] for dep in s['depends_on']): return 'scenario step references unknown dependency'
    visiting=set(); done=set()
    def visit(node):
        if node in done: return False
        if node in visiting: return True
        visiting.add(node)
        if any(visit(dep) for dep in steps[node]['depends_on']): return True
        visiting.remove(node); done.add(node); return False
    if any(visit(node) for node in steps): return 'scenario dependency cycle'
    failures={f['id'] for f in scenario['failure_injections']}
    if len(failures)!=len(scenario['failure_injections']): return 'duplicate failure injection id'
    if any(f['target_step'] not in steps for f in scenario['failure_injections']): return 'failure injection targets unknown step'
    if manifest['scenario_id']!=scenario['scenario_id']: return 'fixture manifest scenario mismatch'
    return None
def load(p): return json.loads(p.read_text())
def main():
    paths=sorted(SCHEMAS.glob('*.schema.json'))
    if not paths: print('ERROR: no simulation schemas',file=sys.stderr); return 2
    validators={}
    for p in paths:
        schema=load(p); cls=jsonschema.validators.validator_for(schema); cls.check_schema(schema); validators[p.name.removesuffix('.schema.json')]=cls(schema)
    expected=set(validators)
    for kind,should_pass in [('valid',True),('invalid',False)]:
        found={p.stem:p for p in sorted((FIXTURES/kind).glob('*.json'))}
        if set(found)!=expected:
            print(f'ERROR: {kind} fixture/schema mismatch missing={sorted(expected-set(found))} extra={sorted(set(found)-expected)}',file=sys.stderr); return 2
        for name in sorted(expected):
            errors=list(validators[name].iter_errors(load(found[name])))
            if should_pass and errors: print(f'FAIL valid/{name}.json: {errors[0].message}',file=sys.stderr); return 1
            if not should_pass and not errors: print(f'FAIL invalid/{name}.json unexpectedly validated',file=sys.stderr); return 1
    fixtures={name:load(FIXTURES/'valid'/f'{name}.json') for name in expected}
    semantic_error=semantic_checks(fixtures)
    if semantic_error: print(f'FAIL semantic validation: {semantic_error}',file=sys.stderr); return 1
    claim=fixtures['claim-record']; evidence=fixtures['simulation-evidence']; evaluation=fixtures['evaluation-record']
    if evidence['evidence_id'] not in claim['evidence_refs']: print('FAIL claim does not reference retained evidence',file=sys.stderr); return 1
    if evaluation['evidence_ref']!=evidence['evidence_id']: print('FAIL evaluation/evidence reference mismatch',file=sys.stderr); return 1
    if evidence['status']=='PASS' and evaluation['result']!='ACCEPT': print('FAIL passing retained evidence is not accepted by fixture evaluation',file=sys.stderr); return 1
    print(f'simulation contracts: {len(validators)} schemas, {len(validators)*2} fixtures, semantic references OK'); return 0
if __name__=='__main__': raise SystemExit(main())
