import test from 'node:test';
import assert from 'node:assert/strict';
import {fresh, restore, authorize} from '../src/state.mjs';
import {readProbe, recordDepth, compareDepth, reviewLog, checkRig, readyForPermit} from '../src/survey.mjs';

function survey(state) {
  assert.ok(recordDepth(state.survey,'bridge',40));
  assert.ok(recordDepth(state.survey,'ford',25));
  assert.ok(compareDepth(state.survey,'ford','below'));
}

test('a waterline reading requires bed contact and clamps to the sounding depth', () => {
  assert.deepEqual(readProbe('bridge',31),{depth:31,contact:false});
  assert.deepEqual(readProbe('bridge',44),{depth:38,contact:true});
  assert.deepEqual(readProbe('ford',18),{depth:16,contact:true});
  assert.equal(readProbe('unknown',30),null);
  assert.equal(readProbe('ford',NaN),null);
});

test('the survey requires two physical readings and a correct comparison with the posted limit', () => {
  const {survey:s}=fresh();
  assert.equal(recordDepth(s,'bridge',30),false);
  assert.equal(recordDepth(s,'ford',24),true);
  assert.equal(compareDepth(s,'ford','below'),false);
  assert.equal(recordDepth(s,'bridge',42),true);
  assert.equal(compareDepth(s,'bridge','below'),false);
  assert.equal(compareDepth(s,'ford','above'),false);
  assert.equal(compareDepth(s,'ford','below'),true);
  assert.deepEqual(s.readings,{ford:16,bridge:38});
});

test('Lin changes her permit only after direct comparison of the dated log and sounding', () => {
  const s=fresh('middle');
  assert.equal(readyForPermit(s),false);
  survey(s);
  s.survey.asked=true;
  const proof=['log','sounding'];
  for (const [sources, note] of [
    [['log','rack'],'Today it is 16 cm, below the 20 cm limit.'],
    [proof,'Today it is 26 cm, below the 20 cm limit.'],
    [proof,'Today 16 cm is not below 20 cm.'],
    [proof,'Today 16 cm. Apples are below twenty.'],
  ]) assert.equal(reviewLog(s.survey,sources,note).ok,false,note);
  assert.equal(readyForPermit(s),false);
  assert.equal(reviewLog(s.survey,proof,'Today the ford is 16 cm, which is less than 20 cm.').ok,true);
  assert.equal(readyForPermit(s),true);
  const resumed=restore(JSON.stringify(s));
  assert.equal(readyForPermit(resumed),true);
  assert.deepEqual(resumed.survey.interview.at(-1).sources,proof);
  assert.equal(resumed.survey.interview.at(-1).output,'constructed');
});

test('fresh route approval needs the current safety permit but legacy saves can continue', () => {
  const s=fresh('elementary');
  s.question='Can you help me?';
  s.clues=['bridge','rack'];
  const claim={fact:'matching-boards',inference:'fill-sockets'};
  assert.equal(authorize(s,'bridge',s.clues,'Both boards are 90 cm.',claim),false);
  const {fieldEdition,survey:_,...prior}=s;
  const legacy=restore(JSON.stringify(prior));
  assert.equal(readyForPermit(legacy),true);
  assert.equal(authorize(legacy,'bridge',legacy.clues,'Both boards are 90 cm.',claim),true);
});

test('rigging needs the fairlead and far cleat within the safe load band', () => {
  assert.equal(checkRig('outer',true,65),'edge');
  assert.equal(checkRig('inner',false,65),'cleat');
  assert.equal(checkRig('inner',true,45),'slack');
  assert.equal(checkRig('inner',true,87),'strain');
  assert.equal(checkRig('inner',true,60),'secure');
  assert.equal(checkRig('inner',true,74),'secure');
  assert.equal(checkRig('inner',true,NaN),'slack');
});
