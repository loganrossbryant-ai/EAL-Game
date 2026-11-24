import test from 'node:test';
import assert from 'node:assert/strict';
import {fresh, authorize, operate, restore} from '../src/state.mjs';

const bridgeClaim={fact:'matching-boards',inference:'fill-sockets'};
const fordClaim={fact:'ford-depth',inference:'use-shallows'};
for (const [route, clues, pieces, message, claim] of [
  ['bridge', ['bridge', 'rack'], ['boardA', 'boardB', 'rope'], 'The boards match the sockets.', bridgeClaim],
  ['ford', ['depth', 'sign'], ['postA', 'postB', 'pack'], 'I measured 16 cm at the ford.', fordClaim],
]) {
  test(route + ' requires evidence and ordered physical work', () => {
    const state = fresh('middle');
    assert.equal(authorize(state, route, clues, message, claim), false);
    state.question = 'Where is the safe crossing?';
    state.clues = clues;
    assert.equal(authorize(state, route, [...clues].reverse(), message, claim), true);
    assert.equal(operate(state, pieces[2]), false);
    assert.equal(operate(state, pieces[0]), true);
    assert.equal(operate(state, pieces[1]), true);
    assert.equal(operate(state, pieces[2]), true);
    const saved=restore(JSON.stringify(state));
    assert.equal(saved.delivered,true);
    assert.deepEqual(saved.attempts.at(-1),{
      route,cited:[...clues].reverse(),message,accepted:true,production:'student-written',...claim,
    });
  });
}

test('direct authorization rejects the audit nonsense and missing claim', () => {
  for(const [mode,text] of [['elementary','Cat dog tree'],['middle','Cat dog tree fish bird']]) {
    const state=fresh(mode);
    state.question='Where is the safe crossing?';
    state.clues=['bridge','rack'];
    assert.equal(authorize(state,'bridge',state.clues,text,bridgeClaim),false);
    assert.equal(authorize(state,'bridge',state.clues,'The boards match the sockets.'),false);
    assert.equal(state.route,null);
  }
});

test('legacy authorized save remains resumable before and after delivery', () => {
  const state=fresh('elementary');
  state.question='Can you help me?';
  state.clues=['bridge','rack'];
  state.route='bridge';
  state.attempts=[{route:'bridge',cited:state.clues,message:'The boards fit.',accepted:true}];
  assert.equal(restore(JSON.stringify(state)).route,'bridge');
  state.pieces=['boardA','boardB','rope'];
  state.complete=true;
  const saved=restore(JSON.stringify(state));
  assert.equal(saved.complete,true);
  assert.deepEqual(saved.attempts,state.attempts);
  state.attempts[0].production='supported-elementary';
  assert.deepEqual(restore(JSON.stringify(state)).attempts,state.attempts);
});

test('save keeps the last 100 valid physical action records only', () => {
  const state=fresh();
  const action={action:'collected',piece:'boardA',route:'bridge',assisted:false,method:'tap'};
  const latest={...action,action:'placed',assisted:true,method:'guide'};
  state.fieldActions=[...Array(130).fill(action),{...action,piece:'pack'},{...action,method:'strange'},latest];
  const saved=restore(JSON.stringify(state));
  assert.equal(saved.fieldActions.length,100);
  assert.deepEqual(saved.fieldActions.at(-1),latest);
  assert.deepEqual(saved.fieldActions.at(0),action);
});

test('rejects mismatched save versions and unsupported outcomes', () => {
  assert.equal(restore('{"version":2}'), null);
  const state = fresh();
  state.route = 'ford';
  state.pieces = ['postA', 'postB', 'pack'];
  state.delivered = true;
  assert.equal(restore(JSON.stringify(state)).delivered, false);
  assert.equal(authorize(state, 'constructor', [], 'invalid'), false);
});
