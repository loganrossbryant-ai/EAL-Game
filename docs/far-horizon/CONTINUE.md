# SECURITY HOLD — READ FIRST

The user reports Microsoft Defender **Trojan:Script/Wacatac.B!ml**, marked Severe/Active, after the offline download. The affected path and whether the HTML was opened are not established. The user said no further details were shown. Advise recommended quarantine/removal; do not ask the user to restore, allow-list, or disable Defender. If opened, recommend a Defender full scan.

The current Far Horizon ZIP and embedded HTML have been withdrawn from the public main branch in commit `5923d19e5f6d7368224ca5f212d67decf76150f9`. Do not offer old links or silently republish a replacement. Local samples and source are retained for investigation. Official-file and build-integrity checks are NOT antivirus clearance. This is not a confirmed false positive. No Defender scanner is available in this Linux environment. Do not upload samples to third-party services without authorization.

# Far Horizon continuation checkpoint

## Current result

Session 1's first playable Godot/HTML draft is complete. The terminal vertical
slice was tested visually before expansion. The complete Session 1 route and
the final single-file release then passed browser tests.

- Proposed hosted URL (inactive; Pages is NOT enabled): https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/
- Public repository: `loganrossbryant-ai/hello-earth-demo`, branch `main`.
- Published game commit: `90614a9be3120e9b23e0a836da2e16449cf8aeb1`.
- Editable source: `loganrossbryant-ai/EAL-Game`, branch
  `codex/far-horizon-session-01`, project `far-horizon/project.godot`.
- Source implementation commit before this checkpoint:
  `b9648a6fdbf0e98c0e3ee222ed404b4d9abcdb81`.
- Final HTML: `builds/far-horizon-delivery/index.html`, 34,934,692 bytes.
- HTML SHA-256:
  `aae65757c483e136d1fcb9ab79683d2c2b1aabbd20e79f5a63cad3b3b7bf7e6e`.

Correction from the latest user message: GitHub Pages is NOT enabled. Deliver the standalone HTML for local browser opening; do not direct the user to the github.io play URL. The runtime network policy also blocks github.io and the GitHub API. The tested HTML is uploaded under `/far-horizon/`;
the earlier root Hello, Earth! demo is preserved byte-for-byte.

## Confirmed preferences and scope

The teacher/GM controls a shared projected screen. Four department
representatives travel together; the active leader/spokesperson can change.
All 18 fictional crew identities are available for records. Student live
performance and paper records remain supported. No real names are requested.

Build **Session 1 only**. Earth is habitable. The mission deliberately creates a
second civilization. The story runs terminal → boarding → launch → brief
orientation → observation → three-line screenplay capture → route-log ending.
End with Iris: “Route correction accepted.” Venn asks who entered it. Iris:
“No correction was entered.” No later-story revelations or combat are in scope.

The small 11-page Session 1 packet resolved the earlier inaccessible large
deck/PDF. All 11 pages were viewed. The GM bible and six enemy dossier cards
were reviewed earlier. Raw GM documents are outside the public game export.

## Quality direction and remaining draft limits

Silver Pines is the user's named animation/visual benchmark. Current artwork
is original realistic generated art based on their packet. Characters currently
use eight-frame walking sheets, separate idle/turn poses, acceleration, easing,
contact shadows, reflections, and parallax. This is a prototype animation pass;
do not claim finished AA parity or that Silver Pines footage was inspected.

The numbered canonical deck map was not supplied; the six-area directory is
provisional. M01/M02 recordings were not supplied; the game's ambient/SFX bed is
original procedural audio. Do not request the large files again as blockers.

After user feedback, the next useful work is refinement within Session 1,
particularly character gait, turns, interaction staging, and atmospheric depth.
Do not automatically expand into Session 2 or rebuild the published draft.

## Verification and build

Godot 4.6.3 and matching Web templates are installed. Use writable paths:
`XDG_CACHE_HOME=/workspace/.cache XDG_DATA_HOME=/workspace/.local/share
XDG_CONFIG_HOME=/workspace/.config`.

- `far-horizon/tests/browser_slice.py --full`: actual keyboard/mouse input,
  party movement/following, dialogue, writing, paper acknowledgements, boarding,
  five launch cues, cue reload, four department choices/reasons, unclassified
  anomaly, three screenplay lines, exact ending, JSON export, saved ending.
- `far-horizon/tests/browser_html.py`: final release at 1280×720; sound helpers,
  movement/writing, local save restoration, no debug globals, and a confirmed
  new-class reset. No browser errors or external game-asset requests.
- Reports/screenshots: ignored `artifacts/far-horizon-tests/`.
- Direct file:// testing is blocked by managed Chromium; the standalone HTML
  was tested over HTTP. Do not claim direct file opening was verified.
- Export using `far-horizon/export_presets.cfg`; bundle using
  `tools/package_fh_html.py`. See `far-horizon/README.md`.

The workspace still has older uncommitted Earth-demo work and an edited root
README. Preserve those changes. Source/public commits were prepared with
separate temporary Git indexes; the workspace's main branch/index was not
switched or reset.

## Usage-reset request

The user asked to schedule continuation whenever Work/Codex usage comes within
5% of its limit, resuming after a reset. This session exposes **no usage/quota,
reset-time, or task-scheduling tools**. No scheduled task was created. The user
was told this limitation. Do not claim to monitor the allowance or promise an
automatic background restart. Resume from this checkpoint when the user returns
and asks to continue; recheck tool availability if it has changed.

## Offline download

The user explicitly requested the HTML file for direct browser opening. The ZIP download contains only `Far-Horizon-Session-01.html`, with all engine/art/audio/font data embedded. Unzip and open the HTML in Chrome or Edge. Direct file opening remains unverified here because managed Chromium blocks file URLs; the exact HTML was tested over HTTP. Raw GitHub HTML links display source text, so the ZIP is the reliable direct-download route.

Direct download: https://github.com/loganrossbryant-ai/hello-earth-demo/raw/refs/heads/main/far-horizon/Far-Horizon-Session-01.zip

Download commit: `35030471e267db79072ec7ea7dd2da01bdf0a6bf`. The original embedded HTML bytes are unchanged. When updating the game, regenerate both the hosted HTML and the ZIP so the offline download stays current.
