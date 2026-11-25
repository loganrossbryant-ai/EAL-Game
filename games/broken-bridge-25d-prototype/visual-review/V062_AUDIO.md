# Audio mix in v0.6.2

The river, breeze, wildlife, and cabin were close to Ranger Lin’s voice level in the previous package. The default mix now puts spoken dialogue in front. In a matched Chromium playback of the opening line, the quieted background also fades down when the voice starts and gradually returns on completion.

## Controls

Open **Settings → Audio** for five 0–100 sliders. The default percentages are Master 100, Voice 100, Ambience 22, Sound effects 65, and Music 24. **Enable sound** activates the master bus after a gesture. Each group has its own switch. **Preview Ranger Lin** plays her opening clip while the mixer is open. Captions remain in the dialogue panels.

The music switch starts off. The track plays only when music and the master sound are enabled. Sliders and switches are saved with the mission and included in save backups. Older saves adopt the default levels while retaining the switches they already saved.

## Original music and mix

**Alder River Clearing** is an original 50-second loop made for this scene. Sparse plucked strings, breathy flute, low open fifths, and soft reflections suit the woodland clearing and leave space for speech. The asset is rendered locally by `audio/compose_music.py` with a fixed seed. It is bundled as mono 22.05 kHz PCM. The manifest in `audio/music/` records the asset’s hash and origin.

Web Audio uses four channel faders and a master fader. The ambience, music, and effects attenuation envelopes sit downstream of their individual faders. During dialogue those envelopes reduce ambience to 16% of its set level, effects to 34%, and music to 14%. The envelopes return gradually. Changing a fader or changing a switch updates the mix immediately. Music decoding begins when the music is requested. The existing recorded dialogue files are used directly.

| Requirement | Choice and cost | Acceptance evidence |
| --- | --- | --- |
| Audible dialogue | Lower ambience floor and fast speech-triggered attenuation, using local Web Audio. | Real bus measurements from the same clip in v0.6.1 and v0.6.2, plus the final game-output recording. |
| Usable levels | Native labelled range controls with live updates and saved values. | Desktop and both simulated phone orientations, keyboard and touch input, master and per-channel silence checks, reload. |
| Scene music | Original locally synthesized soundtrack with a circular tail and file manifest. | SHA-256, exact 50-second render, peak and loop-join checks, audible opt-in and ducking. |

Run `python3 tests/audio_browser.py` after building. Add `--baseline-html path/to/Broken-Bridge-v0.6.1.html --record` to measure the earlier mix and record the final mixer output. Physical iPhone audio and teacher listening approval remain separate.
