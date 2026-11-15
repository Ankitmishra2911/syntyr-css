# Syntyr editor autocomplete and metadata

Syntyr's editor integration is **optional**. Applications still consume ordinary
prebuilt CSS, HTML, and custom properties without Node, JavaScript, or a build step.

## VS Code and compatible editors

For an opt-in local extension package that bundles these files without an extension runtime, see [ecosystem interoperability](ecosystem-integrations.md). The extension is not yet published to the VS Code Marketplace; the manual workspace integration below remains supported.

Copy these four generated files from the Syntyr release or repository into
your project, e.g. `./vendor/syntyr/metadata/`:

- `syntyr.html-custom-data.json` — HTML attribute values, including themes
- `syntyr.css-custom-data.json` — documented `--syn-*` custom properties
- `syntyr.code-snippets` — a curated set of class completion snippets
- `syntyr-api.json` — complete machine-readable index of classes, tokens and themes

Add the following to your **workspace** `.vscode/settings.json` (not required
for Syntyr consumers using other editors):

```json
{
  "html.customData": ["./vendor/syntyr/metadata/syntyr.html-custom-data.json"],
  "css.customData": ["./vendor/syntyr/metadata/syntyr.css-custom-data.json"]
}
```

Optionally copy `syntyr.code-snippets` to `.vscode/syntyr.code-snippets`.
This provides snippets for common `syn-*` classes in HTML and JSX/TSX. The
custom HTML data includes all classes as possible `class` attribute values,
but the extent of **class-name completion** varies by editor and extension;
do not assume it works identically in every language mode. CSS custom
property autocomplete also depends on the editor's CSS language support.

The JSON files are standard, inspectable data; other editors and integrations
can consume `syntyr-api.json` directly.

## Regenerate after CSS changes

From the Syntyr source repository:

```sh
python3 scripts/export_api_metadata.py
python3 scripts/export_api_metadata.py --check
```

The Python standard-library exporter scans `src/**/*.css`, strips comments,
deduplicates discovered classes and declared custom properties, adds
documented component override variables, and writes stable JSON and snippets.
`--check` fails if the checked-in outputs differ from source. Descriptions
are curated for core APIs and source-file-derived for others.

This is an editor convenience layer, **not** a Tailwind-style CSS compiler.
A class being present in the metadata does not mean its optional stylesheet
is already loaded. Check each item's `module` in the generated catalog and
load the corresponding Syntyr CSS distribution.
