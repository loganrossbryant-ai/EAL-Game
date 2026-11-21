# Tutoring games — scoped Codex instructions

This AGENTS.md applies to games maintained under `tutoring-games/`. It supplements the repository root AGENTS.md, which was originally oriented toward secondary-school EAL. **For tutoring games use the learner profile and game brief in this subtree, not the root's assumed Grade 9–12 level or 80-minute periods.** Follow explicit user directions above standing templates.

## Ground truth and preservation
- Treat `references/allen-lesson-4/` as a **read-only quality benchmark**, not a template to blindly duplicate. The reference is a *release artifact*; it is not proof that a matching modular source build currently exists.
- Check the actual editable game source and last approved release before making edits; preserve old releases and unrelated files.
- Keep existing artwork, audio, navigation and game mechanics unchanged for a language-only update unless a defect is proven and a targeted correction is necessary.
- Never write directly to an approved release or replace a public URL before passing the release gate. Use a branch, staging build and change log.

## Language and learning
- Source target vocabulary and structures from verified latest lesson resources; use a cross-resource alignment matrix.
- Distinguish exposure, recognition, guided production, independently assessable CORE, and optional STRETCH. Choose appropriate difficulty for *this* learner.
- Recur language throughout the game; require meaningful contextual inference, asking questions, preferences, reasons, and increasingly connected ideas when those are lesson targets.
- Keep answers fair: every required task has evidence, a valid accepted answer and non-punitive feedback; impossible distractors, ambiguous questions and unreachable text fail QA.
- Chinese support is strategic and may differ by game; follow the approved brief. Navigation help and translation of graded targets are not the same thing.
- A learner pressing an oral-practice button reports participation only; never record an accurate pronunciation score without an implemented and tested assessment.

## Audio, visual and platform
- Existing approved recordings and images are immutable unless a targeted change is approved. New mandatory narrated lines require exact, verified recordings in the approved voice; missing audio is a release blocker for independent home use.
- Preserve a coherent visual world, readable child-sized controls, high-quality full-color imagery, useful animations, clear feedback and an achievable end goal.
- Test actual button routes, puzzles, progression, wrong-answer retries, save/reset, mobile viewports and the ending. Test service worker cache namespacing and cold offline restart. Test real iPhone/Safari/WeChat separately before claiming it works.

## Required evidence
- When building/updating: use `.agents/skills/update-tutoring-game/SKILL.md` as applicable; for releases use `.agents/skills/release-tutoring-game/SKILL.md`.
- Run `python tutoring-games/scripts/validate_reference.py` to check the immutable benchmark; run release-specific tests for the working game. The reference validator is **not** a gameplay test.
- Produce a change log, language coverage report, audio manifest, screenshot comparisons, browser interaction evidence and exact build checksum. Report PASS / FAIL / NOT TESTED; do not silently relabel FAIL as pass.
- Parent-ready release only when all four mandatory gates in `standards/RELEASE_GATE.md` pass. Otherwise label TEACHER PREVIEW or CLASSROOM PILOT and state blockers.
