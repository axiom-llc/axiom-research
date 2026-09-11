# AXIOM Research

Use this repository as the canonical research workspace for the AXIOM execution ecosystem. Keep durable theory, source-grounded architecture research, and reusable research programs here; keep product code and transient implementation notes in their owning repositories.

**Canonicalized:** 2026-09-11T08:08:11-04:00

## Contents

| File | Role | Authority |
| --- | --- | --- |
| `ai-loop-architecture-taxonomy.md` | Classify iterative, autonomous, human-supervised, and learning loop architectures. | Research taxonomy; validate workload-specific quantitative claims empirically. |
| `apex-transactional-effects-research.md` | Record source-grounded APEX/ASON crash-gap findings and the saga-lite WAL design. | Implementation input tied to the repository snapshots named in the artifact; revalidate current source before coding. |
| `j-space-research.md` | Preserve the J-space falsifiable research program and epistemic boundaries. | Research agenda and toy formalization; do not treat it as evidence about hidden model internals. |
| `rag-crash-consistency-architecture.md` | Define the selected single-owner RAG lifecycle, journaling, recovery, and concurrency model. | Architecture proposal; do not claim power-loss atomicity or implementation completion without tests. |
| `recursive-hyper-optimization.md` | Analyze computable recursive self-optimization and its limits. | Theory; treat APEX references as implementation mapping, not proof of stronger self-modification properties. |
| `temporal-state-resolution.md` | Separate epistemic latency compression from physical time and dynamical evolution. | Conceptual synthesis grounded in cited physical/computational limits. |
| `tacon2026-apex-deterministic-execution-contracts.md` | Preserve the June 2026 academic paper as a diffable historical transcript with original PDF provenance. | Historical publication; do not use it as the current implementation specification where later source-grounded research conflicts. |

## Interpretation Rules

1. Treat current repository source and passing tests in the owning project as authoritative for implemented behavior.
2. Treat source-grounded research artifacts as authoritative only for the snapshots and evidence they explicitly identify.
3. Treat architecture proposals as implementation inputs until code and tests demonstrate the claimed invariants.
4. Treat the June 2026 APEX paper as historical where it describes rollback, validation ownership, replay, RAG embedding, or self-optimization behavior that later source inspection supersedes.
5. Preserve unresolved boundaries explicitly. In particular, revalidate the current ASON-to-APEX authoritative-plan submission contract before implementing the transactional-effects WAL.
6. Keep probabilistic planning and deterministic execution conceptually separate; do not infer execution guarantees from model behavior.
7. Remove transient vendor/product reconnaissance after its durable architectural insight has been incorporated elsewhere.

## Current Research Priorities

1. Verify the current ASON-to-APEX policy-to-execution contract before changing transactional semantics.
2. Use `apex-transactional-effects-research.md` to close the pre-effect durability gap before adding broad rollback claims.
3. Use `rag-crash-consistency-architecture.md` to implement single-owner RAG persistence and crash-injection tests without overstating Chroma durability guarantees.
4. Keep speculative programs such as J-space and temporal-state resolution clearly separated from observed implementation facts.

## Ecosystem

- [AXIOM Apex](https://github.com/axiom-llc/axiom-apex) - deterministic execution runtime.
- [AXIOM RAG](https://github.com/axiom-llc/axiom-rag) - retrieval subsystem.
- [AXIOM ASON](https://github.com/axiom-llc/axiom-ason) - policy/planning layer under active contract verification.
- [AXIOM Demos](https://github.com/axiom-llc/axiom-demos) - deployable demonstrations and provider integrations.
- [AXIOM Research](https://github.com/axiom-llc/axiom-research) - this research workspace.
- [AXIOM Portal](https://axiom-llc.github.io/) - public project index.
