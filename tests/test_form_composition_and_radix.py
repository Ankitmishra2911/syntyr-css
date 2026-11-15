"""Contract tests for opt-in form composition and headless UI styling."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FormCompositionAndRadixContract(unittest.TestCase):
    def test_form_composition_is_in_core_but_not_a_second_runtime(self):
        from scripts.build import COMPONENTS, distributions
        self.assertIn("components/form-composition.css", COMPONENTS)
        css = (ROOT / "src/components/form-composition.css").read_text()
        core = (ROOT / "dist/syntyr.core.css").read_text()
        self.assertIn(css.strip(), core)
        self.assertIn(css.strip(), (ROOT / "dist/syntyr.all.css").read_text())
        self.assertIn("components/form-composition.css", distributions()["syntyr.core.css"])
        self.assertIn("@layer syn.components", css)
        self.assertNotIn("@import", css)
        self.assertNotIn("url(", css)
        self.assertNotIn("!important", css)

    def test_form_fields_support_labels_help_and_container_responsiveness(self):
        css = (ROOT / "src/components/form-composition.css").read_text()
        for selector in (".syn-field", ".syn-field-row", ".syn-field-body",
                         ".syn-input-group", ".syn-input-addon"):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
        self.assertIn("@container syn-region", css)
        self.assertIn("minmax(0, 1fr)", css)
        self.assertIn("min-inline-size: 0", css)
        self.assertIn("border-inline-start", css)
        self.assertIn("forced-colors: active", css)

    def test_radix_styles_are_opt_in_and_never_bundled_into_core(self):
        adapter = (ROOT / "integrations/radix/states.css").read_text()
        self.assertIn(".syn-radix", adapter)
        self.assertIn(".syn-root.syn-radix", adapter)
        self.assertNotIn("display: none", adapter)
        self.assertIn('[data-state="on"]', adapter)
        self.assertIn('[data-state="open"]', adapter)
        self.assertIn("[data-disabled]", adapter)
        self.assertIn("syn-accordion-trigger", adapter)
        self.assertNotIn(".syn-radix", (ROOT / "dist/syntyr.core.css").read_text())
        self.assertNotIn(".syn-radix", (ROOT / "dist/syntyr.all.css").read_text())
        self.assertNotIn("@import", adapter)
        self.assertNotIn("url(", adapter)
        self.assertNotIn("pointer-events: none", adapter)

    def test_copy_owned_recipes_are_semantic_and_have_fallbacks(self):
        recipes = (ROOT / "docs/component-recipes.md").read_text()
        for pattern in ('class="syn-field"', 'class="syn-input-group"',
                        'class="syn-field-row"', 'aria-describedby=', 'method="get"',
                        'type="submit"', 'required'):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, recipes)
        self.assertIn("No JavaScript", recipes)
        self.assertIn("progressive enhancement", recipes.lower())
        self.assertIn("input", recipes)

    def test_radix_integration_docs_require_accessible_behavior_owner(self):
        doc = (ROOT / "docs/radix-integration.md").read_text()
        self.assertIn("radix/states.css", doc)
        self.assertIn("syn-radix", doc)
        self.assertIn("keyboard", doc.lower())
        self.assertIn("aria", doc.lower())
        self.assertIn("data-state", doc)
        self.assertIn("does not", doc.lower())


    def test_review_forced_color_state_visibility(self):
        css = (ROOT / "integrations/radix/states.css").read_text()
        forced = css.split("@media (forced-colors: active)", 1)[1]
        self.assertIn('.syn-button[data-state="on"]', forced)
        self.assertIn('.syn-button[data-state="checked"]', forced)
        self.assertIn("border-color: Highlight", forced)

    def test_review_readme_links_to_live_rendered_example(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("https://syntyr-css.pages.dev/examples/form-composition.html", readme)

    def test_review_browser_test_avoids_immediate_transition_sampling(self):
        smoke = (ROOT / "tests/form_composition_browser.py").read_text()
        self.assertIn("page.wait_for_function", smoke)


if __name__ == "__main__":
    unittest.main()
