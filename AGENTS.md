# Codex project guidance — EAL Immersive Browser Adventures

## Mission
Build, refine, and test a polished, immersive browser adventure for secondary multilingual learners. Prioritize a functional, explorable game world, high-quality and varied art, and authentic English communication embedded in gameplay.

## Always read first
- `GAME_BRIEF.md` for confirmed needs, creative direction, and curriculum constraints.
- `MIGRATION_README.md` for what is and is not transferred.
- New screenshots, game files, textbook pages and other user assets before altering existing work.

## Non-negotiables
- Do not replace exploration with detached quiz screens or generic dashboard backgrounds.
- Make the student character visibly controllable, with navigation to distinct explorable locations. Keyboard and accessible click/tap navigation are preferred.
- Every interaction must occur in the fiction of the game (NPC dialogue, documents, websites, messages, signs, devices, evidence, etc.).
- Model in-world websites on the layout and behavior of real websites without copying real sites wholesale or impersonating real brands.
- Integrate language from original unit materials; don't invent a textbook vocabulary list and present it as verified.
- Every formative checkpoint must have an observable language product, clear success condition, and feedback.
- WIDA 1–4: scaffold unfamiliar vocabulary with Simplified Chinese glosses when useful; use reading/listening/speaking/writing meaningfully, not mechanically.
- Keep a student-facing interface concise. Preserve curricular expectations and ensure the class can be completed in usable 80-minute lesson segments.
- Do not claim a feature is implemented until it runs and has been checked.
- Build one vertical slice (one navigable location + interaction + assessment + onward transition) and test visually before expanding.

## Implementation preferences (proposed, not fixed)
- Consider Phaser for 2D/2.5D exploration and React for rich in-world sites and interfaces; inspect any existing code first and preserve working components.
- Add browser startup instructions and an automated smoke test where practical.
- Store game state in a predictable and inspectable format; simple local save is sufficient for the initial prototype.
- Avoid requesting student real names or personal information. If adding analytics, use anonymous IDs and default to local-only data.

## Quality checks
- Character movement, collision, pathing, triggers, and transitions actually work.
- The game remains accessible at typical school laptop screen sizes.
- No clipped text or low-contrast UI; Simplified Chinese displays correctly.
- Student can identify what to do next from the narrative and environment.
- Every player action contributes to the mystery, helping task, or language objective.
- Explicitly report anything not visually inspected or tested.
