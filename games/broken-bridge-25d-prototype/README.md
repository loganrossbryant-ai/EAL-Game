# The Broken Bridge — 2.5D EAL Engine Prototype
**Status:** DESIGN / WORKING — planning only; NOT a playable build or release.
**Branch:** `codex/broken-bridge-25d-prototype` (forked from `main`, 2026-11-22).
**Purpose:** Test a reusable, iPhone-first 2.5D adventure engine with one coherent 10–15-minute forest scenario and two data-driven language profiles: elementary and middle school.

## Non-negotiables
- Keep all approved Zig, Third Bell, other tutoring titles, existing releases, URLs and saves untouched.
- No public deployment, paid asset generation, purchases, or mutation of an approved release without separate authorization.
- Student language in this technical prototype is **illustrative only** and must NOT be presented as verified textbook alignment.
- Do not commit real student names, private learner records, textbook screenshots, credentials, copyrighted media, or parents' materials to this public repository.
- Visual benchmark: approved Living Environments v6 + tutoring Zig reference; aim higher, toward the current v8 standard.
- External game references are engineering/design references, not source/art to copy wholesale.

## Read in this order
1. Repository-root `AGENTS.md`, `GAME_BRIEF.md`, `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`, and `reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`.
2. Run `python3 scripts/restore_v6.py` AND `python3 scripts/verify_v8_setup.py` on a local or Codex checkout. Inspect both restored approved v6 HTML files, and validate hashes **before writing gameplay code or generating assets**.
3. Tutoring-specific rules presently on `codex/tutoring-game-setup`: `tutoring-games/AGENTS.md`, `tutoring-games/standards/QUALITY_STANDARD_V1.md`, `tutoring-games/standards/RELEASE_GATE.md`, `tutoring-games/references/allen-lesson-4/APPROVED_REFERENCE.md`. This subtree is **not on main**; do not assume these files exist in the new branch without importing them deliberately.
4. Existing exploratory engineering baseline: `codex/signal-playable-demo` (Phaser 3/React/Vite, offline bundle script, Playwright checks). It is *not* an approved visual or curricular template.
5. Then read this folder's `DESIGN_BRIEF.md`, `LANGUAGE_ACTION_MATRIX.csv`, `TOOL_SELECTION_AND_QA.md`, and `CODEX_START_HERE.md`.

## Existing reference conditions established during planning
- `main` has approved v6 reference payloads and restoration script, but the final HTML reference files are not tracked directly. Their exact restoration/hash verification is still required in a real checkout.
- The separate tutoring branch has a read-only Zig PWA release artifact and standards. Its compiled HTML is not evidence of editable source parity.
- The `codex/signal-playable-demo` branch documents Phaser 3.90 + accessible web overlays, state/export, tests, and one-file packaging; no code has yet been imported.
- REGOLITH (https://github.com/winchxyz/moon-rover): reusable inspiration for embodied exploration and meaningful missions; Three.js/WebGL2, MIT code. Engine differs from Phaser.
- Paper Town (https://github.com/100-Devs-1-Game/PaperTown): use as a *design* reference for NPCs/quests and appealing scene composition. Its Godot code cannot be dropped into Phaser. Do not transplant noncommercial third-party art/audio.
- LAAS / Abyssal Garden: inspiration for foliage, layered atmosphere, environmental motion. Both are WebGPU-first and not suitable as required mobile renderers for this prototype.

## What has NOT been verified yet
The exact two restored v6 games have not been reconstructed or opened in this planning session; the Zig compiled PWA has not been executed here; device, browser, audio, offline and gameplay tests have NOT run. No engine or graphics recommendation is yet device-certified. Continue with the commands in `CODEX_START_HERE.md` before implementation.
