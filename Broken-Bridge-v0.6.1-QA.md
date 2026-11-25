# Broken Bridge v0.6.1 river motion check

Codex implementation review, 25 November 2026. **Teacher preview.**

- Source commit `511005a9554b4cc6de1de6697f0515c97cf09cc2` on `codex/broken-bridge-v0.6.1-source`
- Playable HTML SHA-256 `d2a70bae0a1432ad061bfef8148c8df420d9778fe044dfbd43e03ab15845af0c`
- Play ZIP SHA-256 `a8cc2e4c583688cf64a67133a915ff0cb2a6868e90c8bda5c79be3625f876a10`
- Comparison build v0.6.0 from review commit `d82cdc69fea24b934498411d330028774f709076`, HTML SHA-256 `6a0c8483f642527e8f1062fa59ce1f9abf25fbd5c01c7cf2679d424ca65e5a2b`

| Check | Result | Evidence |
| --- | --- | --- |
| Reflections, water edges and rocks | **PASS in inspected Chromium captures** | The prior build streamed narrow Canvas paths and overlay images across its water. In v0.6.1 the breeze and water textures move independently. The view shows shifting reflected light and foam around the bridge and river rocks. Matching sampled rock and bank pixels stayed fixed. `evidence/river-comparison.mp4`, `qa/river-checks.json`. |
| Offline motion and viewport checks | **PASS** | The textured river rendered in the offline package at 1366×768, 390×844 and 844×390. The 1920×1080 ford playthrough was also exercised. The reduced-motion scene used the still water plate. `qa/river.log` and `evidence/river-*.jpg`. |
| Gameplay, saves and audio regression | **PASS** | 19 unit tests, four complete desktop and simulated-phone journeys, and three legacy save migrations. Wrong attempts, both routes, teacher export, reset and local voice replay exercised. Lookout navigation checked independently. `qa/units.log`, `qa/browser.log`, `qa/navigation.log`. |
| Source and packaging | **PASS** | Exact v0.6.1 HTML and Play ZIP reproduced from editable source and pinned npm archives after an offline dependency install. Older releases and their immutable original artwork and sound stay at their original commits. `SOURCE-SHA.txt`, `SHA256SUMS.txt`, `qa/source-rebuild.log`. |
| Literal local-file opening in managed Chromium | **FAIL in this environment** | Administrator policy blocks `file:` navigation. Offline browser tests used the exact HTML at a loopback origin and denied network dependencies. The extracted Play ZIP also launched and saved movement through a real localhost server. `qa/local-file.log`, `qa/loopback-launch.log`. |
| Physical iPhone, classroom alignment and creative sign-off | **NOT TESTED** | Device emulation confirms layout and compositing on the test host. Native phone performance and teacher acceptance remain separate. |

This revision uses the original scenery and trims the displacement to preserve detail in the riverbed. It reuses one Canvas texture with shoreline, rock, and stepping-stone masks. The two recordings were captured from the same stationary in-game camera. The comparison video vertically stacks and crops those recordings to the river. The full revised capture is in `evidence/river-desktop.mp4`.

Chromium 156 on Debian Linux. The timed stationary test sampled 26–29 texture updates in about 1.5 seconds. The desktop frame-interval p95 was 33.3 ms while other browser tests were running. Both simulated phone views were near 16.7 ms in that sample. These are host measurements. See the source note `visual-review/V061_RIVER.md` for the method.
