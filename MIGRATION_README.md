# How to continue the EAL browser game in Codex

This is a **starter brief built from known conversation/project context**, NOT an export of your complete ChatGPT Project and NOT a playable game. It does not contain previous game source, screenshots, in-world website assets, textbook content, or the full chat history.

1. Unzip this folder on your computer, e.g., `Documents/EAL-Browser-Game`.
2. Copy any existing game source files into `source_code/` (or their original directory structure). Do not overwrite a working project unnecessarily.
3. Put screenshots, reference art, textbook materials, and screenshots of prior designs into `reference_assets/`.
4. If you need the complete prior chat transcripts, export ChatGPT data through Settings > Data controls > Export data. Locate the relevant conversations in `conversations.json` and extract the game threads. The full export also contains unrelated account chats; do not drop the full account archive into Codex without filtering.
5. Open the ChatGPT desktop app > Codex, or a Codex client connected to your ChatGPT account, and open this **local folder** as the project. Codex reads `AGENTS.md` as project guidance.
6. Start by asking:

   'Read AGENTS.md and GAME_BRIEF.md. Inspect all source files and reference assets. Explain which earlier game components can be reused, which materials are missing, and propose a small build plan. Build and visually test a working playable vertical slice with a controllable character and one immersive in-world interaction. Do not discard any existing working code.'

7. Test the playable slice together before directing Codex to expand the story.

Official guidance:
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data
- https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex
