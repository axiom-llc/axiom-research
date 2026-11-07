#!/usr/bin/env python3
"""Regression tests for the Git-object publication gate."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "publication_history_check.py"


class PublicationAncestryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "ci@example.invalid")
        self.git("config", "user.name", "CI")
        self.commit_file("README.md", "Public synthetic test repository.\n")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=self.root,
                              text=True, capture_output=True, check=True)

    def commit_file(self, path: str, data: str) -> None:
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(data, encoding="utf-8")
        self.git("add", "--", path)
        self.git("commit", "-qm", "test fixture")

    def remove_file(self, path: str) -> None:
        self.git("rm", "-q", "--", path)
        self.git("commit", "-qm", "remove test fixture")

    def scan(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--base", self.base, "--head", "HEAD"],
            cwd=self.root, text=True, capture_output=True, check=False
        )

    def test_clean_public_delta(self) -> None:
        self.commit_file("docs/public.md", "Synthetic, non-identifying public summary.\n")
        self.assertEqual(0, self.scan().returncode)

    def test_removed_manuscript_still_detected(self) -> None:
        path = "manuscripts/edge-dwelling/opening.md"
        self.commit_file(path, "Unpublished draft, retained only in a test repository.\n")
        self.remove_file(path)
        result = self.scan()
        self.assertEqual(1, result.returncode)
        self.assertIn("restricted historical path", result.stderr)

    def test_deleted_credential_blob_still_detected(self) -> None:
        path = "docs/key.txt"
        self.commit_file(path, "test credential: " + "ghp_" + "A" * 30 + "\n")
        self.remove_file(path)
        result = self.scan()
        self.assertEqual(1, result.returncode)
        self.assertIn("GitHub credential", result.stderr)


if __name__ == "__main__":
    unittest.main()
