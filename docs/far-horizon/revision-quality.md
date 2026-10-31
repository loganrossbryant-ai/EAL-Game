# Session 1 animation revision

The user requested smoother walking, independent activity in every setting, and
ElevenLabs NPC dialogue. The visual work is implemented; recording is blocked
by the missing private ElevenLabs connection. No other speech service is used.

## Changes

- Four original articulated character rigs, continuous two-bone leg movement,
  world-space planted feet and independent level boots.
- Staggered strides, opposing arm swing, breathing, planted direction changes,
  normalized standing/turn silhouettes, contact shadows and floor reflections.
- Followers match the actual speed of the person ahead, with a spacing
  correction. Camera look-ahead eases with velocity.
- Terminal: clouds masked to glass panes, exterior vapor, service-cart motion,
  navigation beacons and foreground leaf movement.
- Launch: cloud/pad vapor, live console plots and status lamps; preserved manual
  ignition, ascent/orbit transition, engine cutoff and floating pen.
- Habitation: wind-driven foreground foliage, warm light and suspended motes.
- Bridge and route log: stars drift within the glass, console plots update,
  navigation sweep rotates and floor ventilation moves.
- Dialogue captions and choices remain available. A local-recording player,
  replay/voice mute and ambience ducking are prepared for the ElevenLabs pack.

## Checked in Chromium

The real-keyboard/mouse Session 1 route passed without browser errors: four
representatives, leader changes, NPC branches, modal movement lock, writing,
local saves, paper and performance acknowledgements, boarding, all five launch
beats, orientation choices, observation, scripts, exact ending and record export.

The motion check passed with 166 steady ground-contact observations and a maximum
measured world-space contact drift of 0 pixels. All four rigs loaded, strides were
staggered, followers maintained steady speed, and idle/both directions/turns were
exercised. Separate fixed-camera captures showed independent visual changes in
all five scene states. Actual browser captures of walking, standing, terminal,
launch, habitation, bridge, dialogue and ending were visually inspected.

These are prototype animations; commercial AA parity is not claimed. Tests used
local HTTP. Direct navigation to the hosted github.io URL is blocked by the
managed runtime policy; deployment is verified through the public Actions run.

## ElevenLabs remains blocked

The authored recording manifest has 34 unique NPC lines / 3,435 characters, for
Venn, Juno, Iris, Rhee and Okafor. The environment has no secret binding and does
not allow api.elevenlabs.io. No speech files have been generated or added, and
real voice playback/replay/mute/ducking has not yet been tested.

`tools/generate_fh_elevenlabs.py` reads ELEVENLABS_API_KEY privately, selects five
distinct accessible stock voices, checks included quota, resumes validated
staged recordings, and publishes a catalog only after every MP3 passes format,
duration and non-silence checks. It sends authored NPC lines only, never student
writing. The API key is never included in the game or browser.

Finish that connection, generate and review the clips, browser-test all recorded
branches and voice controls, then rebuild and repeat Defender validation before
publishing a voiced revision.

## Release validation

The exact ordinary Godot Web export passed the standard 1280×720 browser check:
startup, audio worklets, movement, writing, restoration, no debug observations,
and confirmed new-class reset. No browser errors or unexpected network requests.
One automated save check timed out; the identical build passed both an observed
save run (all five written fields checked) and the unmodified test rerun.

A new Microsoft Defender scan passed on Windows Server 2022, run 41227037912,
source 81d1368b976c3ba4b345cbc23680f791d1522eea. Active normal protection,
script/archive scanning enabled, current signatures 1.463.59.0, no exclusions,
exit code 0, no detections, and matching hashes before/after scanning. Manifest:
863db723d8df541ef0145bf21b469826fad3df797e48fe6e19a50047ee3656f3.
This is actual scan evidence, not an absolute malware-free guarantee. The earlier
packed single HTML and ZIP remain withdrawn.

The ElevenLabs personal-secret requirement and api.elevenlabs.io destination are
saved in the cloud configuration draft, with updated Godot startup instructions.
The save did not apply/publish configuration or create a credential. The user must
enter the key privately, save/review the draft and publish the environment changes.

