# Game and reference source registry

This is an inventory/locator, **not** an automatic certification. Re-check exact branches, artifact SHA and source correspondence at each new task. Recorded from GitHub branch inspection on **2026-11-24**.

| Item | Current location | Classification | What is verified / caution |
|---|---|---|---|
| Living Environments v6 (two exact HTMLs) | `main:reference/_v6_payload/`, restored by `scripts/restore_v6.py` | **APPROVED REFERENCE** | Restore and check hashes locally before inspecting. Never modify. |
| Secondary v8 requirements | `main:docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`, `main:AGENTS.md` | CANONICAL RULES | Read Section 9 and canonical Studio docs. |
| Zig Lesson 4 | `codex/tutoring-game-setup:tutoring-games/references/allen-lesson-4/` | APPROVED TUTORING BENCHMARK | Archive and its SHA listed in `APPROVED_REFERENCE.md`; full modular source parity not demonstrated. Do not copy student assets into new game. |
| Tutoring standards/templates | `tutoring-games/` plus historical setup branch | CANONICAL SCOPED RULES after merge | Text-only scope docs imported/linked. Full archived Zig assets remain in separate reference branch until inspected and approved for migration. |
| Broken Bridge v0.1 planning | `codex/broken-bridge-25d-prototype` | EXPERIMENT | Mostly design documents; NOT the latest game source. |
| Broken Bridge v0.2/v0.3 | `codex/broken-bridge-v0.2.0-review`, `codex/broken-bridge-v0.3.0-review` | HISTORICAL REVIEW | Preserve history and rollback. |
| Broken Bridge v0.4 review | `codex/broken-bridge-v0.4.0-review`; root `Broken-Bridge-v0.4.0-Review.zip` and `Broken-Bridge-v0.4.0.html` | **ACTIVE REVIEW CANDIDATE, NOT APPROVED** | Source embedded in review ZIP; no verified independent modular source-to-release build in the ordinary `games/` tree. See checkpoint for blockers. |
| Phaser proof of concept | `codex/signal-playable-demo` | ENGINEERING REFERENCE ONLY | Do not claim approved visual or curriculum quality. |
| Far Horizon variants | `codex/far-horizon-*`, `codex/fh-defender-scan-*` | EXPERIMENT / HISTORICAL | Preserve until dependency/approval audit. |
| Tutoring student title branches | `codex/allen-grace-unit2-places`, `codex/alan-favorites-cafe` and `codex/alan-scan-*` | WORKING / REVIEW | These are NOT automatically gold-standard engine releases. |
| Other title/trial | `codex/unit9-last-ferry`, `codex/v8-vertical-slice-trial` | TRIAL / HISTORICAL | Keep until provenance and dependencies checked. |
| Published site | `gh-pages` | DEPLOYMENT — PROTECTED | Do not touch before verifying real URLs and rollback. |

Two open PRs observed at audit: tutoring setup kit and Alan's Favorites. **Do not merge, delete, or rebase them automatically.** Reconcile overlapping tutoring standards in any later merge.

### No-destructive-action rule
No branch deletion, git-history rewrite, HTML replacement, archived asset mutation, or `gh-pages` change as part of this documentation consolidation. Before retiring a branch: verify open PRs, commits not in main, source vs built artifact, deployment URLs, dependencies, copyright/privacy, rollback tag and a teacher-approved retirement list.
