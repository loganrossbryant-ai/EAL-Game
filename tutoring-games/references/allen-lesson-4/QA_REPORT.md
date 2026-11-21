# Allen Lesson 4 — Zig Language-Only Revision QA

## User-directed scope
The five-world, full-color sci-fi game is NOT redesigned. The required language now exclusively emphasizes **FOOD, PLACES and ACTIVITIES**; animal/sport/color mini-game targets were replaced. All **54 featured vocabulary entries** (18 per category) are accessible in the optional atlas. The original broader word data and art remain archived inside the HTML without being required in this version.

## What was updated
- Every phonics, identification, sorting, phrase, sentence, reading, reason, interview, and finale question bank now draws from the new three-category focus.
- First-world phonics uses new words and displays a meaningful sentence such as **I like soup because it is warm** in the question itself.
- Every one of 128 rounds gates advancement behind a **CORE short sentence, STRETCH complete reason, or teacher-practice** self-report. No microphone accuracy is claimed.
- Clue Rescue covers food, places and activities with yes/no questions and reason sentences.
- The Holo Scanner now uses contextual two-clue inference instead of showing the target word.
- Pip's reading text is a new six-sentence food/place/activity passage and eight meaning/evidence questions. It is **not claimed to be identical to the printed Lesson 4 Pip reader**; this focused game overrides that older text at the user's direction.
- Radio Interview uses WHAT and WHY exchanges and 8 rounds of real favorite + sensible reason selection.
- Finale tests correct *it is / they are*, linked ideas with *and/but*, and reason clauses; all targets are the new themes.
- Local save key uses a new namespace to avoid confusing earlier progress and to allow Allen to play this new language path from the beginning.

## Test evidence
- Actual Chromium browser control runs: **56/56** rounds in the first seven game modes and **72/72** in the remaining nine, total **128/128** passed prior to the final small instructional and reset fixes.
- After the final fixes, the Sound Moon smoke test, 5/5 final flight checkpoints including wrong-answer retries, teacher dashboard, and reset behavior were rerun successfully.
- Browser exercise validated CORE/STRETCH choice gate and progress counters, and verified mobile 390px viewport had no horizontal overflow in all exercised rounds.
- JavaScript syntax passed `node --check`; no game JavaScript page exceptions were observed in the final smoke test. Headless Chromium had intermittent audio-device warnings; this is not a real-device audio test.
- Original embedded media byte strings unchanged: **397 image/audio URLs**: {'image/webp': 152, 'image/png': 5, 'audio/mpeg': 240}. Original 240 Jesse MP3 recordings remained intact.
- ZIP files and required PWA assets were checked for integrity. Cache cleanup namespaced to the new build only.

## Still unverified / not yet release-certified
1. Many newly written English prompts are not voiced. All 240 existing Jesse MP3s are preserved; the new exact lines must be recorded using the approved Jesse voice and embedded before claiming fully independent audio support.
2. New HTTPS PWA deployment, cold-offline service-worker restart, iPhone Safari and WeChat access are **not certified** here.
3. Tapping 'I said CORE/STRETCH' is self-report only, NOT speech recognition or pronunciation assessment.
4. Actual Grade 1 independent usability and time-on-task require a child/device pilot. The new reading is deliberately more challenging and has Chinese support.

**Release status:** browser-tested content prototype ready for tutor review. **Not yet approved as fully narrated or WeChat/iPhone install-ready**.
