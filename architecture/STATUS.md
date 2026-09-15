# 3. Validation performed and results

The supplied architecture and current implementation state were checked for authority boundaries, durable authorization provenance, provider/account placement, execution-profile identity, workload acceptance, spend constraints, and cross-repository consistency.

**Repository state:** `axiom-apex/main` is at `372a272e99934b3cadf69f08be95de081bfb1de1` (APEX source version `3.2.0`) and `axiom-ason/main` is at `379c4833db012080aa016ac19c30f53f00e548b0` (ASON source version `0.3.0`). Their post-merge hosted CI completed successfully. Publication/release state remains separate from source validation.

**Durable ASON→APEX authorization binding:** the prior approval-provenance gap is resolved at the trusted application boundary. ASON requires caller-supplied `authority_ref`, generates an authorization identity plus exact approved-plan and policy digests, and submits the exact plan through APEX `/authorized-run`. APEX validates the binding, atomically persists authorization provenance with the plan/effect ledger before tool dispatch, and re-validates the durable binding during recovery. Local cross-repository validation passed the authorization/recovery gate (`45 passed`), the APEX offline regression suite (`152 passed, 37 deselected`), and the complete ASON suite (`63 passed`). This does not establish cryptographic attestation of the upstream authority reference or exactly-once external effects.

**Provider implementation:** APEX continues to expose native `gemini` and `ollama` provider selection. Planning compute remains distinct from execution authority.

**Local Ollama workload evidence:** the measured `gemma3:1b` profile passed `2/12` benchmark tasks in each of two complete runs and is not production-routable. The `qwen3.5:0.8b` run produced four consecutive provider timeouts before the user aborted the suite; it is therefore incomplete and not accepted. Endpoint availability is not treated as workload compatibility.

**Gemini integration and workload acceptance:** direct APEX→`gemini-3.8-flash` on APEX revision `372a272e99934b3cadf69f08be95de081bfb1de1`, Python `3.12.9`, and `google-genai 1.66.0` passed the provider smoke (`132` tokens), both live integration tests (`2 passed in 12.16s`), valid halt-terminated dry-run planning (`1074` tokens), real write/read execution (`922` tokens), and all `12/12` benchmark tasks. The benchmark completed in `94.401s` with pass rate `1.0`, speed factor `1.0`, token efficiency `0.9862`, APEX score `0.98624`, and `20,256` benchmark tokens. The canonical validation artifact is `../apex-validation-gemini-3.8-flash-20260914T224016Z.json`. Result: `ACCEPT`.

**Comparison with the prior accepted Gemini profile:** the prior APEX revision completed the same benchmark in `91.247s` with `21,721` tokens, token efficiency `0.9838`, and APEX score `0.983798`. The new revision remains `12/12`; wall time is `3.46%` higher while benchmark token use is `6.74%` lower, token efficiency is `0.24%` higher, and APEX score is `0.25%` higher. These differences are treated as run-level variance/performance evidence, not as a change in the acceptance classification.

**Gemini resource state:** Provider capacity was sufficient for the accepted validation run. Account identifiers, quota, usage, billing state, pricing, and other account-specific telemetry are retained outside the public repository. No public evidence record grants a spend allowance beyond an explicitly authorized cash ceiling.

**Host-harness results:** no measured evidence yet establishes that Codex, AGY, or OpenCode improves accepted direct APEX execution enough to justify nesting or a bespoke adapter.

# 4. Remaining unresolved constraints or uncertainties

1. Exact per-run Gemini cash cost remains unisolated from aggregate account billing.
2. Account-specific provider quota, usage, billing, and identity remain private operational state rather than public architecture evidence.
3. The historical provider-account alias has not been reconciled as a first-class APEX configuration abstraction.
4. No measured comparison yet establishes whether Codex, AGY, or OpenCode improves APEX capability, reliability, automation, or total resource efficiency enough to justify nesting.
5. The Qwen local benchmark is incomplete; the measured Gemma profile is rejected and neither current local profile is production-routable.
6. The durable `authority_ref` binding is trusted caller provenance, not a cryptographic signature or independent proof of human/Harness authority.
7. `reward-harness` remains unavailable for a defensible `PROMOTE`, `RETAIN`, or `SPLIT_LATER` decision.
8. The exact `sensitivity_class` taxonomy remains policy-defined.
9. Domain-specific acceptance contracts, retry evidence, event sources, and mutation rules remain domain concerns.
10. No stronger host-power-loss, distributed recovery, compensation, or exactly-once external-effect guarantee is inferred.
11. No materially different model/provider/context/host profile should be promoted without its own measured acceptance workload.

# 5. Convergence rationale

The intended architecture remains converged: no new repository, provider framework, scheduler, control plane, or generic adapter is required by the new evidence.

Two previously material implementation uncertainties are now resolved:

```text
ASON authorization identity ↔ exact APEX plan/run
direct APEX ↔ Gemini 3.8 Flash workload acceptance
```

The evidence supports the existing architecture rather than requiring a normative contract change. Therefore this update is confined to `STATUS.md` plus a Research validation artifact and requires no architecture `VERSION` bump.

The current accepted execution baseline is:

```text
direct APEX 3.2.0
→ Gemini 3.8 Flash
→ bounded APEX tools
→ 12/12 accepted workload
```

and authorization-required exact plans now use:

```text
caller/Harness authority reference
→ ASON 0.3.0 policy decision
→ exact plan + durable authorization binding
→ APEX 3.2.0 /authorized-run
→ pre-dispatch ledger persistence
→ bounded execution/recovery
```

Further architectural expansion remains unjustified without evidence. The next research action, if host-harness nesting is still strategically relevant, is one measured Codex→APEX comparison against the accepted direct baseline; it should be promoted only if it improves total expected value without weakening authority, spend, sensitivity, or recovery boundaries.

# 6. Estimated additional passes to convergence

`0` additional architecture-contract passes are justified by current evidence. Empirical implementation validation remains ongoing as new execution profiles or host harnesses are proposed.
