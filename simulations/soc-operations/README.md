# Synthetic Security Operations Center

Synthetic validated executable demonstration for `cybersecurity-soc` using the canonical AXIOM simulation contracts and runner. All external/regulated/production effects are modeled as local deterministic files; no production deployment or compliance claim is made.

Run: `python simulations/soc-operations/execute.py --out-dir /tmp/soc-operations-evidence` from `axiom-research` with sibling `axiom-apex` and `axiom-ason` checkouts.

Accepted retained evidence: [`evidence/accepted-20260916/`](./evidence/accepted-20260916/). See [`findings.md`](./findings.md) for observed results and limitations.
