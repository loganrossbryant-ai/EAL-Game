---
name: release-tutoring-game
description: Test, package and promote a tutoring game's browser/mobile/offline release with measurable curricular, visual, audio and device QA, rollback, and truthful readiness labels.
---

# Release tutoring game

Apply `tutoring-games/standards/RELEASE_GATE.md` and the current game's design brief. A passing script alone is insufficient.

1. Record exact source commit, branch, approved reference/version and intended audience/device.
2. Run static code and asset integrity checks plus reference validator; capture command output and hashes. Never use reference validator as a replacement for new-game tests.
3. Execute **every required game round via actual browser controls**, including wrong answers, hint/help, progression, return navigation, save/restore, reset and finale. Record tested counts, not estimated totals.
4. Inspect representative screenshots on supported sizes including narrow phone; ensure original visual quality, color assets, Chinese, sentence frames, prompts and buttons are not clipped.
5. Inventory required recorded prompts and inspect exact text-to-audio mapping, approved voice, play/replay functionality and missing audio. If essential audio is missing, do not mark independent home-ready.
6. Build separate desktop/HTML and supported PWA/offline variants without overwriting old release. Test cache scoping, update path, versioned saving and cold offline restart.
7. Verify actual HTTPS link loads from an external browser; if claiming iPhone/WeChat readiness, perform and document a **physical iPhone** Safari/Home Screen and WeChat test including offline mode. Simulations are not physical tests.
8. Fill `tutoring-games/templates/QA_REPORT_TEMPLATE.md`, changelog and rollback instructions. State PASS/FAIL/NOT TESTED for all four release gates. Use CLASSROOM PILOT if home evidence is missing.
9. Only promote to a parent-facing URL after all home-release gates pass and the user approves any consequential replacement of an existing public build.
