import {fresh, restore, authorize, ROUTES, SAVE_KEY} from './state.mjs';
import {language, repair, sites} from './content.mjs';
import {mountWorld, RANGER_DELIVERY_MS} from './world.mjs';
import {createFieldwork} from './fieldwork.mjs';
import {recommendationFields, wireRecommendation, readRecommendation, reviewRecommendations} from './language.mjs';
import {lines} from './dialogue.mjs';
import {instructionLines} from './instructions.mjs';

const $ = id => document.getElementById(id);
const panel = $('panel'), body = $('panel-body'), stage = $('stage');
const preferredMotion = matchMedia('(prefers-reduced-motion: reduce)');
const read = () => {
  try { return restore(localStorage.getItem(SAVE_KEY)); } catch { return null; }
};
let state = read();
let scene, active, toastTimer, audio, output, speakingClip, voiceNonce=0;
const pins = {};
const motion = () => state?.motion ?? !preferredMotion.matches;
const profile = () => language[state.mode];
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const zh = text => state.zh ? ` <span lang="zh-Hans" class="zh">${text}</span>` : '';
const button = (text, action, cls = '') => `<button data-action="${action}" class="${cls}">${text}</button>`;
const actions = (...buttons) => `<div class="actions">${buttons.join('')}</div>`;
const workId = () => state?.route && repair[state.route].site;
const allLines={...lines,...instructionLines};
const fieldwork=createFieldwork({
  stage, texture:ART, state:()=>state, paused:()=>panel.open, motion,
  onActivity:event=>{state.fieldActions=[...(state.fieldActions??[]),event].slice(-100);save();},
  onGuideVoice:replayVoice,
  walk:(x,y,id)=>{scene?.walk(x,y,id);stage.focus({preventScroll:true});},
  notify,
  onPlaced:()=>{save();updateMission();audioFeedback(430);},
  onDelivered:crossingReady,
});

function stopVoice() {
  voiceNonce++;
  speakingClip?.pause();
  speakingClip=null;
}
function replayVoice(id) {
  if(!VOICE[id]) return;
  stopVoice();
  const clip=new Audio(VOICE[id]);
  speakingClip=clip;
  const nonce=voiceNonce;
  if(id.startsWith('guide')&&!panel.open) {
    const show=()=>{if(nonce===voiceNonce)notify(allLines[id],Math.max(7000,clip.duration*1000));};
    clip.addEventListener('loadedmetadata',show,{once:true});
  }
  clip.play().catch(()=>{
    if(nonce===voiceNonce) notify('Audio could not play. The full caption is on screen.');
  });
}
function caption(id) {
  return `<div class="voiced-line"><p class="speech">${allLines[id]}</p>${
    VOICE[id]?button('Replay Ranger Lin','voice-'+id,'voice-replay'):''}</div>`;
}
function guideVoice(id) {
  return VOICE[id]?`<p class="small">${allLines[id]}</p>`+button('Hear instructions','voice-'+id,'voice-replay'):'';
}
function voicedFeedback(id, prefix='') {
  feedback(prefix+allLines[id]);
  if(VOICE[id]) $('feedback').insertAdjacentHTML('beforeend',button('Replay Ranger Lin','voice-'+id,'voice-replay'));
}
function crossingReady() {
  const bridge=state.route==='bridge';
  open(bridge?'The bridge is open':'The ford is marked','CROSSING READY',
    `<p>${bridge?'The deck is repaired. Ranger Lin is taking the supplies over the bridge.':
      'Your flags mark the safe line. Ranger Lin is taking the supplies along the white stones.'}</p>`+
    actions(button('Watch the crossing','close','primary')),close);
}

for (const [id,site] of Object.entries(sites)) {
  const pin = document.createElement('button');
  pin.className = 'pin';
  pin.setAttribute('aria-label', site.name);
  pin.innerHTML = `<span class="site-mark" aria-hidden="true">${site.icon}</span><span class="pin-label">${site.name}</span>`;
  pin.addEventListener('click', () => approach(id));
  $('pins').append(pin);
  pins[id] = pin;
}

function save() {
  if (!state) return false;
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); return true; } catch { return false; }
}
function audioFeedback(note = 420) {
  if (!state || state.mute) return;
  try {
    const Audio = window.AudioContext || window.webkitAudioContext;
    audio ??= new Audio();
    void audio.resume().catch(() => {});
    if(!output){output=audio.createGain();output.connect(audio.destination);}
    output.gain.value = .24;
    const tone = audio.createOscillator(), envelope = audio.createGain();
    tone.type = 'sine';
    tone.frequency.setValueAtTime(note, audio.currentTime);
    tone.frequency.exponentialRampToValueAtTime(note*.69, audio.currentTime+.18);
    envelope.gain.setValueAtTime(.13, audio.currentTime);
    envelope.gain.exponentialRampToValueAtTime(.001, audio.currentTime+.22);
    tone.connect(envelope); envelope.connect(output);
    tone.onended = () => { tone.disconnect(); envelope.disconnect(); };
    tone.start(); tone.stop(audio.currentTime+.23);
  } catch { /* Audio is optional. */ }
}

function updateMission() {
  if(!state) return;
  let objective = 'Meet Ranger Lin';
  let instruction = 'A storm took out the bridge. Supplies must reach the lookout.';
  if(state.question) {
    objective = 'Find a way across';
    instruction = 'Inspect the bridge and tool rack, or compare the depth marker and fallen sign. Then report back.';
  }
  if(state.route) {
    objective = repair[state.route].name;
    instruction = state.route === 'bridge' ? 'Collect a board at the rack, carry it to the bridge, and fit it into a socket.'
      : 'Return to the fallen sign and mark both ends of the white-stone path.';
  }
  if(state.delivered) {
    objective = 'Report to the ranger';
    instruction = 'The supplies reached the lookout. Return to the clearing to finish your field report.';
  }
  if(state.complete) {
    objective = 'Supplies delivered';
    instruction = state.route==='bridge' ? 'The repaired bridge is open. Export your record from the field log.'
      : 'The white-stone ford is marked. Export your record from the field log.';
  }
  $('objective').textContent = objective;
  $('instruction').textContent = instruction;
  $('count').textContent = state.clues.length+' / 4';
}

function open(title, kicker, html, onAction, type='') {
  stopVoice();
  active={onAction,type};
  panel.classList.toggle('cinematic',type==='conversation');
  $('panel-title').textContent=title;
  $('panel-kicker').textContent=kicker;
  body.innerHTML=html;
  $('close').hidden=type==='start';
  if (!panel.open) panel.showModal();
  panel.scrollTop=0;
  (type==='start'?body.querySelector('button'):$('close'))?.focus({preventScroll:true});
  scene?.keys.clear();
  if(scene) scene.goal=null;
}
function close() { if(active?.type!=='start') panel.close(); }
function notify(message,duration=3600) {
  const notice=$('notice');
  notice.textContent=message;
  notice.hidden=false;
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>{notice.hidden=true;},duration);
}
function feedback(message) {
  const node=$('feedback');
  node.hidden=false;
  node.textContent=message;
}
const feedbackBox='<p id="feedback" role="status" hidden></p>';

body.addEventListener('click',event=>{
  const action=event.target.closest('button[data-action]')?.dataset.action;
  if(action?.startsWith('voice-')) return replayVoice(action.slice(6));
  if(action) active?.onAction(action);
});
$('close').addEventListener('click',close);
panel.addEventListener('cancel',event=>{event.preventDefault();close();});
panel.addEventListener('close',()=>{stopVoice();active=null; stage.focus({preventScroll:true});});
stage.tabIndex=-1;

function launch() {
  open('Choose your field guide','ALDER RIVER STATION',
    '<p>Last night the river rose. The lookout is running low on supplies, and Ranger Lin needs your help finding a way across.</p>'+
    `<div class="stack">${button('Elementary · supported English','elementary','primary')}${button('Middle school · field investigation','middle')}</div>`,
    mode=>{
      state=fresh(mode); active.type=''; close(); save(); updateMission();
      stage.focus({preventScroll:true});
    },'start');
}
function approach(id) {
  if (!scene || panel.open || !state || !sites[id]) return;
  const site=sites[id];
  scene.walk(site.x+(id==='ranger'?29:0),site.y+(id==='ranger'?16:9),id);
  stage.focus({preventScroll:true});
}
function nearest() {
  if(!state) return null;
  let best=null,distance=54;
  for(const [id,site] of Object.entries(sites)) {
    const d=Math.hypot(site.x-state.x,site.y-state.y);
    if(d<distance){best=id;distance=d;}
  }
  return best;
}
function landmarkName(id) {
  return id==='bridge'&&state?.route==='bridge'&&state.delivered?'Repaired bridge':sites[id].name;
}
function placePins(world) {
  fieldwork.render(world);
  const id=nearest();
  $('near').hidden=!id||panel.open;
  const crossing=$('crossing');
  crossing.hidden=!state?.delivered||panel.open;
  crossing.disabled=Boolean(world.goal?.crossing);
  crossing.textContent=world.onFarBank()?'Return across the river':'Walk the crossing';
  if(id) {
    $('near').textContent=id==='ranger'?'Talk to Ranger Lin':'Inspect '+landmarkName(id).toLowerCase();
    $('near').dataset.site=id;
  }
  for(const [key,pin] of Object.entries(pins)){
    const site=sites[key], [x,y]=world.project(site.x,site.y-(key==='ranger'?64:key==='bridge'?-10:14));
    const margin=22;
    pin.hidden=!state||x<margin||x>stage.clientWidth-margin||y<57||y>stage.clientHeight-3;
    pin.style.left=Math.max(margin,Math.min(stage.clientWidth-margin,x))+'px'; pin.style.top=y+'px';
    const label=landmarkName(key);
    if(pin.getAttribute('aria-label')!==label){
      pin.setAttribute('aria-label',label);
      pin.querySelector('.pin-label').textContent=label;
    }
    pin.dataset.context=Boolean(state&&Math.hypot(site.x-state.x,site.y-state.y)<105);
    pin.dataset.seen=Boolean(state?.clues.includes(key)||key==='ranger'&&state?.question);
  }
  if(state){
    $('location').textContent=world.onFarBank()?'Lookout bank':state.x<345?'Ranger clearing':state.x<620?'Bridge approach':state.x<855?'Riverbank':'White-stone ford';
  }
}
$('near').addEventListener('click',()=>interact($('near').dataset.site));
$('crossing').addEventListener('click',()=>{scene?.useCrossing();stage.focus({preventScroll:true});});

const props = {bridge:'bridge-damaged-v3', rack:'rack-loaded', depth:'depth', sign:'sign', ranger:'ranger-v3-portrait'};
function prop(id) {
  const texture=id==='bridge' && state.delivered && state.route==='bridge'?'bridge-restored-v3':props[id];
  const boards=texture==='bridge-damaged-v3'?['boardA','boardB'].map((piece,i)=>
    `<img class="repair-layer" data-piece="${piece}" src="${ART['bridge-patch-v3-'+i]}" alt="" ${state.pieces.includes(piece)?'':'hidden'}>`).join(''):'';
  return `<div class="prop prop-${id}"><img src="${ART[texture]}" alt="">${boards}</div>`;
}
function interact(id) {
  if(panel.open || !id || !state) return;
  if(fieldwork.interact(id)) return;
  if(id==='ranger') return ranger();
  if(id===workId() && !state.delivered) return fieldwork.inspect();
  const site=sites[id];
  if(!state.clues.includes(id)) state.clues.push(id);
  save(); updateMission(); audioFeedback(510);
  const label=id==='depth'?'<p class="small">Bridge: <strong>38 cm</strong> · Ford: <strong>16 cm</strong> · Limit: <strong>20 cm</strong></p>':'';
  open(site.name,'FIELD EVIDENCE',prop(id)+`<p>${state.mode==='elementary'?site.simple:site.clue}${zh(site.zh)}</p>`+label+
    actions(button('Back to trail','close','primary')),close);
}
function ranger() {
  if(state.delivered) {
    if(motion() && !state.complete && scene?.deliveryElapsed<RANGER_DELIVERY_MS) {
      return open('Ranger Lin is on the trail','DELIVERY IN PROGRESS',
        caption('deliveryInProgress')+
        actions(button('Back to trail','close','primary')),close);
    }
    state.complete=true; save(); updateMission();
    const result=state.route==='bridge'?'endingBridge':'endingFord';
    return open('Report from the lookout','MISSION COMPLETE',prop('ranger')+caption(result)+
      actions(button('Export progress','export','primary'),button('Field log','journal'),button('Back to trail','close')),
      action=>{if(action==='export') download(); if(action==='journal') journal(); if(action==='close') close();},'conversation');
  }
  if(state.route) return open('Ranger Lin','CROSSING AUTHORIZED',prop('ranger')+caption(state.route==='bridge'?'authorizedBridge':'authorizedFord')+
    actions(button('Back to trail','close','primary')),close,'conversation');
  const opening = !state.question;
  const words=state.mode==='elementary'
    ? `<p>Bridge ${zh('桥')} · River ${zh('河')} · Board ${zh('木板')} · Ford ${zh('浅滩')}</p>`
    : `<p class="small">Standing order: compare the depth to the posted limit, or check the size of the missing boards.</p>`;
  const response=opening?'opening':state.clues.includes('depth')?'returnFord':
    state.clues.includes('bridge')?'returnBridge':'returnBasic';
  open('Ranger Lin',opening?'RANGER SHELTER':'FIELD CONVERSATION',prop('ranger')+caption(response)+words+
    (opening?`<div class="stack">${profile().questions.map((q,i)=>button(q,'ask'+i,'primary')).join('')}</div>`:
      actions(button('Report the damaged bridge','report'),button('Discuss a crossing plan','plan','primary')))+
    actions(button('I practised speaking','speak'),button('Back to trail','close'))+feedbackBox,
    action=>{
      if(action.startsWith('ask')) {
        const index=Number(action.slice(3));
        state.question=profile().questions[index]; save(); updateMission(); audioFeedback(560);
        const answer=index===0?'directionFord':'directionBridge';
        open('Ranger Lin','DIRECTIONS',caption(answer)+`<p class="small">You asked: ${state.question}</p>`+
          actions(button('Explore the riverbank','close','primary')),close,'conversation');
      }
      if(action==='plan') plan();
      if(action==='close') close();
      if(action==='speak') {state.practiced.push('Ranger conversation');save();feedback('Speaking practice recorded as your own report.');}
      if(action==='report') {
        state.report=state.clues.includes('bridge')?'The bridge is broken.':'I need to check the bridge.';
        if(state.clues.includes('rack')) state.report+=' I found a board.';
        save();
        voicedFeedback(state.clues.includes('bridge')?'reportBridge':'reportMissing',state.report+' ');
      }
    },'conversation');
}
function plan() {
  const clueInputs=Object.entries(sites).filter(([id])=>id!=='ranger').map(([id,site])=>
    `<label><input type="checkbox" name="evidence" value="${id}" ${state.clues.includes(id)?'':'disabled'}>${site.name}${zh(site.zh)}${state.clues.includes(id)
      ?`<small class="cited-observation">${state.mode==='elementary'?site.simple:site.clue}</small>`:' · not yet inspected'}</label>`).join('');
  open('Recommend a crossing','TALK TO RANGER LIN',
    `<p>Choose a route, cite two observations, and tell Lin your own reason.</p>
    <label for="recommend">Your route</label>
    <select id="recommend"><option value="">Choose a plan</option><option value="bridge">Repair the bridge</option><option value="ford">Mark the ford</option><option value="unsafe">Cross beside the bridge</option></select>
    <div class="checks">${clueInputs}</div>`+
    guideVoice(state.mode==='elementary'?'guideElementary':'guideMiddle')+button('Hear evidence instructions','voice-guideEvidence','voice-replay')+recommendationFields({mode:state.mode,draft:state.draft,escape:esc,chinese:state.zh})+feedbackBox+
      actions(button('Tell Ranger Lin','send','primary'),button('Hint','hint'),button('Back','back')),
    action=>{
      if(action==='back') return ranger();
      const route=$('recommend').value;
      const selected=[...body.querySelectorAll('input:checked')].map(input=>input.value);
      if(action==='hint') {
        const hints=['Start with the clue closest to the crossing you want.','For the bridge, check the gap and tool rack. For the ford, check depth and the trail sign.',
          'The bridge needs two 90 cm boards. The ford is 16 cm, below the 20 cm limit. Use the sign to locate the white stones.'];
        feedback(hints[Math.min(state.hints.length,2)]);
        state.hints.push('route evidence');save();return;
      }
      if(!route) return feedback('Choose a recommendation, then add observations.');
      const student=readRecommendation(body,state.mode,route);
      if(route==='unsafe') {
        state.attempts.push({route,cited:selected,message:student.message,production:student.production,fact:student.fact,inference:student.inference,accepted:false});save();
        return voicedFeedback('unsafe');
      }
      const supporting=ROUTES[route].clues.every(id=>state.clues.includes(id)&&selected.includes(id));
      if(!supporting) {
        state.attempts.push({route,cited:selected,message:student.message,production:student.production,fact:student.fact,inference:student.inference,accepted:false});save();
        return voicedFeedback('retryEvidence');
      }
      if(!student.ok) {
        state.attempts.push({route,cited:selected,message:student.message,production:student.production,fact:student.fact,inference:student.inference,accepted:false});
        save();
        return feedback(student.feedback);
      }
      if(!authorize(state,route,selected,student.message,{fact:student.fact,inference:student.inference})) return feedback('This route could not be authorized. Revisit your observations.');
      state.stretch=''; save(); updateMission(); audioFeedback(680);
      open('Crossing authorized','RANGER LIN',caption(route==='bridge'?'authorizedBridge':'authorizedFord')+
        actions(button('Back to trail','close','primary')),close,'conversation');
    },'conversation');
  wireRecommendation(body,draft=>{state.draft=draft;save();});
}

function download(backup = false) {
  const record={
    game:'The Broken Bridge', build:'0.5.0', anonymousSession:state.id, languageMode:state.mode,
    languageSource:'Illustrative. Current textbook alignment has not been verified.',
    evidence:state.clues.map(id=>({id, name:sites[id]?.name, observation:sites[id]?.clue})),
    observedAnswers:{openingQuestion:state.question, bridgeReport:state.report, recommendations:reviewRecommendations(state.attempts)},
    selfReportedSpeakingPractice:state.practiced,
    ungradedReasoning:state.stretch||state.draft,
    legacyOptionalDraft:state.stretch, unsentDraft:state.route?'':state.draft,
    hintsUsed:state.hints, physicalActions:state.fieldActions??[], outcome:{route:state.route, piecesPlaced:state.pieces, suppliesDelivered:state.delivered, fieldReportComplete:state.complete},
    exportedAt:new Date().toISOString(),
  };
  const url=URL.createObjectURL(new Blob([JSON.stringify(backup?state:record,null,2)],{type:'application/json'}));
  const link=document.createElement('a'); link.href=url;link.download=backup?'broken-bridge-save.json':'broken-bridge-progress.json';
  document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function trailMap() {
  const position= Math.round(state.x/1060*100);
  const order=['rack','ranger','bridge','depth','sign'];
  return `<figure class="trail-map">
    <figcaption>Trail map · You are at ${$('location').textContent}</figcaption>
    <div class="trail-track" aria-hidden="true"><i style="left:${position}%"></i></div>
    <div class="trail-stations">${order.map(id=>button(
      '<span aria-hidden="true">'+sites[id].icon+'</span> '+sites[id].name,'walk-'+id)).join('')}</div>
  </figure>`;
}
function fieldSummary() {
  const placements=(state.fieldActions??[]).filter(event=>event.action==='placed');
  if(!placements.length)return '';
  const guided=placements.filter(event=>event.assisted).length;
  return `<p class="small">Materials placed: ${placements.length}. With the field guide: ${guided}. Direct placement: ${placements.length-guided}.</p>`;
}
function journal() {
  const entries=Object.entries(sites).filter(([id])=>id!=='ranger').map(([id,site])=>
    `<li><strong>${site.name}</strong>${zh(site.zh)}<br><span>${state.clues.includes(id)?site.clue:'Unvisited'}</span></li>`).join('');
  open('Field log','ALDER RIVER STATION',
    `<p>${state.complete?'The lookout has its supplies.':state.route?repair[state.route].guide:'Revisit any recorded clue before recommending a route.'}</p>
    <ul class="log-list">${entries}</ul>
    <p class="small">${save()?'Progress is saved in this browser.':'Browser storage is unavailable. Export your progress before closing.'}</p>`+
    trailMap()+fieldSummary()+guideVoice('guideControls')+
    actions(button('Export progress','export','primary'),button('Back to trail','close')),
    action=>{
      if(action==='export') return download();
      close();
      if(action.startsWith('walk-')) approach(action.slice(5));
    });
}
function settings() {
  open('Field settings','ALDER RIVER STATION',
    `<p class="small">English captions stay on screen. Ranger Lin’s local dialogue can be replayed with its own button.</p><div class="stack">
      ${button('Sound effects: '+(state.mute?'off':'on'),'mute')}
      ${button('Environmental motion: '+(motion()?'on':'reduced'),'motion')}
      ${button('Simplified Chinese support: '+(state.zh?'on':'off'),'zh')}
      ${button('Back up save','backup')}
      ${button('Restore a saved mission','restore')}
      ${button('Focus view: '+(stage.classList.contains('focus-view')?'on':'off'),'focus')}
      ${button('Reset progress / change guide','reset')}
    </div>`+actions(button('Back to trail','close','primary')),action=>{
      if(action==='close') return close();
      if(action==='reset') return confirmReset();
      if(action==='backup') return download(true);
      if(action==='restore') return restorePanel();
      if(action==='mute') {state.mute=!state.mute;if(state.mute&&output)output.gain.value=0;else audioFeedback();}
      if(action==='motion') state.motion=!motion();
      if(action==='zh') state.zh=!state.zh;
      if(action==='focus') stage.classList.toggle('focus-view');
      save(); settings();
      body.querySelector(`[data-action="${action}"]`).focus();
    });
}
function restorePanel() {
  open('Restore a saved mission','LOCAL SAVE',
    '<p>Choose a Broken Bridge save backup. Restoring replaces the mission in this browser.</p>'+
    '<label for="save-file">Save backup (.json)</label><input type="file" id="save-file" accept=".json,application/json">'+
    feedbackBox+actions(button('Restore this mission','apply','primary'),button('Back to settings','back')),
    async action=>{
      if(action==='back') return settings();
      const file=$('save-file').files[0];
      if(!file || file.size>200_000) return feedback('Choose a valid save backup under 200 KB.');
      let imported;
      try { imported=restore(await file.text()); } catch { /* Invalid or unreadable backup. */ }
      if(active?.type!=='restore') return;
      if(!imported) return feedback('This file is not a Broken Bridge save backup. Current progress is intact.');
      state=imported;save();updateMission();close();notify('Mission restored.');
    },'restore');
}
function confirmReset() {
  open('Start a new field log?','RESET PROGRESS',
    '<p>This clears this browser’s saved mission. Export your progress first if you want a copy.</p>'+
    actions(button('Export progress','export'),button('Reset this mission','confirm'),button('Keep playing','close','primary')),
    action=>{
      if(action==='export') return download();
      if(action==='close') return close();
      try { localStorage.removeItem(SAVE_KEY); } catch { /* Storage is optional. */ }
      state=null; launch();
    });
}
$('journal').addEventListener('click',()=>{if(state)journal();});
$('settings').addEventListener('click',()=>{if(state)settings();});
window.addEventListener('pagehide',save);
const preview=fresh();
mountWorld(window.Phaser,$('world'),{
  state:()=>state??preview, paused:()=>panel.open||!state, motion,
  near:nearest, placePins, interact, save, fieldworkKey:()=>{const id=fieldwork.near();return id?fieldwork.interact(id,{method:'keyboard'}):false;},
  fieldworkTurn:()=>fieldwork.turn(), carry:()=>fieldwork.carriedPose?.()??null,
  conversation:()=>panel.open && active?.type==='conversation',
  installing:()=>Boolean(fieldwork.installing?.()),
  voicePlaying:()=>speakingClip&&!speakingClip.paused&&!speakingClip.ended,
  ready:world=>{scene=world;},
});
if(state) updateMission(); else launch();
