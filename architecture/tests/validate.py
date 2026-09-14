#!/usr/bin/env python3
"""Validate architecture JSON Schemas and deterministic valid/invalid fixtures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    raise SystemExit("ERROR: install the 'jsonschema' package to run architecture schema validation")

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    schema_paths = sorted(SCHEMAS.glob("*.schema.json"))
    if not schema_paths:
        print("ERROR: no architecture schemas found", file=sys.stderr)
        return 2

    schemas = {}
    for path in schema_paths:
        schema = load(path)
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        schemas[path.name.removesuffix(".schema.json")] = validator_cls(schema)

    expected = set(schemas)
    for kind, should_pass in (("valid", True), ("invalid", False)):
        fixture_dir = FIXTURES / kind
        fixtures = {p.stem: p for p in sorted(fixture_dir.glob("*.json"))}
        missing = expected - set(fixtures)
        extra = set(fixtures) - expected
        if missing or extra:
            print(f"ERROR: {kind} fixture/schema mismatch missing={sorted(missing)} extra={sorted(extra)}", file=sys.stderr)
            return 2

        for name in sorted(expected):
            instance = load(fixtures[name])
            errors = list(schemas[name].iter_errors(instance))
            if should_pass and errors:
                print(f"FAIL valid/{name}.json: {errors[0].message}", file=sys.stderr)
                return 1
            if not should_pass and not errors:
                print(f"FAIL invalid/{name}.json unexpectedly validated", file=sys.stderr)
                return 1

    print(f"architecture schemas: {len(schemas)} schemas, {len(schemas) * 2} fixtures OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
