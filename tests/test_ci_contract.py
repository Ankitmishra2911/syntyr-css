"""CI should gate releases without adding a consumer-side dependency."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContinuousIntegrationContract(unittest.TestCase):
    def test_pull_requests_and_main_pushes_run_standard_library_gates(self):
        workflow = ROOT / ".woodpecker" / "quality.yaml"
        self.assertTrue(workflow.is_file(), "A PR quality workflow is required")
        content = workflow.read_text(encoding="utf-8")
        for contract in (
            "event: pull_request",
            "event: push",
            "branch: main",
            "python:3.14-slim",
            "python3 scripts/build.py --check",
            "python3 -m unittest discover -s tests -v",
            "python3 scripts/build_cloudflare_site.py",
            "python3 scripts/build_cloudflare_site.py --check",
            "python3 scripts/package_release.py",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, content)

    def test_release_browser_matrix_is_explicit_and_not_a_runtime_dependency(self):
        workflow = ROOT / ".woodpecker" / "browser.yaml"
        self.assertTrue(workflow.is_file(), "Require a reproducible release browser workflow")
        content = workflow.read_text(encoding="utf-8")
        for contract in (
            "event: manual",
            "event: tag",
            "playwright/python:v1.65.2-noble",
            "python3 tests/browser_matrix.py --browsers chromium firefox webkit",
            "python3 tests/reflow_test.py --browsers chromium firefox webkit",
            "python3 tests/theme_editor_browser.py",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, content)


if __name__ == "__main__":
    unittest.main()
