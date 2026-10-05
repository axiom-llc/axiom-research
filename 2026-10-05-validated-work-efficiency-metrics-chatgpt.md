# Validated-Work Efficiency Metric Design

**Queue item:** RQ-2026-10-03-003  
**Date:** 2026-10-05  
**Target:** axiom-llc/axiom-research  
**Status:** research only; no routing behavior change

## Question

Which minimal telemetry schema and derived metrics best estimate validated useful work per unit of model, tool, latency, and human-attention cost without Goodharting on token minimization?

## Executive conclusion

AXIOM should not optimize a single “validated-work efficiency” scalar. The smallest defensible design is:

1. retain the current transaction resource fields;
2. bind them to an independently verified outcome and a stable task/route identity;
3. add only the missing time, tool, validation, failure-detection, and human-active-time evidence;
4. compare routes with a vector of outcome-first ratios on chronological holdouts;
5. keep static minimum-capable routing as the control until another policy improves at least one resource dimension without materially degrading validated completion, safety gates, or operator burden.

The present Director telemetry already records most machine-cost inputs: task digest, channel, receipt status, acceptance, latency, incremental cost, input/output tokens, token classes, operator interventions, and retries. It is not yet sufficient for routing research because it lacks an event timestamp, task/route revision class, explicit independent validation evidence, tool-call cost, human active time, failure class, and root-to-detection latency.

No implementation or routing change is justified by this research alone.

## Evidence

### Provider-neutral operation accounting

OpenTelemetry’s GenAI semantic conventions model a logical operation as a span covering the entire operation, including automatic retries. They define provider/model/operation identity, token usage, operation duration, agent/workflow duration, inference-call count, tool-call count, and tool duration. Token counts should be reported only when available; where both used and billable counts exist, the conventions prefer billable counts. The conventions are still marked **Development**, so AXIOM should borrow field meaning rather than freeze its schema to unstable names.

- https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md
- https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-metrics.md

OpenAI’s Agents SDK aggregates request count, input/output/total tokens, cached input tokens, cache-write tokens, reasoning tokens, and per-request usage. Its documentation warns that third-party adapter usage reporting varies by backend and must be validated on the exact provider path. Therefore “missing” and “zero” must remain distinct.

- https://openai.github.io/openai-agents-python/usage/

### Outcome and human-attention emphasis

Google SRE monitoring guidance separates internal metrics from externally visible behavior and argues that alerts should be actionable and directed to humans only when human action is required. This supports treating operator interruption as a first-class cost rather than hiding it inside generic latency.

- https://sre.google/sre-book/monitoring-distributed-systems/

NIST’s AI RMF Playbook treats measurement, testing, evaluation, verification, and validation as context-dependent practices rather than one universal checklist. This supports binding validation method and evidence to each result rather than treating a model’s self-report as validated completion.

- https://airc.nist.gov/airmf-resources/playbook/

### Metric gaming

Manheim and Garrabrant distinguish regressional, extremal, causal, and adversarial Goodhart effects. Any single aggregate score invites selection on noise, out-of-distribution behavior, intervention-induced changes, or deliberate metric manipulation. A resource vector with independent outcome gates is harder to game and easier to audit.

- https://arxiv.org/abs/1803.04585

## Existing AXIOM baseline

At Director revision `98a2fc209e90da4405f9ceda90116c94bf193eaf`, `ExecutionMetric` already records:

- `task_digest`
- `channel_id`
- `status`
- `accepted`
- `latency_ms`
- `incremental_cost_microusd`
- `input_tokens`
- `output_tokens`
- `reported_token_classes`
- `operator_interventions`
- `retries`

The current `accepted` bit is receipt-derived: `status == "SUCCEEDED"`. It is useful execution evidence but is not necessarily an independently validated outcome. Current routing also combines failure, cost, latency, token, intervention, and retry terms into a weighted penalty. That mechanism is deterministic, but its weights are policy choices rather than evidence that one scalar represents useful work.

The existing research artifact `2026-10-03-agent-compute-routing-chatgpt.md` already establishes the controlling principle: validated useful work is the target, static minimum-capable routing remains the baseline, and adaptive routing must beat that baseline after overhead.

## Minimal telemetry schema

Use one append-only record per logical transaction. Preserve missing values as `null`; never coerce unavailable usage to zero.

### Required identity and timing

| Field | Type | Purpose |
|---|---:|---|
| `transaction_id` | string | Stable idempotency/evidence identity for one logical task execution. |
| `task_digest` | string | Existing immutable task binding. |
| `task_class` | string | Coarse, versioned comparison stratum; prevents unrelated work from being averaged together. |
| `risk_class` | string | Binds applicable authority and validation requirements. |
| `channel_id` | string | Existing route identity. |
| `route_revision` | string | Model/provider/effort/tool-policy revision or digest; prevents silent route drift. |
| `started_at` | timestamp | Enables chronological holdout and drift analysis. |
| `latency_ms` | integer | Existing end-to-end logical-operation latency, including retries. |

### Required outcome and validation

| Field | Type | Purpose |
|---|---:|---|
| `receipt_status` | enum | Existing execution result. |
| `claimed_success` | boolean | Existing receipt-level claim, renamed conceptually from `accepted`. |
| `validation_status` | enum | `PASSED`, `FAILED`, `NOT_REQUIRED`, or `UNKNOWN`. |
| `validator_kind` | string | Read-back, schema/static check, executable test, external status, independent review, or other named validator. |
| `validation_evidence_ref` | string/null | Addressable evidence identity; no evidence means no validated-success claim. |
| `validated_success` | boolean/null | True only when required validation passed; null when not established. |
| `failure_class` | string/null | Transient, deterministic, semantic, permission, integrity, ambiguous-effect, validation, or other bounded class. |
| `root_to_detection_ms` | integer/null | Time from root failure/effect start to detection when observable. |

### Required resource vector

| Field | Type | Purpose |
|---|---:|---|
| `incremental_cost_microusd` | integer/null | Existing direct incremental hosted cost. |
| `input_tokens` | integer/null | Existing provider-reported/billable input tokens. |
| `output_tokens` | integer/null | Existing provider-reported/billable output tokens. |
| `reported_token_classes` | object | Existing cached/reasoning/other token detail when available. |
| `model_requests` | integer/null | Logical provider requests; distinguishes long single calls from retry/cascade behavior. |
| `tool_calls` | integer/null | Total tool invocations. |
| `tool_duration_ms` | integer/null | Aggregate tool time where measured. |
| `retries` | integer | Existing retries within the logical transaction. |
| `operator_interventions` | integer | Existing interruption/event count. |
| `operator_active_ms` | integer/null | Actual human work time when observable; do not infer from wall time. |
| `verification_calls` | integer | Cost surface for validators. |

### Optional audit detail

Per-attempt child records may retain request/model/tool spans when available. They are not required for the minimal transaction table. The transaction record is the comparison unit; attempt detail explains anomalies and retry amplification.

## Derived metric vector

All denominators must be explicit. Report numerator, denominator, sample size, missingness, and time window beside every ratio.

### 1. Validated completion rate

[
VCR = rac{N(	ext{validated_success = true})}{N(	ext{eligible transactions with known validation outcome})}
]

This is the primary outcome gate. Claimed success without required validation does not count.

### 2. Claimed-versus-verified gap

[
CVG = rac{N(	ext{claimed_success = true and validated_success != true})}{N(	ext{claimed_success = true})}
]

This detects optimistic receipts and missing verification.

### 3. Resource cost per validated success

Keep these as separate coordinates, not one weighted sum:

- input tokens / validated successes
- output tokens / validated successes
- model requests / validated successes
- tool calls / validated successes
- incremental microusd / validated successes
- latency ms / validated successes
- operator interventions / validated successes
- operator active ms / validated successes

A route is preferable only in the task/risk strata where it remains on the validated Pareto frontier.

### 4. Retry amplification

[
RA_{attempts} = rac{N(	ext{initial attempts + retries})}{N(	ext{logical transactions})}
]

Also report incremental cost, tokens, tool calls, latency, and human attention attributable to retries. A retry can rescue an outcome; it is not automatically waste.

### 5. Verification yield

Report separately:

- real failures detected / verification calls
- final outcomes rescued after verifier-triggered revision / verification calls
- accepted unchanged / verification calls
- known false accepts and false rejects where later ground truth exists
- verifier resource overhead

Do not collapse these into one value until the costs of false acceptance and rejection are fixed for a risk class.

### 6. Failure-detection latency

Report distribution of `root_to_detection_ms` by failure class and validator. Use median and quantiles only when sample size is shown; preserve censored/unknown observations.

### 7. Human-attention cost

Report both interruption count and active time. One five-second confirmation and one hour of repair are not equivalent. If active time is unavailable, retain the event count and mark time unknown.

## Failure modes and Goodhart controls

| Failure mode | Control |
|---|---|
| Token minimization rewards under-computation | Validated completion is a hard gate; tokens remain one cost coordinate. |
| Easy tasks inflate route efficiency | Compare only within versioned task/risk strata. |
| Receipt success is treated as ground truth | Require validator kind, status, and evidence reference. |
| Missing provider usage appears free | Preserve `null`; exclude or bound missing-cost comparisons. |
| Retries are hidden as separate tasks | One logical transaction owns every attempt. |
| Validator overhead is ignored | Count validation calls and their tokens/tool/latency cost. |
| Human repair is hidden | Record intervention count and active time separately. |
| Route/model drift contaminates history | Bind route revision and use chronological splits. |
| A weighted score encodes arbitrary priorities | Keep a vector; weights require explicit external policy. |
| Optimizing the benchmark overfits it | Freeze the evaluation window and promotion rule before candidate scoring. |
| Safety/authority failures look efficient because they stop early | Risk/authority gates precede efficiency comparison; blocked work is never a success. |

## Historical-analysis plan

1. Export existing Director telemetry without changing routing.
2. Join each transaction to current or recoverable validation receipts using stable task/action identity.
3. Exclude from comparative claims any record lacking task class, route revision, or required validation outcome; report the exclusion count.
4. Preserve provider-reported usage exactly. Do not impute unavailable tokens or monetary cost.
5. Group by versioned task class and risk class.
6. Order by `started_at`; use earlier records to define baselines and later records only for evaluation.
7. Report static minimum-capable routing, strong-only routing where observed, and any naturally occurring escalation/cascade path as separate cohorts.
8. Compare VCR and the resource vector. Do not infer counterfactual route performance from tasks observed on only one route.
9. Inspect failures individually for classification, retry effects, validation yield, and human repair.
10. Publish a descriptive receipt with raw counts, exclusions, missingness, and uncertainty before proposing any routing change.

Because routing is observational, route choice and task difficulty are confounded. Historical data can establish logging quality, obvious dominated paths, and hypotheses. It cannot by itself prove that another route would have succeeded on the same task.

## Zero-cost remote MVE

Run a **20-transaction instrumentation MVE**, not a 20-transaction routing trial.

- Use only already-authorized ChatGPT session-hosted execution and GitHub Actions/remote evidence.
- Leave routing unchanged.
- Record the minimal schema for the next 20 naturally occurring eligible transactions.
- Require addressable validation evidence for every transaction whose risk class requires validation.
- At transaction 20, audit schema completeness, null/missing usage, task-class balance, claimed-versus-verified gap, retry amplification, validation yield, human attention, and route-revision drift.
- Produce chronological descriptive tables and a Pareto plot/table; no learned router and no online policy change.
- If records are too heterogeneous for within-stratum comparison, keep collecting; do not manufacture a pooled efficiency score.

Twenty transactions are sufficient to test instrumentation and expose missing fields. They are not asserted to be sufficient for a routing decision.

## Promotion gates for any later routing experiment

A routing candidate may advance only when all are true:

1. **Authority invariant:** privacy, capability, permission, consequence, reversibility, and validation gates are unchanged and evaluated before cost optimization.
2. **Evidence completeness:** every included outcome has the required independent validation evidence; missing resource data is disclosed and cannot make a route appear cheaper.
3. **Comparable scope:** evaluation uses predeclared task/risk strata and route revisions.
4. **Chronological holdout:** policy and thresholds are frozen on earlier data and evaluated on later data.
5. **Outcome non-inferiority:** the candidate does not exceed a predeclared risk-class-specific loss margin for validated completion or serious failure. The margin must be set by the owner/policy, not learned from the test.
6. **Resource improvement:** after model, tool, verification, retry, latency, and human-attention overhead, the candidate improves at least one resource dimension without unacceptable regression in the others.
7. **Simple-baseline test:** it beats static minimum-capable routing and any simpler cascade under the same evidence.
8. **Drift control:** results remain stable across model/provider revisions or the candidate fails closed to the static baseline.
9. **Diagnosability:** route decisions and failures remain attributable to explicit fields.
10. **Reversibility:** rollout begins in shadow/offline mode and can be disabled without canonical-state ambiguity.

If any gate fails, retain static minimum-capable routing.

## Falsifiable hypotheses

- H1: adding explicit validation identity will reveal a nonzero claimed-versus-verified gap hidden by receipt-derived acceptance.
- H2: retry-inclusive cost per validated success will reorder at least one channel comparison relative to token-only cost.
- H3: task/risk stratification will explain more route variance than raw token count.
- H4: operator active time and interruption count will identify different high-burden transactions.
- H5: a single weighted efficiency score will produce route rankings that change materially under plausible policy weights, while the Pareto frontier remains stable.
- H6: current data volume is insufficient for a learned router to beat the static baseline with defensible chronological evidence.

Each hypothesis is rejected if the specified signal is absent in complete comparable data; no routing change follows automatically from acceptance.

## Rejection criteria

Reject the telemetry expansion if the added fields cannot be captured from existing receipts/validation evidence without material operator work, or if they do not change a concrete analysis, stop, retry, verify, or routing decision.

Reject adaptive routing if it fails any promotion gate; if comparative strata remain sparse; if missing data drives the apparent gain; if high-consequence failures concentrate in the candidate route; or if maintenance/calibration cost exceeds observed savings.

## Decision

**ACCEPT_WITH_FOLLOWUP.** Add no router and change no production policy. First prove the minimal transaction/validation join and complete the 20-transaction instrumentation MVE. The likely smallest future implementation is an additive, nullable telemetry schema extension plus an offline report; that candidate still requires separate Director authorization and repository-native tests.
