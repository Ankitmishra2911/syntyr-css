"""v0.4 geometry + terminal enhancement contracts (zero runtime JS)."""
from pathlib import Path
import gzip
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GeometryTerminalContract(unittest.TestCase):
    def test_geometry_is_opt_in_and_ships_as_independent_module(self):
        geometry = (ROOT / "src/geometry.css").read_text()
        build = (ROOT / "scripts/build.py").read_text()
        self.assertIn("cy.geometry", geometry)
        self.assertIn("'cyberline.geometry.css': ('geometry.css',)", build)
        self.assertIn("'geometry.css'", build)
        self.assertIn(".cy-frame--bevel", geometry)
        self.assertIn(".cy-frame--notch", geometry)
        self.assertIn(".cy-frame--bracket", geometry)
        self.assertIn(".cy-frame--inset", geometry)
        self.assertIn(".cy-frame--circuit", geometry)
        self.assertIn("--cy-frame-cut", geometry)
        self.assertIn("--cy-frame-stroke", geometry)
        self.assertIn("@media (forced-colors: active)", geometry)
        core = (ROOT / "dist/cyberline.core.css").read_text()
        all_css = (ROOT / "dist/cyberline.all.css").read_text()
        self.assertNotIn(".cy-frame--bevel", core)
        self.assertIn(".cy-frame--bevel", all_css)
        self.assertLessEqual(len(gzip.compress((ROOT / "dist/cyberline.all.css").read_bytes(), mtime=0)), 8 * 1024)

    def test_table_emphasis_is_opt_in(self):
        css = (ROOT / "src/components/data.css").read_text()
        self.assertNotIn("td:last-child", css)
        self.assertIn(".cy-table-emphasis", css)
        self.assertIn(".cy-cell--numeric", css)
        self.assertIn("font-variant-numeric: tabular-nums", css)

    def test_long_technical_captions_wrap_at_text_zoom(self):
        typography = (ROOT / "src/components/typography.css").read_text()
        self.assertIn("overflow-wrap: anywhere", typography.split(".cy-caption {", 1)[1].split("}", 1)[0])

    def test_stack_grid_allows_terminal_to_shrink_to_mobile_viewport(self):
        layout = (ROOT / "src/components/layout.css").read_text()
        self.assertIn(".cy-stack { display: grid; grid-template-columns: minmax(0, 1fr);", layout)

    def test_nested_geometry_tokens_are_respected(self):
        css = (ROOT / "src/geometry.css").read_text()
        root = css.split(".cy-frame {", 1)[1].split("}", 1)[0]
        for token in ("--cy-frame-cut:", "--cy-frame-stroke:",
                      "--cy-frame-fill:", "--cy-frame-outline:"):
            self.assertNotIn(token, root, "frames must not overwrite inherited tokens")
        for default in ("var(--cy-frame-cut, 1rem)", "var(--cy-frame-stroke, 1px)",
                        "var(--cy-frame-fill, var(--cy-surface))",
                        "var(--cy-frame-outline, var(--cy-frame-strong))"):
            self.assertIn(default, css)

    def test_disabled_button_hover_states_are_excluded(self):
        css = (ROOT / "src/components/buttons.css").read_text()
        for variant in (".cy-button", ".cy-button--primary", ".cy-button--outline",
                        ".cy-button--danger", ".cy-button--ghost"):
            self.assertIn(variant + ":not(:disabled):not([aria-disabled=\"true\"]):hover", css)
        self.assertIn("cursor: not-allowed", css)

    def test_aria_disabled_is_not_functionally_disabled_by_css(self):
        css = (ROOT / "src/components/buttons.css").read_text()
        self.assertNotIn("pointer-events: none", css)
        docs = (ROOT / "docs/components.md").read_text()
        self.assertIn("aria-disabled", docs)
        self.assertIn("does not block activation", docs)

    def test_terminal_readouts_and_states_are_optional(self):
        css = (ROOT / "src/recipes.css").read_text()
        for selector in (".cy-terminal-title", ".cy-terminal-dots", ".cy-terminal-output",
                         ".cy-terminal-error", ".cy-terminal-warning", ".cy-terminal-cursor",
                         ".cy-terminal-path", ".cy-terminal-meta"):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
        self.assertNotIn("@keyframes", css)
        self.assertIn("prefers-reduced-motion", (ROOT / "src/base.css").read_text())

    def test_original_gallery_has_geometry_terminal_example_without_javascript(self):
        page = (ROOT / "examples/geometry-terminal.html").read_text()
        for value in ("cy-frame--bevel", "cy-frame--bracket", "cy-frame--notch",
                      "cy-frame--inset", "cy-frame--circuit", "cy-terminal", "<main",
                      "cy-table-emphasis", "cy-terminal-error", "cy-terminal-warning"):
            with self.subTest(value=value):
                self.assertIn(value, page)
        self.assertIn('href="#main"', page)
        self.assertIn('<main id="main">', page)
        self.assertNotIn("<script", page.lower())
        self.assertIn("geometry-terminal.html", (ROOT / "docs/index.html").read_text())
        self.assertIn("dist/cyberline.geometry.css", page)

    def test_standalone_distribution_is_tracked_for_clean_checkouts(self):
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "dist/cyberline.geometry.css"],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, "generated geometry CSS must be committed, not only built locally")

    def test_download_package_includes_geometry(self):
        package = (ROOT / "scripts/package_release.py").read_text()
        self.assertIn('"dist/cyberline.geometry.css"', package)


if __name__ == "__main__":
    unittest.main()
