import {fresh, restore, authorize, operate, ROUTES, SAVE_KEY} from './state.mjs';
import {language, repair, sites} from './content.mjs';
import {mountWorld} from './world.mjs';

const $ = id => document.getElementById(id);
const panel = $('panel'), body = $('panel-body'), stage = $('stage');
const preferredMotion = matchMedia('(prefers-reduced-motion: reduce)');
const read = () => {
  try { return restore(localStorage.getItem(SAVE_KEY)); } catch { return null; }
};
let state = read();
let scene, active, toastTimer, audio, output;
const pins = {};
const motion = () => state?.motion ?? !preferredMotion.matches;
const profile = () => language[state.mode];
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const zh = text => state.zh ? ` <span lang="zh-Hans" class="zh">${text}</span>` : '';
const button = (text, action, cls = '') => `<button data-action="${action}" class="${cls}">${text}</button>`;
const actions = (...buttons) => `<div class="actions">${buttons.join('')}</div>`;
const workId = () => state?.route && repair[state.route].site;

for (const [id,site] of Object.entries(sites)) {
  const pin = document.createElement('button');
  pin.className = 'pin';
  pin.setAttribute('aria-label', site.name);
  pin.innerHTML = `<span class="site-mark" aria-hidden="true"></span><span class="pin-label">${site.name}</span>`;
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
    instruction = state.route === 'bridge' ? 'Return to the bridge and fit the two boards and rope.'
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
  active={onAction,type};
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
function notify(message) {
  const notice=$('notice');
  notice.textContent=message;
  notice.hidden=false;
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>{notice.hidden=true;},3600);
}
function feedback(message) {
  const node=$('feedback');
  node.hidden=false;
  node.textContent=message;
}
const feedbackBox='<p id="feedback" role="status" hidden></p>';

body.addEventListener('click',event=>{
  const action=event.target.closest('button[data-action]')?.dataset.action;
  if(action) active?.onAction(action);
});
$('close').addEventListener('click',close);
panel.addEventListener('cancel',event=>{event.preventDefault();close();});
panel.addEventListener('close',()=>{active=null; stage.focus({preventScroll:true});});
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
  scene.walk(site.x,site.y+9,id);
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
    pin.dataset.seen=Boolean(state?.clues.includes(key)||key==='ranger'&&state?.question);
  }
  if(state){
    $('location').textContent=world.onFarBank()?'Lookout bank':state.x<345?'Ranger clearing':state.x<620?'Bridge approach':state.x<855?'Riverbank':'White-stone ford';
  }
}
$('near').addEventListener('click',()=>interact($('near').dataset.site));
$('crossing').addEventListener('click',()=>{scene?.useCrossing();stage.focus({preventScroll:true});});

const props = {bridge:'broken', rack:'rack-loaded', depth:'depth', sign:'sign', ranger:'ranger-portrait'};
function prop(id) {
  const texture=id==='bridge' && state.delivered && state.route==='bridge'?'repaired':props[id];
  const boards=texture==='broken'?['boardA','boardB'].map((piece,i)=>
    `<img class="repair-layer" data-piece="${piece}" src="${ART['bridge-fill-'+i]}" alt="" ${state.pieces.includes(piece)?'':'hidden'}>`).join(''):'';
  return `<div class="prop prop-${id}"><img src="${ART[texture]}" alt="">${boards}</div>`;
}
function interact(id) {
  if(panel.open || !id || !state) return;
  if(id==='ranger') return ranger();
  if(id===workId() && !state.delivered) return workbench();
  const site=sites[id];
  if(!state.clues.includes(id)) state.clues.push(id);
  save(); updateMission(); audioFeedback(510);
  const label=id==='depth'?'<p class="small">Bridge: <strong>38 cm</strong> · Ford: <strong>16 cm</strong> · Limit: <strong>20 cm</strong></p>':'';
  open(site.name,'FIELD EVIDENCE',prop(id)+`<p>${state.mode==='elementary'?site.simple:site.clue}${zh(site.zh)}</p>`+label+
    actions(button('Back to trail','close','primary')),close);
}
function ranger() {
  if(state.delivered) {
    if(motion() && !state.complete && scene?.deliveryElapsed<4300) {
      return open('Ranger Lin is on the trail','DELIVERY IN PROGRESS',
        '<p>Watch the crossing. Meet the ranger here when the delivery walk is finished.</p>'+
        actions(button('Back to trail','close','primary')),close);
    }
    state.complete=true; save(); updateMission();
    const result=state.route==='bridge'?'The two boards held. The bridge is open and the supply pack reached the lookout.'
      :'Your flags traced the white stones. The supplies reached the lookout by the ford. The bridge is still closed.';
    return open('Report from the lookout','MISSION COMPLETE',prop('ranger')+`<p class="speech">${result}</p>`+
      actions(button('Export progress','export','primary'),button('Field log','journal'),button('Back to trail','close')),
      action=>{if(action==='export') download(); if(action==='journal') journal(); if(action==='close') close();});
  }
  if(state.route) return open('Ranger Lin','CROSSING AUTHORIZED',prop('ranger')+`<p>${repair[state.route].guide}</p>`+
    actions(button('Back to trail','close','primary')),close);
  const opening = !state.question;
  const words=state.mode==='elementary'
    ? `<p>Bridge ${zh('桥')} · River ${zh('河')} · Board ${zh('木板')} · Ford ${zh('浅滩')}</p>`
    : `<p class="small">Standing order: compare the depth to the posted limit, or check the size of the missing boards.</p>`;
  open('Ranger Lin',opening?'RANGER SHELTER':'FIELD CONVERSATION',prop('ranger')+
    `<p class="speech">${opening?'The lookout needs supplies. A crossing must be made safe before we go.':
      'Tell me what you saw. The bridge and the ford each need a different safety check.'}</p>`+words+
    (opening?`<div class="stack">${profile().questions.map((q,i)=>button(q,'ask'+i,'primary')).join('')}</div>`:
      actions(button('Report the damaged bridge','report'),button('Discuss a crossing plan','plan','primary')))+
    actions(button('I practised speaking','speak'),button('Back to trail','close'))+feedbackBox,
    action=>{
      if(action.startsWith('ask')) {
        const index=Number(action.slice(3));
        state.question=profile().questions[index]; save(); updateMission(); audioFeedback(560);
        const answer=index===0?'The ford is downstream. Look for white stones and check the water depth.'
          :'Check the bridge gap and the board lengths at the tool rack. The inspection tag tells you about the supports.';
        open('Ranger Lin','DIRECTIONS',`<p class="speech">${answer}</p><p class="small">You asked: ${state.question}</p>`+
          actions(button('Explore the riverbank','close','primary')),close);
      }
      if(action==='plan') plan();
      if(action==='close') close();
      if(action==='speak') {state.practiced.push('Ranger conversation');save();feedback('Speaking practice recorded as your own report.');}
      if(action==='report') {
        state.report=state.clues.includes('bridge')?'The bridge is broken.':'I need to check the bridge.';
        if(state.clues.includes('rack')) state.report+=' I found a board.';
        save();
        feedback(state.report+' '+(state.clues.includes('bridge')?'Correct. The supports are sound. Now tell me which crossing you recommend.':'Go to the north edge of the clearing and look for the missing boards.'));
      }
    });
}
function plan() {
  const p=profile();
  const clueInputs=Object.entries(sites).filter(([id])=>id!=='ranger').map(([id,site])=>
    `<label><input type="checkbox" name="evidence" value="${id}" ${state.clues.includes(id)?'':'disabled'}>${site.name}${zh(site.zh)}${state.clues.includes(id)?'':' · not yet inspected'}</label>`).join('');
  open('Recommend a crossing','TALK TO RANGER LIN',
    `<p>Choose what you’ll say and attach the two field observations that support it.</p>
    <label for="recommend">Your recommendation</label>
    <select id="recommend"><option value="">Choose a plan</option><option value="bridge">${p.bridge}</option><option value="ford">${p.ford}</option><option value="unsafe">${p.wrong}</option></select>
    <div class="checks">${clueInputs}</div>
    <label for="draft">${state.mode==='elementary'?'Optional: I saw…':'Optional STRETCH: compare the readings or explain a revision'}</label>
    <textarea id="draft" maxlength="1500">${esc(state.draft)}</textarea>
    <p class="small">${p.stretch}${zh('用证据说明你的选择。')}</p>`+feedbackBox+
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
      if(route==='unsafe') {
        state.attempts.push({route,cited:selected,message:p.wrong,accepted:false});save();
        return feedback('Ranger Lin: Wait. The water at the bridge is 38 cm. Look downstream and compare the ford to its limit.');
      }
      if(!authorize(state,route,selected,p[route])) {
        save();return feedback('Ranger Lin: I need both observations for that plan. Check your field evidence and try again.');
      }
      state.stretch=state.draft; save(); updateMission(); audioFeedback(680);
      open('Crossing authorized','RANGER LIN',`<p class="speech">${route==='bridge'?'Those measurements match. I’ll release the boards and rope.':
        'The ford is within the posted limit. I’ll release the markers and the supply pack.'}</p><p>${repair[route].guide}</p>`+
        actions(button('Back to trail','close','primary')),close);
    });
  $('draft').addEventListener('input',event=>{state.draft=event.target.value;save();});
}

function workbench() {
  const route=state.route, sceneWork=repair[route], pieces=ROUTES[route].pieces;
  const icons=(route==='bridge'?['board','board','rope']:['flag-0','flag-1','supplies'])
    .map(name=>`<img src="${ART[name]}" alt="">`);
  let carried=null;
  const headings=['↗ Northeast','↘ Southeast','↙ Southwest','↖ Northwest'];
  const turns=[0,0];
  const placed=index=>state.pieces.includes(pieces[index]);
  const update=()=>{
    for(let i=0;i<3;i++){
      const source=body.querySelector(`[data-action="pick${i}"]`);
      const target=body.querySelector(`[data-action="place${i}"]`);
      source.disabled=placed(i);
      source.setAttribute('aria-pressed',String(carried===i));
      target.classList.toggle('done',placed(i));
      target.querySelector('.part-icon').innerHTML=placed(i)?icons[i]:'·';
      target.disabled=placed(i);
    }
    for(const image of body.querySelectorAll('.repair-layer')) image.hidden=!state.pieces.includes(image.dataset.piece);
    const rotation=$('rotation');
    if(rotation){
      rotation.hidden=carried===null||carried===2;
      if(!rotation.hidden) rotation.querySelector('output').textContent=headings[turns[carried]];
    }
  };
  const apply=index=>{
    if (carried===null) return feedback('Pick up a piece from the tray first.');
    if (index!==carried) return feedback(route==='bridge'
      ?'That piece won’t fit there. The boards go in their matching sockets, and the rope goes on the cleat.'
      :'Try the matching stone for that marker. The pack belongs at the loading spot.');
    if(route==='ford' && index<2 && turns[index]!==[3,1][index]) {
      return feedback(index===0?'The near flag must point northwest, toward the far white stone.'
        :'The far flag must point southeast, back toward the near white stone.');
    }
    if (!operate(state,pieces[index])) return feedback(route==='bridge'
      ?'Fit both boards before securing the rope.' : 'Place both markers before moving the supply pack.');
    carried=null;
    update(); save(); updateMission(); audioFeedback(index===2?790:430);
    if(state.delivered) {
      const result=route==='bridge'?'The deck is repaired. Ranger Lin is taking the supplies over the bridge.'
        :'Your flags mark the safe line. Ranger Lin is taking the supplies along the white stones.';
      return open(route==='bridge'?'The bridge is open':'The ford is marked','CROSSING READY',
        `<p>${result}</p>`+actions(button('Watch the crossing','close','primary')),close);
    }
    feedback(route==='bridge'?'The board is seated.':'The marker is in position. The flag points along the white stones.');
  };
  const entries=(items,prefix,images)=>items.map((item,i)=>
    `<button data-action="${prefix}${i}" ${prefix==='pick'?'aria-pressed="false" draggable="true"':''}><span class="part-icon" aria-hidden="true">${images[i]}</span>${item}</button>`).join('');
  open(sceneWork.name, 'FIELD WORK',
    prop(sceneWork.site)+`<p>${sceneWork.guide}</p><p class="small">Drag a piece to its place, or tap the piece and then the target.</p>
      <div class="workbench"><div class="tray" aria-label="Materials">${entries(sceneWork.parts,'pick',icons)}</div>
      <div class="targets" aria-label="Placement targets">${entries(sceneWork.targets,'place',['·','·','·'])}</div></div>`+
    (route==='ford'?'<p class="small">Trail map: near stone ↖ far stone. From the far stone, turn back ↘.</p><div id="rotation" class="actions" hidden><output aria-live="polite"></output><button data-action="rotate">Turn marker clockwise</button></div>':'')+
      feedbackBox+actions(button('Back to trail','close')),
    action=>{
      if(action==='close') return close();
      if(action==='rotate' && carried!==null && carried<2) {
        turns[carried]=(turns[carried]+1)%4;update();return;
      }
      const index=Number(action.slice(-1));
      if(action.startsWith('pick')) {carried=index;update();feedback('Holding '+sceneWork.parts[index].toLowerCase()+'.');}
      if(action.startsWith('place')) apply(index);
    });
  for(const node of body.querySelectorAll('.tray button')){
    node.addEventListener('dragstart',event=>{
      carried=Number(node.dataset.action.slice(-1)); event.dataTransfer.setData('text/plain',node.dataset.action);
      event.dataTransfer.effectAllowed='move'; update();
    });
  }
  for(const node of body.querySelectorAll('.targets button')){
    node.addEventListener('dragover',event=>event.preventDefault());
    node.addEventListener('drop',event=>{event.preventDefault();apply(Number(node.dataset.action.slice(-1)));});
  }
  update();
}
function download(backup = false) {
  const record={
    game:'The Broken Bridge', build:'0.2.0', anonymousSession:state.id, languageMode:state.mode,
    languageSource:'Illustrative. Current textbook alignment has not been verified.',
    evidence:state.clues.map(id=>({id, name:sites[id]?.name, observation:sites[id]?.clue})),
    observedAnswers:{openingQuestion:state.question, bridgeReport:state.report, recommendations:state.attempts},
    selfReportedSpeakingPractice:state.practiced,
    ungradedReasoning:state.stretch||state.draft,
    hintsUsed:state.hints, outcome:{route:state.route, piecesPlaced:state.pieces, suppliesDelivered:state.delivered, fieldReportComplete:state.complete},
    exportedAt:new Date().toISOString(),
  };
  const url=URL.createObjectURL(new Blob([JSON.stringify(backup?state:record,null,2)],{type:'application/json'}));
  const link=document.createElement('a'); link.href=url;link.download=backup?'broken-bridge-save.json':'broken-bridge-progress.json';
  document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function journal() {
  const entries=Object.entries(sites).filter(([id])=>id!=='ranger').map(([id,site])=>
    `<li><strong>${site.name}</strong>${zh(site.zh)}<br><span>${state.clues.includes(id)?site.clue:'Unvisited'}</span></li>`).join('');
  open('Field log','ALDER RIVER STATION',
    `<p>${state.complete?'The lookout has its supplies.':state.route?repair[state.route].guide:'Revisit any recorded clue before recommending a route.'}</p>
    <ul class="log-list">${entries}</ul>
    <p class="small">${save()?'Progress is saved in this browser.':'Browser storage is unavailable. Export your progress before closing.'}</p>`+
    '<p class="small">Trail map · Tool rack → Shelter → Bridge → Depth marker → Ford</p>'+
    actions(...Object.entries(sites).map(([id,site])=>button('Walk to '+site.name,'walk-'+id)))+
    actions(button('Export progress','export','primary'),button('Back to trail','close')),
    action=>{
      if(action==='export') return download();
      close();
      if(action.startsWith('walk-')) approach(action.slice(5));
    });
}
function settings() {
  open('Field settings','ALDER RIVER STATION',
    `<p class="small">English dialogue is available as text. Approved voice recordings are pending.</p><div class="stack">
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
  near:nearest, placePins, interact, save, conversation:()=>panel.open && $('panel-title').textContent==='Ranger Lin', ready:world=>{scene=world;},
});
if(state) updateMission(); else launch();
