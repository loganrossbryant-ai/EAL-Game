# Mandatory game release gate

Document PASS, FAIL, NOT TESTED, with evidence location for every item. **Do not silently promote a missing test to PASS.**

| Gate | Required evidence | Failure consequence |
|---|---|---|
| A. Curriculum alignment | Latest lesson and language matrix; required word/grammar coverage from first world through ending; fair questions; CORE/STRETCH/teacher supports; qualified readability | Cannot claim aligned |
| B. Gameplay/visual | Full mandatory path with wrong-answer retry, controls, images, transitions, save/reset, dashboard, ending; desktop/mobile screenshots compared with approved reference | Cannot claim tested game |
| C. Audio/independence | Exact line/audio asset manifest, playback tests, child-relevant instructions, Chinese text rendering; no invented pronunciation scores | If required audio missing: not independently home-ready |
| D. Delivery/device | Artifact integrity, exact deployed URL, online launch, cold offline reload, iPhone Safari/Home Screen + WeChat path where relevant; cache compatibility and rollback verified | If target device untested: not parent-release-certified |

## Allowed labels
- **DESIGN / WORKING** — source and incomplete build; not for students.
- **TEACHER PREVIEW** — content can be inspected; no claim of full path completion.
- **CLASSROOM PILOT** — content and browser path tested; tutor can assist; unresolved audio/device checks disclosed.
- **HOME RELEASE** — all mandatory gates passed including required audio and real target-device testing.

## Evidence record
- Source commit, branch, release version, date; source checksum and artifact SHA-256
- Updated vocabulary/grammar counts, core/stretch matrix, sampled sentence examples
- Automated scripts and precise totals: not merely “all tests passed”
- Test devices/OS/browser, screenshots, video if useful
- Recorded voice IDs, audio file hashes and any missing lines
- Known exclusions or deliberate curriculum differences
- Exact URLs externally opened, rollback method

A user can approve a CLASSROOM PILOT despite missing HOME RELEASE evidence; label it accurately rather than delaying all teaching.
