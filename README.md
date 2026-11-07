# AXIOM Research

**Evidence-driven research in agent reliability, systems architecture, and autonomous workflows.**

AXIOM Research publishes reproducible synthetic demonstrations, independently inspectable evidence, architectural contracts, and selected research summaries. Internal engineering strategies, unpublished manuscripts, private research, operational account information, and confidential material are retained outside this public repository.

## Demonstrated capabilities

The [organizational simulations](simulations/README.md) exercise five distinct synthetic domains through common evaluation and evidence contracts:

| Domain | Demonstration |
| --- | --- |
| Robotics production | Multi-stage engineering, assembly, test, recovery, and simulated field feedback |
| Software development | Delivery workflow with acceptance, authorization, and exception handling |
| Specialty-care administration | Synthetic referral, records, coverage, and scheduling workflow |
| Security operations | Synthetic alert triage and evidence collection |
| Logistics and supply chain | Inventory, allocation, and delivery-exception workflow |

The accepted portfolio records **74 modeled steps, 27 approval-bearing steps, 11 deterministic exception injections, and 74 recorded local-file execution effects/events**. The evidence is revision- and hash-bound.

[Evidence index](simulations/portfolio-summary.json) · [Cross-domain findings](simulations/cross-domain-findings.md) · [Case studies](simulations/case-studies/) · [Reproduction guide](simulations/README.md)

**Evidence boundary:** These are deterministic **synthetic local-file** simulations, with accepted recorded results. They do not demonstrate production deployment, real-world throughput, external-effect exactly-once guarantees, regulatory compliance, or independent professional authority.

## Public architecture

The [architecture contract](architecture/ARCHITECTURE.md) describes component responsibilities and 33 stable, publicly reviewable governing invariants. Machine-readable [schemas](architecture/schemas/) and [validation tests](architecture/tests/) provide compatibility and consistency checks.

At a high level, AXIOM separates human authorization and strategic prioritization from task progression, bounded execution, policy validation, and retrieval. Interfaces and implementation-specific claims must be verified against their owning repositories and accepted evidence.

## Research summaries

These publications are **reviewed public abstracts** of more detailed retained research. They are intended to describe questions, methods, limitations, and externally useful findings without exposing restricted implementation material.

| Topic | Public summary |
| --- | --- |
| Agent reliability | [Long-horizon reliability](2026-10-03-long-horizon-agent-reliability-claude.md) |
| Security | [Tool supply-chain identity](2026-10-05-agentic-mcp-tool-supply-chain-identity-chatgpt.md) · [Cross-step exfiltration controls](2026-10-05-minimal-sequence-aware-exfiltration-policy-chatgpt.md) |
| Verification | [Verified execution boundaries](2026-10-06-canonical-verified-execution-boundary-chatgpt.md) · [Telemetry composition](2026-10-06-execution-telemetry-composition-boundary-chatgpt.md) |
| Optimization | [AI loop taxonomy](ai-loop-architecture-taxonomy.md) · [Recursive optimization](recursive-hyper-optimization.md) |
| Research methods | [Long-running state](temporal-state-resolution.md) · [J-space program](j-space-research.md) |

The [public research queue](research-queue.json) and [public workflow](research-workflow.md) contain only disclosure-safe research directions. The full manual research queue, original prompts, and confidential working artifacts are managed privately. Public queue entries confer no implementation, publication, permission, or spending authority.

## Reproduce and verify

With a suitable Python environment:

```bash
python3 research_queue_check.py research-queue.json
python3 architecture/tests/check.py
python3 simulations/tests/validate.py
python3 .github/scripts/publication_check.py
```

Install the separately declared requirements under `architecture/tests/` and `simulations/tests/` where needed. GitHub Actions runs [architecture](.github/workflows/architecture.yml), [simulation](.github/workflows/simulations.yml), and [publication](.github/workflows/publication.yml) checks. Passing tests establish only their stated validation contracts.

## Ecosystem

[AXIOM APEX](https://github.com/axiom-llc/axiom-apex) · [AXIOM ASON](https://github.com/axiom-llc/axiom-ason) · [AXIOM RAG](https://github.com/axiom-llc/axiom-rag) · [AXIOM Demos](https://github.com/axiom-llc/axiom-demos) · [AXIOM website](https://axiom-llc.github.io/)

## Publication and licensing

Publication follows [PUBLICATION.md](PUBLICATION.md): **public approval is separate from private retention and historical-disclosure remediation**. AXIOM-authored executable code is licensed under the scoped [MIT terms](LICENSE); prose, research, evidence, marks, and third-party materials retain their separate rights.
