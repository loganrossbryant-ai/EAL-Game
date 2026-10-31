# The Far Horizon — Session 01

A playable Godot 4.6.3 classroom draft of **Welcome to Pioneer**, from the last
Earth terminal through the route-log cliffhanger. The GM controls a party of
four department representatives on the shared screen.

The separate `godot/` Earth game is preserved. Only Session 1 is implemented here.

## Playing

The reviewed delivery is the standard Godot Web export: an HTML entry page with separate JavaScript, WebAssembly, game data, and audio helpers. Use current Chrome or Edge and a keyboard/mouse. The hosted game needs no Godot installation.

The earlier custom all-in-one HTML/ZIP was withdrawn after a Defender alert. Do not use that package or the old single-file packager for distribution. Its detection has not been declared a false positive.

| Input | Action |
| --- | --- |
| A/D or left/right | Walk |
| Click the floor | Walk to a point |
| 1–4 / department tabs | Change party leader and spokesperson |
| E | Interact nearby / resume a held final exchange |
| L | Crew log |
| G | GM cues |
| Space | Hold/resume movement |
| Escape | Close the current panel, including while writing |
| SFX button | Enable/disable original ambience and effects |
| Replay / Voice in dialogue | Replay or mute a recorded NPC line when the voice pack is installed |

Speak with Venn, keep the characters' records, and perform each company's
crossing. The GM can acknowledge paper sheets and performances in GM Cues.
There is no real-time boarding failure. All 18 fictional crew names are available
in the writing panels; no real student names are requested.

Launch has five manually advanced beats. In habitation, each department chooses
a place and gives a written or spoken reason. Continue to the bridge, visit the
observation glass, keep three screenplay lines, and end on the route log.

Browser storage saves progress locally. **Export session record** downloads the
writing, Earth objects, dialogue choices, department responses, and GM paper
acknowledgements as JSON. The ending offers a confirmed reset for a new class.

## Building

Install Godot **4.6.3** and its matching Web export templates, plus Python 3.
Open `project.godot` for the editable project. From the repository root:

```sh
godot --headless --path far-horizon --editor --import --quit
mkdir -p builds/far-horizon-release
godot --headless --path far-horizon --export-release Web ../builds/far-horizon-release/index.html
python tools/prepare_fh_review.py
python -m http.server 8073 --directory review-candidate/far-horizon
```

Open `http://localhost:8073`. The managed environment uses writable XDG paths
under `/workspace`; its web export templates are already installed.

## Gameplay verification

- A terminal vertical slice was tested and visually reviewed **before** the ship
  areas were added.
- `tests/browser_slice.py --full`: real movement, followers, leader changes,
  documents, writing, dialogue branches, modal movement lock, paper review,
  boarding, launch, saved cue restoration, four department choices, observation,
  screenplay capture, the exact ending, and JSON export.
- `tests/browser_html.py` supports the standard release with `FH_STANDARD_BUILD=1`: startup, audio helpers, movement/writing, save restoration, no debug globals, and a new class. The standard build passed at 1280×720 without browser errors or unexpected network requests.
- `tests/browser_motion.py`: four continuous rigs, steady foot contact, staggered
  strides, following, turns and visible independent motion in each scene.
- Browser tests run over local HTTP. Live github.io navigation is blocked by the
  managed environment network policy; deployment is verified through GitHub Actions.

Run the tests with Python Playwright, Chromium at `/usr/bin/chromium`, and the
debug export served on port 8070 (`FH_URL` overrides it); the motion test defaults
to port 8080. The standard delivery test uses `FH_HTML_URL`. Reports and
screenshots are under ignored `artifacts/far-horizon-tests/`.

## Art and scope

The GM bible and all 11 pages of the small Session 1 packet were reviewed. The
large visual-aid PPTX and large complete PDF exceeded the transfer limit; the
small packet resolved the opening reference requirements. Raw GM documents and
later-session reveals are excluded from the game.

Original AI-generated terminal, launch, orbit, habitation, bridge, party, and NPC
assets follow the supplied realistic industrial science-fiction references.
Walking now uses original articulated cutout rigs with continuous two-bone leg
motion, world-space foot contacts, independently level boots, staggered strides,
arm counter-swing, breathing, planted turns, and separate front-facing conversation
poses. Followers match the person ahead's speed without repeatedly starting and
stopping; camera look-ahead eases with velocity. Contact shadows and faint floor
reflections ground the party. Silver Pines remains the quality direction;
commercial AA animation parity is not claimed.

Each setting has independent motion: masked sky drift, exterior vapor and a
service cart at the terminal; live launch telemetry, pad vapor, ignition movement,
orbit transition and a floating pen; wind-driven foreground plants, warm light and
motes in habitation; moving stars and console plots on the bridge and route log.

## NPC recordings — connection pending

The current revision has **no ElevenLabs recordings yet**. The environment has no
ElevenLabs secret and does not allow `api.elevenlabs.io`. No other speech provider
has been substituted. Captions and all dialogue choices remain playable.

The authored recording script has **34 unique lines / 3,435 characters / five NPCs**:
Venn, Juno, Iris, Rhee and Okafor. The dialogue player is prepared for local MP3
clips, interruption on next line/close, replay, separate voice mute and ambience
ducking. Playback with real ElevenLabs recordings still needs validation.

To finish recording, configure `ELEVENLABS_API_KEY` privately and allow
`api.elevenlabs.io` in the managed environment. Never put the key in source or the
browser. Export the authored script and review the stock-voice plan:

```sh
godot --headless --path far-horizon --script res://tools/export_voice_script.gd
python tools/generate_fh_elevenlabs.py
python tools/generate_fh_elevenlabs.py --generate
```

The generator uses five distinct accessible premade ElevenLabs voices, checks
included quota, and writes a catalog only after the complete MP3 set validates.
It sends authored NPC dialogue only. It never reads or submits student records.
Import the clips, test playback/interruption/replay/mute and coverage, rebuild,
and repeat Windows validation before publishing a voiced revision.

The numbered canonical deck map and M01/M02 recordings were not supplied. The
six-area directory is provisional; ambience and effects are original procedural
assets produced by `tools/synthesize_fh_audio.py`. No Silver Pines assets are used.

## Windows validation and browser delivery

The exact standard build passed Microsoft Defender on Windows Server 2022: active normal protection, script/archive scanning enabled, no exclusions, current signatures, exit code 0, and no detections. Hashes matched before and after scanning. The final report is from workflow run `41218947705`, source commit `fe242de394fd069263ad5793246e9eada51f0ec8`. This is evidence, not an absolute malware-free guarantee. The earlier packed file remains withdrawn.

`tools/windows_defender_review.ps1` is restricted to ephemeral GitHub Actions runners and never runs the game or disables protection. It creates a report even when scanning is unavailable or fails. `.github/workflows/far-horizon-defender-review.yml` runs on pushes to the review branch. Keep `review-candidate/.gitattributes` so Windows checkout does not change the scanned bytes.

For future releases, run `tools/prepare_fh_review.py`, validate the resulting exact files on Windows, and publish only a build with a matching successful scan report. Changing game files invalidates that clearance. Test the standard delivery with `FH_STANDARD_BUILD=1 FH_HTML_URL=http://127.0.0.1:8073/ python far-horizon/tests/browser_html.py`.

The public `hello-earth-demo` repository has the reviewed build on `gh-pages`. Pages is already active at `https://loganrossbryant-ai.github.io/hello-earth-demo/`. The public repository does not need a paid Pages plan. The hosted URL cannot be checked directly through this runtime's network policy.
