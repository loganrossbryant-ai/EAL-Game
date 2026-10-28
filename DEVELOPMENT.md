# Signal: first playable chapter

A browser adventure for secondary English learners. This milestone contains one complete investigation in the Riverside High newsroom and a small, returnable courtyard conclusion. It intentionally stops before further story expansion.

## Start

Requires Node.js 24 (Node 22.12+ also meets Vite requirements), npm, and a modern browser. No API keys, accounts, database, or external runtime services are needed.

```bash
cd /workspace/EAL-Game
npm ci --no-audit --no-fund
npm run dev -- --port 5173
```

The development server listens on all interfaces. Open the served application using your environment's browser/port access. For a production bundle, run `npm run build`; `npm run preview -- --port 4173` serves it locally. Deploy `dist/` to a static host when separately authorized.

## Play

1. Move with WASD or arrows. Click the floor to walk; click a glowing object to approach and open it. Press E or Space near an object to interact.
2. Speak with Maya and choose a question. Read the community notice, inspect the campaign on the laptop, and check Ms Chen's email. Keep all three sources as evidence.
3. Return to Maya and write a recommendation. Attach two sources, choose a direction, and explain your reasoning with a concrete fact in at least 20 words.
4. Revise if needed, then walk through the far-right courtyard door to see the consequence. You can return to the newsroom.

Escape closes an interaction. Language support levels 2–4 change scaffolding while retaining the same evidence and task. The language companion includes selective Simplified Chinese glosses. Browser text-to-speech and quiet room ambience are optional; every line is available as text.

## Validation

```bash
npm test
npm run build
# With the development server running, and Chromium installed:
npm run test:movement
npm run test:browser
```

Browser tests use `/usr/bin/chromium`; override `CHROMIUM_PATH` if needed. Override `BASE_URL` to test another served build. Screenshots are written to ignored `test-results/`. Tests run in fresh browser contexts and do not overwrite a learner's normal browser save.

The movement test checks eight keyboard directions, physical collisions, click movement, object approach, and modal pause. The story test checks all sources, dialogue, website tabs, revision feedback, draft restoration, completed chapter, courtyard return, export, glossary, and mobile overflow.

## Student work and assessment

Progress is local-only under localStorage key `signal-save-v1`: position, support preference, evidence, dialogue choice, written draft, recommendation, feedback, and submission history. There is no analytics service and no real student name is requested. Use **Field notebook → Export learning record** to download inspectable JSON for teacher review. Browser storage can be cleared by school policies or private browsing; export work that must be retained.

The checkpoint is a transparent automated **completeness** check, not a language-quality or reasoning grade. It checks collected/attached sources, a recommendation, sufficient writing, and the presence of a specific source detail. It cannot judge whether a claim is used accurately or an argument is convincing. Teachers should review the saved writing. All three editorial directions can proceed with a developed explanation and have different narrative consequences.

## Preserved work and materials

The initial checkout was behind remote main. It was fast-forwarded without discarding local work to retrieve `AGENTS.md`, `GAME_BRIEF.md`, and `MIGRATION_README.md`; those files and the original README are retained unchanged. No previous game source, artwork, comparison screenshots, textbook pages, or verified vocabulary lists were supplied.

The current narrative, glossary, and language functions are provisional thematic content for Media Influences and Helping Others, **not a verified transcription of textbook content**. Supply the original unit pages before claiming exact curriculum alignment. The newsroom and courtyard backgrounds were generated for this project; character artwork and fallback room art are drawn locally. Fictional sites use `.example` addresses and accept no payments.

## Structure

- `src/game/MediaRoom.js`: Phaser world, character, pathfinding, collisions, objects, doorway, local fallback art.
- `src/App.jsx`: game/React bridge, objective interface, interactions, local-save lifecycle.
- `src/components/Interfaces.jsx`: fictional campaign site, documents, dialogue, editorial writing, notebook, glossary.
- `src/state.js`: versioned persistence, validation, formative feedback.
- `src/content.js`: provisional source facts and language support.
- `public/assets/`: original generated newsroom and courtyard environment art.

Use the existing checkout for future tasks. This cloud task is already isolated; do not create a Git worktree unless the user explicitly requests one.
