# Tutoring Game Studio — versioned standards

This is a **new, additive** subtree for elementary, adult and private tutoring games within the existing EAL-Game repository. It does not replace the high-school EAL game or any approved releases.

## Read these first
- `AGENTS.md` — local Codex rules (supersedes incompatible secondary assumptions for this subtree)
- `standards/QUALITY_STANDARD_V1.md` — reusable quality baseline
- `standards/RELEASE_GATE.md` — release readiness
- `references/allen-lesson-4/APPROVED_REFERENCE.md` — real benchmark, with limitations
- `templates/GAME_DESIGN_BRIEF_TEMPLATE.md` — start a new game or major content change
- `templates/LANGUAGE_ALIGNMENT_MATRIX_TEMPLATE.csv` — map lesson language into game tasks

## Explicitly separate three things
1. **Immutable reference**: `references/allen-lesson-4/Zig_Lesson_4_FOOD_PLACES_ACTIVITIES_Installable_PWA.zip`; the HTML inside is the known good release artifact. Do not edit.
2. **Editable game source**: source for any new or existing game under `games/<game-slug>/`. Import working code deliberately; don't claim the compiled Zig HTML is modular source.
3. **Released build**: a tested release created from source and identified by a checksum, QA report and version. Use staging before public distribution.

## Verification command
From the repository root:

```bash
python tutoring-games/scripts/validate_reference.py
```

Uses the Python standard library. It checks the benchmark archive, focus-language map and asset counts. **It is not a substitute for end-to-end browser testing.**

## Existing repo compatibility
The root `AGENTS.md` and `GAME_BRIEF.md` refer to secondary classes; do not delete or rewrite them. The existing `eal-adventure/` (Godot) and its browser deployment are separate from the HTML-based Zig release and should not be silently conflated.
