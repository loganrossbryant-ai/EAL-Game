# Codex kickoff — The Broken Bridge 2.5D prototype
**Working branch:** `codex/broken-bridge-25d-prototype`
**Design is approved in principle:** reusable elementary/middle engine, iPhone and browser first, forest setting. This file is a development handoff, NOT an instruction to publish or overwrite any existing game.

## Phase 0: required source gate BEFORE new gameplay/art
1. Check out this branch; verify working tree and identify source SHA.
2. Read root `AGENTS.md`, `GAME_BRIEF.md`, `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`, `reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`.
3. Run:
```bash
python3 scripts/restore_v6.py
python3 scripts/restore_v6.py --check
python3 scripts/verify_v8_setup.py
```
4. **Open/inspect** both exactly restored, hash-matched v6 HTML benchmarks; no inference from metadata alone.
5. Inspect `codex/tutoring-game-setup` branch's `tutoring-games/AGENTS.md`, `standards/RELEASE_GATE.md`, `QUALITY_STANDARD_V1.md` and Zig reference. Run its archived-reference validator only in a checkout where its source is present. Do not overwrite the ZIP. Explicitly record missing sources if inaccessible.
6. Inspect `codex/signal-playable-demo` for Phaser/HTML bridge, save/export, offline packaging, tests, and known limitations. Copy only justifiable engineering portions to a new folder and preserve license notices where applicable.
7. Read all four files in this folder. Confirm no real pupil data, textbook scans or private class documents have entered public git.
8. No gameplay code/assets until the canonical benchmark gate succeeds. If it fails, report exact blocker rather than reconstructing from descriptions.

## Phase 1: engineering spike (separate subfolder, no public deployment)
- Compare 2.5D Phaser Canvas/WebGL rendering on Safari-compatible targets; do not require WebGPU.
- Build a navigation experiment with correct world coordinate->hotspot/touch transforms, accessible DOM overlay and view-safe start button, not a static mockup.
- Measure frame rate, image memory and touch usability. Record actual test browsers and screenshot evidence; no assertion about real iPhone unless real test was done.
- Import no licensed game assets from Paper Town or REGOLITH. Original art only; track third-party code and attribution.

## Phase 2: finished vertical slice, not piecemeal screens
Implement from `DESIGN_BRIEF.md`: one connected ranger clearing/bridge/ford environment, physical prop evidence, NPC conversation with both learner modes, two finishable routes, persistent world-state changes, hint ladders, local save, teacher JSON export, reduced-motion and mute controls. The game must be fun even with text hidden. **Do not** ship generic backgrounds, oversized opaque UI, frozen scenes, or a string of multiple-choice questions.
Audio: do not use browser TTS to substitute for the approved voice. For mandatory new narration, request/verify cost authorization first; label any unvoiced build accordingly.

## Phase 3: quality gate before teacher preview
Automate both language profiles and BOTH branches, wrong evidence, revision, object manipulation, save/load/reset, export content, desktop and mobile snapshots, Chinese rendering, caption routing, reduced motion, zero external dependencies, and offline reload. Manually inspect every actual rendered screenshot. Compare to v6 and Zig references. Record PASS/FAIL/NOT TESTED with source SHA and exact downloadable artifact hash.
First substantial playable slice is presented for teacher creative approval; do not expand or deploy publicly before that checkpoint.

## Source-of-truth/guardrails
- Use this branch only; never replace approved releases or change main by default.
- No real student identifiers in public git. Prefer anonymous mode labels.
- `LANGUAGE_ACTION_MATRIX.csv` is **illustrative**; actual unit alignment remains a separate required curriculum audit using authorized private sources.
- Full offline home release needs actual iPhone/WeChat and genuine required narration testing; browser simulation alone is not enough.
- If there is a missing reference or failing test, stop the affected implementation and write a blocker; do not invent a PASS.
