# 1. Final canonical architecture

# AXIOM

## Hybrid Human–Machine Operating Architecture

**Status:** canonical target architecture under current validated evidence; implementation remains incremental.

**Objective:** maximize expected **portfolio net global value** subject to hard constraints, authority, consent, evidence, and explicit resource budgets:

```text
maximize E[
  outcome value
  + future option value
  - human attention cost
  - latency
  - tokens / compute
  - cash cost
  - operational downside
  - opportunity cost
  - maintenance burden
]
```

Do not force false numerical precision. Apply hard constraints and priority classes first; use measured expected value and Pareto dominance where defensible.

Global value includes revenue, capital, stability, time, deadline avoidance, risk reduction, strategic leverage, reusable infrastructure, knowledge, automation, and future action potential. Existing components and decisions remain only while justified.

## Architecture

```text
                         OWNER / OPERATOR
                  goals · consent · judgment
                  identity · physical action
                             ⇅
                        DIRECTOR AGENT
                    operator/cognitive interface
                             ⇅
                        DIRECTOR CORE
                    strategic control plane
               objectives · priority · constraints
                             │
                         WorkIntent
                             ▼
                           HARNESS
                  logical operational control
             tasks · scheduling · resources
             attempts · acceptance · receipts
                             │
                    ExecutionAssignment
                 ┌───────────┼───────────┐
                 ▼           ▼           ▼
          DETERMINISTIC     APEX        HUMAN
            EXECUTOR      EXECUTOR     EXECUTOR
                             │
                  validated execution plan
                             │
                 authorization required?
                        │          │
                       no         yes
                        │          ▼
                        │         ASON
                        │    exact-plan policy
                        │          │
                        └──────────┤
                                   ▼
                             APEX execution
                                   │
                         run/effect ledger
                                   ▼
                         candidate + evidence
                                   ▼
                              ACCEPTANCE
                                   ▼
                         canonical task commit
                                   ▼
                         CompletionReceipt
                                   ▼
                           DIRECTOR UPDATE
```

RAG, Infra, Ops, API, Research, model providers, compute accounts, and external host harnesses support this path; none constitutes an additional control plane.

## Authority

| Component | Authoritative responsibility |
| --- | --- |
| Owner/Operator | goals, consent, identity, subjective judgment, physical action, final authority |
| Director Agent | operator communication, intent interpretation, direct cognitive work |
| Director Core | strategic objectives, priorities, constraints, portfolio state |
| Harness | task lifecycle, scheduling, resources, cross-executor attempts, acceptance, canonical completion |
| Deterministic executor | locally provable computation or transformation |
| APEX | bounded machine execution, plan validation/execution, run/effect state, recovery and replay |
| Human executor | irreducibly human work and evidence |
| ASON | pre-execution authorization of an exact APEX plan when policy requires |
| RAG | semantic knowledge and server-owned retrieval/storage state |
| Infra | cross-repository integration and contract validation |
| Ops | bounded deterministic operational utilities |
| API | reusable HTTP transport utility |
| Research | evidence, falsification, benchmarks, validation records, durable architectural research |

One fact has one authoritative owner. Higher layers hold references, summaries, or interpretations rather than duplicate lower-layer state.

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
25. `INV-025` — Autonomy increases only from evidence.
26. `INV-026` — Optimize valuable autonomous progress, not automation depth.
27. `INV-027` — A model endpoint responding successfully does **not** establish APEX compatibility; acceptance requires workload-level validation.
28. `INV-028` — Provider/model/context/host configuration is part of the execution profile and cannot be generalized across materially different configurations.
29. `INV-029` — Unverified quota or free allowance is not spendable capacity.
30. `INV-030` — No provider fallback may silently incur cash cost, weaken sensitivity constraints, or cross an authorization boundary.
31. `INV-031` — External coding/agent harnesses do not acquire AXIOM task authority merely by launching or invoking APEX.
32. `INV-032` — Prefer direct APEX execution before adding nested host-harness orchestration.
33. `INV-033` — Account-specific usage and pricing must be verified before assigning nonzero spend capacity.

Current APEX already implements plan generation, schema validation, bounded execution, durable run/effect state, recovery/replay, tools, HTTP/MCP surfaces, and exact-plan execution; treating it merely as a consequential-effect endpoint would duplicate its implemented role.

## Director

### Director Agent

Classify incoming work:

```text
ephemeral cognitive    → perform directly
strategic              → Director Core
persistent operational → Harness
```

Direct execution remains valid when durable orchestration adds no material value.

### Director Core

```text
WorkIntent
  intent_id: string
  objective: non-empty string
  priority_class: P0 | P1 | P2 | P3 | P4 | P5
  hard_constraints: structured object
  required_outcome: non-empty string
  evidence_requirements: list[string]
  context_refs: list[string]
```

Priority:

```text
P0  immediate safety / critical continuity / imminent irreversible risk
P1  hard deadline / required dependency
P2  direct revenue / capital / high-value opportunity
P3  high-leverage infrastructure / automation / research
P4  routine maintenance / optimization
P5  optional improvement
```

Classes outrank speculative numerical scoring. Within a class, rank by defensible expected portfolio value.

## Harness

Harness is the **durable operational orchestration boundary**, implemented by the validated private `axiom-harness` repository when persistence has material value.

It owns:

```text
task specification
task mutable state
resource state
scheduling / leases
cross-executor attempts
acceptance
canonical results
completion receipts
operational events
```

It must not duplicate APEX's internal run/effect journal.

### Task specification

```text
TaskSpec
  task_id: immutable string
  intent_ref: string
  domain: string
  priority_class: P0 | P1 | P2 | P3 | P4 | P5
  deadline: timestamp | null
  execution_window: interval | null
  autonomy_class:
    AUTO | AUTO_NOTIFY | APPROVAL_REQUIRED |
    HUMAN_ASSISTED | HUMAN_ONLY | MONITOR
  capability_requirements: list[string]
  sensitivity_class: policy-defined enum
  mutation_class: M0 | M1 | M2 | M3 | M4
  cash_ceiling: non-negative number
  token_budget: non-negative integer | null
  context_budget: non-negative integer | null
  retry_budget: non-negative integer | null
  human_time_budget_minutes: non-negative integer | null
  context_refs: list[string]
  acceptance_contract: structured object
  dependency_refs: list[string]
```

`TaskSpec` is immutable.

```text
TaskState
  task_id: string
  state:
    PENDING | BLOCKED | READY | LEASED | RUNNING |
    UNKNOWN | FAILED | COMMITTED | CANCELLED
  active_lease_ref: string | null
  canonical_result_ref: string | null
  updated_at: timestamp
```

### Attempts

```text
AttemptRecord
  attempt_id: string
  task_id: string
  resource_id: string
  lease_id: string | null
  context_pack_hash: digest
  executor_run_ref: string | null
  authorization_refs: list[string]
  outcome: FAILED | REJECTED | UNKNOWN | ACCEPTED
  result_ref: string | null
  evidence_refs: list[string]
  retry_safe: boolean
  started_at: timestamp
  completed_at: timestamp | null
```

A retry is a new attempt.

`UNKNOWN` suspends automatic retry until reconciliation establishes safety.

Acceptance and canonical commit are separate. At most one result becomes canonical.

### Resources

```text
ResourceSpec
  resource_id
  capabilities
  maximum_mutation_class
  cost_class
  hard_zero_spend_eligible
  context_limits
  reasoning_tiers
  failure_semantics
  timeout_behavior
  account_ref: string | null

ResourceState
  resource_id
  availability
  quota
  rate_limits
  free_allowance
  current_usage
  billing_period
  hard_spend_ceiling
  pricing_ref
  cooldown
  authentication_readiness
  last_verification
```

Human execution is a resource.

Account, quota, pricing, and usage fields are operational facts, not estimates. Unknown values remain unknown.

For an unaudited account such as `gxy`, `hard_spend_ceiling = 0` until service identity, pricing, current usage, allowance, limits, and billing behavior are verified and a nonzero ceiling is explicitly approved.

### Routing

```text
1. Eliminate resources violating authority or hard constraints.
2. Reuse a valid accepted result/cache when permitted.
3. Prefer deterministic local computation when sufficient.
4. Enforce cash, sensitivity, mutation, capability, quota, and context limits.
5. Eliminate any resource whose required spend is unknown or exceeds its verified envelope.
6. Rank remaining resources by evidence-backed expected accepted net value.
7. Prefer lower cost/latency when outcome value is materially equivalent.
8. Use one executor unless parallelism/redundancy has measured positive value.
9. Queue or block when no compliant executor exists.
```

Availability never overrides authority, safety, or budget.

## APEX and ASON

APEX is the canonical bounded machine execution substrate. Current implementation supports schema-validated plans, bounded execution, replay, persistent run/effect state, recovery, tool execution, CLI/HTTP/MCP interfaces, and orchestration.

ASON selectively governs exact plans before APEX execution.

### Mutation policy

```text
M0  read-only / reasoning
M1  local reversible mutation
M2  external reversible mutation
M3  consequential external mutation
M4  irreversible, safety-critical, or highly sensitive mutation
```

Default:

```text
M0 → eligible executor
M1 → Harness policy
M2 → Harness/domain policy; ASON when required
M3 → exact plan + ASON; human approval when authority requires
M4 → human authorization mandatory + exact-plan ASON validation
```

For authorization-required APEX execution:

```text
authorization_id
approved_plan_digest
policy_digest_or_ref
authority_ref
decision
```

Current ASON generates a unique authorization identity plus caller-supplied authority reference, policy digest/reference, and exact approved-plan digest. Current APEX validates that binding and atomically persists it with the run/effect ledger before tool dispatch. Recovery reuses the durable binding and rejects substitution. This establishes durable application-level authorization provenance for the recorded run; it does not establish cryptographic attestation, independent human-identity verification, or exactly-once external effects.

APEX recovery remains conservative: ambiguous dispatch blocks replay; it does not establish exactly-once external effects.

## APEX compute and provider architecture

APEX currently exposes a provider abstraction with native `gemini` and `ollama` selection. Ollama uses the native `/api/generate` interface with configurable endpoint/model and a single 300-second request attempt.

Treat planning compute separately from execution authority:

```text
task / exact plan
      │
      ├─ exact validated plan available
      │      └─→ APEX validation/execution
      │
      └─ plan generation required
             │
             ├─ native APEX provider
             │      ├─ local Ollama
             │      └─ verified hosted provider
             │
             └─ external host harness/model
                    └─ exact plan or subordinate APEX invocation
```

Provider selection policy:

```text
1. Reuse an already-authorized exact plan when applicable.
2. Prefer a validated local Ollama profile when it satisfies acceptance.
3. Prefer verified already-available zero-spend hosted capacity.
4. Use paid capacity only within an explicit account and task spend envelope.
5. Never perform hidden paid fallback.
6. Do not promote a model/profile from experimental to production without benchmark evidence.
```

A model profile is identified by at least:

```text
APEX revision
provider
model
endpoint
model/runtime version
context configuration
host
relevant generation settings
tool registry/config digest
```

Changing a material field invalidates benchmark equivalence.

### Local Ollama

The current APEX provider contract matches Ollama's documented non-streaming `/api/generate` response fields `response`, `prompt_eval_count`, and `eval_count`. Ollama additionally exposes load, prompt-evaluation, and generation durations suitable for throughput analysis.

Local-model acceptance must measure:

```text
plan parse/schema success
tool-selection correctness
task pass rate
failure behavior
wall latency
prompt/output tokens
generation throughput
memory/compute observations when available
stability across repeated runs
```

Do not infer that Gemma or Qwen is APEX-capable from a successful raw completion alone.

Current unit tests verify Ollama's single-attempt redacted failure behavior but do not provide a live Ollama success/compatibility test.

The existing benchmark already executes real APEX tasks and records pass rate, wall time, token count, and a bounded composite score; its current workload contains file, shell, memory, HTTP, and multi-step cases.

Model-specific live validation is operational evidence, not architecture. Record it in Research status/artifacts with the exact execution profile and authorization boundary. A rejected or unapproved profile must not be re-queued merely because the endpoint remains available; repeat testing requires a new material hypothesis and applicable explicit authorization.

## `gxy` account policy

`gxy` is an account/resource boundary, not an architectural component.

Audit before use:

```text
service/provider identity
authenticated account identity
available models/services
quota
rate limits
free allowances
billing state
pricing
current-period usage
reset/billing period
overage behavior
terms/eligibility constraints
APEX configuration mapping
```

The resulting monthly envelope must distinguish:

```text
verified no-cash capacity
verified paid capacity
current consumption
remaining capacity
hard approved spend ceiling
unknown/unavailable values
```

Until that audit is completed:

```text
incremental cash ceiling = $0
paid overage = disabled/not authorized
billing activation = not authorized
automatic migration = prohibited
unverified quota = unusable for routing
```

No public or accessible repository evidence identifies `gxy` as an APEX-native configuration key; current APEX configuration exposes provider/model credentials and endpoints rather than named account profiles.

## External host harnesses

Use **host harness** for external coding-agent environments such as `codex`, `agy`, and `opencode`. This is distinct from the AXIOM **Harness**.

Canonical rule:

```text
host harness
    ↓
subordinate invocation / development environment
    ↓
APEX
    ↓
validated bounded execution
```

A host harness may:

```text
invoke APEX CLI
call the APEX HTTP interface
connect through an existing compatible protocol
prepare inputs or inspect results
perform development/testing around APEX
```

It must not silently become authoritative for AXIOM scheduling, canonical completion, authorization, or APEX recovery state.

Prefer existing APEX CLI/HTTP/MCP surfaces over creating a `codex`, `agy`, or `opencode` adapter. Create an adapter only after repeated workloads demonstrate measurable value that existing interfaces cannot provide.

Avoid default nested-agent execution:

```text
host harness → APEX → model → tools
```

when direct:

```text
APEX → model → tools
```

achieves the same accepted result more cheaply or reliably.

### Codex

Ollama currently documents direct Codex integration and recommends a large context window; this makes Codex a valid host-harness experiment but does not establish compatibility with the current local APEX model profiles.

### OpenCode

Ollama and OpenCode document local Ollama integration. OpenCode likewise warns that tool use may require substantially larger context windows.

### AGY

Google's Antigravity CLI (`agy`) is itself an agent harness with shell/tool execution capabilities and is therefore a plausible APEX host environment. No APEX-specific integration is presently validated.

Host-harness promotion requires measured improvement in at least one of:

```text
accepted-result quality
capability
reliability
automation
compute utilization
latency
human attention
cash efficiency
```

with no unacceptable increase in state duplication, authority ambiguity, failure modes, or maintenance burden.

## APEX validation evidence

Store validation results as Research artifacts rather than new runtime authority:

```text
ApexValidationRecord
  apex_revision
  provider
  model
  endpoint_ref
  account_ref
  host_harness
  config_digest
  workload_ref
  command
  pass_rate
  wall_time
  token_metrics
  throughput_metrics
  resource_observations
  cash_cost
  failures
  limitations
  result: ACCEPT | REJECT | EXPERIMENTAL
  verified_at
```

A profile is `ACCEPT` only when it satisfies the workload's acceptance contract.

`EXPERIMENTAL` capacity may be used for non-authoritative testing but must not silently replace a validated production path.

## Context

```text
GLOBAL KNOWLEDGE
      ↓
DOMAIN STATE
      ↓
TASK CONTEXT
      ↓
ContextPack
      ↓
exact execution inputs
      ↓
runtime state
```

```text
ContextPack
  task_id: string
  objective: non-empty string
  hard_constraints: list[constraint]
  acceptance_contract: structured object
  authoritative_state: structured object
  source_refs: list[string]
  required_source_excerpts: list[source excerpt]
  resource_constraints: structured object
  prior_relevant_receipts: list[string]
```

Compilation:

```text
exact structured state
→ authoritative references
→ accepted receipts/cache
→ deterministic filtering
→ targeted exact retrieval
→ semantic retrieval
→ model summarization only when necessary
```

Equivalent authoritative input should yield reusable content-addressed context where practical.

Optimize accepted outcomes, reuse, cache hits, retry overhead, token usage, latency, and human minutes—not context volume.

## Acceptance and receipts

Executors never canonically complete tasks.

```text
executor → CandidateResult + evidence
ASON     → authorization decision
APEX     → machine run/effect evidence
Harness  → acceptance → canonical commit
Director → strategic state update
```

```text
CompletionReceipt
  task_id: string
  result_ref: string
  evidence_refs: list[string]
  artifact_hashes: map[string, digest]
  limitations: list[string]
  executor: string
  attempt_id: string | null
  committed_at: timestamp
```

Failed, rejected, and unknown attempts remain attempts.

Acceptance should be deterministic where the contract permits it. Subjective or probabilistic contracts must name the authorized verifier and evidence rather than pretending determinism.

Do not create a shared contracts repository until independent consumers demonstrate persistent costly duplication.

## RAG

RAG is a supporting knowledge/storage subsystem, not a control plane.

Keep exact operational state outside semantic retrieval when a structured authoritative store exists.

## Events and human interruption

```text
event
  ↓
deterministic classification
  ├─ operational-only → Harness
  └─ strategic impact → Director
```

Prefer native events or bounded scheduled checks over generalized polling.

Human interruption is limited to:

```text
ACTION     irreducible manual/physical work
DECISION   subjective judgment/preference
APPROVAL   consequential authorization
EXCEPTION  safe automation cannot continue
```

Information alone should normally be recorded or batched.

## State ownership

```text
Director
  objectives · opportunities · strategic constraints
  compact summaries · decisions · completion refs

Harness
  TaskSpec · TaskState · resources · leases
  attempts · acceptance · canonical task results

APEX
  execution plans · provider configuration
  run state · tool/effect dispatch state
  recovery evidence · machine execution results

RAG
  long-form knowledge · semantic retrieval state

Research
  benchmark evidence · validation matrices
  architecture/falsification artifacts
```

Preferred future private local layout:

```text
~/.config/axiom/       non-secret configuration
~/.local/state/axiom/  mutable structured state
~/.local/share/axiom/  durable private artifacts / receipts
~/.cache/axiom/        reproducible caches / ContextPacks
```

Credentials, provider secrets, and private account state require appropriate secret storage and must not be committed into these repositories.

Preserve existing validated layouts until migration demonstrates greater net value.

## Repository topology

| Repository | Canonical disposition |
| --- | --- |
| `axiom-director` | strategic control |
| `axiom-harness` | private durable operational orchestration core; use only when persistence has material value |
| `axiom-apex` | canonical bounded machine execution runtime |
| `axiom-ason` | selective exact-plan pre-execution policy layer |
| `axiom-rag` | canonical retrieval/storage subsystem |
| `axiom-infra` | integration and portfolio validation |
| `axiom-ops` | bounded deterministic operations utilities |
| `axiom-research` | durable evidence, validation, architecture and falsification workspace |
| `axiom-api` | reusable HTTP transport utility; not a control plane |
| `axiom-blender` | applied domain system |
| `axiom-demos` | examples/prototypes while useful |
| `axiom-llc.github.io` | public presentation |
| `reward-harness` | empirical input to Harness promotion |

Provider accounts, local models, Codex, AGY, and OpenCode do **not** justify repositories merely by existing.

Domains remain data/policy/application scopes unless reusable software independently justifies a repository.

Do not pre-create repositories for planning, evaluation, routing, providers, contracts, scheduling, context, or personal domains.

## Implementation profile

```text
Python standard library first
SQLite + WAL for local durable structured state when suitable
JSON for bounded interchange
CLI-first
Bash/Python for small deterministic utilities
existing HTTP/MCP interfaces before new adapters
no daemon without persistent event-driven value
no broker/distributed scheduler without demonstrated need
no service mesh/Kubernetes
no second database server without demonstrated need
no generic plugin framework before stable adapters exist
no provider proliferation without workload evidence
local validation before hosted CI
bounded I/O and explicit timeout/failure semantics
hash-verified artifacts where provenance matters
minimal dependencies, processes, repositories, state copies, nested agents, and context
```

Existing justified dependencies are not removed merely to satisfy “standard library first.”

## Harness promotion

The first `reward-harness` decision remains:

```text
PROMOTE      generic operational invariants are empirically reusable
RETAIN       application-specific implementation
SPLIT_LATER  reusable core plausible but extraction is premature
```

No standalone `axiom-harness` repository should exist before `PROMOTE`.

If promoted:

```text
immutable TaskSpec
→ eligible resource
→ exclusive lease
→ AttemptRecord
→ executor/APEX run
→ acceptance
→ transactional canonical task commit
→ restart/reopen verification
```

Required evidence:

```text
lease exclusivity
safe lease expiry
restart recovery
explicit UNKNOWN
hard-zero-spend enforcement where requested
capability filtering
bounded retry
context budgets
machine-readable receipts
one authoritative task state
transactional canonical task commit
fault tests across task-state boundaries
```

APEX continues owning its own internal run/effect recovery.

## Migration order

```text
0   preserve validated working paths
1   keep release/state documentation synchronized with live authoritative evidence
2   retain architecture terminology: APEX = canonical machine execution runtime
3   validate only authorized provider/model profiles against direct APEX before host-harness nesting
4   record reproducible ApexValidationRecord artifacts for materially relevant profiles
5   verify account/service/quota/pricing/usage before assigning nonzero spend capacity
6   compare only accepted or explicitly authorized candidate profiles
7   test external host harnesses only against an accepted direct APEX baseline
8   add no host-harness adapter unless existing CLI/HTTP/MCP surfaces prove insufficient
9   preserve durable ASON authorization binding to exact APEX plan/run
10  use Harness only where durable orchestration has measured material value
11  add ContextPack budgeting/cache only where measured
12  add providers/executors only for demonstrated workloads
13  move persistent operational scheduling out of Director only where implementation proves overlap
14  add high-value events/escalations
15  expand reusable primitives only from repeated evidence
16  measure and delete low-value machinery
```

Architecture purity never outranks continuity of a validated working path.

## System identity

AXIOM is a hybrid human–machine operating architecture that allocates intelligence, computation, automation, human attention, and capital toward the Owner/Operator's highest-value achievable portfolio while preserving explicit authority, bounded execution, durable evidence, uncertainty, budget control, and human control.

```text
observe
  ↓
resolve routine state locally
  ↓
reprioritize strategically only when required
  ↓
schedule / compile context / select resource
  ↓
validate provider/account capacity
  ↓
authorize consequential machine plans where required
  ↓
execute
  ↓
accept evidence
  ↓
commit canonical task result
  ↓
update compact strategic state
  ↓
continue
```
