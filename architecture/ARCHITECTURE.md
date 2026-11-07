# AXIOM Architecture — Public Contract

## Purpose

This document preserves the externally reviewable architectural responsibilities,
authority limits, and validation invariants of AXIOM's human–machine engineering
systems. Internal implementation maps, provider/account configurations, routing
decisions, exact interfaces, operational state, and commercially sensitive
architectural analyses are withheld from unrestricted publication.

## Components and authority

- **Owner/Operator:** Retains goals, authorization, acceptance, and policy authority.
- **Director:** Coordinates objectives and priorities within delegated authority.
- **Harness:** Manages durable task progression where necessary.
- **APEX:** Runs bounded machine-execution steps.
- **ASON:** Performs declared policy/plan authorization.
- **RAG:** Provides retrieval and persistent knowledge interfaces subject to evidence
  and data-integrity controls.

Interfaces and enforcement must be evaluated on actual system revisions.
This summary is not evidence of a deployed security guarantee or autonomous physical
capability.

## Governing invariants

1. `INV-001` — Owner/Operator authority is final.
2. `INV-002` — Director decides **what is worth doing**; Harness owns **operational task progression**; executors own only their executions.
3. `INV-003` — Direct ephemeral cognitive/tool work may bypass Harness when persistence adds no material value.
4. `INV-004` — Human attention is a scarce schedulable resource.
5. `INV-005` — Prefer deterministic execution when it satisfies acceptance.
6. `INV-006` — Select the lowest-total-cost eligible mechanism, not merely the nominally cheapest mechanism.
7. `INV-007` — Exact state is queried structurally; long-form knowledge is retrieved semantically.
8. `INV-008` — Context narrows downward.
9. `INV-009` — Workers/executors produce candidates; they do not declare canonical task completion.
10. `INV-010` — Consequential boundaries produce machine-readable evidence.
11. `INV-011` — `UNKNOWN` never implies retry safety.
12. `INV-012` — Retry requires affirmative evidence of safety plus remaining budget.
13. `INV-013` — ASON is policy authorization, not strategy, scheduling, routing, retry, or execution.
14. `INV-014` — APEX is the bounded machine execution runtime, not a second task scheduler.
15. `INV-015` — Harness task attempts and APEX runs are distinct identities.
16. `INV-016` — APEX owns internal dispatch/effect uncertainty; Harness owns cross-executor task outcome.
17. `INV-017` — An authorization-required APEX execution must bind the exact authorization identity and approved plan digest durably before dispatch.
18. `INV-018` — ASON→APEX durable authorization provenance binds the caller-supplied authority reference, authorization identity, policy digest/reference, and exact approved-plan digest to the APEX run before dispatch; this is durable application provenance, not cryptographic attestation or independent proof of human identity.
19. `INV-019` — Never claim exactly-once external effects without proof from the external system.
20. `INV-020` — RAG persistence has one cooperating owner per root.
21. `INV-021` — Repository, process, dependency, context, abstraction, and nested-agent count are costs.
22. `INV-022` — A service, repository, provider adapter, or orchestration layer must remove more total complexity than it adds.
23. `INV-023` — Preserve validated working paths during migration.
24. `INV-024` — Public repositories must not contain live sensitive personal state or credentials.
25. `INV-025` — Autonomy and supply-chain independence increase only from evidence; neither grants authority to change goals, constraints, authorization boundaries, or safety requirements.
26. `INV-026` — Optimize valuable autonomous progress, not automation depth.
27. `INV-027` — A model endpoint responding successfully does **not** establish APEX compatibility; acceptance requires workload-level validation.
28. `INV-028` — Provider/model/context/host configuration is part of the execution profile and cannot be generalized across materially different configurations.
29. `INV-029` — Unverified quota or free allowance is not spendable capacity.
30. `INV-030` — No provider fallback may silently incur cash cost, weaken sensitivity constraints, or cross an authorization boundary.
31. `INV-031` — External coding/agent harnesses do not acquire AXIOM task authority merely by launching or invoking APEX.
32. `INV-032` — Prefer direct APEX execution before adding nested host-harness orchestration.
33. `INV-033` — Account-specific usage and pricing must be verified before assigning nonzero spend capacity.

## Public validation

The tracked [schemas](schemas/), synthetic fixtures, and
[architecture checks](tests/check.py) validate the published interface contract.
They do not expose the full internal implementation, nor do they independently
establish production security, reliability, throughput, or commercial outcomes.

The complete preceding technical architecture was retained byte-identically in
protected storage before this public edition was issued. All changes remain
subject to [publication control](../PUBLICATION.md).
