# Mandatory visual + embodied-interaction acceptance gate (v1)

Applicable to every new EAL/Tutoring adventure. **A running game is not visually approved merely because its build/tests pass.** REGOLITH = purposeful exploration; Paper Town = authored art/NPCs; LAAS/Abyssal Garden = layered atmosphere, not WebGPU requirement. Never copy external game assets/licenses blindly. Broken Bridge v0.1 primitive-vector art and v0.4 soft/scarcely animated plate are *reject examples* for this target.

## PREPRODUCTION — must pass before whole-world expansion
- Inspect exact previous approved executable, source if available, test screenshots and source hashes; don't infer from a title or summary.
- Lock authored camera/perspective, palette, lighting, materials, character proportions and animation, scene-specific visual storytelling, UI/controls, environmental before/after states and prop zooms.
- Use ChatGPT image generation by default for original **background, midground, foreground, characters, interactable props and matching state variants**; transfer files explicitly to Codex and verify source dimensions, alpha and hash/license manifest. No single blurred image falsely marketed as multilayer art.
- Implement ONE complete convincing game-ready location and at least one embodied interaction + NPC; only extend after screenshot review and approval.

## Acceptance criteria — all require actual running evidence
1. **Resolution & material:** author/source scale support target desktop viewing; critical scenery, character sprites, prop closeups look sharp at real zoom. Compare crops at 100%, inspect filtering/DPR/compression; don't merely upscale a soft image. Budget mobile textures.
2. **Depth & camera:** correct parallax, independent layers, proper foreground occlusion, shadows, coherent 2.5D perspective and camera shifts that help gameplay rather than disorient.
3. **Grounding & navigation:** walkable terrain matches rendered surfaces; shared authored polygons/navmesh for player, pointer, NPC routes and save positions. Every boundary/edge verified. No “walk into sky/water/forest painting.”
4. **Characters/NPC:** directional walk loops with distinct useful frames, turns, idle/gesture/hold/use/carrying states, feet and shadows grounded; consistent scale; visible NPC agency and movement.
5. **Environmental animation:** visible directional river/water response, independently swaying foliage, atmospheric movement and local light. Stationary camera captures >=3 distinct systems over 10–15s; reduced-motion equivalent, no global fake wobble.
6. **Physical world actions:** props discovered and manipulated in-world, clear wrong-state retries, bridge/ford consequences substantially affect actual art and later state. Modals support accessibility, not replace immersive primary mechanics.
7. **UI & language:** readable on phone, contextual discovery indicators instead of clutter, 44px controls; meaningful English affects decisions, appropriately scaffolded for learner, avoid regex-only claims of semantic grading.
8. **Delivery:** exact tested build offline, audio captions/replay, save/export, portrait/landscape, performance/memory, no essential external requests.

## Mandatory evidence
- Side-by-side *same framing* prior/revision screenshots at desktop 1920×1080, 1366×768 and 390×844/844×390; 100% image crops.
- Uninterrupted actual-game video showing movement/crossing/return/physical object use, and a stationary-scene video demonstrating environmental motion.
- NPC dialogue, clue closeup, bridge before/after, alternate ford before/after, reduced motion, negative route and save/resume test results.
- For every criterion: `PASS | FAIL | NOT TESTED`, test method + file, source/build SHA, human reviewer. Static assets, generated art and visual diffs are **not** gameplay acceptance.
- **If any criterion fails, do not label polished/reference-level or visually approved.** Art unavailable => ART BLOCKED. Automated checks cannot sign off subjective art quality; teacher's first creative approval is mandatory.

Avoid blanket “v8 PASS” assertions, superficial particle additions, placeholder vectors and rewrites of working logic. Follow targeted, reversible upgrades and source provenance.
