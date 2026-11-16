#!/usr/bin/env python3
"""Copy the canonical CSS artifact to Nulang's static directory.

Run from any directory; no package manager or runtime dependency is needed.
"""
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "dist" / "syntyr.core.css"


def main() -> None:
    if len(sys.argv) > 2:
        raise SystemExit("usage: python3 prepare.py [output_directory]")
    destination = Path(sys.argv[1]) if len(sys.argv) == 2 else HERE / "static"
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / SOURCE.name
    shutil.copyfile(SOURCE, target)
    print(f"Copied {SOURCE.name} to {target}")


if __name__ == "__main__":
    main()
