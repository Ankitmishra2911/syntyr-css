"""Create a deterministic, minimal Cyberline CSS release without third-party tools.

Only allowlisted public MIT artifacts are packaged; business drafts and development
files are deliberately omitted. This script refuses to bundle stale compiled CSS.
"""
import argparse
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "LICENSE",
    "README.md",
    "docs/distribution.md",
    "dist/cyberline.all.css",
    "dist/cyberline.core.css",
    "dist/cyberline.css",
    "dist/cyberline.effects.css",
    "dist/cyberline.semantic.css",
)


def package(output: Path) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or "/" in version or "\\" in version:
        raise ValueError("Invalid VERSION")
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"],
                   cwd=ROOT, check=True, capture_output=True, text=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, mode="w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in FILES:
            source = ROOT / relative
            contents = source.read_bytes()
            info = ZipInfo(f"cyberline-css-{version}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o100644 << 16)
            archive.writestr(info, contents, compress_type=ZIP_DEFLATED, compresslevel=9)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?", help="output ZIP path")
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    target = args.output or ROOT / "release" / f"cyberline-css-{version}.zip"
    package(target)
    print(f"Packaged {len(FILES)} files in {target}")
