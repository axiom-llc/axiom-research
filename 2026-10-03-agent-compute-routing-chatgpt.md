# Agent Compute Economics and Adaptive Routing

**Date:** 2026-10-03  
**Author channel:** ChatGPT, reconciled by AXIOM  
**Target:** `axiom-llc/axiom-research`

## Provenance

- Owner-supplied source SHA-256: `3c0cb08f07ab28ca183f022c1271321ec44670c79d5ac01f2209e8211318d832`.
- AXIOM refreshed decision-critical 2026 sources on 2026-10-03, including LLMRouterBench, WISERouter, FIRE, OpenAI prompt-caching documentation, ARC, and interaction-aware long-horizon compression.
- Experiments were normalized to the AXIOM remote-only boundary.
- This is research input, not deployed routing policy.

Evidence labels: **[E]** empirical · **[T]** theoretical reasoning · **[P]** proposed AXIOM metric/policy · **[H]** falsifiable hypothesis.

## Research Question

How should an autonomous agent rationally allocate model capability, reasoning/test-time compute, tokens, context, retrieval, tool calls, verification, retries, parallelism, and escalation when each resource has cost and its marginal value depends on task difficulty, uncertainty, consequence, reversibility, latency, tool health, privacy, and trajectory state?

The target objective is **validated useful work**, not raw token minimization.

## Executive Findings

1. **[E] Test-time compute has positive but diminishing and task-dependent returns.** Compute-optimal allocation can outperform fixed scaling, but forced continuation eventually flattens or loops.
2. **[E] More context is not monotonically better.** Lost-in-the-middle effects, RULER, and long-context/RAG studies show that nominal context capacity is not equivalent to useful context.
3. **[E/P] Verification has an optimum.** Deterministic/read-back validation is strong when postconditions are observable; generic self-correction is unreliable, and FIRE suggests targeted failure-conditioned interventions can outperform always-on reconsideration.
4. **[E] Retries can amplify cost and failure.** Retry budgets, error classes, backoff, jitter, and fail-fast behavior are standard reliability controls.
5. **[E/P] Adaptive routing can help, but complexity is not automatically rewarded.** FrugalGPT, RouteLLM, Hybrid LLM, AutoMix, WISERouter, and related work show routing gains under tested workloads; RouterBench/LLMRouterBench and simple-kNN results show that strong baselines can be difficult to beat consistently.
6. **[E/T] Parallelism exchanges compute for latency and diversity.** It helps only when branches are sufficiently independent and selection/verification is cheap.
7. **[E] Prompt caching changes economics, not semantic correctness.** Stable reusable prefixes can reduce cost/latency; cache hit rate belongs in telemetry rather than quality scoring.
8. **[P] AXIOM should keep static minimum-capable routing as the control baseline and require adaptive routing to beat it on held-out validated-work efficiency after all overhead is charged.**

## Resource Model

Let task state be:

[
s=(d,u,q,k,r,ell,p,h,x)
]

where:

- `d`: difficulty;
- `u`: uncertainty;
- `q`: required quality;
- `k`: consequence of error;
- `r`: reversibility;
- `ℓ`: latency budget;
- `p`: privacy/exposure constraints;
- `h`: tool/service health;
- `x`: trajectory state.

An allocation decision chooses model/capability tier, reasoning budget, context policy, tool/retrieval action, verification method, parallelism, retry/switch behavior, and escalation.

A practical objective is:

[
max_a E[V_{validated}] - C_{money} - C_{latency} - C_{human} - C_{privacy} - E[L_{residual}]
]

subject to hard reliability, privacy, authority, and latency constraints.

The rule for any optional additional resource `z` is: continue only while expected marginal validated value exceeds expected marginal total cost.

## Context Economics

### Useful context, not maximum context

Additional context can be:

- useful evidence;
- redundant duplication;
- harmful distractor/stale state.

AXIOM should optimize **useful-context density**, not context length.

### Compression

Compression can reduce cost but can also delete rare critical constraints, preserve mistaken summaries, or erase uncertainty. Prefer compression only when:

1. expected reuse justifies the transform;
2. canonical source material remains recoverable/auditable;
3. validation shows no reliability regression.

2026 evidence strengthens externalization as a safer pattern:

- ARC uses an ID-addressable append-only archive and compact references to old tool observations.
- *When Can Agents Forget Their Reasoning?* reports that reasoning history becomes more replaceable after task-relevant state has been externalized into code/files/tool outputs/environmental feedback.

These are promising single-study results, not universal compaction rules.

### Prompt caching

OpenAI's current API documentation describes prompt caching as a cost/latency mechanism. Stable policy/tool-schema/reference prefixes may be economically useful when real cache reuse exists. Log realized cache hits rather than designing around theoretical savings.

## Retrieval and Persistence Economics

Repeated retrieval costs latency, tokenization, source drift risk, and repeated parsing.

Persistent state costs write complexity, stale-state risk, contradiction handling, retention obligations, and invalidation logic.

**Candidate rule [P]:**

Persist information that is expensive to recover, reused, provenance-linked, and explicitly invalidatable. Re-read/retrieve volatile or authority-sensitive facts whose source must be current.

Keep four layers distinct:

1. canonical durable state;
2. derived durable state with provenance/invalidation;
3. session working state;
4. ephemeral retrieval.

## Retry Economics

Track retries as attempts of one logical operation, not as unrelated calls.

Candidate metrics:

[
RA = rac{N_{physical attempts}}{N_{logical operations}}
]

and total retry-cost amplification including larger later contexts, verification, escalation, and operator repair.

Classify failure before retry:

- transient → bounded retry/backoff;
- path-specific → switch path/provider;
- deterministic → do not retry unchanged input;
- semantic → revise plan;
- ambiguous effect/UNKNOWN → reconcile authoritative state before any repeat;
- impossible/unauthorized → stop or escalate.

Retry at one intentional layer; stacked retries across model, SDK, wrapper, and orchestrator can multiply attempts.

## Verification Economics

Prefer the cheapest sufficiently independent verifier:

1. schema/type/static check;
2. authoritative read-back;
3. executable test/query;
4. cross-source consistency;
5. specialized verifier;
6. independent LLM judge;
7. stronger-model review;
8. human review.

Generic self-critique should not substitute for deterministic evidence.

Track **verification yield**:

- accepted unchanged;
- detected real failure;
- caused revision;
- rescued final outcome;
- false accept/reject where audit ground truth exists.

Remove low-yield verification from low-risk classes unless required by authority/compliance.

## Adaptive Routing

### Baseline policies

At minimum compare against:

1. **strong-only**;
2. **static minimum-capable** by task/risk/privacy class;
3. **cheapest-first cascade** with explicit validation/escalation;
4. **simple kNN/task-similarity** routing where history is sufficient.

A learned router is justified only if it improves the validated quality/cost/latency frontier after its own inference, maintenance, calibration, and drift costs are included.

### Risk gates

Routing optimization must occur **after** hard gates:

- privacy/allowed-channel constraints;
- authority/permission;
- consequence;
- reversibility;
- non-idempotent effects;
- minimum validation requirement.

A stronger model can be cheaper per validated task if it prevents retries/human repair; “minimum-capable” therefore means lowest expected-total-cost route satisfying required reliability, not always “smallest model first.”

## Failure-Predictive Telemetry

Candidate features:

- task class;
- model/tool route;
- prior error class;
- retry count;
- verification failures;
- context length/density proxies;
- duplicate/repeated tool calls;
- tool-health history;
- actor/verifier disagreement;
- time since authoritative state refresh;
- root-to-detection lag.

A predictor is useful only if it changes a decision: stop, retry, switch, verify, escalate, or ask the human.

Start with simple interpretable baselines before neural/LLM predictors.

## Proposed Metrics

- **Tokens per validated task (TPVT)**
- **Tokens per validated state transition (TPVST)**
- **Validated-work efficiency (VWE):** validated value / total machine + human resource cost
- **Retry amplification (RA)**
- **Verification-adjusted cost (VAC)**
- **Human-attention cost (HAC)**
- **Failure-detection latency (FDL)**
- **Useful-context density (UCD)**
- **Context redundancy ratio**
- **Escalation rescue rate**
- **Verifier yield**
- **Cache-hit rate**
- **Claimed-vs-verified completion gap**

No single metric should become the objective. In particular, token minimization can reward brittle under-computation.

## Implications for AXIOM

1. Keep token telemetry as accounting, not the optimization target.
2. Make `validated` outcome/state transition the central join key for resource telemetry.
3. Preserve static minimum-capable routing as the baseline control.
4. Add risk gates before cost optimization.
5. Record retries and switches explicitly.
6. Record verification yield.
7. Prefer targeted failure-conditioned controls over generic reflection loops when evidence supports them.
8. Treat adaptive routing as an offline/shadow experiment before production use.
9. Keep context caching/prefix stability measurable and optional.
10. Price operator attention explicitly; a cheap model that causes human repair may be the expensive route.

## Testable Hypotheses

- **H1 [H]** Difficulty-conditioned reasoning budgets improve VWE over one fixed budget without reducing validated completion.
- **H2 [H]** Useful-context-density proxies predict validation failure better than raw input-token count.
- **H3 [H]** After two unchanged deterministic failures, a third identical attempt has lower VWE than switch/escalate/replan.
- **H4 [H]** Deterministic/read-back verification beats generic LLM self-critique on workflows with observable postconditions.
- **H5 [H]** Static minimum-capable routing remains within 2 percentage points of the best learned router at current AXIOM volume after overhead.
- **H6 [H]** Simple kNN routing is a stronger adaptive baseline than a heavier learned router on repeated task families.
- **H7 [H]** Failure-conditioned policies improve repeated reliability more efficiently than always-on verification.
- **H8 [H]** Stable-prefix cache reuse yields measurable cost/latency savings without changing validation rate.
- **H9 [H]** Consequence and reversibility features reduce dangerous downrouting beyond difficulty-only policies.

## Minimum Viable Experiments

All experiments must use **ChatGPT session-hosted compute or GitHub Actions/other already-authorized remote compute**. No Owner-workstation execution or local AXIOM clones. Incremental hosted spend: **$0.00**.

### MVE-1 — historical resource frontier

Group existing validated runs by task class/model/effort and compute completion rate, tokens, tool calls, retries, wall time, and human intervention. Identify Pareto frontiers and classes with flat/negative returns to extra compute.

### MVE-2 — retry survival curve

Estimate:

[
P(success on attempt n mid prior failures, error class, changed arguments?)
]

Derive per-error retry/switch thresholds.

### MVE-3 — verification-yield audit

Measure verifier calls, changed-decision rate, real-failure detection, rescue rate, tokens/time overhead, and false accepts/rejects where auditable.

### MVE-4 — context-density proxy

Use duplicate hashes, referenced evidence/state, retrieval count, and raw context length. Test on a chronological holdout whether density proxies predict validated outcome better than raw token count.

### MVE-5 — static-router replay

Freeze a minimum-capable rule set using an earlier time window and evaluate later tasks only where comparable route/outcome evidence exists. Do not invent counterfactual labels.

### MVE-6 — simple adaptive-router replay

Where sufficient repeated task families exist, compare kNN or logistic routing with static baseline on chronological holdout. Charge router runtime and maintenance overhead.

### MVE-7 — escalation rescue

Measure historical weak→strong model escalation and tool/provider switching separately: rescue rate, added cost, latency, and operator attention.

## Rejection Criteria

### Reject adaptive routing if

- it fails to beat simple baselines on held-out chronological data;
- savings disappear after router/verifier/maintenance overhead;
- OOD or time-split behavior is unstable;
- learned preferences cannot be overridden by hard authority/privacy/risk gates;
- routing errors are difficult to diagnose;
- workload volume/repetition is too low to estimate comparative performance;
- static minimum-capable routing remains on the Pareto frontier.

### Reject predictive telemetry if

- it fails time-split validation;
- it is poorly calibrated at decision thresholds;
- simple priors/logistic/kNN perform equivalently;
- predictions do not change an actionable decision;
- telemetry collection costs more than it saves;
- false negatives concentrate in high-consequence work;
- retraining/calibration creates more operator burden than it removes.

## Open Questions

- What predicts marginal value of more reasoning rather than merely task difficulty?
- How can counterfactual route performance be estimated from single-route production logs?
- Which validators are sufficiently independent of the generator?
- Can useful-context density be measured cheaply enough for online use?
- How quickly do router features decay after model/provider updates?
- When does parallelism create independent error paths versus correlated duplicates?
- What is the smallest telemetry schema that supports reliable routing research?
- How should human attention be priced relative to inference cost?

## References

Core prior work:
- Snell et al. *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters.* arXiv:2408.03314.
- Muennighoff et al. *s1: Simple test-time scaling.* EMNLP 2025.
- Liu et al. *Lost in the Middle.* TACL 2024.
- Hsieh et al. *RULER.* arXiv:2404.06654.
- Jiang et al. *LongLLMLingua.* ACL 2024.
- Chen, Zaharia, Zou. *FrugalGPT.* TMLR 2024.
- Ong et al. *RouteLLM.* ICLR 2025.
- Ding et al. *Hybrid LLM.* ICLR 2024.
- Hu et al. *RouterBench.* arXiv:2403.12031.
- Yang Li. *Rethinking Predictive Modeling for LLM Routing: When Simple kNN Beats Complex Learned Routers.* arXiv:2505.12601.
- Huang et al. *Large Language Models Cannot Self-Correct Reasoning Yet.* ICLR 2024.
- Farquhar et al. *Detecting hallucinations in large language models using semantic entropy.* Nature 2024.
- Dean, Barroso. *The Tail at Scale.* CACM 2013.

2026 refresh:
- Hao Li et al. *LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing.* arXiv:2601.07206. https://arxiv.org/abs/2601.07206
- Agarwal, Jain. *FIRE: Failure-Informed Runtime Engineering for Reliable Language-Model Agents.* arXiv:2609.26048. https://arxiv.org/abs/2609.26048
- Yifei Li, Zihui Gao, Laks V. S. Lakshmanan. *WISERouter: LLM Routing with Workload Budget Constraint.* arXiv:2607.23765. https://arxiv.org/abs/2607.23765
- Dang et al. *Addressable Recall Compaction for Long Context-Window Control in AI Agents.* arXiv:2607.25066. https://arxiv.org/abs/2607.25066
- Wang et al. *When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression.* arXiv:2609.29875. https://arxiv.org/abs/2609.29875
- OpenAI. *Prompt caching.* Accessed 2026-10-03. https://developers.openai.com/api/docs/guides/prompt-caching

## Reconciliation Result

**ACCEPT_WITH_FOLLOWUP.** The next justified step is offline measurement against simple baselines. Do not introduce learned routing, predictive telemetry, or new context-management machinery until it demonstrates incremental validated-work value.
