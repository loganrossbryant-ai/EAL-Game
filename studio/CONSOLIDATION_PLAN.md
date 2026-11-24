# Safe cleanup and migration record — 2026-11-24

## Changes in this normalization
- Add clear root landing README and centralized `studio/` directory.
- Establish one shared QA/visual/audio/source standard and reusable starter templates.
- Import **text-only** tutoring scoped rules/templates from historical setup branch (not private files or the 12 MB reference ZIP).
- Create durable Broken Bridge v0.5 checkpoint and branch registry.
- Add a structure/contract validation script and opt-in CI.
- Root `AGENTS.md` points to canonical studio rules; old v6/secondary instructions stay intact.

## Deliberately NOT changed
- All approved v6 reference payloads, generated reference hashes, Zig archive, other games, release artifacts, branch commits, save URLs, `gh-pages`, existing CI script and deployed content.
- Branches not deleted, renamed, rebased, force-pushed or merged. Existing open tutoring setup and Alan PRs remain for later compatibility review.
- No v0.4 root ZIP or compiled HTML copied to main (large, historical, and source parity unverified).
- No “gold standard engine” source invented; extraction is blocked on visual/gameplay and source validation.

## Next migration after a teacher-approved reference
1. Import **actual modular and reproducible** Broken Bridge source after v0.5+ acceptance; keep a frozen release/tag/sha and full artifact hash.
2. Extract engine modules to reusable `engine/` and adapt one unrelated unit as acceptance test.
3. Reconcile the historical tutoring PR and approved Zig archive location/license/privacy before merge.
4. Audit ~many experimental branches for unique commits and live deployments, label as archive or active, then obtain teacher approval for any deletion.
5. Validate every source/package mapping, release URL, iPhone and offline test with evidence. Only update `studio/STUDIO_REGISTRY.md` to APPROVED after independent verification.
