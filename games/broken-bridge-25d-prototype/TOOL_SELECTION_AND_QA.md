# The Broken Bridge v0.1.0 — tool selection and QA

**Classification:** Playable teacher-review build. Curriculum alignment, approved narration and physical device gates remain open.

## References and production decisions

| Requirement | Choice, reason and observed evidence |
|---|---|
| Canonical visual baseline | **PASS** · Restored and hashed both v6 HTML files using the existing scripts. Opened both in Chromium, moved from map to first scene and inspected the rendered screenshots. The prototype carries forward contextual hotspots, motion controls, focus view and offline delivery. |
| Tutoring standards and Zig | **PASS** · Read tutoring instructions, `RELEASE_GATE.md`, `QUALITY_STANDARD_V1.md` and the Zig approval/QA records at `f977a6c279650b8a385880c86bc00438b91910f8`. Ran the archived Zig validator and inspected its home screenshot. The validator confirms archival integrity. Zig gameplay and device readiness were outside this comparison. |
| Engineering | **PASS** · Reviewed Signal at `f72194ddf5a135ff1a6f2e2b700e57fd770dc900`, including Phaser movement, DOM bridge, save/export, packaging and test limitations. Chose Phaser 3.90 in Canvas mode to match Signal's tested software-renderer path. The prototype uses native HTML dialogs and avoids a UI runtime dependency. WebGL and physical iPhone performance were unmeasured. |
| Exploration and dialogue references | Reviewed REGOLITH's project overview and survey-to-mission loop at `f5f25ba6bf7477c612b408b265c9275a4fd1200d`. Reviewed Paper Town's proximity interaction and authored quest states at `5c890f8f7c468b85e9d204941a9fefb81c0ebbb4`. The prototype follows those principles with physical landmark visits and conditional Ranger Lin dialogue. No code or assets were copied. |
| Art and motion | Original programmatic forest illustration, props and character art in `src/art.mjs` and `src/main.mjs`. Layered foliage, dusk lighting, localized current and reed motion, and camera parallax interpret the brief's atmosphere direction. No playable LAAS or Abyssal Garden source was identified in the supplied material. No external art or paid generation was used. |
| Audio | The dialogue is furnished as readable text. All Ranger Lin speech, question models, evidence prompts, work instructions and outcome lines are pending approved voice recordings. The only audio is original optional oscillator feedback, muted by default. |
| License and packaging | The build embeds Phaser 3.90 locally and includes its MIT license in the archive. Python creates a deterministic ZIP. No CDN, AI API, audio service, font download or runtime network dependency was found in the browser runs. |

## Browser and artifact checks

Chromium 156 on Linux. Phone dimensions are touch emulation. Browser tests open ZIP-extracted HTML in offline contexts and reject every request except the document and optional same-origin favicon. A separate cold launch and reload used an actual loopback HTTP server with external requests blocked.

| Check | Result | Evidence |
|---|---|---|
| State unit suite | **PASS** | 3 tests. Both routes require evidence, work order is enforced, partial progress persists, invalid versions and unsupported routes are rejected. |
| Desktop, 1366 × 768 | **PASS** | Elementary bridge and middle school ford. Arrow walking, mouse interactions, evidence visits, both outcomes and player crossings, desktop board drag, NPC dialogue and return to the shelter. |
| Phone portrait, 390 × 844 | **PASS** | Elementary ford. Tap movement, Chinese glyphs, depth comparison, rotation and marker placement, export and reset. |
| Phone landscape, 844 × 390 | **PASS** | Middle school bridge. Tap movement, repair order and placement, scrollable dialog and export. |
| Negative paths | **PASS** | Unsafe deep-water recommendation, missing evidence, hint, wrong target and premature rope/pack. Ford additionally recovers from a wrongly oriented marker. |
| Persistence and teacher record | **PASS** | Reload mid-task and after completion, anonymous JSON export checked in all four runs. Valid backup restore and invalid backup recovery exercised on desktop. |
| Motion and mute | **PASS** | Reduced-motion preference, explicit toggle, changing Canvas frames and a delayed start of the on-screen delivery, sound effects setting on/off. Hardware audibility was untested. |
| Visual QA | **PASS** | Inspected 16 browser captures of the clearing, depth exhibit, work area and outcome for desktop, portrait and landscape. Touch layout required a camera framing and tap-target adjustment during testing. Recreate evidence with `python3 tests/browser.py`. |
| Offline artifact | **PASS** | ZIP integrity, extracted HTML byte match, four offline playthroughs with reload, plus real loopback launch/reload. |
| Second desktop browser | **NOT TESTED** | Firefox was unavailable. Playwright's official download hosts returned HTTP 403 (domain forbidden) in the cloud environment. |
| Physical iPhone Safari, WeChat, Home Screen, target FPS | **NOT TESTED** | No physical iPhone was available. The ZIP runs through a local web server, and no PWA or hosted deployment was configured. |
| Approved narration | **FAIL** for independent-home release | Recordings are absent. No voice playback, approved-voice routing, home-use or pronunciation claims. |
| Current textbook alignment, learner timing and classroom usability | **NOT TESTED** | No current lesson or learner materials or real learner timing. The 10–15 minute target remains an estimate. |

## Teacher key

- **Bridge:** Two missing 90 cm boards, sound supports, two matching 90 cm boards on the rack. Seat both boards before securing the rope. The repaired deck opens and the ranger delivers over the bridge.
- **Ford:** The ford is 16 cm against a posted 20 cm limit. Deep water at the bridge is 38 cm. The fallen sign maps the white stones. The near marker points northwest and the far marker points southeast. Both markers must be placed before moving the supply pack. The bridge remains closed.
- The export identifies clue exposures, selected claims and citations, optional writing, hints, branch and completion. Its participation and reasoning fields are separate. Structured route checks provide feedback without grading language or pronunciation.

## Artifact identity

- Source branch `codex/broken-bridge-25d-prototype` · implementation base `c40d783d0bef50a4d8f09e4ecd1d13e46f8f1f4a`.
- ZIP SHA-256 `1c970f76e177f2d198900379f32ec2f547c10ba896824d7c3ad2eb003b5730e4`.
- HTML SHA-256 `e88e17f2ea5988a7055fe66faa80e23296b7c1b7c32ae494e1c7fa61d584f08a`.
