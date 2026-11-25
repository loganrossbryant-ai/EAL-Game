# The Broken Bridge

**v0.6.0 · Teacher preview · Illustrative language practice**

A storm damaged the bridge to Alder River lookout. Sound the river at two stations, compare the readings with the ford limit, and show Ranger Lin why yesterday’s notice needs correcting. Repair and load-test the bridge for visitor access, or mark the ford for the supply run and leave the bridge closed. Both routes stay within the same clearing.

## Play offline

Download the versioned **Play ZIP** or **Review ZIP** from the GitHub review branch. Extract it and double-click `Broken-Bridge-v0.6.0.html`. The Review ZIP places it in `play/` with the screenshots, videos, QA, and editable project in adjacent folders.

If your browser restricts local files, run `python3 -m http.server 8000 --bind 127.0.0.1` from the folder containing the HTML. Open `http://127.0.0.1:8000/Broken-Bridge-v0.6.0.html`. Internet access is unnecessary. Use the same address and browser when resuming a save.

Tap the trail to walk or use the arrow keys and WASD. Tap landmarks to approach, or press E nearby. Turn flags or boards with R or the field belt. The belt offers guided travel. In the bridge rig, the player must still thread, fasten and load-test the rope. **Enable sound** starts the world mix after a click or tap. Voice, ambience and effects each have a setting. Dialogue also has captions and replay.

The Field log includes a route map and an anonymous teacher JSON export. Settings provides save backup and restore, reset, Chinese support, focus view and reduced motion. Earlier saves retain their original progression rules and may resume where they left off.

## Reproduce

From `games/broken-bridge-25d-prototype/`, use Node.js 24 and Python 3.12. The lockfile pins Phaser 3.90.0 and eventemitter3 5.0.4. Chromium, Python Playwright and FFmpeg/ffprobe are needed for browser QA and recordings.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm test
npm run build
python3 -m pip install -r tests/requirements.txt
python3 tests/browser.py
BRIDGE_TEST_CASE=motion python3 tests/browser.py
python3 tests/navigation_browser.py
python3 tests/evidence.py
```

The build writes the standalone HTML and deterministic offline ZIP to `build/`. The browser scripts test the exact HTML extracted from that ZIP and write evidence to `test-results/v060/`. Set `CHROMIUM_PATH` if Chromium is installed outside `/usr/bin/chromium`. The Review ZIP supplies the matching npm tarballs and offline rebuild instructions.

[Design, changes and tool verification](visual-review/V060_HANDOFF.md) · [Art and sound provenance](visual-review/V060_ASSETS.md) · [Language-action matrix](LANGUAGE_ACTION_MATRIX.csv)

## Rollback and project scope

The v0.5 source is pinned to `58fa3490a720a2676b3d86d2c5033280ac97a1d5`. Its [standalone HTML](downloads/Broken-Bridge-v0.5.0.html) and [QA record](visual-review/V050_QA.md) remain available. Prior builds in `downloads/` support live save migration tests.

The field survey, evidence interview, rigging, pathfinding, sound mix and local packaging are implemented for this story. Native iPhone testing, textbook alignment, creative approval and reuse on another title require separate review.
