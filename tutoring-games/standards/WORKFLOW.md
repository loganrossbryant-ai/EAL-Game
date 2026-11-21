# Reusable tutoring-game production workflow

## 0. Identify the correct starting point
Check the latest classroom slides, printed pages, homework and game source, plus parent/student feedback. Read the relevant `AGENTS.md`. Inventory the last approved release and test evidence. Never assume the newest filename means the latest approved release.

## 1. Freeze the design brief
Write a one-page brief: learner age/level, targeted lessons/textbook pages, theme/world, minimum required interactions, language stages, CORE/STRETCH, help and bilingual policy, assets/voice restrictions, offline device, teacher assessment and endings. Resolve only consequential creative questions.

## 2. Prepare a language map (before code)
A row for each high-priority target: word/phrase, Chinese, intended production level, lesson/PPT/print/homework refs, opening/game stage(s), task text, correct answers, clue evidence, voice line. Flag where source content mismatches the new game scope.

## 3. Edit as small patches
Preserve approved art/navigation/recordings and avoid rewriting game architecture unless a source refactor is explicitly justified. Changes must be traceable to the language map and pass a content fairness check. Use an isolated git branch and keep old files/builds intact.

## 4. Run incremental QA after each item
Content validator and code syntax → individual new modes → full world and finale → original feature regression → mobile screenshot inspection → audio lookup/playback → offline/HTTPS → real device. Fix issues found, rerun affected tests and dependent smoke tests.

## 5. Deliver only verified states
Provide a versioned ZIP, browser build, teacher guide/instructions, release report and changelog. Preserve rollback to previous approved version. Label unvoiced or untested builds CLASSROOM PILOT, not HOME RELEASE.
