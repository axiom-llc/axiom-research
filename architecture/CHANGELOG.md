# 2. Material changes

1. **Integrated compute/account state into resource routing.** Quota, rate limits, free allowance, current usage, billing period, pricing reference, and hard spend ceiling are now explicit resource-state concerns.
2. **Set the unaudited `gxy` envelope to zero incremental cash by policy.** Unknown quota or pricing cannot be interpreted as usable capacity.
3. **Separated model/provider compute from execution authority.** APEX may use different planning resources without changing its role as bounded machine executor.
4. **Defined host harnesses separately from AXIOM Harness.** `codex`, `agy`, and `opencode` remain subordinate execution/development environments and gain no scheduling or canonical-completion authority.
5. **Made direct APEX the integration baseline.** Nested harness→APEX execution is adopted only when measurement shows positive global value.
6. **Reused APEX's existing CLI/HTTP/MCP surfaces before permitting bespoke harness adapters.**
7. **Added execution-profile identity.** Provider, model, context, endpoint, runtime, host, and configuration are part of benchmark equivalence.
8. **Added `ApexValidationRecord` as a Research artifact.** This captures reproducible model/account/harness results without introducing another runtime state owner.
9. **Made workload acceptance—not endpoint availability—the production criterion for local models.**
10. **Added explicit no-hidden-paid-fallback invariant.**
11. **Moved local Gemma/Qwen validation and `gxy` audit ahead of speculative new providers or adapters.**
12. **Preserved all prior authority, APEX/ASON, retry, recovery, acceptance, RAG, repository, and Harness-promotion boundaries required for correctness.**
