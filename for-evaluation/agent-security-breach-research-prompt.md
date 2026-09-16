# Agent Security Breach Research Prompt

## Status
For evaluation only. This is a research prompt, not an implementation directive.

## Trigger
The current AXIOM news pull included reports of agent-linked security incidents, including an AI-agent-linked data breach and reporting that autonomous agents probed an external model platform before a major compromise. The briefing correctly treated the headlines alone as insufficient evidence for an AXIOM implementation change. They nevertheless justify source-grounded research because AXIOM operates agent, policy, deterministic execution, retrieval, API, infrastructure, and applied-integration boundaries.

## Research task
Determine which concrete security failure modes demonstrated by documented real-world AI-agent incidents are relevant to the current AXIOM architecture, and identify any evidence-backed gaps without assuming that a reported external incident applies to AXIOM.

Use primary technical sources, incident disclosures, vendor advisories, vulnerability records, standards, peer-reviewed research, and current canonical AXIOM repositories. Treat news headlines only as discovery leads. Verify the underlying incident facts before using them.

Inspect at minimum the current public state of `axiom-apex`, `axiom-ason`, `axiom-rag`, `axiom-api`, `axiom-infra`, `axiom-director`, and agent-facing integrations in `axiom-demos`. Preserve validated AXIOM guarantees and distinguish implemented behavior from documentation, inference, and proposed controls.

Evaluate only materially relevant classes such as indirect prompt injection, tool or authority escalation, confused-deputy behavior, credential or secret exposure, unsafe network/resource access, malicious retrieved content, cross-boundary data exfiltration, dependency or supply-chain compromise, unsafe autonomous reconnaissance, insufficient provenance, and audit/recovery gaps. Do not force every class to apply.

For each supported finding, provide: incident/source evidence; affected AXIOM repository and exact boundary; verified current AXIOM evidence; exploit or failure preconditions; existing mitigation; residual gap; minimal recommended control; compatibility and operational costs; required tests or adversarial validation; and confidence/remaining uncertainty. Explicitly identify findings already addressed by current architecture and findings for which evidence is insufficient.

Prioritize falsifiable, implementation-relevant conclusions. Do not redesign the ecosystem broadly, implement changes, modify repositories, or convert speculative correlations into requirements.

## Required output
Produce one source-cited research report with: executive findings; verified incident evidence; AXIOM boundary map; supported gaps; already-addressed risks; rejected/unsupported hypotheses; minimal candidate controls; validation plan; and unresolved questions. End with a concise set of research conclusions suitable for later human approval or rejection. No implementation is authorized by this prompt.
