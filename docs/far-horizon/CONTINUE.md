# Far Horizon continuation — 2026-11-02

The current task is the **GM-only first three sessions**, with four travelling
representatives, selectable NPC dialogue, clear clues and manual scene/beat
navigation. Student editing/accounts/email/Microsoft 365/Word workflows were
cancelled. **ElevenLabs is explicitly deferred; do not request or inspect keys.**

The user authorized publishing the revised browser game for PC and iPhone.
Do not ask again for that publication. Do not publish environment settings.

## Story and references

The campaign remains byte-identical to the previous published draft: 18 scenes,
64 manual beats, 13 clue cards, seven NPCs, 21 academic terms with Simplified
Chinese/Korean/Japanese glosses. Use only the first three sessions. Canon:

- **Board → launch → crew introduction/tour**.
- Full bible **M-77 / TOMORROW 14:32 / TECHNICIAN COHORT 01 / Collision with
  unrecorded passenger resolved.** The contradictory P-73 ticket is excluded.
- End at the sealed **+103 DAYS** packet header, before its contents.

The v14 PPT slides 1–28 and GM bible pp.4–11 inform the game. Raw references
remain outside the checkout under `/workspace/reference-review/far-horizon-v14`
and `/workspace/attachments`. All requested references are accessible; no new
upload is needed. Actual original NPC photos are in `assets/portraits/`.

## Implemented detail revision

`PioneerStage3D` renders the default foreground, using nine skinned human GLBs
and original articulated machinery. The earlier 2D collision/follower controllers
are retained but their cutouts are hidden. Clothing shells, collars, pockets,
seams, emblems, rank details, straps and equipment are separate geometry. Skin
uses continuous vertex color and fitted geometric eyes; the earlier projected
AI face shader is no longer active. Idle/Walk/Use, eyelid morphs, body turns and
independent phases remain. Pelvis translation is constant through every Walk
clip. Source/CC0 license and original AI material provenance are recorded in
`assets/ART.md` and `assets/models/`.

`data/room_layouts.json` has nine authored profiles: a west terminal balcony,
flat boarding lane, flat launch deck, central two-ended mezzanine, flat lounge,
short workshop dais, personnel lift, curved level bridge aisle and short K-17
instrument plinth. Followers converge at the route junction. The lift gathers
all four riders, carries them together, restricts movement to its upper deck,
and restores the correct cabin stop after save/reload. Old route state migrates
without discarding clues or beats.

Distinct courier, cargo loader, medical skimmer, repair orb, repair tool spider,
game table, scanner and optical assembly replace universal foreground props.
M-77 has layered armor, individual tracks, hydraulic/cable detail, articulated
clamp/welder and animated sparks. Static scenery is batched; **animated sparks
must remain protected from batching**. Indicators retain their authored scale.
NPCs and machinery have been spaced to avoid intersecting one another.

Seven byte-identical PPT photos appear at the top of both Godot dialogue and
the HTML touch reading panel. `data/portraits.json` provides display-only crop
regions. NPC medium shots respect the scenic bounds; opening dialogue hides the
current cue panel and closing it restores the panel. Clues remain large and
readable; the separate same-browser GM desk and touch scene picker still work.

The debug-only `?preview=depth` prototype and old `browser_stage3d.py` /
`browser_depth.py` assumptions describe the **earlier uniform right gallery**.
Use `browser_detail_slice.py` and `browser_detail_rooms.py` for the current game.

## Build and verification

Godot 4.6.3 and its matching non-threaded Web template are installed. Blender
4.3.2 builds the models. Run `build_fh_props3d.py` before `build_fh_detail_props.py`
so the detailed M-77 replaces the earlier base model. `build_fh_crew3d.py` imports
our own `fh_character_detail.py` and reads CC0 asset data in the reference folder.
Do not restore the removed face projection or unanchored hair offsets.

Export standard separate Web files, copy with `tools/export_fh_web_assets.py`,
then freeze with `tools/prepare_fh_review.py`. The current candidate contains
**30 hashed files**, including seven original portrait JPGs and their catalog.
No single-file HTML packing or antivirus exclusion belongs in delivery.

The final candidate manifest SHA-256 is:
`6d4bf022029e395f8f569386dfea4d37ca9da734018dc7b8d75ad5be812320df`.
Active Windows Defender run **41369106496**, review commit
`e50ca11419164ade12b1fa7e241e6b26713bb23c`, passed with matching before/after
hashes, no detections/errors, normal active protection, script/archive scanning,
no exclusions and signatures **1.463.80.0**. The previous attempt failed before
scanning with a Windows RPC error; the successful retry used the identical tree.
Actual reports are in `docs/far-horizon/defender-detail-*.json`.

Current game-code checkpoint is **8625aaebcd18abdf4219795117029f9a54aed5f6** on
`codex/far-horizon-gm-sessions-1-3`. Later validation/documentation commits may
follow it without changing the reviewed game files.

The terminal/lounges, all route types, lift round trip and upper save restoration
have been exercised. The final focused regression passed all nine animated
profiles and seven portrait headers without browser errors or text overflow.
Model integrity confirms original first-28-slide portrait bytes and constant
Walk pelvis height. Exact-release story, desktop and touch results are recorded
under `artifacts/far-horizon-tests/`; final release/deployment JSON records take
precedence over provisional notes.

The test machine uses software WebGL. Full PC rendering is checked separately
from the 64-beat story pass, which uses the shipping touch world profile with a
full-size UI. Phone checks use Chromium iPhone-size/touch emulation. **No physical
iPhone or Safari-engine test** was possible; the official WebKit download was
blocked by network policy. Do not claim commercial AA parity or hardware FPS.

## Publication and workspace boundaries

Normal play URL:
`https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html`.
The detail build is **published** as host commit
**3efc35c0022c8e311ef4dea2965f97794797c3d0** on `hello-earth-demo:gh-pages`.
Pages run **41370777111** completed **Success** for that exact commit and records
the deployed base URL. The public release metadata matches the scanned manifest
and all 30 uploaded game hashes. Only 16 paths inside the owned Far Horizon
namespace changed; the other games were preserved.

The final `pages-detail-deployment.json` records the source, scan, host and run.
Direct github.io access is blocked by this runtime policy; verify public GitHub
Actions plus remote commit/hash identity, and distinguish that from live-site
browser navigation.

Preserve the unrelated root game and `alan-island/` tree. Do not reset or switch
the shared `work` checkout (HEAD 51d239a): the root README and Earth `godot/` have
unrelated local work. Use a temporary Git index and explicit paths for focused
commits. `/workspace/hello-earth-demo` is a separate clean checkout; preserve it.
The withdrawn packed HTML/ZIP stays withdrawn; no false-positive verdict was
established for the original alert.
