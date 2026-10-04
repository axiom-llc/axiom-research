# Cross-domain organizational simulation findings

## Scope and evidence basis

This synthesis covers only the five accepted `VALIDATED_EXECUTABLE_DEMO` simulations retained in this repository: robotics production, software development, specialty-care administration, SOC operations, and logistics/supply chain. `portfolio-summary.json` binds the aggregate to the exact retained evidence/evaluation artifacts by SHA-256 and source revision.

Across the five cases, the retained evidence represents 74 modeled organizational steps, 29 modeled departments, 31 actors, 27 approval-bearing steps, 11 deterministic exception injections, and 74 APEX effects/events. Every retained effect is recorded `SUCCEEDED`. Each case independently passed the same seven checks: APEX completion, durable authorization/plan binding, exact terminal-state equality, effect-ledger presence, authorization evidence, failure before APEX dispatch when authority is omitted, and live recovery that reused completed local-file effects.

## Cross-domain findings

1. **The Research contracts generalized without domain-specific APEX machinery.** All five domains use the same organization, scenario, fixture, evidence, evaluation, and runner contracts. No simulation required a new APEX, ASON, RAG, or Harness runtime semantic.
2. **Organizational semantics and machine execution remained cleanly separable.** Domain workflows describe actors, dependencies, approvals, exceptions, and expected outcomes; each simulation separately supplies an exact ASON request. This avoided turning the Research model into a second execution engine.
3. **Authority is a repeated cross-domain boundary.** Every accepted run carried an application-level authority reference and exact approved-plan digest into APEX. In every domain, the same exact execution request without authority failed before APEX run creation.
4. **Conservative completed-effect recovery generalized across the portfolio.** Live replay reused already completed local-file effects in all five runs. Across those recovery checks, 67 produced files retained identical nanosecond modification times. This is direct evidence for completed-effect reuse in these runs, not an exactly-once external-effect guarantee.
5. **Exception modeling is portable, but business exceptions are not runtime failures.** The portfolio represents dependency unavailability, retry-safe/non-retry-safe exceptions, and approval denial inside synthetic organizational state. Those modeled exceptions should not be conflated with APEX execution failures or empirical defect/incident rates.
6. **Deterministic acceptance is reusable when outcomes are machine-observable.** Exact terminal-state comparison plus durable run evidence was sufficient for these scenarios. Subjective quality, professional judgment, physical safety, and real-world outcome evaluation remain outside this deterministic acceptance boundary.

## Reusable primitive decision

The evidence does **not** justify adding a new APEX/ASON/Harness primitive. Repeated behavior is already covered by existing exact-plan authorization, effect-ledger recording, run-detail evidence, and recovery semantics.

The justified reusable improvement is Research-side evidence aggregation: `portfolio-summary.json` provides a canonical, hash-bound index of accepted simulation evidence and common validation checks. This should remain evidence tooling, not runtime authority. Future domains should extend the same contracts unless a repeated, measured limitation demonstrates persistent costly duplication or an actual runtime capability gap.

## Architectural limits exposed

- All tool effects in this portfolio are local-file simulations. No external SaaS, clinical, security, logistics, manufacturing, payment, or physical-control system was mutated.
- The simulations do not validate distributed state coordination, external idempotency, reconciliation after unknown third-party outcomes, or host-power-loss guarantees.
- Synthetic authority references demonstrate application-level provenance only; they do not authenticate a human approver independently.
- Harness was not required because each retained scenario is one bounded exact APEX run. This portfolio therefore does not validate durable multi-attempt organizational scheduling or resource arbitration.
- RAG was not required by these deterministic fixture-driven cases. No cross-domain retrieval-quality claim follows from this portfolio.
- The five domains are evidence of breadth across modeled workflow structures, not proof that arbitrary organizations can be operated autonomously.

## Publication boundary

Derived demos, case studies, or sales claims may state only what these retained artifacts directly establish: AXIOM executed five materially different synthetic organizational workflows through the same domain-neutral Research/ASON/APEX evidence path, with explicit authority gates, durable execution evidence, deterministic terminal validation, and completed-effect recovery in local-file simulations. Any stronger claim requires additional evidence.
