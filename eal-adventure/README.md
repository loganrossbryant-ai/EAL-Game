# Alan’s Favorites Island — expanded festival collection

Separate Godot 4.6.3 project in `eal-adventure/`, based on Far Horizon `66e5f5a`.
Far Horizon source, reviewed build and existing public root game are preserved.

## What is playable

**All 144 agreed entries are reachable in activities: 18 per topic.** The bank is
connected to real scene controls and resident requests rather than just stored
in JSON. Five settings link the eight topics:

| Setting | Resident | Topics | Festival purpose |
| --- | --- | --- | --- |
| Seaside café | Mina | Food | Prepare the festival table |
| Animal sanctuary | Ari | Animals | Prepare the animal parade display |
| Sports park | Max | Sports, activities | Plan games and activity choices |
| Story square | Luna | Entertainment, people | Build the festival story wall |
| Art garden | Zoe | Colors, places | Decorate lanterns and the festival map |

The **Island trail** button is visible in the opening greeting and café. Alan
walks to a location on the island map, explores its setting, reads a resident’s
note, collects and delivers an illustrated card, builds a matching sentence and
makes his own choice. Four choices appear in an ordinary round. The picture
shelves and personal pages also let him browse all eighteen words in that topic,
with four per page. Resident replays cycle through all eighteen entries. One
helpful mission per topic earns a festival stamp; mastering all 144 is not a gate.

Controls: tap paths / residents / shelves, use the touch stick, or arrows / WASD
and E / Enter. Dialogue pauses movement. Wrong comprehension matches allow gentle
retries. Personal preferences have no wrong answer. “We said it” records manual
participation, never pronunciation accuracy.

## Chinese policy

The **操作** button supplies navigation and control instructions only. It cannot
reveal Chinese meanings of target words or preference sentences in resident
notes, collecting, ordinary picture–word matching, sentence building, speaking
or personal albums. This applies even when a saved Chinese-help setting is on.

Target-word Chinese appears only in a clearly labelled **Translation game**.
Translation support used before a comprehension attempt is logged separately
from navigation help, so the teacher can interpret accuracy correctly. Classroom
Chinese decks and bilingual strips are intended for explicit translation work.

## Vocabulary and artwork

`data/vocabulary.json` keeps the exact 144 English/Chinese entries and source-page
references from the supplied word-card PDF. Stable IDs distinguish, for example,
food orange from color orange. Every entry has a resolving, distinct local
illustration, sentence form and word chunks. The original approved pictures are
retained where appropriate; new scalable SVG illustrations cover the expanded
collection. Four new scenic environments and four resident sprites complement
the existing café, Alan and Pip.

`tools/draw_vocabulary.py` builds the additional SVGs and grammar data.
`tools/export_classroom.py OUTPUT.html --all-topics` produces the complete
self-contained printable decks. The full PDF has fifty A4 pages. Use crayons or
real colored objects for color meanings when printing in black and white.

## Voice coverage

The 117 approved Jesse clips from the supplied HTML remain byte-identical.
The voice is Jesse, `rLl4PSDTzX3VHL4wjSFI`. Existing exact clips are reused for
words, preference sentences and common feedback. Vocabulary selection is **not
restricted to those clips**.

New words also appear in written resident notes, picture–word matching,
translation and sentence building. Additional Jesse recordings remain pending:
the approval-sample generation did not start because ElevenLabs reported busy.
No bulk dialogue was generated, no alternate voice or browser speech synthesis
was substituted, and no word fragments were spliced. Unrecorded lines have no
silent replay button and do not increment “heard” counts. Voice and music have
separate controls, with replay, master mute and music ducking.

## Offline iPad / iPhone

Open the entry in Safari, choose **Save for offline**, wait for **Offline ready**,
then **Share → Add to Home Screen**. Open the island icon and test Airplane Mode.
The non-threaded Godot Web export bundles every image, font, recording and music
file. No learner account, API key, CDN or runtime voice service is required.

For an already installed old build, use the `update.html` entry once. It downloads
the complete new pack, checks that the new worker controls the page, then enables
play. Saved progress is retained. Old Alan caches are removed only after the new
pack is complete; other classroom data is untouched. A backup ZIP includes the
ordinary separate-file export and Python standard-library desktop recovery
server. It is not a signed native iOS app or a ZIP that runs directly in Files.

Physical iOS Safari/Home Screen behavior remains unverified. Browser touch
emulation and a cold offline restart are tested separately and do not replace
an adult’s Airplane Mode check on Alan’s actual device.

## Progress and teacher review

Menu → Teacher shows available / encountered / practised vocabulary by topic,
completed missions, festival stamps, patterns, first-attempt accuracy, translation
support, further practice and manual speaking participation. Export and confirmed
reset are local. The existing `alan-favorites-island-v1` save key is migrated
without deleting the learner’s favorites or past practice.

## Build

```sh
godot --headless --path eal-adventure --editor --import --quit
mkdir -p builds/alan-island
godot --headless --path eal-adventure --export-release Web ../builds/alan-island/index.html
python3 eal-adventure/tools/prepare_web.py builds/alan-island
python3 -m http.server 8093 --directory builds/alan-island
```

Use matching Godot 4.6.3 Web templates. The managed runtime uses writable XDG
paths under `/workspace`. Always start `prepare_web.py` with a fresh standard
export. JavaScript, WebAssembly, game data and audio helpers stay separate.

Current browser tests are `browser_expanded.py` (all 144 reachable entries,
Chinese boundaries and all topic missions), `browser_milestone.py` (café negative
cases and reset), `browser_offline.py` (exact release and cold offline play),
`browser_touch.py` (iPad/iPhone emulation) and `browser_update.py` (real old-pack
installation upgraded without losing its save). Reports are in `docs/`.
