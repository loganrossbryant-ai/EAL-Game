# Alan’s Favorites Island — café milestone

A separate Godot **4.6.3** project in `eal-adventure/`, based on
`codex/far-horizon-session-01` at `66e5f5a`. Far Horizon, its release candidate,
notes, scripts and public root game are preserved.

This is the first playable scene for review. Other island locations have not
been built. The café has a controllable Alan, following teal robot Pip, Mina,
three food stalls, a festival table, animated characters and scenery, local
progress, optional Simplified Chinese and approved prerecorded Jesse audio.

## Play

Tap the terrace to walk, tap a stall or resident to approach and interact, or
use arrows / WASD and E / Enter. The lower-left stick also moves Alan. Dialogue
pauses movement. The Chinese button reveals short meanings and instructions.

Help Mina by listening to her favorite, collecting food, delivering it and
building the matching sentence. “We said it” records speaking participation.
Choose a personal favorite, hear its sentence, ask Pip, then visit the festival
table. The table gains food, bunting, lights and balloons. Another order rotates
through eight voiced foods without requiring mastery of the vocabulary bank.

Food stalls also provide picture–word, Chinese–English and listen-and-find
practice. Personal choices never contribute to comprehension accuracy.

## iPad / iPhone offline delivery

Use the **single-threaded Godot Web export as an installable offline web app**.
No Apple signing account, learner account, API key or runtime service is used.

1. Open the public café entry in **Safari** while connected.
2. Tap **Save for offline** and wait for **Offline ready**. All game bytes,
   pictures, fonts, music and speech are copied to that device.
3. Use **Share → Add to Home Screen**.
4. Open the island icon, enable Airplane Mode, and verify **Play with Pip**.

Landscape is recommended. The first installation requires access to the play
site; after installation no VPN or internet is needed. Website data can be
removed by the user or operating system, so check Airplane Mode before relying
on the installation. This is an offline web app, not a signed native iOS app.
An HTML file or ZIP opened directly in iOS Files is not the delivery route.

The backup ZIP contains the ordinary separate-file export and a Python standard
library local server for desktop recovery. It is not a directly installable iOS
application. Physical Safari / Home Screen verification remains necessary;
Chromium touch emulation does not establish actual iOS compatibility.

## Vocabulary, art and classroom reuse

`data/vocabulary.json` has **144 entries / 18 in each of eight topics**, imported
from pages 34–37 of the supplied Alan word cards. It stores stable IDs, exact
English and Chinese, source page, and illustration paths. Food entries include
the sentence form; the café uses these fields for words and meanings.

The café illustrates rice, noodles, dumplings, pizza, ice cream, bread, eggs,
sandwich, apple, banana, orange and strawberry in groups of four. There are 12
distinct food illustrations, including four scalable SVGs. The eight supplied
food pictures and Pip are reused from the approved HTML. New café scenery and
Alan / Mina artwork were generated for this scene. No unrelated word shares a
food illustration. The other 132 pictures are not claimed complete.

`tools/export_classroom.py` creates a self-contained black-and-white printable
café preview: separate picture, English and Chinese decks, bilingual sentence
strips, matching sets and “I say, you draw” prompts. It reads the same vocabulary
and illustrations. The supplied 144-word PDF remains the full agreed word deck.
Future illustrations can be added by stable vocabulary ID without changing the
learning records or printable workflow.

## Voice and sound

The supplied HTML contains 117 Jesse recordings. They are imported unchanged;
`data/voice.json` maps exact text to bundled MP3 files. The approved voice is
Jesse, `rLl4PSDTzX3VHL4wjSFI`. No browser speech synthesis or runtime voice API
exists in this game. The eight reusable foods have word, listen request, “My
favorite food…” and “I like…” recordings. Personal album and resident tasks use
these fully voiced foods.

Noodles, dumplings, bread and eggs are available for visual matching. A small
Jesse sample for those words and two additional lines was requested; ElevenLabs
reported busy and did not start or charge it. New recordings remain pending
sample approval. The name model and “That’s my favorite, too!” have text support
but no new recording is claimed. No substitute voice or artificial word splicing
was used. Voice/music levels and master mute are separate; replay interrupts
the previous clip, and music ducks while Jesse speaks. Music and chime are
original instrumental WAV files, generated during asset preparation and bundled.

## Progress and teacher summary

`Menu → Teacher` shows completed missions, rounds, words seen/heard/practised,
patterns, first-attempt results and items needing further practice. Speaking is
manual participation, never verified pronunciation. JSON export and a confirmed
reset are available. The browser save key is `alan-favorites-island-v1`; native
development uses `user://alan-favorites-island-v1.json`. Nothing is uploaded.

## Build and verify

From the repository root, with matching Godot Web templates installed:

```sh
godot --headless --path eal-adventure --editor --import --quit
mkdir -p builds/alan-island
godot --headless --path eal-adventure --export-release Web ../builds/alan-island/index.html
python3 eal-adventure/tools/prepare_web.py builds/alan-island
python3 -m http.server 8073 --directory builds/alan-island
```

The managed environment uses writable XDG cache, data and config paths under
`/workspace`. Use a fresh standard export before `prepare_web.py`; do not pack
Godot JavaScript or WebAssembly into a custom all-in-one HTML file.

`tests/browser_milestone.py` plays the debug export on port 8072. It verifies
actual movement, dialogue locking, retries, grammar, personal choices, Chinese,
speaking participation, saved completion, mini-games, controls and reset.
`tests/browser_touch.py` uses Chromium touch and viewport emulation for landscape
iPad, portrait iPad and landscape iPhone. `tests/browser_offline.py` tests the
exact release on port 8073, caches the full app, closes the browser process,
restarts with networking disabled, completes the mission and checks real decoded
PCM audio, separate music control and master mute. No physical iOS test is
claimed. Evidence and limitations are in `docs/verification.md`.
