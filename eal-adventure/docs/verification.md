# Expanded festival verification — 1 November 2026

Far Horizon source, reviewed build, and public root game remain preserved.
The separate project starts from `66e5f5ac63b2da147a4f4f8baea36e94a0bc46ff`.
Its actual Godot source and standard browser export were inspected before the
café was built. This update connects the complete agreed collection to play.

## Current candidate

- Exactly **144 entries, eighteen per topic**, retain the supplied PDF wording,
  Chinese meanings and source references. All entries have distinct resolving
  local illustrations. No unrelated words share a picture file or image hash.
- Five settings connect the café, sanctuary, park, story square and art garden.
  Resident requests, illustrated collections, delivery, sentence building,
  personal choices and manual speaking confirmation contribute eight stamps.
  Ordinary rounds show four choices. Replays and catalogue pages expose all
  eighteen entries in each topic without a mastery gate.
- General Chinese support explains controls only. Target-word Chinese is rendered
  only inside the explicitly labelled translation games. Translation support is
  logged separately from navigation help. Preferences remain ungraded.
- **117 approved Jesse MP3 files are byte-identical** to the supplied HTML.
  Vocabulary selection no longer depends on available recordings. Missing clips
  have no silent replay control and do not increment heard counts.
- The full classroom PDF has **fifty A4 pages**: black-and-white pictures,
  separate English/Chinese decks, sentence strips and drawing prompts. Use color
  materials or real objects when using the color cards in black and white.
- All **29 candidate files** match their SHA-256 manifest, all ordinary export
  files match the final build, and the complete backup ZIP passes CRC checking.

The frozen production export is Godot **4.6.3**, non-threaded Web / GL
Compatibility. Its complete offline cache revision is **651bdc26e421acc7**
(22 bundled web files, approximately 59.3 MiB). The fresh `update.html` entry
replaces an old installed pack while retaining the existing local save key.
A completion marker and controlling-worker version check gate updated play.

## Browser results

**268 expanded-game checks passed** with real input. All 144 cards were reached
through scene controls, all eighteen café foods and personal choices were
available, all eight missions reached the ending, and contributions survived
reload. Ordinary tasks revealed no target Chinese with navigation help enabled.
Explicit translation displayed the intended Chinese and logged its assistance.
Wrong delivery and sentence-order attempts gave retries; preferences were not
scored. Unrecorded new words were not falsely counted as heard. No Godot/browser
errors or external runtime requests were recorded. See [expanded-report.json](expanded-report.json).

**32 café regression checks passed**, covering movement and following, dialogue
movement lock, Jesse replay, wrong/correct deliveries, grammar and sentence order,
personal preferences excluded from accuracy, manual speaking participation,
festival changes, restoration, all eighteen foods, matching and translation,
voice/mute settings, teacher export, replay and confirmed reset. See
[milestone-report.json](milestone-report.json).

**Three emulated touch layouts passed**: iPad landscape 1024×768, iPad portrait
768×1024 and iPhone landscape 844×390. Touch moved Alan, opened resident dialogue,
enabled navigation help, entered the new sanctuary and read Ari's request without
revealing the Chinese answer. Screenshots were visually inspected. See
[touch-report.json](touch-report.json).

**17 exact-release/offline checks passed.** The complete app was cached, the
browser process closed, and a fresh process reopened from a disk-backed profile
with all networking disabled. The café delivery/sentence/personal-choice mission
reached its visible ending. A new sanctuary dolphin card was collected and
delivered offline. A Web Audio analyser measured decoded Jesse PCM; offline
replay worked, the separate music control reached zero and master mute suppressed
actual output samples. The production export exposes no debug bridge and logged
no browser/Godot errors. See [offline-report.json](offline-report.json).

Only the setup instructions and cache metadata changed after the game checks.
Every game/asset byte, including the PCK and game HTML, remains identical. The
final offline and installed-pack upgrade checks are rerunning for this entry
revision. Updated reports and Windows validation will be recorded before delivery.

The exact candidate passed [Windows validation run 41299138392](https://github.com/loganrossbryant-ai/EAL-Game/actions/runs/41299138392):
active normal protection, signatures `1.463.70.0`, native exit 0, no detections,
no error, and matching before/after file hashes. Candidate manifest SHA-256:
`a24bfc530a48dbddff3a95b790164dfb6d7eb0b453b55b5a0a09ef58ff6fa4c4`.
The actual result is [defender-report.json](defender-report.json).

## Remaining limits

Additional Jesse speech awaits sample approval. The attempted small sample did
not start because ElevenLabs reported busy; no substantial new dialogue,
alternate voice, browser synthesis or fragment splicing was used. Existing exact
clips are reused. New unrecorded entries use written English resident notes and
picture activities. Manual “We said it” confirms participation, not pronunciation.

Physical iOS Safari / Add to Home Screen testing is unavailable. Chromium touch
emulation and a cold offline restart cannot establish actual device behavior.
An adult should run the documented Airplane Mode check on Alan's iPad/iPhone.
The delivery is an offline web app and complete backup ZIP, not a signed native
iOS binary or an archive that runs directly in Files.

Third-person his/her progression, richer clue and arrangement activities, and
full newly recorded listening coverage remain later work. The current review
specifically fixes playable vocabulary breadth and the Chinese-support policy.

Direct github.io navigation is outside the environment's network policy.
Interactive checks use exact release files over local HTTP. Publication is
verified through GitHub Pages deployment status and exact remote blob hashes.
The existing Windows release process is applied to a separate `alan-review/`
candidate, preserving the Far Horizon release candidate and report.
