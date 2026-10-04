# Robotics-production flagship findings

## Retained result

The accepted evidence under `evidence/accepted-20260916/` is a `VALIDATED_EXECUTABLE_DEMO` of the fictional SR-1 robotics-production workflow. The execution is bound to the pre-evidence Research source revision `76abf779a9e1a12262594444a49d98981147d2a0` plus exact scenario/fixture hashes recorded in `evidence.json`.

Observed execution facts:

- 22 modeled organizational steps span requirements, engineering, procurement, receiving/inventory, production planning, mechanical/electrical assembly, software load, test, quality, rework, release, simulated deployment, and field feedback.
- The exact ASON request contains 19 local-file tool effects; APEX recorded 19 `SUCCEEDED` effect states and 19 tool events.
- ASON authorization identity, policy digest/reference, exact approved-plan digest, and synthetic authority reference were durably present in APEX run detail.
- A negative control submitted the same exact plan without an authority reference; ASON refused authorized dispatch before an APEX run was created.
- The exact expected terminal organizational state matched the produced terminal-state artifact.
- Live APEX replay completed successfully and all 16 produced JSON files retained identical nanosecond modification times, directly showing that the completed effects were reused rather than redispatched in this recovery exercise.
- Deterministic evaluation returned `ACCEPT`; retained evidence reports no execution limitation or unexpected failure for this run.

## Modeled exception paths

The supplier delay, wrong-revision receiving quarantine, firmware first-pass failure/reflash, and motor-mount torque nonconformance/rework are deterministic synthetic business exceptions. They demonstrate workflow representation and recovery handoffs; they are not empirical defect frequencies and are not evidence of autonomous diagnosis or physical corrective action.

## Architectural finding

The flagship did not require new APEX, ASON, RAG, or Harness runtime semantics. The Research organization/scenario contracts remained separate from the exact ASON/APEX execution plan, while APEX supplied durable authorization/effect evidence and conservative completed-effect recovery. This supports continuing the approved program with domain-neutral Research contracts rather than embedding robotics-specific machinery in APEX.

## Limits

This run uses local files only. It controls no robot, PLC, industrial equipment, supplier system, inventory system, payment, firmware flasher, deployment system, or production credential. The synthetic release board is an application-level authority reference, not independent identity attestation. The result does not establish regulatory compliance, production readiness, industrial safety, exactly-once external effects, distributed recovery, real-world throughput, cost savings, or autonomous engineering/safety authority.
