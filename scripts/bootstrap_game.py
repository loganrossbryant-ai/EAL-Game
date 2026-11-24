#!/usr/bin/env python3
"""Non-destructive game planning scaffold. This is NOT an approved playable engine."""
from pathlib import Path
import argparse
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
COPIES = {
    "NEW_GAME_BRIEF.md": "DESIGN_BRIEF.md",
    "CURRICULUM_ACTION_MATRIX.csv": "CURRICULUM_ACTION_MATRIX.csv",
    "ART_ASSET_MANIFEST.csv": "ART_ASSET_MANIFEST.csv",
    "AUDIO_LINE_MANIFEST.csv": "AUDIO_LINE_MANIFEST.csv",
    "QA_REPORT.md": "QA_REPORT.md",
}

def bootstrap_game(root: Path, slug: str, title: str, audience: str) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 56:
        raise ValueError("Slug must be lowercase ASCII letters, digits, hyphens, <=56 characters")
    if audience not in ("school", "tutoring"):
        raise ValueError("Audience must be school or tutoring")
    if not title.strip():
        raise ValueError("Title cannot be blank")
    relative = Path("games") if audience == "school" else Path("tutoring-games/games")
    dest = root / relative / slug
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing work: {dest}")
    templates = root / "studio/templates"
    for name in COPIES:
        if not (templates / name).is_file():
            raise FileNotFoundError(f"Missing canonical template: {templates / name}")
    dest.mkdir(parents=True, exist_ok=False)
    try:
        for name, target in COPIES.items():
            shutil.copyfile(templates / name, dest / target)
        (dest / "README.md").write_text(
            f"# {title.strip()}\n\n"
            f"**Status: DESIGN / WORKING — NOT a playable or approved build**\n\n"
            f"Audience: {audience}\n\n"
            "Engine: NO APPROVED REUSABLE ENGINE YET. Do not claim inherited visual "
            "or technical quality. Read ../../studio/README.md from the repo root; "
            "for tutoring also read scoped tutoring-games/AGENTS.md.\n\n"
            "## Required next steps\n"
            "1. Verify exact curriculum sources privately. Keep scans and student identities off public GitHub.\n"
            "2. Fill DESIGN_BRIEF.md and CURRICULUM_ACTION_MATRIX.csv.\n"
            "3. Create original art, animation and voice manifests with actual assets and source hashes.\n"
            "4. After an APPROVED engine exists, import its exact version and retain a source SHA. "
            "Until then this folder is a planning scaffold only.\n"
            "5. Validate the one-location playable vertical slice using studio/templates/QA_REPORT.md, "
            "real screenshots/video and classroom/device gates.\n",
            encoding="utf-8",
        )
    except Exception:
        shutil.rmtree(dest)
        raise
    return dest

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--audience", required=True, choices=("school", "tutoring"))
    parser.add_argument("--create", action="store_true", help="actually create files (default: dry-run)")
    args = parser.parse_args()
    relative = "games" if args.audience == "school" else "tutoring-games/games"
    if not args.create:
        print(f"DRY RUN only: would create {relative}/{args.slug} using canonical templates.")
        print("Will NOT create working gameplay, engine, art, narration or student-ready releases.")
        return
    dest = bootstrap_game(ROOT, args.slug, args.title, args.audience)
    print(f"CREATED planning scaffold: {dest.relative_to(ROOT)}")
    print("ENGINE NOT APPROVED; user creative approval and full QA still required.")

if __name__ == "__main__":
    main()
