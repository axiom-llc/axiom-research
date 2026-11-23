# Independent technical evaluation

This public protocol helps an engineering reviewer assess reproducible AXIOM work without mistaking architectural intent, retained synthetic results, or a passing test for production assurance.

## Evaluation order

1. **Pin the revision.** Record the exact Git commit and relevant artifact blob IDs before testing.
2. **Establish scope.** Identify the claimed behavior, synthetic or production environment, tested configuration, acceptance contract, and limits.
3. **Inspect evidence.** Cross-check the [portfolio summary](simulations/portfolio-summary.json), domain [claims](simulations/claims/), [accepted evaluation records](simulations/), and [cross-domain findings](simulations/cross-domain-findings.md). Keep reported effects distinct from actual customer outcomes.
4. **Validate public contracts.** Run the checks below in an isolated checkout. Preserve interpreter version, installed dependencies, complete output, exit codes, and failures.
5. **Review engineering boundaries.** Inspect [architecture invariants](architecture/ARCHITECTURE.md), [schemas](architecture/schemas/), [simulation runner](simulations/runner.py), and [publication controls](PUBLICATION.md).
6. **Classify the conclusion.** State what passed, what remains unverified, and what additional evidence a production or commercial claim would require.

## Public reproduction commands

```bash
python3 -m pip install -r architecture/tests/requirements.txt
python3 -m pip install -r simulations/tests/requirements.txt
python3 research_queue_check.py research-queue.json
python3 architecture/tests/check.py
python3 simulations/tests/validate.py
python3 .github/scripts/publication_check.py
```

Run from the repository root in a Git checkout. The two dependency files declare test-time packages; no live agent services or external accounts are required for the checks above.

## What can and cannot be concluded

| Evidence | Supported conclusion | Not established |
| --- | --- | --- |
| Public schema and fixture checks | Published interfaces and provided examples satisfy their validation rules in the tested environment | Complete or secure production implementation |
| Retained accepted simulation evidence | A recorded synthetic workload met the documented acceptance checks at its source revision | Real-world delivery, autonomous professional authority, or customer impact |
| Architecture invariants | Explicit intended responsibilities, authority boundaries, and design constraints are documented | Deployment, runtime enforcement, or universally proven security |
| [RSI comparison](rsi/implementation-review-2026-11-08.md) | Recorded bounded Python performance and behavior comparisons | General workload speedup, production ROI, or implementation approval |

The [simulation runner](simulations/runner.py) is **not a standalone public replay**: integrated operation depends on sibling ASON/APEX sources, configured service access, and separate authorization. Follow [simulations/README.md](simulations/README.md) for that boundary.

Keep failures and inconclusive cases in the report. Separate source-backed observations from interpretation, hypotheses, and forward-looking engineering opportunities. Public availability is not a promise of independent audit certification.
