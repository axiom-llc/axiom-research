# SR-1 high-fidelity operating day

This bounded item-20 simulation expands the SR-1 robotics model into a reconstructable synthetic operating day. `operating-day.json` records 28 causally ordered operations plus explicit resources, schedules, queues, decisions, communications, synthetic USD transactions, inventory movements, documents, events, situations, issues, approvals, state transitions, and outcomes.

`execute.py` divides the day into four durable operational phases. AXIOM Harness owns task/resource leases, deterministic acceptance, and canonical phase receipts; ASON authorizes each exact plan; APEX records and executes each local synthetic effect. No real procurement, payment, manufacturing, robot control, deployment, or professional authority occurs.
