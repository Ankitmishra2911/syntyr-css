"""Fail closed on CSS source drift without adding a compiler or runtime dependency.

Usage: python3 scripts/maintenance_policy.py

Every source must be owned by a shipped distribution; a distribution must not
include the same module twice. Component theme forks and specificity overrides
introduce long-lived maintenance cost and are not allowed. No byte ceilings.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from .build import SOURCE, all_distributions
except ImportError:
    from build import SOURCE, all_distributions


COMMENTS = re.compile(r"/\*.*?\*/", re.DOTALL)
THEME_ATTRIBUTE = re.compile(r"\[\s*data-syn-theme\b")
# CSS core must never add a hidden network or application asset dependency.
CSS_IMPORT = re.compile(r"^\s*@import\b", re.IGNORECASE | re.MULTILINE)
CSS_URL = re.compile(
    r"\burl\s*\(\s*(?:\"([^\"\n]*)\"|'([^'\n]*)'|([^\s)]*))\s*\)",
    re.IGNORECASE,
)

# Adapter-only syntax and DOM contracts must not become core CSS requirements.
# Keep the list narrow: native HTML/ARIA states remain valid core selectors.
INTEGRATION_LEAK = re.compile(
    r"@(?:theme|apply|tailwind|plugin|config)\b"
    r"|\.syn-(?:shadcn|radix|figma)(?!\w)"
    r"|\.(?:radix-|react-aria-|shadcn-)"
    r"|--(?:tw|radix|react-aria|figma)-"
    r"|\[\s*data-(?:radix|react-aria)-"
)


def find_issues(source_root: Path = SOURCE, bundles: dict | None = None) -> list[str]:
    """Return deterministic, actionable violations of the source ownership policy."""
    registry = all_distributions() if bundles is None else bundles
    issues = []
    referenced = set()
    for bundle, sources in sorted(registry.items()):
        seen = set()
        for source in sources:
            source_path = Path(source)
            if source_path.is_absolute() or ".." in source_path.parts or source_path.suffix != ".css":
                issues.append(f"{bundle}: invalid source: {source}")
                continue
            if source in seen:
                issues.append(f"{bundle}: duplicate source: {source}")
            seen.add(source)
            referenced.add(source)
            if not (source_root / source).is_file():
                issues.append(f"{bundle}: missing source: {source}")

    for path in sorted(source_root.rglob("*.css")):
        name = path.relative_to(source_root).as_posix()
        if name not in referenced:
            issues.append(f"unregistered source: {name}")
        content = COMMENTS.sub("", path.read_text(encoding="utf-8"))
        if CSS_IMPORT.search(content):
            issues.append(f"{name}: CSS import; bundle the source at build time")
        for match in CSS_URL.finditer(content):
            asset = next((value for value in match.groups() if value is not None), "").strip()
            if not asset.lower().startswith("data:") and not asset.startswith("#"):
                issues.append(f"{name}: external CSS asset; embed or own it in the host application")
                break
        # Theme palette variants must live in tokens, not in copied components.
        if name not in {"tokens.css", "base.css", "print.css", "viz.css"} and THEME_ATTRIBUTE.search(content):
            label = "component theme fork" if name.startswith("components/") else "theme fork"
            issues.append(f"{name}: {label}; change theme tokens instead")
        if INTEGRATION_LEAK.search(content):
            issues.append(f"{name}: integration leak; keep vendor-specific syntax, selectors and tokens in integrations/")
        # base.css already contains the deliberate reduced-motion exception.
        if name != "base.css" and "!important" in content:
            issues.append(f"{name}: !important outside base.css; use cascade layers")

    return sorted(issues)


def main() -> int:
    issues = find_issues()
    if issues:
        for issue in issues:
            print("MAINTENANCE POLICY: " + issue)
        return 1
    print("OK: CSS sources are registered, theme-neutral and free of integration-specific CSS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
