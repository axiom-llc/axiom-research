# Machine-speed anomaly halt policy

- Queue item: `RQ-2026-10-04-013`
- Research date: 2026-10-05
- Target: `chatgpt`
- Scope: low-complexity, offline-validated anomaly controls for agent network and tool activity
- Manager classification: `ACCEPT_WITH_FOLLOWUP`

## Executive decision

Adopt a **small deterministic guard-and-tripwire state machine**, not a machine-learning anomaly detector.

The baseline has two deliberately separate layers:

1. **Preventive invariants** block an individual unsafe effect before it occurs. They cover authorization drift, forbidden destinations, and sensitive-read-to-egress sequences.
2. **Behavioral tripwires** use low-cardinality counters and short/long event windows to detect abnormal volume, repeated denials, excessive tool chaining, and destination novelty. Tripwires first reduce the lane to read-only; a further anomaly or forbidden effect attempt halts the invocation.

The policy should use existing trace/tool receipts, declared authority, destination classifications, and queue/workflow budgets. It should not inspect raw prompt or tool-result bodies by default. A single unfamiliar destination is not enough to halt a benign read-only workflow; novelty becomes a stop condition only when joined to a sensitive lineage, an elevated effect, an authorization mismatch, or a sustained rate/denial pattern.

All numeric limits remain **configuration under test**. This artifact defines how to derive and validate them; it does not invent production thresholds.

## Research question

Which low-complexity telemetry signals and stopping rules can detect and halt abnormal agent network/tool behavior at machine speed without excessive false shutdowns?

## Evidence boundary

### Current external evidence

1. OpenTelemetry's current GenAI semantic conventions define an `execute_tool` span with tool name, agent identity when applicable, conversation/call identifiers, tool type, and low-cardinality error type. The conventions also define per-invocation tool-call counts and tool duration. This is enough to express a provider-neutral tool-event spine without recording sensitive arguments or results. The conventions are still marked **Development**, so AXIOM should map them at an adapter boundary rather than freeze its durable schema to every field name.
2. OpenTelemetry explicitly warns that tool arguments/results and model content can contain sensitive information and should not be captured by default. The anomaly baseline therefore uses classifications, hashes, counts, and reason codes rather than raw content.
3. The MCP security guidance identifies token audience validation, exact redirect validation, private/link-local destination blocking, redirect revalidation, DNS rebinding/TOCTOU risk, and least-privilege scope changes as security boundaries. Those conditions are better treated as deterministic preventive invariants than statistical anomalies.
4. Google's SRE alerting guidance evaluates alert rules by precision, recall, detection time, and reset time. It shows why one short threshold window is noisy, one long window resets poorly, and a simple multi-window rule improves the trade-off. AXIOM can reuse the principle with event windows rather than importing the example service thresholds.
5. NIST SP 800-137 treats continuous monitoring as a program that maintains ongoing awareness of security state to support risk decisions. It supports measuring control-relevant state continuously, but it does not prescribe AXIOM-specific halt thresholds.
6. NIST SP 800-53 Rev. 5 (current patch release noted by NIST as 5.2.0 on 2025-08-27) provides the durable control vocabulary around event logging, continuous monitoring, incident handling, and system monitoring. It is a governance reference, not evidence that a particular numeric detector is effective.

### Prior AXIOM evidence reused

- `RQ-2026-10-04-008` concluded that a compact sensitive-source/effect sequence rule can block material read-to-network paths without general-purpose taint tracking.
- `RQ-2026-10-04-012` concluded that schema digests need tool identity/version/endpoint binding for high-risk remote tools.

This artifact composes those controls into a halt policy. It does not reopen their implementation decisions.

### Synthesis and unvalidated claims

The state machine, signal combinations, threshold-selection method, and promotion gates below are **AXIOM synthesis**. They remain unvalidated until the offline replay passes. Any claim that they reduce incidents or false shutdowns is an `UNVALIDATED_HYPOTHESIS`.

## Minimal event contract

Emit one normalized event at each authorization decision, tool start, tool end, network-resolution decision, redirect hop, and lane-state transition.

| Field | Purpose | Cardinality / privacy rule |
|---|---|---|
| `event_id`, `trace_id`, `invocation_id` | Deduplicate and reconstruct order | Opaque IDs; do not derive from content |
| `seq` | Total order within an invocation | Monotonic integer |
| `observed_at` | Diagnose delays | UTC timestamp; event order remains authoritative |
| `agent_id`, `workflow_id` | Attribute activity | Stable internal identifiers |
| `tool_id`, `tool_version_digest` | Bind behavior to approved implementation | Low-cardinality ID plus digest |
| `operation_class` | `READ`, `WRITE`, `EXECUTE`, `NETWORK`, `AUTH_CHANGE` | Required enum |
| `effect_risk` | `LOW`, `ELEVATED`, `HIGH` | Derived from policy, not model text |
| `decision`, `reason_code` | `ALLOW`, `DENY`, `ERROR` | Stable low-cardinality codes |
| `destination_class` | approved external, new external, private, link-local, loopback, metadata, unresolved | Store normalized class; hostname may be separately access-controlled |
| `destination_id` | Compare destination novelty | Canonical destination key or keyed hash |
| `auth_snapshot_digest` | Detect scope/audience/authority drift | Compare to approved receipt |
| `data_lineage_class` | public, internal, sensitive, credential-like, unknown | Carry compact lineage from existing policy |
| `attempt_id`, `parent_event_id` | Join retries and tool chains | Prevent retry inflation |
| `lane_state` | `NORMAL`, `DEGRADED_READ_ONLY`, `HALTED` | Recorded before and after transitions |

Do not require raw prompts, tool arguments, returned content, secrets, or authorization tokens. Where a destination hostname must be retained for enforcement, keep it in the enforcement receipt with existing access controls; the detector may consume only its canonical classification and keyed identifier.

## Signals

### Hard preventive invariants

These are not anomaly scores. A match blocks the pending effect and transitions directly to `HALTED`.

| ID | Signal | Deterministic predicate | Required evidence |
|---|---|---|---|
| `H-AUTH-DRIFT` | Authorization or identity drift | observed tool/version/endpoint, token audience, granted scope, or authority digest differs from the approved receipt for a high-risk call | approval receipt + observed binding |
| `H-FORBIDDEN-DEST` | Forbidden network destination | destination is private, link-local, metadata, disallowed loopback, non-HTTPS in production, or a redirect/DNS result leaves the approved set | resolution and redirect-hop receipts |
| `H-SENSITIVE-EGRESS` | Sensitive read-to-egress sequence | `SENSITIVE`, `CREDENTIAL_LIKE`, or `UNKNOWN` lineage reaches an unapproved network effect in the same invocation/trace | lineage class + ordered tool/network events |
| `H-TELEMETRY-GAP` | Missing enforcement evidence | a high-risk effect lacks the minimum authority, destination, lineage, or decision fields | completeness check before effect |
| `H-HALT-BYPASS` | Action attempted while halted | any effectful operation begins after `HALTED` | lane state + ordered event |

A hard rule must run at the enforcement point. Detecting it asynchronously after the effect is monitoring, not prevention.

### Soft behavioral tripwires

Soft signals are deliberately simple and independently explainable.

| ID | Signal | Computation | Why it is not sufficient alone |
|---|---|---|---|
| `S-DEST-NOVELTY` | First-seen destination for workflow/tool scope | membership lookup against an approved/observed destination set | new destinations are normal in discovery and browsing |
| `S-RATE` | Tool/effect volume over declared budget | token bucket or count per event window, keyed by agent + operation class | bursts can be legitimate |
| `S-DENY-LOOP` | Repeated denied intent | count unique attempts sharing normalized tool + reason + destination/effect class; collapse retries by `attempt_id` | one deny proves prevention worked, not compromise |
| `S-CHAIN-DEPTH` | Excessive tool chain | tool-call count and maximum ordered chain depth per invocation | complex but valid tasks may be deep |
| `S-ERROR-RATIO` | Failed/denied operations | bad events divided by total attempts, with a minimum event count | small samples are unstable |
| `S-AUTH-CHURN` | Repeated elevation requests | count scope/authority elevation attempts and granted/denied outcomes | an explicit user-directed workflow may elevate once |
| `S-RETRY-VARIANTS` | Policy probing | denied operation followed by argument/destination variants with the same effect class | recovery logic may legitimately vary parameters |

### Windowing

Use two event-count windows per invocation or workflow scope:

- **Fast window:** detects a burst before many tool boundaries pass.
- **Slow window:** detects sustained or low-and-slow behavior across more events.

Event-count windows avoid depending on scheduler latency, but wall-clock timestamps remain necessary for diagnosing replay and stuck invocations. The specific window sizes are replay parameters, not fixed here.

## Stopping state machine

### States

- `NORMAL`: declared operations proceed through ordinary authorization.
- `DEGRADED_READ_ONLY`: deny `WRITE`, `EXECUTE`, `NETWORK`, and `AUTH_CHANGE`; allow only explicitly safe local/read operations needed to preserve evidence or explain the stop.
- `HALTED`: no new tool or network effects. Preserve receipts and require an independently authorized recovery decision.
- `RECOVERY_PENDING`: optional administrative label outside the executing agent; never lets the same invocation self-resume.

### Transitions

1. Any hard invariant match: block the pending effect, write an atomic halt receipt, transition `NORMAL|DEGRADED -> HALTED`.
2. Two **independent** soft-signal families in the fast window: transition `NORMAL -> DEGRADED_READ_ONLY`.
3. One soft signal exceeding both fast and slow window thresholds: transition `NORMAL -> DEGRADED_READ_ONLY`.
4. While degraded, any additional soft-signal family, repeated denied effect, or requested elevated effect: transition `DEGRADED_READ_ONLY -> HALTED`.
5. Clean completion ends the invocation. A quiet interval does not auto-resume a halted invocation.
6. Only a separate recovery authority may start a new invocation after reviewing the halt receipt; the stopped agent cannot clear its own state.

This requires corroboration for soft anomalies while keeping deterministic hazards immediate.

## Threshold selection without unsupported precision

Define a small configuration vector:

- `B[operation_class]`: declared token-bucket capacity and refill for each effect class.
- `D`: repeated-denial attempts after retry collapsing.
- `C`: tool-call/chain-depth limit derived from the workflow plan or explicit step budget.
- `F`, `S`: fast and slow event-window sizes.
- `R`: bad-event ratio plus minimum denominator.
- `E`: authority-elevation attempt budget.

Choose values in this order:

1. Start from **declared operational budgets** where they exist. A workflow that says it may perform at most eight external reads should not be granted a learned budget of fifty.
2. For missing budgets, build a small candidate grid from observed benign traces. Do not use maxima alone; inspect the workflows that define the upper tail.
3. Run the grid on development replay data and remove dominated configurations.
4. Freeze the remaining configurations.
5. Evaluate once on a chronological holdout set that includes newly added adversarial traces.
6. Select the lowest-complexity configuration that satisfies every absolute safety gate and the predeclared benign-shutdown budget.
7. If no configuration satisfies both, reject the baseline or narrow its scope. Do not add ML merely to improve a dashboard score.

## False-positive analysis

| Benign case | Likely signal | Mitigation |
|---|---|---|
| First access to a legitimate research source | destination novelty | novelty alone does not stop a read-only call; use approved destination class or corroboration |
| Batch validation or repository enumeration | rate, chain depth | budget by operation class and workflow plan; count pages/continuations as declared work |
| Transient provider failure with retries | error ratio, retry variants | collapse retries under one `attempt_id`; distinguish transport errors from policy denials |
| User-approved privilege elevation | auth churn | compare to a signed/recorded approval; one matching elevation is not drift |
| Exploratory tool use | tool-call count | use per-invocation declared step budget and degrade before halt |
| A legitimately changed tool version | auth drift | fail closed until a new approval receipt exists; this is intentional friction, not a false positive |
| A redirecting public endpoint | destination novelty | validate every hop; approved redirect target can proceed, private/reserved target cannot |
| Long-running low-rate workflow | slow-window signal | scope windows by workflow phase and reset only at validated phase boundaries |

False shutdown rate must be reported by workflow and effect class, not only as one aggregate. A low global rate can hide a detector that always stops a rare, valuable workflow.

## False-negative and evasion analysis

- **Low and slow:** addressed by the slow window and cumulative declared budgets.
- **Retry identifier rotation:** detector joins on normalized intent/effect, not only caller-provided attempt IDs.
- **Tool hopping:** counters aggregate by effect class and trace as well as tool ID.
- **Destination churn:** first-seen identifiers aggregate into a novelty count; private/reserved classification remains a hard rule.
- **Split across sub-agents:** parent/child trace lineage must roll up tool counts exactly once.
- **Telemetry suppression:** missing mandatory evidence before a high-risk effect triggers `H-TELEMETRY-GAP`.
- **Post-halt race:** lane transition and effect authorization must share an atomic compare-and-set or equivalent serialized decision.
- **Benign-looking sequence fragments:** existing sequence-aware lineage must survive handoff and retry; otherwise the effect remains `UNKNOWN` and is not allowed to egress.

## Offline replay plan

### Corpus

Create four versioned, non-production-effect trace sets:

1. **Benign historical:** scrubbed receipts from successful workflows, stratified by workflow/effect class.
2. **Hard hazards:** authorization drift, forbidden/reserved destinations, redirect escapes, sensitive-read-to-egress, missing telemetry, and post-halt attempts.
3. **Soft anomalies:** request bursts, denial loops, tool-depth expansion, destination fan-out, elevation churn, and error storms.
4. **Evasion/negative controls:** low-and-slow traces, tool hopping, retry-ID rotation, nested agents, long benign workflows, and legitimate new public destinations.

Synthetic traces must declare which external effect would have happened, but replay must never issue it.

### Harness behavior

- Sort by `seq`; reject duplicate or impossible ordering.
- Execute the same deterministic policy code intended for enforcement.
- Record every state transition, matching signal, policy version, and blocked effect.
- Run each trace twice and require byte-equivalent decisions/reason codes.
- Test partial telemetry explicitly.
- Use a chronological train/tune/holdout split for threshold selection.
- Produce per-workflow and per-effect confusion matrices plus detection and reset distributions.

### Metrics

- Hard-hazard block recall before first forbidden effect.
- Soft-anomaly precision and recall.
- Benign degrade rate and benign halt rate.
- Detection delay in tool boundaries and wall-clock time.
- Reset/recovery time.
- Duplicate decision rate and nondeterminism count.
- Coverage: fraction of high-risk effects with complete minimum telemetry.
- Worst subgroup result by workflow and effect class.
- Policy evaluation overhead at p50/p95/p99, measured in the target runtime.

Report confidence intervals and raw denominators. Do not promote on percentages without counts.

## Promotion gates

### Absolute safety gates

All must pass:

1. Every hard-hazard replay is blocked **before** its first forbidden external effect.
2. Missing mandatory telemetry never fails open for a high-risk effect.
3. Halt state cannot be cleared by the stopped invocation, retry, child agent, or handoff.
4. Replays are deterministic and emit stable reason codes.
5. Parent/child and retry accounting counts each tool attempt exactly once.
6. Raw secrets, token values, prompt bodies, and tool results are absent from detector telemetry by default.
7. Existing ordinary authorization remains authoritative; the anomaly policy cannot grant an action that authorization denied.

### Effectiveness gates

Before replay, the owner must declare:

- maximum acceptable benign-degrade rate,
- maximum acceptable benign-halt rate by workflow/effect class,
- maximum hard-hazard detection delay,
- minimum soft-anomaly precision/recall for the selected threat set,
- maximum evaluation overhead.

Promotion requires the frozen configuration to satisfy every declared bound on the chronological holdout and every absolute safety gate. If the corpus is too small for a useful confidence interval, report `INSUFFICIENT_EVIDENCE`; do not claim success from zero observed false halts.

## Rejection criteria

Reject or narrow this baseline if any of the following occurs:

- A hard hazard reaches an external effect before the halt decision.
- High-risk actions proceed when minimum telemetry is missing.
- Benign false halts exceed the predeclared budget in any material workflow subgroup.
- The same replay produces inconsistent state transitions.
- Counter joins double-count retries, pagination, or child-agent calls.
- Destination classification cannot defend redirects, DNS changes, private/reserved ranges, and alternate IP forms at the enforcement point.
- The detector requires raw sensitive content to achieve acceptable results.
- Evaluation overhead threatens the tool boundary it is meant to protect.
- A learned detector is proposed before this deterministic baseline is shown inadequate on a frozen corpus.
- Recovery semantics permit the acting agent to self-authorize resumption.

## Falsifiable hypotheses

1. A hard-invariant layer will block all seeded authorization/destination/sequence hazards before effect; one miss rejects the implementation.
2. Requiring two independent soft signals or one dual-window signal will reduce benign halts versus any single fast-window threshold while preserving the declared soft-anomaly recall.
3. Retry collapsing will materially reduce false rate/deny alarms without reducing detection of variant probing.
4. Per-effect and per-workflow budgets will outperform one global request-rate threshold on benign-halt rate.
5. A slow event window will detect seeded low-and-slow traces that evade the fast window.
6. Treating destination novelty alone as non-halting will reduce research/browsing false stops; novelty plus sensitive lineage or elevated effect will still block the seeded hazards.
7. Fail-closed telemetry completeness will expose instrumentation gaps before high-risk effects rather than silently biasing the detector.
8. The deterministic policy will remain within the predeclared latency budget; failure rejects promotion rather than justifying asynchronous enforcement.

All are `UNVALIDATED_HYPOTHESIS` until replayed.

## Minimal implementation candidate

No implementation PR is prepared in this transaction.

A bounded follow-up candidate exists only after the repository owning the effect-enforcement point is identified: implement a pure `evaluate(event, state, config) -> decision` replay library plus JSON fixtures, with no live tool/network integration. Its owner, repository, and native validation path are not established by the research repository alone, so creating code now would guess authority and placement.

## Sources

Accessed 2026-10-06 unless noted.

1. OpenTelemetry, “Semantic conventions for generative client AI spans” (current main; status Development): https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
2. OpenTelemetry, “Generative AI metrics” (current main; status Development): https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-metrics.md
3. Model Context Protocol, “Security Best Practices,” specification snapshot 2025-11-25: https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices
4. Google, *Site Reliability Engineering Workbook*, Chapter 5, “Alerting on SLOs”: https://sre.google/workbook/alerting-on-slos/
5. NIST SP 800-137, *Information Security Continuous Monitoring (ISCM) for Federal Information Systems and Organizations*: https://csrc.nist.gov/pubs/sp/800/137/final
6. NIST SP 800-53 Rev. 5, Release 5.2.0 notice and controls: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
7. AXIOM Research, `2026-10-05-minimal-sequence-aware-exfiltration-policy-chatgpt.md`.
8. AXIOM Research, `2026-10-05-agentic-mcp-tool-supply-chain-identity-chatgpt.md`.

## Manager disposition

`ACCEPT_WITH_FOLLOWUP`

The evidence supports testing this small deterministic baseline. Acceptance is limited to a durable research recommendation and an offline replay design. It does not authorize production enforcement, live network actions, tool-control deployment, or an implementation repository choice.
