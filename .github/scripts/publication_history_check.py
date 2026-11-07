#!/usr/bin/env python3
"""Block newly introduced sensitive Git blobs, including add-then-delete commits.

Unlike a working-tree scan, this checks every blob introduced in the proposed commit range. When the
GitHub event's base is unavailable after an authorized history rewrite, it
conservatively scans every blob reachable from the new head. It does not make
older public history safe or authorize a history rewrite.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from publication_check import CONTENT_RULES, RESTRICTED_PATH, RESTRICTED_SUFFIX


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def check(base: str, head: str) -> list[str]:
    git("rev-parse", "--verify", f"{head}^{{commit}}")
    try:
        git("rev-parse", "--verify", f"{base}^{{commit}}")
        revision_range = f"{base}..{head}"
    except RuntimeError:
        # Force-with-lease history remediation can make github.event.before
        # unreachable. Scan every reachable object instead of bypassing review.
        revision_range = head
    failures: list[str] = []
    objects = git("rev-list", "--objects", revision_range).splitlines()
    for entry in objects:
        if b" " not in entry:
            continue  # Commit or tree, with no associated path.
        oid, raw_path = entry.split(b" ", 1)
        if git("cat-file", "-t", oid.decode("ascii")).strip() != b"blob":
            continue
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if RESTRICTED_PATH.search(path) or RESTRICTED_SUFFIX.search(path):
            failures.append(f"{path}: restricted historical path")
            continue
        body = git("cat-file", "blob", oid.decode("ascii"))
        if b"\0" in body:
            failures.append(f"{path}: binary historical blob")
            continue
        for reason, pattern in CONTENT_RULES.items():
            if path == ".github/scripts/publication_check.py" and reason == "first-person family or clinical record":
                continue
            if pattern.search(body):
                failures.append(f"{path}: {reason} in newly introduced Git history")
    return sorted(set(failures))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="verified base commit SHA")
    parser.add_argument("--head", required=True, help="verified PR head/push commit SHA")
    args = parser.parse_args()
    try:
        failures = check(args.base, args.head)
    except RuntimeError as exc:
        print(f"PUBLICATION BLOCKED: cannot inspect commit ancestry: {exc}", file=sys.stderr)
        return 1
    if failures:
        for failure in failures:
            print(f"PUBLICATION BLOCKED: {failure}", file=sys.stderr)
        return 1
    print("Publication ancestry gate: no restricted new Git blobs in verified range")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
