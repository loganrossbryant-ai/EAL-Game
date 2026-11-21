---
name: update-tutoring-game
description: Modify the language, lesson alignment or mechanics of an existing tutoring game while preserving approved visual quality, audio, functionality and independent-child scaffolding.
---

# Update an approved tutoring game

Use this workflow when a user requests language changes, word-bank updates, clue difficulty, grammar progression, or localized targeted improvements to an established game.

1. Identify learner, latest textbook/PPT/print/homework and observed outcomes. Verify exact file versions; never infer them from names alone.
2. Open `tutoring-games/AGENTS.md`, `standards/QUALITY_STANDARD_V1.md`, the current game's source/readme, and its last change log. Inspect `references/allen-lesson-4/APPROVED_REFERENCE.md` for quality comparison, not a mandate to reuse story.
3. Prepare/update a **language alignment matrix** with five stages: recognition, clue inference, supported phrases, complete preference/reason sentences, connected ideas and question exchange (when applicable). Ensure newer required language appears in early, middle and late rounds, including the finale.
4. Enumerate existing modes, images, audio, save keys, location transitions and endings. Mark preserve-by-default.
5. Edit data first if a content/data layer exists. For monolithic legacy code, make minimal surgical patches and test before any optional refactor. Do not remake working art or a complete game.
6. Validate each clue has fair evidence and all required answers are accepted; verify singular/plural, reason subjects/verbs, English/Chinese. CORE should be doable with practiced supports; STRETCH is more complex but genuinely optional.
7. QA after each changed mode, then test full required route and original regressions. Recheck screenshots, mobile view, audio routing, dashboard, progress, resets, offline packaging.
8. Document any newly required narration and only map audio assets after verified generation in the approved voice. Never mark unrecorded content voiced.
9. Produce a versioned staging build, aligned language map, test logs, change log and truthful release label. Do not publish over an approved parent link until the release skill gate passes.
