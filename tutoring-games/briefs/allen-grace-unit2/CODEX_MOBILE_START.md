# Codex mobile starter — Allen + Grace / Timezones 1A Unit 2

**Status:** Design handoff for a NEW game; NO game built or published.
**Source:** User-supplied correct Timezones 1A Unit 2 **"This Place Is Amazing!"** pp. 18–29. Exclude the older **"What Does She Look Like?"** screenshots (different learners). Package ID: `ALLEN-GRACE-TZ1A-U2-PLACES-V1`.

## Read before coding

Read `tutoring-games/AGENTS.md`, `tutoring-games/standards/QUALITY_STANDARD_V1.md`, `tutoring-games/standards/RELEASE_GATE.md`, applicable `.agents/skills/` instructions, and the read-only approved Zig benchmark. The benchmark is a RELEASE ARTIFACT, not proof of modular source availability. Preserve ALL previously approved games, images, recordings and public URLs. Start on this isolated feature branch.

**Important scope:** This single Markdown file is an accurate *mobile starter handoff*, NOT a replacement for inspecting the original PPT, classroom print pack, homework PDFs and full-resolution textbook screenshots. Do not claim those source files are in the repository; request or retrieve them before final curriculum parity review. The separately available 15 KB `Allen_Grace_Unit2_Codex_Mobile_Only.zip` contains exact full text-only game brief, 32-word language map, 25 interaction seeds and cross-resource parity table if the user can attach it later. Until then build ONE reviewed vertical slice using the verified language below and explicitly log missing artifacts.

## Learners

- Allen: Grade 1 EAL; can use familiar preference/reason structures with scaffolds.
- Grace: joining the group; proficiency UNKNOWN. Begin with a 5-minute diagnostic and an accessible CORE level. Provide separate anonymous local progress profiles; do not collect identifying information or pretend the diagnostic establishes formal WIDA scoring.
- Instruction is 120 minutes weekly. Lesson 1 primarily teaches pp.18–25. Pages 26–29 are future/extension and cannot introduce mandatory unmodeled knowledge.

## Verified language targets

| Target vocabulary (English — 简体中文) | Stage |
|---|---|
| city 城市, beach 海滩, building 建筑物, street 街道, island 岛 | CORE |
| big 大的, small 小的, beautiful 美丽的 | CORE |
| sea 海, store 商店, museum 博物馆, hotel 酒店, room 房间, tourists 游客, flag 旗帜, mountain 山, rock 岩石, famous 著名的, popular 受欢迎的 | EXPOSURE |
| boat 船, town 小镇, restaurant 餐馆, house 房子, tall 高的, long 长的, clean 干净的, colorful 五颜六色的, old 旧的／古老的, new 新的, interesting 有趣的, amazing 令人惊叹的 | GUIDED |
| underground 地下的／在地下 | STRETCH |

Sentence goals from classroom:
- CORE `This place is ___.` / `The buildings are ___.` / `Is it ___? Yes, it is. / No, it isn't.`
- GUIDED `Are the houses ___? Yes, they are. / No, they aren't.` / `It is ___ and ___.`
- STRETCH `It is small, but many people live there.` / `I like the beach because it is beautiful.` / `There is a restaurant on the island.`
- Distinguish singular `is/isn't` and plural `are/aren't`. Use logical adjective–noun matches, not arbitrary technically grammatical combinations.
- Phonics: /ɪ/ in `city, big, building` versus /iː/ in `sea, street, green`. Textbook calls /iː/ "long i" but DO NOT confuse it with /aɪ/ as in `bike`.

## Verified screenshot-grounded reading facts

- pp18–19: Rio de Janeiro coast/city and vocabulary `sea, beach, building, store, city, street`.
- pp20–21: Amsterdam conversation includes big city, colorful buildings, NEMO Science Museum; singular/plural `be`, negative forms, yes/no questions. Mexico City plaza photo supports question writing.
- pp22–23: World landmarks and vowel listening; actual textbook VIDEO/AUDIO not supplied, so do not invent their answers.
- p24 Santa Cruz del Islote: small Colombian island, reached by boat from Cartagena, more than 1,000 people live there, school, two stores and a restaurant.
- p25 Coober Pedy: small Australian town reached by car from Adelaide, underground houses, stores and hotels; about 1,500 people live in underground houses.
- pp26–27: compare/contrast with `and/but`, comprehension and a place poster — later scaffolded application.
- pp28–29: Ha Long Bay images and video review — future lesson. Do not require video answers without the video.

## Early-to-late curriculum arc (proposal, not quotas)

Game working title: **Atlas Rescue: The Missing Postcards**. A flying atlas loses location postcards; the learner explores visually coherent, detailed environments, gathers clues, restores captions and sees meaningful scene changes.

1. **City Harbor (FIRST vertical slice):** city, beach, building, street; `This place is beautiful`; `The buildings are tall`; `Is it a beach?`; hints, phonics, optional `and` stretch. Target complex sentence models START HERE.
2. Colorful Streets: `is/are`, `isn't/aren't`, `Are they...?`, adjective-based clue inference.
3. Island Village: short adapted Santa Cruz reading, `boat/restaurant/island`, `and/but`.
4. Underground Town: Coober Pedy reading, compare places with evidence, short reasons.
5. Wonder Bay finale only AFTER relevant classroom language introduced: supported connected explanation; not mandatory in initial slice.

Do not copy Zig's exact 5-world or 128-round scale; use the benchmark's artistic, interactive and instructional *quality*, not its content quotas.

## First task for Codex — build ONLY one City Harbor playable slice

- Original high-quality child-friendly world scene (do not falsely label generated/placeholders as approved textbook art), simple tap/keyboard navigation, coherent objective, working progress consequence.
- Implement 3 CORE language interactions, 1 evidenced inference clue with accessible reread, 1 `Is it...? / Are they...?` exchange, and 1 nonmandatory `and/but` or meaningful reason STRETCH.
- Show Chinese meaning support when appropriate; record whether hints were used. Correct answers must be deterministically supported by displayed photo/text/clues; reasonable alternatives accepted.
- Separate anonymous local saves for Allen and Grace; clear retry and teacher progress readout.
- Speaking participation tap is NOT microphone recognition or pronunciation scoring.
- Retain existing approved Jesse recordings **only if identical line**. Queue every new mandatory voice line for genuine Jesse audio; no chopped clips or undisclosed browser TTS. Missing mandatory audio means CLASSROOM PILOT, not HOME RELEASE.
- Run syntax/data validation, actual clickable UI navigation and wrong-answer retry tests, completion and reset tests, mobile-size screenshots, Chinese glyph test, content fairness check and audio manifest; record PASS/FAIL/NOT TESTED.
- Preserve existing releases and leave public deployment untouched. Stop after the vertical slice; provide screenshots, source commit, change log, incomplete-source list and QA evidence for approval.

## Quick parity anchors (first slice)

| Objective | Textbook | PPT slides | Print pages | Homework | Game |
|---|---|---|---|---|---|
| city/beach/building/street | p18 | S4, S6–8, S12–14, S28 | P2–4, P7–8 | D1 #1–3, D2 #1–2 | Harbor |
| `This place is...` | p20–21 | S5, S15–18 | P5–6 | D1 #4/#6/#7, D2 #5 | Harbor |
| `The buildings are...` | p20–21 | S5, S16–18 | P5–6 | D1 #5, D2 #4/#6 | Harbor |
| `Is it...` / `Are they...` | p21 | S3, S14, S17–18 | P6, P8 | D2 #3–4/#7 | Harbor |
| short /ɪ/ vs long /iː/ | p23 | S21–23 | P9 | D2 #1–2 | Harbor sound probe |
| `and/but` | p26–27 plus prior lesson | S3, S19, S24 | P6, P12 | D3 #3 stretch | Harbor OPTIONAL |

The references are from the current source package's initial cross-resource map; revalidate against the actual PPT/print/homework when accessible. Do not state full classroom–game parity until then.

## Definition of successful first milestone

A runnable local demo and visible screenshots; tested clickable traversal, real image/clue evidence, accessible CORE completion and optional STRETCH, independent local profiles, reasonable answer feedback, teacher progress, explicit missing-audio list, no modifications to approved games. **No full-game production and no parent release in this task.**
