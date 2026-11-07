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
    if failures:
        for item in failures:
            print(f"PUBLICATION BLOCKED: {item}", file=sys.stderr)
        return 1
    print(f"Publication gate: {len(paths) - 1} tracked files screened")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
