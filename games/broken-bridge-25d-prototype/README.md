# The Broken Bridge

**v0.3.0 · Playable teacher review candidate**

A storm has damaged the bridge to Alder River lookout. Walk the riverbank, compare physical clues and report a plan to Ranger Lin. Fit two boards and secure their rope to reopen the bridge, or rotate and place markers along the white-stone ford and move the supply pack. The crossing you prepare becomes walkable and determines how the ranger delivers the supplies.

Elementary and middle school share the same forest, evidence and physical solutions. Elementary offers shorter supported English and Simplified Chinese glosses. Middle school asks for a contextual question, an evidence-backed recommendation and optional comparative reasoning. The language matrix is illustrative. Speaking practice is self-reported participation.

## Play locally

For future review builds, provide the standalone HTML first so the reviewer can open it directly in a browser. The ZIP is an optional companion.

Download [Broken-Bridge-v0.3.0.html](downloads/Broken-Bridge-v0.3.0.html) and open it in your browser. If your browser blocks local files or restricts save storage, serve that same file locally.

From the folder containing the HTML, run `python3 -m http.server 8000 --bind 127.0.0.1` and open `http://127.0.0.1:8000/Broken-Bridge-v0.3.0.html`. Internet access is unnecessary.

Choose a language guide. Click or tap the trail and landmarks to move, or use the arrow keys or WASD. Press E near an object to interact. After Lin authorizes the route, tap a piece and walk it to the matching socket or stone. The field action button provides a touch and keyboard alternative and walks you to the relevant anchor. Press R or use Turn marker clockwise to orient a flag.

Use the same address and browser to resume. The Field log contains collected observations, landmark directions and the teacher JSON export. Settings offers save backups, restore, reset, Chinese support, focus view, reduced motion and optional sound effects. Use Replay Ranger Lin to hear locally bundled Kokoro dialogue. Captions remain visible. See the [audio manifest and evaluation](audio/README.md).

## Develop and verify

From this folder, with Node.js and Python 3:

```sh
npm ci --ignore-scripts
npm test
npm run build
python3 tests/browser.py
```

The browser suite uses Python Playwright and Chromium. Set `CHROMIUM_PATH` if Chromium is installed elsewhere. The build writes the single-file HTML and deterministic ZIP to `build/`. Browser screenshots land in `test-results/`. See [v0.3 visual QA and screenshots](visual-review/V030_QA.md), [change log](visual-review/CHANGELOG.md), [asset provenance](visual-review/ASSET_PROVENANCE.md), and the [archived v0.1.0 test record](TOOL_SELECTION_AND_QA.md).

## Reusable systems

| System | What carries forward |
|---|---|
| World controller | Phaser Canvas rendering, camera projection, keyboard and targeted touch walking, riverbank traversal limits, proximity interactions and DOM modal pause |
| Content profiles | Authored clue records, language scaffolds and route requirements over a shared world |
| Dialogue and evidence | Deterministic NPC responses, cited observations, recoverable plan rejection and hint progression |
| Physical tasks | Ordered persistent pieces with drag and accessible select-then-place inputs, plus rotation checks |
| Learning records | Versioned local save, portable backup/restore and a separate anonymous teacher export |
| Offline build | Single embedded HTML, reproducible ZIP and browser tests against the exact extracted bytes |

The source handoff is in [CODEX_START_HERE.md](CODEX_START_HERE.md), [DESIGN_BRIEF.md](DESIGN_BRIEF.md) and the [language-action matrix](LANGUAGE_ACTION_MATRIX.csv).

The frozen [v0.2 standalone HTML](downloads/Broken-Bridge-v0.2.0.html) and its [visual QA](visual-review/QA.md) remain available for comparison.
