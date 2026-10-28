# First-location validation

Validated in the managed cloud machine with Node 24.19.0, npm 11.9.0, and system Chromium. Browser tests create isolated contexts. No student profile or external accounts were used.

- Frozen-lockfile reinstall: `npm ci --no-audit --no-fund` — passed.
- State and assessment: `npm test` — 12 tests passed; no skips (9 state/assessment and 3 downloadable-artifact regressions).
- Production bundle: `npm run build` — passed. Vite reports the expected large Phaser bundle warning; no build errors.
- Physical gameplay: `npm run test:movement` — passed. WASD, arrows, collision, click walking, all five newsroom targets, E interaction, and modal pause; no uncaught browser errors.
- Story flow: `npm run test:browser` — passed. Actual mouse-driven approach to NPC and evidence; campaign tabs; first failed submission and successful revision; saved draft restoration; courtyard completion and return after reload; JSON download; Chinese glossary; mobile overflow and Escape dismissal; no uncaught browser errors.
- Screenshots visually inspected: desktop newsroom, campaign website, completed editorial note, mobile layout, courtyard.

Corrections made during validation: fixed saved courtyard initialization to wait for scene readiness, retained previously earned completion while editing a new draft, and used Phaser Canvas for reliable rendering on software-only browsers.

Screenshots are in ignored `test-results/`. The development server is started separately using the instructions in DEVELOPMENT.md. A fresh-task restore/publication has not been tested. Text-to-speech is browser/OS dependent; full transcripts remain available. Real classroom use, teacher scoring, and precise alignment to original textbook pages remain outside this first milestone.

Download follow-up: fixed replacement-string expansion in the offline packager, which had corrupted literal dollar sequences inside bundled JavaScript and caused a blank page. `npm run test:demo` now serves the exact downloadable HTML bytes and runs the full student journey without Vite transforms or separate asset requests. The corrected artifact passes. Managed Chromium blocks direct file URLs, so local-file navigation itself was not tested in that managed browser.
