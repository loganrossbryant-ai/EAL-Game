"""Record authored Far Horizon NPC lines with ElevenLabs, never student data.

The key is read from the environment on this build machine only. Nothing in
the Godot game calls ElevenLabs or contains a service credential. A complete,
validated set is required before a catalog is published into the game assets.
Run without --generate to inspect the script and proposed voice selection.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "far-horizon/assets/voices"
API = "https://api.elevenlabs.io"
MODEL = "eleven_multilingual_v2"
PREFERENCES = {
    "venn": ["Alice", "Matilda"],
    "juno": ["Jessica", "Bella"],
    "iris": ["Sarah", "Rachel"],
    "rhee": ["George", "Daniel"],
    "okafor": ["Eric", "Liam"],
}


def read_script():
    lines = json.loads((ASSETS / "dialogue.json").read_text())["lines"]
    ids = set()
    for line in lines:
        expected = line["speaker"] + "_" + hashlib.sha256(line["text"].encode()).hexdigest()[:16]
        if line["id"] != expected or expected in ids:
            raise ValueError("Stale or duplicate authored dialogue ID")
        ids.add(expected)
    return lines


def probe(path):
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name",
        "-of", "json", str(path),
    ]))
    duration = float(data["format"]["duration"])
    if not 0.35 < duration < 100 or not any(s["codec_name"] == "mp3" for s in data["streams"]):
        raise ValueError("Speech output is not a playable MP3 of a plausible duration")
    volume = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                            capture_output=True, text=True, check=True).stderr
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", volume)
    if not mean or float(mean.group(1)) < -45:
        raise ValueError("Recording is silent or too quiet to review")
    return round(duration, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true", help="Use ElevenLabs credits to record missing authored lines")
    parser.add_argument("--voice-map", type=Path, help="Optional JSON mapping of the five speaker IDs to accessible stock voice IDs")
    args = parser.parse_args()
    lines = read_script()
    print(f"Authored script: {len(lines)} clips; {sum(len(l['text']) for l in lines)} characters; five fictional NPCs.")
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("Connection needed: configure ELEVENLABS_API_KEY as a private environment secret and allow api.elevenlabs.io. No audio generated.")
    def service(path, body=None):
        headers = {"xi-api-key": key}
        if body is not None: headers["Content-Type"] = "application/json"
        request = Request(API + path, headers=headers, data=json.dumps(body).encode() if body is not None else None)
        try:
            with urlopen(request, timeout=120 if body is not None else 40) as response:
                return response.read(), response.headers.get("content-type", "")
        except HTTPError as error:
            # Do not dump request headers, tokens, or service response bodies.
            raise SystemExit(f"ElevenLabs connection failed (HTTP {error.code}). No fallback provider used.") from None

    def get(path):
        data, _ = service(path)
        return json.loads(data)

    available = get("/v1/voices")["voices"]
    by_id = {v["voice_id"]: v for v in available}
    mapping = json.loads(args.voice_map.read_text()) if args.voice_map else {}
    for speaker, preferred in PREFERENCES.items():
        if speaker not in mapping:
            match = next((v for name in preferred for v in available if v["name"] == name and v.get("category") == "premade"), None)
            if not match:
                raise SystemExit(f"No preferred stock voice available for {speaker}. Supply --voice-map with accessible stock voices.")
            mapping[speaker] = match["voice_id"]
        selected = by_id.get(mapping[speaker])
        if not selected or selected.get("category") != "premade":
            raise SystemExit(f"{speaker}: choose an accessible premade voice. Custom/cloned voices are not accepted by this script.")
        print(f"{speaker}: {selected['name']}")
    if len(set(mapping.values())) != len(PREFERENCES):
        raise SystemExit("Use a distinct stock voice for each of the five NPCs.")

    old_path = ASSETS / "catalog.json"
    old = json.loads(old_path.read_text()) if old_path.exists() else {}
    staging = ROOT / "builds/fh-elevenlabs-staging"
    receipts_path = staging / "receipts.json"
    receipts = json.loads(receipts_path.read_text()) if receipts_path.exists() else {}
    clips = {}
    missing = []
    for line in lines:
        filename = line["id"] + ".mp3"
        path = ASSETS / filename
        entry = old.get("clips", {}).get(line["id"], {})
        staged_entry = receipts.get(line["id"], {})
        staged_path = staging / filename
        if path.exists() and old.get("provider") == "ElevenLabs" and old.get("model") == MODEL and entry.get("voice_id") == mapping[line["speaker"]] and entry.get("sha256") == hashlib.sha256(path.read_bytes()).hexdigest():
            probe(path)
            clips[line["id"]] = entry
        elif staged_path.exists() and staged_entry.get("model") == MODEL and staged_entry.get("voice_id") == mapping[line["speaker"]] and staged_entry.get("sha256") == hashlib.sha256(staged_path.read_bytes()).hexdigest():
            probe(staged_path)
            clips[line["id"]] = staged_entry
        else:
            missing.append(line)
    required = sum(len(l["text"]) for l in missing)
    subscription = get("/v1/user/subscription")
    remaining = int(subscription["character_limit"]) - int(subscription["character_count"])
    print(f"Missing recordings: {len(missing)}; characters needed: {required}; account characters remaining: {remaining}.")
    if required > remaining:
        raise SystemExit("Insufficient included quota. This script will not enable overage billing.")
    if not args.generate:
        print("Plan only. Add --generate to record the authored script.")
        return

    # A failed batch leaves the previous catalog intact; partial files are never
    # represented as a complete voice pack. This directory is outside the game.
    staging.mkdir(parents=True, exist_ok=True)
    for number, line in enumerate(missing, 1):
        content, content_type = service(
            "/v1/text-to-speech/" + mapping[line["speaker"]] + "?output_format=mp3_44100_128",
            body={"text": line["text"], "model_id": MODEL,
                  "voice_settings": {"stability": 0.65, "similarity_boost": 0.75,
                                     "style": 0.05, "use_speaker_boost": True, "speed": 0.96}},
        )
        if "audio" not in content_type:
            raise SystemExit(f"Recording stopped at {line['id']}: response is not audio; no new catalog published.")
        path = staging / (line["id"] + ".mp3")
        path.write_bytes(content)
        duration = probe(path)
        clips[line["id"]] = {"file": path.name, "speaker": line["speaker"], "model": MODEL,
                              "voice_id": mapping[line["speaker"]], "seconds": duration,
                              "sha256": hashlib.sha256(content).hexdigest()}
        receipts[line["id"]] = clips[line["id"]]
        receipts_path.write_text(json.dumps(receipts, indent=2) + "\n")
        print(f"Recorded {number}/{len(missing)}: {line['speaker']} ({duration}s)", flush=True)
    if len(clips) != len(lines):
        raise RuntimeError("Incomplete voice catalog")
    for line in lines:
        path = staging / (line["id"] + ".mp3")
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == clips[line["id"]]["sha256"]:
            (ASSETS / path.name).write_bytes(path.read_bytes())
    catalog = {"provider": "ElevenLabs", "model": MODEL, "session": 1, "clips": clips}
    with tempfile.NamedTemporaryFile(mode="w", dir=ASSETS, suffix=".json", delete=False) as file:
        json.dump(catalog, file, indent=2)
        file.write("\n")
        temp = Path(file.name)
    temp.replace(old_path)
    print(f"Complete ElevenLabs catalog saved: {len(clips)} validated clips. Import and browser-test before release.")


if __name__ == "__main__":
    main()
