# CONTINUE BROKEN BRIDGE — durable handoff checkpoint

**Saved:** 2026-11-25. **Latest review:** v0.5.0, **NOT approved**. Use this when the teacher says **“continue Broken Bridge”** or **“continue prototype.”**

## Latest independent audit — v0.5.0 (2026-11-25)
- **Current review branch:** `codex/broken-bridge-v0.5.0-review` at observed GitHub head `7e66cdd6150dba329338b8787ea60c4e92785213`. Review ZIP root contains `Broken-Bridge-v0.5.0-Review.zip` and compiled `Broken-Bridge-v0.5.0.html`; game folder exposes planning documents, not reproducible editable `src/` and test suite. **Source-to-build parity and 14 claimed unit tests NOT independently reproduced.**
- **Review ZIP:** 30 entries (HTML, evidence screenshots/videos, README/license). Embedded HTML SHA-256 `5ecb11dd066102f7c96d51dc4dea5f62d38d26a376a5c63ef3a9c739ee4ac240` matches supplied START-HERE. Local Chromium navigation was blocked by administrator policy; reported browser runs are not independent verification.
- **Voice/audio:** 22 distinct decodable MP3 narration clips (3.7–8.3s); no ongoing forest/river/wind ambience, authentic footsteps/rope/bridge SFX or music layer identified. SFX disabled by default; voice plays only by replay buttons. Current 'Sound effects' setting does not control narration. Supplied 3 gameplay videos have **no audio stream** and cannot establish the sound gate.
- **Motion:** `paintWorld` moves current/glints, two foreground sprites ~3 world units, a canopy overlay by ~0.013 rad, motes and light pulse. Forest and much ground remain flattened/static. In supplied same-camera ambient pair only ~0.86% of total pixels change >12 channel values (limited two-frame measurement). User reports the scene still feels lifeless.
- **Puzzle variety:** four clue inspections + evidence-backed route recommendation + bridge (two boards/rope) or ford (two markers/pack); both reuse collect/orient/place sequencing. This is **not yet a demonstrated reusable puzzle library**, nor varied mystery, instrument, mechanism, testimony or system-reconfiguration play.
- **Other missing:** meaningful NPC/world reactivity beyond scripted crossing; story complication/decision trade-off; multiple genuine language functions throughout, rather than one recommendation and prewritten reports; connected spatial discovery; mobile camera navigation.
- **Navigation:** v0.5 introduced authored near/far ground regions and provided test evidence addressing v0.4 sky walking. Do not treat this as still broken without new reproduction. Physical iPhone/WeChat and current-textbook alignment remain NOT TESTED.
- **v0.6 priority:** (1) commit reproducible modular game source/tests and protect v0.5 baseline; (2) integrated offline audio mixer and actual **audible** action/ambience demo; (3) original independently animated forest/river/near foliage with stationary-camera video and reduced motion; (4) THREE distinct *mechanic families* (evidence/instrument, spatial/mechanical manipulation, investigation/NPC communication) with meaningful EAL action and fair retries; (5) stronger NPC story/camera/mobile; (6) separate visual/audio/gameplay/device PASS/FAIL/NOT TESTED.
- Detailed external handoff created in the user's conversation: `Broken_Bridge_v050_Independent_Audit_and_v060_Codex_Handoff.md`. Not automatically attached to GitHub; inspect it when user supplies it. Do not invent that the file was committed.
- **No new game, no engine approval, no public deployment and no paid generation** pending teacher creative review. Preserve all previous releases, saves and approved voice assets.

## Historical checkpoint — v0.4.0
The section below preserves the previous detailed v0.4 findings and source locations for rollback. Its 'latest' references refer to the historical review, not the current working version.

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
