#!/usr/bin/env python3
"""Prepare and verify a private candidate for AXIOM Research history remediation."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def cmd(*args: str, data: bytes | None = None, env: dict | None = None) -> bytes:
    result = subprocess.run(
        args, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )
    if result.returncode:
        raise RuntimeError(
            "command failed: " + " ".join(args[:3]) + "\n"
            + result.stderr.decode("utf-8", "replace")[-5000:]
        )
    return result.stdout


def refs(repo: Path) -> dict[str, str]:
    output = cmd("git", f"--git-dir={repo}", "for-each-ref",
                 "--format=%(refname) %(objectname)").decode()
    return dict(line.split() for line in output.splitlines())


def tree_of(repo: Path, ref: str) -> str:
    return cmd("git", f"--git-dir={repo}", "rev-parse",
               f"{ref}^{{tree}}").decode().strip()


def prepare(bundle: Path, registry_path: Path, dest: Path) -> dict:
    if dest.exists():
        raise ValueError("refuse to overwrite existing destination")
    dest.mkdir(parents=True)
    registry = json.loads(registry_path.read_text())
    restricted_actions = {
        "public_abstract_with_verified_private_original",
        "public_summary_with_verified_private_original",
        "removed_from_default_branch",
    }
    targets = sorted((x for x in registry["assets"]
                      if x["action"] in restricted_actions), key=lambda x: x["path"])
    if len(targets) != 31:
        raise ValueError("restricted path count changed")
    for x in targets:
        path = x["path"]
        if path.startswith("/") or ".." in Path(path).parts or "\n" in path:
            raise ValueError("unsafe or malformed restricted path")
    original = dest / "original.git"
    rewritten = dest / "rewritten.git"
    cmd("git", "clone", "--quiet", "--mirror", str(bundle), str(original))
    cmd("git", "clone", "--quiet", "--mirror", str(bundle), str(rewritten))
    before = refs(original)
    if before["refs/heads/main"] != "62e5582a0f0ff90f5a9ef3dedb85757c86ffd42f":
        raise ValueError("pinned public main changed")
    if len([p for p in before if p.startswith("refs/heads/")]) != 45:
        raise ValueError("unexpected public branch inventory")

    filt = ["git", "-C", str(rewritten), "filter-repo", "--force",
            "--sensitive-data-removal", "--invert-paths"]
    for x in targets:
        filt.extend(("--path", x["path"]))
    cmd(*filt)
    after_filter = refs(rewritten)
    if len([p for p in after_filter if p.startswith("refs/heads/")]) != 45:
        raise ValueError("rewrite dropped a branch")
    index = dest / "restore.index"
    env = dict(os.environ, GIT_INDEX_FILE=str(index))
    cmd("git", f"--git-dir={rewritten}", "read-tree", "refs/heads/main", env=env)
    restored = 0
    for x in targets:
        path = x["path"]
        if x["current_blob"] is None:
            continue
        entry = cmd("git", f"--git-dir={original}", "ls-tree",
                    "refs/heads/main", "--", path).decode().strip()
        mode, typ, sha, old_path = entry.split(None, 3)
        if typ != "blob" or old_path != path or sha != x["current_blob"]:
            raise ValueError("current public file changed: " + path)
        body = cmd("git", f"--git-dir={original}", "cat-file", "blob", sha)
        inserted = cmd("git", f"--git-dir={rewritten}",
                       "hash-object", "-w", "--stdin", data=body).decode().strip()
        if inserted != sha:
            raise ValueError("public blob retention mismatch")
        cmd("git", f"--git-dir={rewritten}", "update-index",
            "--add", "--cacheinfo", f"{mode},{sha},{path}", env=env)
        restored += 1
    if restored != 29:
        raise ValueError("missing curated public summaries")
    final_tree = cmd("git", f"--git-dir={rewritten}", "write-tree", env=env).decode().strip()
    original_tree = tree_of(original, "refs/heads/main")
    if final_tree != original_tree:
        raise ValueError("rewritten public tree differs from approved original")

    parent = refs(rewritten)["refs/heads/main"]
    e = dict(
        os.environ,
        GIT_AUTHOR_NAME="AXIOM retention",
        GIT_AUTHOR_EMAIL="noreply@users.noreply.github.com",
        GIT_COMMITTER_NAME="AXIOM retention",
        GIT_COMMITTER_EMAIL="noreply@users.noreply.github.com",
        GIT_AUTHOR_DATE="2026-11-07T02:46:00 +0000",
        GIT_COMMITTER_DATE="2026-11-07T02:46:00 +0000",
    )
    rewritten_main = cmd(
        "git", f"--git-dir={rewritten}", "commit-tree", final_tree,
        "-p", parent,
        data=b"security: restore reviewed public HEAD following restricted history purge\n",
        env=e,
    ).decode().strip()
    cmd("git", f"--git-dir={rewritten}", "update-ref",
        "refs/heads/main", rewritten_main, parent)
    cmd("git", f"--git-dir={rewritten}", "fsck", "--full", "--no-reflogs")
    after = refs(rewritten)
    if set(before) != set(after):
        raise ValueError("rewrite changed the ref name set")
    if tree_of(rewritten, "refs/heads/main") != original_tree:
        raise ValueError("post-commit public tree changed")

    forbidden = {x["source_blob"] for x in targets if x.get("source_blob")}
    reachable = set(line.split(b" ", 1)[0].decode()
                    for line in cmd("git", f"--git-dir={rewritten}",
                                    "rev-list", "--objects", "--all").splitlines())
    if forbidden & reachable:
        raise ValueError("original restricted blobs remain reachable")

    bundle_out = dest / "sanitized.bundle"
    cmd("git", f"--git-dir={rewritten}", "bundle",
        "create", str(bundle_out), "--all")
    cmd("git", f"--git-dir={rewritten}", "bundle", "verify", str(bundle_out))
    verified = dest / "checkout"
    cmd("git", "clone", "--quiet", str(bundle_out), str(verified))
    if cmd("git", "-C", str(verified), "rev-parse",
           "HEAD^{tree}").decode().strip() != original_tree:
        raise ValueError("independent checkout tree mismatch")

    changed = [key for key in before if before[key] != after[key]]
    report = {
        "source_main": before["refs/heads/main"],
        "source_main_tree": original_tree,
        "sanitized_main": rewritten_main,
        "sanitized_main_tree": tree_of(rewritten, "refs/heads/main"),
        "source_refs": before,
        "sanitized_refs": after,
        "ref_changes": len(changed),
        "affected_pull_refs": [p for p in changed if p.startswith("refs/pull/")],
        "targets_count": len(targets),
        "curated_files_restored": restored,
        "source_blob_count": len(forbidden),
        "remaining_original_source_blobs": 0,
        "sanitized_bundle_sha256": hashlib.sha256(bundle_out.read_bytes()).hexdigest(),
        "sanitized_bundle_bytes": bundle_out.stat().st_size,
    }
    (dest / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("SANITIZED_READY", json.dumps({
        k: report[k] for k in ("sanitized_main", "sanitized_main_tree",
            "ref_changes", "targets_count", "curated_files_restored",
            "remaining_original_source_blobs", "sanitized_bundle_sha256")
    }))
    return report


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: scrub_prepare.py SOURCE.bundle MANIFEST.json EMPTY_DEST")
    prepare(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
