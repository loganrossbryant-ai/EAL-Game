import test from 'node:test';
import assert from 'node:assert/strict';
import { STORAGE_KEY, initialState, loadProgress, saveProgress, evaluateResponse } from '../src/state.js';

function memoryStorage(initial) {
  let value = initial;
  return { getItem: (key) => key === STORAGE_KEY ? value : null, setItem: (key, next) => { assert.equal(key, STORAGE_KEY); value = next; } };
}
const evidence = ['campaign', 'request', 'email'];
const response = 'I recommend checking with Ms Chen before we share this campaign because her email mentions 48 families, while the campaign promotes 120 kits without explaining who needs them.';

test('saves and restores the actual student product, evidence, feedback, and history', () => {
  const storage = memoryStorage();
  const feedback = evaluateResponse({ response, decision: 'verify', evidence, sources: ['campaign', 'email'] });
  const state = { ...initialState, response, decision: 'verify', evidence, sources: ['campaign', 'email'], feedback, completed: true, room: 'courtyard', level: 2, position: { x: 450, y: 600 }, responses: [{ response, decision: 'verify', evidence, feedback, timestamp: '2026-10-28T12:00:00Z' }] };
  assert.equal(saveProgress(state, storage), true);
  const loaded = loadProgress(storage);
  assert.equal(loaded.response, response);
  assert.equal(loaded.completed, true);
  assert.equal(loaded.room, 'courtyard');
  assert.deepEqual(loaded.evidence, evidence);
  assert.deepEqual(loaded.sources, ['campaign', 'email']);
  assert.equal(loaded.responses[0].timestamp, '2026-10-28T12:00:00Z');
  assert.equal(loaded.level, 2);
  assert.deepEqual(loaded.position, { x: 450, y: 600 });
});

test('corrupt, old-version, and unavailable saves permit fresh play', () => {
  for (const raw of ['{broken', 'null', '[]', '{"version":9}', undefined]) {
    assert.equal(loadProgress(memoryStorage(raw)).completed, false);
    assert.deepEqual(loadProgress(memoryStorage(raw)).evidence, []);
  }
  const denied = { getItem() { throw new Error('disabled'); }, setItem() { throw new Error('quota'); } };
  assert.equal(loadProgress(denied).response, '');
  assert.equal(saveProgress(initialState, denied), false);
});

test('malformed fields cannot unlock the courtyard or contaminate state', () => {
  const loaded = loadProgress(memoryStorage(JSON.stringify({ version: 1, level: 99, evidence: ['campaign', 'bogus', 'campaign'], response: 9, completed: true, room: 'courtyard', position: { x: -10, y: 8 }, responses: [null, 'bad'] })));
  assert.equal(loaded.level, 3);
  assert.deepEqual(loaded.evidence, ['campaign']);
  assert.equal(loaded.response, '');
  assert.equal(loaded.completed, false);
  assert.equal(loaded.room, 'newsroom');
  assert.equal(loaded.position, null);
  assert.deepEqual(loaded.responses, []);
});

test('fresh saves have separate arrays', () => {
  const first = loadProgress(memoryStorage());
  first.evidence.push('campaign');
  first.sources.push('email');
  assert.deepEqual(loadProgress(memoryStorage()).evidence, []);
  assert.deepEqual(loadProgress(memoryStorage()).sources, []);
  assert.deepEqual(initialState.evidence, []);
  assert.deepEqual(initialState.sources, []);
});

test('keeps an earned completion and courtyard access while a new revision is drafted', () => {
  const storage = memoryStorage();
  const feedback = evaluateResponse({ response, decision: 'verify', evidence, sources: ['campaign', 'email'] });
  const state = {
    ...initialState,
    evidence,
    sources: ['campaign', 'email'],
    response: 'I am improving my recommendation',
    decision: 'verify',
    feedback: null,
    completed: true,
    room: 'courtyard',
    responses: [{ response, decision: 'verify', evidence, sources: ['campaign', 'email'], feedback, timestamp: '2026-10-28T12:00:00Z' }],
  };
  assert.equal(saveProgress(state, storage), true);
  const loaded = loadProgress(storage);
  assert.equal(loaded.completed, true);
  assert.equal(loaded.room, 'courtyard');
  assert.equal(loaded.feedback, null);
  assert.equal(loaded.response, state.response);
  assert.equal(loaded.responses[0].response, response);

  // An unsuccessful history item alone does not establish completion.
  state.responses[0].feedback = { ...feedback, passed: false };
  saveProgress(state, storage);
  assert.equal(loadProgress(storage).completed, false);
});

test('all three editorial choices can succeed with a developed, sourced explanation', () => {
  for (const decision of ['pause', 'publish', 'verify']) {
    assert.equal(evaluateResponse({ response, decision, evidence, sources: ['campaign', 'email'] }).passed, true);
  }
});

test('revision feedback identifies missing investigation, sources, language product, and detail', () => {
  const result = evaluateResponse({ response: 'I agree.', decision: '', evidence: ['campaign'], sources: ['campaign'] });
  assert.equal(result.passed, false);
  assert.equal(result.nextSteps.length, 5);
  assert.match(result.message, /do not grade your English/);
});

test('cannot cite an uncollected source or count repeated sources twice', () => {
  assert.equal(evaluateResponse({ response, decision: 'verify', evidence: ['campaign'], sources: ['campaign', 'email'] }).passed, false);
  const result = evaluateResponse({ response, decision: 'verify', evidence, sources: ['email', 'email'] });
  assert.equal(result.passed, false);
  assert.match(result.nextSteps.join(' '), /two different/);
});

test('accepts supported factual details but does not call unsupported numeric claims correct', () => {
  const base = 'I suggest we verify this message before sharing it with everyone at school because we should understand the campaign and use our resources carefully. ';
  for (const detail of ['Ms Chen requested blankets and supplies.', 'The campaign says 120 kits.', 'The site takes a 35% fee.', 'Ms Chen mentions 48 families.']) {
    assert.equal(evaluateResponse({ response: base + detail, decision: 'verify', evidence }).passed, true);
  }
  const unsupported = evaluateResponse({ response: base + 'There are 999 families.', decision: 'verify', evidence });
  assert.equal(unsupported.passed, false);
  assert.match(unsupported.nextSteps.join(' '), /specific source detail/);
});
