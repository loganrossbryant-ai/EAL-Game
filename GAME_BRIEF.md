# GAME_BRIEF.md — EAL 2026–2027 Next-Generation Browser Adventures

**Status:** Standing reusable development brief; revised 2026-11-08. Read with `AGENTS.md` and `docs/EAL_NEXT_GENERATION_GAME_QUALITY_STANDARD.md`. This is NOT a script for a particular class or a requirement to re-create prior games.

## Purpose and creative promise
Create an original story-rich browser adventure that would be compelling **without a grade**. Students use reading, English communication, evidence interpretation and unit grammar to repair, negotiate, investigate, escape, build, or change an explorable fictional world. The approved Sound Editions are the minimum quality floor, not content or mechanic templates.

### Authoritative source order
1. User's latest explicit instructions and actual current student/class profile.
2. Actual photographed/uploaded textbook unit pages and objectives; cite internally where required language comes from.
3. Approved game files and the Project's detailed next-generation standard.
4. Existing repository source and tests, for reusable engineering components.
5. Original invented narrative and enrichment language, explicitly classified as such.

If textbooks, artwork or reference files are only in a ChatGPT Project, Codex must **receive an accessible copy**; a linked GitHub repo alone does not import Project sources. Do not infer anything not actually inspected.

## Non-negotiable player experience
- **Fast playable hook:** a compelling impossible event or consequential crisis within the opening moments; minimal teacher-facing exposition in the student UI.
- **Connected world:** recognisable spatial geography, navigation, meaningful revisits, environmental storytelling, cinematic story-specific assets. No mockups/screenshots pretending to be gameplay scenery.
- **Physical interaction:** a unique signature system plus several different verbs (rotate, tune, trace, rebuild, interview, calibrate, compare, negotiate); credible manipulable devices and authentic-world documents, not a procession of quizzes.
- **Visible reactivity:** important choices and written actions change a room, relationship, route, resource, or evidence later on; saved state and alternate meaningful pathways, no cosmetic-only endings.
- **Believable people:** small recurring cast with conditional speech, motives, relationships and persistent behaviors; distinguish testimony from verified evidence.
- **Escalating drama:** coherent causal discoveries, reversal of an early belief, a costly decision, and satisfying resolution including evidence-based alternate outcomes.
- **Immersive audiovisuals:** layered 2D/2.5D scenery, prop closeups, relevant ambience and restrained original sound effects, separate mute/volume controls default OFF, optional motion-reduced setting.
- **Student access:** English text stays legible, optional Simplified Chinese academic glosses and hints, no rapid-reading timers or audio-only educational information.

## Educational gameplay design contract
For each required objective, record source, vocabulary/grammar, in-world action, evidence of use, and feedback/teacher verification. Natural actions: read a technician's work order to configure machinery, write a warning that changes evacuation behavior, explain a misleading source to convince a journalist, repair a web directory for an actual user. Writing has recipient, factual constraints, purpose and visible result. Offline validators can check structured evidence and completion; they are NOT automatic reasoning/quality grades. Preserve responses for teacher review.

Adapt to each student group. The previous classes are useful examples but not defaults: Grade 9–10 could tolerate independent evidence reasoning; Grade 11–12 may need more visual agency and shorter guided productions. Required language must come from **that** new unit, not the old briefs.

## Architecture and packaging
Reuse the `codex/signal-playable-demo` branch as **engineering reference**: Phaser 3, React, Vite, Playwright, local save and a single-file demo build already exist there. Do not assume this demo has approved visuals, complete branches, or verified textbook language. Choose Phaser+HTML when movement/camera/hotspots matter; a robust self-contained vanilla HTML game is also acceptable for a smaller adventure. Commit to a new branch rather than disrupting other projects. Package everything offline: scripts, fonts, environmental images, animation, soundtrack, SFX and data. Require save/resume, teacher-readable export, accessible interaction and tested delivery artifacts.

## Required design artifacts (primarily internal)
- Curriculum source audit + `target language → player action` matrix.
- Art-direction sheet + named location/prop shot list + consistent NPC references.
- Location graph, clue provenance table, story reversal, branch-state machine and ending conditions.
- Distinct puzzle contract for each major interaction: cause in-world; controls; evidence and language; feedback/failure; hint sequence; persistent consequence; teacher answer rationale.
- Internal vertical slice that meets art and functionality standards before creating the whole game.
- Automated browser QA plus actual visual review, negative paths, exports, responsive layout and no-network test of release package.

## Release acceptance
A new title is not finished until all promised narrative branches, scenes, puzzles, source-aligned English actions, save/export, offline assets and sound controls work and have been verified. Submit the exact tested package with versioned filename and a short QA summary that distinguishes **built**, **browser-tested**, **visually inspected**, and **unverified** items. Do not present missing materials, synthetic test completions or proposed features as already completed.

## Approved reference catalogue
- **The Town That Rebuilds Itself — Sound Edition** (9–10 Community Builders): full visual/audio/technical benchmark.
- **Do Not Answer Your Own Voice — Sound Edition** (11–12 Secrets and Lies): full visual/audio/technical benchmark.
- **A Town Worth Staying In** (11–12 Development): simulation/decision design reference. Archived prior source distribution missing some external art.
- **The Internet of a Missing Town / Greyhaven** (9–10 Designing the Web): website mechanics and provenance design reference; archived prior source distribution missing some external art.
- **Far Horizon**: photographic ambition benchmark **only**, not source art to borrow.

## Demo without a new unit
When asked to demonstrate capability before a unit is selected, deliver a **self-contained, finished short play experience** that shows physical interaction, a signature mechanic, changing world states, language-use consequences, NPC agency, alternate outcomes, original environmental art, sound and offline reliability. Mark vocabulary as **illustrative / not textbook-verified**. Never present this as a finished curriculum-aligned class game without real unit pages.