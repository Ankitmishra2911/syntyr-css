"""Build reproducible modular CSS distributions using only Python's standard library.

No compiler, minifier, runtime JS, network access, or package-manager install.
"""
from pathlib import Path
import argparse
import gzip
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src'
DIST = ROOT / 'dist'
COMPONENTS = (
    'components/layout.css', 'components/typography.css',
    'components/buttons.css', 'components/forms.css',
    'components/overlays.css', 'components/data.css', 'components/patterns.css',
)

def assemble(paths):
    return '\n'.join((SOURCE / path).read_text(encoding='utf-8').strip() for path in paths) + '\n'

def distributions():
    core = ('tokens.css', 'base.css') + COMPONENTS
    return {
        'cyberline.core.css': core,
        'cyberline.semantic.css': ('semantic.css',),
        'cyberline.recipes.css': ('recipes.css',),
        'cyberline.effects.css': ('effects.css',),
        'cyberline.utilities.css': ('utilities.css',),
        # Original starter's import path remains valid; semantic mode stays opt-in.
        'cyberline.css': core + ('effects.css',),
        'cyberline.all.css': core + ('semantic.css', 'recipes.css', 'effects.css', 'utilities.css'),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='fail if committed dist is stale')
    args = parser.parse_args()
    failed = False
    for name, inputs in distributions().items():
        output = assemble(inputs).encode('utf-8')
        path = DIST / name
        zipped = len(gzip.compress(output, mtime=0))
        if args.check:
            match = path.exists() and path.read_bytes() == output
            print(f'{"OK" if match else "STALE"} {name}: {len(output)} raw / {zipped} gzip')
            failed |= not match
        else:
            DIST.mkdir(exist_ok=True)
            path.write_bytes(output)
            print(f'WROTE {name}: {len(output)} raw / {zipped} gzip')
    return int(failed)

if __name__ == '__main__':
    sys.exit(main())
