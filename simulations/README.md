# AXIOM organizational simulation research program

This directory defines the canonical, domain-neutral research contracts for reproducible synthetic organizational simulations executed through AXIOM. Research owns models, assumptions, accepted evidence, evaluations, findings, and evidence-traceable claims. It does not own runtime execution semantics.

## Pipeline

`domain selection → operational research → organization model → synthetic fixtures/scenario → AXIOM execution → evidence capture → deterministic evaluation → retained research → derived demo/case study → evidence-traceable claim`

Use current owning-system interfaces. APEX remains the bounded execution substrate; ASON remains pre-execution policy/authorization; RAG remains retrieval/storage; Harness owns durable multi-attempt/task orchestration when persistence materially helps; Infra may own cross-repository execution adapters; Demos and the website contain derived presentation only.

## Contracts

- `organization-model` describes departments, actors, authority, resources, policies, and modeled state.
- `scenario-spec` describes objectives, workflow stages, dependencies, approvals, failure injection, expected terminal state, acceptance, and evidence requirements.
- `fixture-manifest` proves fixtures are synthetic, records provenance/assumptions, and binds retained fixture artifacts by digest.
- `simulation-evidence` binds one execution to exact repository revisions, inputs, AXIOM run/authorization references, effects, events, outcomes, failures, recovery, metrics, and limitations.
- `evaluation-record` separates deterministic acceptance from execution and records observed checks.
- `claim-record` prevents public capability claims without explicit evidence references and scope/limitations.

## Evidence classes

`SYNTHETIC_SIMULATION` means a modeled organization uses synthetic inputs. `VALIDATED_EXECUTABLE_DEMO` additionally requires reproducible execution plus accepted validation evidence. `PRODUCTION_DEPLOYMENT` is reserved for actual production evidence and is intentionally unavailable as a scenario/evidence classification here; it may appear in claim metadata only when independently supported by real production evidence.

Never infer production performance, regulatory compliance, autonomous professional authority, universal organizational capability, exactly-once external effects, or economic benefit from a simulation. Regulated, safety-critical, financial, legal, medical, robotics, industrial, and physical workflows retain explicit human/professional authority and simulate uncontrolled external effects.


## Runner and deterministic evaluation

`python simulations/runner.py` validates an organization/scenario/fixture bundle, binds it to an explicit exact ASON request, submits that request through the real ASON CLI to APEX, retrieves the durable APEX run record, and emits schema-valid `SimulationEvidence` plus `SimulationEvaluationRecord` artifacts. The runner does not translate organizational workflow semantics into executable tools: each simulation supplies its own exact execution request.

The current deterministic acceptance contract can require successful APEX completion, durable authorization/plan binding, exact terminal-state equality, and named evidence such as the effect ledger. A simulation should have its APEX plan produce its terminal-state JSON artifact; the runner reads that artifact after execution. This keeps organizational modeling, AXIOM execution, and acceptance separate.

## Initial approved portfolio

1. Robotics production — flagship: requirements through engineering, procurement, inventory, planning, assembly, firmware/software, test, quality, defect handling, release, deployment simulation, and field feedback.
2. Software-development organization.
3. Specialty-care administration.
4. Cybersecurity/SOC operations.
5. Logistics and supply chain.

The portfolio is designed to stress different architectural properties rather than maximize domain count.

Accepted cross-domain results are summarized in [`portfolio-summary.json`](./portfolio-summary.json) and synthesized in [`cross-domain-findings.md`](./cross-domain-findings.md). The summary is evidence-indexing metadata only; it does not create new runtime authority or expand the scope of the underlying evidence.

## Retention and publication

Retain only artifacts with durable research, engineering, benchmarking, demonstration, or commercial value. Canonical evidence remains separate from derived presentation. Website and sales claims must identify supporting `claim-record`/evidence artifacts and preserve their limitations. Failed and inconclusive experiments remain valuable when they reveal architectural limits.

## Validation

```bash
python -m pip install -r simulations/tests/requirements.txt
python simulations/tests/validate.py
git diff --check -- simulations
```

## Operational fidelity

Item 20 adds `operational-fidelity-v1`, a reconstructable record for material actors, resources, schedules, queues, decisions, communications, synthetic financial state, inventory, documents, events, situations, issues, approvals, recovery, state transitions, and outcomes. Completeness is scoped to the modeled operation and must pass reference-closure, reconciliation, and reconstruction checks.
