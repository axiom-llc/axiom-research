# AXIOM Research

**Evidence-driven engineering research on reliable AI-assisted systems, bounded autonomy, and verifiable execution.**

This public repository contains source code, machine-readable contracts, deterministic synthetic simulations, retained evaluation evidence, and carefully scoped research summaries. It is an inspectable technical portfolio—not a claim of production deployment, external customer results, or unrestricted autonomous authority.

**For engineering reviewers, employers, and prospective clients:** start with the accepted [simulation evidence](simulations/portfolio-summary.json), review the [architecture contract](architecture/ARCHITECTURE.md), and follow the [independent evaluation guide](independent-review-target.md).

## Selected engineering work

| Work | What can be inspected | Evidence |
| --- | --- | --- |
| **Multi-domain workflow simulation** | Five synthetic organizational models; task dependencies, approvals, fault injection, recovery, and local-file effects | [Portfolio summary](simulations/portfolio-summary.json) · [cross-domain findings](simulations/cross-domain-findings.md) |
| **Bounded agent architecture** | Separation of prioritization, durable task progression, policy authorization, execution, and retrieval; 33 stable public invariants | [Architecture](architecture/ARCHITECTURE.md) · [schemas](architecture/schemas/) · [checks](architecture/tests/) |
| **Evidence-first verification** | JSON-schema validation, positive/negative fixtures, deterministic acceptance, provenance and publication screening | [Simulation tests](simulations/tests/) · [publication gate](.github/scripts/publication_check.py) · [review protocol](independent-review-target.md) |
| **Research-source optimization experiment** | Exact-source candidate generation, behavioral holdouts, comparative timing, and explicit non-promotion when broader acceptance is incomplete | [RSI experiment](rsi/README.md) · [implementation review](rsi/implementation-review-2026-11-08.md) |

### Quantified synthetic evidence

The retained [accepted portfolio record](simulations/portfolio-summary.json) covers **five domains, 74 modeled workflow steps, 27 approval-bearing steps, 11 injected exception cases, and 74 recorded local-file execution effects/events**. These totals describe the recorded synthetic demonstrations at their cited source revisions, not deployed processes or independently measured customer impact.

| Domain | Example engineering challenge | Detailed evidence |
| --- | --- | --- |
| Robotics production | Engineering-to-assembly coordination, quality checks, defect handling, recovery | [Case study](simulations/case-studies/robotics-production.md) |
| Software development | Delivery, authorization, acceptance tests, exception handling | [Case study](simulations/case-studies/software-development.md) |
| Security operations | Alert triage, evidence capture, workflow control | [Case study](simulations/case-studies/soc-operations.md) |
| Logistics and supply chain | Inventory allocation, fulfillment, delivery exceptions | [Case study](simulations/case-studies/logistics-supply-chain.md) |
| Specialty-care administration | Synthetic referral, scheduling, record and coverage coordination | [Case study](simulations/case-studies/specialty-care-administration.md) |

## Engineering capabilities and research methods

- **System architecture:** component contracts, explicit authority boundaries, machine-readable interfaces, and traceable design invariants.
- **Reliability and recovery:** failure injection, deterministic state reconstruction, bounded retries, unknown-outcome handling, and acceptance tests.
- **Validation and provenance:** exact-revision/source-digest references, schema checks, negative fixtures, retained evidence, and reproducible comparison methods.
- **Security-aware design:** policy authorization, supply-chain identity, sensitive-data boundaries, and evidence-based claims instead of unverified guarantees.
- **Technical research:** source assessment, competing hypotheses, falsifiable evaluation plans, limitations, and careful separation of observed results from proposed designs.

The architecture and demonstrations establish **inspectable engineering practices** within their stated scope. Security assurance, production reliability, real-world safety, regulatory compliance, and commercial return require additional evidence specific to a deployed system.

## Reproduce the public checks

Use Python 3 and a Git checkout of this repository. Install the declared validation dependencies:

```bash
python3 -m pip install -r architecture/tests/requirements.txt
python3 -m pip install -r simulations/tests/requirements.txt
```

From the repository root:

```bash
python3 research_queue_check.py research-queue.json
python3 architecture/tests/check.py
python3 simulations/tests/validate.py
python3 .github/scripts/publication_check.py
```

These commands validate the public queue, architecture contract, synthetic fixtures, and disclosure-screening rules. They **do not rerun the recorded ASON/APEX executions** or independently reproduce third-party operational outcomes. Integrated replay through [the simulation runner](simulations/runner.py) has additional owning-repository, service, and authorization dependencies documented in the [simulation guide](simulations/README.md). Existing GitHub workflow definitions are not proof of currently available CI or a passing run.

For a review plan that distinguishes reproducibility, evidence provenance, and deployment assertions, use [Independent technical evaluation](independent-review-target.md).

## Research library

Public summaries cover [long-horizon agent reliability](2026-10-03-long-horizon-agent-reliability-claude.md), [tool identity and supply-chain controls](2026-10-05-agentic-mcp-tool-supply-chain-identity-chatgpt.md), [verified execution boundaries](2026-10-06-canonical-verified-execution-boundary-chatgpt.md), [AI feedback/optimization structures](ai-loop-architecture-taxonomy.md), and [temporal-state research](temporal-state-resolution.md). Many are intentionally short, **redacted public abstracts**, not full technical papers.

The [public research queue](research-queue.json) and [research workflow](research-workflow.md) show disclosure-safe research questions and methodological controls. Queue entries do not authorize execution or imply that a proposal has been implemented.

## Repository guide

- [`architecture/`](architecture/) — canonical public architecture, schemas, invariants, tests, and change record.
- [`simulations/`](simulations/) — domain models, executable simulation support, synthetic fixtures, case studies, and retained accepted evidence.
- [`rsi/`](rsi/) — bounded optimization experiment, source-anchored candidate generator, tests, and acceptance limitations.
- [`security/`](security/) and [`for-evaluation/`](for-evaluation/) — reviewed public research abstracts and evaluation topics.
- [`independent-review-target.md`](independent-review-target.md) — reproducible technical-review procedure.
- [`PUBLICATION.md`](PUBLICATION.md) — disclosure boundaries, provenance requirements, and publication review.

## Engagement and rights

AXIOM's related implementation repositories include [APEX](https://github.com/axiom-llc/axiom-apex), [ASON](https://github.com/axiom-llc/axiom-ason), and [RAG](https://github.com/axiom-llc/axiom-rag). They have separate implementation authority and acceptance evidence. [AXIOM's website](https://axiom-llc.github.io/) provides the public engagement entry point.

See [publication control](PUBLICATION.md) and the scoped [license](LICENSE). The MIT grant applies to AXIOM-authored executable software and validation/test code; research prose, evidence, marks, and third-party materials retain their separate rights.
