# AXIOM Research Pipeline

## Purpose

Provide a repeatable manual-model research pipeline for `axiom-director`:

`priority queue -> researcher prompt -> manual model execution -> artifact -> ChatGPT Research-Manager reconciliation -> durable research -> candidate self-improvement`

The pipeline expands structured research context without granting research output implementation authority.

## Roles

- **Claude.researcher** — deep reliability, systems, adversarial architecture, and methodological analysis.
- **Gemini.researcher** — broad literature synthesis, memory/context/state architecture, and comparative systems analysis.
- **ChatGPT.researcher** — compute economics, routing, telemetry, cross-source verification, and AXIOM-specific experimental design.
- **ChatGPT.Research-Manager** — validates provenance, reconciles researcher outputs against current sources and AXIOM authority, removes unsupported precision, extracts durable findings/hypotheses, updates the queue, and routes any proposed system change through existing Director self-optimization authority.

These are workflow roles, not autonomous identities or independent authorities.

## Queue authority

`research-queue.json` is the sole durable research-prompt queue.

Ordering:

1. lower integer `priority`;
2. higher `value_score`;
3. earlier `created_at`;
4. lexical `id`.

Statuses:

`QUEUED -> ISSUED -> COMPLETE`

Exceptional terminal/intermediate statuses: `BLOCKED`, `REJECTED`.

`ISSUED` means Director rendered a prompt for the operator to submit manually. It never means Claude, Gemini, or ChatGPT actually received the prompt.

## Automated R&D lane

A separately admitted Director automation may process only `chatgpt` queue items without manual prompt handoff. It must satisfy the current Director branch/PR write gate before mutation, preserve this queue as the sole research queue, use the same deterministic ordering restricted to eligible `chatgpt` items, and keep WIP to one research item plus at most one directly derived implementation candidate.

Automated work is non-canonical until normal review/integration: research artifacts, queue transitions, code candidates, tests, and documentation live on isolated `automation/rd/<work-id>` branches and may be proposed through pull requests. The automation may not merge its own PRs, release/deploy/publish, spend, send external messages, alter secrets or repository authority, reroute `claude-manual`/`gemini-manual` items, or widen its own admission threshold.

Each automated cycle must prefer current primary sources, preserve uncertainty, independently validate repository effects, measure useful output and friction, and stop at convergence rather than manufacturing work. Repeated evidence may justify a self-improvement proposal to the pipeline itself, but that proposal remains branch/PR-only and cannot self-authorize broader effects.

## `research` cycle

### 1. Select

Read current `axiom-research/main:research-queue.json`, validate the schema, and select the deterministic top `QUEUED` item.

Do not create speculative work merely to keep the pipeline busy. If no material queue item remains, stop with `ACCEPT` and report queue exhaustion.

### 2. Render

Map target:

- `claude-manual` -> Claude.researcher
- `gemini-manual` -> Gemini.researcher in AI Studio
- `chatgpt` -> ChatGPT.researcher

Render one exact, self-contained, copy-ready prompt containing:
- current date;
- repository target `axiom-llc/axiom-research`;
- research question/objective;
- required deliverables;
- queue constraints;
- evidence/provenance requirements;
- instruction to distinguish evidence, synthesis, and hypotheses;
- suggested output filename based on queue ID/title.

The operator manually submits the prompt in a separate model/session.

### 3. Issue state

After rendering, Director may change only that item from `QUEUED` to `ISSUED` and record `issued_at` plus the current Director session ID when available.

This mutation records dispatch preparation, not external delivery.

### 4. Ingest result

When the operator supplies the resulting artifact, `research: ingest <artifact>` invokes ChatGPT.Research-Manager.

Research-Manager must:
1. identify the exact queue item;
2. inspect the complete supplied artifact;
3. refresh decision-critical citations where current verification matters;
4. distinguish primary evidence, preliminary/vendor evidence, synthesis, and speculation;
5. remove or explicitly flag unsupported precision;
6. normalize proposed experiments to current AXIOM execution/cost boundaries;
7. compare against existing `axiom-research` artifacts to avoid duplication;
8. produce the smallest durable research artifact or reconciliation update;
9. mark the queue item `COMPLETE` only after the durable artifact is accepted into `axiom-research`;
10. enqueue follow-up questions only when they independently pass the value/novelty test.

## Self-improvement boundary

Research may identify improvements to Director/APEX/RAG or other AXIOM components. It does **not** self-apply them.

Pipeline:

`research evidence -> Research-Manager reconciliation -> candidate durable lesson -> existing optimize/learn pipeline -> repository-native implementation/validation -> ship/release authority as separately applicable`

No research artifact can grant mutation, commit, push, deployment, publication, spending, or external-effect authority.

Recursive improvement is bounded by:
- fresh evidence;
- semantic deduplication;
- deterministic or practical validation;
- authority separation;
- stop-at-convergence;
- no recursive execution triggered solely by the fact that a prior research/optimization cycle ran.

## Priority policy

Promote prompts that can materially improve:
- validated-work efficiency;
- long-horizon reliability;
- failure detection/recovery;
- memory/state correctness;
- routing/compute allocation;
- evidence quality;
- operator attention cost;
- architecture simplicity.

Reject/deprioritize prompts that are:
- generic surveys with no decision path;
- duplicates of existing research;
- impossible to validate;
- dependent on unavailable paid compute;
- primarily speculative architecture generation;
- unrelated to current AXIOM capability/reliability.

## Output contract

Bare `research` returns only:
- selected queue ID/title/target;
- one copy-ready researcher prompt;
- queue-state effect performed;
- next expected input: the generated artifact.

`research: status` is read-only.

`research: ingest <artifact>` returns:
- item ID;
- Research-Manager classification: `ACCEPT | ACCEPT_WITH_FOLLOWUP | REVISE | REJECT | BLOCKED`;
- durable artifact/state changes actually verified;
- any newly queued follow-up IDs;
- system-improvement candidates routed to `learn`/`optimize`, never silently applied.
## Automation direction

`research-queue.json` remains the single durable pending-research authority. Do not create a parallel `research-pending` queue or repurpose `for-evaluation/` as an editable task queue; `for-evaluation/` is provenance/intake for prompts that have not yet been reconciled into durable research.

The current manual submission step is a capability boundary, not a permanent architecture requirement. When an authorized remote provider/channel exposes the required research capability, is healthy, satisfies the task's evidence requirements, and fits the active incremental-cost ceiling, Director may dispatch a queued item automatically while preserving the same deterministic item identity and state transitions. A failed or ambiguous dispatch must remain explicit; provider memory or task state never becomes canonical.

The target automated lifecycle is:

`research queue -> bounded researcher execution -> Research-Manager reconciliation -> durable evidence -> candidate engineering task -> owning-repository branch/PR -> repository-native validation -> Director classification -> separately authorized merge/release/external effect`

Automation may select, dispatch, retrieve, reconcile, test, and prepare changes within existing authority. Research output must never self-authorize code mutation, merge, release, deployment, spending, publication, credential expansion, or other external effects. Repository protection and approval gates remain authoritative. Do not trigger another research/development cycle solely because the prior cycle completed; require a distinct unresolved question, failed validation, or validated improvement opportunity and stop at convergence.

