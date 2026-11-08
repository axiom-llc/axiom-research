"""Research native RSI: source binding, safe patch, rollback and semantic holdouts."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from rsi.native import GenerationError, generate, propose, validate_rule
from rsi.benchmark import fixture, load

ROOT = Path(__file__).resolve().parents[1]
RULE = json.loads((ROOT / "rsi/generators.json").read_text())["rules"][0]
SOURCE = (ROOT / RULE["path"]).read_text()


class NativeRSITests(unittest.TestCase):
    def test_generation_revision_binding_and_idempotency(self):
        report = generate(ROOT)
        self.assertEqual(report["repository"], "axiom-llc/axiom-research")
        self.assertEqual(len(report["candidates"]), 1)
        self.assertFalse(report["mutation_authority"])
        self.assertEqual(propose(SOURCE, RULE, "a"*40),
                         propose(SOURCE, RULE, "a"*40))
        self.assertIsNone(propose(SOURCE.replace(RULE["before"], RULE["after"], 1),
                                  RULE, "a"*40))
        with self.assertRaises(GenerationError):
            generate(ROOT, "a"*40)

    def test_unsafe_path_and_ambiguous_source_rejected(self):
        for bad in ("../escape.py", "/etc/file.py", "tests/test_no.py"):
            with self.assertRaises(GenerationError):
                validate_rule({**RULE, "path": bad})
        with self.assertRaises(GenerationError):
            propose(SOURCE + RULE["before"], RULE, "a"*40)

    def test_semantics_original_and_candidate(self):
        a = load(SOURCE)
        b = load(SOURCE.replace(RULE["before"], RULE["after"], 1))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"q.json"
            path.write_text(json.dumps(fixture(25)))
            self.assertEqual(a(path), b(path))
            bad=fixture(3)
            bad["items"][0].pop("status")
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, "missing"):
                a(path)
            with self.assertRaisesRegex(ValueError, "missing"):
                b(path)

    def test_git_patch_reversal_recovers_exact_bytes(self):
        patch=propose(SOURCE,RULE,"a"*40)["patch"]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            file=root/RULE["path"]
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_text(SOURCE)
            subprocess.run(["git","init","-q"],cwd=root,check=True)
            initial=file.read_bytes()
            for args in (["git","apply","--check","-"],["git","apply","-"],
                         ["git","apply","-R","--check","-"],["git","apply","-R","-"]):
                subprocess.run(args,cwd=root,input=patch,text=True,check=True,
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertEqual(file.read_bytes(),initial)


if __name__ == "__main__":
    unittest.main()
