"""Check the shipped audio with an independent, local Whisper tiny.en decoder."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np
import sherpa_onnx

AUDIO = Path(__file__).resolve().parent
SAMPLE_RATE = 16000


def normalized(text):
    clean = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    clean = clean.replace("look out", "lookout").replace("centimetres", "centimeters")
    clean = re.sub(r"\b38\b", "thirty eight", clean)
    return " ".join(clean.split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_dir", type=Path, help="Extracted Sherpa-ONNX Whisper tiny.en archive")
    args = parser.parse_args()
    recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(args.model_dir / "tiny.en-encoder.int8.onnx"),
        decoder=str(args.model_dir / "tiny.en-decoder.int8.onnx"),
        tokens=str(args.model_dir / "tiny.en-tokens.txt"), num_threads=2,
    )
    manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
    captions = json.loads(subprocess.check_output([
        "node", "--input-type=module", "-e",
        "import {lines} from './src/dialogue.mjs'; console.log(JSON.stringify(lines));",
    ], cwd=AUDIO.parent))
    clips = manifest["clips"]
    assert set(captions) == set(clips), "Dialogue keys do not match the manifest"
    assert {entry["file"] for entry in clips.values()} == {p.name for p in AUDIO.glob("*.mp3")}
    results = []
    for line_id, entry in clips.items():
        clip = AUDIO / entry["file"]
        assert hashlib.sha256(clip.read_bytes()).hexdigest() == entry["sha256"], f"Checksum: {clip}"
        assert captions[line_id] == entry["caption"], f"Caption differs: {line_id}"
        decoded = subprocess.check_output([
            "ffmpeg", "-loglevel", "error", "-i", str(clip), "-f", "f32le",
            "-ar", str(SAMPLE_RATE), "-ac", "1", "pipe:1",
        ])
        samples = np.frombuffer(decoded, dtype="<f4")
        assert samples.size and np.isfinite(samples).all(), f"Invalid audio: {clip}"
        peak = float(np.max(np.abs(samples)))
        assert 0.05 < peak < 1, f"Peak is out of bounds ({peak}): {clip}"
        stream = recognizer.create_stream()
        stream.accept_waveform(SAMPLE_RATE, samples)
        recognizer.decode_stream(stream)
        observed = stream.result.text.strip()
        match = normalized(observed) == normalized(entry["caption"])
        results.append((line_id, match, observed, entry["caption"], peak))
    for line_id, match, observed, caption, peak in results:
        status = "MATCH" if match else "REVIEW"
        print(f"{status}\t{line_id}\tpeak {peak:.3f}\t{observed}")
        if not match:
            print(f"  Caption: {caption}")
    print(f"{sum(row[1] for row in results)}/{len(results)} normalized transcript matches")
    if not all(row[1] for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
