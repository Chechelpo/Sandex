#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sandex.handlers.zipHandler import ZipHandler
from sandex.handlers.tarHandler import TarHandler
from sandex.extractor import File_dirs
from sandex.orchestrator import run

VERSION = "0.1.0"

def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # First pass: only parse --version
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--version", action="store_true")
    known, remaining = pre.parse_known_args(argv)

    if known.version:
        print(f"sandex {VERSION}")
        return 0

    # Full parser
    ap = argparse.ArgumentParser(prog="sandex")
    ap.add_argument("archive", type=Path, help = "Path of file to extract ")
    ap.add_argument("--out", type=Path, help="Output directory (default: archive's directory)")
    ap.add_argument("--name", type=str, help="Name of the extracted folder. (default: archive's name without suffix)")
    args = ap.parse_args(remaining)

    #Create file config
    archive = args.archive.resolve()
    out_base = args.out.resolve() if args.out else archive.parent
    out_name = args.name if args.name else None

    file_config = File_dirs(archive, out_name, out_base)


    #Create resource configs

    try:
        final_dir = run(file_config)
        print(final_dir)
        return 0
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 1



if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
