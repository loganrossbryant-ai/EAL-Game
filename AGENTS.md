# EAL 2026–2027 — v8 game production rules (Codex repository)

## Read first, every new or resumed game task

Before modifying gameplay or generating assets, run `python3 scripts/restore_v6.py` from the repository root; the two approved v6 HTML files are reconstructed exactly from Git-stored parts, and their SHA-256 values are validated. Then inspect these repository references:
- `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md` (v2.1, tool-directed governance and quality gates)
- `reference/EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`
- `reference/The_Town_That_Rebuilds_Itself_Living_Environments_v6.html`
- `reference/Do_Not_Answer_Your_Own_Voice_Living_Environments_v6.html`
- The active unit's original textbook material, student profile, and canonical source manifest (supply privately; do not commit sensitive student information to public repositories).

If reconstruction fails or any required files are missing, disclose exactly which are unavailable, and stop before development. Do not claim they were reviewed. Never silently replace newer sources with older game versions.

## Quality and process

1. V6 is the **minimum** visual/offline/mobile benchmark. Aim for v8 cinematic 2.5D exploration, varied authentic physical puzzles, and meaningful world-state changes. Do not copy benchmark artwork or narrative.
2. Map required textbook language to player actions. Scaffold appropriately; use accurate Chinese glosses and evidence-backed student writing.
3. Before scaling, build and test **one finished representative vertical slice** with actual art, scene-specific motion, integrated language action, offline mobile functionality, and visible consequence.
4. Maintain a brief per-task **Tool Selection and Verification Record**: requirement, choice/rationale/cost, acceptance test, observed result, fallback/blocker. Passing a tool call is not acceptance.
5. Prefer no-extra-cost tooling; no paid generation, public deployment, subscription, or irreversible action without teacher approval.
6. Keep a readable, modular codebase with original assets and deterministic offline release packaging. Prefer Phaser and accessible HTML if technical validation supports them; don't force an unsuitable engine.
7. Run actual browser/playthrough tests for all chapters, wrong answers, branches, save/restore, export, and mobile/touch/reduced-motion/offline. Inspect visual screenshots. Do not label an unverified build final.
8. Preserve approved v6 references as immutable benchmarks. Use a distinct working folder/branch and versioned release assets.

## Approval model

Teacher signs off consequential curriculum/creative/cost changes and the first fully playable new-architecture vertical slice. Codex/assistant owns ordinary tool choices, implementation, and QA. Report blockers; never quietly lower the standard.

## Public-repository safeguard

The repository may be public. Never commit identifiable student records, private classroom documents, copyrighted textbook scans, credentials, or other sensitive information. If a required source cannot be shared, record the blocker and request an authorized private source. Reference games remain approved exemplars only; do not edit them in place.
