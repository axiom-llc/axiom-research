# High-fidelity SR-1 operating-day findings

## Retained result

The accepted item-20(a) evidence expands the prior SR-1 workflow slice into one reconstructable synthetic operating day. It records 28 causally ordered operations spanning 10 actors, 7 operational resources, schedules and queues, 4 decisions, 5 communications, 4 synthetic USD transactions totaling $21,390, 5 inventory movements, 9 documents, 9 events, 4 operational situations, 5 issues, 5 approvals, 9 state transitions, and 2 outcomes.

Execution used four durable AXIOM Harness tasks/resources. Each phase produced a deterministic candidate result, was accepted by SHA-256, and received a canonical Harness completion receipt. ASON authorized four exact local plans; APEX recorded 16/16 successful effects/events. Missing authority was rejected before dispatch, and every APEX run's durable plan digest matched its ASON authorization.

## Architectural finding

This bounded operating-day model required no new APEX, ASON, or Harness runtime primitive. Harness adds material value here because the simulated day spans multiple persistent operational phases and resource assignments; APEX continues to own only bounded machine effects. Synthetic financial amounts remain modeled organizational state and do not alter Harness's real hard-zero-spend boundary.

## Limits

This is one synthetic operating day, not a complete company model or production deployment. It does not yet model multi-day backlog evolution, payroll/accounts payable, supplier competition, staffing absences, maintenance, capacity contention across multiple units, customer support queues, or every enterprise document/system. No real payment, procurement, manufacturing, robot motion, deployment, or professional approval occurred. Item 20 remains in progress.
