# Simple Routing Baselines Under Sparse Evidence

**Queue item:** RQ-2026-10-03-006  
**Date:** 2026-10-06  
**Target:** axiom-llc/axiom-research  
**Status:** research only; no online deployment or routing behavior change

## Question

Under low data volume and model/provider drift, which simple routing policies are hardest to beat, and how should AXIOM decide that adaptive routing is not yet justified?

## Executive conclusion

AXIOM should retain **static minimum-capable routing** as the control. The strongest simple challenger is a **deterministic validator-triggered escalation cascade**: start with the least costly route that satisfies explicit capability and authority constraints, then escalate only after a named incompatibility, timeout, failed validator, or other preregistered condition. A coarse static task-class lookup can be tested only where each class has enough recent evidence; under sparse data it fragments the sample and is usually less defensible.

Adaptive routing is not justified until a frozen candidate beats both static baselines on later chronological data after charging model, tool, validation, retry, latency, operator-attention, and router-maintenance overhead. Promotion requires outcome non-inferiority, a worthwhile net resource improvement, adequate action support or direct paired observations, stability across two non-overlapping recent evaluation blocks, and no material harm in a predeclared task/risk stratum. If uncertainty is too wide to decide, the correct result is **INSUFFICIENT_EVIDENCE**, not promotion.

No universal transaction count is defensible. AXIOM must choose risk-specific loss margins and minimum worthwhile savings before looking at the holdout, then collect enough comparable observations to make those margins testable. Until that is possible, use historical data only for a coverage audit and descriptive offline replay. Do not infer unobserved counterfactual model outcomes.

## Decision scope

This artifact defines an offline benchmark and promotion gate. It does not authorize:

- online experimentation or traffic allocation;
- a learned router;
- changes to capability, privacy, authority, safety, or validation gates;
- new provider spend;
- counterfactual claims from single-route logs;
- model/provider performance claims beyond the cited or measured evidence.

Unsupported performance expectations remain hypotheses.

## Evidence

### Evaluation must match deployed traffic and continue after change

OpenAI's current evaluation guidance recommends task-specific evaluation, representative production and expert data, continuous evaluation, and explicit comparison criteria. It also identifies non-representative datasets and "vibe-based" assessment as anti-patterns. Pairwise comparison or classification is generally more reliable than unconstrained model grading. This supports a frozen, task-specific, chronological benchmark rather than a pooled subjective score.

- https://platform.openai.com/docs/guides/evaluation-best-practices

### Canary comparisons require comparable populations and enough time

Google SRE's canary guidance treats a canary as a time-limited comparison between canary and control populations, warns that a small canary can be dominated by variance, and recommends isolating canary/control metrics. It also notes that evaluation intervals must fit the canary duration and that absolute measures matter alongside ratios. This supports separate recent time blocks, paired or comparable task populations, raw denominators, and explicit uncertainty.

- https://sre.google/workbook/canarying-releases/

### AI evidence and context drift over time

NIST AI RMF 1.0 states that AI systems, data, and contexts may change over time, that measurements can be oversimplified or context-insensitive, and that real-world performance may differ from controlled settings. It treats test, evaluation, verification, and validation as lifecycle activities and makes risk tolerance contextual. NIST announced in 2026 that AI RMF 1.0 is being revised; this artifact uses the current published framework as risk guidance, not as a fixed routing standard.

- https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- https://www.nist.gov/itl/ai-risk-management-framework

### Logged routing data has partial-feedback limits

Contextual-bandit logs reveal the outcome only for the action that was taken. Li et al.'s replay estimator is unbiased when the log was generated with randomized action support appropriate to the evaluated policy. Dudík, Langford, and Li show the trade-off between direct reward modeling and inverse-propensity methods: direct estimates can be biased, while inverse-propensity estimates can have high variance where logging probabilities are small; doubly robust estimation can help only when its support and modeling assumptions are met. Policy learning with deficient support cannot recover reliable values for actions that were never or rarely observed.

- https://arxiv.org/abs/1003.5956
- https://arxiv.org/abs/1103.4601
- https://proceedings.mlr.press/v130/sachdeva21a.html

**Consequence for AXIOM:** deterministic production logs without recorded action propensities do not support an unbiased offline comparison of arbitrary alternative routes. A causal estimator must not be invoked as decoration. Use direct paired observations where available; otherwise report the coverage gap.

## AXIOM baseline contract

This artifact builds on `2026-10-05-validated-work-efficiency-metrics-chatgpt.md`:

- validated completion precedes efficiency;
- static minimum-capable routing remains the control;
- task/risk class and route revision are explicit;
- logical-transaction cost includes retries and validation;
- missing usage remains unknown rather than zero;
- human attention is a separate cost;
- no single weighted efficiency score is canonical.

A route is **eligible** only after existing authority, privacy, capability, consequence, reversibility, and validation requirements are satisfied. Routing may optimize only among eligible routes. An inexpensive ineligible route is not a baseline candidate.

## Baseline policies

### B0 — Static minimum-capable global control

For every eligible transaction, use the least costly fixed route that satisfies the declared task capabilities and risk requirements. Freeze the route and revision for the evaluation window.

Why it is hard to beat:

- no model-selection inference cost;
- no training data or calibration loop;
- minimal state and recovery surface;
- behavior is attributable and auditable;
- sparse data does not change the policy.

Failure mode: one global route can be overpowered for a minority of tasks or become stale after provider/model change. Those failures should appear as validator failures, incompatibility events, or revision drift rather than be hidden by a pooled average.

### B1 — Static task-class lookup

Map each predeclared coarse task class to one fixed minimum-capable route. The mapping is chosen on training history, frozen before evaluation, and changed only by an explicit offline review.

Why it may help:

- captures large, stable capability differences without online learning;
- remains deterministic and inspectable;
- has no per-request inference overhead beyond class assignment.

Why it often loses under sparse evidence:

- every added class fragments the sample;
- class definitions can encode hindsight;
- rare classes produce unstable estimates;
- model/provider revision invalidates several cells at once.

Reject or collapse a class whose definition is not available before outcome, whose membership changes during evaluation, or whose holdout evidence cannot test the declared margins.

### B2 — Deterministic validator-triggered escalation

Start with B0. Escalate to one fixed stronger route only when a preregistered event occurs, such as:

- explicit capability incompatibility before execution;
- timeout or provider unavailability;
- schema/format validation failure;
- repository-native test failure;
- independent semantic validator failure;
- bounded retry budget exhausted.

The escalation trigger must be evidence produced by a named validator or runtime state, not a learned score or free-form model preference. The logical transaction owns all attempts and all associated costs.

Why it is the strongest simple challenger:

- spends more only where a detectable failure demands it;
- preserves a deterministic recovery story;
- converts validator evidence into an actionable route without training a router;
- produces paired within-transaction evidence for the failed first attempt and escalated outcome.

Failure mode: if validators are weak, noisy, or expensive, the cascade may miss semantic failures, over-escalate, or cost more than a fixed stronger route. All trigger and escalation overhead must be charged.

### B3 — Static strong-route reference

Use one fixed high-capability eligible route. This is a reference, not the cost control. It estimates whether B0/B2 sacrifice outcomes and exposes cases where the entire "minimum-capable" declaration is wrong.

### B4 — Post-hoc oracle upper bound

For tasks with actual outcomes from more than one route, choose the cheapest successful eligible result after seeing all outcomes. This is deliberately non-deployable. It estimates the maximum benefit that any perfect selector could have achieved on the observed paired subset.

If the oracle's improvement over B0/B2 is smaller than adaptive routing's measured overhead or minimum worthwhile margin, stop: no learned policy can justify itself on that evidence.

### A1 — Adaptive challenger

A frozen learned or bandit-style policy may be evaluated only after B0–B4. It receives only fields available before the routing decision, emits an explicit route and score/reason, and falls back to B0 when inputs or route revisions are unknown. It is never the control.

## Cost and outcome model

Do not promote on token price alone. Evaluate a vector with lexicographic gates.

### Gate 1 — Validated outcome

For candidate (c) and control (b), within each predeclared task/risk stratum:

[
Delta_{success} = p_c(	ext{validated success}) - p_b(	ext{validated success})
]

Choose a maximum tolerable loss (delta_s ge 0) before viewing the holdout. The candidate must establish that its plausible downside is no worse than (-delta_s). Serious authority or safety failures have a zero-tolerance gate unless an external policy explicitly says otherwise.

### Gate 2 — Total measured resource cost

Per logical transaction include:

[
C = C_{model} + C_{tool} + C_{validation} + C_{retry} + C_{latency} + C_{human} + C_{router}
]

Keep each coordinate visible even if an explicit policy later converts some coordinates to a common unit. `C_router` includes classification/inference, telemetry, calibration, evaluation, incident diagnosis, and maintenance overhead. Amortized fixed cost must name its horizon; it cannot be silently omitted.

Define a minimum worthwhile improvement (delta_c) before holdout analysis. A statistically distinguishable but operationally trivial saving does not justify additional failure modes.

### Gate 3 — Stability and diagnosability

The sign and practical magnitude of the gain must remain acceptable across:

- two non-overlapping recent chronological holdout blocks;
- the newest relevant model/provider revision block;
- every material predeclared task/risk stratum;
- raw and retry-inclusive transaction accounting.

A candidate that wins only by pooling old revisions or by hiding one materially harmed stratum fails.

## Time-split evaluation protocol

1. **Declare the data cut.** Record the latest included timestamp, route revisions, eligibility rules, exclusions, and missingness.
2. **Run a coverage audit first.** Count transactions by task class, risk class, route revision, chosen action, validator outcome, and whether alternative-route outcomes actually exist. Record logging propensities if they were captured.
3. **Freeze the benchmark.** Before final evaluation, freeze B0–B4, candidate A1, features, task classes, loss margin (delta_s), worthwhile cost margin (delta_c), and exclusion rules.
4. **Split chronologically.** Use older data for policy construction and threshold selection. Reserve two later, non-overlapping blocks for evaluation. Never randomly shuffle across model/provider revisions.
5. **Prefer paired comparisons.** When the same frozen task input has actual eligible outputs from multiple routes, compare within task. Preserve prompt/tool/policy revisions so the pair is meaningful.
6. **Use observational logs descriptively.** Where only the selected route has an outcome, report route/task coverage and measured outcomes. Do not label another route a counterfactual winner.
7. **Use off-policy estimators only with support.** Replay, inverse-propensity, or doubly robust estimates require known logging behavior, nonzero support for candidate actions, bounded weights, and separation between nuisance-model fitting and evaluation. If any condition fails, mark the estimate unavailable.
8. **Report uncertainty and denominators.** For sparse binary outcomes use an appropriate exact or small-sample interval; for paired continuous/resource differences use paired resampling or a preregistered exact/permutation method. Name the method and report raw counts.
9. **Inspect failures.** Review all serious failures and a fixed sample of ordinary disagreements. A metric win cannot override an unexplained authority, integrity, or validation regression.
10. **Repeat after revision drift.** A provider/model/tool-policy revision starts a new revision block. Old evidence may inform hypotheses but cannot silently certify the new route.

## Sample-size caveats

There is no honest universal minimum (N). Required evidence depends on:

- baseline validated-success rate;
- allowed non-inferiority loss (delta_s);
- minimum worthwhile resource improvement (delta_c);
- outcome variance and task heterogeneity;
- paired versus independent observations;
- number and rarity of task/risk strata;
- action-support probability;
- desired error rates and repeated comparisons;
- model/provider drift rate.

AXIOM should use the stricter of outcome precision and cost precision. Before data collection, compute or simulate the sample needed to make both margins decidable under conservative baseline rates. If the available sample cannot exclude an unacceptable outcome loss or cannot establish worthwhile savings, report **INSUFFICIENT_EVIDENCE**.

Rules for sparse evidence:

- show numerator and denominator, not only percentages;
- prefer intervals and raw paired differences over asymptotic p-values;
- do not pool incompatible revisions to manufacture power;
- do not claim "no difference" from a non-significant result;
- do not create task classes after inspecting failures;
- do not reuse the final holdout to tune the candidate;
- correct or bound claims when testing many policies/strata;
- require replication in the second recent holdout block.

## Promotion gate

Promote an adaptive candidate from research to a separately authorized shadow test only when all conditions hold:

1. **Scope:** all candidate routes pass existing eligibility and authority gates.
2. **Frozen comparison:** features, policies, margins, costs, and exclusions were fixed before final holdout scoring.
3. **Outcome non-inferiority:** the one-sided lower confidence bound for (Delta_{success}) clears (-delta_s) overall and in every material risk stratum.
4. **No serious regression:** no new authority, safety, integrity, privacy, or unverifiable-success failure appears.
5. **Worthwhile net benefit:** after all routing overhead, the confidence bound for improvement clears the preregistered (delta_c) in at least one important resource dimension without an unacceptable regression in another.
6. **Simple-baseline dominance:** A1 beats B0 and B2; the observable oracle B4 leaves enough headroom to pay for A1.
7. **Support:** every material A1 action has direct paired evidence or valid logged-action support. Unsupported actions fail the gate.
8. **Temporal replication:** the result clears gates in both non-overlapping recent holdout blocks and remains acceptable on the newest route revision.
9. **Stratum integrity:** no material task/risk class is harmed beyond its declared margin; class definitions were fixed in advance.
10. **Diagnosability:** every routing decision, fallback, validation result, and cost is attributable from durable evidence.
11. **Reversibility:** the candidate defaults to B0 on unknown inputs and can be disabled without ambiguous transaction state.
12. **Independent authorization:** this research does not self-authorize implementation, online shadowing, provider spend, deployment, or release.

Any failed or undecidable condition retains B0/B2.

## Rejection and stop conditions

Reject the adaptive candidate, or stop collecting under the current design, when any of the following is true:

- deterministic logs lack action propensities and paired route outcomes are too rare;
- candidate actions have deficient support;
- uncertainty remains wider than the predeclared outcome or cost margins;
- apparent gains disappear after retry, validation, latency, human, or router overhead;
- gains depend on old route revisions or one time block;
- a simpler task-class lookup or deterministic cascade matches the gain;
- task classes are unstable or too sparse;
- router features leak post-outcome information;
- calibration or maintenance effort exceeds observed savings;
- a serious failure cannot be explained and bounded;
- the B4 oracle shows too little attainable headroom;
- added instrumentation or policy complexity is not addressable and auditable.

"Reject" means retain the static policy. It does not prove adaptive routing can never help; it says the current evidence cannot justify the additional mechanism.

## Zero-incremental-cost remote MVE

Run an offline **coverage-and-headroom study** using existing durable telemetry and already-produced outputs. Do not call providers, route live work, or synthesize missing outcomes.

### Phase 0 — Evidence inventory

For the complete available data cut, produce one table with:

- transaction and timestamp;
- task/risk class;
- route revision and selected route;
- logging propensity, if actually recorded;
- claimed and independently validated outcome;
- model/tool/validation/retry/latency/human cost fields;
- alternative-route outcome references, if actually available;
- missingness and exclusion reason.

Success criterion: every included field is traceable to an addressable receipt. Otherwise the MVE ends with a telemetry-gap report.

### Phase 1 — Baseline replay

Without generating new model outputs:

- apply B0 and B1 only where the chosen historical action matches the baseline;
- reconstruct B2 from recorded validator/timeout events and actual escalation attempts;
- score B3 only on tasks actually executed on the strong route;
- compute B4 only on the paired subset with multiple actual eligible outcomes.

Report coverage separately from performance. Do not fill unobserved route/task cells.

### Phase 2 — Headroom decision

- If B4 cannot improve enough over B0/B2 to exceed (delta_c) plus plausible router overhead, reject A1.
- If B4 shows headroom but evidence support is inadequate, return **INSUFFICIENT_EVIDENCE** and specify the smallest future paired-data collection needed.
- If support is adequate, freeze one A1 candidate and the full protocol before touching either holdout block.
- Evaluate both blocks once. No retuning after the first result.

Expected near-term outcome under sparse AXIOM telemetry: a coverage receipt and either rejection or insufficient evidence, not deployment. This is an **UNVALIDATED_HYPOTHESIS** until the inventory is run.

## Falsifiable hypotheses

- **H1:** B2 reduces unnecessary strong-route use relative to B3 without exceeding the declared validated-success loss margin.
- **H2:** After all overhead, B2 matches or exceeds the net benefit of any evaluated A1 candidate.
- **H3:** At least one coarse B1 class lacks enough recent within-revision evidence to test its margins, making the global B0 safer.
- **H4:** Retry- and validation-inclusive accounting reverses at least one ranking produced by model-price-only accounting.
- **H5:** The paired-subset B4 oracle leaves too little headroom to pay for an adaptive router.
- **H6:** Route-revision drift changes candidate rankings across the two recent holdout blocks.
- **H7:** Existing deterministic logs lack sufficient action support for valid inverse-propensity or doubly robust evaluation.

Reject each hypothesis when the preregistered analysis on traceable evidence shows the opposite. None of these hypotheses authorizes a routing change.

## Manager classification

**ACCEPT_WITH_FOLLOWUP.**

The benchmark is implementable as an offline research analysis, but the immediate recommendation is conservative: keep static minimum-capable routing and its deterministic validator-triggered escalation challenger. First run the zero-cost coverage-and-headroom MVE. Prepare no adaptive-router implementation candidate until evidence support, margins, ownership, and a repository-native validation path are explicit.
