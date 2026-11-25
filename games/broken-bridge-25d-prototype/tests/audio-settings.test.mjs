import test from 'node:test';
import assert from 'node:assert/strict';
import {fresh, restore} from '../src/state.mjs';

test('new and older missions get the quieter mix with music opt-in', () => {
  const freshSave=fresh();
  assert.equal(freshSave.sound.enabled,false);
  assert.equal(freshSave.sound.music,false);
  assert.equal(freshSave.sound.volumes.voice,100);
  assert.equal(freshSave.sound.volumes.master,100);
  assert.ok(freshSave.sound.volumes.ambience<=30);

  const older={version:1,id:'old',mode:'middle',fieldEdition:6,
    sound:{enabled:true,voice:false,ambience:true,effects:false}};
  const loaded=restore(JSON.stringify(older));
  assert.deepEqual(loaded.sound,{...freshSave.sound,enabled:true,voice:false,effects:false});
  const legacy=restore(JSON.stringify({version:1,mode:'elementary',mute:true}));
  assert.equal(legacy.sound.effects,false);
});

test('all saved volume levels round trip, and malformed values are bounded', () => {
  const save=fresh();
  save.sound.music=true;
  save.sound.volumes={master:0,voice:72,ambience:13,effects:34,music:57};
  assert.deepEqual(restore(JSON.stringify(save)).sound,save.sound);
  save.sound.volumes={...save.sound.volumes,master:106,voice:-12,ambience:'90'};
  const loaded=restore(JSON.stringify(save));
  assert.equal(loaded.sound.volumes.master,100);
  assert.equal(loaded.sound.volumes.voice,0);
  assert.equal(loaded.sound.volumes.ambience,fresh().sound.volumes.ambience);
  assert.equal(loaded.sound.volumes.music,57);
});
