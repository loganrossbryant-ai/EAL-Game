# Planned reusable EAL Adventure Engine — NOT YET BUILT

**Status:** architecture plan, not a functioning engine. Gold-standard Broken Bridge v0.5+ first needs teacher approval and verified source/build parity.

## Extract only after proof
- Core: scene graph/world state/conditional transitions; pathfinding via authored navigation polygons; camera & pointer transforms.
- Presentation: high-resolution layered 2.5D scenes, occlusion, environmental motion controllers, character directional sprite animation and physical prop components.
- Interaction: inspect/carry/rotate/place/connect, NPC conversation, clues, fair retry/hints and consistent input/touch accessibility.
- Language: learner-mode content data, grade-appropriate construction, evidence-based claim structure, transcript/teacher-review audit (not pretend auto semantic accuracy).
- Voice: Kokoro offline recording/bundle pipeline; existing approved voice adapters with no revoicing; captions/replay/mute; manifested line coverage.
- Persistence/release: schema migration & local save, teacher JSON export, offline bundle, no CDN, real browser/device QA.
- Art pipeline: prompt style bible, multi-layer ChatGPT image outputs, before/after geometry, alpha & motion frames; asset hashes and rights.
- Testing: scenario-agnostic behavioral tests, screenshot/video acceptance matrix, performance, cold offline, negative paths, baseline regressions.

## Proposed eventual source layout (DO NOT claim exists yet)
`engine/src/{world,navigation,actors,interactions,dialogue,language,audio,save,teacher}`, `engine/tests/`;
`games/<new-title>/{content,scenes,assets,audio,tests,qa}`;
`studio/standards/`, `studio/templates/`, `releases/<approved-title>/<version>/` (published only when authorized).

## Reusability verification
Create a deliberately DIFFERENT new game using a different story/scene/evidence/language map, importing the same engine without copying The Broken Bridge-specific art or puzzles. Prove no engine-core regressions, all major interactions and audio, mobile/offline, and preserve original baseline. Only then publish a versioned gold-standard engine release.
