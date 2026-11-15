"""Contracts for the opt-in Lit demonstration; no Node dependency for this suite."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "lit"


class ElementParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class LitInteroperabilityContract(unittest.TestCase):
    def test_lit_demo_is_isolated_from_the_css_distribution(self):
        core = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        demo = json.loads((DEMO / "package.json").read_text(encoding="utf-8"))
        self.assertNotIn("dependencies", core)
        self.assertNotIn("devDependencies", core)
        self.assertTrue(demo["private"])
        self.assertIn("lit", demo["dependencies"])
        self.assertIn("esbuild", demo["devDependencies"])
        self.assertEqual(demo["scripts"]["build"].count("--bundle"), 1)
        self.assertTrue((DEMO / ".gitignore").is_file())
        self.assertNotIn("examples/lit", (ROOT / "scripts/build_cloudflare_site.py").read_text())

    def test_html_has_static_fallback_and_only_local_assets(self):
        html = (DEMO / "index.html").read_text(encoding="utf-8")
        parser = ElementParser()
        parser.feed(html)
        self.assertTrue(any(
            tag in {"main", "body"} and "syn-root" in attrs.get("class", "").split()
            for tag, attrs in parser.elements
        ))
        self.assertTrue(any(
            tag == "link" and attrs.get("href") == "../../dist/syntyr.core.css"
            for tag, attrs in parser.elements
        ))
        self.assertEqual(
            [attrs.get("src") for tag, attrs in parser.elements if tag == "script"],
            ["./dist/demo.js"],
        )
        for tag in ("syn-demo-status-panel", "syn-demo-shadow-signal"):
            self.assertTrue(any(el == tag for el, _ in parser.elements), tag)
        self.assertGreaterEqual(html.count("data-lit-fallback"), 2)
        self.assertNotIn("https://", html)
        self.assertNotIn("onclick=", html)

    def test_light_dom_component_uses_real_syntyr_classes_and_public_event(self):
        js = (DEMO / "status-panel.js").read_text(encoding="utf-8")
        self.assertIn("createRenderRoot()", js)
        self.assertIn("return this;", js)
        self.assertIn("data-lit-fallback", js)
        self.assertIn("syn-panel", js)
        self.assertIn("syn-status--success", js)
        self.assertIn("static properties", js)
        self.assertIn("reflect: true", js)
        self.assertIn("?disabled=", js)
        self.assertIn("new CustomEvent(", js)
        self.assertIn("bubbles: true", js)
        self.assertIn("composed: true", js)

    def test_shadow_dom_component_uses_inherited_tokens_and_exposes_parts(self):
        js = (DEMO / "shadow-signal.js").read_text(encoding="utf-8")
        self.assertIn("static styles = css", js)
        for token in ("--syn-surface", "--syn-text", "--syn-accent", "--syn-focus-ring"):
            self.assertIn(token, js)
        for part in ('part="panel"', 'part="toggle"'):
            self.assertIn(part, js)
        self.assertIn("aria-pressed=", js)
        self.assertIn("new CustomEvent(", js)
        self.assertNotIn("createRenderRoot()", js)

    def test_contract_and_guides_describe_interoperability_boundary(self):
        guide = (ROOT / "docs/lit-integration.md").read_text(encoding="utf-8")
        spec = (ROOT / "docs/component-authoring.md").read_text(encoding="utf-8")
        framework_guide = (ROOT / "docs/framework-integrations.md").read_text()
        readme = (ROOT / "README.md").read_text()
        for term in ("Shadow DOM", "Light DOM", "::part()", "--syn-", "npm ci",
                     "progressive enhancement", "custom event"):
            self.assertIn(term.lower(), guide.lower(), term)
        for term in ("disabled", "aria-", "data-syn-", "CSS", "CustomEvent", "keyboard"):
            self.assertIn(term.lower(), spec.lower(), term)
        self.assertIn("lit-integration.md", framework_guide)
        self.assertIn("lit-integration.md", readme)
        self.assertIn('href="lit-integration.html"', (ROOT / "docs/guides.html").read_text())
        self.assertTrue((ROOT / "tests/lit_browser.py").is_file())


if __name__ == "__main__":
    unittest.main()
