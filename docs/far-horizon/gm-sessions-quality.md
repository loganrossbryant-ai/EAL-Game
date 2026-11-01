# Far Horizon — Sessions 1–3, 3D foreground revision

**PC/iPhone preview checks and exact desktop QA passed. Fresh Windows Defender
scan passed. Public deployment is verified: Pages run 41323549024, commit 7953e57. ElevenLabs remains
deferred.**

## Scope and story

The GM operates one projected game and a separate same-browser control window.
There are no student accounts, response forms, emails, Word documents or servers.
Four department representatives travel together. NPC dialogue stays selectable.
Optional paper/live-performance prompts support the class without gating progress.
Academic vocabulary glosses cover 21 terms in Simplified Chinese, Korean and
Japanese; the GM can print a separate handout for WIDA 1–3 support.

| Session | Story and evidence retained |
| --- | --- |
| 1 | Healthy Earth / deliberate second civilization; wants, needs, fear, Earth object; boarding; five manual launch beats; crew introduction and six-area orientation after launch; fleeting unclassified lensing; optional screenplay lines; exact route-correction exchange |
| 2 | Ordinary ship friction; M-77 welding a functional door; Rhee; two threat boxes and two one-box minor drones; three manual encounter rounds; shutdown/retreat/containment; intact tomorrow maintenance clue; “Nobody deletes the record”; restricted-access boundary |
| 3 | Four-department observations; 37 / 102 days without a route change; incompatible K-17 measurements; unsynchronized working clocks; biological timing drift; fact/inference/question council; “Both”; second ambiguous lensing; reflection before the sealed +103 DAYS header; stop before contents |

The teacher confirmed **board → launch → crew introduction/tour** and the bible's
full **M-77 / TOMORROW 14:32 / TECHNICIAN COHORT 01 / “Collision with unrecorded
passenger resolved.”** record, styled like the PPT. The conflicting P-73 ticket
is excluded. Campaign integrity checks confirm 18 scenes, 64 beats and 13 clues.
Only v14 slides 1–28 and bible pp.4–11 inform the shipped campaign.

## Implemented and checked

The default game has skinned 3D crew/NPC models with idle, walk and use clips,
head motion, eyelid geometry, gestures and gradual turns. Moving solid props use
geometry. Raised galleries and paths into depth have accessible junctions; each
follower passes through the junction before changing routes. Using a gallery
terminal turns the leader's back toward the camera, reaches toward the device,
then zooms onto its actual screen. Escape returns to movement. Transcript/source
cards remain available, and the GM can reveal them instantly without walking.

Each setting has relevant moving subjects: terminal traffic and a service drone;
launch ventilation, orbit blending and a pen only after cutoff; habitation foliage;
a recreation orrery; M-77's joints/wheels/welding and two drones; restricted-area
ventilation; bridge/K-17 navigation gimbals and ship interfaces. Lensing is manually
cued, fleeting and unclassified. No later plot explanation is shown.

| Check | Result |
| --- | --- |
| Godot 4.6.3 import / native startup | Passed; no script/runtime errors |
| Default-game 3D browser check, 1366×768 | Passed; zero browser errors |
| Actual raised/depth route, independent gaits, turn/use, zoom/return, movement lock, returning followers, physical onward travel, picture hold | Passed |
| Visible scene motion in all eight settings | Passed; changing 3D transforms and rendered pixels |
| Sampled actual skeletal pelvis variation during steady flat walking | 0.000000 m observed |
| Exact standard release, 1280×720 | Passed all 64 beats across 18 scenes; zero browser errors |
| Clues, scene jumps, selectable dialogue, local save/reload, Chinese/Korean/Japanese glosses | Passed |
| Session reset: location, cue, evidence, threats; preservation of other sessions | Passed |
| External runtime network requests | None observed; game/desk assets were same-origin |
| Production debug global | Absent |
| NPC voice pack | Deferred; 0 recordings, readable/selectable dialogue available |

The recorded input-driven interaction was also sampled visually: the leader
turns his back, reaches toward the terminal, then the camera moves onto the screen.
The final close-up has no foreground bodies obscuring its text. The first full
GM run caught an unused 2D orrery null-texture error; the unused renderer is now
disabled and its optional texture handling is guarded. The final new 3D and exact
release runs both have zero browser errors.

## Practical limits and delivery

This remains a prototype with original Pioneer artwork and model/animation work.
It does not match commercial AA character-detail or animation production values.
Chromium used software graphics here and reported 3fps during inspection; that
verifies behavior/rendering, not classroom GPU smoothness. Test the shared build
on the actual projecting laptop before a lesson. Older 2D planted-foot statistics
do not validate the new 3D characters; the new pelvis result measures their skeleton.

The release candidate contains **18 separate files, about 93 MiB**, with exact
SHA-256 hashes and Godot/font/CC0 model licenses. No packed single HTML or ZIP is
used. No fresh Defender clearance or new deployment is claimed. The older live
Session 1 scan does not apply to these bytes. Respect the earlier no-publication
instruction before uploading the new candidate or replacing the shared demo.

Versioned machine-readable evidence and file hashes:
`docs/far-horizon/3d-release-local-verification.json`.
Local detailed artifacts (ignored by Git):

- `artifacts/far-horizon-tests/stage3d/results.json`
- `artifacts/far-horizon-tests/gm-release/results.json`
- `artifacts/far-horizon-tests/stage3d/turn-and-reach-review.jpg`
- `artifacts/far-horizon-tests/stage3d/04-item-closeup.png`
- `artifacts/far-horizon-tests/interaction-video/terminal-interaction.mp4`

No automatic usage-reset scheduler is available; none was created.

## PC/iPhone shared preview — 2026-11-01

`play.html` provides one shared entry with a 16:9 game frame, touch movement,
Interact, Read, Scenes, Return, Previous/Next and the existing desktop GM desk.
Read uses large, scrollable story/clue text and selectable NPC replies. The
18-scene picker works on a phone without a popup. Touch release, cancellation,
blur and timeout stop movement. Phone rendering uses lower 3D resolution.

The iPhone-size Chromium touch test passed at 390×844 and 844×390, including
actual touch movement/depth/use/zoom, NPC reply selection, clues, rotation and
no stuck walking. The shared desktop entry passed keyboard focus, movement,
GM popup/scene jumps and reading. Both had zero browser errors. The exact new
standard desktop release again passed all **64 beats**, save/reload, three
gloss languages and reset/preservation with zero errors.

No physical iPhone or Safari-engine test is claimed. The official WebKit browser
download was blocked by the environment's domain policy, which was not bypassed.

Fresh active Windows Defender review **41322320949** passed with exit0 and no
detections/errors, current signatures **1.463.73.0**, script/archive scanning
enabled, no exclusions, and matching hashes before/after scanning. The report
matches all **22** candidate files and manifest
`2f484806730de72363d1b11c01bfbdd0e71709a7b1dce430935d0641442cdc56`.
A clean scan is evidence, not an absolute malware-free guarantee.

Versioned evidence: `pc-iphone-release-verification.json` and
`defender-pc-iphone-report.json`. The earlier 18-file record is historical.
The user authorized publication; host only under `far-horizon/` and preserve
the independent root/Alan Island game. Deployment must still be observed.

The shared URL is now published at
https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html.
Pages run **41323549024** succeeded for commit
`7953e570a3da1b236df1361e3e1cbcf2390237e3`. All22 game-file hashes match the
scanned candidate. The existing root game and Alan Island tree are unchanged.
Verification used actual Pages/GitHub commit evidence; direct github.io navigation
is blocked by this environment's policy and was not claimed. See
`pages-pc-iphone-deployment.json`.
