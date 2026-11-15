"""Deterministic CSS distributions and optional selective builds (Python stdlib only).

The default build remains stable and dependency-free. A custom build can select
modules explicitly or conservatively infer *whole modules* from application
sources. It never drops individual selectors or dynamically generated states.
"""
from pathlib import Path
import argparse
import gzip
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
DIST = ROOT / "dist"

COMPONENTS = (
    "components/layout.css", "components/typography.css",
    "components/buttons.css", "components/forms.css",
    "components/overlays.css", "components/data.css", "components/patterns.css",
)
MODULES = ("semantic", "recipes", "geometry", "effects", "application", "presets", "utilities")
SCAN_EXTENSIONS = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro",
                   ".js", ".ts", ".go", ".rs", ".py", ".php", ".md", ".templ",
                   ".erb", ".eex", ".heex", ".liquid", ".njk"}
IGNORED_DIRS = {".git", "node_modules", "dist", "vendor", "build", ".next", ".output"}
CLASS_RE = re.compile(r"(?<![\w-])syn-[a-z][a-z\d_-]*")
CSS_CLASS_RE = re.compile(r"\.((?:syn-)[a-z][a-z\d_-]*)")
THEME_RE = re.compile(r'data-syn-theme="([a-z-]+)"')
THEME_RULE = re.compile(r'(?m)^[ \t]+:where\(\.syn-root\[data-syn-theme="([a-z-]+)"\]')


def assemble(paths):
    return "\n".join((SOURCE / path).read_text(encoding="utf-8").strip()
                     for path in paths) + "\n"


def distributions():
    core = ("tokens.css", "base.css") + COMPONENTS
    return {
        "syntyr.core.css": core,
        "syntyr.application.css": ("application.css",),
        "syntyr.presets.css": ("presets.css",),
        "syntyr.semantic.css": ("semantic.css",),
        "syntyr.recipes.css": ("recipes.css",),
        "syntyr.effects.css": ("effects.css",),
        "syntyr.geometry.css": ("geometry.css",),
        "syntyr.utilities.css": ("utilities.css",),
        "syntyr.css": core + ("effects.css",),
        "syntyr.all.css": core + ("semantic.css", "recipes.css", "geometry.css",
                                  "effects.css", "utilities.css"),
    }


def choices(csv, allowed, flag):
    if csv is None:
        return None
    options = csv.split(",")
    invalid = set(options) - set(allowed)
    if not options or "" in options or invalid:
        raise ValueError(f"{flag}: unknown or empty values: {', '.join(sorted(invalid or {''}))}")
    return set(options)


def scan_classes(paths):
    """Conservative class/module detection; no full CSS selector purge."""
    names = set()
    for user_path in paths:
        path = Path(user_path)
        if not path.exists():
            raise ValueError(f"Scan path does not exist: {path}")
        if not (path.is_file() or path.is_dir()):
            raise ValueError(f"Scan path must be a regular file or directory: {path}")
        files = [path] if path.is_file() else (
            p for p in path.rglob("*") if p.is_file()
            and not any(part in IGNORED_DIRS for part in p.relative_to(path).parts)
            and p.suffix.lower() in SCAN_EXTENSIONS
        )
        for file in files:
            if file.stat().st_size > 5_000_000:
                raise ValueError(f"Scan file exceeds 5 MB; select smaller files: {file}")
            text = file.read_text(encoding="utf-8", errors="replace")
            names.update(CLASS_RE.findall(text))
            if 'data-syn-density' in text or 'data-syn-geometry' in text:
                names.add("syn--presets-marker")
    return names


def select_sources(components=None, modules=None, used_classes=None):
    component_names = {Path(p).stem for p in COMPONENTS}
    active_components = choices(components, component_names, "--components")
    active_modules = choices(modules, MODULES, "--modules")
    if active_components is None:
        active_components = set() if used_classes is not None else set(component_names)
    if active_modules is None:
        active_modules = set()
    if used_classes is not None:
        for path in COMPONENTS:
            classes = set(CSS_CLASS_RE.findall((SOURCE / path).read_text(encoding="utf-8"))) - {"syn-root"}
            if used_classes.intersection(classes):
                active_components.add(Path(path).stem)
        for module in MODULES:
            classes = set(CSS_CLASS_RE.findall((SOURCE / f"{module}.css").read_text(encoding="utf-8"))) - {"syn-root"}
            if used_classes.intersection(classes) or (
                module == "presets" and "syn--presets-marker" in used_classes
            ):
                active_modules.add(module)
    return ("tokens.css", "base.css") + tuple(
        p for p in COMPONENTS if Path(p).stem in active_components
    ) + tuple(f"{name}.css" for name in MODULES if name in active_modules)


def prune_themes(tokens, themes):
    """Exclude unrequested named palettes, but always retain the default grid."""
    supported = set(THEME_RE.findall(tokens))
    requested = choices(themes, supported, "--themes")
    if requested is None:
        return tokens
    requested.add("grid")  # The root without a theme attribute needs a palette.
    removed = []
    for match in THEME_RULE.finditer(tokens):
        if match.group(1) in requested:
            continue
        start = match.start()
        brace = tokens.find("{", match.end())
        end = tokens.find("}", brace) + 1
        if brace < 0 or end == 0:
            raise ValueError(f"Malformed theme rule: {match.group(1)}")
        removed.append((start, end))
    for start, end in reversed(removed):
        tokens = tokens[:start] + tokens[end:]
    return tokens


def custom_css(paths, themes=None):
    return "\n".join(
        prune_themes((SOURCE / p).read_text(encoding="utf-8").strip(), themes)
        if p == "tokens.css" else (SOURCE / p).read_text(encoding="utf-8").strip()
        for p in paths
    ) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify committed distributions")
    parser.add_argument("--components", help="comma-separated component names")
    parser.add_argument("--modules", help="comma-separated optional module names")
    parser.add_argument("--themes", help="comma-separated named palette subset (grid fallback retained)")
    parser.add_argument("--scan", action="append", metavar="PATH",
                        help="infer whole CSS modules from a source file/directory; repeatable")
    parser.add_argument("--safelist", help="comma-separated dynamic syn-* class names")
    parser.add_argument("--output", type=Path, help="write an opt-in custom CSS distribution")
    parser.add_argument("--report", type=Path, help="write deterministic JSON usage/size report")
    args = parser.parse_args()
    custom = any((args.components is not None, args.modules is not None,
                  args.themes is not None, args.scan, args.safelist, args.output))
    if args.check and custom:
        parser.error("--check is only supported for standard distributions")
    if custom and not args.output:
        parser.error("custom builds require --output")
    if not custom and args.report:
        parser.error("--report requires a custom build")

    try:
        if custom:
            if args.output.resolve() in {(DIST / name).resolve() for name in distributions()}:
                raise ValueError("Custom build cannot overwrite the canonical dist artifacts")
            used = scan_classes(args.scan) if args.scan else None
            if args.safelist:
                safe = choices(args.safelist, set(args.safelist.split(",")), "--safelist")
                if not all(re.fullmatch(r"syn-[a-z][a-z0-9_-]*", c) for c in safe):
                    raise ValueError("--safelist entries must be syn-* class names")
                used = (used or set()).union(safe)
            paths = select_sources(args.components, args.modules, used)
            css = custom_css(paths, args.themes).encode("utf-8")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(css)
            report = {
                "included_sources": list(paths),
                "selected_themes": sorted(set(THEME_RE.findall(css.decode("utf-8")))),
                "raw_bytes": len(css),
                "gzip_bytes": len(gzip.compress(css, mtime=0)),
            }
            if args.report:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"WROTE {args.output}: {report['raw_bytes']} raw / {report['gzip_bytes']} gzip")
            return 0
        failed = False
        for name, inputs in distributions().items():
            output = assemble(inputs).encode("utf-8")
            path = DIST / name
            zipped = len(gzip.compress(output, mtime=0))
            if args.check:
                match = path.exists() and path.read_bytes() == output
                print(f"{'OK' if match else 'STALE'} {name}: {len(output)} raw / {zipped} gzip")
                failed |= not match
            else:
                DIST.mkdir(exist_ok=True)
                path.write_bytes(output)
                print(f"WROTE {name}: {len(output)} raw / {zipped} gzip")
        return int(failed)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    sys.exit(main())
