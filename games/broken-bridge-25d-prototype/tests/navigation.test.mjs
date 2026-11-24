import test from 'node:test';
import assert from 'node:assert/strict';
import {canWalk, canTravel, crossingPaths, pathTo, recoverFoot, targetFoot} from '../src/navigation.mjs';

for (const route of ['bridge','ford']) {
  test(route+' crossing connects two walkable banks without opening water or background', () => {
    const state={route,delivered:true,pieces:[]};
    const crossing=crossingPaths[route];
    const far=crossing.at(-1);
    const path=pathTo(state,[278,449],far);
    assert.ok(path);
    assert.deepEqual(path.at(-1),far);
    for (let i=0;i<path.length;i++)
      assert.ok(canTravel(state,i===0?[278,449]:path[i-1],path[i]));
    assert.ok(pathTo(state,far,[278,449]));
    assert.equal(canTravel(state,[620,430],[620,290]),false);
    assert.equal(canWalk({...state,delivered:false},...far),false);
    for(const point of [[450,202],[829,230],[570,349],[1070,468],[900,510]]) {
      assert.equal(canWalk(state,...point),false);
      assert.equal(targetFoot(state,...point)?.join(',')===point.join(','),false);
    }
    assert.equal(targetFoot(state,far[0],210),null);
    const recovered=recoverFoot(state,far[0],202);
    assert.ok(canWalk(state,...recovered));
    assert.ok(recovered[1]>=267&&recovered[1]<=315);
  });
}

test('placing the near flag opens only the marked ford during fieldwork', () => {
  const state={route:'ford',delivered:false,pieces:['postA']};
  assert.ok(pathTo(state,[956,425],[829,299]));
  assert.equal(canWalk(state,450,360),false);
});
