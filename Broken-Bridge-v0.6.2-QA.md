# Broken Bridge v0.6.2 audio review

Codex implementation review, 25 November 2026. **Teacher preview.**

- Source commit `4862cd68e1e30f0f2af7641c3d2307f309d2e7fa` on `codex/broken-bridge-v0.6.2-source`
- Playable HTML SHA-256 `c2e6a4d515c39e080c6ce2b8d18dc0eaa02411017d06d0ddcb0c0aae05a25c4f`
- Play ZIP SHA-256 `6a030f5354bde21cac3d41bf963a33339d85c0ece5cdef4963f1c577c1b0875d`
- Comparison build v0.6.1 from review commit `3166c9c5143cf7dbafec2e26922efa28a206e628`, HTML SHA-256 `d2a70bae0a1432ad061bfef8148c8df420d9778fe044dfbd43e03ab15845af0c`

| Check | Result | Evidence |
| --- | --- | --- |
| Voice priority | **PASS** | Matched opening-line playback in Chromium measured ambience 15 dB lower before speech than v0.6.1. During speech, the new ambience bus measured 26 dB below voice. The bed returned after the line. These are RMS observations from the actual buses at the same location. `qa/audio-mixer-review.json`, `evidence/audio-mixer-preview.mp4`. |
| Audio controls and saved settings | **PASS** | Tested labelled master, voice, ambience, effects, and music levels. The master slider and switch silenced output, music and ambience faders reached silence, voice at zero gave feedback, and effects played in isolation. Preference restoration was checked after reload. Actual keyboard and touch input worked in 390×844 and 844×390 simulations. `qa/audio.log`, `qa/mixer.log` and the three mixer screenshots. |
| Optional score | **PASS** | Music began off and only started after opt-in with sound enabled. The 50-second original loop has verified PCM format, checksum, unclipped peak, and a smooth recorded sample join. When the preview line played, both the music and ambience buses attenuated. The video contains actual browser mixer audio. `qa/audio-streams.log`, `audio/music/manifest.json` in source. |
| Gameplay, saves and scene regression | **PASS** | 21 unit tests, four complete offline desktop and phone-size playthroughs, and three older-save migrations. Verified both routes, captions and recorded voice replay, teacher export, and reset. River motion passed the focused texture and reduced-motion test. `qa/unit.log`, `qa/browser.log`, `qa/river.log`. |
| Reproducible offline artifact | **PASS** | Clean source, verified bundled npm tarballs, and offline dependency install reproduced the exact game HTML and Play ZIP bytes. `qa/source-rebuild.log`, `SOURCE-SHA.txt`, `SHA256SUMS.txt`. |
| Literal local-file opening in managed Chromium | **FAIL in this environment** | Administrator policy blocks `file:` navigation. Tests launched the exact HTML at a loopback origin with external requests denied. The ZIP includes localhost launch instructions. `qa/local-file.log`. |
| Native iPhone audio and listening review | **NOT TESTED** | Device emulation verifies the settings and playback in Chromium. Physical iPhone audio and teacher listening approval remain separate. |

The comparison used the same opening voice clip and a parked character at the ranger clearing. Playback evidence was recorded at 1366×768 in Chromium 156 on Debian Linux. The audio is the live game output. For the composition, defaults, and ducking details, see `visual-review/V062_AUDIO.md` in the editable source.
