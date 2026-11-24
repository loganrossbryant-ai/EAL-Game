#!/usr/bin/env python3
"""Read-only structural safety check. Not a quality verdict."""
from pathlib import Path
import csv
import json
import sys

root = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "GAME_BRIEF.md",
    "docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md",
    "reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md",
    "scripts/restore_v6.py",
    "studio/README.md", "studio/STUDIO_REGISTRY.md", "studio/START_NEW_GAME.md",
    "studio/checkpoints/BROKEN_BRIDGE_CONTINUE.md",
    "studio/standards/PRODUCTION_CONTRACT.md",
    "studio/standards/VISUAL_AND_INTERACTION_GATE.md",
    "studio/templates/NEW_GAME_BRIEF.md",
    "studio/templates/CURRICULUM_ACTION_MATRIX.csv",
    "studio/templates/ART_ASSET_MANIFEST.csv",
    "studio/templates/AUDIO_LINE_MANIFEST.csv",
    "studio/templates/QA_REPORT.md",
    "studio/templates/CONTENT_PACK.example.json",
    "studio/architecture/ENGINE_EXTRACTION.md",
    "tutoring-games/AGENTS.md",
    "tutoring-games/standards/RELEASE_GATE.md",
]
failures = []
for file in required:
    path = root / file
    if not path.is_file() or path.stat().st_size == 0:
        failures.append(f"Missing/empty required file: {file}")
for filename, columns in {
    "studio/templates/CURRICULUM_ACTION_MATRIX.csv": ["target_id", "source_id", "english_target", "player_action"],
    "studio/templates/ART_ASSET_MANIFEST.csv": ["asset_id", "source_pixels", "sha256", "owner_license"],
    "studio/templates/AUDIO_LINE_MANIFEST.csv": ["line_id", "english_transcript", "audio_path", "pronunciation_review"],
}.items():
    try:
        with (root / filename).open(encoding="utf-8-sig", newline="") as f:
            cols = next(csv.reader(f))
        if not set(columns).issubset(cols):
            failures.append(f"Missing CSV fields: {filename}")
    except Exception as ex:
        failures.append(f"Cannot parse {filename}: {ex}")
try:
    content=json.loads((root/"studio/templates/CONTENT_PACK.example.json").read_text(encoding="utf-8"))
    if content.get("status") != "ILLUSTRATIVE_NOT_RUNTIME":
        failures.append("Content example must remain labeled illustrative, not approved runtime")
except Exception as ex:
    failures.append(f"Cannot parse content example: {ex}")

for x in failures:
    print("FAIL", x)
if failures:
    sys.exit(1)
print(f"PASS structural-only: {len(required)} required files present; sample manifest schemas parsable")
print("NOT TESTED: approved binary hashes, running gameplay, art quality, devices, narration, classroom readiness")
