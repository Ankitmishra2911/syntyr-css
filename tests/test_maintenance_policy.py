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
            file.write_text("/* @apply .syn-radix --tw-color */\n.syn-root { color: var(--syn-text, CanvasText); }")
            self.assertEqual(find_issues(src, {"syntyr.core.css": ("tokens.css",)}), [])

    def test_important_declarations_outside_accessibility_base_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src / "components").mkdir()
            (src / "base.css").write_text("@media (prefers-reduced-motion: reduce) { * { animation-duration: 0s !important; } }")
            (src / "components" / "card.css").write_text(".syn-card { color: red !important; }")
            bundles = {"syntyr.core.css": ("base.css", "components/card.css")}
            issues = find_issues(src, bundles)
            self.assertTrue(any("!important outside base.css" in issue for issue in issues), issues)
            (src / "components" / "card.css").write_text("/* !important is discouraged */ .syn-card { color: red; }")
            self.assertEqual(find_issues(src, bundles), [])



class VariableResolutionPolicyTests(unittest.TestCase):
    """CSS var() without a declared token or fallback is silent runtime breakage."""

    def test_undefined_variable_without_fallback_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "buttons.css").write_text(
                ".syn-button { color: var(--syn-missing-color); }"
            )
            issues = find_issues(source, {"buttons.css": ("buttons.css",)})
            self.assertTrue(any("--syn-missing-color" in issue for issue in issues), issues)

    def test_custom_variable_with_explicit_fallback_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "buttons.css").write_text(
                ".syn-button { color: var(--syn-override, var(--syn-inner, blue)); }"
            )
            self.assertEqual(find_issues(source, {"buttons.css": ("buttons.css",)}), [])

    def test_defined_token_used_by_another_module_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "tokens.css").write_text(":root { --syn-accent: blue; }")
            (source / "buttons.css").write_text(".syn-button { color: var(--syn-accent); }")
            self.assertEqual(find_issues(source, {"css": ("tokens.css", "buttons.css")}), [])

    def test_comment_only_variable_reference_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "buttons.css").write_text(
                "/* var(--syn-discontinued) */ .syn-button { color: var(--syn-override, blue); }"
            )
            self.assertEqual(find_issues(source, {"buttons.css": ("buttons.css",)}), [])


    def test_quoted_variable_references_do_not_trigger_false_positives(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "label.css").write_text(
                r'.syn-label { content: "escaped \"quote\" var(--syn-not-a-variable)"; }'
            )
            self.assertEqual(find_issues(source, {"css": ("label.css",)}), [])

    def test_quoted_fake_declarations_do_not_hide_undefined_variables(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "label.css").write_text(
                '.syn-label { content: "--syn-not-declared: teal"; color: var(--syn-not-declared); }'
            )
            issues = find_issues(source, {"css": ("label.css",)})
            self.assertTrue(any("unresolved CSS variable" in issue for issue in issues), issues)


class ImportantExceptionPolicyTests(unittest.TestCase):
    def test_important_outside_reduced_motion_is_rejected_in_base(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                ".syn-root { color: red !important; }\n"
                "@media (prefers-reduced-motion: reduce) { .syn-root * { animation-duration: 0s !important; } }"
            )
            issues = find_issues(source, {"core": ("base.css",)})
            self.assertTrue(any("!important outside reduced-motion" in issue for issue in issues), issues)

    def test_unrelated_important_within_reduced_motion_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                "@media (prefers-reduced-motion: reduce) { .syn-root { color: red !important; } }"
            )
            issues = find_issues(source, {"core": ("base.css",)})
            self.assertTrue(any("!important" in issue for issue in issues), issues)

    def test_supported_reduced_motion_overrides_remain_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                "@media (prefers-reduced-motion: reduce) { .syn-root * {"
                "scroll-behavior: auto !important;"
                "transition-duration: 0s !important;"
                "animation-duration: 0s !important;" "} }"
            )
            self.assertEqual(find_issues(source, {"core": ("base.css",)}), [])

    def test_reduced_motion_exception_rejects_negated_media(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                '@media not all and (prefers-reduced-motion: reduce) {'
                ' .syn-root { animation-duration: 0s !important; } }'
            )
            issues = find_issues(source, {"core": ("base.css",)})
            self.assertTrue(any("outside reduced-motion" in issue for issue in issues), issues)

    def test_reduced_motion_exception_rejects_unrestricted_media_list(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                '@media screen, (prefers-reduced-motion: reduce) {'
                ' .syn-root { animation-duration: 0s !important; } }'
            )
            issues = find_issues(source, {"core": ("base.css",)})
            self.assertTrue(any("outside reduced-motion" in issue for issue in issues), issues)

    def test_reduced_motion_exception_accepts_nested_media_after_declaration(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "base.css").write_text(
                '.syn-root { color: red; @media (prefers-reduced-motion: reduce) {'
                ' animation-duration: 0s !important; } }'
            )
            self.assertEqual(find_issues(source, {"core": ("base.css",)}), [])

if __name__ == "__main__":
    unittest.main()
