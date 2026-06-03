# AXIOM Research

## Formal Methods, Agent Control Loop Taxonomies, and Self-Optimization Theory

This repository houses the theoretical foundations, formal academic papers, and architectural taxonomies underpinning the AXIOM agentic execution ecosystem. The research preserved here outlines the formal computability bounds, safety-by-design mathematical constraints, and loop-control models implemented within the [Axiom Apex](https://github.com/axiom-llc/axiom-apex) deterministic execution runtime.

---

## 1. Repository Contents

### A. Loop Architecture Taxonomy
*   **File**: `ai-loop-architecture-taxonomy.md`
*   **Abstract**: A comprehensive taxonomic classification of artificial intelligence feedback and control loop architectures, organizing systems by their autonomy level, human dependency, execution control, and failure modes.
*   **Key Concepts**:
    *   **Self-Consumption Loops (The "Ralph Wiggum" Loop)**: Systems that recursively process and repair their own potentially malformed outputs through parsing engines and error signal parsing.
    *   **Self-Improving Loops (Heuristic Adaptation)**: Systems that dynamically rewrite context-embedded rules (e.g., rule tables, do-lists, and exception tables) without modifying model weights.
    *   **Inner Loop Control**: Pre-execution validation pipelines executing invisible quality-control passes before emitting structured outputs.
    *   **Prompting Iterative Refinement Loops**: Evaluation-guided rating loops and self-imposed critic loops that optimize outputs through structural feedback.
    *   **Human Involvement Loops**: Human-in-the-loop (HITL) and human-on-the-loop (HOTL) gating mechanisms with alerting and override thresholds.
    *   **Systems Learning Loop Families**: Feedback retraining pipelines (self-curated learning) and loop fusion optimizations designed to compress compute and latency.

### B. Recursive Hyper-Optimization
*   **File**: `recursive-hyper-optimization.md`
*   **Abstract**: A rigorous, computability-grounded formal analysis of recursive hyper-optimization—the process by which a computable system safely alters its own operational optimization structures through recursive meta-updates while maintaining monotonic performance improvements.
*   **Key Concepts**:
    *   **Formal Foundations**: Restricting self-modification entirely to recursive functions under Church-Turing limits to ensure system verifiability.
    *   **Computational Self-Reference**: Utilizing Kleene's fixed-point recursion theorems to allow program self-modification without introducing semantic paradox or circular grounding.
    *   **Computational Autopoiesis**: Conceptualizing self-improving agents as self-producing entities that maintain continuous functional reorganization within computationally defined boundaries.
    *   **The Infinite Hierarchy Problem**: Resolving ascending meta-level regression (the infinite tower of self-improvers) through mathematical fixed-point collapse.

### C. Deterministic Execution Contracts for LLM Agent Systems
*   **File**: `tacon2026_apex_deterministic_execution_contracts.pdf`
*   **Abstract**: A formal academic publication presenting the concrete architecture, policy enforcement boundaries, and empirical evaluation of the AXIOM two-stage plan-deterministic execution model.
*   **Key Concepts**:
    *   **The Type-Confusion Model of Prompt Injection**: Characterizing prompt injection as a structural type-confusion failure over semantically untyped input-control channels (analogous to memory-unsafe control-flow corruption).
    *   **Correctness Envelopes**: Defining bounded, pre-execution verification gates that evaluate multi-step plans against structural safety rules.
    *   **RSI and BDSO Architecture**: Designing a Benchmark-Driven Self-Optimization (BDSO) loop that evaluates Gemini-generated codebase patches inside isolated subprocesses, scoring candidates against the `apex_score` fitness function.
    *   **The Paranoid Exclusion Invariant**: Establishing the safety boundary wherein the plan auditor (`paranoid.py`) is permanently excluded from self-modification lists.

---

## 2. Theoretical Invariants Realized in AXIOM Apex

The formal theories in this repository serve as the direct blueprint for the [Axiom Apex](https://github.com/axiom-llc/axiom-apex) core execution engine:

*   **Information-Flow Separation**: Generation is probabilistic, but execution is structurally constrained. Probabilistic planners propose, structural schemas validate, and the stateless execution kernel runs.
*   **The Correctness Gate**: Implemented natively in `apex/core/validator.py` and `apex/core/schema.py`, enforcing Pydantic validations, step ceilings, and blast-radius constraints before any tools are dispatched.
*   **SIGALRM Isolation**: Mitigates process hangs and tool-calling timeouts at the Unix syscall level using signal-interrupt handlers.
*   **Self-Healing Recovery**: Implements the transactional rollback logic (`apex/core/rollback.py`) described in the paper to reverse physical side-effects on execution failures.

---

## 3. References

The academic publications contained in this workspace cite and build upon the following foundational literature:

*   Ahn, M., et al. (2022). *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances*. arXiv:2204.01691.
*   Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073.
*   Greshake, K., et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv:2302.12173.
*   Perez, F., \& Ribeiro, I. (2022). *Ignore Previous Prompt: Attack Techniques For Language Models*. arXiv:2211.09527.
*   Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv:2302.04761.
*   Schmidhuber, J. (2003). *Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements*. Technical Report IDSIA-19-03.
*   Yao, S., et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629.

---

## 4. Official Ecosystem

*   **AXIOM Apex (Core Engine)**: [github.com/axiom-llc/axiom-apex](https://github.com/axiom-llc/axiom-apex)
*   **AXIOM Demos (Blueprints)**: [github.com/axiom-llc/axiom-demos](https://github.com/axiom-llc/axiom-demos)
*   **AXIOM Research (Theory)**: [github.com/axiom-llc/axiom-research](https://github.com/axiom-llc/axiom-research)
*   **AXIOM Portal (Web)**: [axiom-llc.github.io](https://axiom-llc.github.io)

---
© 2026 AXIOM LLC. Built for deterministic autonomous execution.
