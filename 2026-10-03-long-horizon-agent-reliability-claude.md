# Long-Horizon Agent Reliability

**Date:** 2026-10-03  
**Author channel:** Claude (manual), reconciled by AXIOM  
**Target:** `axiom-llc/axiom-research`

## Provenance

- Owner-supplied source SHA-256: `8280fd074af4a91ffe015fa74543ca9abfb7d656aac08b91d49c2bcc8eedf986`.
- The source explicitly stated that it had **not** performed live retrieval and that its 2026 literature coverage was incomplete.
- AXIOM refreshed decision-critical claims against primary/current sources on 2026-10-03 and removed or downgraded claims that could not be supported.
- This artifact is research input. It does not establish implemented AXIOM behavior or authorize architectural changes.

Evidence labels: **[E]** established/widely corroborated · **[P]** primary but preliminary/single-study · **[S]** synthesis · **[H]** hypothesis.

## Research Question

Why do autonomous LLM-agent systems lose reliability as task horizon increases, and which mechanisms most effectively preserve correctness across long-running, multi-step execution?

## Executive Findings

1. **[E/P] Reliability decreases with task horizon, but horizon is multidimensional.** Step count, wall-clock duration, and session count should be measured separately. METR's time-horizon work, repeated-success metrics such as `pass^k`, and 2026 long-horizon benchmarks all show that single-attempt capability is not equivalent to reliable long-duration execution.
2. **[P] 2026 evidence strengthens failure-localization as a first-class measurement problem.** Traverse analyzes 2,518 long-horizon trajectories and 6,967 mistakes; frontier judges locate the first mistake in fewer than one third of long runs. HORIZON reports nonlinear degradation and increasing planning/memory failures across 3,100+ trajectories.
3. **[E] Intrinsic self-correction is not a dependable verifier.** External evidence such as tests, tool read-back, deterministic validators, and independent checks is materially stronger than generic “reconsider” loops.
4. **[P] Targeted runtime controls look more promising than universal verification.** FIRE reports gains from failure-conditioned policies on Terminal-Bench 2.1 while generic verification/reconsideration controls do not provide the same benefit.
5. **[S] AXIOM's largest near-term research gap is measurement, not a wholesale architecture redesign.** Existing bounded tasks, durable state, explicit effect boundaries, and postcondition checking are directionally aligned with classical dependability engineering; what is missing is stronger attribution of failures and resource waste.

## Definitions

- **Task horizon:** report dependent step count, elapsed wall time, and session count separately.
- **Verified completion:** required postconditions are confirmed from authoritative evidence rather than the acting model's assertion.
- **Claimed completion:** the actor states that the task is complete.
- **Root failure:** earliest incorrect state/action that changes the trajectory.
- **Detection point:** step at which the failure becomes recognized.
- **Detection latency / wasted work:** work performed between root failure and detection.
- **Recovery rate:** fraction of detected failures returned to a correct trajectory without human intervention.

A useful baseline is `R(H)=(1-λ)^H`, but this is only a null model. Real trajectories violate independence because earlier mistakes change later context, tool state, and reachable actions.

## Current Evidence

### Horizon degradation

- METR, *Measuring AI Ability to Complete Long Tasks* (2025), operationalizes task-completion horizons and reports rapid historical growth in the 50%-success horizon. The result is capability evidence, not proof of robust high-reliability operation.
- Khanal, Tao, Zhou, *Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents* (arXiv:2603.29231), evaluates 10 open models over 23,392 episodes and explicitly separates capability from repeated reliability as task duration changes. **[P]**
- Wang et al., *The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break* (arXiv:2604.11978), reports 3,100+ trajectories across Web, OS, Embodied, and Database domains, with nonlinear performance collapse and increasing planning/memory failures as horizon grows. **[P]**
- Rahman et al., *Locating Hidden Failures Makes Long-Horizon Agents More Reliable* (arXiv:2609.17930), analyzes 2,518 trajectories and 6,967 mistakes and releases human-verified long-horizon failure-localization data. **[P]**

### Self-conditioning and context

Earlier work on lost-in-the-middle effects, effective context limits, multi-turn degradation, and self-conditioning supports the narrower claim that adding trajectory history can reduce rather than monotonically increase effective reliability. This does **not** imply that every long context is harmful; relevant externalized state can improve reliability.

### Verification and correction

- Huang et al. (2023), Stechly et al. (2024), and Kamoi et al. (2024) show limits of unsupported intrinsic self-correction on reasoning/planning tasks. **[E within those task classes]**
- Executable tests, direct read-back, schema checks, and other externally grounded signals provide stronger correction mechanisms.
- Agarwal & Jain, *FIRE: Failure-Informed Runtime Engineering for Reliable Language-Model Agents* (arXiv:2609.26048), reports that targeted failure-conditioned runtime policies improve repeated success while generic verification/reconsideration arms are much weaker. **[P]**
- Traverse shows that knowing a trajectory failed is easier than locating the first failure; specialized failure localization can outperform general frontier judges. **[P]**

## Failure Taxonomy

| Class | Operational signature | Preferred countermeasure |
|---|---|---|
| Model/reasoning | Wrong inference/tool arguments with correct state and plan | stronger/decomposed reasoning, external validation |
| Planning | Missing preconditions or infeasible ordering | bounded decomposition, precondition validation, replanning |
| State/memory | stale facts, lost constraints, contradictory state | durable structured state, provenance, invalidation |
| Tool/channel | timeout, partial effect, schema drift, rate limit | idempotency, bounded retry, read-after-write |
| Environment drift | authoritative world changes after observation | action-time refresh/revision binding |
| Verification | false accept/reject, correlated validator failure | independent deterministic/read-back validators |
| Orchestration/harness | duplicate dispatch, bad resume, lost task | deterministic state machine, fault injection |
| Human interface | ambiguity, approval fatigue, stale authorization | explicit bounded approvals and assumptions |

Attribute the **root** class separately from contributing later failures.

## Evaluation Methodology

AXIOM should extend binary success with:

| Metric | Definition |
|---|---|
| `R(H)` | verified success versus step count, elapsed time, and session count |
| Claimed-vs-verified gap | rate of actor completion claims not supported by postconditions |
| Root failure class | earliest causal failure category |
| Detection latency | steps/tokens/time from root failure to recognition |
| Wasted work | resource use after root failure and before detection |
| Recovery rate | fraction of detected failures recovered autonomously |
| Human intervention rate | required escalations per task |
| Verifier yield | failures caught / verifier calls, plus false accepts/rejects where audited |
| UNKNOWN rate | ambiguous-effect outcomes requiring reconciliation |
| Retry amplification | physical attempts per logical operation |
| Constraint retention | preservation of pinned requirements across handoffs/compaction |

Benchmark design should control horizon separately from difficulty, pin model/harness revisions, use deterministic oracles wherever possible, and distinguish infrastructure/tool failure from model failure.

## Implications for AXIOM

1. Preserve current bounded-task and explicit-postcondition principles as the **baseline**, not as proven optimum.
2. Add failure-class, root/detection position, recovery path, and claimed-vs-verified fields before introducing new routing or memory architecture.
3. Audit session-handoff constraint retention.
4. Audit validator independence: the actor should not be able to manufacture the evidence that certifies its own effect.
5. Treat generic reflection as low-priority unless it beats deterministic/targeted validation on measured AXIOM workloads.
6. Evaluate Harness/direct execution by reliability-versus-horizon rather than assuming either is superior.

## Testable Hypotheses

- **H1 [H]** Verified success declines faster with long horizon than an independence model fitted only to short tasks predicts.
- **H2 [H]** At least 10% of long-horizon AXIOM failures originate in state/tool/orchestration rather than model reasoning.
- **H3 [H]** Independently validated workflows have a materially smaller claimed-vs-verified completion gap than self-reported workflows.
- **H4 [H]** Per-effect deterministic validation reduces root-to-detection wasted work by at least 20% relative to end-only validation at comparable completion rate.
- **H5 [H]** Re-reading durable constraints before consequential effects improves session-handoff constraint retention.
- **H6 [H]** Deterministic fault injection exposes non-zero harness failures even when the model is replaced with a scripted oracle.
- **H7 [H]** Blind retry after UNKNOWN effects produces more duplicate effects than read-and-reconcile.
- **H8 [H]** After two unchanged deterministic failures, switching/replanning has higher validated-work efficiency than another identical retry.
- **H9 [H]** Actor and validator errors are more correlated when they share model/session context than when validation reads authoritative state independently.
- **H10 [H]** Later same-type steps exhibit higher error rates than earlier ones after controlling for task difficulty.

## Minimum Viable Experiment

**Goal:** produce the first AXIOM reliability-vs-horizon dataset without changing production behavior.

### Part A — historical telemetry

1. Read existing authoritative remote receipts/telemetry.
2. Use **ChatGPT session-hosted Python/SQLite or GitHub Actions**, never the Owner workstation, to derive horizon fields and validation outcomes.
3. Compute `R(H)`, claimed-vs-verified gap, retry amplification, recovery rate, and root-to-detection distance where evidence exists.
4. Preserve unknowns instead of inventing missing labels.

### Part B — deterministic fault injection

1. Run synthetic N-step workflows in an isolated GitHub Actions workspace or dedicated remote test repository.
2. Replace the model with a deterministic scripted oracle.
3. Inject timeout-after-effect, duplicate delivery, stale revision, truncated-state, and interrupted-resume faults.
4. Compare blind retry versus read-and-reconcile.
5. Record duplicates, recovery correctness, and detection latency.

### Part C — handoff retention

Use session-hosted compute or CI to replay the existing handoff representation and deterministically grade preservation of pinned constraints.

**Incremental hosted spend:** `$0.00`.  
**Stop condition:** if historical evidence lacks step-level granularity, record that gap and run only deterministic Parts B/C.

## Open Questions

- Does self-conditioning reproduce on contemporary tool-using AXIOM trajectories?
- Is elapsed-time drift more important than step count for multi-day tasks?
- How correlated are actor and verifier errors across model families?
- Which checkpoint interval minimizes verifier cost plus wasted-work risk?
- How much state loss comes from compaction versus planning drift?
- Do 2026 HORIZON/Traverse/FIRE results replicate on AXIOM-like remote tool workflows?

## References

Primary/current refresh:
- Khanal, Tao, Zhou. *Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents.* arXiv:2603.29231 (2026). https://arxiv.org/abs/2603.29231
- Wang et al. *The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break.* arXiv:2604.11978 (2026). https://arxiv.org/abs/2604.11978
- Rahman et al. *Locating Hidden Failures Makes Long-Horizon Agents More Reliable.* arXiv:2609.17930 (2026). https://arxiv.org/abs/2609.17930
- Agarwal, Jain. *FIRE: Failure-Informed Runtime Engineering for Reliable Language-Model Agents.* arXiv:2609.26048 (2026). https://arxiv.org/abs/2609.26048
- Kwa et al. *Measuring AI Ability to Complete Long Tasks.* arXiv:2503.14499 (2025). https://arxiv.org/abs/2503.14499

Retained foundational/earlier literature:
- Ross, Gordon, Bagnell. DAgger. AISTATS 2011.
- Garcia-Molina, Salem. *Sagas.* SIGMOD 1987.
- Saltzer, Reed, Clark. *End-to-End Arguments in System Design.* ACM TOCS 1984.
- Candea, Fox. *Crash-Only Software.* HotOS 2003.
- Liu et al. *Lost in the Middle.* arXiv:2307.03172.
- Hsieh et al. *RULER.* arXiv:2404.06654.
- Huang et al. *Large Language Models Cannot Self-Correct Reasoning Yet.* arXiv:2310.01798.
- Stechly et al. *On the Self-Verification Limitations of LLMs on Reasoning and Planning Tasks.* arXiv:2402.08115.
- Kapoor et al. *AI Agents That Matter.* arXiv:2407.01502.

## Reconciliation Result

**ACCEPT_WITH_FOLLOWUP.** Preserve the measurement program and falsifiable hypotheses. Do not infer that any new architecture is justified until AXIOM produces its own horizon-conditioned evidence.
