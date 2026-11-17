# Working on Syntyr CSS (repository agent instructions)

Syntyr is an MIT-licensed, CSS-first design system. The `syn-*` class namespace, `--syn-*` tokens, and `data-syn-*` attributes form its public API. This file guides **contributors to this repository**; consumer agents should read [docs/ai-quickstart.md](docs/ai-quickstart.md) or [agents/syntyr/SKILL.md](agents/syntyr/SKILL.md).

## Source of truth
- Edit `src/*.css` and `src/components/*.css`, not generated `dist/*.css`. `scripts/build.py` is the CSS distribution manifest.
- Prefer semantic HTML, native CSS, scoped `.syn-root` and opt-in `.syn-semantic`. Do not introduce mandatory JavaScript, network assets, npm, or runtime dependencies.
- Keep opt-in effects, Viz, recipes, geometry, symbols, utilities and print modules separate. Never quietly move optional CSS into core.
- Compose existing HTML, classes, tokens and native states before adding a new CSS class, variant, abstraction or module. If a new primitive is genuinely necessary, document the composition alternatives, reuse evidence and long-term cost in the PR.
- Keep React, Tailwind, shadcn, Figma, and agent/editor tooling as independently removable adapters that consume the public CSS contract; never make core CSS or its build depend on them. Vendor selectors, directives and states belong only in `integrations/`.
- Design for keyboard navigation, zoom/reflow, forced colors and reduced motion. Do not misuse ARIA to simulate application behavior.
- Document compatibility changes in `docs/api-stability.md`; experimental alpha APIs may change without compatibility aliases.
- Verify actual selectors against the appropriate CSS module before documenting them. CSS doesn't implement fetching, authentication, validation or chart calculation.

## Version boundaries
- `VERSION` identifies the current **unreleased** source candidate, presently `0.3.0-alpha.5`.
- The currently published immutable release is `0.3.0-alpha.4`; it does not include every candidate module or theme.
- Do not imply that the source candidate's APIs are in the published release. Prefer pinned assets in consumer examples.

## Verification
Run from the repository root:

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 scripts/build_playground_catalog.py --check
python3 scripts/maintenance_policy.py
python3 scripts/build_agent_docs.py
python3 scripts/build_agent_docs.py --check
python3 -m unittest discover -s tests -v
python3 scripts/build_cloudflare_site.py
python3 scripts/build_cloudflare_site.py --check
```

The Python standard library is the only mandatory build requirement. Browser checks use optional developer-installed Playwright.

## Publishing and safety
- Cloudflare uses a strict file allowlist in `scripts/build_cloudflare_site.py`; a new public doc needs an explicit entry. The release ZIP uses its own allowlist in `scripts/package_release.py`.
- Never publish `business/`, `.env`, credentials, internal working notes, `tests/` or the repo root wholesale.
- Update `llms.txt` when public documentation changes. `llms-full.txt` is generated; never edit it directly.
- `metadata/components.json` is a **curated, non-exhaustive** agent-facing catalog. Each class must exist in its declared CSS module; tests check this. Prefer expanding canonical docs over cloning them into multiple hand-maintained indexes.
- `docs/catalog.html` owns the copyable HTML gallery. If it changes, regenerate `docs/playground-catalog.js` via `python3 scripts/build_playground_catalog.py`; the static site build rejects stale generated snippets. Do not edit the generated JS by hand.
- Work on a feature branch; do not commit generated local preview directories.
