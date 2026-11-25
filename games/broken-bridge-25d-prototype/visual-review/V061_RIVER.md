# River motion in v0.6.1

This teacher-preview patch follows the review of v0.6.0. The scene originally drew dozens of thin crests as Canvas paths over the river on every render and moved five cropped overlays. The reference audit reproduced those screen-space strokes in the exact v0.6.0 HTML.

## Implementation

`src/river.mjs` samples the existing Alder River plate (`assets/scenery-bank.webp`). A shoreline mask and separate rock and stepping-stone footprints limit the animated surface. Small, downstream-travelling displacements bend the reflections and existing foam with finer movement at the far bank. A softer mask limits the effect at water edges. The ford step cue disturbs only nearby water pixels. The standing waves near the boulders come from the original authored pixels.

The animation reuses one Canvas texture. It copies the plate at its original texel density and updates at up to 18 Hz, with spatial wave terms computed at scene startup. The original plate is visible with reduced motion. New assets and dependencies are unnecessary. The old water sprites remain archived with their v0.6.0 art-generation sources.

| Requirement | Tool and cost | Acceptance evidence |
| --- | --- | --- |
| Water reads as part of the painted scene | Phaser Canvas texture sampled from the existing art. Local JavaScript and Canvas 2D. | Prior and revised fixed-camera captures. Animated reflection and midstream sample boxes, with stable rock and bank sample boxes. |
| Forward motion and clean edges | Directional spatial wave terms, masked stones and shore, small local ford wake. | Actual desktop, phone portrait and phone landscape scenes. Original plate remains still when the reduced-motion preference is set. |
| Offline play and release preservation | Existing self-contained HTML, pinned dependencies and archive scripts. No new downloads needed to run the game. | Full browser journeys and source-to-build checksum checks. v0.6.0 remains available from its frozen review commit. |

Run `python tests/river_browser.py` after building. Add `--baseline-html path/to/Broken-Bridge-v0.6.0.html --record` to compare both versions from the same camera position. The recording and screenshot checks support teacher review. Classroom use, real iPhone performance and creative acceptance remain separate.
