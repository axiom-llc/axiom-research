# Routing Telemetry Coverage and Headroom Audit

**Queue item:** RQ-2026-10-06-017  
**Date:** 2026-10-06  
**Director revision:** `17963cad6dee8a43e4999a5bd0751e9250a8c660`  
**Research revision:** `c218f0d119db822b875dddb421f00642ffbbe8f1`  
**Status:** research only; no provider calls, online experiment, routing change, deployment, or spend

## Question

What evidence does current AXIOM Director telemetry actually expose for evaluating static minimum-capable and validator-triggered escalation baselines, and what smallest evidence gap must close before any adaptive-routing trial is justified?

## Executive conclusion

AXIOM cannot yet run the accepted routing headroom study from durable repository evidence.

The control policy is implemented: `select_channel` deterministically filters ineligible channels and selects the minimum-capable eligible channel by background fit, incremental cost, capability surplus, trust rank, and stable channel ID. An adaptive selector and a SQLite telemetry store also exist. However, current telemetry is not wired into a durable production path inside the repository, does not record time or route revision, treats receipt status `SUCCEEDED` as acceptance, drops the receipt's validation evidence, and cannot link first attempts to validator-triggered escalations.

Therefore:

- **B0 static minimum-capable:** implementation exists, but durable outcome evidence is insufficient for performance evaluation.
- **B2 validator-triggered escalation:** cannot be reconstructed because trigger, attempt, and transaction-link evidence are absent.
- **B4 paired oracle/headroom bound:** cannot be computed because alternative-route outcomes are not recorded as paired observations.
- **Adaptive routing:** remains unjustified.
- **Current decision:** `INSUFFICIENT_EVIDENCE`, not rejection of all future adaptation.

The smallest useful next change is an additive, nullable telemetry schema extension plus production wiring that records transaction time, task/risk stratum, route revision, independent validation identity, and attempt/escalation linkage. It must not change route selection. Only after a zero-cost instrumentation window produces traceable comparable records should AXIOM run the offline B0/B2/B4 study.

## Scope and method

This is a current-code audit, not an empirical model comparison. Evidence was read from the exact Director revision above and checked against the accepted contracts:

- [Validated-work efficiency metric design](https://github.com/axiom-llc/axiom-research/blob/c218f0d119db822b875dddb421f00642ffbbe8f1/2026-10-05-validated-work-efficiency-metrics-chatgpt.md)
- [Simple routing baselines under sparse evidence](https://github.com/axiom-llc/axiom-research/blob/c218f0d119db822b875dddb421f00642ffbbe8f1/2026-10-06-simple-routing-baselines-sparse-evidence-chatgpt.md)

Current primary repository sources:

- [execution_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_runtime.py)
- [execution_telemetry.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/execution_telemetry.py)
- [telemetry_store.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/modules/telemetry_store.py)
- [portable_runtime.py](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/portable_runtime.py)
- [execution telemetry tests](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/tests/test_execution_telemetry.py)
- [telemetry store tests](https://github.com/axiom-llc/axiom-director/blob/17963cad6dee8a43e4999a5bd0751e9250a8c660/tests/test_telemetry_store.py)

Repository code search at the bound revision found:

- `MetricBuffer` only in its defining module and its tests;
- `TelemetryStore` only in its defining module and its tests;
- `adaptive_select_channel` in its defining module, tests, and the portable request interface.

This establishes absence of in-repository production wiring at the audited revision. It does not claim that no external or uncommitted runtime holds data.

## Current routing behavior

### Static control exists

`select_channel` first excludes every channel with capability, registration, eligibility, exposure, authorization, health, or cost blockers. It then deterministically minimizes:

1. background mismatch;
2. declared incremental cost;
3. capability surplus;
4. trust rank;
5. channel ID.

This is a concrete B0 implementation and preserves authority/capability gates before efficiency.

### Adaptive selector exists but is not evidence of deployment

`adaptive_select_channel` uses the same blocker filter, then scores channel summaries with a weighted penalty over acceptance, cost, latency, tokens, interventions, and retries. `portable_runtime.py` accepts caller-supplied metrics and returns a selected channel.

The repository evidence does not establish that this selector is connected to live routing or that its input metrics are durable, representative, or independently validated. It must be treated as an available mechanism, not a validated policy.

### Dispatch is single-shot

`dispatch_task` probes channels, selects one, dispatches once, validates task/effect binding, invokes an optional observer, and returns. It does not implement a validator-triggered escalation cascade or link multiple attempts into one logical transaction.

## Current telemetry contract

`ExecutionMetric` and schema version 2 persist:

| Field | Present | Routing-study use |
|---|---:|---|
| `task_digest` | yes | Immutable task-envelope binding, but not a human-readable task/risk stratum. |
| `channel_id` | yes | Route identity, but not provider/model/tool-policy revision. |
| `status` | yes | Receipt status; not independent validation. |
| `accepted` | yes | Set to `status == "SUCCEEDED"`; claimed success only. |
| `latency_ms` | yes | Dispatch wall latency for one selected attempt. |
| `incremental_cost_microusd` | yes | Maximum of receipt/channel declarations. |
| `input_tokens`, `output_tokens` | yes | Provider-reported totals; unavailable and zero are conflated. |
| `reported_token_classes` | yes | Provider-neutral token subclasses when reported. |
| `operator_interventions` | yes | Count only; no active-time evidence. |
| `retries` | yes | Aggregate count; retry attempts are not addressable. |
| auto-increment `sequence` | store only | Stable insertion order, not a timestamp. |

The store supports all-record or channel-filtered reads ordered by ascending sequence. A positive `limit` returns the earliest matching rows, not an explicitly defined recent window.

## Coverage matrix against accepted contracts

| Required evidence | State | Consequence |
|---|---|---|
| Stable logical transaction ID | partial | `task_digest` binds an envelope but cannot link distinct attempts/validators as one transaction. |
| Observation timestamp | missing | No chronological holdout, drift window, or wall-clock data cut. |
| Task class | missing | Cannot stratify heterogeneous work. |
| Risk class | missing | Cannot apply risk-specific non-inferiority margins. |
| Route revision | missing | Silent model/provider/tool-policy drift contaminates history. |
| Route decision kind | missing | Cannot distinguish B0, B1, B2, or adaptive decisions. |
| Attempt index and parent transaction | missing | Cannot reconstruct cascades or retry-inclusive paired outcomes. |
| Escalation trigger | missing | B2 cannot be evaluated or diagnosed. |
| Independent validation status | missing | `accepted` is receipt-derived claimed success. |
| Validator kind/evidence reference | missing | Outcomes are not addressable or independently auditable. |
| Receipt `validation` tuple | available upstream, dropped | Potential evidence names exist on `ExecutionReceipt` but are not copied into `ExecutionMetric`. |
| Failure class | missing | Failures cannot be separated by capability, provider, validation, permission, or integrity cause. |
| Tool calls/duration | missing | Tool overhead is uncharged. |
| Verification calls/cost | missing | Validation overhead and yield cannot be measured. |
| Human active time | missing | Intervention count cannot distinguish seconds from hours. |
| Usage availability | missing | Default zero can mean either zero or unavailable. |
| Logging propensity/action support | missing | Unbiased off-policy estimators are unavailable. |
| Alternative-route paired outcome | missing | B4 oracle headroom cannot be computed. |
| Durable production append path | not found in repository | Existing store and buffer do not establish collected data. |

## Headroom feasibility decision

### B0

The policy can be inspected and tested as code. Its historical validated completion, total cost, and drift stability cannot be measured from the current repository evidence.

### B2

Not feasible to score. A valid B2 record needs at least:

- logical transaction ID;
- attempt index;
- selected route and route revision;
- named escalation trigger;
- validator result/evidence reference;
- all attempt costs;
- final independently validated outcome.

Current aggregate `retries` cannot substitute for these fields.

### B4

Not feasible to score. The post-hoc oracle requires actual outcomes from more than one eligible route on the same frozen task input. No paired-output contract or addressable alternative-result reference exists in current telemetry.

### Adaptive challenger

No promotion test is possible. Current weighted penalties may rank supplied metrics, but ranking code is not evidence that an adaptive policy beats B0 or B2. Running it on sparse, non-versioned, receipt-derived success data would manufacture confidence.

## Minimal additive evidence contract

Preserve current fields and add nullable fields in a new schema version. Null must mean unavailable; zero must remain a measured zero.

### Identity and time

- `transaction_id`: stable logical execution identity.
- `observed_at`: UTC event timestamp.
- `task_class`: coarse, versioned pre-outcome stratum.
- `risk_class`: policy-defined consequence/validation stratum.
- `route_revision`: digest or stable provider/model/effort/tool-policy identity.

### Decision and attempt linkage

- `decision_kind`: `STATIC_MINIMUM`, `STATIC_CLASS`, `VALIDATOR_ESCALATION`, `STATIC_STRONG`, or named experimental policy.
- `attempt_index`: zero-based position within the logical transaction.
- `parent_attempt_id` or stable attempt identity.
- `escalation_trigger`: null for initial attempts; otherwise a bounded named runtime/validator condition.

### Validation

- `validation_status`: `PASSED`, `FAILED`, `NOT_REQUIRED`, or `UNKNOWN`.
- `validator_kind`: named independent validation class.
- `validation_evidence_ref`: addressable durable evidence.
- `failure_class`: bounded failure taxonomy.

The receipt's existing `validation` tuple may be preserved as claimed validation metadata, but it must not be promoted to independent validation merely because the provider reported it.

### Resource availability

Add availability flags or nullable values for cost and token fields so missing is not recorded as zero. Add tool calls/duration, verification calls, and operator active time only when their evidence source is defined. Do not infer human time from wall latency.

## Smallest implementation candidate

**Owner:** `axiom-llc/axiom-director`  
**Candidate:** additive telemetry schema v3 and observer wiring only  
**Behavioral constraint:** route selection remains unchanged

Bound the candidate to:

1. add nullable identity/time/decision/validation/attempt fields to `ExecutionMetric`;
2. migrate schema v2 to v3 without rewriting existing rows;
3. copy only actually available envelope, channel, receipt, and independent-validator fields;
4. wire one authorized runtime composition root to append through `TelemetryStore`;
5. add migration, round-trip, missing-versus-zero, and no-routing-change tests.

Do not add an adaptive policy, change weights, enable online experimentation, or treat self-reported validation as authoritative.

This candidate is implementation-ready only after the owning composition root and independent validation callback are identified. The current repository proves the storage owner and test locations, but not the canonical runtime data location or independent-validator evidence source. Therefore this run should not fabricate implementation wiring.

## Zero-cost remote MVE

### Phase 1 — Wiring proof

Using repository-native tests only:

1. migrate an in-memory schema v2 store to v3;
2. append one initial attempt and one validator-triggered escalation sharing a transaction ID;
3. preserve missing usage as null and measured zero as zero;
4. round-trip route revision and validation evidence identity;
5. prove `select_channel` returns the same result before and after the telemetry-only change.

### Phase 2 — Instrumentation window

After separate implementation authorization and integration:

1. leave production routing on B0;
2. collect every naturally occurring eligible transaction without new provider calls;
3. require addressable validation evidence where policy requires validation;
4. record route revisions and all actual attempts;
5. stop at the first revision boundary and publish raw counts, missingness, and exclusions.

No fixed transaction count is asserted. Collection continues until the predeclared outcome and cost margins are testable or a drift boundary forces a new block.

### Phase 3 — Coverage decision

- If no paired alternative-route outcomes exist, B4 remains unavailable.
- If no validator-triggered escalations occur, B2 outcome evidence remains unavailable.
- If validation evidence is missing, validated-completion analysis stops.
- If route revision or time is missing, chronological analysis stops.
- If coverage is adequate, freeze B0/B2/B4 definitions and margins before scoring.

## Promotion criteria

Telemetry may advance from schema candidate to instrumentation-only PR when:

1. migration preserves every schema v2 row;
2. missing and measured zero remain distinguishable;
3. timestamps, transaction IDs, and route revisions round-trip;
4. attempt/escalation linkage is deterministic and validated;
5. independent validation remains distinct from receipt claims;
6. current routing-selection tests remain unchanged and pass;
7. no provider call, online route change, spend, workflow, authority, or permission mutation is introduced.

An adaptive-routing experiment remains blocked until:

1. B0 and B2 can be scored on traceable recent data;
2. action support or direct paired observations exist;
3. B4 shows enough attainable headroom to pay routing overhead;
4. outcome non-inferiority and worthwhile-cost margins are predeclared;
5. two non-overlapping chronological blocks clear the accepted gates.

## Rejection criteria

Reject or narrow the telemetry candidate if:

- the canonical runtime composition root cannot be identified;
- an independent validator cannot emit addressable evidence;
- new fields are populated with guesses, inferred timestamps, or fabricated revisions;
- migration rewrites or reinterprets historical rows;
- self-reported receipt validation is mislabeled independent;
- instrumentation changes route choice or introduces provider calls;
- collection cannot distinguish missing from zero;
- the resulting data still cannot reconstruct B0/B2 attempts.

Reject adaptive routing if the instrumentation window cannot establish supported comparable outcomes or if B4 headroom does not exceed full router overhead.

## Falsifiable findings

- **F1:** Repository code search will continue to find no production `TelemetryStore` caller until explicit observer wiring is added.
- **F2:** At least one naturally occurring transaction will contain unavailable usage that current schema would encode as zero.
- **F3:** Current receipt-derived `accepted` will disagree with independently validated outcome for at least one transaction.
- **F4:** Without explicit attempt linkage, at least one retry or escalation will be impossible to reconstruct from aggregate `retries`.
- **F5:** A route-revision boundary will materially reduce the usable chronological sample.
- **F6:** B4 headroom will remain unavailable until the system records paired actual outcomes.

These are **UNVALIDATED_HYPOTHESES** until the bounded instrumentation evidence exists.

## Manager classification

**ACCEPT_WITH_FOLLOWUP.**

Current code supports a minimum-capable control and telemetry primitives, but not a defensible offline routing comparison. Preserve B0, do not deploy adaptive routing, and authorize only the smallest additive instrumentation candidate after its composition root and independent validation evidence source are identified.
