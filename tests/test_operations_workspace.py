"""Contracts for the optional operations workspace module and its no-JS reference page."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "examples/operations-workspace.html"
CSS = ROOT / "src/workspaces.css"


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.targets = []
        self.controls = []
        self.labels = set()
        self.scripts = []
        self.remote = []
        self.mains = 0
        self.h1s = 0
        self.forms = []
        self.landmarks = []
        self.current = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.targets.append(a["href"][1:])
        if tag == "label" and a.get("for"):
            self.labels.add(a["for"])
        if tag in ("input", "select"):
            self.controls.append((a.get("id"), a.get("name")))
        if tag == "form":
            self.forms.append(a.get("method", "get"))
        if tag in ("script", "iframe"):
            self.scripts.append(tag)
        if tag in ("img", "link", "script"):
            url = a.get("src", a.get("href", ""))
            if url.startswith(("http:", "https:", "//")):
                self.remote.append(url)
        if tag == "main":
            self.mains += 1
        if tag == "h1":
            self.h1s += 1
        if a.get("aria-current") == "page":
            self.current += 1


class OperationsWorkspaceTests(unittest.TestCase):
    def test_module_is_optional_and_dist_builds_it(self):
        source = (ROOT / "scripts/build.py").read_text()
        self.assertIn("'syntyr.workspaces.css': ('workspaces.css',)", source)
        self.assertIn("'workspaces.css'", source)
        self.assertTrue(CSS.exists())
        css = CSS.read_text()
        for class_name in (
            ".syn-ops-workspace", ".syn-ops-stage", ".syn-ops-results",
            ".syn-ops-map", ".syn-ops-marker", ".syn-ops-record",
            ".syn-ops-inspector", ".syn-ops-legend",
        ):
            self.assertIn(class_name, css)
        self.assertIn("@container", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("forced-colors", css)
        self.assertNotIn("@import", css)
        self.assertNotIn("url(", css)

    def test_static_example_is_semantic_and_host_ready(self):
        self.assertTrue(PAGE.exists())
        page = PAGE.read_text()
        audit = PageAudit()
        audit.feed(page)
        self.assertEqual(audit.mains, 1)
        self.assertEqual(audit.h1s, 1)
        self.assertEqual(audit.current, 1)
        self.assertEqual(audit.scripts, [])
        self.assertEqual(audit.remote, [])
        self.assertEqual(audit.forms, ["get"])
        self.assertEqual(set(audit.targets) - audit.ids, set())
        self.assertTrue({"query", "status", "type"} <= {name for _, name in audit.controls})
        self.assertTrue({identity for identity, _ in audit.controls} <= audit.labels)
        self.assertIn("ILLUSTRATIVE DATA", page)
        self.assertIn("not a live map", page)
        self.assertIn('href="../dist/syntyr.workspaces.css"', page)
        self.assertIn('href="../dist/syntyr.core.css"', page)
        self.assertIn('href="../dist/syntyr.recipes.css"', page)
        self.assertIn('class="syn-ops-workspace"', page)
        self.assertIn('class="syn-ops-stage"', page)
        self.assertIn('class="syn-ops-results"', page)
        self.assertIn('aria-label="Illustrative map markers"', page)
        self.assertIn("role=\"status\"", page)
        self.assertNotIn("onclick=", page.lower())

    def test_public_docs_and_browser_suite_link_example(self):
        self.assertIn("operations-workspace.html", (ROOT / "README.md").read_text())
        self.assertIn("operations-workspace.html", (ROOT / "docs/index.html").read_text())
        self.assertIn("operations-workspace.html", (ROOT / "scripts/build_cloudflare_site.py").read_text())
        self.assertIn("public_css = tuple(all_distributions())", (ROOT / "scripts/build_cloudflare_site.py").read_text())
        for test in ("browser_matrix.py", "reflow_test.py", "axe_audit.py"):
            self.assertIn('"examples/operations-workspace.html"', (ROOT / "tests" / test).read_text())


if __name__ == "__main__":
    unittest.main()
