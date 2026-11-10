# V8 vertical-slice acceptance checklist

The first v8 trial must meet ALL of these gates before scaling into a full game.

## Source & language
- [ ] Canonical approved v6 files restored with matching SHA-256.
- [ ] Relevant original textbook pages actually inspected; required forms/words mapped to player actions.
- [ ] Learner scaffolds and accurate Simplified Chinese glosses verified.

## Visual + audio
- [ ] Original scene-specific layered 2.5D art exceeds v6 baseline (not flat drawings pasted over photos).
- [ ] Physical objects align with evidence and can be manipulated within the scene.
- [ ] Subtle, localized, optional environmental motion; reduced-motion supported.
- [ ] No placeholder room imagery, repeated backgrounds, or obscuring UI.
- [ ] If voice is used, captions are complete and audio is local/offline; no paid generation without authorization.

## Gameplay
- [ ] Character can move between meaningful positions or spaces.
- [ ] A nontrivial context-grounded interaction requires source evidence and target language.
- [ ] An NPC conversation has meaningful outcomes, not a one-line information kiosk.
- [ ] A decision or correctly authorized action visibly changes the environment and persists on return.
- [ ] Correct, incorrect and alternate attempts are functional, comprehensible, and recoverable.

## Technical + QA
- [ ] Offline build opens on desktop after extraction; no required external requests or VPN.
- [ ] Mobile touch controls and responsive layout pass automated Chromium width checks.
- [ ] Save/resume and student report export work with exact delivered files.
- [ ] Reduced-motion and mute states verified.
- [ ] Screenshots of actual interactions visually inspected, not only JS-console checks.
- [ ] Test report names paths, tool choices, asset provenance, pass/fail, and unresolved limitations.
- [ ] Teacher approves the first fully polished new v8 creative direction before scaling.

**Important:** these are acceptance criteria, not a claim that a playable trial exists yet.
