# Robotics production — SR-1

Flagship `VALIDATED_EXECUTABLE_DEMO` for the AXIOM organizational-simulation research program. It models a fictional robotics manufacturer end to end using synthetic fixtures and exact ASON-authorized APEX effects.

Run from `axiom-research` with sibling `axiom-apex` and `axiom-ason` checkouts:

```bash
python simulations/robotics-production/execute.py --out-dir /tmp/axiom-robotics-evidence
```

The driver starts an isolated loopback APEX server with a temporary history database, submits the exact local-file plan through the real ASON CLI, retrieves APEX's durable authorization/effect evidence, validates the exact terminal state, then performs live APEX replay. It verifies completed file effects were reused rather than redispatched by proving their nanosecond modification times did not change across replay.

No physical robot, industrial controller, supplier, payment, external deployment, production credential, or private data is used. The simulation does not establish production performance, regulatory compliance, exactly-once external effects, or autonomous engineering/safety authority.

Retained accepted evidence: [`evidence/accepted-20260916/`](./evidence/accepted-20260916/). See [`findings.md`](./findings.md) for the observed result, modeled exception distinction, architectural finding, and explicit limits.
