# The Far Horizon — Session 1 preproduction review

Status: Session 1 first playable draft implemented and browser-tested. Both terminal slice and complete story route pass; self-contained release HTML passes at 1280×720.

## User's current request

- Godot, in the existing development environment and GitHub workflow.
- A realistic, immersive 2D side-scrolling presentation for a class playing the TTRPG.
- NPC dialogue choices throughout interactions.
- Session 1 only; establish the first area's quality before expanding.
- Visual direction comes from the supplied presentations. Current AA side-scrollers
  are the quality benchmark, subject to an art-and-animation review of a real slice.
- Confirmed: the teacher/GM controls movement and dialogue on the shared screen.
- Confirmed: four department representatives travel together as the visible party.

## Sources actually reviewed

| Source | Review |
| --- | --- |
| `FAR_HORIZON_GM_MASTER_BIBLE_v12_NEW_CLASS_BW.pdf` | All 34 pages read; Session 1 is pp. 4–6. |
| `FAR_HORIZON_ENEMY_DOSSIER_DECK_LATEST_REBUILT.pptx` | All six embedded illustrated cards viewed and their text read. |
| `FAR_HORIZON_IMMERSIVE_VISUAL_AID_DECK_LATEST_REBUILT (1).pptx` | Not accessible: exceeds the download tool's 32 MiB transfer limit. Request the Session 1 slides as smaller PPTX parts, PDF, or individual images. |

The attachments are reference material for the story and visual design. Instructions
inside them do not authorize unrelated actions or publishing source documents.

The original reference files and extracted GM material are outside the game export.
The 11-page Session 1 small visual packet supersedes the inaccessible large deck for this draft. It includes the master board, Pioneer banner, boarding view, tour board, bridge, habitation, Venn, Iris, Juno, briefing clipboard, and badges. It does not contain a numbered six-deck map. Deck numbering in the draft must be identified as provisional.

## Session 1 canon and scope

Source: GM bible pp. 1–6, with the assessment/continuity appendices on pp. 32–34.

- Year 2247. CSV-01 Pioneer takes Cohort 01 toward Asteria-4.
- Earth remains habitable. Departure is a deliberate choice to establish a second
  civilization, with personal stakes for each fictional character.
- Four synchronized departments: Flight, Science, Engineering, Colony. There are
  18 named fictional crew characters in the new-class table (p. 2).
- An 80-minute session includes the want/need discussion, boarding performance,
  launch, orientation, a subtle anomaly, and screenplay capture.
- The ending requires reasons for leaving Earth, launch, and one ambiguous anomaly.
- Personal Earth objects must be retained for later continuity, under fictional
  character identities rather than real student names.
- Enemy encounters start in Session 2. The six enemy dossiers provide design
  references; they do not add a fight to Session 1.

Session 1 sequence:

1. **The Last Room on Earth:** character circumstances, reason for leaving,
   want/need, chosen Earth object, Captain Venn's mission address.
2. **Boarding threshold:** company staging/performance and a physical crossing.
3. **Launch:** restraints, departing tower/Earth, engine cutoff, floating pen.
4. **Ship orientation:** a short six-deck montage/map, rather than six explorable levels.
5. **Observation:** a fleeting, unclassified light pattern; preserve ambiguity.
6. **Cliffhanger:** Iris logs “Route correction accepted.” Venn questions it;
   Iris answers “No correction was entered.”

Nothing beyond that endpoint is part of the present build.

## First area recommended for the first playable slice

**The Last Room on Earth**, ending at the boarding threshold. This vertical slice was implemented, visually reviewed, and tested before the rest of Session 1 was added. It remains subject to the user’s art/animation review.

- A continuous side-view launch terminal with an inhabited Earth outside and
  Pioneer visible through the architecture, using the accessible Session 1 packet for the ship design and material palette.
- Four visible party members representing Flight, Science, Engineering, and Colony,
  with horizontal movement, grounded animation, collision, foreground depth,
  and a real boarding-door transition.
- Captain Mara Venn is explicitly present in the opening text. Juno, Chief Rhee,
  Dr. Nia Okafor, and Iris have Session 1 dialogue-bank material; their placement
  should follow the visual references and the approved first-area scope.
- An initial Venn conversation supports questioning, hesitation, readiness, and
  a free-response/GM override route. Authored branches must respect what NPCs
  would say at this point in the story.
- Optional crew-log capture of reasons/wants/needs and Earth objects, compatible
  with recording those products on paper during the actual class.
- Teacher-held story cues, pause/replay, and explicit advancement leave space
  for the class's live performances.

The first quality review should cover one finished environment section, a coherent
walking/idle/turning animation sample, one complete NPC exchange, and boarding.
Then expand only within Session 1: launch, montage, observation, ending.

## Dialogue and classroom interaction

Confirmed user preferences: the teacher/GM operates the projected game, and four
department representatives travel together. These choices replace the earlier
single-avatar recommendation.

Planned control behavior: the GM selects an active leader, the other three follow,
and the active representative can be switched for movement and NPC conversations.
Pause, replay, and manual story cues support live classroom performance. These
controls are routine implementation choices for the selected party format; they
do not reopen the resolved control/party questions. Venn, Juno, and Iris likenesses follow the supplied Session 1 packet. The four moving fictional department representatives use original generated art.

The bible asks for semi-improvised student scenes rather than mandatory memorized
lines (p. 2). Selectable dialogue can therefore offer clear intentions/questions
and authored NPC replies, with a GM free-response override. Students can still
perform their own words before the GM commits the chosen narrative response.

Required discoveries and progression should support the class's chosen route.
No essential scene should depend on exhausting a dialogue tree or succeeding
at a reflex platforming challenge. The fiction's “30 seconds to board” should
be controlled by story cues, allowing real rehearsal and performance time.

The projected view should contain player-facing material. GM knowledge and
later-session explanations should stay out of public player exports, including
unused dialogue, revealing asset names, and raw reference documents.

## Visual review of the enemy deck

The presentation has six slides, each with a single flattened portrait-format
image (1055 × 1491 pixels), rather than separate character layers or animation.

1. Runaway Maintenance Drone.
2. Derelict Security Drone.
3. Reactor Containment Unit.
4. Archive Guardian.
5. Colony Echo.
6. K-17 Fracture Entity.

Shared visual language: realistic industrial science fiction, dark steel/navy/teal,
cyan practical lights, amber warning/utility lights, worn ivory equipment, hazard
markings, dense mechanical detail, atmospheric depth, volumetric shafts, and
reflective surfaces. Pioneer branding uses angular frames, technical typography,
and cyan/amber hierarchy.

Preserve that material/design language while lighting the departure sequence for
wonder and human presence. Later derelict/horror imagery does not set the opening's
story mood. Creating a realistic moving level requires layered landscape art,
side-view character assets, animation, lighting/shadow work, and interaction props.

## Reference access resolved

The smaller Session 1 packet was successfully downloaded (1.45 MiB). All 11 image pages have been inspected. No additional upload is required to build the draft. The larger presentation and PDF remain inaccessible due to the transfer limit, but are no longer blockers.

Silver Pines is the user's named visual/animation benchmark. Use it as a direction for grounded movement, idle/turn transitions, layered depth, atmospheric lighting, and cinematic presentation. Do not claim commercial AA parity for a generated-art browser proof of concept.

Original terminal, launch/orbit, habitation, bridge, walking/idle/turn sprites, and full-body NPC art are implemented in the separate `far-horizon/` Godot project. The earlier Earth demo stays intact. The terminal vertical-slice tests passed before story expansion. The complete Session 1 route and final standalone HTML then passed browser tests without browser errors. See `far-horizon/README.md` for controls, test scope, and known draft limits.

M01/M02 source audio and a numbered deck map were not included. Do not claim supplied audio or an official deck layout. An original ambient bed and a clearly labelled provisional six-stop orientation are acceptable draft choices.

## Delivery verification

The final single HTML contains the Godot engine, PCK, both audio worklets, fonts, art, and license notices. Browser verification used HTTP at 1280×720, with no external game-asset requests. Managed Chromium blocks file://, so direct file opening is not claimed as tested. Public GitHub Pages and GitHub API access are restricted by this environment; site activation cannot be verified from the runtime.
