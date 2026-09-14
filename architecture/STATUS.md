# 3. Validation performed and results

The supplied architecture and modification task were checked for ownership uniqueness, provider/account placement, control-plane duplication, spend enforcement, model/profile identity, nested-harness semantics, acceptance boundaries, and migration ordering.

**Repository state:** the accessible APEX default branch remains at commit `0fa8ffc92d09d13821b4ae0d041ecebf7c94236d`. The published immutable `v3.1.1` release exists and contains the wheel/source/checksum artifacts, while the current README still calls the version unreleased; this is confirmed documentation drift rather than architectural uncertainty.

**Provider implementation:** APEX currently supports exactly `gemini` and `ollama` through the configured provider abstraction. Ollama uses `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, native `/api/generate`, non-streaming generation, temperature `0.2`, and a 300-second request timeout.

**Ollama protocol compatibility:** APEX consumes response fields that remain present in current Ollama documentation. Ollama exposes additional duration metrics sufficient to calculate detailed prompt/generation performance if the validation path chooses to capture them.

**Current test gap:** the APEX provider tests validate Ollama's fail-closed, one-attempt, redacted-error path but do not perform a live successful Ollama provider test.

**Existing benchmark capability:** `apex.bench` already provides a suitable first production gate: real APEX subprocess execution, per-task wall duration, pass/fail results, token counts, aggregate pass rate, speed factor, token efficiency, and composite score. The supplied benchmark covers twelve file/shell/memory/HTTP/multi-step workloads.

**Codex/OpenCode:** current Ollama documentation explicitly supports both environments and recommends substantially larger contexts for these coding harnesses. Their availability therefore justifies experiments, not a presumption that the current local Gemma/Qwen profiles are suitable inside them.

**AGY:** current Antigravity documentation identifies `agy` as a terminal agent harness with reasoning, execution, and orchestration capabilities. That supports classification as a host harness, but no APEX-specific integration result is available.

**Live local results:** no Gemma/Qwen APEX benchmark was executed in this pass because this environment cannot access the user's local Ollama daemon, CPU/RAM telemetry, or filesystem checkout.

**`gxy` audit:** no authenticated account billing/quota/usage surface is available in this execution environment, and the repository itself contains no named `gxy` configuration abstraction. Consequently, services, quotas, rate limits, free allowance, current consumption, and monthly paid capacity remain unverified. No charge was incurred.

**Additional compute:** none was promoted or tested because direct local APEX validation and the account audit are prerequisite evidence. This avoids speculative provider/adaptor expansion.

**Host-harness results:** no APEX-through-Codex/AGY/OpenCode execution was claimed because the direct local baseline has not yet been measured. The architecture now explicitly requires that baseline before nested-harness comparisons.

# 4. Remaining unresolved constraints or uncertainties

1. Live APEX results for the installed Gemma and Qwen models are unavailable until the commands above run against the user's local Ollama service.
2. `gxy` service identity, authenticated configuration, quota, limits, allowance, pricing, current usage, billing state, and reset behavior remain unavailable; the only defensible current incremental spend envelope is `$0`.
3. No measured comparison yet establishes whether Codex, AGY, or OpenCode improves APEX capability, reliability, automation, or compute utilization enough to justify nesting.
4. Peak CPU, RAM, model-load, and detailed Ollama evaluation metrics are not currently emitted by `apex.bench`; add measurement only if wall-time/token evidence proves insufficient.
5. Current ASON still lacks the target durable approval-identity binding to APEX recovery state.
6. `reward-harness` remains unavailable for a defensible `PROMOTE`, `RETAIN`, or `SPLIT_LATER` decision.
7. The exact `sensitivity_class` taxonomy remains policy-defined.
8. Domain-specific acceptance contracts, retry evidence, event sources, and mutation rules remain domain concerns.
9. No stronger host-power-loss, distributed recovery, compensation, or exactly-once external-effect guarantee is inferred.
10. No new model/provider or external harness should be promoted until its exact configuration is measured against an acceptance workload.

# 5. Convergence rationale

The modification exposed one genuine architectural gap: compute/account/harness validation lacked an explicit place in the resource and evidence model.

The minimal correction is **not** another orchestrator, provider framework, repository, or generic adapter layer. Existing architecture already contains the required primitives:

```text
Harness resource state
APEX provider abstraction
APEX exact-plan validation/execution
CLI / HTTP / MCP interfaces
Research evidence
acceptance contracts
cash ceilings
```

The converged solution therefore:

```text
models/accounts → measured resources
external agent CLIs → subordinate host harnesses
benchmarks → Research evidence
accepted configuration → routable capacity
```

without altering canonical authority.

Further simplification would erase required distinctions:

```text
strategy ≠ operation
task ≠ attempt
attempt ≠ APEX run
provider compute ≠ execution authority
host harness ≠ AXIOM Harness
endpoint availability ≠ workload acceptance
free-tier claim ≠ verified spend capacity
authorization ≠ execution
execution ≠ acceptance
acceptance ≠ canonical commit
unknown outcome ≠ retry permission
```

Further expansion into dedicated provider repositories, per-harness adapters, new schedulers, new control planes, or automatic multi-provider failover currently has no evidence of positive expected global value.

The architecture has therefore converged under currently available evidence. **Implementation validation has not converged** because live local Ollama state, authenticated `gxy` account telemetry, and empirical host-harness comparisons are unavailable in this environment.

The highest-value next action is the direct Gemma/Qwen APEX benchmark. It establishes the baseline required before either account migration or host-harness nesting can be rationally evaluated.

# 6. Estimated additional passes to convergence

`indeterminate`
