# Causal and Temporal Memory for Persistent Agents

**Date:** 2026-10-03  
**Author channel:** Gemini (AI Studio), reconciled by AXIOM  
**Target:** `axiom-llc/axiom-research`

## Provenance

- Owner-supplied transport/source SHA-256: `cfd56ae7e84a8086890a7de36d113bf68af5269723c0e1c650e2988f678a037b`.
- The supplied artifact mixed useful architectural synthesis with several highly specific 2026 benchmark names/numbers and an immediate recommendation for a bitemporal event-sourced ledger.
- AXIOM refreshed decision-critical sources, removed claims that could not be independently resolved, corrected paper identifiers, and downgraded architecture prescriptions to testable hypotheses.
- This file is a **reconciled research ingest**, not a verbatim copy and not implementation authority.

Evidence labels: **[E]** established/widely corroborated · **[P]** primary but preliminary/single-study/vendor-originated · **[S]** synthesis · **[H]** hypothesis.

## Research Question

What memory architecture best supports persistent autonomous agents when correctness depends on causality, provenance, temporal validity, contradiction resolution, and selective forgetting rather than semantic similarity alone?

## Executive Findings

1. **[E/S] Semantic similarity and temporal validity are different problems.** Vector retrieval remains useful for semantic discovery, but cosine similarity does not by itself determine which of two contradictory assertions is currently authoritative.
2. **[P] MemStrata provides direct 2026 evidence for deterministic supersession.** On its evaluated evolving-knowledge benchmarks, cosine similarity distinguishes contradiction from duplicate at AUROC 0.59; RAG serves stale values 15–40% of the time when forced to answer, while its deterministic temporal-validity layer reduces the stale-fact error to approximately zero in that benchmark.
3. **[P] Long-term memory benchmarks continue to expose invalid-memory reuse.** Memora introduces Forgetting-Aware Memory Accuracy (FAMA) and reports that contemporary memory agents provide only marginal improvement on forgetting-aware tasks.
4. **[P/S] Event sourcing is promising mainly for replay, provenance, and recovery, not because it has been proven universally superior for agent memory.** ESAA and PROJECTMEM provide current examples, but the evidence base is still limited and system-specific.
5. **[P] Graph and causal-memory approaches are credible alternatives, not established defaults.** Zep/Graphiti, ActMem, and related work show benefits in their tested settings; they also add extraction, storage, and reasoning complexity.
6. **[P] Explicit addressable external state can reduce dependence on raw history.** ARC reports high recall under compaction by storing tool observations in an append-only addressable log; 2026 reasoning-compression work likewise finds that historical reasoning becomes more replaceable after task-relevant state has been externalized.
7. **[S] AXIOM should test the smallest temporal/supersession extension to its existing structured state before considering a graph database, global causal DAG, or full event-sourced redesign.**

## Memory Taxonomy

### Functional roles

- **Working memory:** volatile active context, current plan, recent observations.
- **Episodic memory:** dated execution/events with high provenance and detail.
- **Semantic/current-state memory:** compact assertions intended to represent current truth.
- **Procedural memory:** executable rules, schemas, runbooks, tool contracts.

### Storage/retrieval substrates

| Substrate | Strength | Principal risk |
|---|---|---|
| Long context only | simple, no external retrieval | context dilution, truncation, stale-history coexistence |
| Vector retrieval | semantic/fuzzy discovery | similarity does not encode current validity |
| Structured relational state | deterministic current-state queries | schema/maintenance burden |
| Event log | replay/provenance/history | write volume and projection complexity |
| Temporal/bitemporal state | explicit validity and supersession | additional schema semantics |
| Knowledge/temporal graph | relationships and multi-hop retrieval | extraction/graph-maintenance overhead |
| Causal graph | explicit dependency reasoning | hallucinated/incorrect edges; causal discovery cost |
| Hybrid | combines semantic discovery with authoritative state | synchronization and authority ambiguity |

## Memory Lifecycle

A durable memory system should make these operations explicit:

`observe → admit/write → encode → retrieve → reason → update → invalidate → consolidate → forget`

The key distinction for AXIOM is **authority**:

- semantic retrieval can propose relevant evidence;
- authoritative structured state should determine current operational facts where a schema exists;
- superseded records may remain available for audit/history without being eligible as current state;
- derived summaries should retain provenance and invalidation links.

## Current Evidence

### Temporal validity and stale facts

Yadav, *Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge* (arXiv:2606.26511), introduces MemStrata. In its controlled evolving-knowledge benchmarks:

- contradiction-vs-duplicate discrimination by cosine similarity is AUROC 0.59;
- temporal retrieval reaches 0.95–1.00 answer accuracy versus RAG 0.20–0.47 on the evaluated evolving tasks;
- forced-answer RAG returns the superseded value 15–40% of the time;
- deterministic supersession drives that benchmark's stale-fact error to approximately zero.

These results are **single-author/preprint evidence** and should not be generalized directly to AXIOM production workloads.

### Long-term forgetting

*Memora: A Comprehensive Benchmark for Long-Term Memory in Agents* (arXiv:2604.20006; Findings of ACL 2026) evaluates long-term memory and introduces FAMA, which penalizes reuse of obsolete/deleted memories. The paper reports frequent invalid-memory reuse and only marginal improvement from existing memory agents. **[P]**

### Event-oriented memory

- *Event Sourcing for Autonomous AI Agents (ESAA)* (arXiv:2602.23193) applies append-only event sourcing and projections to autonomous-agent state. It supports the plausibility of event-oriented state management, not a universal superiority claim. **[P]**
- *PROJECTMEM* (arXiv:2606.12329, revised 2026-09-30) reports a six-month author-run project-memory system with 3,228 events across 27 projects. This is useful feasibility evidence but not controlled proof of improved reliability. **[P]**

### Graph and causal memory

- *Zep: A Temporal Knowledge Graph Architecture for Agent Memory* (arXiv:2501.13956) reports improvements over several baselines on conversational-memory benchmarks. Because the work is vendor-originated and the benchmark conditions differ from AXIOM's structured systems tasks, treat quantitative claims as **[P]**.
- *ActMem* (arXiv:2603.00026) studies causal/semantic graph memory and counterfactual reasoning. It supports causal structure as a research direction, not an authorization to build a global causal DAG. **[P]**

### Context externalization

- *Addressable Recall Compaction for Long Context-Window Control in AI Agents* (ARC, arXiv:2607.25066) stores older tool observations in an ID-addressable append-only log and reports 99.40% exact-answer accuracy on its needle evaluation versus 88.12% for the best baseline in that experiment; LongBench-v2 Hard gains are smaller (29.97% versus 28.25%). **[P]**
- *When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression* (arXiv:2609.29875) reports that historical reasoning becomes more safely removable after task-relevant derived state is externalized into reliable artifacts/tool outputs. **[P]**

## Similarity Retrieval: Strengths and Limits

Vector retrieval is well-suited for:

- locating semantically related prior material;
- fuzzy discovery over unstructured research;
- code/text similarity;
- candidate evidence retrieval before validation.

It should not by itself decide:

- which configuration value is current;
- whether an instruction was revoked;
- which task state supersedes another;
- whether an external effect completed;
- which authority wins when records conflict.

The failure is not that embeddings are useless; it is that **semantic proximity is not a temporal-validity contract**.

## Structured State, Events, and Temporal Semantics

AXIOM's current structured-state approach should remain the baseline.

The smallest useful extension to test is not a new graph database. It is explicit supersession metadata for state classes that actually exhibit stale-value failures, for example:

`scope, entity, attribute, value, valid_from, valid_to, source_ref, superseded_by`

Optional event provenance could add:

`event_id, parent_event_id, observed_at, actor, payload_ref`

These are **research candidates**. They should not be generalized to every AXIOM fact or action unless measurement demonstrates value.

## Contradiction and Invalidation

Prefer deterministic invalidation where the domain defines a single authoritative slot, revision, or state transition.

Potential rules:

1. if a new authoritative observation supersedes the same scoped state slot, close the old validity interval;
2. retain the old observation for audit/history;
3. exclude invalidated rows from “current truth” retrieval;
4. preserve provenance to the exact source/event;
5. require explicit uncertainty when two observations cannot be deterministically ordered.

Do not force a deterministic slot model onto inherently multi-valued or disputed facts.

## Consolidation and Forgetting

For technical agent state, continuous age-based decay is a poor universal default because some old invariants remain valid while recent scratch data can become irrelevant immediately.

Prefer:

- explicit supersession for changed facts;
- TTL only for classes with real expiry semantics;
- compaction of redundant history after authoritative state is externalized;
- retention of enough provenance to reconstruct why the current state exists;
- hard deletion where privacy/legal requirements demand it.

The original Gemini draft cited `MemDecay-Bench` and `DRIFTBENCH` with precise figures. Those claims were **removed** because the refresh did not establish a sufficiently reliable primary-source basis for them.

## Cost and Complexity Tradeoffs

| Approach | Correctness potential | Complexity | AXIOM interpretation |
|---|---:|---:|---|
| Current structured state | high for schematized current facts | low-moderate | **baseline** |
| Add supersession/validity fields | higher for evolving single-valued facts | moderate | first treatment to test |
| Append-only event provenance | replay/audit benefits | moderate | test only where recovery/debugging needs it |
| Temporal/knowledge graph | useful multi-hop relationships | high | no adoption without measured gain |
| Global causal DAG | potentially rich explanation | very high | reject by default; local causal links only if justified |
| Flat vector memory as authority | weak temporal correctness | low-moderate | use for discovery, not operational authority |
| Hybrid | potentially strongest | highest coordination burden | require explicit authority boundaries |

## Implications for AXIOM

1. Preserve repository-backed/structured authority.
2. Add temporal semantics only where stale-current-state errors are observed or the MVE shows benefit.
3. Keep semantic retrieval as a discovery layer, not the arbiter of current state.
4. Prefer local parent/provenance links over unconstrained global causal discovery.
5. Do **not** deploy Neo4j/Memgraph or a standalone temporal graph from this research alone.
6. Do **not** replace existing Director state with a “BESL” architecture without experimental evidence.
7. Treat source precision as part of memory quality: unsupported research claims must not become canonical architecture facts.

## Testable Hypotheses

- **H1 [H]** Explicit supersession reduces stale-state errors relative to in-place/unversioned retrieval on rapidly changing technical state.
- **H2 [H]** Semantic similarity alone cannot reliably classify active-versus-superseded contradictory assertions.
- **H3 [H]** Adding validity metadata to the existing relational state yields most of the stale-fact benefit without requiring a graph database.
- **H4 [H]** Parent-event provenance improves root-cause traceability after compaction/handoff.
- **H5 [H]** Addressable externalized tool state reduces repeated retrieval/tool execution compared with retaining raw observations in active context.
- **H6 [H]** Discrete invalidation outperforms generic time decay on technical invariants whose validity changes by explicit update.
- **H7 [H]** A temporal graph does not improve validated AXIOM task completion enough to justify its operational overhead relative to relational temporal state.
- **H8 [H]** Historical reasoning can be compacted more aggressively once all task-relevant derived state is durably externalized.

## Minimum Viable Experiment

**Goal:** determine whether minimal temporal/supersession structure materially outperforms AXIOM's existing structured-state baseline before any architecture expansion.

### Conditions

- **A — current AXIOM baseline:** current structured state semantics.
- **B — temporal treatment:** same storage substrate plus explicit validity/supersession fields and deterministic current-state filtering.
- **C — optional semantic-retrieval baseline:** only if an existing zero-cost remote path is already available; do not add infrastructure merely for the experiment.

### Workload

Create a synthetic remote fixture containing deterministic state changes:

- configuration flips;
- API/function renames;
- dependency/version changes;
- corrected diagnoses/root causes;
- rollback/reversion events.

Grade:

- current-state accuracy;
- stale-fact error rate;
- contradiction/invalidation correctness;
- provenance traceability;
- retrieval/processing latency;
- tokens/tool calls where applicable;
- implementation/maintenance complexity.

### Execution boundary

Run only through **ChatGPT session-hosted Python/SQLite or GitHub Actions/other already-authorized remote compute**. Do not execute on the Owner workstation or use local clones. Incremental hosted spend must remain **$0.00**.

### Decision gate

Reject additional temporal/event machinery if the current baseline matches the treatment within the pre-registered practical margin. If the treatment wins, promote only the smallest field/transition set required by the observed failure class. A graph database or global causal layer requires a separate experiment.

## Open Questions

- Which AXIOM state classes are actually vulnerable to stale-value retrieval?
- How often does source time differ materially from validity time?
- Can deterministic domain keys resolve supersession without an LLM extraction step?
- What event granularity provides useful replay without write amplification?
- How should uncertain/conflicting observations coexist?
- At what scale does a graph representation outperform relational indexes on AXIOM workloads?
- How much context can be removed safely after state externalization?

## References

Primary/current sources refreshed 2026-10-03:

- Yadav. *Temporal Validity in Retrieval Memory: Eliminating Stale-Fact Errors for AI Agents over Evolving Knowledge.* arXiv:2606.26511 (2026). https://arxiv.org/abs/2606.26511
- *Memora: A Comprehensive Benchmark for Long-Term Memory in Agents.* arXiv:2604.20006; Findings of ACL 2026. https://arxiv.org/abs/2604.20006
- *Event Sourcing for Autonomous AI Agents (ESAA).* arXiv:2602.23193 (2026). https://arxiv.org/abs/2602.23193
- *PROJECTMEM.* arXiv:2606.12329 (2026; revised 2026-09-30). https://arxiv.org/abs/2606.12329
- *ActMem.* arXiv:2603.00026 (2026). https://arxiv.org/abs/2603.00026
- Rasmussen et al. *Zep: A Temporal Knowledge Graph Architecture for Agent Memory.* arXiv:2501.13956 (2025). https://arxiv.org/abs/2501.13956
- Wu et al. *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory.* arXiv:2410.10813. https://arxiv.org/abs/2410.10813
- *Addressable Recall Compaction for Long Context-Window Control in AI Agents.* arXiv:2607.25066 (2026). https://arxiv.org/abs/2607.25066
- *When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression.* arXiv:2609.29875 (2026). https://arxiv.org/abs/2609.29875

## Reconciliation Result

**REVISE → ACCEPT_WITH_FOLLOWUP.** The memory research is retained after citation repair and removal of unsupported precision. The architecture recommendation is narrowed to an experiment: **measure minimal temporal/supersession semantics against current structured state before adding event-sourcing or graph complexity.**
