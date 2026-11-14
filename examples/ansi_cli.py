#!/usr/bin/env python3
"""Portable, stdlib-only themed CLI demo; does not change terminal settings."""
from pathlib import Path
import argparse
import json
import os
import sys

PALETTES = Path(__file__).resolve().parents[1] / "terminal" / "palettes.json"


def _rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def styled(text, foreground, enabled, background):
    """Use a matching background to retain legibility on light terminal defaults."""
    if not enabled:
        return text
    fg = ";".join(str(value) for value in _rgb(foreground))
    bg = ";".join(str(value) for value in _rgb(background))
    return f"\x1b[38;2;{fg}m\x1b[48;2;{bg}m{text}\x1b[0m"


def _enable_windows_vt(stream):
    """Windows consoles need successful VT activation before ANSI is emitted."""
    try:
        import ctypes
        import msvcrt
        handle = msvcrt.get_osfhandle(stream.fileno())
        kernel32 = ctypes.windll.kernel32
        # Explicit pointer-sized handles are required on 64-bit Windows.
        kernel32.GetConsoleMode.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32))
        kernel32.SetConsoleMode.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
        kernel32.GetConsoleMode.restype = ctypes.c_int
        kernel32.SetConsoleMode.restype = ctypes.c_int
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        vt_flag = 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        return bool(mode.value & vt_flag or kernel32.SetConsoleMode(handle, mode.value | vt_flag))
    except (OSError, AttributeError, ValueError, ImportError):
        return False


def should_color(stream, environ):
    if not stream.isatty() or "NO_COLOR" in environ:
        return False
    if environ.get("CLICOLOR") == "0" or environ.get("TERM", "") == "dumb":
        return False
    return _enable_windows_vt(stream) if os.name == "nt" else True


def main():
    parser = argparse.ArgumentParser(description="Preview Cyberline ANSI palettes")
    parser.add_argument("--theme", choices=("grid", "noir", "studio"), default="grid")
    parser.add_argument("--no-color", action="store_true", help="Always output plain text")
    args = parser.parse_args()
    theme = json.loads(PALETTES.read_text(encoding="utf-8"))["themes"][args.theme]
    enabled = not args.no_color and should_color(sys.stdout, os.environ)
    background = theme["background"]
    print(styled("CYBERLINE / CLI STATUS", theme["accent"], enabled, background))
    print(f"Theme: {args.theme}")
    print(f"[{styled('OK', theme['ansi'][2], enabled, background)}] 6 tasks completed")
    print(f"[{styled('WARN', theme['ansi'][3], enabled, background)}] 1 task pending")
    print("Run with --no-color for machine-readable/plain logs.")


if __name__ == "__main__":
    main()
