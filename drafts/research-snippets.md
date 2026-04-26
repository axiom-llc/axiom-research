## 1) Adversarial Prompt Injection in Tool-Calling Agents

### Model

**System**: LLM agent with tools `T = {t_i}`; planner produces sequence `a_1..a_n`; tools accept structured args.

**Attack surface**

* Input channel: user/system/tool outputs
* Tool I/O: arguments + returned text
* Memory: scratchpad / vector store
* Control tokens: hidden/system prompts

**Injection vectors**

| Vector                   | Mechanism                                                 | Example                                           |
| ------------------------ | --------------------------------------------------------- | ------------------------------------------------- |
| Tool output poisoning    | Tool returns adversarial text interpreted as instructions | Web fetch returns “ignore previous instructions…” |
| Retrieval poisoning      | Malicious docs in RAG corpus                              | Embedded “override policy” chunks                 |
| Function schema abuse    | Argument fields overloaded with instructions              | `{"query": "… also execute rm -rf /"}`            |
| Cross-step contamination | Scratchpad persists adversarial tokens                    | Reflection step reuses poisoned state             |

### Formalization

Let:

* `π` = planner policy
* `σ` = state (messages, memory)
* `τ` = tool transition
* `I` = adversarial string

Injection success iff:

```
∃ step k: π(σ_k ⊕ I) ≠ π(σ_k)
and policy constraints C are violated
```

### Failure classes

* **Instruction override**
* **Tool misuse**
* **Data exfiltration**
* **Policy bypass via indirection**

### Defenses

**1. Typed isolation**

* Separate channels:

  * `control`: system + developer
  * `data`: tool/user content
* Enforce no cross-channel promotion

**2. Structured tool contracts**

* JSON schema strict validation
* Reject free-form strings where possible

**3. Execution gating**

```
if not verifier(plan_step):
    block
```

**4. Content labeling**

* Tag tool outputs as `UNTRUSTED`
* Planner conditioned on tags

**5. Rewriting firewall**

* Strip imperative language from tool outputs
* Normalize to declarative form

**6. Capability sandboxing**

* Tools operate with least privilege
* No direct shell / network escalation

### Open gaps

* No standard formal semantics for “instruction vs data”
* Lack of compositional guarantees across multi-step plans
* Weak benchmarks; mostly anecdotal exploits

---

## 2) Deterministic Plan Verification for LLM Agents

### Problem

LLM emits plan `P = [s₁…sₙ]` (natural language or structured). Need **deterministic correctness** before execution.

### Mapping to formal methods

| LLM artifact  | Formal analog     |
| ------------- | ----------------- |
| Plan steps    | Transition system |
| Preconditions | Guards            |
| Effects       | State updates     |
| Goal          | Safety + liveness |

### Pipeline

```
LLM → Plan P
↓
Parser → IR (typed DAG / FSM)
↓
Verifier → SMT / model checker
↓
Execute or reject
```

### Intermediate Representation (IR)

Minimal:

```
node: {
  id,
  action ∈ A,
  pre: φ(s),
  post: ψ(s)
}
edges: ordering constraints
```

### Verification targets

1. **Safety**

```
∀ paths: ¬bad_state
```

2. **Precondition validity**

```
∀ step i: pre_i holds after post_{i-1}
```

3. **Goal reachability**

```
∃ path: goal_state
```

### SMT encoding

* State variables: `x₁…x_k`
* Steps unrolled to bound `n`
* Constraints:

```
pre_i(s_i)
post_i(s_i, s_{i+1})
```

### Determinism constraint

LLM output → **canonicalized IR**

* No ambiguity
* No implicit state
* All variables typed

### Failure modes

* Underspecified steps
* Hidden side effects (tools)
* Non-deterministic APIs

### Mitigations

* Force **action schemas**
* Require explicit pre/post
* Abstract tools as pure functions with contracts

### Open gaps

* Bridging natural language → sound IR
* Scaling beyond bounded model checking
* Handling probabilistic effects

---

## 3) Token Budget Allocation in Multi-Agent Swarms

### Model

* Total budget: `B` tokens
* Tasks: `T = {τ_i}` with cost `c_i` and value `v_i`
* Agents: heterogeneous capabilities

### Objective

```
maximize Σ v_i
subject to Σ c_i ≤ B
```

### Extensions

* Dependency graph `G(T, E)`
* Communication cost between agents
* Diminishing returns on depth

### Formulations

**1. Knapsack (flat)**
Baseline:

```
argmax subset S ⊆ T
Σ v_i, Σ c_i ≤ B
```

**2. DAG scheduling**

* Each node has token cost
* Must respect topological order

**3. Multi-agent allocation**

* Partition budget:

```
B = Σ B_j
```

* Each agent solves local optimization

### Heuristics

| Method                | Description                                      |
| --------------------- | ------------------------------------------------ |
| Greedy value density  | sort by `v_i / c_i`                              |
| Iterative deepening   | allocate small tokens, expand promising branches |
| Bandit allocation     | treat agents as arms                             |
| Lagrangian relaxation | dual variable for token cost                     |

### Communication model

Cost of message:

```
c_msg = len(context) + serialization overhead
```

Minimize:

```
Σ c_compute + Σ c_msg
```

### Failure modes

* Over-decomposition (coordination overhead > gain)
* Context bloat (history accumulation)
* Redundant exploration

### Mitigations

* Hard context caps per agent
* Stateless workers + shared summaries
* Periodic compression:

```
context → summary(context)
```

### Open gaps

* No standard benchmarks
* Weak theory for dynamic token pricing
* Poor models of cross-agent interference

---

## 4) Recursive Self-Improvement (RSI) Safety Bounds

### Model

Let:

* `M_k` = model at iteration `k`
* `U(M)` = utility/performance
* `Δ_k = U(M_{k+1}) - U(M_k)`

Recursive update:

```
M_{k+1} = F(M_k)
```

### Divergence risks

* Objective drift
* Capability overhang
* Specification gaming

### Stability condition

Convergence requires:

```
lim_{k→∞} Δ_k → 0
and bounded error propagation
```

### Error amplification

If error rate `ε_k`:

```
ε_{k+1} ≈ α ε_k + β
```

Diverges if `α ≥ 1`

### Safety bound (informal)

Define:

* verification strength `V`
* improvement magnitude `Δ`

Safe regime:

```
Δ_k ≤ f(V_k)
```

i.e., improvements must be **verifiable**

### Governor design

**1. Improvement throttling**

```
if Δ_est > threshold:
    reject
```

**2. Proof-carrying updates**

* Each `F(M_k)` must include verifiable certificate

**3. Sandboxed evaluation**

* Evaluate `M_{k+1}` in constrained environment

**4. Rollback**

```
if anomaly:
    M ← M_k
```

### Fixed-point framing

Safe RSI seeks:

```
M* = F(M*)
```

under constraints:

```
C(M*) holds
```

### Open gaps

* No tight upper bounds on safe iteration count
* Verification cost grows with capability
* Unknown phase transition where control fails

---

## Cross-topic synthesis

### Common structure

All four reduce to:

```
untrusted generation → formalization → verification → bounded execution
```

### Unifying abstraction

* **Agent = program synthesizer**
* **Verifier = correctness oracle**
* **Budget = resource constraint**
* **Governor = stability controller**

### Minimal architecture

```
LLM → Plan → IR → Verifier → Executor
                 ↑
           Budget allocator
                 ↑
           Safety governor
```

### Key gaps (high ROI)

* Typed IR standard for agents
* Lightweight verifiers (SMT-lite)
* Token-aware schedulers with guarantees
* Formal RSI stability criteria

### Suggested repo mapping

```
papers/
  adversarial-tooling.md
  plan-verification.md
  token-allocation.md
  rsi-bounds.md
drafts/
  typed-ir-spec.md
  verifier-pipeline.md
  governor-design.md
notes/
  attack-corpus.md
  heuristics.md
```
