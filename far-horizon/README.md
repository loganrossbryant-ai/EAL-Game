# The Far Horizon — GM visual aid, Sessions 1–3

A Godot 4.6.3 presentation that the teacher operates while the class plays the
TTRPG. Four department representatives walk together through realistic ship
interiors. NPC conversations, manually held story beats and readable evidence
cards support live performance. There are no student accounts, response forms,
Word documents or classroom servers. The separate `godot/` Earth game is preserved.

The story follows GM Bible v12 pp.4–11 and the supplied chronological visual
deck v14 slides 1–28. The teacher confirmed **board → launch → introduction/tour**
and the complete **M-77 / TOMORROW 14:32** maintenance record. This version ends
at the sealed **+103 DAYS** packet header; later-session material is excluded.

## Play

Use a standard hosted Godot Web build in current Chrome or Edge. Its HTML,
JavaScript, WASM and game data are separate files. Opening just `index.html`
from a local disk is not supported by Godot; use a web host or local HTTP server.
The previously packed single HTML/ZIP remains withdrawn after the Defender alert.

Press **G** to open the **GM desk** in a second window. Keep that window on the
teacher's laptop and project the game window. Both windows must stay in the
same browser and origin. The desk is a presentation control, not a login or a
networked student application. Extend the display, rather than mirroring it,
if the notes must remain off the projector.

| Input | Action |
| --- | --- |
| A/D or arrows; click the floor | Walk |
| 1–4 or department buttons | Select the party leader |
| E | Take the marked access path, talk, use a terminal, or travel at a room exit |
| Enter / Page Down | Next beat, then next scene |
| Page Up | Previous beat, then previous scene |
| G | Open the separate GM desk |
| Space | Hold/resume the moving picture and party |
| P | Hide/show presentation controls |
| C | Reveal the evidence board of already shown cards |
| V | Optional academic vocabulary glosses |
| Escape | Close the projected card or conversation |

The desk jumps directly to any of 18 scenes and 64 beats, previews all 13 clues
privately, reveals/hides cards, opens NPC dialogue, controls sound/voice and tracks
M-77's two threat boxes and the minor drones' one each. All encounter rounds are
manually advanced. No combat result or writing task can prevent a clue reveal.
Progress, scene positions and chosen paths autosave locally under a new GM-only storage key.
Resetting one session preserves other sessions; the desk asks before resetting.

Optional Chinese, Korean and Japanese glosses cover **21 drama/evidence terms**,
not entire dialogue. Print the desk's vocabulary handout for targeted WIDA 1–3
support. Projected glosses are visible to everyone. Performance and paper-writing
prompts are optional, presented supports without in-game input or progression gates.

## Build and check

Use Godot 4.6.3 and its matching non-threaded Web templates, Python, Playwright and
Chromium. From the repository root:

```sh
export XDG_CACHE_HOME=/workspace/.cache
export XDG_DATA_HOME=/workspace/.local/share
export XDG_CONFIG_HOME=/workspace/.config
python tools/build_fh_campaign.py
godot --headless --editor --path far-horizon --import
godot --headless --path far-horizon --export-debug Web ../builds/far-horizon-debug/index.html
python tools/export_fh_web_assets.py builds/far-horizon-debug
python -m http.server 8090 --bind 127.0.0.1 --directory builds/far-horizon-debug
```

In another terminal: `python far-horizon/tests/browser_gm.py`. The test uses real
keyboard/mouse/GM controls and reads debug snapshots without setting game state.
It traverses all scenes/beats/cards, checks the desk, selectable dialogue, language
support, skeletal pelvis stability, followers, scene motion and local save.
`python far-horizon/tests/browser_stage3d.py` checks the default game's depth path,
staggered skeletal walks, turn-and-reach, real item zoom, return camera, returning
followers, physical onward travel and picture hold. Tests use Chromium's software
renderer; those frame rates are not measurements of school laptop GPU performance.
Reports/screenshots: `artifacts/far-horizon-tests/gm/` (ignored by Git).

The previous `browser_slice.py`, `browser_motion.py` and `browser_html.py` files
are historical tests of the retired Session 1 writing workflow. Use the new GM
tests for this implementation. The quality report in `docs/far-horizon` records
what actually passed; this README does not certify an untested build.

## Audio and visuals

The local sound effects and ambience are original procedural audio. The new
NPC script has **44 distinct authored lines / 3,102 characters / seven speakers**.
**ElevenLabs is deferred at the teacher's request.** No NPC voice pack is included.
Text and selectable dialogue work without recordings, and the GM desk reports their
absence. Original ambience and effects remain available. No API key belongs in
the game, source repository or browser.

If voices are requested in a future revision, configure the private key and run
`python tools/generate_fh_elevenlabs.py` to inspect
the seven distinct premade voice choices and quota, then `--generate` to record.
The generator publishes a catalog only after every MP3 passes duration/codec/
non-silence/hash checks. Browser playback, interruption, replay and mute still
need testing with actual ElevenLabs clips before a voiced release.

Original generated backgrounds follow the supplied references; see `assets/ART.md`.
The foreground now uses actual skinned 3D characters, original Pioneer uniforms,
idle/walk/use clips, head motion, eyelid geometry, gradual turns and separate gait
phases. CC0 MakeHuman/MPFB asset data supplies the human mesh and rig; its program
code is not shipped. Original procedural 3D machines have rounded hulls and moving
subassemblies. Raised galleries, stairs and paths into depth are traversable.
Using a gallery terminal turns the leader toward its controls, then moves the
camera onto its actual screen. Escape returns to exploration; a transcript/source
button provides the large accessible evidence card. The GM can reveal cards
instantly from the desk, without walking or completing another activity.
Shuttles, hovering drones, M-77's joints and welding, foliage, ventilation rotors,
an orrery, instrument gimbals, orbit blending and the post-cutoff pen animate in
their appropriate rooms. Solid moving subjects use geometry, not cutout sprites.
The lensing seeds are GM-cued and fleeting. Silver Pines guides the ambition;
this is a custom prototype, not a claim of commercial AA animation parity.

## Release

Prepare a **new standard release** and copy the web desk before preparing review:

```sh
godot --headless --path far-horizon --export-release Web ../builds/far-horizon-release/index.html
python tools/export_fh_web_assets.py builds/far-horizon-release
python tools/prepare_fh_review.py
```

New game bytes need a new matching successful Windows Defender report. The prior
Session 1 scan does not clear this draft. Preserve exact candidate bytes, review
manifest and `review-candidate/.gitattributes`. Follow `docs/far-horizon/security-review.md`.
No antivirus exclusions or disabling protection on a user's machine is part of delivery.

The existing public Pages site is hosted from `hello-earth-demo:gh-pages`.
This Sessions 1–3 revision must not be described as deployed until its matching
release is actually scanned, published and observed. Preserve the unrelated main
branch/Earth demo and never copy private history or raw GM documents into hosting.
