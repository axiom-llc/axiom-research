#!/usr/bin/env python3
"""Fail closed on obvious private assets, credentials, and identifying records.

This is a deterministic publication gate, not a guarantee of IP safety.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RESTRICTED_PATH = re.compile(
    r"(^|/)(?:manuscripts?|personal|private|confidential|secrets?|credentials?)(?:/|$)"
    r"|(?:psychiatr|mental-health|trauma-history|family-case)",
    re.IGNORECASE,
)
RESTRICTED_SUFFIX = re.compile(
    r"(?:^|/)\.env(?:\.|$)|\.(?:pem|p12|pfx|key|kdbx|sqlite|db|eml|msg)$",
    re.IGNORECASE,
)
CONTENT_RULES = {
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub credential": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{35,})"),
    "OpenAI credential": re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Slack token": re.compile(rb"xox[baprs]-[0-9A-Za-z-]{20,}"),
    "US SSN": re.compile(rb"\b\d{3}-\d{2}-\d{4}\b"),
    "personal email": re.compile(
        rb"\b[A-Za-z0-9._%+-]+@(?:gmail\.com|yahoo\.com|outlook\.com|proton\.me|protonmail\.com)\b",
        re.IGNORECASE,
    ),
    "first-person family or clinical record": re.compile(
        rb"\b(?:my (?:mother|father|sister|brother|psychiatrist|diagnosis|medication)|"
        rb"family trauma|I was diagnosed|I was hospitalized)\b",
        re.IGNORECASE,
    ),
}


REDACTED_PUBLIC_ABSTRACTS = {
    "2026-10-05-agentic-mcp-tool-supply-chain-identity-chatgpt.md",
    "2026-10-05-machine-speed-anomaly-halt-policy-chatgpt.md",
    "2026-10-05-minimal-sequence-aware-exfiltration-policy-chatgpt.md",
    "2026-10-06-canonical-verified-execution-boundary-chatgpt.md",
    "2026-10-06-execution-telemetry-composition-boundary-chatgpt.md",
    "2026-10-06-routing-telemetry-coverage-headroom-audit-chatgpt.md",
    "security/2026-10-04-agent-security-incident-boundary-review.md",
    "security/2026-10-04-autonomous-agent-egress-boundary-evaluation.md",
    "security/2026-11-04-change-triggered-security-validation-feasibility.md",
    "security/2026-11-05-commercial-verification-and-privacy-opportunities.md",
    "for-evaluation/agent-security-breach-research-prompt.md",
    "for-evaluation/autonomous-agent-unauthorized-network-probing-controls.md",
    "for-evaluation/runtime-ai-misbehavior-telemetry-and-disclosure-framework.md",
    "autonomous-organizations-agentmail-chatgpt-research-20261003.md",
    "zero-cost-compute-harness-research.md",
    "j-space-research.md",
    "recursive-hyper-optimization.md",
    "temporal-state-resolution.md",
    "ai-loop-architecture-taxonomy.md",
    "claude-agent-systems-research-20261002.md",
    "2026-10-03-long-horizon-agent-reliability-claude.md",
}


def main() -> int:
    paths = subprocess.check_output(["git", "ls-files", "-z"]).split(b"\0")
    failures: list[str] = []
    for raw in paths:
        if not raw:
            continue
        path = raw.decode("utf-8", errors="surrogateescape")
        if RESTRICTED_PATH.search(path) or RESTRICTED_SUFFIX.search(path):
            failures.append(f"{path}: restricted path or file type")
            continue
        try:
            data = Path(path).read_bytes()
        except OSError:
            failures.append(f"{path}: tracked file unavailable")
            continue
        if b"\0" in data:
            failures.append(f"{path}: binary requires separate publication review")
            continue
        for rule, pattern in CONTENT_RULES.items():
            if path == ".github/scripts/publication_check.py" and rule == "first-person family or clinical record":
                continue  # Scanner's own rule definition is not personal evidence.
            if pattern.search(data):
                failures.append(f"{path}: {rule}")
    # Fail closed when a formerly restricted public abstract is replaced
    # with a new full-length implementation or manuscript.
    tracked = {raw.decode("utf-8", errors="surrogateescape") for raw in paths if raw}
    for path in sorted(REDACTED_PUBLIC_ABSTRACTS):
        if path not in tracked:
            failures.append(f"{path}: missing reviewed public abstract")
            continue
        data = Path(path).read_bytes()
        if b"Disclosure class: REDACT" not in data or len(data) > 3000:
            failures.append(f"{path}: restricted source may have replaced public abstract")
    # The queue must remain an explicitly public-safe view of research intake.
    import json

    try:
        queue = json.loads(Path("research-queue.json").read_text(encoding="utf-8"))
        if any(
            "automation" in item
            or not item.get("question", "").startswith("What independently verifiable public evidence")
            or not item.get("objective", "").startswith("Assess the public research literature")
            for item in queue.get("items", [])
        ):
            failures.append("research-queue.json: unreviewed internal research intake")
        if "public disclosure-safe" not in " ".join(queue.get("policy", {}).get("notes", [])):
            failures.append("research-queue.json: missing public-scope policy")
    except (OSError, ValueError, TypeError, KeyError):
        failures.append("research-queue.json: cannot verify public-scope format")
    if failures:
        for item in failures:
            print(f"PUBLICATION BLOCKED: {item}", file=sys.stderr)
        return 1
    print(f"Publication gate: {len(paths) - 1} tracked files screened")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
