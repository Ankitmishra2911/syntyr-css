"""Regression tests for source ownership and low-entropy CSS distribution."""
from pathlib import Path
import tempfile
import unittest

from scripts.maintenance_policy import find_issues


class MaintenancePolicyTests(unittest.TestCase):
    def test_current_source_and_distribution_registry_have_no_drift(self):
        self.assertEqual(find_issues(), [])

    def test_root_font_role_aliases_have_one_canonical_default(self):
        tokens = (Path(__file__).resolve().parents[1] / "src/tokens.css").read_text()
        self.assertEqual(tokens.count("--syn-font-ui: var(--syn-font);"), 1)
        self.assertEqual(tokens.count("--syn-font-display: var(--syn-font);"), 1)

    def test_duplicate_bundle_sources_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "tokens.css").write_text("@layer syn.tokens {}")
            issues = find_issues(src, {"syntyr.core.css": ("tokens.css", "tokens.css")})
            self.assertTrue(any("duplicate source" in issue for issue in issues), issues)

    def test_unregistered_css_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "tokens.css").write_text("@layer syn.tokens {}")
            (src / "abandoned.css").write_text(".unused { color: red; }")
            issues = find_issues(src, {"syntyr.core.css": ("tokens.css",)})
            self.assertTrue(any("unregistered source: abandoned.css" in issue for issue in issues), issues)

    def test_missing_registered_css_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            issues = find_issues(Path(directory), {"syntyr.core.css": ("missing.css",)})
            self.assertTrue(any("missing source: missing.css" in issue for issue in issues), issues)

    def test_component_theme_forks_are_rejected_but_token_themes_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "components").mkdir()
            (src / "tokens.css").write_text(':where(.syn-root[data-syn-theme="noir"]) { --syn-bg: black; }')
            (src / "components" / "card.css").write_text('/* [data-syn-theme="ignored"] */\n.syn-card[data-syn-theme="noir"] { color: red; }')
            bundles = {"syntyr.core.css": ("tokens.css", "components/card.css")}
            issues = find_issues(src, bundles)
            self.assertTrue(any("component theme fork" in issue for issue in issues), issues)
            (src / "components" / "card.css").write_text('/* [data-syn-theme="ignored"] */\n.syn-card { color: var(--syn-bg); }')
            self.assertEqual(find_issues(src, bundles), [])

    def test_optional_recipes_cannot_fork_presentation_by_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "recipes.css").write_text('.syn-card[data-syn-theme="noir"] { border: 1px solid red; }')
            issues = find_issues(src, {"syntyr.recipes.css": ("recipes.css",)})
            self.assertTrue(any("theme fork" in issue for issue in issues), issues)

    def test_core_refuses_framework_specific_css_directives_and_selectors(self):
        examples = (
            "@theme inline { --color-ui: blue; }",  # Tailwind v4
            ".syn-root { @apply flex; }",  # Tailwind-only syntax
            ".syn-shadcn { color: red; }",  # Adapter-owned surface
            ".syn-shadcn-button { color: red; }",  # Adapter-owned extension
            ".syn-radix[data-state=\"open\"] { color: red; }",  # Adapter-owned surface
            ".syn-root { color: var(--radix-popover-trigger-width); }",  # Vendor variable
            ".syn-root[data-radix-menu-content] { color: red; }",  # Vendor DOM shape
        )
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            file = src / "components" / "card.css"
            file.parent.mkdir()
            registry = {"syntyr.core.css": ("components/card.css",)}
            for css in examples:
                with self.subTest(css=css):
                    file.write_text(css)
                    issues = find_issues(src, registry)
                    self.assertTrue(any("integration leak" in issue for issue in issues), issues)

    def test_comments_do_not_trigger_integration_leak_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            file = src / "tokens.css"
            file.write_text("/* @apply .syn-radix --tw-color */\n.syn-root { color: var(--syn-text); }")
            self.assertEqual(find_issues(src, {"syntyr.core.css": ("tokens.css",)}), [])

    def test_css_imports_rejected_in_css_core(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            f = src / "tokens.css"
            registry = {"syntyr.core.css": ("tokens.css",)}
            for value in ('@import "theme.css";', '@import url("https://example.org/font.css");'):
                with self.subTest(value=value):
                    f.write_text(value, encoding="utf-8")
                    self.assertTrue(any("CSS import" in e for e in find_issues(src, registry)))

    def test_unbundled_css_urls_rejected_but_embedded_sources_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            f = src / "tokens.css"
            registry = {"syntyr.core.css": ("tokens.css",)}
            for value in ('url("https://example.org/logo.svg")', 'url(/images/logo.svg)',
                          'url("../icons/logo.svg")', 'url(//example.org/logo.svg)'):
                with self.subTest(value=value):
                    f.write_text(f'.syn-root {{ background: {value}; }}', encoding="utf-8")
                    self.assertTrue(any("external CSS asset" in e for e in find_issues(src, registry)))
            f.write_text('/* @import "bad.css"; url(https://bad.test/img) */'
                         '.syn-root { filter: url("#contrast");'
                         'background: url(data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=); }', encoding="utf-8")
            self.assertEqual(find_issues(src, registry), [])

    def test_important_declarations_outside_accessibility_base_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "components").mkdir()
            (src / "base.css").write_text("@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }")
            (src / "components" / "card.css").write_text(".syn-card { color: red !important; }")
            bundles = {"syntyr.core.css": ("base.css", "components/card.css")}
            issues = find_issues(src, bundles)
            self.assertTrue(any("!important outside base.css" in issue for issue in issues), issues)
            (src / "components" / "card.css").write_text("/* !important is discouraged */ .syn-card { color: red; }")
            self.assertEqual(find_issues(src, bundles), [])


if __name__ == "__main__":
    unittest.main()
