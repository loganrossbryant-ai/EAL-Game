# Café milestone verification — 1 November 2026

Source starts from Far Horizon `66e5f5ac63b2da147a4f4f8baea36e94a0bc46ff`.
The actual Godot source, scenery, articulated-character code, dialogue, UI,
exports and existing release process were inspected. Its standard Web build was
opened in Chromium at 1366×768. No Far Horizon file was edited.

## Observed results

- **32 gameplay checks passed** with real inputs, including movement, tap
  navigation, following, dialogue movement lock, Chinese reveal, local Jesse
  replay, incorrect and correct deliveries, sentence grammar/order, personal
  choices excluded from accuracy, manual speaking participation, festival
  changes, saved restoration, twelve illustrated foods, three menu activity
  types, sound controls, teacher export, reset, rotating orders and preserved
  festival contributions. No browser or Godot errors, or external runtime
  requests, were recorded.
- **15 exact-release / offline checks passed.** The complete app was cached,
  the browser process closed, and a fresh process opened using the same
  disk-backed profile with networking disabled. The cached entry page and game
  loaded, the delivery/sentence/personal-choice sequence reached the festival
  ending, and progress persisted. A Web Audio analyser measured decoded Jesse
  PCM samples; replay worked offline, the separate music control reached zero,
  and master mute suppressed actual output samples. The release exposes no
  test bridge.
- **Three touch layouts passed**: iPad landscape 1024×768, iPad portrait
  768×1024 and iPhone landscape 844×390. Real emulated touch moved Alan,
  approached Mina and revealed Chinese without browser errors. Screenshots
  were visually inspected. Landscape is recommended.
- The **eight-page A4 classroom preview** was rendered as a PDF and its card
  layout visually inspected. Pictures are black-and-white; English and Chinese
  decks are separate and have no matching numbers.
- All **117 extracted Jesse MP3s are byte-identical** to the supplied HTML.
  The data has exactly 18 entries in each of eight topics, matching the supplied
  PDF key. All twelve café illustrations resolve to distinct local assets.
- The backup ZIP passes its CRC check and includes every ordinary export file,
  all licenses, the classroom preview and offline instructions. Candidate file
  sizes and SHA-256 hashes are recorded in `alan-review/manifest.json`.

The tested offline pack's cache revision is **fe0882f1feb43ff1**. The export is
Godot 4.6.3, GL Compatibility, non-threaded Web; its JavaScript, WebAssembly,
PCK and audio helpers remain separate files. A completion marker is written
only after every cache entry has been saved. The installer and worker templates
participate in the cache revision so future updates receive a new complete pack.

## Limits that remain

Physical iOS Safari / Add to Home Screen testing was not available. Chromium
touch emulation and a cold offline restart do not establish real-device Safari
compatibility. An adult should perform the documented Airplane Mode check on
Alan's device. This is an offline web app, not a signed native iOS binary. The
ZIP itself does not run directly in iOS Files.

Eight café foods have fully voiced approved word and preference clips. Noodles,
dumplings, bread and eggs use visual matching while new speech awaits a Jesse
sample. The attempted sample did not start because ElevenLabs reported busy;
nothing was charged. No substantial new dialogue or substitute voice was made.
The name sentence and “That's my favorite, too!” have text models but no new
recording is claimed. Manual “We said it” is participation, not pronunciation
assessment.

The remaining locations, broader activity types and third-person “his/her”
progression await review of this café milestone. Future animal sentences must
use number agreement, such as “My favorite animals are dogs.”

Direct github.io navigation is outside this environment's network policy.
Public hosting is verified through GitHub Pages deployment status and exact
published file hashes; interactive browser checks use those exact files locally.
Windows release validation follows the existing project workflow in an isolated
`alan-review/` candidate, preserving the Far Horizon candidate and report.
