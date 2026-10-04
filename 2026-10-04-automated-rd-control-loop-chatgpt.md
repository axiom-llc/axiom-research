# Fully automated research-to-development control loop

**Queue item:** RQ-2026-10-04-016  
**Research date:** 2026-10-04  
**Scope:** smallest safe branch/PR-only AXIOM R&D architecture

## Conclusion

AXIOM does not need a second autonomous orchestration architecture. The smallest safe design is the existing Director R&D loop with four hard boundaries: a pre-write admission gate, one canonical research queue, isolated machine-owned branches, and independent PR/CI review before canonical integration. Research may propose implementation, but it must not grant implementation authority or certify its own effects.

The recommended state machine is:

`READ_GATE -> RECONCILE_WIP -> SELECT_ONE -> RESEARCH -> WRITE_ARTIFACT -> VERIFY_ARTIFACT -> COMPLETE_QUEUE_ON_BRANCH -> VALIDATE -> OPEN_PR -> [OPTIONAL_DERIVED_IMPL_BRANCH -> VALIDATE -> OPEN_PR] -> STOP`

Any failed authority, provenance, validation, or freshness check transitions to `READ_ONLY/BLOCKED`, not a weaker execution mode.

## Evidence

Current GitHub branch protection supports required approving reviews, required status checks, conversation resolution, restrictions on pushes, and preventing bypass. Required checks must succeed against the latest commit SHA. These controls make branch/PR isolation a native enforcement surface rather than an AXIOM-specific merge mechanism.

- GitHub, *About protected branches*: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub, *Troubleshooting required status checks*: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

GitHub also warns that `pull_request_target` can expose write privileges or secrets when untrusted PR code is executed. R&D validation should therefore prefer ordinary `pull_request` execution and must not introduce privileged PR-head execution merely to automate validation.

- GitHub, *Events that trigger workflows*: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- GitHub, *Securely using pull_request_target*: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

OpenAI's current Agents SDK separates tool guardrails from human approval and supports serializing interrupted run state for later resumption. Its tracing model records task, turn, generation, function-tool, guardrail, and handoff spans. These are implementation examples—not requirements—but they support two useful design principles: validate at effect boundaries and make long-running work resumable from explicit durable state rather than hidden model context.

- OpenAI Agents SDK, *Guardrails*: https://openai.github.io/openai-agents-js/guides/guardrails/
- OpenAI Agents SDK, *Human-in-the-loop*: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/
- OpenAI Agents SDK, *Tracing*: https://openai.github.io/openai-agents-js/guides/tracing/

NIST's AI RMF resources emphasize testing, evaluation, verification, and validation (TEVV). This supports preserving independent validation as a distinct stage rather than treating model confidence or successful generation as proof of correctness.

- NIST AI Resource Center: https://airc.nist.gov/
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework

## Minimal authority contract

| Stage | Read | Write | Forbidden effect |
|---|---|---|---|
| Admission/reconcile | gate, workflows, queue, branches, PR/CI | none | all mutations before admission |
| Research | authoritative sources + bound repo revisions | research branch only | canonical state, external submission |
| Queue transition | branch-local queue copy | selected item only | manual-target reroute, canonical queue write |
| Validation | branch revision + tests/checks | validation artifacts only if needed | weakening checks |
| Publication | validated head revision | PR create/update | merge |
| Derived implementation | accepted evidence + owner repo | separate `-impl` branch | research self-authorizing merge/release |

Capability is therefore monotonic within a cycle: later stages may use only the authority admitted at cycle start; no output can widen it.

## Deterministic selection and WIP

1. Reconcile any open `automation/rd/*` branch or PR first.
2. Otherwise select only `QUEUED && target == "chatgpt"`.
3. Sort by `priority asc -> value_score desc -> created_at asc -> id asc`.
4. Bind the cycle to the selected queue ID and repository revisions.
5. Keep WIP to one research item and at most one directly derived implementation candidate.

Manual `claude-manual` and `gemini-manual` items are never rerouted.

## Evidence acquisition and Research-Manager reconciliation

For each material claim:

- prefer primary/authoritative current sources when behavior can drift;
- record source URL and retrieval/research date;
- distinguish observed repository state, external evidence, synthesis, hypothesis, and unknown;
- reject unsupported numeric precision;
- treat contradictory evidence as unresolved until explicitly reconciled;
- re-read the durable artifact before moving the branch-local queue item to `COMPLETE`.

A model-generated artifact is evidence input, not an execution receipt.

## Implementation gate

Create a software candidate only if all three are explicit:

1. **owner** — exact repository/component responsible;
2. **change** — bounded behavior or defect supported by the research/evidence;
3. **validation** — executable test/check capable of falsifying the candidate.

Otherwise stop with the research PR. The implementation uses `automation/rd/<work-id>-impl`, never the research branch, so research acceptance and code acceptance remain independently reviewable.

## Failure and recovery semantics

Persist only durable checkpoints: selected work ID, bound revisions, artifact path, queue state on the branch, validation result, and PR identity. On restart, reconcile remote branches/PRs before selecting new work.

| Failure | Required action |
|---|---|
| admission stale/failed | read-only stop |
| source unavailable | preserve uncertainty; block if decision-critical |
| artifact write/read-back mismatch | do not complete queue item |
| validation failure | repair only evidence-supported scope; otherwise block |
| PR/branch already exists | resume/converge; do not duplicate |
| base branch drift | refresh evidence/validation where material |
| implementation ownership unclear | research-only stop |
| marginal useful value exhausted | convergence stop |

Retries should be bounded to failures with a plausible transient cause. Repeating a deterministic failure without new evidence is not progress.

## Provider/channel routing

The queue target is an authority boundary, not merely a model preference:

- `chatgpt`: eligible for automated R&D after admission.
- `claude-manual`, `gemini-manual`: remain manual.
- Research-Manager reconciliation may consume completed artifacts but cannot rewrite target semantics to gain automation authority.

No provider result may certify the external effect that it requested.

## Zero-cost incremental implementation plan

1. **Keep current queue and workflows.** No new scheduler state database.
2. **Use the existing admission gate** before every write-capable cycle.
3. **Use GitHub branch/PR state as the durable execution ledger** for WIP and recovery.
4. **Require artifact read-back plus queue validation** before branch-local completion.
5. **Use existing repository CI/status checks** for candidate validation; do not create privileged validation paths.
6. **Add telemetry only when a missing measurement blocks evaluation:** work ID, bound SHAs, latency, retries, validation result, durable findings, software changes, human interventions, downstream merge outcome.

## Falsifiable promotion gates

The design is worth retaining only if repeated remote cycles show:

- no mutation when admission is stale;
- no duplicate WIP under restart/retry;
- deterministic eligible-item selection;
- branch-local queue mutation limited to the selected item;
- artifact read-back before completion;
- validation tied to the exact candidate revision;
- zero self-merges/releases/spend/external sends;
- implementation PRs occur only with explicit owner/change/validation evidence.

Reject or revise the design if any invariant requires a second canonical queue, hidden runtime state for recovery, privileged CI execution of untrusted branch code, or research output to grant itself effect authority.

## Uncertainty

This research establishes a control architecture, not proof that every repository currently enforces equivalent branch protection or CI. Repository-specific protection/ruleset configuration must be independently inspected when it becomes decision-critical. Likewise, OpenAI Agents SDK behavior is cited as current implementation evidence, not as an AXIOM dependency.

## Direct implementation candidate

No new software implementation is justified by this artifact alone. The current Director `rd-loop.md` already embodies the minimal architecture above. Creating parallel orchestration code would add authority surface without demonstrated benefit. The correct next evidence is repeated bounded-cycle telemetry and review outcomes; only observed friction or a concrete defect should trigger a code candidate.
