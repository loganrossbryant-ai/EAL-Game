"""Generate the v0.4 field guides while preserving the original dialogue MP3s."""

import argparse
import json
from pathlib import Path
import subprocess

from generate_kokoro import AUDIO, LANGUAGE, MODEL_FILES, SPEED, VOICE, Kokoro, digest, onnxruntime

INSTRUCTIONS = AUDIO / "instructions"


def read_instructions():
    return json.loads(subprocess.check_output([
        "node", "--input-type=module", "-e",
        "import {instructionLines} from './src/instructions.mjs'; "
        "console.log(JSON.stringify(instructionLines));",
    ], cwd=AUDIO.parent))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_dir", type=Path)
    args = parser.parse_args()
    for name, sha256 in MODEL_FILES.items():
        if digest(args.model_dir / name) != sha256:
            raise SystemExit(f"Checksum mismatch: {name}")

    onnxruntime.disable_telemetry_events()
    options = onnxruntime.SessionOptions()
    options.intra_op_num_threads = 2
    options.inter_op_num_threads = 1
    options.log_severity_level = 3
    session = onnxruntime.InferenceSession(
        str(args.model_dir / "kokoro-v1.0.onnx"), options, providers=["CPUExecutionProvider"],
    )
    engine = Kokoro.from_session(session, str(args.model_dir / "voices-v1.0.bin"))
    INSTRUCTIONS.mkdir(exist_ok=True)
    clips = {}
    for line_id, caption in read_instructions().items():
        samples, sample_rate = engine.create(caption, voice=VOICE, speed=SPEED, lang=LANGUAGE)
        output = INSTRUCTIONS / f"{line_id}.mp3"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "f32le", "-ar", str(sample_rate), "-ac", "1", "-i", "pipe:0",
            "-af", "adelay=80,apad=pad_dur=0.12,alimiter=limit=0.89:level=0",
            "-codec:a", "libmp3lame", "-b:a", "48k", "-map_metadata", "-1", str(output),
        ], input=samples.astype("<f4").tobytes(), check=True)
        duration = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(output),
        ]))
        clips[line_id] = {
            "file": output.name, "caption": caption, "sha256": digest(output),
            "duration_seconds": round(duration, 3),
        }
        print(f"{line_id}: {duration:.2f} seconds", flush=True)
    manifest = {
        "character": "Ranger Lin", "engine": "Kokoro-ONNX 0.6.1",
        "source_release": "https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0",
        "voice": VOICE, "language": LANGUAGE, "speed": SPEED,
        "model_files_sha256": MODEL_FILES, "clips": clips,
    }
    (INSTRUCTIONS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
