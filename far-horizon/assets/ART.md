# Session 1 art provenance

All PNG game environments and character sheets below were generated specifically
for this draft, using the user's Far Horizon packet as a visual reference.

| Asset | Purpose |
| --- | --- |
| terminal.png | Continuous Earth departure-terminal level |
| launch.png | Launch-cradle level, before ignition |
| launch_orbit.png | Matching interior with orbital exterior for launch blending |
| habitation.png | Student-habitation gallery level |
| bridge.png | Bridge/observation gallery level |
| crew_walk.png | Four fictional department representatives, 8 walking frames each |
| crew_idle.png | Four idle and four front/turn poses |
| officers.png | Captain Mara Venn and Juno Reyes, full body/portrait atlas |

`iris.jpeg`, `briefing.jpeg`, and `badges.jpeg` come from pages 8, 10, and 11 of
the user's supplied Session 1 small packet. Their flattened illustrations are
used as reference/portraits/props. `session_01_reference.png` is the earlier
reference board and is excluded from exports.

The animation sheets are original generated prototype assets, not motion
capture or rigged 3D characters. No assets from Silver Pines are included.

## Sessions 1–3 GM revision (2026-11-01)

The new work uses the teacher's chronological visual-aid deck v14, slides 1–28,
as its design reference. The original embedded images were inspected before use.
No Silver Pines art or animation is included. These are original generated
photorealistic scenic plates and transparent cutouts, not purchased production
3D models or motion capture.

| New asset | Source / use |
| --- | --- |
| recreation.png | Original AI art inspired by v14 slides 13–14; warm Pioneer lounge, clear walkable foreground |
| corridor.png | Original AI art inspired by v14 slide 15; habitation maintenance passage, door and life-support panel |
| k17.png | Original AI art inspired by v14 slides 21–22; black-hole observation gallery, no permanent human-like figure |
| utility_drone.png | Original AI hovering service actor, generated and then background-removal edited using image generation |
| m77.png | Original AI heavy maintenance actor inspired by the M-77 silhouette in v14 slide 17; tracked base, clamp and welder |
| shuttle.png | Original AI side-view transport for independent movement outside the terminal glass |
| officers_s23.png | Original AI Rhee / Vale / Okafor sheet, then transparent-background edit; visual continuity with v14 slides 16, 23 and 24 |

The source generation results are retained unchanged in `/workspace/generated_images`.
Game files are byte copies of those results; game-art pixels were not edited in
Python. Normal Godot atlas regions, transforms, clipping masks and procedural
light/spark/particle geometry provide runtime animation/compositing.

Raw display props in `assets/props/` are unmodified embedded image bytes from the
teacher's PPT: mission (6), badges (11), restricted notice (20), anomaly readout
(25), clocks (26), biometric screen (27), and the three officer references (16,
23,24). The conflicting P-73 / MT-4487 ticket is not distributed; a readable
M-77 record is rendered from the teacher-confirmed bible text. Every evidence
prop has a large selectable transcript card so painted lettering is not needed
to read the clue. None of slides 29–88 is included.

The Noto CJK subset in `fonts/Academic.otf` and `web/academic.otf` was made from
Google's official NotoSansCJKsc-Regular.otf, obtained from the notofonts/noto-cjk
repository. Required Chinese/Korean/Japanese glyph coverage was checked. The
unmodified license is included as `fonts/LICENSE-NotoCJK.txt`.
