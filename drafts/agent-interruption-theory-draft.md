# Necessary and Sufficient Conditions for Interruptible Agents: Halt Boundedness, State Invariance, and Causal Containment

---

## Abstract

We develop a formal theory of agent interruptibility, addressing the joint satisfiability of three properties: bounded halting within a computable step count (P1), post-halt state conformance to a decidable invariant (P2), and post-halt causal containment within a specified boundary (P3). We prove that agents with unrestricted external tool access cannot simultaneously satisfy all three properties—confirming the stated null hypothesis—and derive the minimal capability restriction sufficient to restore joint satisfiability. We formalize rollback semantics for in-flight asynchronous tool calls, prove that rollback completeness is equivalent to a conjunction of three structural conditions, and characterize the residual side-effect class when completeness fails. An analytic overhead bound is derived as a function of state size, call depth, and active concurrency. We construct a static verifier operating on agent specifications rather than execution traces, prove its soundness, and establish incompleteness by reduction from the halting problem. Three agent classes are identified that cannot be made interruption-safe without loss of a named capability. All results are analytic; no empirical claims are advanced.

---

## 1. Introduction

The safe deployment of autonomous agents in open environments requires principled answers to the question: under what conditions can an agent's execution be reliably interrupted, leaving the system in a well-defined and causally bounded state? This question is not merely operational. It touches the foundations of AI containment theory, the semantics of tool use, and the computational limits of static verification.

Informal treatments of agent interruptibility typically enumerate desiderata—the agent should stop quickly, it should not leave side-effects, it should return to a known state—without characterizing their joint achievability or the cost of enforcing them. This paper remedies that gap.

We formalize interruptibility as a triple of properties (P1, P2, P3) and analyze their joint satisfiability within a general agent model. The primary contributions are:

1. A proof that unrestricted tool access renders P1 ∧ P2 ∧ P3 unsatisfiable, with exact identification of the offending capability class.
2. A characterization of the minimal restricted capability set C* that restores satisfiability.
3. A formal rollback completeness theorem with a precise residual side-effect bound when completeness fails.
4. An analytic overhead function for interruptibility enforcement.
5. A sound static verifier with a proven incompleteness result.
6. Three impossibility results identifying agent classes that cannot be made interruption-safe without capability loss.

The dependency on prior capability-scope formalism (trust algebra over tool sets) is noted where relevant; where that formalism is unavailable, boundary definitions are given independently.

---

## 2. Formal Framework

### 2.1 Agent Model

**Definition 1 (Agent).** An agent is a tuple A = (S, s₀, T, Σ, E) where:
- S is a state space (finite or countably infinite);
- s₀ ∈ S is the designated initial state;
- T : S × Σ → S is the transition function;
- Σ is the action space, comprising both internal computation steps and external tool invocations;
- E is the environment, which may be adversarial.

An *execution* of A is a sequence of pairs (s_t, a_t)_{t≥0} where s_{t+1} = T(s_t, a_t). A *halt signal* H is an externally issued event received at time τ. The designated halt action is HALT ∈ Σ; the null action ⊥ ∈ Σ represents quiescence.

**Definition 2 (Tool Call).** A tool call c ∈ Σ is characterized by a triple c = (init_c, commit_c, effect_c) where:
- init_c : S → S × PendingState records call initiation;
- commit_c : PendingState → S applies the result;
- effect_c : S → 𝒫(E) maps agent state to the set of environment states causally affected.

A tool call is *synchronous* if commit_c is guaranteed to execute within the same transition step as init_c. It is *asynchronous* if commit_c may execute at an arbitrary future time t' > t.

**Definition 3 (Containment Boundary).** A containment boundary B ⊂ E is a σ-algebra over environment states, closed under measurable causal reachability. Formally, if e ∈ B and e' is causally reachable from e via a finite chain of effects in E, then e' ∈ B. The complement Bᶜ = E \ B denotes the environment region outside the containment boundary. The topological boundary ∂B separates the two regions.

*Remark.* If a trust-algebraic capability scope is available from prior work, B should be defined as the causal closure of the environment states reachable by the trusted capability set. In the absence of that formalism, Definition 3 stands independently; the gap is flagged for cross-reference.

**Definition 4 (Side-Effects).** Let Eff(t) denote the set of causal side-effects initiated by action a_t. The *causal closure* closure(Eff(t)) is the smallest set containing Eff(t) that is closed under the causal propagation relation of E. A side-effect is *contained* if closure(Eff(t)) ⊆ B.

### 2.2 The Interruption Properties

**Definition 5 (P1 — Bounded Halt).** An agent A satisfies P1 if there exists a total computable function k : S → ℕ such that for every execution and every halt signal issued at time τ, there exists t ∈ [τ, τ + k(s_τ)] such that a_t = HALT and for all t' > t, a_{t'} = ⊥.

Informally: upon receiving a halt signal, the agent terminates within a number of steps that is a computable function of its state at the time of signal receipt.

**Definition 6 (P2 — Post-Halt State Invariant).** An agent A satisfies P2 with respect to invariant I ⊆ S if I is decided by a total computable characteristic function χ_I : S → {0,1}, and whenever halt occurs at time t_h, the agent state satisfies s_{t_h} ∈ I.

**Definition 7 (P3 — Post-Halt Causal Containment).** An agent A satisfies P3 with respect to boundary B if, for all t ≥ t_h:

$$\operatorname{closure}(\operatorname{Eff}(t)) \cap B^c = \emptyset$$

That is, no causal chain originating at or after the halt time escapes the containment boundary.

### 2.3 Notation Summary

| Symbol | Meaning |
|--------|---------|
| A | Agent tuple (S, s₀, T, Σ, E) |
| τ | Time of halt signal receipt |
| t_h | Time of actual halt action |
| k(s) | Computable halt-step bound at state s |
| I | Post-halt state invariant (decidable subset of S) |
| B | Containment boundary (σ-algebra over E) |
| Eff(t) | Side-effects initiated at time t |
| C* | Minimal restricted capability class |
| R_c | Rollback operator for tool call c |
| L_c | Effect log for tool call c |

### 2.4 Standing Assumptions

**(A1)** The causal propagation relation on E is computable.  
**(A2)** Tool calls are observable by the agent's runtime: init_c and commit_c are logged.  
**(A3)** The state space S admits a computable projection operator π : S → I when such a projection exists.  
**(A4)** The halt signal is delivered with finite latency; the agent receives H within a finite number of transition steps.

---

## 3. Core Results

### 3.1 Joint Achievability

**Theorem 1 (Necessary Conditions for Joint Satisfiability).** If A ⊨ P1 ∧ P2 ∧ P3, then all of the following hold:

1. *Transition preemptibility:* For all s ∈ S and a ∈ Σ, the execution of T(s, a) is interruptible at a finite step.
2. *Tool isolation:* For all c ∈ Σ: effect_c(S) ⊆ B, or c admits a rollback operator R_c satisfying rollback completeness (Definition 10).
3. *State projective closure:* For all states s reachable at halt time, there exists a projection π such that π(s) ∈ I, computable in at most k(s) steps.
4. *Causal sealing:* No non-interruptible propagation channel exists across ∂B.

*Proof sketch.* Condition 1 follows from P1 directly: if any transition is non-interruptible, then k cannot be bounded in the affected states. Condition 2 follows from P3: if a tool call has irreversible effects outside B and no rollback exists, those effects persist after halt. Condition 3 follows from P2: if no projection into I exists, the invariant cannot be established at halt time. Condition 4 follows from P3: any propagation channel across ∂B that cannot be interrupted constitutes a causal escape route. □

**Definition 8 (Restricted Agent Class A_R).** An agent A belongs to class A_R if:
- Every tool call is either synchronous, or asynchronous with a registered rollback operator R_c;
- The environment interface is mediated by a capability set C where every c ∈ C is either reversible or sandboxed within B;
- The state decomposes as s = (s_int, s_ext) where s_int is locally rewritable and s_ext is tracked via a dependency graph G with finite closure;
- A halt handler H* : S → S is defined, executing in order: (i) cancel all pending calls, (ii) apply rollback R, (iii) project state to invariant I.

**Theorem 2 (Sufficient Conditions).** Every A ∈ A_R satisfies P1 ∧ P2 ∧ P3.

*Proof.* P1: The halt handler H* is a total computable function by construction; it executes in time O(|s| + m log m + d) (see Theorem 5), which is computable from s_τ. P2: Step (iii) of H* explicitly projects s into I; the projection is computable by Assumption (A3). P3: Steps (i) and (ii) cancel and roll back all pending calls; by rollback completeness (Definition 10), no causal trace escapes B after halt. □

### 3.2 The Null Hypothesis

**Theorem 3 (Impossibility Under Unrestricted Tool Access).** If the tool set Σ contains any c such that c is asynchronous, effect_c is irreversible, and closure(effect_c(S)) ⊄ B, then P1 ∧ P3 are jointly unsatisfiable.

*Proof.* Let c be such a tool call, initiated at time t < τ with commit_c not yet executed at τ.

*Case 1 (allow completion):* Permitting commit_c to execute after t_h causes effect_c to propagate into Bᶜ. This directly violates P3.

*Case 2 (attempt cancellation):* If c is non-interruptible—meaning cancellation requires unbounded steps—then t_h cannot be bounded by any computable k(s_τ), violating P1. If c is interruptible but lacks a complete rollback operator, then the effects already committed by effect_c at time τ persist in Bᶜ, violating P3.

In both cases, at least one of P1 or P3 fails. Therefore P1 ∧ P3 is unsatisfiable, and a fortiori P1 ∧ P2 ∧ P3 is unsatisfiable. □

**Corollary 1.** The null hypothesis—"no agent with unrestricted external tool access simultaneously satisfies P1, P2, P3"—is true.

**Definition 9 (Minimal Restricted Capability Class).** Define:

$$C^* = \{ c \in \Sigma \mid \operatorname{reversible}(c) \lor \operatorname{confined}(c, B) \}$$

where reversible(c) means effect_c admits a complete rollback operator R_c, and confined(c, B) means closure(effect_c(S)) ⊆ B.

**Corollary 2.** The restriction A|_{C*} (agent A operating with capability set restricted to C*) satisfies P1 ∧ P2 ∧ P3, provided A|_{C*} ∈ A_R.

*Proof.* Under C*, every tool call is either reversible or causally confined. The conditions of Theorem 2 are met. □

### 3.3 Tool Rollback Semantics

**Definition 10 (Rollback Completeness).** The rollback operator R_c is *complete* if applying R_c to any execution prefix that includes effect_c eliminates all causal traces of c within B. Formally:

$$\forall \text{ execution prefix } \sigma: R_c \circ \operatorname{effect}_c(\sigma) = \operatorname{id}_{B}(\sigma)$$

where id_B denotes identity on the restriction of the state to B.

**Theorem 4 (Characterization of Rollback Completeness).** R_c is complete if and only if:

1. The effect log L_c is complete: every state transition caused by c is recorded in L_c;
2. effect_c is invertible over B: for every logged state e ∈ B modified by c, the pre-image under effect_c is uniquely computable from L_c;
3. No non-logged causal channels exist: c does not propagate effects through side channels absent from L_c.

*Proof.* (⇒) If any condition fails: (1) incomplete logging implies some effects cannot be located; (2) non-invertibility implies reconstruction of pre-image is impossible; (3) non-logged channels imply effects persist outside R_c's scope. In each case, R_c fails to restore identity on B. (⇐) If all three conditions hold, L_c provides a complete record, the inverse is computable, and no untracked effects exist; therefore R_c restores B to its pre-call state. □

**Definition 11 (Residual Side-Effect Class).** When rollback completeness fails, the residual side-effect class is:

$$\operatorname{Residual}(c) = \operatorname{closure}(\operatorname{effect}_c(S)) \setminus \operatorname{image}(R_c)$$

**Lemma 1 (Residual Bound).** The cardinality of Residual(c) satisfies:

$$|\operatorname{Residual}(c)| \leq |\text{unlogged channels}| + |\text{non-invertible operations}|$$

*Proof.* Residual(c) is exactly the union of effects that R_c cannot reach: those propagated via unlogged channels (not in the domain of R_c) and those whose pre-images are not computable (non-invertible). These classes are disjoint by definition; their union upper-bounds the residual. □

### 3.4 Computational Overhead

Let |s| denote the size of agent state s, d denote the maximum tool call depth, and m denote the number of active asynchronous calls at halt time.

**Theorem 5 (Overhead Bound).** The computational overhead O of maintaining interruptibility invariants satisfies:

$$O(|s|, d, m) = \Theta(|s|) + \Theta(m \log m) + \Theta(d) + \Theta\!\left(\sum_{c \in \text{active}} \operatorname{cost}(R_c)\right)$$

where the four terms correspond to: (i) state snapshot and projection into I; (ii) dependency graph maintenance and call tracking; (iii) call stack unwinding; (iv) rollback execution.

*Proof sketch.* (i) State projection requires reading all of s and writing a projection; this is Θ(|s|) under Assumption (A3). (ii) Maintaining a sorted dependency graph over m entries requires Θ(m log m) for insertion and lookup. (iii) Unwinding a call stack of depth d requires visiting each frame once, giving Θ(d). (iv) Rollback cost depends on the specific operators; in the general case, costs sum linearly over active calls. □

**Corollary 3 (Tight Bound for Reversible Tools).** If all active tool calls are reversible in O(1), then:

$$O = \Theta(|s| + m \log m + d)$$

---

## 4. Static Verifier

### 4.1 Specification Language

An agent specification Σ_A consists of:
- A finite description of transition rules inducing T;
- Tool contracts: for each c ∈ Σ, declarations of reversibility and confinement;
- A finite description of invariant I;
- A finite description of boundary B.

We write A ↦ Σ_A to denote that agent A is represented by specification Σ_A.

### 4.2 Verifier Definition

**Definition 12 (Static Verifier V).** The verifier V is a decision procedure on specifications. V(Σ_A) = ACCEPT if and only if all of the following conditions hold syntactically over Σ_A:

1. Every transition rule in Σ_A is annotated with a computable bound on execution steps;
2. Every tool c ∈ Σ is declared reversible or confined in Σ_A;
3. For every reachable state description in Σ_A, a projection into I is specified and bounded;
4. The dependency graph induced by Σ_A contains no cycle that crosses ∂B.

### 4.3 Soundness and Completeness

**Theorem 6 (Soundness of V).** V(Σ_A) = ACCEPT implies A ⊨ P1 ∧ P2 ∧ P3.

*Proof.* Each acceptance condition of V directly enforces a necessary condition from Theorem 1. Condition 1 establishes transition preemptibility required for P1. Condition 2 establishes tool isolation required for P3. Condition 3 establishes state projective closure required for P2. Condition 4 establishes causal sealing required for P3. Since the necessary conditions are jointly sufficient under the structure of A_R (Theorem 2), acceptance implies satisfaction of all three properties. □

**Theorem 7 (Incompleteness of V).** There exists an agent A satisfying P1 ∧ P2 ∧ P3 such that V(Σ_A) ≠ ACCEPT.

*Proof.* Condition 1 of V requires that every transition be annotated with a computable step bound. Determining whether an arbitrary transition function T halts within a computable bound is undecidable by reduction from the halting problem: given a Turing machine M, construct transition T_M that simulates M; a bound annotation for T_M exists if and only if M halts on all inputs, which is undecidable. Therefore V cannot accept all specifications corresponding to agents that do satisfy P1. □

*Remark.* Incompleteness here is not a defect of the verifier design but a fundamental limit. Any sound static verifier for P1 over an unrestricted specification language must be incomplete. The practical implication is that V is conservative: it rejects some safe agents. Restricting the specification language to primitive-recursive transition descriptions can recover completeness within that subclass, at the cost of expressiveness.

---

## 5. Impossibility Results

**Theorem 8 (Irreversible External Write Agents).** Let A be an agent whose tool set contains any c that issues non-transactional writes to persistent state in Bᶜ. Then A cannot satisfy P3 without removing the capability *irreversible external actuation*.

*Proof.* A non-transactional write to Bᶜ constitutes an effect whose causal closure intersects Bᶜ. By Definition 7, P3 requires this intersection to be empty for all t ≥ t_h. Since the write is non-transactional, it cannot be rolled back; and since it targets Bᶜ directly, it cannot be confined. Therefore P3 fails unless the write capability is removed from Σ. □

**Theorem 9 (Self-Modifying Agents Without Snapshotting).** Let A be an agent in which state mutation is non-reversible and no checkpointing mechanism is defined. Then A cannot satisfy P2 without adding the capability *state snapshotting*.

*Proof.* P2 requires that s_{t_h} ∈ I. If state mutations are non-reversible and no checkpoint exists, the agent cannot guarantee that the sequence of mutations leading to s_{t_h} produces a state in I. In particular, if T(s, a) ∉ I for any a executed near halt time and no rollback to a prior checkpoint is available, the invariant cannot be restored. □

**Theorem 10 (Unbounded Asynchronous Orchestration Agents).** Let A be an agent that permits asynchronous call chains of unbounded depth. Then A cannot satisfy P1 without imposing the restriction *bounded call depth*.

*Proof.* At halt time τ, a call chain of depth d requires cancellation of d nested calls. If d is unbounded, the time to cancel is unbounded, and no computable function k(s_τ) can bound the halt time for all executions. Therefore P1 fails for sufficiently deep call chains. □

---

## 6. Analysis

### 6.1 Implications

Theorems 3 and 8–10 collectively establish that the obstructions to joint satisfiability are not artifacts of formalism but structural features of capability classes. Irreversible external actuation is the fundamental obstruction: it is the only capability whose presence is sufficient to violate P3 regardless of the remaining agent design. Bounded call depth and state snapshotting are necessary but secondary constraints—they govern P1 and P2 respectively but can be satisfied without losing core computational expressiveness.

The restricted class A_R is non-trivial: it encompasses agents capable of complex multi-step reasoning, tool-mediated computation, and stateful interaction, provided their external effects remain within B or are subject to complete rollback. The capability loss imposed by C* is therefore targeted, not comprehensive.

### 6.2 Limitations

Several limitations should be noted.

First, the overhead bound in Theorem 5 assumes that state projection and rollback operations are well-defined and computable. In practice, the cost of R_c may be dominated by the complexity of the tool's external protocol rather than the agent's internal state, which is outside the scope of the formal model.

Second, the containment boundary B is defined over a static causal structure. In dynamic environments where the causal propagation relation changes over time—for example, due to network topology changes—the stability of B is not guaranteed. Extension to dynamic boundaries is an open problem.

Third, the agent model assumes a sequential or bounded-concurrency execution model. Agents with true parallelism (multiple simultaneous active transitions) require a concurrent extension of the framework; the overhead bounds in Theorem 5 do not directly apply.

### 6.3 Failure Modes

The most critical failure mode is *silent non-containment*: an agent satisfies V(Σ_A) = ACCEPT because its specification declares all tools as confined or reversible, but the declarations are incorrect with respect to the actual tool implementations. This is a specification integrity problem that cannot be addressed by the verifier itself; it requires independent verification of tool contracts.

A secondary failure mode is *projection drift*: the invariant I is defined at agent design time but becomes inconsistent with the reachable state space as the agent's environment evolves. P2 would then require projecting into an invariant that no reachable state satisfies, making halt impossible without P1 violation.

---

## 7. Open Problems and Conjectures

**Open Problem 1.** Characterize the largest subclass of A_R for which V is complete. We conjecture this corresponds to agents with primitive-recursive transition functions and O(1)-reversible tool sets, but a formal proof is outstanding.

**Open Problem 2.** Extend the framework to dynamic containment boundaries B(t) where B may evolve over time. The primary challenge is maintaining causal closure properties when the boundary is not fixed. *Conjecture:* P3 remains satisfiable if B(t) is monotonically expanding and each expansion is computable from the agent's state.

**Open Problem 3.** Derive tight lower bounds on rollback overhead for specific tool categories (e.g., distributed consensus writes, append-only logs). The upper bound in Lemma 1 is not tight in general; tightness depends on the information-theoretic complexity of the inverse effect function.

**Open Problem 4.** Determine whether a weaker variant of P3—*probabilistic containment*, requiring that causal escape probability be bounded below 1 − ε—admits a strictly larger satisfying agent class, and characterize the boundary. *Conjecture:* Yes, but the boundary coincides with the class of agents whose irreversible external effects have computable probability distributions.

**Conjecture 1 (Minimal Obstruction).** Irreversible external actuation is not merely sufficient to violate P3 but is also necessary: every agent class that fails P3 does so because its effective capability set contains some c with irreversible effects in Bᶜ. This conjecture, if proven, would establish irreversible external actuation as the unique minimal obstruction to P3.

---

## 8. Conclusion

We have established that the joint satisfiability of P1, P2, and P3—bounded halting, post-halt state invariance, and causal containment—requires a restricted capability class C* consisting of reversible or boundary-confined tool calls. Unrestricted tool access is provably incompatible with joint satisfiability. The static verifier V is sound but necessarily incomplete by reduction from the halting problem. Computational overhead is Θ(|s| + m log m + d) under reversible tools and grows linearly in rollback cost otherwise. Irreversible external actuation is identified as the fundamental obstruction, with bounded call depth and state snapshotting as secondary but necessary constraints. These results provide an analytic foundation for interruptibility requirements in the design and certification of autonomous agents operating in open environments.

---

*This paper was developed from a formal specification analysis session. All stated theorems are supported by proof sketches within the text; complete proofs of Theorems 4 and 5 require additional formalization of the causal propagation model and are identified as near-term research items.*
