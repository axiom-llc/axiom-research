# Canonical Verified-Execution Transaction Boundary

**Queue item:** RQ-2026-10-06-019  
**Date:** 2026-10-06  
**Director revision:** `17963cad6dee8a43e4999a5bd0751e9250a8c660`  
**Research revision:** `6f097a86b461b7a187f1ef40ea00d855819b9226`  
**Status:** research only; no route-selection change, runtime activation, schema migration, deployment, or spend

## Question

What is the smallest Director-owned composition contract that can sequence authorized dispatch, caller-owned independent validation, and durable observation without changing channel selection or activating a new runtime?

## Decision

Add a new reusable module named `modules/verified_execution.py` as the canonical **transaction boundary**, not as a daemon, provider adapter, CLI, HTTP service, scheduler, or new authority.

The module should compose existing responsibilities in this fixed order:

`TaskEnvelope -> dispatch_task -> independent verifier -> observation sink -> verified result`

It should not own:

- channel registration, provider transport, credentials, or live probes;
- task selection, authorization, or approval;
- route policy or adaptive objective weights;
- the filesystem path or lifecycle of a durable store;
- workflow scheduling;
- canonical task acceptance.

Callers inject adapters, an independent verifier, and an observation sink. The new boundary owns sequencing, identity checks, and fail-visible propagation only. This establishes one testable path that future hosted runtimes may call without prematurely choosing a production process or telemetry schema.

## Evidence

This decision is bound to the exact Director revision above.

Current source establishes:

- [execution_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_runtime.py) owns immutable envelopes, live channel gating, deterministic selection, one dispatch, and receipt digest/effect validation.
- [execution-channels.md](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution-channels.md) requires authoritative postcondition validation outside provider runtimes and states that channel output is evidence, not canonical state.
- [execution_telemetry.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_telemetry.py) contains route-performance metrics but currently derives acceptance from executor status.
- [telemetry_store.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/telemetry_store.py) is an optional SQLite implementation, not a composition owner.
- [INTERFACES.md](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/agent/INTERFACES.md) requires external evidence before completion.
- [director.md](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/director.md) keeps planning, authorization, execution, independent verification, and canonical state separate.
- The accepted [composition-boundary audit](https://github.com/axiom-llc/axiom-research/blob/6f097a86b461b7a187f1ef40ea00d855819b9226/2026-10-06-execution-telemetry-composition-boundary-chatgpt.md) found no existing production caller that owns the complete transaction.

No external web evidence is needed because this is a repository-specific ownership and interface decision.

## Alternatives

### Extend `dispatch_task`

Rejected.

`dispatch_task` is the provider-neutral dispatch primitive. Adding independent verification and persistence would make a low-level routing function own caller policy and storage lifecycle. It would also make every adapter dispatch depend on a persistence choice.

### Extend `portable_runtime.py`

Rejected.

The portable API calculates routes and envelopes from caller-supplied documents. It does not dispatch. Making it the composition owner would activate a new effect path and risk persisting caller-supplied metrics as if they were observed outcomes.

### Extend `autonomy_runtime.py`

Rejected.

That runtime is a fixed read-only GitHub maintenance attachment. It has caller-owned verification, but its actions and receipts are not the portable execution contract. Broadening it would violate its narrow role.

### Add only schema-v3 columns

Rejected as the next step.

A schema without one authoritative producer preserves the current wiring gap. Field design cannot establish sequencing or evidence authority.

### New transaction-boundary module

Accepted.

A pure, dependency-injected module can establish the exact sequencing and evidence contract without activating a provider, process, endpoint, schedule, or durable database.

## Typed interface contract

Names below are implementation decisions for the bounded candidate.

### `ValidationEvidence`

Immutable value object:

- `status: str` — one of `PASSED`, `FAILED`, `NOT_REQUIRED`, `UNKNOWN`;
- `validator_kind: str` — non-empty stable verifier class;
- `subject_digest: str` — must equal the bound task envelope digest;
- `evidence_ref: str | None` — durable address when actually available;
- `failure_class: str | None` — bounded reason for `FAILED` or `UNKNOWN`;
- `observed_at: str | None` — actual externally supplied UTC observation time; never synthesized from an unavailable clock.

Rules:

1. `PASSED` requires `evidence_ref`.
2. `FAILED` requires `failure_class`.
3. `UNKNOWN` requires `failure_class`.
4. `NOT_REQUIRED` must not carry an evidence reference or failure class.
5. Every non-null string is trimmed and non-empty.
6. The transaction boundary rejects a subject-digest mismatch.

### `IndependentVerifier`

Protocol:

`verify(envelope: TaskEnvelope, dispatch: DispatchResult) -> ValidationEvidence`

The verifier is caller-owned. It may inspect authoritative remote state, CI, or another task-specific source. It must not treat `ExecutionReceipt.status` or `ExecutionReceipt.validation` as independent proof.

### `VerifiedExecutionObservation`

Immutable record containing:

- task digest and source revision;
- selected channel ID;
- executor receipt status;
- independent validation evidence;
- observed dispatch latency supplied by the existing dispatch observer;
- actual receipt resource counts already available.

This contract is intentionally separate from `ExecutionMetric` schema v2. It avoids falsely mapping missing validation or usage into legacy fields before schema-v3 design is implemented.

### `ExecutionObservationSink`

Protocol:

`append(observation: VerifiedExecutionObservation) -> object`

The sink owns storage and may be in-memory, SQLite-backed, remote, or disabled by an explicit caller choice. The boundary does not select a path, open a database, or suppress sink failure.

### `VerifiedDispatchResult`

Immutable result containing:

- existing `DispatchResult`;
- `ValidationEvidence`;
- the exact `VerifiedExecutionObservation` submitted to the sink.

### `execute_verified`

Inputs:

- immutable task envelope;
- adapter iterable;
- required independent verifier;
- required observation sink;
- optional existing selector, background preference, and monotonic clock injection.

Sequence:

1. call existing `dispatch_task` exactly once;
2. use a private observer to capture dispatch latency without altering selection;
3. invoke the independent verifier exactly once;
4. validate evidence identity and structural invariants;
5. construct one observation;
6. append exactly once;
7. return the verified result.

## Failure semantics

| Failure | Required behavior |
|---|---|
| Probe, selection, dispatch, receipt-binding, or effect validation error | Propagate existing exception; do not call verifier or sink. |
| Verifier returns malformed or mismatched evidence | Raise boundary error; do not append. |
| Verifier reports `FAILED` or `UNKNOWN` | Append that actual result and return it; never promote executor `SUCCEEDED` to acceptance. |
| Verifier raises unexpectedly | Propagate; do not manufacture evidence or acceptance. |
| Sink append fails | Propagate; do not report durable observation or successful transaction completion. |
| Sink returns an implementation-specific receipt | Preserve it only if a later contract explicitly requires it; first slice may ignore the return value. |

The contract distinguishes execution completion from independent acceptance. A returned `FAILED` or `UNKNOWN` validation result is a valid observed transaction, not a successful accepted task.

## Authority and security properties

The boundary must preserve:

- hard capability, authorization, health, exposure, privacy, and cost gates in `dispatch_task`;
- existing deterministic default route selection;
- adapter ownership of transport only;
- caller ownership of independent verification;
- sink ownership of storage only;
- no authority derived from model, provider, receipt, telemetry, or research output;
- no automatic retry, escalation, release, merge, spending, scheduler, or canonical-state mutation.

The module is orchestration code, not a new control plane.

## Bounded implementation slice

The first candidate should modify only:

- create `modules/verified_execution.py`;
- create `tests/test_verified_execution.py`.

It should not modify:

- `execution_runtime.py`;
- `execution_telemetry.py`;
- `telemetry_store.py`;
- `portable_runtime.py`;
- provider adapters;
- workflows or permissions;
- any active runtime entrypoint.

This contract-only slice is implementation-ready because its owner, interfaces, tests, and non-goals are explicit. It does not claim production telemetry is wired.

## Repository-native validation plan

Required tests:

1. executor `SUCCEEDED` plus verifier `FAILED` remains independently failed in the appended observation;
2. subject-digest mismatch raises before append;
3. verifier executes only after receipt digest/effect validation;
4. sink error propagates;
5. verifier error propagates without fabricated observation;
6. exactly one observation is appended;
7. the selected channel matches direct `select_channel` for the same snapshots;
8. malformed validation status and field combinations are rejected;
9. existing execution-runtime tests remain unchanged and pass.

Strongest repository validation:

- `python -m pytest tests/ -q`;
- the repository’s compile checks;
- `python -m director_state check`;
- `git diff --check`;
- exact-head GitHub Actions/PR checks.

## Promotion gate for later telemetry wiring

Schema-v3 and a durable producer remain blocked until a later candidate supplies:

1. an authorized actual runtime caller of `execute_verified`;
2. a concrete independent verifier for that task class;
3. a durable evidence-reference owner;
4. missing-versus-zero field semantics;
5. migration and round-trip tests;
6. no-route-change proof.

## Falsifiable claims

- Adding the contract-only module will leave existing route-selection tests unchanged.
- A synthetic executor `SUCCEEDED` / verifier `FAILED` transaction will persist as validation `FAILED`.
- No current production behavior will change because no runtime entrypoint imports the new module.
- Any future caller that cannot supply an independent verifier and observation sink will fail to use the canonical boundary rather than silently recording receipt success.

These remain unvalidated until the implementation candidate passes repository-native tests.

## Manager classification

**ACCEPT_WITH_FOLLOWUP.**

The module-level transaction boundary is the smallest justified implementation step. It resolves sequencing and evidence ownership without choosing a provider process or prematurely migrating telemetry storage. A bounded implementation candidate in `axiom-director` is justified; production wiring and schema-v3 remain deferred.
