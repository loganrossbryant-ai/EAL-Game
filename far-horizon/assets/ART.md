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

## Volumetric foreground revision

The default GM game now uses `assets/models/*.glb` for its foreground characters
and moving machines. The earlier transparent human/machine sheets above remain
portrait/reference assets; they are not the new moving world characters.

- Human base mesh, morphs, fitted eyes, eyelid targets, weights and the 53-bone
  game rig are CC0 asset data from MakeHuman and MPFB2. Sources and license are in
  `models/SOURCES.json` and `models/LICENSE-MakeHuman-CC0.txt`. No upstream program
  code is executed or shipped by the game.
- `tools/build_fh_crew3d.py` builds the original Pioneer uniforms, raised seams,
  collars, hair, packs, tablets and boots and bakes analytical limb poses into
  Idle / Walk / Use clips. Nine fictional characters have independent models.
- `tools/build_fh_props3d.py` creates the original rounded construction kit,
  articulated utility drone, tracked M-77 and small shuttle. These are generated
  geometry, not converted Silver Pines assets.
- `uniform_fabric.png`, `ship_alloy.png` and `crew_face_atlas.png` are original AI
  material images, viewed and copied unchanged from the generation results.
  The earlier face atlas and `data/face_fit.json` remain historical source assets;
  the detail revision below replaces projected face shading with continuous
  vertex-painted skin and fitted geometric eyes.
- Stairs, raised galleries, screens, planters/leaves, rotors, rings, pen and sparks
  are runtime 3D geometry. The scenic background plates remain static scenic art.

The real-time material lighting, animation and geometry are prototype work.
These assets are not motion capture or a claim of commercial AA production quality.

## Character, machinery and layout detail revision — 2026-11-02

The nine human models now have separate skinned fabric shells with bound edges,
fitted standing collars, lapels where appropriate, raised pocket flaps and snaps,
stitched seams, department emblems, rank braids, cuffs, woven belts, shoulder
straps and role-specific equipment. Venn has navy and gold officer details;
Juno has the reference bob, hood and orange work details; Okafor has a medical
coat; Rhee and Vale carry field tablets. Hair, eyes and skin are geometry and
vertex color, not a projected photograph. The real eyelid morph and normalized
Idle / Walk / Use clips remain. `tools/fh_character_detail.py` supplies the
original surfacing and clothing code used by `build_fh_crew3d.py`.

`tools/build_fh_detail_props.py` and `fh_prop_geometry.py` author distinct courier,
cargo loader, medical skimmer, repair orb, six-legged repair tool unit, game table,
security scanner and K-17 optical assembly. M-77 has layered ivory armor,
individual track links, road wheels, hydraulic hardware, cables, vent grilles,
an amber optic, an articulated clamp and copper welding tool. Independent pivot
assemblies are internally merged by material for rendering. No new enemy type
or plot event is implied by the repair-unit designs.

`robot_enamel.png` is original AI material art generated against the PPT robot
reference, viewed and copied byte-for-byte from
`/workspace/generated_images/exec-725fbb13-b1f2-4d3f-b88e-f0705dcf2b37.png`.
The source image pixels were not edited.

The seven JPGs under `portraits/` are unmodified embedded images from the supplied
v14 PPT: Venn (5), Iris (8), Juno (9), Rhee (16), M-77 (17), Vale (23), Okafor (24).
`data/portraits.json` defines display-only crop regions. Godot uses AtlasTexture;
the browser reading panel uses SVG viewBox. Both show the actual supplied image
at the top of each NPC dialogue, without synthesizing a replacement portrait.

`data/room_layouts.json` defines nine location profiles: a west terminal balcony,
flat boarding lane, flat launch deck, central commons mezzanine with a descending
exit, flat lounge, short workshop dais, personnel lift, level curved bridge aisle,
and short K-17 instrument plinth. Static rail/fixture geometry is batched by
material; moving machines and their joints stay independent. Shared locations
recur only where the three-session story revisits the same room.

## Textured cast and classroom projection revision (2026-11-02)

The active portraits are unchanged embedded images from the newly supplied
classroom visual deck: Venn 37, Vale 39, Okafor 40, Rhee 41, Juno 42 and Iris 44.
M-77 uses the illustration region of enemy dossier slide 2; the contradictory
stat block is outside the displayed region. Original bytes, dimensions, source
slides and SHA-256 values are recorded in `data/portraits.json`. Human photos
and the enemy illustration fill half the dialogue screen. The previously
confirmed GM-bible story and encounter counters remain canonical.

`skin_microdetail.png` is an original AI-generated seamless skin material tile,
viewed and copied unchanged from `exec-f939c6b7-cc07-4aeb-897d-454c5f2352be.png`.
It and the original uniform material are source inputs to Blender's 3D UV bake.
No NPC portrait is projected onto a character. The nine cast members now have
2048-pixel albedo maps and 1024-pixel tangent-normal/roughness/metallic maps in
`art/characters/`. Contact shading and material detail are baked once. Skinning,
eyelid morphs, physical clothing geometry and three animation clips remain.
Hidden inner garment faces are removed, and two material surfaces replace the
previous many-material characters. UVs, tangents, deform weights and mipmaps
are explicitly checked. Juno's pulled-back hairstyle follows the new photo.

Unused historical 2D character/machine sheets and baking-only skin art remain
in source, but are excluded from this 3D browser export. These are original
prototype models and textures; no Silver Pines assets or animation are included.
