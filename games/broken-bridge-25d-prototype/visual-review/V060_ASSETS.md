# v0.6 asset provenance

## Original illustrations

ChatGPT ImageGen used the existing, original Alder River plate `originals/exec-352d35e3-5b2d-4e73-ab53-8ed54f01d44e.png` for palette, perspective and late-afternoon lighting. The new 1536 × 1024 source is `originals/exec-4860558b-8d71-457a-8c87-a7a3872f294f.png` (SHA-256 `a7d62c75625813cc6c573a6a4fd36a4940f54bb84a3489d7a471b8553a50eec5`). The prompt asked for six isolated chroma-keyed prop cutouts with no typography, exactly one per cell. Palette and visual identity remain specific to this original clearing.

| Runtime image(s) | Origin and edits | Placement |
| --- | --- | --- |
| `wind-fern.webp`, `wind-reed.webp`, `wind-fir.webp`, `wind-cedar.webp` | Keyed sprites from the v0.6 sheet. Removed chroma spill and tightened crop. | Individual foreground and bank vegetation and separate evergreen boughs. Each has an attachment pivot, motion period, and scene depth. |
| `survey-winch.webp`, `bridge-rig.webp` | Keyed ranger instrument and rigging sheet cells. Real controls and changing probe/rope overlays are rendered in the interface. | Gauge and rope close-ups. |
| `stream-amber.webp`, `stream-jade.webp`, `stream-wake.webp` | Registered water crops from the v0.5 plate, mirrored and feathered at edges. | Independently advected surface details over the painted river. |
| `ridge-mist.webp` | Low-contrast ridge mist lifted as an alpha matte from the v0.5 plate. | Three drift planes at different depths. |
| `survey-water.webp`, `trail-overview.webp` | Crops of the original v0.5 plate. | Instrument view and map. |

`python3 visual-review/prepare_v060.py` rebuilds these derivatives from the two supplied originals. Existing authored imagery, animated scout and ranger, bridge states and art history remain in the source tree. Earlier provenance is in [ASSET_PROVENANCE.md](ASSET_PROVENANCE.md), [V030_ART.md](V030_ART.md), [V040_ART.md](V040_ART.md) and [V050_QA.md](V050_QA.md). Art is original game material, distributable as part of the project. No reference game’s artwork was imported.

## Audio

The original 15 Lin clips and seven field guides retain their binary hashes and caption manifests. Six new full lines use the same local Kokoro v1.0 `af_heart` voice and en-US configuration. The source, model and voice hashes are recorded in `audio/field-dialogue/manifest.json`. Reference-title Jesse audio remains in its archive. All 28 game voice recordings are packaged locally with replay and captions.

`audio/produce_soundscape.py` renders 22 original cues and loops to PCM WAV with a fixed seed. The river surface, tree breeze, sparse wildlife, and cabin timber creaks have separate loop and gain envelopes. Gravel, wood and stone footsteps each have three variants. Board, rope, bridge, instrument, splash, notice, and handoff effects have distinct envelopes. `audio/world/manifest.json` lists all 22 files, lengths and SHA-256 values. These are original synthesized sound assets, packaged for distribution with the game. The runtime uses authored audio files with gain, spatial blend and stereo pan. It does not depend on network requests to play back speech or effects.

To rerender or check dialogue, use [audio/README.md](../audio/README.md) with `audio/generate_field_dialogue.py` and `audio/check_field_dialogue.py`. The voices and model are Kokoro/ONNX assets under the upstream open-source terms linked there. The generated voice waveforms are included; model files are only needed for regeneration and transcribing test audio. The review archive's SHA-256 manifest inventories its source and evidence files.
