# The Broken Bridge v0.2.0 — visual QA

**Status:** Playable visual review candidate. The art judgment below records an internal screenshot review. Teacher acceptance remains pending.

## Running-build evidence

The screenshots were captured through actual play from the same single-file HTML delivered in the download. Phone sizes are Chromium touch emulations. Comparison images contain crops or resized views of those captures.

- [Desktop opening](screenshots/01-desktop-opening.jpg) and [v0.1.0 versus v0.2.0](screenshots/baseline-v-revision.jpg)
- [Phone portrait opening](screenshots/02-phone-portrait.jpg) and [phone landscape opening](screenshots/03-phone-landscape.jpg)
- [Ranger dialogue](screenshots/04-ranger-dialogue.jpg), [depth clue](screenshots/05-depth-clue.jpg), and [repair workbench](screenshots/07-repair-workbench.jpg)
- [Damaged bridge](screenshots/06-broken-bridge.jpg), [repaired bridge](screenshots/08-repaired-bridge.jpg), and [matched-camera comparison](screenshots/bridge-before-after.jpg)
- [Ford outcome on phone](screenshots/09-ford-after.jpg) and [ford outcome on desktop](screenshots/11-ford-desktop.jpg)
- [Compact, reduced-motion landscape](screenshots/10-compact-reduced-motion.jpg)

| Visual gate dimension | Result in reviewed captures |
|---|---|
| Authored detail and materials | **PASS** · Wet wood grain, board splinters, gravel, wet stone, moss, fabric and rope are identifiable. The forest layers, character frames and props are raster assets from original production sheets. |
| Art direction | **PASS** · Warm left light and cool cast tones connect the setting and props. Lin's ochre coat and field hat and the scout's teal coat and burgundy cap stay recognizable across animation. The dialogue portrait is cropped from the same source frame at higher resolution. |
| Depth and cinematography | **PASS** · Foreground ferns and rocks frame the trail, the stream separates the banks, and low-contrast ridgelines make the distance readable. Foreground cutouts scroll independently and can overlap actors. The phone portrait shows a scrolling section of the scene. |
| Legibility and storytelling | **PASS** · The river is visible through the open deck, and the storm debris and shallow-stone route read spatially. The revised HUD preserves the establishing view. Context labels use focus or hover, with a separate action prompt within reach. |
| Motion and persistent response | **PASS** · Water, foreground foliage, character motion and shelter light respond locally. Browser playback verified the ranger waits until the delivery dialog is dismissed. Bridge boards and rope, ford flags and the delivered pack leave visibly distinct states. |
| Mobile composition | **PASS** in Chromium 390 × 844 and 844 × 390 · Touch movement, readable Chinese, landmark hit areas of at least 44 CSS px, scrollable dialogs, compact focus view and reduced motion were exercised. A 75-frame portrait sample measured a 16.7 ms median frame interval on this Linux host. Physical device performance remains unmeasured. |
| Runtime, accessibility and offline | **PASS** for the exercised browser paths · Desktop keyboard and mouse, touch, progressive puzzle feedback, local persistence, export, settings, reduced motion, backup/restore, reset and offline loading. Keyboard focus labels and accessible button names are retained. Full assistive-technology review remains untested. |

The detailed comparison rationale, reference access, and exact baseline are in [art direction](ART_DIRECTION.md). The running revision was compared with actual local v0.1.0, approved v6 and Zig imagery, and the pinned REGOLITH overview. Paper Town was available through Godot scene and dialogue sources. Its selected LFS character media returned HTTP 403. The teacher-uploaded screenshot and canonical LAAS/Abyssal Garden assets were unavailable to this task.

## Runtime verification and open gates

- **PASS** · Three state unit tests. Four complete Chromium runs on Linux from the extracted offline artifact with external requests denied. Desktop runs covered elementary bridge and middle-school ford. Portrait covered elementary ford and landscape covered middle-school bridge. Both valid and negative play paths, player crossing and returning, delayed NPC departure, save and reload, teacher export, mute and reset were exercised.
- **PASS** · The standalone HTML launched and reloaded over actual loopback HTTP with zero external requests. An elementary ranger-question save created by v0.1.0 resumed in v0.2.0 at the same origin. All 27 textures are local WebP assets, about 11.4 MiB as decoded RGBA before canvas overhead.
- **NOT TESTED** · Direct local-file launch on an unmanaged browser. The managed Chromium instance returned `ERR_BLOCKED_BY_ADMINISTRATOR` for `file://`, so the tested fallback was loopback HTTP. Physical iPhone Safari, WeChat, browser comparison beyond Chromium, and classroom timing remain untested.
- **FAIL for independent-home release** · Approved voice recordings remain unavailable. Audio is optional synthesized effect feedback, with no recorded or synthesized speech. English dialogue and the illustrative language matrix require no audio to complete a route. No verified textbook alignment.

## Artifact identity

- Baseline tag `broken-bridge-v0.1.0-baseline` at `14aae94d15735a711664c0c543bab72aad9e091d`
- Revision branch `codex/broken-bridge-25d-prototype`
- Standalone HTML SHA-256 `90d57cf2886367bac646664aae1a050e615a4f6fd08ef761a12de1f0aeb7ca3b`
- Offline test ZIP SHA-256 `d2b0e759fe59c3dd3baf9909edc3fd68d0ba5ffa4bd9997ea0458d0384c903c5`
- [Change log](CHANGELOG.md) and [asset provenance](ASSET_PROVENANCE.md)
