import assert from 'node:assert/strict';
import test from 'node:test';
import { checkRecommendation, reviewRecommendations } from '../src/language.mjs';

const boards = { route: 'bridge', fact: 'matching-boards', inference: 'fill-sockets' };
const supports = { route: 'bridge', fact: 'sound-supports', inference: 'repair-deck' };
const depth = { route: 'ford', fact: 'ford-depth', inference: 'use-shallows' };
const stones = { route: 'ford', fact: 'white-stones', inference: 'flag-stones' };

test('rejects the exact elementary and middle audit nonsense with correct claim slots', () => {
  assert.equal(checkRecommendation('elementary', 'Cat dog tree', boards).ok, false);
  assert.equal(checkRecommendation('middle', 'Cat dog tree fish bird', boards).ok, false);
  assert.equal(checkRecommendation('middle', 'Cat dog tree fish bird bridge', boards).ok, false);
});

test('elementary production accepts short supported observations and synonyms', () => {
  assert.deepEqual(checkRecommendation('elementary', ' The boards fit. ', boards), {
    ok: true, message: 'The boards fit.', production: 'supported-elementary',
    fact: 'matching-boards', inference: 'fill-sockets',
  });
  assert.equal(checkRecommendation('elementary', 'Two planks match.', boards).ok, true);
  assert.equal(checkRecommendation('elementary', 'The beams are still strong.', supports).ok, true);
  assert.equal(checkRecommendation('elementary', 'I saw white rocks.', stones).ok, true);
  assert.equal(checkRecommendation('elementary', 'Bridge', boards).ok, false);
});

test('middle production accepts independent detail, synonyms and compatible unit equivalents', () => {
  assert.equal(checkRecommendation('middle','We can fill the gap with 90-centimetre planks.',boards).ok,true);
  assert.equal(checkRecommendation('middle','The deck needs planks measuring ninety centimeters.',boards).ok,true);
  assert.equal(checkRecommendation('middle','The two planks are 0.9 m long.',boards).ok,true);
  assert.equal(checkRecommendation('middle','The bridge framing is intact, so repair the deck.',supports).ok,true);
  assert.equal(checkRecommendation('middle','The support beams were not damaged.',supports).ok,true);
  assert.equal(checkRecommendation('middle','I checked 16 cm at the ford.',depth).ok,true);
  assert.equal(checkRecommendation('middle','The ford is shallow and under the limit.',depth).ok,true);
  assert.equal(checkRecommendation('middle','The bridge is 38 cm and the ford is 16 cm.',depth).ok,true);
  assert.equal(checkRecommendation('middle','The bridge is too deep but the ford is shallow.',depth).ok,true);
  assert.equal(checkRecommendation('middle','The crossing is only 160 millimeters deep.',depth).ok,true);
  assert.equal(checkRecommendation('middle','Follow the stepping stones and mark both ends.',stones).ok,true);
});

test('chosen fact, inference and wording must support the same route', () => {
  assert.equal(checkRecommendation('middle','I checked 16 cm at the ford.',boards).ok,false);
  assert.equal(checkRecommendation('middle','The boards do not fit the sockets.',boards).ok,false);
  assert.equal(checkRecommendation('middle','The boards are 80 cm and they fit.',boards).ok,false);
  assert.equal(checkRecommendation('middle','The boards are 80 cm but the gap is 90 cm.',boards).ok,false);
  assert.equal(checkRecommendation('middle','The supports are broken and unsafe.',supports).ok,false);
  assert.equal(checkRecommendation('middle','The ford is shallow at 38 cm.',depth).ok,false);
  assert.equal(checkRecommendation('middle','The bridge is 16 cm but the ford is 38 cm.',depth).ok,false);
  assert.equal(checkRecommendation('middle','The ford is not shallow enough.',depth).ok,false);
  assert.equal(checkRecommendation('middle','There are no white stones here.',stones).ok,false);
  assert.equal(checkRecommendation('middle','The boards fit the bridge.',{...boards,inference:'use-shallows'}).ok,false);
  assert.equal(checkRecommendation('middle','The boards fit the bridge.',{...boards,fact:'short-boards'}).ok,false);
  assert.equal(checkRecommendation('middle','The boards fit the bridge.',{route:'bridge'}).ok,false);
  assert.equal(checkRecommendation('middle','I recommend the ford because',depth).ok,false);
});

test('teacher exports distinguish structured, prior student, legacy and empty attempts', () => {
  const legacy = { route: 'ford', message: 'We should use the ford because the water is shallow.', accepted: true };
  const olderStudent = { ...legacy, message: 'I checked 16 cm at the ford.', production: 'student-written' };
  const current = { ...olderStudent, fact: 'ford-depth', inference: 'use-shallows' };
  const empty = { route: 'unsafe', message: '', accepted: false };
  assert.deepEqual(reviewRecommendations([legacy, olderStudent, current, empty]).map(
    ({submissionSource, languageReview, structuredEvidence})=>[submissionSource,languageReview,structuredEvidence]), [
    ['legacy-route-selection', 'not-applicable', null],
    ['student-written', 'teacher-review', null],
    ['student-written', 'teacher-review', { fact:'ford-depth', inference:'use-shallows' }],
    ['no-student-output', 'not-applicable', null],
  ]);
});
