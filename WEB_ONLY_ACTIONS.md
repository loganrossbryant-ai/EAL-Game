# Browser-only instructions: minimal setup steps

1. Download `Tutoring_Game_Standards_V1_Setup_Kit.zip` from this ChatGPT message and keep it on your computer. Do not unzip for the GitHub web-upload path.
2. In **ChatGPT → Tutoring-Allen → ⋯ → Project settings**, append `01_CHATGPT_PROJECT_INSTRUCTIONS_APPEND.md` to existing instructions and save. Leave all other instructions alone.
3. In GitHub open `https://github.com/loganrossbryant-ai/EAL-Game`. In the branch selector choose `codex/alan-favorites-cafe`. Create branch `codex/tutoring-game-setup` **from that branch**. Do not use main as the base for the new setup branch.
4. On the new branch choose **Add file → Upload files**; upload the **single ZIP file** `Tutoring_Game_Standards_V1_Setup_Kit.zip` to the repository root and commit it to the setup branch. At this point the ZIP is only stored, not installed; no game code has changed.
5. Open Codex on the web, select the EAL-Game repo and `codex/tutoring-game-setup` branch, and paste the entire `PROMPTS/CODEX_SETUP_FROM_GITHUB_UPLOAD.md`. Codex should extract the ZIP, remove only the temporary uploaded ZIP, run the two checks, and open a PR into `codex/alan-favorites-cafe`.
6. Review PR: changed files should be new `tutoring-games/`, new `.agents/skills/`, and setup docs/templates. Check that existing games and root guidance have no changes; check both tests PASS. Merge only after review.
7. Start a new Codex task with `PROMPTS/CODEX_FIRST_GAME_TASK.md` for a small proof-of-process change. Do not order a whole new game until that regression test passes.

**Fallback:** If GitHub refuses the ZIP upload or Codex cannot access the branch, upload/extract the ZIP into the repository using an authorized cloud computer or local git checkout instead. Do not tell Codex to recreate the benchmark from memory.

**Note:** New lesson PPTs and homework already inside this ChatGPT Project are **not automatically** filesystem files in Codex Cloud. For each future revision, hand off a verified language matrix/brief plus source files, or commit them to an explicitly linked lesson-source directory before claiming alignment.
