# Far Horizon detail revision — 2026-11-02

Scope remains the GM-operated first three sessions. No student accounts or
editing, ElevenLabs work, or later-session story content has been added. The
18-scene / 64-beat / 13-clue campaign is byte-identical to the published draft.

## Changes

- Nine authored layout profiles replace the repeated right-side gallery. The
  boarding lane, launch deck and lounge are flat. Other locations use a west
  balcony, a two-ended central mezzanine, a short workshop dais, a four-person
  lift, a curved level aisle or a short instrument plinth.
- Nine skinned humans have tailored fabric shells, closed fabric edges, standing
  collars, role-specific details and equipment, geometric hair, fitted eyes,
  continuous skin coloring, existing eyelid geometry and normalized gait clips.
- M-77 and eight other location-specific robot, drone and machinery models have
  layered construction and separately animated subassemblies. Lounge furniture,
  boarding gates, service arms and instrument fixtures vary by location.
- Both the projected dialogue box and touch reading panel show actual original
  PPT portraits. All seven are byte copies, with presentation-only crop regions.
- NPC medium shots preserve the scenic bounds. Dialogue hides the current cue
  panel; closing it restores the cue. The lift gathers the four representatives,
  carries them together and restores its correct stop after saving/reloading.
- Static scenery is batched by material. Scale animation retains the original
  dimensions of small Iris and refreshment indicators.

## Build

Use the matching Godot 4.6.3 Web template. Export standard separate files and run
`tools/export_fh_web_assets.py` and `tools/prepare_fh_review.py`. The candidate has
30 hashed files, including the seven reference portraits and crop catalog.

For model rebuilds, run the original `build_fh_props3d.py` first, then
`build_fh_detail_props.py` so the detailed M-77 replaces the earlier model.
`build_fh_crew3d.py` imports the two own-code detail helpers and reads the existing
CC0 MakeHuman/MPFB asset data under `/workspace/reference-review/makehuman`.
Art provenance and the CC0 license are recorded under `far-horizon/assets/`.

## Validation completed

The 18-scene / 64-beat exact standard release passed through the real GM desk,
including clue reveals, selectable dialogue, saved progress, three academic
gloss languages, session reset and preservation of other sessions. The full-size
story UI was checked in the shipping touch world rendering profile. Full PC
rendering, keyboard movement, GM popup, scene jump and reading panel passed
separately. All nine room profiles visibly animate, all seven NPC dialogue
headers use their actual PPT images, and no dialogue text overflows its panel.
No browser errors or external runtime requests were recorded.

The distinct route types, two-ended mezzanine, four-person lift round trip and
upper stop after reload were exercised. Final placement and animation batching
were rechecked in the nine-room regression. The moving weld sparks remain
independent of static batches. Nine GLBs retain constant Walk pelvis height.
All seven portrait hashes match embedded images in slides 1–28.

Phone-size touch tests passed walking, depth travel, item zoom, original NPC
photos and replies, 18-scene selection, readable clues, orientation changes and
released movement. Those checks emulate an iPhone in Chromium; a physical
iPhone and Safari engine were not tested. The browser machine uses software
WebGL, so these checks do not establish hardware frame rate or AA parity.

Fresh active Windows Defender run **41369106496** passed the exact **30 files**,
with matching hashes before/after, native exit 0, no detections/errors, normal
active protection, script/archive scanning, no exclusions and signatures
**1.463.80.0**. An earlier runner failed before scanning with a Windows RPC
service error; the successful retry used the identical tree and manifest.
The old packed HTML/ZIP remains withdrawn.

Candidate manifest SHA-256:
`6d4bf022029e395f8f569386dfea4d37ca9da734018dc7b8d75ad5be812320df`.
Actual reports and detailed local verification are included beside this file.

## Published draft

[Play on PC or open in a phone browser](https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html).

Host commit `3efc35c0022c8e311ef4dea2965f97794797c3d0`, Pages run
**41370777111**, completed **Success**. The matching run summary identifies that
commit and the deployed base URL. Public raw metadata and the remote hosting ref
also match. Only `far-horizon/` changed; the root game and Alan Island tree are
identical to the previous host. Direct live-site navigation is blocked by the
runtime policy, so browser validation used the exact files locally.
