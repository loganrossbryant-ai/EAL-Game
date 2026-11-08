# AGENTS.md — EAL Immersive Game Development (current)

> Applies to the whole repository unless a child directory provides more specific guidance. Last updated 2026-11-08. Replaces outdated unit-specific assumptions in previous versions of this file.

## Mission and verified references
Build **original, cinematic, accessible, fully offline educational adventures** in which authentic English use changes the fictional world. Approved baseline: *The Town That Rebuilds Itself — Sound Edition* and *Do Not Answer Your Own Voice — Sound Edition*. Earlier archived *Two Towns* games are useful gameplay references, but their source distribution is missing scene artwork and must not be treated as a fully restored visual release. *Far Horizon* is an artistic ambition reference ONLY; its assets must not be reused in unrelated games.

Read, in order:
1. This file and `GAME_BRIEF.md` (current universal development contract).
2. `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md` (detailed production and QA standard).
3. The actual approved game files, textbook pages, and class profile if available **in the task**. Files stored in a separate ChatGPT Project are NOT automatically present in this Git repository; note missing sources and do not imply otherwise.
4. Existing functional game code, tests, and previous working commits before replacing anything. Preserve proven systems.

## Source-of-truth, education, and privacy
- Map **confirmed textbook** vocabulary, grammar, reading, and writing goals into a `objective → language → player action → evidence → teacher verification` matrix *before scripting a full game*. Distinguish textbook-required words from task/narrative language and enrichment. Never label guessed vocabulary "from the textbook".
- Adapt independence and scaffolds to the **specified students**, not their grade alone. Simplified Chinese glosses are selective and correct. Meaningful output is required; multiple-choice checks alone are insufficient.
- Spoken/written communication must accomplish an in-world objective (repair ticket, urgent broadcast, interview request, website redesign) and have a visible consequence. Explicitly avoid detachable worksheets and unsupported AI-like automated evaluation claims.
- Keep identifiable student work and restricted textbook scans OUT of this public repository. Default to local-only save; do not collect real names or contact data. A writing or reasoning quality grade must not be inferred from keyword counts.

## Art and worldbuilding
- Cinematic, photorealistic story-specific scenery with coherent architecture, geography, props, character continuity and narrative-causal connections.
- Game backgrounds must be environment-only art: **never** a generated promo mockup with fake HUD/buttons or baked-in instructional text. Real readable props and UI belong in actual HTML/game interfaces; facts/times/measurements must match the story data.
- Make places change physically after decisions. Use layered/parallax foreground/midground/backdrop, relevant weather, machinery, silhouettes, lighting and environmental audio where feasible. Provide reduced-motion settings.
- Smaller recurring casts with distinct motives, relationships, location changes and conditional dialogue outperform many one-off exposition characters.
- Original genre-appropriate soundtracks and effects; independently adjustable, start muted. No required information audio-only. Do NOT assume ElevenLabs is authorized for future media.

## Gameplay, mechanics, and narrative
- Each title requires a **distinct signature mechanic** motivated by its world and at least several different player verbs (e.g. calibrate, connect, compare, repair, reconstruct, negotiate). A quiz with a new skin is not a new mechanic.
- Strong hook → investigation → evidence reversal → costly choice → visibly different later playable states → resolved central mystery. Map branch dependencies and persist state. Mistakes lead to repairable consequences, not dead ends.
- Physical exploration should be truly interactive: direct player control or meaningful click-to-move, real hotspots/collision if using a spatial engine, in-world interfaces that work, clear pathways and readable evidence.
- Avoid arbitrary fast countdowns that penalize learners for reading English; use escalating tension and hint ladders instead.

## Architecture (choose deliberately)
- **Existing Phaser + React + Vite + Playwright demo:** inspect `codex/signal-playable-demo`; reuse infrastructure selectively. It is a technical proof, not an approved final narrative or verified textbook mapping.
- Phaser and HTML can combine a genuine game world with readable authentic documents. A simpler self-contained HTML/CSS/JS game is valid when it provides better quality and reliability for a smaller task. Do not migrate good working releases purely for technology's sake.
- Offline means ALL essential textures/audio/scripts/fonts ship locally or embedded. No remote CDN/API/login/VPN for gameplay. Verify actual packaged release with network disabled and from its delivered path; a dev-server success is insufficient.
- Save/resume, multi-path persistence, student writing/report export, keyboard/touch/accessibility, reduced motion, separate music/effects settings and a teacher key where appropriate.

## Development stages (do not repeatedly ask for approval)
1. **Audit:** read real sources, existing code, class constraints, user decisions and approved games; log any source gap.
2. **Design:** create internal act graph, scene geography, NPC goals, branch-state table, prop shot list, language-action map, puzzle specifications and outcome conditions.
3. **Vertical slice:** implement one representative playable segment containing original scene art, spatial interaction, a real puzzle, language-caused action, visible later consequence, save/export; visually inspect and test before scaling.
4. **Produce:** complete all scenes/character/evidence art, narrative, sound and mechanics; no duplicated generic backgrounds.
5. **QA:** systematically launch the *actual build*; check each scene, artifact, NPC, navigation, puzzle, hint, decision, alternate ending, saving, export, sound, responsive sizing, offline independence and JS errors. Run automated tests AND inspect screenshots. Distinguish simulated progression from human-style playthrough.
6. **Release:** provide the exact tested self-contained game/package, concise teacher instructions, version, changelog, and honest QA limitations. Never label an unfinished vertical slice "complete game".

## Repository discipline
- Create a task-specific branch for new games; do not overwrite `far-horizon/`, `eal-adventure/`, approved files or working branches.
- Keep generated assets versioned and local. Avoid giant base64 source blobs in normal tracked source when individual assets and a build pipeline are available; distribution bundles may embed assets.
- For a request to test creative capacity without a new textbook unit, clearly mark it **creative/technical demonstration, not curriculum-certified**; showcase systems without inventing unit requirements.
- When something can't be tested or a connector isn't available, report the exact limitation rather than inventing a completion claim.