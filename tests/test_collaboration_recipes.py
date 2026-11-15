"""Opt-in human/agent collaboration UI contract."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLASSES = (
    "syn-conversation", "syn-conversation__stream", "syn-message",
    "syn-message__avatar", "syn-message__meta", "syn-message__body",
    "syn-message__actions", "syn-identity", "syn-presence",
    "syn-attachment", "syn-composer", "syn-composer__toolbar",
    "syn-collab-layout", "syn-thread-panel", "syn-agent-run",
)


class DemoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.classes = set()
        self.themes = set()
        self.scripts = 0
        self.unlabeled_textareas = []
        self.textareas = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.classes.update(a.get("class", "").split())
        if "data-syn-theme" in a:
            self.themes.add(a["data-syn-theme"])
        if tag == "script":
            self.scripts += 1
        if tag == "textarea":
            self.textareas.append(a)


class CollaborationRecipes(unittest.TestCase):
    def test_optional_module_is_built_but_excluded_from_core(self):
        from scripts.build import all_distributions
        self.assertIn("syntyr.collaboration.css", all_distributions())
        source = (ROOT / "src/collaboration.css").read_text(encoding="utf-8")
        compiled = (ROOT / "dist/syntyr.collaboration.css").read_text(encoding="utf-8")
        self.assertEqual(source.strip(), compiled.strip())
        for name in CLASSES:
            with self.subTest(name=name):
                self.assertIn("." + name, compiled)
                self.assertNotIn("." + name, (ROOT / "dist/syntyr.core.css").read_text())
        self.assertIn(".syn-conversation", (ROOT / "dist/syntyr.all.css").read_text())

    def test_module_is_scoped_and_themeable_with_no_js(self):
        source = (ROOT / "src/collaboration.css").read_text()
        self.assertIn("@layer syn.recipes", source)
        self.assertIn(":where(.syn-root, .syn-root *)", source)
        for token in ("--syn-surface", "--syn-border-subtle", "--syn-text",
                      "--syn-muted", "--syn-accent", "--syn-focus-ring"):
            self.assertIn("var(" + token, source)
        self.assertIn(":focus-visible", source)
        self.assertIn("--syn-collab-avatar: min(2rem, 36px)", source)
        self.assertIn("forced-colors: active", source)
        self.assertIn("prefers-reduced-motion: reduce", source)
        self.assertIn("@media (max-width:", source)
        self.assertNotIn("@import", source)
        self.assertNotRegex(source.lower(), r"@keyframes\s+(blink|pulse|thinking)")
        self.assertNotIn("javascript:", source.lower())

    def test_static_three_theme_example_is_accessible_and_server_ready(self):
        demo = (ROOT / "examples/collaboration.html").read_text(encoding="utf-8")
        parser = DemoParser()
        parser.feed(demo)
        self.assertTrue({"minimal", "grid", "noir"} <= parser.themes)
        self.assertEqual(parser.scripts, 0)
        for name in CLASSES:
            with self.subTest(name=name):
                self.assertIn(name, parser.classes)
        self.assertIn('syntyr.collaboration.css', demo)
        self.assertIn('<time datetime=', demo)
        self.assertIn('role="status"', demo)
        self.assertIn('aria-label="', demo)
        self.assertIn('disabled', demo)  # no fake posting or execution
        for textarea in parser.textareas:
            self.assertTrue(textarea.get("aria-label") or textarea.get("aria-labelledby") or textarea.get("id"))
        self.assertNotRegex(demo, r'<button(?![^>]*disabled)[^>]*>\s*(?:Send|Approve|Run)')
        self.assertNotIn("onclick=", demo.lower())

    def test_release_documentation_and_packaging(self):
        from scripts.package_release import FILES
        self.assertIn("dist/syntyr.collaboration.css", FILES)
        self.assertIn("docs/collaboration.md", FILES)
        self.assertIn("examples/collaboration.html", FILES)
        guide = (ROOT / "docs/collaboration.md").read_text()
        self.assertIn("syntyr.collaboration.css", guide)
        self.assertIn("application", guide.lower())
        self.assertIn("Chatudo", guide)
        self.assertIn("examples/collaboration.html", (ROOT / "README.md").read_text())
        for script in ("browser_matrix.py", "reflow_test.py", "axe_audit.py"):
            self.assertIn('"examples/collaboration.html"', (ROOT / "tests" / script).read_text())


if __name__ == "__main__":
    unittest.main()
