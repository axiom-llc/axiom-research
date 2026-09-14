# AXIOM Architecture

This directory contains the canonical, versioned architecture contract for the AXIOM ecosystem.

It lives in `axiom-research` because Research owns durable architecture, evidence, validation, and falsification. Runtime implementation remains in each owning repository. Architecture describes intended system behavior; it does not by itself prove that behavior is implemented.

## Canonical files

| Path | Role |
| --- | --- |
| `ARCHITECTURE.md` | Normative intended architecture, authority boundaries, lifecycle semantics, and governing invariants. |
| `VERSION` | Semantic version of the architecture contract. |
| `schemas/*.schema.json` | Machine-verifiable projections of explicitly specified record shapes and enums. |
| `STATUS.md` | Current validation evidence, implementation gaps, unresolved constraints, and convergence state. |
| `CHANGELOG.md` | Durable record of material architecture changes. |
| `tests/` | Deterministic contract, schema, and fixture validation. |

Do not create duplicate canonical copies of these facts elsewhere.

## Source of truth

Use the authority that matches the question:

| Question | Authority |
| --- | --- |
| What AXIOM is intended to do | `ARCHITECTURE.md` |
| What a specified architecture record permits | `schemas/*.schema.json`, as a projection of `ARCHITECTURE.md` |
| What a runtime currently does | Current source plus passing tests in the owning repository |
| Whether repositories conform together | Reproducible integration evidence, primarily in `axiom-infra` |
| What is currently validated, blocked, or unresolved | `STATUS.md` |
| Why a decision exists or how it was falsified | Durable research evidence in `axiom-research` |
| What changed historically | Git history plus `CHANGELOG.md` |
| Generated summaries or agent interpretations | Non-authoritative |

`ARCHITECTURE.md` is authoritative for intended architecture. A schema must not silently contradict it. A conflict between normative prose and a schema is a defect to reconcile before acceptance.

Current source and passing tests in an owning runtime repository outrank architecture or research descriptions when making claims about implemented behavior. Such evidence does not silently rewrite the intended architecture; a mismatch is architecture/implementation drift that must be resolved explicitly.

Owner/Operator authority remains final.

## Versioning

`VERSION` uses `MAJOR.MINOR.PATCH`.

- **MAJOR** — incompatible contract change, including incompatible authority, ownership, lifecycle, invariant, repository-responsibility, or schema semantics; removing/reusing an invariant ID; removing or retyping a schema field; adding a required field; or otherwise invalidating previously conforming behavior/data.
- **MINOR** — backward-compatible normative addition, such as an optional schema field, compatible new record/capability, or new invariant that does not invalidate existing conforming behavior.
- **PATCH** — contract clarification or correction that changes no accepted/rejected behavior and is neither incompatible nor additive.

Changes confined to `README.md`, `STATUS.md`, tests, CI, formatting, or other contract-neutral infrastructure do **not** require a `VERSION` bump.

Every contract-version change must update `CHANGELOG.md` in the same change. Stable version tags, if used, are `architecture-vMAJOR.MINOR.PATCH` and must never be moved or rewritten.

## Stable invariant identities

Invariant IDs are durable references.

- Never renumber an existing invariant to make the list visually convenient.
- Never reuse a retired ID for different semantics.
- Treat a semantic change to an existing invariant as a compatibility decision, not an editorial edit.
- Update deterministic validation intentionally when the invariant set changes.
- Preserve historical meaning in Git history and `CHANGELOG.md`.

Current deterministic validation requires the ordered set `INV-001` through `INV-033`.

## Change contract

Before accepting a normative architecture change, record enough information to make the decision reviewable:

```text
objective
compatibility classification: MAJOR | MINOR | PATCH
affected invariant IDs
affected schemas/contracts
evidence and source references
affected repositories
acceptance criteria
unresolved assumptions or constraints
```

Apply these rules:

1. Make the smallest change that satisfies the objective.
2. Do not invent serialization, taxonomy, timing, authority, recovery, or policy semantics that remain unspecified.
3. Preserve unresolved state explicitly until evidence resolves or rejects it.
4. A schema-semantic change requires corresponding valid/invalid fixtures and deterministic validation.
5. An implementation claim requires reproducible evidence from the owning repository or integration environment.
6. Resolving an item in `STATUS.md` requires evidence; do not delete uncertainty merely because a proposed design exists.
7. A new repository, control plane, provider abstraction, adapter, scheduler, or persistent service requires evidence that it removes more total complexity than it adds.
8. Public repository changes must not introduce live credentials, private account state, or sensitive personal state.
9. Contract changes must pass all applicable acceptance gates before becoming canonical.

## AI and agent workflow

AI/agent optimization is permitted as a proposal-and-validation mechanism, not as an independent authority.

For each architecture iteration:

1. Read the complete current contract, `STATUS.md`, relevant schemas/tests, and affected implementation evidence.
2. Identify one defensible high-value change and state its compatibility class.
3. Preserve existing authority boundaries and stable IDs unless the change explicitly and justifiably modifies them.
4. Produce the minimum patch plus any required fixtures/tests.
5. Run deterministic validation.
6. Distinguish observed implementation facts, research evidence, inference, and proposed architecture.
7. Preserve unknowns and unresolved decisions; never convert missing evidence into an assumption.
8. Require explicit Owner acceptance for normative changes before they become canonical.

Agents must not:

- auto-merge normative architecture changes without Owner acceptance;
- claim implementation from architecture text alone;
- promote endpoint availability to workload compatibility;
- infer retry safety from an `UNKNOWN` outcome;
- silently weaken authorization, sensitivity, mutation, or spend constraints;
- use hidden paid fallback or unverified account capacity;
- create repositories or orchestration layers merely to increase abstraction;
- erase contradictory evidence or unresolved constraints to make the architecture appear converged.

Autonomy may increase only from evidence.

## Acceptance

Run locally:

```bash
python architecture/tests/check.py
git diff --check
```

For changes under `architecture/**`, the `Architecture` GitHub Actions workflow must pass after push or pull request.

A normative change is accepted only when:

- deterministic contract/schema/fixture checks pass;
- changed-line whitespace checks pass;
- required version and changelog updates are present;
- required implementation or integration evidence is reproducible;
- no unresolved material conflict is silently discarded; and
- the Owner accepts the normative change.

A passing architecture CI run establishes internal contract consistency. It does not by itself establish that runtime repositories implement the architecture.

## Unresolved state

`STATUS.md` is the canonical current record for architecture-relevant validation gaps and unresolved constraints.

Unresolved items remain explicit until one of these occurs:

```text
RESOLVED  — evidence establishes the required fact or implementation
REJECTED  — evidence falsifies or supersedes the proposed path
DEFERRED  — still valid, but intentionally outside current scope
```

Record the evidence or owner decision when changing that state. Do not infer resolution from elapsed time, a successful unrelated test, or an agent recommendation.

## Minimality

Architecture maintenance follows the architecture's own complexity discipline:

```text
one authoritative owner per fact
minimal repositories
minimal dependencies
minimal duplicated state
deterministic checks before probabilistic judgment
evidence before autonomy
evidence before abstraction
preserve validated working paths
```

Add process only when it removes more total complexity, risk, or ambiguity than it creates.
