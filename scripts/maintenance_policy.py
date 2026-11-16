"""Fail closed on CSS source drift without adding a compiler or runtime dependency.

Usage: python3 scripts/maintenance_policy.py

Every source must be owned by a shipped distribution; a distribution must not
include the same module twice. Component theme forks, missing CSS variables
without fallbacks, and specificity overrides introduce long-lived maintenance
cost and are not allowed. No byte ceilings.
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
CUSTOM_PROPERTY = re.compile(r"(?<![\w-])(--syn-[a-zA-Z0-9_-]+)\s*:")
VAR_REFERENCE = re.compile(r"\bvar\(\s*(--syn-[a-zA-Z0-9_-]+)\s*([,)])")
IMPORTANT = re.compile(r"!\s*important\b", re.IGNORECASE)
BLOCK_OR_IMPORTANT = re.compile(r"[{}]|!\s*important\b", re.IGNORECASE)
REDUCED_MOTION = re.compile(r"\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)")
ALLOWED_MOTION_DECLARATION = re.compile(
    r"(?:scroll-behavior\s*:\s*auto|transition-duration\s*:\s*0s|animation-duration\s*:\s*0s)",
    re.IGNORECASE,
)


def base_important_issues(content: str) -> list[str]:
    """Allow only the existing accessibility overrides inside reduced-motion media.

    This intentionally small block walk is used only for base.css, whose
    handwritten CSS does not contain braces inside strings or declarations.
    It is not a general-purpose CSS parser or a consumer build dependency.
    """
    blocks = []
    cursor = 0
    issues = []
    for token in BLOCK_OR_IMPORTANT.finditer(content):
        if token.group() == "{":
            blocks.append(content[cursor:token.start()].strip())
            cursor = token.end()
        elif token.group() == "}":
            if blocks:
                blocks.pop()
            cursor = token.end()
        else:
            preceding = content[cursor:token.start()].rsplit(";", 1)[-1].strip()
            reduced_motion = any(
                block.startswith("@media") and REDUCED_MOTION.search(block)
                for block in blocks
            )
            if not reduced_motion or not ALLOWED_MOTION_DECLARATION.fullmatch(preceding):
                issues.append("base.css: !important outside reduced-motion accessibility allowlist")
    return issues


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
    cleaned_sources = {}
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
        cleaned_sources[name] = content
        # Theme palette variants must live in tokens, not in copied components.
        if name not in {"tokens.css", "base.css", "print.css", "viz.css"} and THEME_ATTRIBUTE.search(content):
            label = "component theme fork" if name.startswith("components/") else "theme fork"
            issues.append(f"{name}: {label}; change theme tokens instead")
        if INTEGRATION_LEAK.search(content):
            issues.append(f"{name}: integration leak; keep vendor-specific syntax, selectors and tokens in integrations/")
        if name == "base.css":
            issues.extend(base_important_issues(content))
        elif IMPORTANT.search(content):
            issues.append(f"{name}: !important outside base.css; use cascade layers")

    # A custom property can be supplied by a theme or consumer when var() has
    # a fallback. Without a fallback, a misspelled/missing default silently
    # invalidates the consuming declaration in the browser.
    declarations = {
        match.group(1) for content in cleaned_sources.values()
        for match in CUSTOM_PROPERTY.finditer(content)
    }
    for name, content in sorted(cleaned_sources.items()):
        for match in VAR_REFERENCE.finditer(content):
            token, delimiter = match.groups()
            if delimiter == ")" and token not in declarations:
                issues.append(f"{name}: unresolved CSS variable without fallback: {token}")

    return sorted(set(issues))


def main() -> int:
    issues = find_issues()
    if issues:
        for issue in issues:
            print("MAINTENANCE POLICY: " + issue)
        return 1
    print("OK: CSS sources are registered once per bundle, with no component theme forks or !important overrides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
