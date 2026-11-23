# The Broken Bridge

**v0.1.0 · Playable teacher-review build**

A storm has damaged the bridge to Alder River lookout. Walk the riverbank, compare physical clues and report a plan to Ranger Lin. Fit two boards and secure their rope to reopen the bridge, or rotate and place markers along the white-stone ford and move the supply pack. The crossing you prepare becomes walkable and determines how the ranger delivers the supplies.

Elementary and middle school share the same forest, evidence and physical solutions. Elementary offers shorter supported English and Simplified Chinese glosses. Middle school asks for a contextual question, an evidence-backed recommendation and optional comparative reasoning. The language matrix is illustrative. Speaking practice is self-reported participation.

## Play locally

1. Extract [Broken-Bridge-v0.1.0-Offline.zip](downloads/Broken-Bridge-v0.1.0-Offline.zip).
2. From the extracted folder run `python3 -m http.server 8000 --bind 127.0.0.1`.
3. Open `http://127.0.0.1:8000/Broken-Bridge-v0.1.0.html` in your browser. Keep the terminal open while playing. Internet access is unnecessary.
4. Choose a language guide. Click or tap the trail and landmarks to move, or use the arrow keys or WASD. Press E near a landmark to interact. In the work area, drag a piece to its destination or select the piece and then the target.

Use the same address and browser to resume. The Field log contains collected observations, landmark directions and the teacher JSON export. Settings offers save backups, restore, reset, Chinese support, focus view, reduced motion and optional sound effects. Approved narration is pending.

## Develop and verify

From this folder, with Node.js and Python 3:

```sh
npm ci --ignore-scripts
npm test
npm run build
python3 tests/browser.py
```

The browser suite uses Python Playwright and Chromium. Set `CHROMIUM_PATH` if Chromium is installed elsewhere. The build writes the single-file HTML and deterministic ZIP to `build/`. Browser screenshots land in `test-results/`. See [the QA record](TOOL_SELECTION_AND_QA.md) for test coverage and outstanding gates.

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
