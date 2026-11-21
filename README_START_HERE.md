# Tutoring Game Standard V1 — ready-to-use setup kit

This kit was prepared against the actual final Allen Lesson 4 release package and the current `loganrossbryant-ai/EAL-Game` Codex branch. It is a **setup kit**, not an already installed workspace and not a newly certified mobile game.

## Do these actions in this order

1. **Keep a backup:** Download and retain `Allen_Lesson_4_Complete_Package_Food_Places_Activities_FINAL.zip`. The existing copy is already present in the Tutoring-Allen Project. Do not replace it. This setup kit also contains the actual final installable PWA as an immutable benchmark.
2. **Update ChatGPT Project:** Open Tutoring-Allen → `•••` → **Project settings** → instructions. **Append** the entire content of `01_CHATGPT_PROJECT_INSTRUCTIONS_APPEND.md` after the existing tutoring instructions; do not replace them.
3. **Add authoritative source:** Attach `tutoring-games/references/allen-lesson-4/APPROVED_REFERENCE.md`, `standards/QUALITY_STANDARD_V1.md`, and if storage permits the original approved complete package as Project reference sources. These are reference files; do not duplicate existing textbook screenshots.
4. **Install in Codex:** Open the existing `loganrossbryant-ai/EAL-Game` repo in Codex on the web. Start a task/feature branch from `codex/alan-favorites-cafe` (or latest real Allen source branch). Give it the setup ZIP and paste `PROMPTS/CODEX_SETUP_TASK.md`. If task attachments are unavailable, upload the ZIP to a temporary branch in GitHub using Add file → Upload files, then tell Codex to extract it into repository root and delete that temporary ZIP before its PR. Do not merge over approved game files.
5. **Verify on the PR:** Check `tutoring-games/AGENTS.md`, two `.agents/skills/` folders, `tutoring-games/references/allen-lesson-4/`, template files and passing `validate_reference.py` / unit tests. Approve only if the diff does not alter old released games.
6. **Do a small trial:** Start a new Codex task using `PROMPTS/CODEX_FIRST_GAME_TASK.md`. Review one revised mode and its screenshots before broader refactoring.
7. **Release policy:** New home games need the four `RELEASE_GATE.md` checks, including complete required audio and a real physical iPhone offline test. Until then label the result CLASSROOM PILOT / TEACHER PREVIEW.

## Important truths about the supplied benchmark
- Final complete Lesson 4 ZIP: 15 entries, exact source and nested PWA integrity checked.
- PWA: HTML + manifest + service worker + language JSON + 240 preserved MP3 clips.
- Game language is focused on food, places and activities; the classroom deck still also includes earlier animal/sports examples, and the newer Pip passage differs from the earlier printed one. Preserve that distinction when preparing new parity maps.
- Previous QA states 128/128 browser rounds and five finale checkpoints passed, but it explicitly does not certify new Jesse voice lines or iPhone/WeChat cold offline readiness. Do not overstate.

## Repository map in this ZIP
- `01_CHATGPT_PROJECT_INSTRUCTIONS_APPEND.md` — append to project settings
- `tutoring-games/AGENTS.md` — Codex rules for tutoring only
- `.agents/skills/` — Codex reusable update/release skills
- `tutoring-games/standards/` — benchmark, workflow and release gate
- `tutoring-games/references/allen-lesson-4/` — immutable reference PWA, screenshots, baseline QA and language map
- `tutoring-games/templates/` — brief, language matrix, example data, QA, changelog, learner pilot
- `tutoring-games/scripts/validate_reference.py` and `tests/` — executable baseline integrity checks
- `PROMPTS/` — ready-to-paste Codex tasks

## Caveat about installation
This ZIP by itself does **not** change ChatGPT Project settings, GitHub, or Codex. Until its contents are committed to the correct repository branch and the Project addendum is saved, the new standard is not persistent across all workspaces.
