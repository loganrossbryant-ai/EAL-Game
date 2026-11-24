# CONTINUE BROKEN BRIDGE — durable handoff checkpoint

**Saved:** 2026-11-24. **Latest review:** v0.4.0, **NOT approved**. Use this when the teacher says **“continue Broken Bridge”** or **“continue prototype.”**

## Locate correct source and preserve it
- Repo: `loganrossbryant-ai/EAL-Game`
- Latest actual packaged build branch: `codex/broken-bridge-v0.4.0-review`; observed branch head `b56e041bb3381692a1d9a459907abfb1f6ffd245` at checkpoint.
- Root on that branch has `Broken-Bridge-v0.4.0-Review.zip` (~30 MB), `Broken-Bridge-v0.4.0.html` (~6 MB), and `games/broken-bridge-25d-prototype/` planning files. **The ordinary `games/` directory is not verified to contain the modular v0.4 source.** Inspect ZIP's `src/` first, establish reproducible source-to-build correspondence, and move/extract into a *new versioned working source folder only after validating files*, with original artifact untouched.
- Earlier docs on `codex/broken-bridge-25d-prototype` are planning notes, **not** the latest game.
- Teacher supplied screenshot of v0.4 bridge crossing: ranger/scout can walk into a distant sky/forest image once on far bank. This is a demonstrated visual/navigation FAIL.
- Keep v0.4, v0.3, v0.2, Zig, v6, URLs, voice and save compatibility unchanged; create a separate v0.5 working branch and reproducible rollback.

## Teacher's actual v0.5 requirements (highest priority)
1. **World navigation:** Fix `src/world.mjs` loose far-bank `canWalk`/bank math. Author a polygonal ground path/navigation mesh for near bank, bridge, far bank, and ford. Use one navigation contract for keyboard, tap-to-walk, NPC scripted traversal, save/resume. No walking into sky, water, building or non-ground background. Verify round-trip crossings and arbitrary outside-point clicks.
2. **Visual clarity:** Diagnose raster softness and scaling. v0.4 image assets include `forest.webp` at **1600×800**, `scenery-distance.webp` and `scenery-bank.webp` at **1470×735**, so 1920×1080 display/camera and zoom can enlarge a soft plate. Diagnose source softness vs compression vs filtering vs device-pixel ratio. Produce crisp original high-resolution game-ready **layered** assets, matching before/after states, memory-budgeted for iPhone. No blur/sharpen filter as substitute for actual detail.
3. **Environment in motion:** v0.4 `src/art.mjs` `paintWorld()` uses approximately ±7px current shift, opacity changes, tiny canopy rotation and lamp alpha. Need visible directional river current/ripples, independent foliage movement, drifting mist/leaves/light, physical responses at bridge/rocks; motion reduced variant. A static establishing screenshot is not adequate.
4. **Characters and performance:** v0.4 has 160×192 per-frame directional scout/ranger sprites, but characters remain tiny in wide shot. Check apparent scale, foot contacts, shadows, natural turns, walking/carrying/placing/inspection, NPC physical cross/delivery. Never merely increase size by arbitrary number; inspect actual gameplay footage.
5. **Interaction/UI:** Real carried boards, placed planks, rope fastening, ranger inspection, ford markers with visible persistent outcomes; decrease persistent floating icons, use contextual prompts without hiding key information.
6. **Curriculum/audio:** Maintain elementary/middle modes and evidence-backed claims, try invalid/contradictory English, preserve complete Kokoro audio with local captions/replay; never infer oral pronunciation. Do not claim textbook alignment without original lesson files. Preserve existing Jesse source recordings.
7. **Devices/QA:** Test actual desktop + simulated phone portrait/landscape, safe areas, touch controls, cold offline, save/reset, both outcomes and negative paths. Real iPhone Safari/Home Screen/WeChat are distinct unverified gates until physically tested. No unnecessary CDN/network/WebGPU.

## Acceptance evidence before creative review
- An **uninterrupted player video**: cross bridge, move along far-bank path with proper grounding, return, plus equivalent ford traversal.
- An **uninterrupted stationary-camera video** (10–15s) showing at least THREE separately visible ambient systems; reduced-motion comparison.
- Unaltered actual running screenshots at desktop 1920×1080 and 1366×768; phone portrait/landscape; clue closeup, NPC dialogue, before/after bridge, before/after ford, interactions.
- Matched v0.4/v0.5 crops at 100% for shelter, bridge, ground, vegetation and characters; source dimensions, compression and perf measurements.
- Explicit navigation coordinate tests for all legal/illegal polygons and crossing transitions; report PASS/FAIL/NOT TESTED with screenshot/video/test paths and source SHA.
- Test language invalid strings, wrong evidence, both modes/routes, audio routes, teacher report, save/restore/reset, offline zero requests. Logs alone do not certify subjective artistic quality.
- If required art/voice/device tooling unavailable report ART BLOCKED / NOT TESTED honestly; stop claiming v8/gold-standard/HOME RELEASE.

## Resume instruction for ChatGPT/Codex
**Do not start a fresh game.** Read `studio/README.md`, `standards/PRODUCTION_CONTRACT.md`, `standards/VISUAL_AND_INTERACTION_GATE.md`, and this checkpoint. Fetch the current latest Broken Bridge working branch, compare since this saved v0.4 SHA, inspect exact ZIP/source and actual assets/tests, then target ONLY outstanding failures. Preserve all functioning mechanics and voice. When teacher later signs off a fully polished playable slice, freeze the gold-standard reference and extract a reusable engine; **that extraction has NOT happened yet**.
