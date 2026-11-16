"""Build a deterministic, relocatable Syntyr CLI archive from reviewed sources.

The extracted CLI needs Python's standard library only. It never downloads code
or changes project files without explicit --apply.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

if __package__:
    from .build_shadcn_registry import ROOT, OUTPUT, generate
else:
    from build_shadcn_registry import ROOT, OUTPUT, generate

FILES = (
    "VERSION",
    "LICENSE",
    "docs/cli.md",
    "metadata/syntyr-contract.json",
    "scripts/syntyr_cli.py",
    "scripts/syntyr_check.py",
    "scripts/registry_install.py",
    "scripts/build_shadcn_registry.py",
)


def package_cli(output: Path) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or "/" in version or chr(92) in version:
        raise ValueError("Invalid Syntyr version")
    contract = json.loads((ROOT / "metadata/syntyr-contract.json").read_text(encoding="utf-8"))
    if contract.get("source_version") != version:
        raise ValueError("Validator contract release version does not match CLI")
    generated = generate()
    actual = {
        p.relative_to(OUTPUT).as_posix(): p.read_bytes()
        for p in OUTPUT.rglob("*.json")
    }
    if actual != generated:
        raise ValueError("Registry differs from generated sources; rebuild before packaging")
    bundle = {relative: (ROOT / relative).read_bytes() for relative in FILES}
    bundle.update({f"registry/{name}": content for name, content in generated.items()})
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, content in sorted(bundle.items()):
            info = ZipInfo(f"syntyr-cli-{version}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, help="Output archive path")
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    target = args.output or ROOT / "release" / f"syntyr-cli-{version}.zip"
    package_cli(target)
    print(f"Created {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
