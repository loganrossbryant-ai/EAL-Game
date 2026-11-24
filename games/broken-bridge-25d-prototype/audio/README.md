# Ranger Lin dialogue audio

The game packages a new English Kokoro voice for Ranger Lin. The captions in [dialogue.mjs](../src/dialogue.mjs) are the exact synthesis text. Each line ID resolves to its own locally bundled MP3. The [manifest](manifest.json) records each caption, filename, duration and SHA-256. Simplified Chinese remains available as on-screen text. No existing Jesse recording is part of this change.

## Provenance and generation

The recorded assets use Kokoro-ONNX 0.6.1 with the Kokoro 1.0 model, the built-in `af_heart` voice, `en-us` G2P and speed 0.91. Generation ran on the local Linux CPU. FFmpeg 7.1.5 encoded mono MP3 at 48 kbit/s after adding brief silent lead and tail space and applying a peak limiter. The bundle contains only the generated clips. The model weights, voice embeddings and generation dependencies stay outside the game and are unnecessary for playback.

The model and voice files come from the upstream `model-files-v1.0` release. The generation script checks the exact SHA-256 values also listed in the manifest. [Model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0) · [Kokoro model license](https://github.com/hexgrad/kokoro/blob/main/LICENSE) · [Kokoro-ONNX license](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE)

Run from the prototype folder with Python 3.12, Node.js, FFmpeg and FFprobe.

```sh
python -m pip install kokoro-onnx==0.6.1
python audio/generate_kokoro.py /path/to/kokoro-model-files
```

## Audio QA

The independent local pronunciation check decodes each shipped MP3 with FFmpeg and transcribes the actual waveform with Whisper tiny.en through Sherpa-ONNX 2.0.3. It checks for a complete one-to-one mapping, exact caption equality between source and manifest, recorded file hashes, successful decoding and sane peak levels before comparing transcripts. Normalization ignores case and punctuation and accounts for the format of 38, the spelling of centimetres and word separation in lookout. The transcript check is a reproducible intelligibility check of synthetic clips. Teacher review of accent, phoneme detail, prosody and age suitability, and physical iPhone audio remain separate.

```sh
python -m pip install sherpa-onnx==2.0.3
python audio/check_pronunciation.py /path/to/sherpa-onnx-whisper-tiny.en
```

All 15 final clips passed the normalized transcript comparison, the caption/hash checks, and the FFmpeg waveform checks. A separate offline Chromium media fixture advanced playback for all 15 MP3 data URLs after a click.

The Whisper tiny.en archive used in QA has SHA-256 `2bd6cf965c8bb3e068ef9fa2191387ee63a9dfa2a4e37582a8109641c20005dd`. The model is a QA tool only, and the game never transcribes, evaluates or sends a learner's speech. [QA model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-tiny.en.tar.bz2)
