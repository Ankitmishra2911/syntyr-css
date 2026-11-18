"""CodeMirror 6 is an optional docs-only enhancement with an HTML textarea fallback."""
from pathlib import Path
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CodeMirrorPlaygroundTests(unittest.TestCase):
    def test_isolated_pinned_editor_build(self):
        manifest = ROOT / "tools/playground-editor/package.json"
        package = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertTrue(package["private"])
        self.assertIn("codemirror", package["dependencies"])
        self.assertIn("@codemirror/lang-html", package["dependencies"])
        self.assertIn("esbuild", package["devDependencies"])
        for section in ("dependencies", "devDependencies"):
            for version in package[section].values():
                self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertTrue((manifest.parent / "package-lock.json").is_file())
        source = (manifest.parent / "src/editor.mjs").read_text()
        self.assertIn('from "codemirror"', source)
        self.assertIn('from "@codemirror/lang-html"', source)
        self.assertIn("EditorView.updateListener", source)
        self.assertIn("syntyr:load-example", source)
        self.assertIn("dispatchEvent", source)
        self.assertTrue((ROOT / "docs/playground-editor.js").is_file())

    def test_textarea_remains_source_of_truth_and_progressive_fallback(self):
        page = (ROOT / "docs/playground.html").read_text()
        controller = (ROOT / "docs/playground.js").read_text()
        self.assertIn('id="playground-markup"', page)
        self.assertIn('src="playground-editor.js"', page)
        self.assertIn('id="playground-editor-mount"', page)
        self.assertIn('textarea', page)
        self.assertIn('syntyr:load-example', controller)
        self.assertIn('markup.value', controller)
        self.assertIn('sandbox="allow-same-origin"', page)
        self.assertNotIn('allow-scripts', page)

    def test_site_includes_only_self_hosted_editor_asset(self):
        publisher = (ROOT / "scripts/build_cloudflare_site.py").read_text()
        self.assertIn('"playground-editor.js"', publisher)
        self.assertNotIn('cdn.jsdelivr', (ROOT / "docs/playground.html").read_text())
        self.assertNotIn('unpkg.com', (ROOT / "docs/playground.html").read_text())
        notices = (ROOT / "docs/playground-editor.licenses.txt").read_text()
        self.assertIn("@codemirror/view", notices)
        self.assertIn("@lezer/html", notices)
        self.assertIn("MIT License", notices)
        self.assertIn("playground-editor.licenses.txt", publisher)
        self.assertIn("CodeMirror 6", (ROOT / "THIRD_PARTY_NOTICES.md").read_text())

if __name__ == "__main__":
    unittest.main()
