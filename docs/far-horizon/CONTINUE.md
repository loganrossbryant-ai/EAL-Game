# Far Horizon — current animation revision

The current task is refinement of Session 1: smoother walking, environmental
motion in each setting, and ElevenLabs NPC recordings. The visual revision is
implemented and its full Session 1 route and motion checks pass. See
[revision-quality.md](revision-quality.md) for changes, evidence and limits.

## Active external dependency

ElevenLabs is not connected. No ELEVENLABS_API_KEY is configured, and
api.elevenlabs.io is outside the network policy. The user was asked to configure
the secret privately and allow the host; their answer is pending. Do not put the
key in chat/source/browser, substitute another service, or claim recordings are
finished. The script contains 34 authored NPC lines / 3,435 characters / five
speakers. The local player and generator are prepared but actual speech and
voice-control QA remain blocked.

## Build and verification

Godot 4.6.3 and matching non-threaded Web templates are installed. Use:
XDG_CACHE_HOME=/workspace/.cache XDG_DATA_HOME=/workspace/.local/share
XDG_CONFIG_HOME=/workspace/.config.

- Debug server: builds/far-horizon-debug, port 8080.
- Standard scan candidate: review-candidate/far-horizon, port 8081.
- `FH_URL=http://127.0.0.1:8080 python far-horizon/tests/browser_slice.py --full`
  traverses Session 1 with actual inputs and checks all story gates.
- `python far-horizon/tests/browser_motion.py` checks contacts, follower speed,
  staggered gaits, turns, and fixed-camera scene motion. Latest: 166 steady
  contacts; maximum contact drift 0 pixels; all five scene states animate.
- `FH_STANDARD_BUILD=1 FH_HTML_URL=http://127.0.0.1:8081/ python
  far-horizon/tests/browser_html.py` checks the exact standard release.
- Ignored reports/screenshots: artifacts/far-horizon-tests.

## Release/security workflow

The earlier packed all-in-one HTML and ZIP remain withdrawn after the reported
Wacatac alert. The detection was never declared a false positive. Use only the
standard separate-file Godot Web export. See [security-review.md](security-review.md).

After every game-byte change, export, run tools/prepare_fh_review.py, test those
exact files, push codex/far-horizon-defender-review and wait for a matching
scan_passed Windows report. Retain review-candidate/.gitattributes. Publish only
matching hashed files, with current active Defender, no exclusions, exit 0, no
detections, and before/after integrity checks. Never reuse old scan clearance.

Public repository: loganrossbryant-ai/hello-earth-demo, branch gh-pages.
Browser URL: https://loganrossbryant-ai.github.io/hello-earth-demo/.
Pages is already enabled. The public main branch preserves the unrelated root
Earth demo and the withdrawal notice. Do not publish private source history into
the public branch. Use that public branch's current commit as release parent.
Live github.io is blocked here; verify Pages through its public Actions page and
test exact build files over local HTTP.

Editable source: loganrossbryant-ai/EAL-Game, branch
codex/far-horizon-session-01. The workspace stays on main with unrelated dirty
Earth-demo work/root README preserved. Prepare commits with temporary Git
indexes and explicit paths. Do not reset or switch over those changes.

## Confirmed scope

Session 1 only: healthy Earth, a deliberate second civilization, terminal,
boarding performance, five manually cued launch beats, six-area orientation,
observation, three screenplay lines and the exact route-log exchange. Four
representatives travel together; the GM controls the shared screen. Keep all 18
fictional identities and paper/live-performance options. No real student names.
No combat, later-session reveals or automatic countdown.

The small 11-page packet resolved the oversized visual files. The GM bible was
reviewed. The numbered canonical deck map and M01/M02 recordings were not
supplied; the directory remains provisional and ambience/SFX are original.
Silver Pines is the quality direction, not a claim of AA animation parity.

No quota/reset monitoring or scheduled continuation tool exists in this session.
No automated usage-reset task was created; resume when the user returns.
