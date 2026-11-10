# Approved Living Environments v6 — Immutable Reference Builds

This folder contains the teacher-approved **minimum** presentation/offline/mobile references for v8 games, not artwork to copy into new stories.

## Restore exact approved HTML files

The source games are too large for a single upload through the connected repository integration. Their complete UTF-8 bytes are stored, without edits, as numbered blobs under `reference/_v6_payload/`.

Run from repository root:

```bash
python3 scripts/restore_v6.py
python3 scripts/restore_v6.py --check
```

The script reconstructs both HTML files and compares their SHA-256 hashes with the teacher-approved values in `EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`. It refuses to overwrite an altered existing file and exits with a failure code on incomplete/corrupt input.

**Codex must run this before inspecting v6 files.** The generated HTML files are intentionally ignored by Git, because their exact contents are tracked through the numbered source parts. Do not modify these references in place.

## Source-of-truth order

1. `../docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md` — v2.1 including Section 9 tool-directed governance
2. `EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md` — approved SHA-256 hashes and visual baseline
3. Exact restored Town and Voice v6 HTML files
4. Current textbook pages and learner profiles **provided privately**, not committed to this public repository.

Current v8 development should go under `games/` and `shared/`. Existing approved game branches and releases remain unchanged.
