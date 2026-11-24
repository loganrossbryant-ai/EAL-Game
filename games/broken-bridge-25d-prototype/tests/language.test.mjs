import assert from 'node:assert/strict';
import test from 'node:test';
import { checkRecommendation, reviewRecommendations } from '../src/language.mjs';

test('elementary production accepts a short original or scaffolded sentence', () => {
  assert.deepEqual(checkRecommendation('elementary', ' The boards fit. '), {
    ok: true, message: 'The boards fit.', production: 'supported-elementary',
  });
  assert.equal(checkRecommendation('elementary', 'bridge').ok, false);
  assert.equal(checkRecommendation('elementary', 'I recommend').ok, false);
});

test('middle school production requires a short developed explanation', () => {
  assert.deepEqual(checkRecommendation('middle', 'I checked 16 cm at the ford.'), {
    ok: true, message: 'I checked 16 cm at the ford.', production: 'student-written',
  });
  assert.equal(checkRecommendation('middle', 'I recommend the ford.').ok, false);
  assert.equal(checkRecommendation('middle', 'I recommend the ford because').ok, false);
  assert.equal(checkRecommendation('middle', 'word word word word word').ok, false);
});

test('teacher exports distinguish legacy and unsubmitted attempts', () => {
  const legacy = { route: 'ford', message: 'We should use the ford because the water is shallow.', accepted: true };
  const current = { ...legacy, message: 'I checked 16 cm at the ford.', production: 'student-written' };
  const empty = { route: 'unsafe', message: '', accepted: false };
  assert.deepEqual(reviewRecommendations([legacy, current, empty]).map(({submissionSource, languageReview}) =>
    [submissionSource, languageReview]), [
    ['legacy-route-selection', 'not-applicable'],
    ['student-written', 'teacher-review'],
    ['no-student-output', 'not-applicable'],
  ]);
});
