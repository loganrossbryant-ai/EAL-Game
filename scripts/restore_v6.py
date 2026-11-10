#!/usr/bin/env python3
"""Restore exact immutable approved v6 HTML games from Git-stored UTF-8 source parts.

Run: python3 scripts/restore_v6.py
Verify: python3 scripts/restore_v6.py --check

No third-party packages or network access are needed.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference"
MANIFEST = {
    "town": (
        "The_Town_That_Rebuilds_Itself_Living_Environments_v6.html",
        "e201a4e4b3ac0d734ab9863f96249ffe9a54273a22a93c372d76b87176c6fee1",
        10,
    ),
    "voice": (
        "Do_Not_Answer_Your_Own_Voice_Living_Environments_v6.html",
        "f7ece90a49b5e6c87c5cd4797602148b0439e8a84ba82208bcbdc9097f4a48af",
        9,
    ),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def restore(key: str, check_only: bool) -> bool:
    name, expected, count = MANIFEST[key]
    target = REF / name

    if target.exists():
        current = digest(target)
        if current != expected:
            print(f"ERROR {key}: existing approved file has a DIFFERENT hash; refusing to overwrite {target}")
            return False
        print(f"PASS {key}: existing reference matches {expected}")
        return True

    if check_only:
        print(f"MISSING {key}: run python3 scripts/restore_v6.py to restore {target}")
        return False

    parts = sorted((REF / "_v6_payload" / key).glob("part_*.txt"))
    if len(parts) != count:
        print(f"ERROR {key}: expected {count} parts, found {len(parts)}")
        return False
    if [p.name for p in parts] != [f"part_{i:03d}.txt" for i in range(count)]:
        print(f"ERROR {key}: payload part numbering is incomplete")
        return False

    temp = target.with_suffix(".html.partial")
    try:
        with temp.open("wb") as out:
            for part in parts:
                with part.open("rb") as source:
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        out.write(block)
        actual = digest(temp)
        if actual != expected:
            print(f"ERROR {key}: reconstructed SHA-256 mismatch; expected {expected}, got {actual}")
            return False
        temp.replace(target)
        print(f"PASS {key}: restored {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)")
        return True
    finally:
        if temp.exists():
            temp.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing files without creating them")
    args = parser.parse_args()
    success = all(restore(key, args.check) for key in MANIFEST)
    sys.exit(0 if success else 1)
