"""Opt-in server-rendered framework compatibility; no added core runtime."""
from html.parser import HTMLParser
from pathlib import Path
import json
import unittest

from scripts.build import distributions

ROOT = Path(__file__).resolve().parents[1]


class TagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ServerFrameworkIntegrationTests(unittest.TestCase):
    def test_optional_stylesheet_is_distributed_and_does_not_change_core(self):
        files = distributions()
        self.assertEqual(files["syntyr.server.css"], ("server.css",))
        self.assertNotIn("server.css", files["syntyr.core.css"])
        self.assertNotIn("server.css", files["syntyr.semantic-bundle.css"])
        self.assertIn("server.css", files["syntyr.all.css"])
        self.assertEqual(
            (ROOT / "src/server.css").read_text().strip() + "\n",
            (ROOT / "dist/syntyr.server.css").read_text(),
        )
        pkg = json.loads((ROOT / "package.json").read_text())
        self.assertEqual(pkg["exports"]["./server.css"], "./dist/syntyr.server.css")

    def test_opt_in_styles_are_scoped_and_do_not_manage_state_or_dom(self):
        css = (ROOT / "src/server.css").read_text()
        self.assertIn("@layer syn.components", css)
        self.assertIn(".syn-root", css)
        for token in (
            "[data-loading]", ".htmx-request", ".phx-click-loading",
            ".phx-submit-loading", ".phx-change-loading", "turbo-frame[busy]",
            '[data-syn-state="loading"]',
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)
        self.assertNotIn("!important", css)
        self.assertNotIn("pointer-events: none", css)
        self.assertNotIn("opacity:", css)
        self.assertNotIn("animation:", css)
        self.assertNotIn("@import", css)
        self.assertNotIn("url(", css)

    def test_copyable_templates_use_identical_css_contract(self):
        fixtures = {
            "liveview.heex": ("phx-submit", "phx-change", "phx-disable-with"),
            "livewire.blade.php": ("wire:submit", "wire:model", "data-syn-theme"),
            "turbo.html": ("turbo-frame", "data-turbo-frame", 'method="get"'),
            "search.templ": ('templ Search(', 'method="get"', 'class="syn-button'),
        }
        for file, required in fixtures.items():
            with self.subTest(file=file):
                template = (ROOT / "examples/server-rendered" / file).read_text()
                self.assertIn("syn-root", template)
                self.assertIn("syn-input", template)
                self.assertIn("syn-button", template)
                self.assertNotIn("<script", template.lower())
                for fragment in required:
                    self.assertIn(fragment, template)
        turbo = TagParser()
        turbo.feed((ROOT / "examples/server-rendered/turbo.html").read_text())
        self.assertTrue(any(tag == "turbo-frame" for tag, _ in turbo.tags))
        self.assertTrue(any(tag == "form" and a.get("method") == "get" for tag, a in turbo.tags))

    def test_copy_owned_go_server_components_reuse_core_without_runtime(self):
        base = ROOT / "examples/server-components-go"
        mod = (base / "go.mod").read_text()
        component = (base / "templates/components.html").read_text()
        page = (base / "templates/page.html").read_text()
        handler = (base / "main.go").read_text()
        guide = (ROOT / "docs/framework-integrations.md").read_text()
        self.assertNotIn("require ", mod)
        self.assertIn('"html/template"', handler)
        self.assertIn('"net/url"', handler)
        self.assertIn('template.ParseFS', handler)
        self.assertNotIn("template.HTML(", handler)
        self.assertIn("examples/server-components-go", guide)
        self.assertIn("examples/server-components-go", (ROOT / "llms.txt").read_text())
        for name in ("syn.field", "syn.notice", "syn.button", "syn.table", "syn.pagination"):
            self.assertIn('{{define "' + name + '"}}', component)
            self.assertIn('{{template "' + name + '"', page)
        for attr in ('aria-invalid="true"', 'aria-describedby=', 'role="alert"', 'scope="col"', 'scope="row"'):
            if attr == 'role="alert"':
                self.assertIn('role="{{if .Danger}}alert', component)
            else:
                self.assertIn(attr, component)
        for css_class in ("syn-field", "syn-input", "syn-alert", "syn-button", "syn-table"):
            self.assertIn(css_class, component)
        self.assertIn("syntyr.core.css", page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn("<script", component.lower())

    def test_docs_cover_versions_and_dom_ownership_without_claiming_runtime(self):
        guide = (ROOT / "docs/framework-integrations.md").read_text()
        for name in ("LiveView", "Livewire", "Turbo", "HTMX", "Go templ",
                     "syntyr.server.css", "wire:loading", "data-loading",
                     "phx-submit-loading", "turbo-frame[busy]", "aria-busy"):
            self.assertIn(name, guide)
        self.assertIn("examples/server-rendered/", guide)
        self.assertIn("zero", guide.lower())


if __name__ == "__main__":
    unittest.main()
