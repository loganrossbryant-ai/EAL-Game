"""Prepare the ordinary Godot export for review, without single-file packing.

This produces a scan candidate, not a security-cleared release. It preserves
the exported HTML/JS/WASM/PCK bytes and records every distributed file's hash.
"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "builds/far-horizon-release"
DEST = ROOT / "review-candidate/far-horizon"
NAMES = (
    "index.html", "index.js", "index.wasm", "index.pck", "index.png",
    "index.audio.worklet.js", "index.audio.position.worklet.js",
)


def prepare():
    DEST.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        shutil.copy2(EXPORT / name, DEST / name)
    licenses = DEST / "licenses"
    licenses.mkdir(exist_ok=True)
    for p in sorted((ROOT / "far-horizon").glob("GODOT-*.txt")) + sorted(
        (ROOT / "far-horizon/assets/fonts").glob("LICENSE-*.txt")
    ):
        shutil.copy2(p, licenses / p.name)
    expected = {Path(n) for n in NAMES} | {
        Path("licenses") / p.name for p in licenses.iterdir() if p.is_file()
    }
    actual = {p.relative_to(DEST) for p in DEST.rglob("*") if p.is_file()}
    if actual != expected:
        raise RuntimeError(f"Unexpected candidate files: {actual ^ expected}")
    manifest = {
        "status": "candidate-not-security-cleared",
        "format": "standard-godot-web-export",
        "engine": "Godot 4.6.3, non-threaded Web release",
        "files": [
            {"path": p.as_posix(), "bytes": (DEST / p).stat().st_size,
             "sha256": hashlib.sha256((DEST / p).read_bytes()).hexdigest()}
            for p in sorted(actual)
        ],
    }
    (DEST.parent / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(actual)} separate, hashed files; no scan clearance claimed.")


if __name__ == "__main__":
    prepare()
