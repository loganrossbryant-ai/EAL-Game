# The Far Horizon — Session 01

A playable Godot 4.6.3 classroom draft of **Welcome to Pioneer**, from the last
Earth terminal through the route-log cliffhanger. The GM controls a party of
four department representatives on the shared screen.

The separate `godot/` Earth game is preserved. Only Session 1 is implemented here.

## Playing

The delivery build is a single `index.html` containing the engine, artwork,
fonts, ambient sound, sound effects, and license notices. Use current Chrome or
Edge and a keyboard/mouse. The hosted page needs no Godot installation.

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
| Sound button | Enable/disable original ambience and effects |

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
python tools/package_fh_html.py
python -m http.server 8071 --directory builds/far-horizon-delivery
```

Open `http://localhost:8071`. The managed environment uses writable XDG paths
under `/workspace`; its web export templates are already installed.

## Verified

- A terminal vertical slice was tested and visually reviewed **before** the ship
  areas were added.
- `tests/browser_slice.py --full`: real movement, followers, leader changes,
  documents, writing, dialogue branches, modal movement lock, paper review,
  boarding, launch, saved cue restoration, four department choices, observation,
  screenplay capture, the exact ending, and JSON export.
- `tests/browser_html.py`: the delivered release HTML at 1280×720, embedded audio
  helpers, real movement/writing, save restoration, no debug globals, and a new
  class. No browser errors or external game-asset requests.
- Direct `file://` navigation was not tested: managed Chromium blocks that
  protocol. The self-contained file was verified over HTTP.

Run the tests with Python Playwright, Chromium at `/usr/bin/chromium`, and the
debug export served on port 8070 or the delivery HTML on 8071. Reports and
screenshots are under ignored `artifacts/far-horizon-tests/`.

## Art and scope

The GM bible and all 11 pages of the small Session 1 packet were reviewed. The
large visual-aid PPTX and large complete PDF exceeded the transfer limit; the
small packet resolved the opening reference requirements. Raw GM documents and
later-session reveals are excluded from the game.

Original AI-generated terminal, launch, orbit, habitation, bridge, party, and NPC
assets follow the supplied realistic industrial science-fiction references.
Walking uses eight sprite frames per department, separate idle/turn poses,
acceleration/deceleration, contact shadows, floor reflections, camera easing,
foreground trim, and atmospheric motion. These are prototype animations. Silver
Pines is the quality direction; commercial AA animation parity is not claimed.

The numbered canonical deck map and M01/M02 recordings were not supplied. The
six-area directory is provisional; ambience and effects are original procedural
assets produced by `tools/synthesize_fh_audio.py`. No Silver Pines assets are used.
