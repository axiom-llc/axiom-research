# Claude agent-systems research ingest — 2026-10-02

## Provenance

- Source: Owner-supplied Claude research-results attachment received 2026-10-02.
- Source SHA-256: `d0554c8cb8c58401ff7bf4144e28e42df2962749d54442b736a20c239c007e16`.
- Source size: 163,326 bytes; 3,042 lines.
- Status: model output and cited-source synthesis, not implementation authority and not independent validation.
- Reconciliation rule: source-backed claims, Claude synthesis, sample implementations, self-reported test results, and synthetic examples remain distinct.
- The duplicated validator/evidence section in the supplied output is treated as one result, not two independent confirmations.

## Accepted durable findings

### 1. LLM token-efficiency research

The strongest decision-relevant result is methodological: optimize **cost per successful task**, not tokens per call, and instrument before changing behavior.

Accepted candidate levers, in evidence/ROI order:

1. stable prompt-prefix caching where the provider supports it;
2. concise tool-output projection with handles/pagination instead of injecting large raw payloads;
3. batched stale-observation clearing only after durable state is flushed and a minimum reclaim threshold is met;
4. deferred tool-schema loading when the tool catalog is materially large;
5. deterministic validation followed by model/effort escalation only on validator failure;
6. structured external state/handoff records and just-in-time retrieval;
7. compaction only when masking/projection is insufficient;
8. multi-agent isolation only where parallel breadth or context isolation justifies its coordination/token cost.

Quantitative savings reported by the source are **not accepted as AXIOM performance claims**. Most come from provider documentation, vendor-internal studies, or isolated benchmarks and must be reproduced on AXIOM workloads before promotion.

The source itself identifies unresolved evidence gaps for Codex/Responses compaction, effort-level savings, deterministic-first validation savings, and prompt compression on agent transcripts. Those gaps remain open.

### 2. Remote GitHub execution design

The supplied EXEC / VERIFIER / RELEASE split is directionally consistent with AXIOM's existing remote-only boundary:

- GitHub remains repository authority.
- No local-workstation fallback.
- Mutations are non-force and precondition-bound.
- Unknown write outcomes require read-after-write reconciliation rather than blind retry.
- CI evidence must bind to the exact head SHA.
- Verification should be independent of the actor claiming the effect.
- Release authority should remain separate from implementation authority.
- Durable receipts should identify externally re-fetchable effects.

This is accepted as **research input**, not as a replacement for Director's existing task/receipt/runtime contracts. The sample `rcpt/1` schema and `exec.py` implementation are proposals only.

### 3. Human-input gateway findings

The current Director human-input gateway remains canonical. Claude's gateway contributes useful candidate controls:

- destination and authorization scopes come from a trusted envelope, never from the text being parsed;
- quoted/source material should be explicitly inert data;
- normalization/rewrites should be auditable;
- malformed structured input should fail closed;
- ambiguous consequential authorization should not silently pass.

The supplied implementation is **not adopted wholesale**. Its fixed risky-verb lexicon and regex-based semantic checks are intentionally limited, create false-positive/false-negative risk, and overlap an existing Director-owned contract. Claude's reported `35/35` test result is self-reported model evidence, not independently reproduced AXIOM validation.

### 4. Validation/evidence protocol

Accepted research principles:

- separate non-deterministic collectors from a deterministic validator core;
- bind evidence to immutable subjects such as commit/artifact digests;
- pin check definitions so the change under test cannot silently redefine its own validator;
- rank evidence by provenance/independence;
- never allow executor/model assertions to substitute for required independently verifiable evidence;
- keep `UNKNOWN` explicit rather than coercing it to pass;
- evaluate implementation and release claims separately.

The supplied schema/reference validator is a design proposal. It is not an implemented AXIOM validator until an owning runtime adopts and tests it.

### 5. Workflow benchmark methodology

Accepted methodological direction:

- benchmark a complete workflow cell `(model@version, harness, tool_profile, prompt_adapter)`, not a model name in isolation;
- maintain both controlled-tooling and provider-native tracks;
- use immutable task packs, deterministic oracles, protected-state checks, and append-only traces;
- report capability coverage separately from failures;
- report multiple dimensions rather than hiding tradeoffs in one weighted score;
- use repeated runs and confidence intervals;
- separate infrastructure failures from model/workflow failures while still reporting the infrastructure-failure rate;
- verify completion claims against executed evidence.

The example benchmark numbers in the supplied output are explicitly synthetic and are not evidence.

## Bibliography status

Claude supplied a bibliography spanning Anthropic prompt caching/context management/effort/pricing/tooling material, OpenAI prompt caching, Gemini context caching, Context Rot, RouteLLM, FrugalGPT, LLMLingua, and related work.

This ingest preserves that provenance classification but does not claim an independent revalidation of every citation or numerical result. Any quantitative AXIOM claim must be tied to the exact underlying source or reproduced by an AXIOM benchmark.

## Canonical reconciliation

- **Research authority:** this file records the accepted research-level findings and limitations.
- **Director implementation authority:** existing `modules/execution_telemetry.py`, `modules/telemetry_store.py`, `modules/human_input.py`, remote-execution modules, and their tests remain canonical for implemented behavior.
- **Architecture authority:** no new architecture version is justified. The research largely strengthens existing remote-only, explicit-authority, provenance, and verification principles.
- **No implementation claim:** none of Claude's sample code is considered shipped AXIOM code merely because it appeared in the supplied result.

## Smallest high-ROI follow-up

Before applying any token-reduction technique, perform a bounded **token-efficiency telemetry baseline** in `axiom-director`.

Required outcome:

1. audit the existing execution telemetry against the measurement fields needed to compute cost per successful task and distinguish provider-reported token classes;
2. add only the minimum missing provider-neutral fields/derived metrics needed for reliable baseline measurement, preserving backwards compatibility;
3. add deterministic tests for aggregation, zero-success handling, retries, and persisted telemetry;
4. do **not** add prompt caching, masking, compaction, tool truncation, or model routing changes in the same task;
5. run the existing Director test suite and report the exact changed files, test result, and any fields that remain unavailable from current providers.

Promotion gate: the telemetry baseline must pass existing tests and make no routing/behavioral change. Only after baseline evidence exists should one optimization lever be tested at a time.
