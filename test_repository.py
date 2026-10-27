"""Offline checks for agent releases and saved public evaluations."""
from pathlib import Path
import ast
import json
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent

def run(relative):
    return subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT,
                          capture_output=True, text=True)

class RepositoryTests(unittest.TestCase):
    def test_original_baseline_evidence(self):
        p = run("scripts/verify_repository.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_e126_release(self):
        p = run("scripts/verify_e126_release.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_summary_mentions_all_versions(self):
        p = run("scripts/summarize_results.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        for term in ("N093:", "N117:", "E126 seed 76:", "hybrid=16", "not private Kaggle"):
            self.assertIn(term, p.stdout)

    def test_single_readme_and_links(self):
        self.assertFalse((ROOT / "RESULTS.md").exists())
        self.assertIn("## Results on public games", (ROOT / "README.md").read_text(encoding="utf-8"))
        for md in ROOT.rglob("*.md"):
            for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
                target = link.split("#", 1)[0].split("?", 1)[0].strip("<>")
                if not target or target.startswith(("http://", "https://", "mailto:", "/", "#")):
                    continue
                destination = (md.parent / target).resolve()
                self.assertTrue(destination.is_relative_to(ROOT.resolve()), target)
                self.assertTrue(destination.exists(), f"Broken link: {md.relative_to(ROOT)} -> {target}")

    def test_notebooks(self):
        notebooks = list(ROOT.glob("*.ipynb"))
        self.assertEqual(len(notebooks), 1)
        nb = json.loads(notebooks[0].read_text(encoding="utf-8"))
        self.assertEqual(nb["nbformat"], 4)

    def test_plots(self):
        images = list((ROOT / "results/plots").glob("*.svg"))
        self.assertGreaterEqual(len(images), 2)
        for file in images:
            self.assertTrue(ET.parse(file).getroot().tag.endswith("svg"), str(file))

    def test_single_requirements_file(self):
        self.assertTrue((ROOT / "requirements.txt").is_file())
        self.assertFalse((ROOT / "requirements-agent.txt").exists())
        self.assertFalse((ROOT / "requirements-analysis.txt").exists())
        dependencies = [
            line.strip() for line in (ROOT / "requirements.txt").read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(len(dependencies), len(set(dependencies)))
        self.assertTrue({"numpy>=1.24", "scipy", "torch", "pandas>=2.0", "matplotlib>=3.7"}.issubset(dependencies))

    def test_readable_policy_uses_local_baseline(self):
        source = ast.parse((ROOT / "src/local_effect_policy.py").read_text(encoding="utf-8"))
        imports = [node.module for node in ast.walk(source) if isinstance(node, ast.ImportFrom)]
        self.assertIn("src.frozen_n093", imports)
        self.assertNotIn("submission", imports)
        frozen = ast.parse((ROOT / "src/frozen_n093.py").read_text(encoding="utf-8"))
        self.assertTrue(any(isinstance(node, ast.ClassDef) and
                            node.name == "PretrainedPUCTCore" for node in frozen.body))

if __name__ == "__main__":
    unittest.main()
