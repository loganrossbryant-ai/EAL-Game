# Shared production contract — all EAL game types

This is the canonical, learner-agnostic standard for school EAL and tutoring. See `../../AGENTS.md`, secondary quality standard in `../../docs/`, `VISUAL_AND_INTERACTION_GATE.md`, and scoped tutoring `../../tutoring-games/AGENTS.md` when relevant.

## Source-of-truth order
1. Latest explicit teacher direction; actual unit/student sources and latest approved lesson feedback, never guessed.
2. Exact archived APPROVED game binaries **and** editable source correspondence where available; source manifests and SHA hashes.
3. Existing gameplay implementation, tests, prior approvals, design brief and content/voice manifests.
4. Canonical visual/production/release standards; new original assets and interactions only as needed.

If files or real device evidence are missing, state that. Do not claim inherited quality merely because a README says so. No textbook scans or identifiable learner records committed to public GitHub.

## Lesson & pedagogy contract
Map required textbook words/functions/reading → lesson PPT/print/homework → game affordance and meaningful English sentence/question → actual world effect → teacher evidence, with exposure vs CORE vs STRETCH and Chinese glosses. The game MUST teach its language before requiring it and recycle it across multiple scenes. Elementary and older learners are not interchangeable. Negative trials and multiple correct interpretations must be fair.

## Art & immersion
ChatGPT image generation is default for original scenery layers, player/NPC sprite sheets, props, and before/after states. Transfer actual approved image files into Codex repository with SHA, provenance and license information. Concept imagery is not running gameplay. **Never silently downgrade** to primitive Canvas/vector placeholder forests or drawn stick-person characters. Use original layered 2.5D, foreground occlusion, meaningful camera work, scene-specific motion, and persistent world changes. See separate visual gate for exact demonstrations. Optional Blockbench/Blender, or fal/Runway only with licenses and cost approval. Do not require WebGPU.

## Audio & independent use
New games: Kokoro TTS by default, verify licensing/voice/language accuracy, write full locally bundled lines, captions and replay buttons. Existing Jesse or any approved voices: preserve exactly unless teacher approves replacing. Do not use browser TTS stand-ins or splice word clips. “I spoke” clicks are participation only. Missing required narration blocks HOME RELEASE.

## Engineering approach
Default offline-capable Phaser + accessible HTML after feasibility validation. Prefer real-world coordinate interactions, shared nav geometry, visible physical actions; no empty quiz boxes disguised as world puzzles. Versioned source/bundle/save schema, rollback artifacts, no external essential scripts/fonts/assets/APIs/CDNs. Mobile controls >=44 CSS px; correct Chinese, captions, mute, reduced-motion, backtracking and teacher export.
**No new game is a plug-and-play clone until the reusable engine has actually been released and tested on an unrelated scenario.**

## Required gates
- **A Curriculum** — language aligned and fair, source listed.
- **B Visual/world/gameplay** — exact running screenshots, coherent art/animation, valid navigation, physical interactions, NPCs, both outcomes, no softlocks.
- **C Audio/independence** — 100% required lines mapped and replayed, actual voice/licensing, English/Chinese readability.
- **D Delivery/device** — exact artifact checksum, offline cold restart, mobile simulated tests, real target iPhone/WeChat if home release.
- **E Release preservation** — untouched approved builds, links, saves, branch/version/rollback.

QA labels: DESIGN/WORKING, TEACHER PREVIEW, CLASSROOM PILOT, HOME RELEASE (only all relevant gates verified). Each acceptance row needs a real evidence path and reviewer; no generic “all PASS.” Teacher approves the first polished new engine slice and any consequential costs/public deployment.
