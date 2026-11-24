# EAL Game Studio — authoritative production index

**Scope:** all EAL and tutoring games. These files govern `ChatGPT ↔ Codex` handoffs after merging to the target branch. Individual projects may add requirements, but cannot waive this quality gate.

## Mandatory reading sequence
1. Repository root `AGENTS.md`; `GAME_BRIEF.md`; relevant game-specific `AGENTS.md` (e.g. `tutoring-games/AGENTS.md`).
2. Approved original reference and its exact file: `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md` (including Section 9), restored two v6 HTMLs; for tutoring, consult Zig via `codex/tutoring-game-setup` until its approved release files are centrally imported.
3. `standards/PRODUCTION_CONTRACT.md`, then `standards/VISUAL_AND_INTERACTION_GATE.md`.
4. `STUDIO_REGISTRY.md` to select the **last approved** source build, not the branch with the newest number.
5. `START_NEW_GAME.md` and `templates/` for curriculum/action mapping, asset/audio manifests, and acceptance evidence.
6. Active game's `DESIGN_BRIEF.md`, source files, existing test coverage and exact artifact hashes.

## Honest present capabilities
**Templates and governance exist; a released and reusable 2.5D engine does NOT yet exist.** The Broken Bridge v0.4 candidate still has a sky-walking defect, soft scenery at display scale, and weak environmental movement. The engine extraction plan in `architecture/ENGINE_EXTRACTION.md` is a FUTURE task, not completed code. Do not claim plug-and-play implementation until a deliberately different game passes reuse tests.

## End-to-end workflow
Private curriculum/source audit → content and game-action matrix → original ChatGPT art (transferred to actual source repo) + locally generated offline Kokoro dialogue → one physically interactive, cinematically polished vertical slice → real browser playthrough and independent visual review → mobile/audio/offline QA → teacher's creative approval → reproducible and versioned reference release → reusable engine extraction → unrelated-unit clone test.

**Do not pay for 3D generation or deploy publicly without authorization.** Use free Blockbench/Blender (if available) optionally; don't force WebGPU on iPhone. Every check must say PASS / FAIL / NOT TESTED with evidence.

For resumption: [Broken Bridge checkpoint](checkpoints/BROKEN_BRIDGE_CONTINUE.md).
