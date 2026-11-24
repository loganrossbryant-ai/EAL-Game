"""Produce the game's caption-matched Ranger Lin MP3s locally with Kokoro."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from kokoro_onnx import Kokoro
import onnxruntime

AUDIO = Path(__file__).resolve().parent
MODEL_FILES = {
    "kokoro-v1.0.onnx": "7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5",
    "voices-v1.0.bin": "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}
VOICE = "af_heart"
LANGUAGE = "en-us"
SPEED = 0.91


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_dir", type=Path, help="Kokoro-ONNX v1.0 model and voices directory")
    args = parser.parse_args()
    for name, sha in MODEL_FILES.items():
        if digest(args.model_dir / name) != sha:
            raise SystemExit(f"Checksum mismatch: {name}")

    captions = json.loads(subprocess.check_output([
        "node", "--input-type=module", "-e",
        "import {lines} from './src/dialogue.mjs'; console.log(JSON.stringify(lines));",
    ], cwd=AUDIO.parent))
    onnxruntime.disable_telemetry_events()
    opts = onnxruntime.SessionOptions()
    opts.intra_op_num_threads = 2
    opts.inter_op_num_threads = 1
    opts.log_severity_level = 3
    session = onnxruntime.InferenceSession(
        str(args.model_dir / "kokoro-v1.0.onnx"), opts, providers=["CPUExecutionProvider"],
    )
    engine = Kokoro.from_session(session, str(args.model_dir / "voices-v1.0.bin"))
    clips = {}
    for line_id, caption in captions.items():
        samples, sample_rate = engine.create(caption, voice=VOICE, speed=SPEED, lang=LANGUAGE)
        output = AUDIO / f"{line_id}.mp3"
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
    (AUDIO / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
