# Optional real-browser adoption regression

`tests/adoption_visual_browser.py` runs **Chromium** against three built
independent consumer fixtures: Tailwind v4, static Astro and the opt-in
shadcn semantic-token example. It uses ephemeral local HTTP servers and
checks real DOM/computed styles, nested theme tokens, keyboard focus outlines,
missing assets and viewport overflow. It compares PNG screenshots against
checked-in baselines at `tests/visual-baselines/`.

This is **development-only** tooling, not part of Syntyr's CSS package or
its zero-JS runtime contract. It is not yet an enforced release gate.

## Commands

```sh
cd examples/tailwind-v4 && npm install && npm run build && cd ../..
cd examples/astro && npm install && npm run build && cd ../..
cd examples/shadcn-bridge && npm install && npm run build && cd ../..

python3 -m venv /tmp/syntyr-adoption-browser
/tmp/syntyr-adoption-browser/bin/pip install playwright pillow
/tmp/syntyr-adoption-browser/bin/python -m playwright install chromium
/tmp/syntyr-adoption-browser/bin/python tests/adoption_visual_browser.py
```

If a verified Chromium binary is already installed, optionally point to
it with `SYNTYR_CHROMIUM_EXECUTABLE=/absolute/path/to/chrome` when running.
Baselines in this branch were captured on Linux using the local Chromium
1255 Playwright-browser cache. Rendering differences across operating systems,
browser revisions and installed fonts can cause false positives. The current
comparison tolerates up to 2% pixels differing by more than 24 units.

For **intentional**, reviewed UI changes, regenerate baselines with
`--update-baselines`, inspect all three PNG images and commit the new
artifacts. Do not regenerate baselines simply to hide a failure.

Use this alongside accessibility/axe checks; pixel comparisons alone cannot
verify screen-reader semantics, correct focus order, or component behavior.
