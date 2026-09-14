#!/usr/bin/env python3
"""Validate architecture version, invariant identities, schemas, and fixtures."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "ARCHITECTURE.md"
VERSION = ROOT / "VERSION"
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
INVARIANT_RE = re.compile(r"^(\d+)\. `INV-(\d{3})` — ", re.MULTILINE)
EXPECTED_INVARIANTS = 33


def check_version() -> bool:
    value = VERSION.read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(value):
        print(f"ERROR: architecture/VERSION must be MAJOR.MINOR.PATCH, got {value!r}", file=sys.stderr)
        return False
    return True


def check_invariants() -> bool:
    text = ARCHITECTURE.read_text(encoding="utf-8")
    declarations = [(int(ordinal), int(identifier)) for ordinal, identifier in INVARIANT_RE.findall(text)]
    expected = [(n, n) for n in range(1, EXPECTED_INVARIANTS + 1)]
    if declarations != expected:
        print(
            "ERROR: governing invariants must declare contiguous, ordered "
            f"INV-001..INV-{EXPECTED_INVARIANTS:03d}; got {declarations}",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    ok = check_version() and check_invariants()
    if not ok:
        return 1
    schema_status = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "validate.py")],
        check=False,
    ).returncode
    if schema_status:
        return schema_status
    print(f"architecture contract: version {VERSION.read_text(encoding='utf-8').strip()}, 33 invariants OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
