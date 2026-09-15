# 3. Validation performed and results

The canonical architecture remains version `1.0.0`; no contract or invariant changed during this synchronization. Live implementation, tests, and runtime evidence were reconciled against the architecture authority, recovery, provider, spend, and interoperability boundaries.

**Repository state:** `axiom-apex/main` is at `67696d661d5084cb2cb4aa641835e725dbb6f75f` (source version `3.2.0`) and `axiom-ason/main` is at `379c4833db012080aa016ac19c30f53f00e548b0` (source version `0.3.0`). Both working trees were clean and synchronized with `origin/main` at validation time.

**ASON → APEX authorization and interoperability:** ASON remains policy authorization only. Caller-supplied `authority_ref`, exact approved-plan digest, policy identity, and authorization identity are bound before APEX dispatch. Current cross-repository validation passed `18/18` ASON/APEX integration tests and the full ASON suite (`63/63`). This remains trusted caller provenance, not cryptographic attestation or an exactly-once guarantee.

**APEX recovery reliability:** current APEX additionally binds each new live effect-ledger run to a SHA-256 digest of the planner-visible tool-registry contract. Registry key/name, input/output type schemas, required arguments, and `retry_safe` participate; registry ordering, implementation code, environment, provider state, and remote-service semantics do not. Missing or changed registry binding blocks live recovery before dispatch. The current zero-provider offline gate passed `159` tests with `37` deselected.

**Provider implementation:** APEX continues to expose native `gemini` and `ollama` provider selection. Planning compute remains distinct from execution authority.

**Provider-backed Gemini evidence:** current APEX revision `67696d661d5084cb2cb4aa641835e725dbb6f75f` is accepted for the exact direct-host profile `gemini / gemini-3.8-flash`, Python `3.12.9`, `google-genai 1.66.0`, and execution-profile digest `430069bf67aaaf9aa1c45ac665a94d714213422de9a5c30e7431dfd2d262c3de`. Provider smoke, both live integration tests, valid halt-terminated planning, real write/read execution, and a clean `12/12` benchmark passed (`100.725s`, APEX score `0.98635`). One prior full attempt observed a redacted pre-planning provider failure on `multi_step_chain`; no tool effect was dispatched and the failure did not reproduce on the clean full rerun. Canonical evidence is `../apex-validation-gemini-3.8-flash-20260915T034212Z.json`. Acceptance is exact-profile evidence and does not generalize to changed source, provider, model, configuration digest, host harness, or workload.

**Local Ollama evidence:** `gemma3:1b` remains measured at `2/12` benchmark tasks in two complete runs and is not production-routable. The `qwen3.5:0.8b` benchmark remains incomplete after four consecutive provider timeouts and is not accepted. Endpoint availability is not workload compatibility.

**Harness state:** the validated generic operational slice was promoted into private `axiom-harness` version `0.1.0`; its standalone invariant suite passed `15/15`, while the reward-specific application remained separate and passed its reduced `48/48` suite after duplicate generic ownership was removed. Harness remains durable operational orchestration only when persistence has material value.

**Optional remote operator infrastructure:** Desktop Commander Remote MCP `0.2.50` was validated as an optional privileged host-access channel for explicit operator-authorized inspection, tests, diagnostics, and maintenance. It is not an AXIOM authority source, APEX target by default, Harness executor by default, CI dependency, or runtime requirement. Its live unrestricted filesystem scope and external beta-service/telemetry state prohibit unattended routing without separate hardening and validation.

**Account/resource evidence:** account-specific compute, billing, quota, and trial state remains private operational state owned by Director/runtime evidence rather than this public architecture status. Verified account evidence does not create a nonzero spend allowance; free-tier eligibility and enabled APIs are not equivalent to remaining quota or authorized spend.

# 4. Remaining unresolved constraints or uncertainties

1. Exact per-run hosted-model cash cost remains unisolated from aggregate account billing.
2. Any materially changed APEX source/provider/model/configuration digest/host harness/workload requires its own measured provider-backed acceptance.
3. The Qwen local benchmark remains incomplete; measured Gemma remains rejected and neither local profile is production-routable.
4. `authority_ref` remains trusted caller provenance rather than cryptographic proof of human/Harness authority.
5. The exact `sensitivity_class` taxonomy and domain-specific acceptance/retry/event/mutation contracts remain policy/domain concerns.
6. No stronger host-power-loss, distributed recovery, compensation, submission-deduplication, or exactly-once external-effect guarantee is inferred.
7. Desktop Commander unattended routing remains blocked pending exact directory/tool scope, privacy/telemetry posture, authentication, failure semantics, and deterministic acceptance evidence.
8. No host-harness nesting, provider abstraction, or additional control plane is justified without measured net-value evidence.

# 5. Convergence rationale

The intended architecture remains converged. Current evidence strengthens implementation reliability and operational channel knowledge without changing the normative authority path:

```text
Owner/Operator
→ Director
→ WorkIntent
→ Harness when durable orchestration has material value, otherwise authorized direct work
→ ASON policy authorization where required
→ APEX or another bounded executor
→ evidence
→ acceptance/commit
→ CompletionReceipt / Director update
```

APEX registry-contract recovery binding, Harness promotion, account-resource discovery, trial activation, and optional Remote MCP access are implementation/status evidence. None requires a new architecture invariant, repository, scheduler, provider framework, or mandatory dependency. `architecture/VERSION` therefore remains `1.0.0`.

The next substantive portfolio objective is not an architecture pass. Director owns the singleton Current Opportunity and currently selects productization of the validated reliability/control capability; this status file does not duplicate that queue.

# 6. Estimated additional passes to convergence

`0` additional architecture-contract passes are justified by current evidence. Future status updates should be evidence-driven and must not generalize acceptance across materially different source, provider, model, context, host, tool-registry, or billing profiles.
