#!/usr/bin/env python3
"""Validate architecture contract, references, change coupling, schemas, and fixtures."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
ARCHITECTURE = ROOT / "ARCHITECTURE.md"
VERSION = ROOT / "VERSION"
CHANGELOG = ROOT / "CHANGELOG.md"
SCHEMAS = ROOT / "schemas"
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
INVARIANT_RE = re.compile(r"^(\d+)\. `INV-(\d{3})` — ", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
EXPECTED_INVARIANTS = 33
REQUIRED_PATHS = (
    ROOT / "README.md",
    ARCHITECTURE,
    VERSION,
    ROOT / "STATUS.md",
    CHANGELOG,
    SCHEMAS,
    ROOT / "tests",
)


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def check_required_paths() -> bool:
    missing = [str(path.relative_to(REPO_ROOT)) for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        print(f"ERROR: missing canonical architecture paths: {missing}", file=sys.stderr)
        return False
    return True


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


def iter_refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                yield child
            yield from iter_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_refs(child)


def resolve_json_fragment(document, fragment: str) -> bool:
    if not fragment:
        return True
    fragment = unquote(fragment)
    if fragment.startswith("/"):
        value = document
        for raw_part in fragment[1:].split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            try:
                if isinstance(value, list):
                    value = value[int(part)]
                else:
                    value = value[part]
            except (KeyError, IndexError, ValueError, TypeError):
                return False
        return True

    anchor = fragment
    stack = [document]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            if value.get("$anchor") == anchor:
                return True
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    return False


def check_schema_references() -> bool:
    ok = True
    cache: dict[Path, object] = {}

    def load_json(path: Path):
        if path not in cache:
            cache[path] = json.loads(path.read_text(encoding="utf-8"))
        return cache[path]

    for schema_path in sorted(SCHEMAS.glob("*.schema.json")):
        document = load_json(schema_path)
        for ref in iter_refs(document):
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc:
                continue
            target = schema_path if not parsed.path else (schema_path.parent / unquote(parsed.path)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                print(f"ERROR: schema reference escapes architecture/: {schema_path.name}: {ref}", file=sys.stderr)
                ok = False
                continue
            if not target.is_file():
                print(f"ERROR: unresolved schema reference: {schema_path.name}: {ref}", file=sys.stderr)
                ok = False
                continue
            try:
                target_document = load_json(target)
            except (OSError, json.JSONDecodeError) as exc:
                print(f"ERROR: invalid referenced schema {target}: {exc}", file=sys.stderr)
                ok = False
                continue
            if parsed.fragment and not resolve_json_fragment(target_document, parsed.fragment):
                print(f"ERROR: unresolved schema fragment: {schema_path.name}: {ref}", file=sys.stderr)
                ok = False
    return ok


def markdown_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")]
    if " " in value:
        value = value.split(" ", 1)[0]
    return value


def check_markdown_references() -> bool:
    ok = True
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK_RE.findall(text):
            target_text = markdown_target(raw)
            if not target_text or target_text.startswith("#"):
                continue
            parsed = urlsplit(target_text)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (markdown.parent / unquote(parsed.path)).resolve()
            try:
                target.relative_to(REPO_ROOT)
            except ValueError:
                print(
                    f"ERROR: Markdown reference escapes repository: "
                    f"{markdown.relative_to(REPO_ROOT)}: {target_text}",
                    file=sys.stderr,
                )
                ok = False
                continue
            if not target.exists():
                print(
                    f"ERROR: unresolved Markdown reference: "
                    f"{markdown.relative_to(REPO_ROOT)}: {target_text}",
                    file=sys.stderr,
                )
                ok = False
    return ok


def changed_architecture_paths(base: str | None, head: str) -> set[str] | None:
    args = ["diff", "--name-only"]
    if base:
        args.extend([base, head])
    else:
        args.append("HEAD")
    args.extend(["--", "architecture"])
    result = run_git(*args)
    if result.returncode:
        print(f"ERROR: git diff failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def check_version_changelog_coupling(base: str | None, head: str) -> bool:
    changed = changed_architecture_paths(base, head)
    if changed is None:
        return False
    if "architecture/VERSION" in changed and "architecture/CHANGELOG.md" not in changed:
        scope = f"{base}..{head}" if base else "working tree vs HEAD"
        print(
            f"ERROR: architecture/VERSION changed in {scope} without architecture/CHANGELOG.md",
            file=sys.stderr,
        )
        return False
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="base Git ref/SHA for change-coupling validation")
    parser.add_argument("--head", default="HEAD", help="head Git ref/SHA; default: HEAD")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checks = (
        check_required_paths(),
        check_version(),
        check_invariants(),
        check_schema_references(),
        check_markdown_references(),
        check_version_changelog_coupling(args.base, args.head),
    )
    if not all(checks):
        return 1

    schema_status = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "validate.py")],
        check=False,
    ).returncode
    if schema_status:
        return schema_status

    print(
        f"architecture contract: version {VERSION.read_text(encoding='utf-8').strip()}, "
        f"{EXPECTED_INVARIANTS} invariants, references and change coupling OK"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
