# EAL 2026–2027 — Next-Generation Immersive Game Design Standard

**Status:** Project source / standing creative and production brief  
**Version:** 2.1 — amended 8 November 2026 (approved v6 baseline + mandatory execution gates + tool-directed production governance)  
**Purpose:** Improve future educational browser games beyond the currently approved titles without discarding successful systems.  
**Relationship to prior files:** This document **expands and supersedes** `FUTURE_GAME_QUALITY_BRIEF.md` when planning future games. The existing Project instructions still govern curriculum fidelity, student differentiation, printing, source-first work, and quality assurance. Do not reinterpret this as a request to modify already approved games.

---

## 1. North-star experience

**Build a compelling adventure game in which authentic English communication is how the player changes the world.** A student should want to continue investigating even without a grade attached. The language instruction must be real, rigorous, and traceable to the unit, yet the player should experience it primarily as *investigating, repairing, persuading, deciding, surviving, discovering,* or *building*—not as completing a worksheet in disguise.

A successful new game combines:

1. **The atmosphere of a cinematic mystery:** A distinctive world, striking environmental art, music, and suspense.
2. **The freedom of an adventure game:** Physical exploration, manipulation, discoveries, and genuine player agency.
3. **The consequences of a simulation:** Choices persist, relationships evolve, and locations visibly change.
4. **The learning design of a strong EAL lesson:** Required vocabulary, grammatical structures, comprehension, and evidence-based language production enable success.

**North-star evaluation question:** *Would students still want to play if they were not being graded?*

The approved games are **minimum production-quality benchmarks, never mechanical templates**. Future titles must be original in worldbuilding, art, puzzles, pacing, and signature gameplay systems.

---

## 2. Canonical references and limits

### Approved references to inspect before development

**Current minimum approved production baseline (takes precedence for new builds)**

- **The Town That Rebuilds Itself — Living Environments v6** (Grades 9–10, *Community Builders*): approved benchmark for scene-specific environmental animation, Focus View, classroom-safe offline behavior, mobile-responsive controls, and preserved evidence-to-action gameplay. Exact file: `The_Town_That_Rebuilds_Itself_Living_Environments_v6.html`.
- **Do Not Answer Your Own Voice — Living Environments v6** (Grades 11–12, *Secrets and Lies*): companion benchmark for cinematic mystery presentation, optional environmental motion, investigation mechanics, mobile interaction, and offline packaging. Exact file: `Do_Not_Answer_Your_Own_Voice_Living_Environments_v6.html`.
- **`EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`** defines the required v6 patterns, exact file hashes, and explicit limitations. These v6 games replace older Sound Editions **as the minimum current presentation/technical baseline**, but **not** as narrative templates or a ceiling on visual fidelity, puzzle variety, or environmental realism.

**Additional approved and archival references**

- **The Town That Rebuilds Itself — Sound Edition** (Grades 9–10, *Community Builders*): movable map, evidence dossiers, clickable physical clues, supported writing, civic consequences, environmental atmosphere, optional sound.
- **Do Not Answer Your Own Voice — Sound Edition** (Grades 11–12, *Secrets and Lies*): unsettling mystery, evidence comparison, cautious claims, witnesses, ethical decisions, and branching outcomes.
- **A Town Worth Staying In** (Grades 11–12, *Development*, earlier source archive): six-week settlement simulation, eight residents, resource trade-offs, fairness threshold, council reports, and competitive dimension.
- **The Internet of a Missing Town / Greyhaven: The Ninth Guest** (Grades 9–10, *Designing the Web*, earlier source archive): fictional linked websites, functional search/filter/review systems, provenance and usability investigations, archive mystery.
- **Far Horizon:** **Visual-quality benchmark only** for photographic realism, cinematography, scene density, convincing physical props, and character presentation. Never transplant its images, portraits, music, or worldbuilding into unrelated games unless expressly requested.

### Archival caveat

The approved **Sound Editions are complete reference builds**. The earlier *Two Towns* source ZIP supplied for the library is missing **13 externally distributed scene images**. Preserve its original gameplay and source as-is. Do not claim its archived visual presentation is complete until those missing assets are recovered; do not silently substitute unrelated images or treat the incomplete build as an approved art reference.

### Source-first rule

Inspect the actual current unit pages, teacher-provided objectives, student group profile, approved game files, and relevant Project conversations before inventing a new game. Separate **textbook-required language**, **necessary task language**, and **optional enrichment**. If a source is missing or inaccessible, identify the limitation instead of inventing textbook requirements.

---

## 3. Visual immersion: make locations behave like living places

### 3.1 Story-specific cinematic environments

- Design original, location-specific 2.5D or 2D environments with coherent architecture, geography, lighting, weather, material textures, period, and recurring motifs.
- Plan each location with a **scene storyboard and a physical clue-prop shot list**: establishment shot, interactable objects, close-up evidence inserts, state changes, and critical character positions.
- Use **environment-only** AI-generated images for game scenery. Keep all navigational UI and readable text in actual HTML/game interfaces. **Never use promotional mockups, reused slides, screenshots, or baked-in labels as playable backgrounds.**
- NPCs should have consistent, role-specific photorealistic portraits or character models. Maintain recognizable facial identities across dialogue, locations, emotional states, and repeat encounters.
- Every evidence insert must depict the *actual object described by the text*: the clock, camera, maintenance log, gate measurement, access card, reservoir gauge, transcript, or device. Text and measurements must agree across the prop, document, puzzle, and teacher key.
- Avoid generic repeated backgrounds, oversized panels obscuring scenery, floating placeholder icons, or unmotivated HUD decorations.

### 3.2 Layered 2.5D presentation

Prefer high-quality, efficient effects over full 3D for initial browser releases:

- Separate foreground, midground, background, and atmospheric layers to create depth and subtle parallax when the camera/player moves.
- Animate **meaningful** scene elements—rippling floodwater, unstable machines, moving fog, fluorescent flicker, changing surveillance lights, security shutters, printouts, or distant silhouettes.
- Use selective camera movement and cinematic entrances, framing, and lighting transitions; do not apply the same endless zoom to every scene.
- Keep animations restrained during demanding reading tasks. Provide reduced-motion support and never make essential clues depend on animation alone.
- Make interior/exterior travel feel spatially connected: doors, corridors, ladders, stairwells, paths, blocked routes, and return visits.

### 3.3 Persistent visible world-state changes — highest priority

Design at least one visible **before → decision/action → after** transformation per major narrative sequence, adapted to the game's scope:

- An infrastructure repair restores lights, lowers water, or opens a route.
- Withheld evidence leads to a protest, closed shop, evacuation, damaged relationship, or altered notice.
- A character leaves a location, barricades a door, withdraws a document, or returns after trust is earned.
- Weather, security, or environmental hazards intensify because time and decisions matter.

A resource meter or toast message alone **does not count** as a sufficiently reactive world.

---

## 4. Storytelling: mystery, stakes, and causal consequences

### 4.1 Recommended dramatic arc

1. **Impossible opening:** A striking incident establishes a question that a player urgently wants answered; playable investigation starts quickly.
2. **First explanation:** Physical and written evidence support a plausible theory; the player meets core characters and explores connected locations.
3. **Reversal:** A later discovery changes the interpretation of a previously observed object or statement, encouraging students to reconsider rather than merely move forward.
4. **Costly choice:** Two or more valuable goals conflict. The player must accept a sacrifice involving safety, trust, time, access, privacy, fairness, or resources.
5. **Confrontation and resolution:** The ending depends on collected evidence, language-based actions, relationships, and consequential decisions. Resolve the main mystery explicitly; optional ambiguity can remain.

Events must follow **narrative causality**: the player visits the pump room because of a river measurement, not simply because “Chapter 3 unlocked.”

### 4.2 Stakes and pressure

Use story-derived tension:

- Limited resources and mutually exclusive priorities.
- Evidence that may be lost, altered, or made public.
- Conflicting NPC objectives and competing accounts.
- Routes that close, systems that degrade, and consequences that unfold over time.
- Characters or communities visibly affected by the player's choices.

**Avoid penalizing EAL reading speed.** Prefer reversible preparation, meaningful warning signs, pausable situations, and hint ladders over arbitrary high-pressure countdowns. Difficulty should come from interpreting evidence and choosing actions, not from rushing English comprehension.

### 4.3 Causal branch graph, not cosmetic endings

Map the story as explicit dependencies. Plan **2–4 materially different investigation paths where appropriate**; the exact count depends on the unit, group, duration, and technical scope. A branch should change later access, documents, NPC availability/trust, physical conditions, or the resolution—not merely the ending's color or a score.

Consequences must persist into **at least one later playable scene or interaction**, not be announced only immediately after the choice. Every route must remain finishable; avoid softlocks. Allow productive mistakes to produce fresh obstacles, evidence, and revision opportunities rather than dead ends.

### 4.4 NPC agency and relationships

Prefer a **small recurring cast (roughly 4–6 substantial characters where appropriate)** over a large set of one-off information kiosks. Each important character should have:

- a distinct visual identity, voice/style of written dialogue, physical location, and routine;
- goals, vulnerabilities, and potentially conflicting motives;
- knowledge that is conditional on the player's discoveries;
- relationship states that respond to honesty, caution, accusation, help, or betrayal;
- observable later actions: they move, cooperate, conceal, refuse access, intervene, or change testimony.

Interviews should feel like tactical conversations with different information costs, not a repetitive list of “ask question / receive paragraph” choices.

---

## 5. Puzzles and mechanics: actions unique to each fictional world

### 5.1 One signature mechanic per game

Every substantial new game should introduce a defining gameplay system that is **not a recycled version of the other titles' primary loop**. Examples:

| World / unit | Potential signature mechanic | Required language must enable… |
|---|---|---|
| Community Builders | Operate flood-control valves, inspect infrastructure, choose what to repair under constraints | Evidence-based claims, passive voice, consequences and recommendations |
| Secrets and Lies | Synchronize CCTV feeds and clocks; reconstruct manipulated media and contradictory timelines | Modal deductions, cautious claims, comparisons of sources and credibility |
| Designing the Web | Navigate interconnected fictional sites; trace redirects, reconstruct a broken navigation graph, test usability | Evaluation of reliability, site structure, user needs, comparisons and explanations |
| Development | Build a working neighborhood transport/service network with budgets, access, resident welfare and unintended effects | Justify priorities, explain trends, compare outcomes, evaluate trade-offs |

These are **suggested possibilities, not mandated stories**. Each new unit deserves an original central mechanic built around its actual objectives.

### 5.2 Distinct puzzle verbs

Favor **physical, contextual operations** over repeated multiple-choice or sorting:

- turn, route, connect, calibrate, measure, assemble;
- reconstruct, synchronize, annotate, trace, compare;
- search, filter, recover, test, debug, redesign;
- negotiate, allocate, coordinate, persuade, deploy.

A substantial title should normally include **at least four genuinely different puzzle verbs**, adjusted for age, session length, and learning needs. A code lock, evidence sort, and multiple-choice question should not all be considered distinct merely because they have different visual skins.

### 5.3 Puzzle design contract

For every significant puzzle, document:

1. **Fictional reason it exists:** Why is this problem present in the world?
2. **Player action:** What does the player physically or cognitively manipulate?
3. **Required evidence and language:** Which specific textbook forms or reading skills are necessary?
4. **Visual feedback:** What changes in the environment when an attempt succeeds or fails?
5. **Failure state:** How does the game guide revision without giving away the answer or softlocking progress?
6. **Persistent effect:** What later encounter, route, document, or world state changes?
7. **Teacher key:** What evidence supports the intended solution, and what alternatives are defensible?

**Test:** If the learning prompt could be pasted into an ordinary worksheet without losing anything important, redesign the mechanic.

---

## 6. English as gameplay, not a visible checkpoint

### 6.1 Language should cause visible action

Make reading and writing **diegetic**—part of what characters and institutions require to act. Example actions:

- Write a maintenance order; the engineer reads it and repairs the generator; lights return.
- Submit a correctly evidenced public warning; residents evacuate or take precautions.
- Correct a misleading article; the newspaper and characters respond to the correction.
- Explain why a design disadvantages residents; a council permits a redesigned access route.
- Repair and explain a broken web navigation structure; a missing resource or clue becomes accessible.

Writing should not be an isolated “word-count gate” inserted after a puzzle. The message must have **a recipient, purpose, credible constraints, and observable consequence**.

### 6.2 Authentic, varied text forms

Use written material belonging naturally in the world: security logs, texts, interviews, emails, blueprints, notices, accessible data tables, survey findings, repair tickets, journal excerpts, forum posts, websites, archived records, captions, and correspondence. Distinguish unreliable testimony from directly observed evidence. Where sources contradict, let students examine both visually and textually.

### 6.3 Textbook fidelity and differentiated support

- Build a **unit-language-to-action matrix** before writing the story: objective → required vocabulary / grammar → authentic player use → evidence of learning → teacher verification.
- Explicitly separate textbook-required terms from narrative-only, Tier 2 academic, Tier 3 subject-specific, and enrichment vocabulary. Do not mislabel all academic words as Tier 3.
- Provide accurate Simplified Chinese glosses for necessary vocabulary at the point of use, with optional support rather than constant translations of whole pages.
- Offer scaffold levels: vocabulary reveal, sentence frames, example analysis, progressively more specific hints, and optional challenge tasks.
- Differentiate for the actual student group. Do **not** automatically assign the prior Grades 9–10 higher-agency design to a lower-agency Grades 11–12 group, or vice versa.
- Keep the fiction sophisticated while offering short, comprehensible tasks and visual objectives when needed.

### 6.4 Honest writing assessment

Offline code can reliably check certain patterns (key forms, selected citations, factual consistency with structured evidence, completion) but **cannot reliably grade nuanced reasoning or writing quality**. Distinguish automatic progression checks from genuine evaluation. Preserve student responses for teacher assessment. Prefer defensible alternative responses rather than fragile exact-string validation.

---

## 7. Sound and atmosphere

- Compose original, story-specific ambient soundscapes and restrained SFX that reinforce places, danger, and discoveries. Escalate ambience when a scene changes rather than simply turning up volume.
- Keep music and effects **separately adjustable**; start both **muted** for classroom use. Persist volume choices across scene changes without restarting tracks needlessly.
- Make audio optional and never the sole source of essential clues. Offer readable transcripts/captions for speech.
- Use natural speech sparingly only where it strengthens characterization. No heavy filters or robotic delivery. The user-approved Sound Editions demonstrate a successful classroom-friendly default.

---

## 8. Technical architecture and delivery

### 8.1 Game engine recommendation (optional, not compulsory)

For more complex future worlds, **consider Phaser plus HTML**: Phaser can handle spatial movement, sprites, cameras, layers, animated objects, scene transitions, and interactions; HTML can handle credible emails, records, writing interfaces, and export. This is a *proposed engineering approach*, not a requirement to migrate games that already function well. Evaluate feasibility and offline packaging before adopting it.

A 2.5D browser experience may be preferable to full 3D for independent classroom deployment, consistent art, load performance, and accessibility. The student should never need a VPN, remote API, external font, CDN, or cloud account to play a required portion of the game.

### 8.2 Required systems where appropriate

- Persistent world-state store for branch choices, locations, NPC trust, equipment states, and consequences.
- Save/resume across sessions (plus import/export if local browser storage is restricted).
- Student written-work export with sources and decisions; teacher-readable reports.
- Responsive hotspots, legible text, functional keyboard/mouse interactions, and accessible contrast.
- Reduced-motion support and independently switchable sound controls.
- Stable offline asset packaging: preferably fully embedded HTML or a clearly organized local package verified after extraction.
- Explicitly versioned assets and game files; no broken references or placeholder art in the submitted edition.

---

## 9. Revised production workflow — do not improvise the full game screen by screen

### Stage A: Source and learner audit

Read required unit pages and previously approved games. Identify target language, class size, proficiency, independence, likely misconceptions, and session length. Identify missing sources up front; do not fabricate curriculum.

### Stage B: Narrative systems blueprint

Produce an internal story arc, location graph, branch dependencies, recurring NPC goals, world-state schema, major interactive objects, signature mechanic, puzzle-verb list, and language-action mapping. Define consequences *before* writing the endings.

### Stage C: Vertical slice benchmark

Internally implement and test one representative portion containing a convincing location, character interaction, physically contextual puzzle, meaningful language action, a state change visible in the world, and save/export. **This is an internal quality checkpoint, not a substitute for delivering the complete game.** Expand only when its art and interaction quality are comparable to the approved references.

### Stage D: Original art and audio production

Generate original location environments, NPC reference sheets, object/prop close-ups, state variants, ambient animation layers, and sound, using a consistent art direction. Audit every scene for story match, composition, character continuity, readable interfaces, and no reused reference art.

### Stage E: Integration and systemic testing

Connect real scene interactions, unlock dependencies, NPC routines, world changes, and language-triggered actions. Test the actual UI, not just internal state objects.

### Stage F: Final classroom QA

Run favorable, risky, and unusual decision paths; exercise puzzles, hint ladders, evidence interpretation, writing, exports, audio controls, and offline launching. Inspect every room and modal as rendered, including text placement at common classroom screen sizes. Fix defects before the release.

**Delivery evidence:** Clearly distinguish created, inspected, automatically tested, manually tested, and actually used with students. Never claim a game is finished when required scenes, evidence, or branches are placeholders or unverified.

### Mandatory execution and release gates — standing requirement (added 8 November 2026)

> **Every future EAL browser game must start at the approved Living Environments v6 quality baseline and aim toward the higher visual, mechanical, and learning standards in this document.** Before full production, verify the canonical game source and original textbook chapter pages, map required unit language to player actions, plan the complete game, and internally build **one genuinely finished representative location**. That location must include coherent original scene art, motivated optional animation, a physically credible interactive puzzle, required unit-language use, a visible persistent consequence, and offline functionality. **Do not scale up an inadequate vertical slice.**
>
> **Preserve approved systems and make targeted corrections.** Do not substitute an older game version, copied reference art, unrelated imagery, a mock-up, or placeholder interactions for requested current work. If source material, image generation, audio production, or testing is unavailable, disclose the blocker; do not silently downgrade the quality or claim the missing feature is complete.
>
> **A build is not final merely because it launches, its story has an ending, or a ZIP exists.** Complete curriculum, visual, narrative, interaction, accessibility, offline, desktop/mobile, and export checks against the *actual delivered files*. Test wrong answers, alternative choices, and persistent state changes. Correct defects internally before teacher review. Deliver only verified files with a concise QA record distinguishing passed checks, untested conditions, and open limitations. Never claim physical iPhone Safari or classroom verification unless it was actually performed.

**Default decision rule:** The teacher approves educational direction and consequential creative departures; routine design, development, and internal QA decisions are made independently against the approved references. Present a polished playable vertical slice for creative approval when the art or game mechanics depart materially from precedent; do not ask the teacher to inspect successive incomplete prototypes or catch defects that can be found automatically.

### Tool-directed production governance — standing requirement (added 8 November 2026)

**The assistant owns tool selection, production coordination, verification, and routine internal revisions.** Do not default to the easiest available tool or assume that being granted permission to use plugins means their outputs have been used to their potential. Match each step of production to the required outcome, not to the tool's marketing claims.

**Before the first asset or code implementation:** inspect this standard, the exact approved v6 reference builds, the available textbook and learner sources, and the current canonical game-source version. Build an internal **Tool Selection and Verification Record** with one entry per substantial capability. Each entry must state:

1. **Required player-facing result:** the concrete curriculum/gameplay/visual/audio/technical acceptance criterion.
2. **Chosen tool and rationale:** the capability, current access, compatibility, offline output format, likely costs/credits, and why this tool is better than realistic alternatives.
3. **Validation method:** the observable proof needed before integrating the output (for example, actual image-pixel and geometry inspection, voice sample and transcript checks, playable interactions, or mobile screenshot comparisons).
4. **Observed result and source identity:** generated file or code version; what succeeded, failed, or remained unverified. Keep a source/asset manifest with exact filenames or repository revision IDs and provenance.
5. **Fallback or blocker:** an equivalent, verified alternative when available; otherwise explicitly mark the feature as blocked. **Never silently substitute weaker artwork, a diagram over a photograph, a mock-up, synthetic placeholder audio, or a superficial multiple-choice interaction.**

**Default tool routing (verify suitability when work begins; not a rigid or exclusive plugin mandate):**

- **Curriculum and creative direction:** ChatGPT plus the original textbook pages, current learner profiles, approved examples, and this Project's instructions.
- **World art and characters:** image generation or suitable image-editing tools for consistent, physically believable, story-specific assets; inspect actual output quality and matching scene states before development.
- **Environmental motion:** layered browser/engine animation for stable, localized effects; use generated video only when continuity, file size, offline/mobile compatibility, and cost can be verified.
- **Voices and sound:** locally packaged speech/audio using an available appropriate tool (for example ElevenLabs for voice performances); confirm dialogue text, speaker consistency, intelligibility, and captions. Playback cannot depend on a live service.
- **Game code and version control:** a maintainable browser-capable development stack (Phaser plus accessible HTML is the preferred v8 candidate, subject to technical validation), source control, and deterministic export builds. Keep the exact approved v6 files unchanged as reference versions.
- **Technical and visual QA:** browser automation plus direct inspection of rendered desktop/mobile scenes; full gameplay/negative paths, persistent consequences, export/save, keyboard and touch, reduced-motion, and fully offline testing. Automated success cannot establish artistic quality or real classroom usability by itself.

**Cost and permission rule:** Prefer available no-cost tools when they meet the standard. Check account/model availability and credit requirements before use. **Ask the teacher for approval before incurring new paid credits, enabling paid services, creating public deployments, or making other consequential/irreversible changes.** Existing plugin connectivity does not imply free or unlimited generation. Do not request approval for ordinary tool selection, internal edits, or QA operations.

**Teacher checkpoints:** Reserve approval for (a) material changes to curriculum/story direction, cost, or other consequential decisions, and (b) **one genuinely polished vertical slice** when introducing a major new interaction/engine/art architecture (such as the first v8 migration). After that approval, complete routine production and internal checks independently. Provide concise evidence-based reports rather than multiple unfinished prototypes. Do not claim work continues autonomously between conversations unless an authorized scheduled or delegated execution mechanism is actually running.

**Release rule:** A tool call, generated file, or passing automated test is not itself an accepted deliverable. Compare real outputs against these standards; reject inadequate output before scaling it; report remaining blockers honestly. No final/flagship claim while mandatory artwork, unit language, mechanics, offline packaging, or QA gates remain unsatisfied.

---

## 10. Acceptance checklist for a future *finished* game

Use these conditions as a release gate. Scale mechanical counts to project length and learners, without relaxing quality.

### Narrative and interaction

- [ ] The opening establishes a compelling mystery or consequential problem quickly.
- [ ] Travel and discoveries follow causal logic rather than chapter menus alone.
- [ ] The game has an original signature mechanic and several genuinely different puzzle actions.
- [ ] Each major decision alters a later playable state; alternate paths yield meaningfully different discoveries or outcomes.
- [ ] Recurring NPCs respond to the player's past behavior, and their accounts remain consistent with the evidence or intentionally deceptive in a traceable way.
- [ ] The central conflict is resolved; no mandatory route leads to an accidental dead end.

### Visuals and sound

- [ ] Every location has original, story-specific environment art; no borrowed *Far Horizon* scenery, generic placeholders, or promotional imagery used as backgrounds.
- [ ] Character identities, clothing, props, documents, timestamps, and geography remain visually and narratively consistent.
- [ ] Evidence objects are genuinely visible and inspectable, not just text descriptions in modal boxes.
- [ ] Important decisions visibly change at least one room, NPC encounter, route, or physical condition.
- [ ] Atmosphere/animation is purposeful, readable, optional or reducible where needed.
- [ ] Original music and SFX remain independently optional and start muted.

### Education

- [ ] Required unit vocabulary, grammar, reading, and writing goals are mapped to actual player actions.
- [ ] Students must understand/use English to solve real fictional problems rather than answer detachable worksheets.
- [ ] Scaffolding and Simplified Chinese glosses are accurate and appropriate to this class.
- [ ] Teacher notes explain the expected reasoning, supporting sources, acceptable alternatives, and what is/is not automatically assessed.

### Technical and evidence-based verification

- [ ] All essential assets load offline after opening the actual delivered files.
- [ ] All clickable hotspots, map routes, puzzles, decisions, hints, and endings work in browser interaction tests.
- [ ] Representative negative paths and state changes have been tested, not just the ideal route.
- [ ] Save/resume, student-work export, responsive layouts, accessibility, and sound controls are verified.
- [ ] No unacknowledged missing assets, broken links, external network dependencies, or untested promises remain.
- [ ] The delivered files are the exact files tested, with clear versioning and a brief QA report.

---

## 11. Illustrative integrated scenario: flood-control investigation

**Scene:** A newly renovated riverbank looks immaculate, but the maintenance warning lamp turns red while rain begins to fall.

**Investigate:** The player examines two separate visual exhibits—a physical water gauge and a dated pump log—then reads a resident survey and the engineer's written note. The records disagree about whether the repair was completed.

**Operate:** The player must read the repair instructions, route two valves, and assess which route protects which neighborhood. A wrong configuration causes a visible increase in downstream water, not an instant “incorrect” popup.

**Communicate:** The technician refuses to authorize an unverified repair. The player prepares a written maintenance order using required passive constructions and cites the actual gauge and log.

**Decide:** The student must choose between an expensive repair, a public evacuation warning, or withholding the report. Different paths change later streets, resources, residents, council dialogue, and available evidence.

**Discover:** A later photograph reveals the flood wall was installed earlier than the public report claims. The player now reinterprets evidence encountered in the opening scene.

**Educational core:** Reading comprehension, evidence evaluation, passive voice, community impact, and supported recommendation are all necessary to accomplish the fictional mission.

This is a **design example**, not a required story, textbook passage, or confirmed feature of any currently approved title.

---

## 12. How to use this document in the Project

**Read-first trigger for every future EAL game request:** At the start of any new EAL game proposal, revision, migration, build, tool-selection task, or release, **consult this current file before proposing code or generating assets**, alongside the exact approved v6 builds and unit sources. Apply the mandatory Tool Selection and Verification Record from Section 9, even if the teacher only says “build it” or “continue.” Where the canonical file is unavailable, request access to that source or document the block; never quietly edit an older version.

**Project-instructions reminder to install:** This requirement belongs in the ChatGPT Project's Instructions field *as well as this file*. A source document cannot by itself guarantee every future chat will retrieve it. Add the following compact permanent directive to Project Instructions:

> **EAL game read-first rule:** For every EAL game design, revision, coding, or release task, first inspect `EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md` (including its Section 9 tool-directed governance), `EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`, the exact two approved Living Environments v6 HTML files, and the relevant textbook pages/student profiles. Treat v6 as the minimum quality baseline. Internally choose and verify the right tools for art, animation, speech, gameplay, and QA; log acceptance evidence and blockers; do not silently downgrade or use older game sources. Build and verify one complete playable vertical slice before scaling. Ask the teacher only for consequential changes, costs, or first-time v8 creative-direction approval; do routine QA independently. Never claim final quality without checking the exact delivered files.

Keep this Markdown file attached to **EAL 2026–2027 → Project sources** alongside the approved v6 HTML builds and `EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`. Treat it as the **current forward-looking design standard** and the approved **Living Environments v6** editions as the **minimum visual, animation, offline, and mobile baselines**. Older Sound Editions remain archived references, not the default production benchmark.

For a new project, a short instruction is sufficient:

> Inspect the exact approved Living Environments v6 game files, `EAL_LIVING_ENVIRONMENTS_V6_APPROVED_REFERENCE.md`, the EAL Game Library, and `EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`. First map the authentic unit language to meaningful player actions, then design an original, cinematic, offline adventure with one signature mechanic, reactive environments, recurring NPCs, unique puzzles, and consequential branches. Internally test a representative playable section before expanding. Deliver only a complete, independently verified build with student export and teacher guidance.

When newer games are explicitly approved, archive them as additional quality benchmarks; do not silently overwrite the approved v6 or older Sound Editions. Keep the standards evolving upward without copying the same game structure each time.