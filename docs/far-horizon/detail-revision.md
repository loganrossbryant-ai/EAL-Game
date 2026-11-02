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

## Validation in progress

The terminal's left balcony, controllable party and Venn dialogue, and the flat
lounge with Juno's selectable dialogue have run in Chromium without errors.
The original PPT images were visually inspected in both dialogue boxes. Close-up
model renders were inspected and hair placement, complexion patches, eyes and
collar fitting corrected. The repaired bob/ponytail anchors and final scale fixes
are included in the remaining room/release checks.

The browser test machine renders WebGL in software. It is useful for checking
real interaction, layout and rendered images, not for asserting a hardware frame
rate. Physical iPhone/Safari performance is not tested. Commercial AA parity is
not claimed. Release validation and the fresh matching Defender report must be
recorded before this revision is described as published.
