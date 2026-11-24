# v0.4 spoken field guides

Seven optional English field guides are bundled as MP3s. Each clip uses the exact caption in [instructions.mjs](../../src/instructions.mjs). The [manifest](manifest.json) maps line IDs to captions, file hashes and durations.

| ID | Intended use |
|---|---|
| `guideControls` | Walk and approach objects by touch or keyboard |
| `guideBoard` | Collect, carry and place one board at a time |
| `guideRope` | Hook the rope and pull it tight at the second cleat |
| `guideFord` | Orient the two flags and deliver the pack |
| `guideEvidence` | Inspect and select observations that support the chosen route |
| `guideElementary` | Build a short observation with the word bank or original words |
| `guideMiddle` | Write an evidence-linked recommendation |

Generation used Ranger Lin’s existing Kokoro v1.0 `af_heart` configuration without changing the 15 v0.3 MP3s. The [original audio documentation](../README.md) records source links and dependencies. The new manifest includes the same pinned model and voice-file SHA-256 values. The models are required for development checks only. The game uses local audio and captions. No Jesse audio was replaced.

## Checks

- All seven new caption mappings, file hashes, and finite waveform and peak-level checks passed.
- Local Whisper tiny.en independently transcribed the seven MP3s with seven normalized caption matches. This tests intelligibility of the delivered synthetic clips. A human review of accent, pronunciation and prosody remains pending.
- All seven new MP3 data URLs advanced playback after a replay click in an offline Chromium media fixture.
- All 15 existing clips still match their recorded SHA-256 values, and the existing pronunciation checker passed 15 out of 15.
- Physical iPhone playback remains untested. The offline media fixture checks audio bytes and browser decoding. In-game button routing requires separate gameplay evidence.

To regenerate or verify the new clips, run these commands from the prototype folder after installing the dependencies described in the [original audio documentation](../README.md).

```sh
python audio/generate_instructions.py /path/to/kokoro-model-files
python audio/check_instruction_audio.py /path/to/sherpa-onnx-whisper-tiny.en
```
