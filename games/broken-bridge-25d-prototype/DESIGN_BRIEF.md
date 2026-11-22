# The Broken Bridge — 2.5D reusable engine vertical-slice design brief
**Build classification:** experimental design / no classroom or parent release.
**Audience:** two content profiles over one world/state/action engine. Elementary (Grades 1–3, recognition → supported production); middle school (Grades 6–8, novice EAL / WIDA ~1.9 as an indicative scaffolding target). No age-specific student data in source.
**Goal:** demonstrate that the player moves, inspects evidence, speaks/chooses purposeful English, acts physically, and observes persistent consequences.

## Creative premise
A severe night storm damaged a footbridge crossing a forest river. A ranger needs to deliver emergency supplies to a lookout on the far bank. A damaged trail notice suggests that the bridge may be unsafe; there is also a shallow ford downstream. The player must **investigate the site, choose a safe route, communicate that plan, then carry out an observable repair or marking action**. The ending depends on evidence and decisions, not on scoring a detached quiz.

## Vertical-slice scope (10–15 minutes, one spatially connected world)
- **Scene A — Ranger clearing:** riverside path, ranger NPC, small shelter, tool rack, visible far bank, damaged bridge, river (with distinct before/after states), directional markers and accessible map.
- **Scene B — Connected bridge / ford edge:** camera pans or player walks a short connected distance to inspect depth marker and a fallen sign; revisit possible. Avoid a separate scene menu or teleport-only navigation.
- **Closing return:** back to the ranger and visible delivery outcome (bridge restored *or* ford safely marked). Return confirms persistent choice.
- Optional 2D parallax + localized motion only: flowing river, slight swaying needles/grass, changing warning lamp, plank position, ranger turn/look. No mandatory WebGPU.
- Character may move by keyboard and tap-to-walk; accessible joystick or large touch movement controls if thumb movement tests show need. No tiny hotspots or clipped bottom buttons.

## Story dependencies and possible outcomes
`intro -> [talk_ranger, inspect_bridge, inspect_depth_marker, inspect_ford_sign, collect_available_materials (any order)] -> explain_route -> {bridge_path | ford_path} -> carry_out_action -> ranger_response -> return_and_export`.
- **Bridge path:** evidence shows safe conditions; collect/position two boards and secure rope using physical drag/snap interactions. Ranger authorizes work after evidence-backed dialogue. Bridge changes from visibly broken to traversable, ranger crosses with supplies.
- **Ford path:** depth marker and trail sign support safe crossing; orient two marker posts and move the supply pack to the marked crossing. The bridge stays broken; a marked riverbank route opens and ranger chooses it.
- **Wrong/uncertain plan:** ranger shows a relevant clue and suggests further inspection. Never softlock or require memorizing inaccessible evidence. Unreasonable plan is revisable.
- **Persistent consequence:** choice saved; world look, available crossing, NPC location/line, ending and teacher record agree on resume. Both routes valid if supported by observed evidence; author one unambiguous, reachable evidence chain per route.

## Signature mechanic: Inspect → explain → physically change the world
The player must interpret visible depth/safety evidence before configuring the river crossing. The main verbs are **inspect, collect, compare, position, ask/explain**. Objects in-world matter: don't treat them as menu-based multiple choice. Show cause and effect: bridge board snaps into place, path lights change, markers physically reposition, ranger actually travels across.
Every mandatory puzzle contract: 1) in-world reason 2) observable inputs 3) evidence required 4) acceptable solutions 5) visible response 6) reversible wrong states/hint ladder 7) saved consequence 8) teacher rationale.

## Core interactions
| Object or NPC | Meaningful action | Evidence and fair retry | Visible change |
|---|---|---|---|
| Broken bridge | inspect structural gap, measure board slots | nearby missing planks; clear silhouettes | repair sockets highlight; later bridge reconnects |
| Depth marker | inspect water line; compare with posted safety limit | number plus pictogram; large zoom and repeat access | route choice updates |
| Trail sign | inspect torn map and orientation | readable right-way cues; no hidden transcript | safe ford recognized; sign/markers move |
| Tool rack | collect physical boards or posts | spatial preview and inventory hints | rack empties, carried objects visible |
| Ranger NPC | ask, get modelled language, explain choice | optional translation, word bank, 3-level hints | trust/authorization, NPC moves and changes dialogue |
| Crossing task | place/rotate 2 objects or guide pack | reversible operations, non-punitive feedback | repaired bridge or visible marked crossing |
| Ending | return to ranger and export | summary names evidence and choices | final world-state + teacher record |

## Learning design: shared mechanic, differentiated language, NOT two separate stories
- **Elementary CORE:** recognize/locate concrete words, produce one comprehensible sentence about the bridge/location, ask one supported question; familiar action prompts with images and Chinese glosses.
- **Elementary STRETCH:** explain choice using `because`, compare safe/unsafe routes, combine two ideas, optional spelling/phonics.
- **Middle CORE:** ask for location/clarification, identify two details from visual evidence, recommend a safe plan with a structured reason. All prompts remain short, age-respectful.
- **Middle STRETCH:** compare plans and consequences, challenge first assumption with evidence, explain revised decision in connected sentences.
- Same clue availability and valid physical solutions for both profiles. Language mode controls the **scaffolding and output**, not which terrain facts are true.
- Illustrative text is mapped in `LANGUAGE_ACTION_MATRIX.csv`. Before aligning to real learners, replace/extend it only after checking actual lesson PPT/textbook/print/homework maps.
- Speaking participation button logs “practised” only; NEVER claim automatic speech recognition, correct pronunciation or independent assessment unless intentionally built and tested.

## Dialogue and teacher records
NPC schema: `npc_id, dialogue_node, prerequisite_flags, choice_id, model_text, zh_gloss, audio_asset_id?, required_evidence[], outcome_flags[], hint_levels[], voice_text_fallback`. NPC dialogue is authored and deterministic for offline replay, not fetched from an LLM.
Teacher report: anonymous local session ID, language profile, clue exposure, selected action, hint use, sentence draft or selected frame, self-reported speaking participation, branch and completion. Clearly separate **observed answer**, **self-reported speech**, and **ungraded reasoning**.
Save `localStorage`/IndexedDB as appropriate with versioned schema; provide JSON export and safe import/recovery where local storage is unavailable.

## Visual asset shot list (original, game-ready)
1. Establishing forest clearing as aligned distant/mid/foreground layers (empty UI).
2. Persistent bridge scene BEFORE (gap, missing boards) and AFTER (same geometry, boards repaired).
3. Ford edge BEFORE and AFTER with two marker posts and traversable route.
4. River surface animation tiles/overlay; sparse wind/leaf particles; reduced-motion still variant.
5. Ranger consistent full-body sprite states: idle, listening, pointing, walking; close-up expression portraits.
6. Child/teen-neutral player avatar sprites with walk/idle, no gendered assumption.
7. Inspectable prop inserts: depth marker with consistent tick values, damaged direction sign, two boards, rope, emergency supply pack, site map.
8. Finish states for bridge and ford, with matched perspective/color/light.
All readable game text lives in real DOM, never baked into generated scenery. Match physical evidence exactly across prop closeups, dialogue and accepted outcomes. No reuse of licensed game assets.

## Engineering direction (subject to technical spike)
- **Baseline:** Phaser 3 + DOM interface (accessible button/dialogue/Chinese text) using local bundled assets; lightweight Vite build, Playwright tests, offline single-HTML release if feasible. WebGL2 with Canvas fallback preferred; no hard WebGPU requirement.
- **Parallax 2.5D:** static camera-safe art planes plus light camera movement; genuine character movement in foreground; hotspots anchored to world coordinates; camera-to-screen transform shared with pointer input.
- Responsive layout: 390×844 and 844×390 phone targets plus 1366×768 desktop. Respect safe areas; always visible start/continue/back; all controls >=44 CSS px; native scroll within dialogue panels; reduced motion.
- **Offline:** zero mandatory CDN/fonts/APIs; bundle assets and scripts locally. If shipping a PWA, verify HTTPS install and real cold-restart offline. Local `file://` and iOS Home Screen are not equivalent; never promise both without separate tests.
- On-device performance target to measure (not claimed): sustained ~30 fps on a representative iPhone with ambient layers and scene UI, no unexpected GPU reset; adaptive texture/resolution options.
- Audio: optional ambience and SFX default muted; spoken model audio must be complete and in approved voice **if required for independent home use**. No voice synthesis or paid credits initiated in this design branch. Caption every spoken line.
- Do not use live speech recognition or an online AI API in mandatory gameplay.

## Out of scope for the FIRST slice
Open world procedural generation; full WebGPU; 3D physics; dynamically generated LLM dialogue; parent accounts/cloud analytics; 5 worlds/128 rounds; large voice casts; unverified sharing links; real-time speech grading. Those can be evaluated after one polished and verified slice.

## Acceptance demonstration
An elementary profile and middle-school profile can each: enter -> move to 2 places -> investigate multiple actual props -> ask NPC -> commit to evidence-backed choice -> manipulate items -> watch persistent world change -> return -> resume/export teacher report. Negative and alternate branches must function. QA and actual device results are recorded in `TOOL_SELECTION_AND_QA.md`.
