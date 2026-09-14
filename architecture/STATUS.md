# 3. Validation performed and results

The supplied architecture and modification task were checked for ownership uniqueness, provider/account placement, control-plane duplication, spend enforcement, model/profile identity, nested-harness semantics, acceptance boundaries, and migration ordering.

**Repository state:** the accessible APEX default branch remains at commit `0fa8ffc92d09d13821b4ae0d041ecebf7c94236d`. The published immutable `v3.1.1` release exists and contains the wheel/source/checksum artifacts, while the current README still calls the version unreleased; this is confirmed documentation drift rather than architectural uncertainty.

**Provider implementation:** APEX currently supports exactly `gemini` and `ollama` through the configured provider abstraction. Ollama uses `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, native `/api/generate`, non-streaming generation, temperature `0.2`, and a 300-second request timeout.

**Ollama protocol compatibility:** APEX consumes response fields that remain present in current Ollama documentation. Ollama exposes additional duration metrics sufficient to calculate detailed prompt/generation performance if the validation path chooses to capture them.

**Provider validation:** unit tests validate fail-closed provider behavior. Live local Ollama workload tests now reject the current Gemma/Qwen profiles, while direct APEX→Gemini integration has passed the provider smoke, existing live integration tests, dry-run planning, and real write/read execution. The Gemini profile remains `EXPERIMENTAL` until workload-level acceptance is measured.

**Existing benchmark capability:** `apex.bench` already provides a suitable first production gate: real APEX subprocess execution, per-task wall duration, pass/fail results, token counts, aggregate pass rate, speed factor, token efficiency, and composite score. The supplied benchmark covers twelve file/shell/memory/HTTP/multi-step workloads.

**Codex/OpenCode:** current Ollama documentation explicitly supports both environments and recommends substantially larger contexts for these coding harnesses. Their availability therefore justifies experiments, not a presumption that the current local Gemma/Qwen profiles are suitable inside them.

**AGY:** current Antigravity documentation identifies `agy` as a terminal agent harness with reasoning, execution, and orchestration capabilities. That supports classification as a host harness, but no APEX-specific integration result is available.

**Live local results:** `gemma3:1b` completed two 12-task APEX benchmark runs and passed 2/12 tasks in each (`pass_rate = 0.1667`), with wall times 583.896 s and 527.865 s. Most failures were malformed or invalid generated plans; the repeatable passes were `read_file` and `large_file_write`. `qwen3.5:0.8b` was manually stopped after four consecutive tasks each failed at the provider's approximately 300-second timeout; the fifth task had begun. These exact local profiles are not production-routable. The Qwen suite is incomplete and must not be represented as a completed 12-task benchmark.

**`gxy` audit:** no authenticated account billing/quota/usage surface is available in this execution environment, and the repository itself contains no named `gxy` configuration abstraction. Consequently, services, quotas, rate limits, free allowance, current consumption, and monthly paid capacity remain unverified. No charge was incurred.

**Gemini integration:** on APEX revision `0fa8ffc92d09d13821b4ae0d041ecebf7c94236d`, `gemini-3.8-flash` passed a direct provider smoke (`131` tokens), both existing live integration tests (`2 passed in 22.35s`), a valid halt-terminated APEX dry-run (`1457` tokens), and real APEX write/read execution (`961` tokens). Evidence is recorded in `../apex-validation-gemini-3.8-flash-20260914T210930Z.json`. Account identity and credential remain excluded from public state.

**Host-harness results:** no APEX-through-Codex/AGY/OpenCode execution is accepted. Direct APEX provider validation remains the prerequisite baseline before nested-harness comparisons.

# 4. Remaining unresolved constraints or uncertainties

1. The direct Gemini integration gate passes, but the 12-task APEX workload benchmark has not yet established production acceptance for `gemini-3.8-flash`.
2. Account-specific quota, limits, free allowance, pricing tier, current usage, billing state, and reset behavior remain unverified in public evidence; no nonzero spend capacity may be inferred.
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

The architecture has therefore converged under currently available evidence. **Implementation validation has not converged** because Gemini workload acceptance, private account/resource state, the target ASON approval binding, and empirical host-harness comparisons remain unresolved.

The highest-value next action is the 12-task direct APEX→Gemini benchmark, provided the private account's zero/approved-spend envelope is verified first. This is the remaining workload-level gate before the Gemini profile can be considered for production routing.

# 6. Estimated additional passes to convergence

`indeterminate`
