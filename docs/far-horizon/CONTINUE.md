# Far Horizon continuation — 2026-11-01

Latest scope: **GM-only**, first **three sessions**, four travelling department
representatives, selectable NPC dialogue, clear evidence, direct scene/beat jumps.
No student editing, accounts, groups, emails, Word or Microsoft 365 workflow.
**ElevenLabs is explicitly deferred. Do not check or ask for another key.**

Canon confirmations: full bible **M-77 / TOMORROW 14:32 / TECHNICIAN COHORT 01 /
Collision with unrecorded passenger resolved.** clue, styled like the PPT;
**board → launch → crew introduction/tour**. End before the sealed +103 DAYS packet
contents. Reference v14 slides 1–28 and bible pp.4–11 inform these sessions; no
later-session material ships. Raw references remain outside the checkout under
`/workspace/reference-review/far-horizon-v14` and `/workspace/attachments`.

## Current implementation

`tools/build_fh_campaign.py` authors 18 scenes / 64 manual beats / 13 clue cards /
seven NPCs / 21 academic terms with Simplified Chinese, Korean and Japanese glosses.
`main.gd`, `gm_story.gd`, `gm_state.gd` retain the GM flow, optional paper/live prompts,
revealed-only evidence board, local save, threats and same-browser GM desk. New
`routes` state preserves the selected access path per scene.

The **default main game is now 3D foreground**, with a SubViewport behind its UI.
Hidden 2D collision/follower controllers remain, but their cutout visuals are not
rendered. `CinematicAvatar` loads real skinned GLBs: four reps plus Venn, Juno, Rhee,
Vale, Okafor. Idle/walk/use clips, head motion, blinks, gestures and body turns.
`PioneerStage3D` builds traversable stairs/depth paths/galleries, real screens,
original machines, plant leaves, ventilation rotors, an orrery, navigation gimbals,
Iris emitter rings, orbit blending, post-cutoff pen and cued lensing. M-77 joints,
wheels, welder sparks and task light respond to the manual encounter beats.

E near the marked junction approaches it and changes path. Each follower must
cross that junction before changing routes, including when reversing from an
upper path. E near a gallery terminal turns/reaches, zooms onto the actual screen,
locks movement and offers transcript/source and other scene records. Escape
returns to the world. The desk can reveal any card immediately without walking.
Old packed HTML remains withdrawn; use standard Godot Web files only.

The separate `?preview=depth` scene is a **debug-only historical vertical slice**.
The default game is the implementation to verify and deliver.

## Art pipeline / corrections

Blender 4.3.2 builder scripts: `tools/build_fh_crew3d.py`, `build_fh_props3d.py`.
Upstream **CC0 asset data only** at `/workspace/reference-review/makehuman`; sources
and license in `assets/models`. No upstream AGPL application code is copied.
Original uniforms, equipment, hair and machines; original AI cloth/alloy/face
materials. Retain anatomical labels in BASE topology coordinates, the official
barycentric eye fitting, normalized analytic limb IK and 0.80m gait. Earlier
chicken-wing arms/bowed knees were rejected and corrected. New smoothing, raised
collars/seams and shaped boots are included. Nine human GLBs are built.

Actual item close-ups initially had foreground bodies occluding text. The new
stage explicitly hides models once the close camera reaches the screen and
restores them on return. GeometryInstance transparency alone did not reliably
remove them in Compatibility Web rendering. Keep this fix.

No Silver Pines assets/animation were copied. Two screenshots were visible;
composition and user-described behavior informed the revision. Do not claim
commercial AA parity or that unseen animation footage was reviewed. Never use
Python to edit game-art pixels; mesh/UV processing and QA screenshot analysis are
normal implementation. The unused generated depth-terminal plate stays outside
the game because its painted ramp/person conflicted with the geometry.

## Validation / running

See `gm-sessions-quality.md` for current results. The earlier 2D planted-contact
figures do **not** validate the new 3D characters. The first depth preview proved
path/NPC/zoom/return, then timed out walking in its second room on the software
renderer; use the integrated default-game test for final results.

- `far-horizon/tests/browser_gm.py`: all scenes/beats/cards, actual skeletal pelvis
  stability, followers, dialogue, GM desk, glossary, local save and scene motion.
- `far-horizon/tests/browser_stage3d.py`: default game's raised route, independent
  gait phases, back-facing use, physical item zoom, movement lock, camera return,
  returning followers, physical onward travel, second setting and picture hold.
- `far-horizon/tests/browser_release_gm.py`: exact ordinary release via public GM
  controls and a read-only BroadcastChannel observer; no debug setters/globals.
- `browser_depth.py`: historical debug prototype only.

Godot 4.6.3 with matching Web templates; Blender 4.3.2; Chromium; Python Playwright,
Pillow/NumPy/FontTools; system ffmpeg. Playwright's bundled video ffmpeg is absent. A task-specific cache at
`/workspace/.cache/fh-playwright/ffmpeg-1011/ffmpeg-linux` links system ffmpeg;
`capture_interaction.py` records the real interaction using that path. Writable XDG paths under
`/workspace/.cache`, `/workspace/.local/share`, `/workspace/.config`.
Local debug HTTP port 8090, directory `builds/far-horizon-debug`. Network sockets /
Chromium need approved escalation. Sandbox editor socket errors are distinct from
script/runtime errors. Chromium uses a **software renderer**, not a classroom GPU;
wait for game-state conditions rather than assuming wall time equals game time.

## Release / preservation

The user said not to publish environment changes; no new public game deployment
or environment publication has been made during this revision. Prepare a tested
reviewable result before any publication question. A new release needs a fresh
matching active Windows Defender report before delivery. New bytes are not
cleared by the old Session 1 scan. `prepare_fh_review.py` preserves ordinary
HTML/JS/WASM/PCK + GM desk/font/data + licenses and hashes each file. No antivirus
exclusions, packed single HTML, or claims of guaranteed malware absence.

Historical live URL: https://loganrossbryant-ai.github.io/hello-earth-demo/,
`gh-pages` commit 07971c1af1de899ec831accf98b64e5ad15bccb2, Pages run 41227599343.
Old Defender review: 81d1368b976c3ba4b345cbc23680f791d1522eea, run 41227037912.
These are **old S1 only**, not this draft. Public github.io is blocked here;
use actual matching GitHub Actions/deployment evidence if later publishing.

Workspace branch `work` remains at baseline 51d239a; most Far Horizon source is
untracked relative to it. Local checkpoint branch
`codex/far-horizon-gm-sessions-1-3` initially c644bd9fe5bf1342ba55da3eb00aadec2b335fa5,
parent old source66e5f5ac. Use a temporary index and explicit Far Horizon paths for
new focused commits. Never reset/switch over the workspace. Preserve unrelated
root README and `godot/` Earth work, and clean `/workspace/hello-earth-demo` checkout.
No raw references, secrets, builds, imports or screenshots in a source commit.
Source EAL-Game is now public. Hosting must not copy source/private history.

No quota/reset scheduling tool is available; no automatic continuation was created.

## Most recent verification

Default `browser_stage3d.py` passed with zero errors: actual 3D routes, four
independent walk phases, sampled skeletal pelvis variation 0.0m, back-facing Use,
zoom/return/movement lock, followers returning without dropping, connected launch
setting, picture hold, visible motion in all eight rooms. Software renderer
reported 3fps; do not claim classroom GPU smoothness. A short actual input-driven
recording was reviewed; still `stage3d/turn-and-reach-review.jpg`, MP4 under
`interaction-video/terminal-interaction.mp4`.

The full prior GM run traversed all 64 beats/13 clues and tested save/dialogue/three
gloss languages/layout, then caught an unused retired 2D orrery null texture. Fixed
its optional texture handling and disabled that unused renderer in main. New 3D
test, including recreation, has zero errors.

Fresh release candidate is 18 separately hashed files (~93MiB) with CC0 model
license included. Exact 1280×720 release walkthrough PASSED all 64 beats, scene jumps, clues,
dialogue, save/reload, all three gloss languages and session reset/preservation,
with zero browser errors and no debug global. Its initial fixed
1.3-second movement wait was too short on software graphics; it now waits for
actual travel before releasing the key, as the 3D test does. No game behavior
changed for that test correction. No new Defender clearance or publication.

Final evidence is versioned in `docs/far-horizon/3d-release-local-verification.json`,
including the exact candidate manifest hash/file hashes and both successful
results. Candidate bytes have not changed since the passing release test.
The short recording uses a workspace symlink to system ffmpeg; back/reach frame
and final readable zoom were visually inspected. The final source checkpoint is saved only on the local
`codex/far-horizon-gm-sessions-1-3` branch, with an expected-old-ref check.
Workspace `work` is untouched; no push/publication.

## PC/iPhone publication authorized (latest)

The user explicitly approved uploading/scanning/publishing and asked for a version
they can open on both PC and iPhone. No further publication permission is needed.
Keep ElevenLabs deferred and environment settings unchanged.

Shared entry: `play.html/js/css`, with an actual Godot `index.html` frame at 16:9.
Touch movement/Interact, large Read panel with validated NPC reply selection,
18-scene picker, Previous/Next and Return. Static poster is an unchanged byte copy
of the original terminal art. Phone 3D viewport uses half resolution and no MSAA.
Input timeouts/blur/pointer-cancel prevent stuck walking. Same game/story/save.

Phone emulation test passed in Chromium (390×844 / 844×390), zero errors. Real
physical iPhone Safari was not tested. Official WebKit download failed with the
network-policy 403 Domain forbidden; no bypass. Do not claim Safari testing.
The installer removed the task-specific ffmpeg symlink; it has been restored.

Candidate now has 22 separately hashed files. Review commit
`a4fdcc3cb468f6a254d1cca0b63c4f77b4dda5e8` was prepared and pushed to the existing
`codex/far-horizon-defender-review` branch to trigger a fresh Windows scan.
Manifest hash: `2f484806730de72363d1b11c01bfbdd0e71709a7b1dce430935d0641442cdc56`.
Phone QA: `artifacts/far-horizon-tests/phone/results.json`. Complete desktop
release QA is running against the same candidate on local HTTP port8092.

Host `hello-earth-demo:gh-pages` has newer independent Alan Island work! Latest
fetched parent is a4712a30ab6494f2deab78a9253b30beb806e806. Preserve its root and
`alan-island` files; publish the new Far Horizon only under **far-horizon/**.
Planned URL `https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html`.
Fetch again before creating/pushing the Pages commit, use a temporary index and
only the new owned folder, fast-forward only. Never force-push or copy source
history into hosting. Exact candidate hashes and the fresh scan must match.

Temporary source index from the last turn was deleted after source checkpoint
4bca990; create a new one parented to 4bca990 for the mobile source change.
Runtime and skill were read; network is enforced, git push dry-run succeeded.
GitHub APIs/github.io are not allowed; GitHub HTML/raw/git are allowed. Use
Actions summaries and public report branches to verify scan/deployment.

PC/iPhone final validation: phone preview PASS; PC shared entry PASS; exact PC
release all64 beats PASS, zero errors, save/reload/glosses/reset PASS.
Fresh Defender run41322320949 PASS, sourcea4fdcc3, same22-file manifest, no
detections, signatures1.463.73.0, active/no exclusions/hash match. Actual report
saved at `defender-pc-iphone-report.json`; full verification JSON at
`pc-iphone-release-verification.json`. Deployment is now authorized and ready.

## NOW LIVE — authoritative latest state

Shared PC/iPhone URL:
https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html

Public host commit7953e570a3da1b236df1361e3e1cbcf2390237e3, Pages run41323549024
SUCCESS, exact commit visible in public run. Remote gh-pages matches. All22
published game-file hashes match Defender reviewa4fdcc3, run41322320949 PASS.
Root/Alan Island trees were preserved exactly. Live github.io navigation is
policy-blocked; do not claim it was opened here. Physical iPhone/Safari was not
tested; iPhone13-size touch/rotation/Read/dialogue/scene picker passed Chromium
emulation. PC shared wrapper/keyboard/GM popup passed, and all64 exact release
beats/save/gloss/reset passed with zero errors. ElevenLabs deferred.

Source was pushed to EAL-Game branch `codex/far-horizon-gm-sessions-1-3`, code
commitab749b7600c50f7bcdc335f55058e5e4dc2a5f4f. Deployment metadata follow-up
is a child on that same branch. Workspace `work` remains baseline; unrelated
root README/godot Earth and clean hello-earth-demo checkout unchanged.

Latest records: `pages-pc-iphone-deployment.json`, `defender-pc-iphone-report.json`,
`pc-iphone-release-verification.json`. Candidate22 files (~95MiB), manifest2f4848...
No environment configuration changes or publication. User's approval covers
this game release; do not request it again for an already-authorized next step.
