"""Enforce the public opt-in root boundary and intrinsic layout contract."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RootScopingContract(unittest.TestCase):
    def test_every_component_module_is_opt_in_under_syn_root(self):
        for source in sorted((ROOT / "src/components").glob("*.css")):
            with self.subTest(component=source.stem):
                css = source.read_text(encoding="utf-8")
                self.assertIn(":where(.syn-root) {", css)

    def test_semantic_mode_requires_syn_root_on_same_or_ancestor_element(self):
        css = (ROOT / "src/semantic.css").read_text(encoding="utf-8")
        self.assertIn(":is(.syn-root.syn-semantic, .syn-root .syn-semantic)", css)
        self.assertNotIn(".syn-semantic :where(", css)
        self.assertIn("button[data-syn-semantic]", css)

    def test_optional_presentation_modules_do_not_style_outside_root(self):
        for module in ("recipes", "geometry", "effects"):
            with self.subTest(module=module):
                css = (ROOT / "src" / f"{module}.css").read_text(encoding="utf-8")
                self.assertIn(":where(.syn-root) {", css)

    def test_layout_adapts_to_container_instead_of_viewport(self):
        css = (ROOT / "src/components/layout.css").read_text(encoding="utf-8")
        self.assertIn("grid-template-columns: repeat(auto-fit, minmax(min(100%, 21rem), 1fr))", css)
        self.assertNotIn("@media (max-width: 45rem) { .syn-layout", css)

    def test_root_itself_can_form_container_query_region(self):
        css = (ROOT / "src/components/patterns.css").read_text(encoding="utf-8")
        self.assertIn(":where(.syn-root.syn-region)", css)


if __name__ == "__main__":
    unittest.main()
