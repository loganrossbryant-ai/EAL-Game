"""Decode and independently transcribe the new standalone field guides."""

import argparse
import json
from pathlib import Path
import subprocess

import numpy as np
import sherpa_onnx

from check_pronunciation import SAMPLE_RATE, normalized
from generate_instructions import INSTRUCTIONS, digest, read_instructions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_dir", type=Path, help="Extracted Sherpa-ONNX Whisper tiny.en archive")
    args = parser.parse_args()
    manifest = json.loads((INSTRUCTIONS / "manifest.json").read_text(encoding="utf-8"))
    captions = read_instructions()
    clips = manifest["clips"]
    assert set(captions) == set(clips), "Instruction keys do not match the manifest"
    assert {entry["file"] for entry in clips.values()} == {p.name for p in INSTRUCTIONS.glob("*.mp3")}
    recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(args.model_dir / "tiny.en-encoder.int8.onnx"),
        decoder=str(args.model_dir / "tiny.en-decoder.int8.onnx"),
        tokens=str(args.model_dir / "tiny.en-tokens.txt"), num_threads=2,
    )
    matches = 0
    for line_id, entry in clips.items():
        clip = INSTRUCTIONS / entry["file"]
        assert digest(clip) == entry["sha256"], f"Checksum: {clip}"
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
        matches += match
        print(f"{'MATCH' if match else 'REVIEW'}\t{line_id}\tpeak {peak:.3f}\t{observed}")
        if not match:
            print(f"  Caption: {entry['caption']}")
    print(f"{matches}/{len(clips)} normalized instruction transcript matches")
    if matches != len(clips):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
