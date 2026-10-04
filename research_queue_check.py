#!/usr/bin/env python3
"""Validate AXIOM Research's canonical research queue."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re

STATUSES = ["QUEUED", "ISSUED", "COMPLETE", "BLOCKED", "REJECTED"]
TARGETS = ["claude-manual", "gemini-manual", "chatgpt"]
ORDERING = ["priority asc", "value_score desc", "created_at asc", "id asc"]
REQUIRED = {
    "id", "priority", "value_score", "status", "target", "created_at",
    "title", "question", "objective", "deliverable", "constraints",
}
ID_RE = re.compile(r"^RQ-\d{4}-\d{2}-\d{2}-\d{3}$")


def fail(message: str) -> None:
    raise ValueError(message)


def nonempty_text(value, field: str, item_id: str) -> None:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        fail(f"{item_id}: {field} must be non-empty trimmed text")


def validate(path: Path) -> dict:
    queue = json.loads(path.read_text(encoding="utf-8"))
    if queue.get("schema_version") != 1:
        fail("unsupported research queue schema")

    policy = queue.get("policy")
    if not isinstance(policy, dict):
        fail("research queue policy must be an object")
    if policy.get("owner_repo") != "axiom-llc/axiom-research":
        fail("research queue owner_repo must be axiom-llc/axiom-research")
    if policy.get("ordering") != ORDERING:
        fail("research queue ordering contract changed")
    if policy.get("statuses") != STATUSES:
        fail("research queue status contract changed")
    if policy.get("researcher_targets") != TARGETS:
        fail("research queue target contract changed")
    if policy.get("manager_target") != "chatgpt":
        fail("research queue manager_target must be chatgpt")
    if policy.get("incremental_hosted_cost_usd") != 0:
        fail("research queue hosted-cost ceiling must remain zero")

    items = queue.get("items")
    if not isinstance(items, list):
        fail("research queue items must be a list")

    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            fail("research queue items must be objects")
        item_id = item.get("id", "<unknown>")
        missing = REQUIRED - set(item)
        if missing:
            fail(f"{item_id}: missing {sorted(missing)}")
        nonempty_text(item["id"], "id", item_id)
        if ID_RE.fullmatch(item["id"]) is None:
            fail(f"{item_id}: invalid id format")
        if item["id"] in seen:
            fail(f"duplicate research queue id: {item['id']}")
        seen.add(item["id"])

        if isinstance(item["priority"], bool) or not isinstance(item["priority"], int) or item["priority"] < 0:
            fail(f"{item_id}: priority must be a non-negative integer")
        if isinstance(item["value_score"], bool) or not isinstance(item["value_score"], (int, float)):
            fail(f"{item_id}: value_score must be numeric")
        if item["status"] not in STATUSES:
            fail(f"{item_id}: invalid status")
        if item["target"] not in TARGETS:
            fail(f"{item_id}: invalid target")

        try:
            date.fromisoformat(item["created_at"])
        except (TypeError, ValueError):
            fail(f"{item_id}: created_at must be ISO YYYY-MM-DD")

        for field in ("title", "question", "objective"):
            nonempty_text(item[field], field, item_id)
        if not isinstance(item["deliverable"], list) or not item["deliverable"]:
            fail(f"{item_id}: deliverable must be a non-empty list")
        if not isinstance(item["constraints"], list):
            fail(f"{item_id}: constraints must be a list")
        for field in ("deliverable", "constraints"):
            for value in item[field]:
                nonempty_text(value, field, item_id)

        if item["status"] == "ISSUED":
            nonempty_text(item.get("issued_at"), "issued_at", item_id)
        if item["status"] == "COMPLETE":
            nonempty_text(item.get("artifact"), "artifact", item_id)
            nonempty_text(item.get("completed_at"), "completed_at", item_id)

    queued = sorted(
        (item for item in items if item["status"] == "QUEUED"),
        key=lambda item: (
            item["priority"],
            -float(item["value_score"]),
            item["created_at"],
            item["id"],
        ),
    )
    return {
        "items": len(items),
        "queued": len(queued),
        "next": queued[0]["id"] if queued else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", nargs="?", type=Path, default=Path("research-queue.json"))
    args = parser.parse_args()
    print(json.dumps(validate(args.queue), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
