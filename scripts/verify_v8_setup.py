#!/usr/bin/env python3
"""Read-only EAL v8 repository preparation/approved-reference audit. Offline, stdlib only."""
from __future__ import annotations
import hashlib
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
failures = []
def check(ok: bool, label: str):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        failures.append(label)

standard = root / "docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md"
agents = root / "AGENTS.md"
brief = root / "GAME_BRIEF.md"
manifest = root / "reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md"
for f in [standard, agents, brief, manifest, root / "scripts/restore_v6.py"]:
    check(f.is_file(), f"required file {f.relative_to(root)}")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""
st = read(standard)
ag = read(agents)
br = read(brief)
ma = read(manifest)

check("**Version:** 2.1" in st, "canonical standard is v2.1")
check("### Tool-directed production governance" in st, "mandatory tool governance is present")
check("scripts/restore_v6.py" in ag, "Codex instructions require reference restoration")
check("docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md" in ag, "Codex instructions point to the canonical standard")
check("Living Environments v6" in br and "Sound Editions are the minimum quality floor" not in br,
      "game brief uses current v6 baseline, not obsolete Sound Edition floor")

items = [
("The_Town_That_Rebuilds_Itself_Living_Environments_v6.html",
 "e201a4e4b3ac0d734ab9863f96249ffe9a54273a22a93c372d76b87176c6fee1"),
("Do_Not_Answer_Your_Own_Voice_Living_Environments_v6.html",
 "f7ece90a49b5e6c87c5cd4797602148b0439e8a84ba82208bcbdc9097f4a48af"),
]
for name, sha in items:
    p = root / "reference" / name
    check(name in ma and sha in ma, f"approved reference manifest matches {name}")
    if p.exists():
        check(hashlib.sha256(p.read_bytes()).hexdigest() == sha, f"exact SHA-256 for {name}")
    else:
        check(False, f"missing restored reference {name}; run python3 scripts/restore_v6.py")
for p in [
 root / "games/_v8_trial/README.md",
 root / "games/_v8_trial/ACCEPTANCE.md",
 root / "games/_v8_trial/TOOL_SELECTION_RECORD.md",
 root / "shared/README.md",
 root / "releases/README.md",
]:
    check(p.is_file(), f"trial scaffolding {p.relative_to(root)}")
if failures:
    print(f"\nAUDIT FAILED: {len(failures)} requirement(s) not met.")
    sys.exit(1)
print("\nAUDIT PASSED: reference sources, instructions and trial workspace ready.")
