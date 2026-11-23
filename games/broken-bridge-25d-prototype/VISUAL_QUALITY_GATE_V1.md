# VISUAL QUALITY GATE V1 — 2.5D Tutoring Adventures
**Status:** proposed reusable standard, added to The Broken Bridge experimental branch following a teacher review of the v0.1.0 draft (2026-11-23). Not a replacement for the current tutoring release gate or approved v6/Zig references. Do not merge into main/rewrite approved games without review.

## Why this gate exists
A technically functional prototype can still be visually below the agreed standard. The Broken Bridge v0.1.0 packaged HTML was inspected: its `illustratedWorld()`, `fir()`, and `figure()` functions draw nearly all scenery and figures with Canvas primitives; no authored environment images or character sprite assets were identified in the student HTML. Layering and environmental animation exist, but the screenshot has repetitive polygonal vegetation, basic human figures, weak perspective, barely legible bridge damage, floating landmark labels, and insufficient cinematic storytelling.

**A runnable game is not an art-approved game.** Automated tests and bundle integrity cannot substitute for visual review.

## Visual promise
Use **REGOLITH** for mission-world believability and grounded environmental response; **Paper Town** for authored, coherent character/world styling and the pleasure of inhabiting a place; **LAAS/Abyssal Garden** as atmosphere/motion inspiration only. Do not blindly combine their incompatible engines, copy their assets, or demand WebGPU for iPhone.

Target: cinematic, polished, authored **2.5D** with coherent perspective, convincing lighting, textured materials, rich but readable composition, consistent figures/props, multilayer depth and subtle localized movement. The goal is not photorealism at the cost of mobile performance. Tiny repetitive polygons, gradient-only scenery, icon people, or static quiz wallpaper are **temporary engineering placeholders**, not shippable visual assets.

## Mandatory staged art workflow
**Gate 0 — Reference and source audit (BEFORE art changes):**
- Restore/verify/inspect exact approved v6 benchmarks and Zig archive; inspect the actual source and teaching materials relevant to the lesson.
- Preserve present gameplay and original branch; make a revertible `v0.1.0` archive and source hash. Record the provenance of the uploaded teacher screenshot and exact HTML artifact.
- Record a visual comparison against REGOLITH, Paper Town and our approved references; establish one cohesive style direction rather than combining incompatible art.

**Gate 1 — Authored visual direction (BEFORE rebuilding the world):**
- Produce an art-direction sheet with color palette, time of day, camera/perspective, environmental materials, character proportions, lighting, shot list, and visual storytelling.
- Make at least ONE **actual proposed in-game establishing scene**, not a text prompt or stock/reference screenshot; include a correctly scaled consistent ranger/player sprite example and a matching inspected prop. Verify that the art is original and can be distributed.
- Build a before/after **bridge** visual plan with exactly matching camera, bank geometry, weather, shadows and asset placements. The damaged crossing must be immediately understandable without text.
- Show one screenshot or rendered art composite at desktop view and an iPhone-size viewport **internally** before extending production; compare to the agreed external reference visuals. If the output looks like the existing v0.1.0, reject and revise the artwork. Do not fill missing art with basic shapes and claim full art approval.
- If high-quality art generation/consistent sprite production is inaccessible, mark **ART PRODUCTION BLOCKED**. Don't silently downgrade to vector drawings; request needed asset/tool access instead. Obtain cost approval before paid generations.

**Gate 2 — Real interactive 2.5D integration:**
- Separate background / midground / character-actor / foreground-occlusion / particles & atmosphere layers, with appropriate parallax, object occlusion and collision.
- Scene-specific subtle motion: rippling river, swaying near vegetation, lantern light, wind or rain where narratively justified; no generic global zoom/pan.
- Character sprites with consistent appearance, idle/walk/listen/speaking gestures, proper scale and shadow contact.
- Inspectable in-world props and distinct zoomed closeups. Interactive hotspots anchored to actual objects. UI emphasizes objectives without concealing the location; contextual prompts must be accessible and tappable.
- State changes must be visually dramatic and physically understandable: before/after bridge genuinely different, alternative ford visibly marked; NPC traverses the chosen route. Avoid substitute text telling the player something changed while art remains effectively unchanged.
- Keep rendering efficient: mobile-friendly asset formats, resolution variants, memory budgeting, motion toggle, safe-area sizing, and no required WebGPU/network.

**Gate 3 — Visible acceptance evidence (BEFORE teacher preview):**
Save screenshots from the *running* build (not image mocks): (1) opening at desktop, (2) opening at phone portrait and landscape, (3) NPC dialog, (4) inspectable clue close-up, (5) broken bridge before, (6) repaired bridge after, (7) ford alternative after, (8) reduced-motion / compact UI. Include side-by-side comparisons with actual prior build.
Review and document each dimension as PASS, FAIL or NOT TESTED:
1. Authored detail & material quality — no placeholder vector scenery or generic repeated assets.
2. Art direction — consistent palette, perspective, character scale, recognizable world and props.
3. Depth and cinematography — foreground occlusion, hierarchy, lighting, atmospheric layering.
4. Legibility and story clarity — storm damage visible, physical solutions comprehensible, objects discoverable, interface not blocking essential imagery.
5. Environmental animation/state response — localized meaningful motion and **substantial** persistent before/after changes.
6. Mobile composition — no cut-off controls, readable captions/Chinese, 44px touch targets, responsive art and acceptable measured performance.
7. Runtime, accessibility & offline — actual playable screenshot evidence, full correct/negative routes, saves/exports, audio manifest and cold offline load.
**Any FAIL in the visual criteria blocks calling the build “polished”, “v8-quality”, “reference-level” or “ready for creative approval.”** A subjective human art review remains required: numerical screenshot tests alone cannot assert quality.

## Targeted revision strategy for The Broken Bridge
- Preserve the existing `v0.1.0` quest/state machine, valid language paths, UI code and save/export behavior unless a verified defect is found.
- Replace or augment the `illustratedWorld()` scenery textures, geometry art and `figure()` human drawing with original authored scenery layers and coherent NPC sprites.
- Fix bridge evidence at the artwork and gameplay coordinate level so the opening damage visually reads as an unsafe gap, while keeping both solution routes and persistence.
- Retire redundant full-size floating labels where in-world affordances and tap-hover prompts suffice.
- First implement one highly polished, tested ranger-clearing scene. **Only after it passes this gate**, use the same production pipeline for additional scenes or future tutoring games.

## Evidence and authorizations
- Track source commit, source art prompts and originals, edits, asset hashes/rights, exact build checksum, actual screenshots, test device/browser, iPhone/Safari/WeChat status, and audio/voice evidence.
- Never copy assets from REGOLITH/Paper Town/LAAS/Abyssal Garden without license-specific clearance. Paper Town visual assets may be noncommercial.
- Do not conflate a ChatGPT-generated **concept image** with a game scene implemented and verified on the actual target device.
- Until all applicable tutoring `RELEASE_GATE.md` gates pass, label appropriately DESIGN/WORKING, TEACHER PREVIEW or CLASSROOM PILOT, never HOME RELEASE.
