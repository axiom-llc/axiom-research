# Execution Telemetry Composition Boundary

**Queue item:** RQ-2026-10-06-018  
**Date:** 2026-10-06  
**Director revision:** `17963cad6dee8a43e4999a5bd0751e9250a8c660`  
**Research revision:** `de4366522e67053432b6727c8869bc324a5053bc`  
**Status:** research only; no routing, runtime, workflow, deployment, permission, or spend change

## Question

Which current AXIOM Director entrypoint can own durable `ExecutionMetric` persistence, and which current independent verification result can supply addressable validation evidence without changing routing behavior?

## Executive conclusion

No current Director entrypoint satisfies both requirements at the bound revision.

The repository contains:

- a single-dispatch library function with an optional in-process observer;
- an in-memory metric observer;
- a SQLite metric store;
- a product-facing route/envelope API that does not dispatch or persist;
- a separate read-only autonomy composition root with an independent boolean verification phase.

Repository-wide code search found no production caller that composes `dispatch_task`, `MetricBuffer`, and `TelemetryStore`. It also found no addressable independent validator result linked to a `TaskEnvelope` or `ExecutionReceipt`. The existing receipt `validation` tuple is provider/executor-reported evidence and the runtime documentation explicitly leaves authoritative postcondition verification to callers.

Therefore the telemetry-v3 implementation proposed by the prior audit remains **NOT_IMPLEMENTATION_READY**. Selecting `portable_runtime.py` or `autonomy_runtime.py` as the owner would be speculative and would conflate distinct responsibilities. The smallest non-speculative next decision is to designate or create one canonical execution composition root and one typed, addressable independent-validation result contract. Only after that boundary exists should schema-v3 persistence wiring be implemented.

## Scope and method

This is a revision-bound repository audit, not an empirical runtime test.

Evidence was gathered from current `axiom-director` source and repository-wide default-branch code search at the exact Director revision above. The audit inspected:

- [execution_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_runtime.py)
- [execution_telemetry.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_telemetry.py)
- [telemetry_store.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/telemetry_store.py)
- [portable_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/portable_runtime.py)
- [autonomy_cycle.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/autonomy_cycle.py)
- [autonomy_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/autonomy_runtime.py)
- the corresponding execution, telemetry, store, and autonomy tests
- the accepted [routing telemetry coverage and headroom audit](https://github.com/axiom-llc/axiom-research/blob/de4366522e67053432b6727c8869bc324a5053bc/2026-10-06-routing-telemetry-coverage-headroom-audit-chatgpt.md)

No web evidence was required because the question is exclusively about current repository composition and evidence ownership.

## Repository-wide call graph evidence

### Dispatch boundary

`dispatch_task`:

1. probes adapters;
2. chooses one eligible channel;
3. dispatches once;
4. validates task digest and declared effects;
5. invokes an optional observer;
6. returns `DispatchResult`.

Its docstring explicitly states that it validates only task binding and declared-effect evidence and that callers must independently verify authoritative external postconditions.

Code search found `dispatch_task` only in:

- `modules/execution_runtime.py`;
- `tests/test_execution_runtime.py`;
- `tests/test_callback_adapter.py`.

No product or scheduled runtime caller was found.

### Metric boundary

`MetricBuffer.observer` matches the dispatch observer signature and creates one `ExecutionMetric`. It:

- derives `accepted` from `receipt.status == "SUCCEEDED"`;
- copies latency, cost, token, intervention, retry, and token-class fields;
- does not copy `receipt.validation`;
- retains metrics only in process memory.

Code search found `MetricBuffer` only in:

- `modules/execution_telemetry.py`;
- `tests/test_execution_telemetry.py`.

Search for an explicit `observer=` dispatch binding found only the execution-runtime test.

### Persistence boundary

`TelemetryStore` owns SQLite schema version 2 and can append, extend, and read `ExecutionMetric` rows.

Code search for `TelemetryStore(` found constructor use only in `tests/test_telemetry_store.py`. No production append path was found.

### Product-facing route API

`portable_runtime.py` exposes:

- `/v1/catalog`;
- `/v1/route`;
- `/v1/envelope`;
- equivalent CLI commands.

It parses caller-supplied historical metrics and calls `adaptive_select_channel`, but it does not:

- instantiate adapters;
- call `dispatch_task`;
- independently verify an outcome;
- instantiate `MetricBuffer` or `TelemetryStore`;
- append durable evidence.

It is a routing-calculation surface, not an execution composition root.

### Autonomy composition root

`autonomy_runtime.py` is a real composition root for one bounded purpose: GitHub-native read-only maintenance. It supplies `plan`, `execute`, and `verify` methods to `autonomy_cycle.run_cycles`.

Its verification evidence is materially stronger than executor self-report for that narrow workflow: verification is performed by caller-owned code after execution, and the emitted document includes phase receipts and hashes of inspected state. However:

- it does not use `TaskEnvelope`, `ExecutionReceipt`, `dispatch_task`, or `ExecutionMetric`;
- `CycleReceipt.verified` is a boolean, not an addressable evidence reference;
- its evidence hashes cover its fixed read-only maintenance payloads, not general execution postconditions;
- its workflow artifact retention is external to `TelemetryStore`;
- broadening it into the generic execution runtime would change its declared read-only role.

It is a pattern for separation of execution and verification, not a valid drop-in evidence source for routing telemetry.

## Composition-root candidate comparison

| Candidate | Dispatch owner | Independent verification | Durable metric append | Decision |
|---|---:|---:|---:|---|
| `portable_runtime.py` | No | No | No | Reject as current owner; route/envelope API only. |
| `autonomy_runtime.py` | No generic dispatch | Yes, narrow boolean checks | No execution-metric append | Reject as generic owner; preserve read-only scope. |
| Library-level `dispatch_task` | Performs dispatch | Explicitly caller-owned and absent | Optional observer only | Insufficient alone; libraries cannot choose canonical persistence location. |
| Existing application caller | Not found | Not found | Not found | Cannot integrate without inventing a caller. |
| New designated execution service | Possible | Possible | Possible | Viable only after an explicit ownership/interface decision. |

## Independent validation evidence matrix

| Evidence | Producer | Bound to task | Independent of executor | Addressable | Suitable now |
|---|---|---:|---:|---:|---:|
| `ExecutionReceipt.status` | selected adapter | digest checked | No | No | No |
| `ExecutionReceipt.validation` | selected adapter | receipt-bound | No | String tuple only | No |
| `MetricBuffer.accepted` | observer | metric-bound | No; status-derived | No | No |
| `CycleReceipt.verified` | autonomy caller | action ID | Yes for its narrow action | No durable evidence ref in receipt | No for generic execution |
| autonomy `evidence_sha256` | read-only runtime | named maintenance payload | Yes for its narrow read | Hash in workflow artifact | Pattern only |
| repository CI/status check | GitHub | commit/head | Yes relative to submitted change | Yes: run/check URL | Suitable for repository-change validation, not every routed task |
| future typed validator result | caller-owned verifier | required | Required | Required | Missing contract |

## Required boundary contract

The minimum contract must preserve authority separation and avoid routing behavior changes.

### Canonical execution composition root

A designated caller must own, in one transaction:

1. immutable `TaskEnvelope`;
2. authorized adapter set and selected route revision;
3. `dispatch_task` invocation;
4. independent postcondition verification;
5. one durable observation append after verification;
6. failure handling that records UNKNOWN rather than manufacturing success.

The repository does not currently establish whether this owner should be a new service module, a future hosted runtime, or another externally composed caller. That is an architecture/ownership decision, not a storage implementation detail.

### Typed independent-validation result

The smallest useful result needs:

- `status`: `PASSED | FAILED | NOT_REQUIRED | UNKNOWN`;
- `validator_kind`: stable bounded identifier;
- `evidence_ref`: durable addressable reference when available;
- `subject_digest`: binds evidence to the task/result or exact repository head;
- `failure_class`: bounded cause when failed or unknown;
- `observed_at`: actual UTC observation time.

A receipt-reported string must not silently populate this structure. The caller-owned verifier creates it after dispatch or explicitly records UNKNOWN.

### Durable observation sink

The composition root, not the selector and not the adapter, must append the combined dispatch and validator observation. Storage failures must be visible and must not retroactively change the external result. Missing usage remains null; measured zero remains zero.

## Integration readiness decision

**Decision: NOT_IMPLEMENTATION_READY.**

The prior schema-v3 field design remains reasonable, but two implementation-critical owners are absent:

1. the canonical caller that controls dispatch lifecycle and persistence location;
2. the verifier that can emit addressable independent evidence for that caller.

Adding columns now would create a schema with no authoritative producer. Wiring `TelemetryStore` into `portable_runtime.py` would persist caller-supplied routing inputs rather than actual outcomes. Wiring it into `autonomy_runtime.py` would instrument a separate read-only controller and still leave generic dispatch unobserved. Treating `receipt.validation` as independent would violate the evidence boundary.

## Smallest bounded next step

**Owner:** `axiom-llc/axiom-director`  
**Type:** architecture/interface decision before implementation

Choose exactly one canonical execution composition root and specify its ownership of:

- adapter probing and dispatch;
- route-revision identity;
- postcondition validator invocation;
- evidence-reference durability;
- telemetry append location and failure semantics.

Then add one repository-native contract test that freezes the boundary without changing route choice:

1. construct an immutable task and one authorized adapter;
2. dispatch once;
3. produce caller-owned validation evidence bound to the task/result;
4. append one observation through an injected temporary store;
5. prove a validation failure is stored as failed or unknown, never status-derived success;
6. prove `select_channel` behavior is unchanged.

Only after this test identifies the actual module and interfaces should schema-v3 migration and production wiring proceed.

## Rejection criteria

Reject or defer implementation if:

- the proposed owner is only a selector, parser, adapter, or test helper;
- the validator result is derived solely from `ExecutionReceipt.status` or `ExecutionReceipt.validation`;
- the evidence reference cannot be read independently;
- a storage write changes route selection or dispatch authorization;
- telemetry failure is hidden;
- absent values are encoded as measured zero;
- a read-only runtime must gain execution effects merely to host telemetry;
- the design assumes an external caller that is not identified in repository evidence.

## Falsifiable follow-up hypotheses

- **H1 — UNVALIDATED_HYPOTHESIS:** A future hosted execution service, rather than `portable_runtime.py`, will be the correct composition root because it can own both authorized dispatch and postcondition verification.
- **H2 — UNVALIDATED_HYPOTHESIS:** Repository CI/status checks can supply addressable independent validation evidence for repository-write tasks, but a different validator class will be required for non-repository effects.
- **H3 — UNVALIDATED_HYPOTHESIS:** Once a composition root is designated, the first telemetry rows will expose cases where executor-reported `SUCCEEDED` differs from independent validation.

## Manager classification

**ACCEPT_WITH_FOLLOWUP.**

The audit closes the prior discovery question without fabricating integration: no current entrypoint can correctly own both durable execution telemetry and addressable independent validation. Preserve current routing behavior. Do not implement schema-v3 wiring until Director designates the composition root and validator-result contract.
