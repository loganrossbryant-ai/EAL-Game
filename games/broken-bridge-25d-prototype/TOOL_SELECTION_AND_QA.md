# Tool Selection and Verification Record + prototype quality gate
**Status:** Planning record; PASS is prohibited without an observable run. Created on separate branch. No paid tools executed.

| Capability | Initial choice and rationale | Acceptance proof | Observed | Fallback / blocker |
|---|---|---|---|---|
| Canonical references | Local checkout + `scripts/restore_v6.py` and `verify_v8_setup.py`; Zig reference and tutoring rules from separate setup branch | Both v6 SHA-256 match; Zig archive validated; visual benchmark reviewed | NOT TESTED in this planning environment; scripts/manifests/instructions read | Must restore and inspect locally before gameplay changes; do not claim review of exact HTML |
| Engine + 2.5D controls | Phaser 3 + DOM; `codex/signal-playable-demo` is engineering reference only | keyboard, mouse and actual touch movement, pause/modal behavior, 390px/landscape layouts, 30fps target | NOT TESTED | Implement lightweight Canvas fallback or reduce effects after device measurements |
| Visuals | original layered environment + localized Phaser/CSS animation; emulate LAAS/Abyssal Garden atmosphere without adopting WebGPU | consistent before/after art, objects actually match evidence, screenshots at mobile/desktop, reduced-motion | NOT STARTED | reduce layers/texture size, not replace interactive scene with flat quiz image |
| NPC and narrative | deterministic state-machine dialogues, authored English/Chinese strings; no live API | complete choices, correct/incorrect path, guarded states, NPC reacts later, no softlock | NOT STARTED | full transcript and on-screen guidance |
| Language | two data profiles with shared world; `LANGUAGE_ACTION_MATRIX.csv` illustrative | each mandatory target modelled early and reused, meaning-changing actions, teacher export | PARTIAL: drafted illustrative map only; NOT textbook-aligned | Align to actual private lesson materials before teaching |
| Narration | captions now; locally packaged verified voice performances before independent release | 100% required spoken lines exact files, routing/playback, offline, no robotic substitutes | NOT STARTED, zero voice generated | CLASSROOM PILOT at most if independence requires audio |
| Offline delivery | Vite build with locally bundled JS/images/audio; evaluate single-file and PWA separately | no external requests; fresh install and cold offline restarts desktop and iPhone Safari/Home Screen | NOT TESTED | bundled offline ZIP for classroom use; never assume file:// equals iOS install |
| QA | Playwright plus manual screenshot inspections; real target-device testing | all routes, retries, restore/reset, export, mobile layout, Chinese font, audio/mute, reduced-motion, offline | NOT TESTED | teacher preview until tests pass |
| License/source lineage | MIT code allowed with preserved license notices; Godot Paper Town only design reference pending per-asset audit | provenance/asset manifest, per-source license notices | PARTIAL: repository licenses reviewed; no code copied | use original graphics and clean implementation |

## Required real test matrix
- **Desktop:** Chrome and one other mainstream browser: keyboard, mouse, all state routes, save/reset, report export, wrong answer handling, backtrack, muted/reduced motion.
- **Simulated mobile:** 390x844 portrait and 844x390 landscape, touch-mode, safe areas, overlay scroll, every clickable control and dialogue button in view. Cross-check screenshots.
- **Physical iPhone:** Safari direct HTTPS, Home Screen installed PWA if used, WeChat browser -> external Safari, language rendering, tap/drag, audio unlock, save/resume, offline cold restart; record OS/device/browser. **Not yet available/tested.**
- **Offline:** cold network denial after install or ZIP extraction, no remote scripts/fonts/API calls; verify actual artifact after reload and save data integrity.
- **Cross-mode:** elementary and middle modes, each valid route, each failure/retry, language persistence, report differences; graded oral pronunciation is explicitly OUT.
- **Audio:** every required line mapped to source asset and transcript before asserting student independence.

## Release status definitions
DESIGN / WORKING = planning or incomplete engine. TEACHER PREVIEW = viewable without a complete path guarantee. CLASSROOM PILOT = verified browser path but missing device/voice gates with tutor present. HOME RELEASE = every tutoring release gate including voice and actual target device passed.
Do not publish an HTTPS URL or claim the game is playable until deployment and opening are actually tested. Public deployment requires explicit approval.

## Audit anchors
- Main approved technical baseline: `AGENTS.md`, `GAME_BRIEF.md`, `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`, `reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`.
- Separate tutoring standards: branch `codex/tutoring-game-setup`, `tutoring-games/standards/RELEASE_GATE.md` and `QUALITY_STANDARD_V1.md`.
- Modular prototype candidate: `codex/signal-playable-demo`, `DEVELOPMENT.md`, `src/`, `tests/`, `demo/`.
- Source branch from `main` commit `0790cb3be5c0e6340257594516e44e4913bc7777`; new branch commits logged in Github.
