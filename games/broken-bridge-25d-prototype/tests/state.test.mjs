import test from 'node:test';
import assert from 'node:assert/strict';
import {fresh, authorize, operate, restore} from '../src/state.mjs';

for (const [route, clues, pieces] of [
  ['bridge', ['bridge', 'rack'], ['boardA', 'boardB', 'rope']],
  ['ford', ['depth', 'sign'], ['postA', 'postB', 'pack']],
]) {
  test(route + ' requires evidence and ordered physical work', () => {
    const state = fresh('middle');
    assert.equal(authorize(state, route, clues, 'reason'), false);
    state.question = 'Where is the safe crossing?';
    state.clues = clues;
    assert.equal(authorize(state, route, clues.reverse(), 'reason'), true);
    assert.equal(operate(state, pieces[2]), false);
    assert.equal(operate(state, pieces[0]), true);
    assert.equal(operate(state, pieces[1]), true);
    assert.equal(operate(state, pieces[2]), true);
    assert.equal(restore(JSON.stringify(state)).delivered, true);
  });
}

test('rejects mismatched save versions and unsupported outcomes', () => {
  assert.equal(restore('{"version":2}'), null);
  const state = fresh();
  state.route = 'ford';
  state.pieces = ['postA', 'postB', 'pack'];
  state.delivered = true;
  assert.equal(restore(JSON.stringify(state)).delivered, false);
  assert.equal(authorize(state, 'constructor', [], 'invalid'), false);
});
