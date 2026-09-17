
# AXIOM Research

Canonical research workspace for the AXIOM execution ecosystem.

Keep durable theory, source-grounded implementation research, architecture
decisions, and reusable research programs here. Product code and transient
implementation notes belong in their owning repositories.

## Organizational simulation evidence program

The approved [`simulations/`](./simulations/) program connects domain/process research to synthetic organization models, actual AXIOM execution evidence, deterministic evaluation, retained findings, executable demonstrations, and evidence-traceable public claims. Canonical evidence remains in Research; runtime authority remains in the owning AXIOM components. Simulations never imply production deployment or autonomous licensed/professional authority.

## Research artifacts

| File                                                   | Role                                                                                | Current interpretation                                                                                                              |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `ai-loop-architecture-taxonomy.md`                     | Taxonomy of iterative, autonomous, supervised, and learning control loops.          | Architectural taxonomy; workload-specific quantitative claims require empirical validation.                                         |
| `apex-transactional-effects-research.md`               | Source-grounded APEX/ASON effect-durability and recovery research.                  | Historical design input; APEX now has a durable effect ledger, but broader compensation remains constrained.                        |
| `write-file-compensation-readiness.md`                 | Audit of `write_file` compensation requirements.                                    | Automatic `write_file` compensation remains blocked pending authority, preimage, concurrency/version, and reconciliation contracts. |
| `rag-crash-consistency-architecture.md`                | Single-owner RAG persistence, journaling, and recovery design.                      | Core process-crash design has been implemented in `axiom-rag`; host-power-loss guarantees remain explicitly out of scope.           |
| `rag-http-compatibility-contract.md`                   | Caller/server compatibility analysis for HTTP-only RAG storage access.              | Defines the compatibility requirements that led to the versioned RAG HTTP surface.                                                  |
| `rag-http-decision-resolution.md`                      | Resolution of namespace, provider/configuration, and raw-vector/identity authority. | Accepted decision input for the RAG 1.4 HTTP compatibility implementation.                                                          |
| `independent-review-target.md`                          | Bounded reproducible review target for execution and storage evidence.             | Review packet only; it is not independent review, certification, or production evidence.                                           |
| `j-space-research.md`                                  | Falsifiable J-space research program and epistemic boundaries.                      | Research agenda/toy formalization, not evidence about hidden model internals.                                                       |
| `recursive-hyper-optimization.md`                      | Computability-grounded recursive self-optimization analysis.                        | Theory; ordinary APEX execution is not itself recursive hyper-optimization.                                                         |
| `temporal-state-resolution.md`                         | Epistemic latency versus physical/dynamical time.                                   | Conceptual synthesis grounded in stated physical/computational constraints.                                                         |
| `tacon2026-apex-deterministic-execution-contracts.md`  | Diffable transcript of the June 2026 APEX paper.                                    | Historical publication; later source-grounded findings override conflicting implementation descriptions.                            |
| `tacon2026_apex_deterministic_execution_contracts.pdf` | Original June 2026 publication.                                                     | Historical source artifact.                                                                                                         |

## Validated implementation state represented by the research

### ASON → APEX

ASON validates caller-supplied plans against caller-supplied policy and submits
the approved tool sequence to APEX without probabilistic replanning. The current
ASON→APEX path durably binds authorization identity, caller authority reference,
policy digest/reference, and exact approved-plan digest to the APEX run before
dispatch; recovery preserves that binding and rejects substitution. This is
application-level provenance, not cryptographic attestation or independent
human-identity proof. APEX is the
bounded deterministic execution substrate.

The submission boundary is verified. Do not reopen that design question without
contradictory live evidence.

### APEX transactional effects

APEX durably binds an accepted execution plan to its run and records effect
intent before dispatch. Recovery reuses completed results and blocks ambiguous
dispatch states rather than blindly repeating them.

This is conservative process-crash recovery, not an exactly-once external-effect
guarantee.

Automatic `write_file` rollback now fails closed. Safe compensation still
requires explicit owner-approved authority, durable preimage, version/concurrency
safety, forward/inverse ambiguous-outcome reconciliation, and durable inverse
execution.

### RAG durability

`axiom-rag` now implements:

* one cooperating process owner per persistence root;
* one retained Chroma client per root;
* serialized supported access;
* opaque versioned record identities;
* durable replacement intents;
* startup recovery;
* finite-vector validation;
* namespace/embedding-space provenance validation.

These guarantees cover tested process crashes on local Linux filesystems. They
do not establish host-power-loss atomicity across Chroma SQLite/HNSW or protect
against non-cooperating direct Chroma access.

### RAG HTTP compatibility

RAG 1.5.0 unreleased source provides a server-owned versioned compatibility surface:

```text
/v1/inspect
/v1/create
/v1/ingest
/v1/replace
/v1/fetch
/v1/query
/v1/delete
```

and a bounded `rag.http_client.Client` with no retries, redirects, or direct
Chroma fallback.

Namespace authority, provider/configuration ownership, and raw-vector/identity
transport decisions are resolved for the trusted-application scope.

CLI/APEX storage adapters use the HTTP client in the RAG 1.5.0 unreleased source,
under the accepted explicit host-local mapping. Evaluators remain local; the
earlier proposal to migrate their storage is excluded by owner direction.
Validation covers separate-owner callers, caller parity, recovery, and local
Docker Compose RAG/APEX connectivity: service ownership, authentication, HTTP
routing, restart persistence, and portfolio CI. The Compose evidence used dummy
credentials; it does not validate live provider-backed ingest/query, publication,
or a production deployment.

## Interpretation rules

1. Current source and passing tests in the owning repository outrank research
   descriptions of implemented behavior.
2. Source-grounded research is authoritative only for the snapshots/evidence it
   identifies.
3. Architecture proposals remain implementation inputs until code and tests
   demonstrate their invariants.
4. Do not infer deterministic model behavior from deterministic execution
   boundaries.
5. Do not claim exactly-once effects, host-power-loss atomicity, or distributed
   recovery without direct evidence.
6. Preserve unresolved owner decisions explicitly rather than silently choosing
   semantics.
7. Keep speculative research clearly separated from observed implementation
   facts.

## Current priorities

1. Use the integrated CLI/APEX HTTP storage migration as the baseline for
   any separately authorized release or deployment.
2. Keep evaluators local and preserve the explicit mapping and single-owner
   boundary; evaluator HTTP migration remains a separate scope. Treat the local
   Compose integration as validated, not as a production deployment.
3. Keep `write_file` compensation blocked until its authority, inverse/preimage,
   version-safety, and reconciliation contracts are approved.
4. Continue research only when it provides a falsifiable experiment, a durable
   architectural decision, or implementation-relevant evidence.

## Validation

Research Markdown should remain internally consistent and whitespace-clean:

```bash
git diff --check
```

Any implementation claim should additionally be revalidated in its owning
runtime repository.

## Ecosystem

* [AXIOM APEX](https://github.com/axiom-llc/axiom-apex) — deterministic execution runtime.
* [AXIOM ASON](https://github.com/axiom-llc/axiom-ason) — pre-execution policy layer.
* [AXIOM RAG](https://github.com/axiom-llc/axiom-rag) — retrieval/storage subsystem.
* [AXIOM Infra](https://github.com/axiom-llc/axiom-infra) — local integration and portfolio CI.
* [AXIOM Demos](https://github.com/axiom-llc/axiom-demos) — applied integrations.
* [AXIOM API](https://github.com/axiom-llc/axiom-api) — reusable HTTP client base.
* [AXIOM LLC](https://axiom-llc.github.io/) — public project site.
