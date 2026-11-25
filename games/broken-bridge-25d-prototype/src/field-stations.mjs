import {compareDepth, FORD_LIMIT, readProbe, recordDepth, reviewLog, RIG_LOAD, checkRig} from './survey.mjs';

const stationNames={bridge:'Bridge approach',ford:'White stones'};
const relationshipLabels={below:'below',above:'above',equal:'equal to'};
const rigLabels={
  edge:'The outer path rubs the broken edge. Reroute through the inner guide.',
  cleat:'The far end is loose. Catch the rope in the far cleat.',
  slack:'The deck still moves. Pull the rope farther.',
  strain:'The deck is strained. Ease the load back.',
  secure:'The deck is steady. The rope can be locked.',
};

export function showSounding(kit,state) {
  const {open,body,button,caption,zh,feedback,feedbackBox,close,save,fx,onSurvey}=kit;
  const survey=state.survey;
  let station='bridge', payout=0;
  const stations=Object.entries(stationNames).map(([id,name])=>button(name,'station-'+id)).join('');
  open('Depth marker','RIVER SURVEY',
    `<p>Sound both stations before comparing them with the posted ${FORD_LIMIT} cm limit.
      ${zh('先测量两个地点的水深，然后与 20 厘米的限值比较。')}</p>`+caption('gaugeGuide')+
    `<div class="station-controls" role="group" aria-label="Sounding station">${stations}</div>
      <div class="instrument-frame"><div class="sounding-scene" data-station="bridge" aria-hidden="true">
        <div class="sounding-water"></div><img src="${ART['survey-winch']}" alt="">
        <div class="sounding-scale"><i>0</i><i>10</i><i>20</i><i>30</i><i>40</i></div>
        <div class="sounding-line"></div><span class="sounding-bed"></span>
      </div>
      <div class="instrument-commands"><label for="probe-length">Lower the probe</label>
      <input type="range" id="probe-length" min="0" max="44" step="1" value="0">
      <p id="probe-status" class="instrument-status" role="status"></p>
      <div class="station-controls">${button('Raise probe','raise')}${button('Log reading','record','primary')}</div></div></div>
      <p id="sounding-record"></p>
      <div id="sounding-compare" hidden>
        <div class="comparison-controls">
          <label>Passable station<select id="ford-station"><option value="">Choose</option>
            <option value="bridge">Bridge approach</option><option value="ford">White stones</option></select></label>
          <label>Compared with ${FORD_LIMIT} cm<select id="ford-relation"><option value="">Choose</option>
            ${Object.entries(relationshipLabels).map(([id,value])=>`<option value="${id}">${value}</option>`).join('')}</select></label>
        </div>
        ${button('Log comparison','compare','primary')}
      </div>`+feedbackBox+`<div class="actions">${button('Hint','hint')}${button('Back to trail','close')}</div>`,
    action=>{
      if(action==='close')return close();
      if(action.startsWith('station-')){
        if(payout>0)return feedback('Raise the probe fully before moving the carriage.');
        station=action.slice(8);
        feedback('Probe moved to '+stationNames[station]+'.');
      }
      if(action==='raise'){slider.value='0';payout=0;feedback('Probe clear of the water.');}
      if(action==='record'){
        if(!recordDepth(survey,station,payout))return feedback('Lower the probe until it touches the riverbed.');
        fx('probe-contact',778);
        feedback(stationNames[station]+': '+survey.readings[station]+' cm logged.');
        save();
      }
      if(action==='compare'){
        const comparison=compareDepth(survey,find('#ford-station').value,find('#ford-relation').value);
        if(!comparison)return feedback('Compare each recorded depth with the limit. Which station is shallower than 20 cm?');
        onSurvey();
        feedback('Today the water at the white stones is 16 cm, below the 20 cm limit. Take the report to Lin.');
      }
      if(action==='hint'){
        const hints=['The line measures the depth when the weight touches the riverbed.',
          'Log at both stops. Lift the probe to zero to move between them.',
          'A safe reading here is smaller than 20 cm. Compare 38 cm and 16 cm.'];
        kit.hint(survey,'survey',hints);
      }
      render();
    },'depth');
  const find=selector=>body.querySelector(selector);
  const slider=find('#probe-length');
  const picture=find('.sounding-scene');
  picture.style.setProperty('--sounding-water', 'url('+ART['survey-water']+')');
  slider.addEventListener('input',()=>{
    const hadContact=readProbe(station,payout).contact;
    payout=Number(slider.value);
    if(!hadContact&&readProbe(station,payout).contact)fx('probe-contact',778,.38);
    render();
  });
  function render(){
    const {depth,contact}=readProbe(station,payout);
    picture.dataset.station=station;
    picture.dataset.contact=String(contact);
    picture.style.setProperty('--payout',depth/44);
    picture.style.setProperty('--bed',station==='bridge'?38/44:16/44);
    for(const id of Object.keys(stationNames)){
      find(`[data-action="station-${id}"]`).setAttribute('aria-pressed',String(id===station));
    }
    find('#probe-status').textContent=contact?`Bed contact · ${depth} cm`:payout?'Line lowering · '+depth+' cm':'Probe raised';
    find('#sounding-record').textContent=Object.keys(stationNames)
      .map(id=>stationNames[id]+': '+(survey.readings[id]?`${survey.readings[id]} cm`:'—')).join(' · ');
    find('#sounding-compare').hidden=!survey.readings.bridge||!survey.readings.ford;
    if(survey.compared){
      find('#ford-station').value='ford';find('#ford-relation').value='below';
    }
  }
  render();
}

export function showInterview(kit,state) {
  const {open,body,button,caption,zh,feedback,feedbackBox,close,save,portrait,onCorrection}=kit;
  const survey=state.survey;
  if(survey.corrected){
    return open('Ranger Lin','NOTICE REVISED',portrait()+caption('revisedNotice')+
      `<div class="actions">${button('Discuss a crossing plan','plan','primary')}${button('Back to trail','close')}</div>`,
      action=>action==='plan'?kit.plan():close(),'conversation');
  }
  open('Ranger Lin','THE OLD FORD NOTICE',portrait()+
    `<p>Lin marked the ford closed after the storm. Ask when she checked it.
      ${zh('询问她是什么时候测量水深的。')}</p>`+
    `<div class="actions">${button('When did you check the ford?','when','primary')}${button('Back to trail','close')}</div>`,
    action=>{
      if(action==='close')return close();
      survey.asked=true;save();answer();
    },'conversation');
  if(survey.asked)answer();

  function answer(){
    const readings=survey.compared;
    const model=state.mode==='elementary'?'Today it is ___ cm. That is ___ 20 cm.':
      'Yesterday the ford was deeper. Today it is ___ cm, which is ___ the limit of 20 cm.';
    open('Ranger Lin','YESTERDAY AND TODAY',caption('oldNotice')+
      `<p class="field-slip"><strong>Lin’s log · yesterday</strong><br>White stones: 26 cm. Ford closed.</p>`+
      (readings?`<p class="field-slip"><strong>Your sounding · today</strong><br>White stones: 16 cm. Posted limit: 20 cm.</p>
      <p>Show Lin the two records that explain what changed. Write a correction.
        ${zh('选出昨天和今天的记录，然后说明水位有什么变化。')}</p>
      <div class="checks">
        <label><input type="checkbox" name="notice-source" value="log">Yesterday’s ford log</label>
        <label><input type="checkbox" name="notice-source" value="sounding">Today’s river sounding</label>
        <label><input type="checkbox" name="notice-source" value="rack">Board length from the rack</label>
      </div>
      <label for="notice-correction">Your correction</label><p class="small">${model}</p>
      <textarea id="notice-correction" maxlength="350"></textarea>
      `:`<p>Take both soundings at the depth marker before asking Lin to change the notice.</p>`)+feedbackBox+
      `<div class="actions">${readings?button('Show the two records','compare','primary')+button('Hint','hint'):''}
        ${button('Back to trail','close')}</div>`,
      action=>{
        if(action==='close')return close();
        if(action==='hint')return kit.hint(survey,'interview',[
          'Compare records of the same place on different days.',
          'Use the dated log and your sounding. Start with “Today” and compare 16 cm with 20 cm.',
        ]);
        const sources=[...body.querySelectorAll('input[name="notice-source"]:checked')].map(input=>input.value);
        const attempt=reviewLog(survey,sources,body.querySelector('#notice-correction').value);
        save();
        if(!attempt.ok)return feedback(attempt.feedback);
        onCorrection();
        open('Ranger Lin','NOTICE REVISED',portrait()+caption('revisedNotice')+
          `<div class="actions">${button('Watch Lin turn the notice','close','primary')}</div>`,close,'conversation');
      },'conversation');
    if(readings)body.querySelector('#notice-correction').value=survey.interview.at(-1)?.note??'';
  }
}

export function showRig(kit,state,finish) {
  const {open,body,button,caption,zh,feedback,feedbackBox,close,fx}=kit;
  let path='',cleat=false,load=0;
  open('Bridge rigging','TWO BOARDS · ONE SAFETY LINE',
    `<p>Keep the rope clear of the broken edge, then test the deck under load.
      ${zh('让绳子避开破损的边缘，然后检查拉力。')}</p>`+caption('rigGuide')+
    `<div class="instrument-frame"><div class="rig-scene">
      <img src="${ART['bridge-rig']}" alt="">
      <svg viewBox="0 0 420 175" aria-hidden="true" preserveAspectRatio="none"><path class="rig-line"></path></svg>
      ${button('Inner guide','inner','rig-inner')}${button('Outer edge','outer','rig-outer')}${button('Far cleat','cleat','rig-cleat')}
     </div>
     <div class="instrument-commands"><label for="rig-load">Pull on the line · safe band ${RIG_LOAD.min}–${RIG_LOAD.max}</label>
     <div class="load-scale"><input type="range" id="rig-load" min="0" max="100" value="0"></div>
     <p id="rig-status" class="instrument-status" role="status"></p></div></div>`+feedbackBox+
    `<div class="actions">${button('Lock and test','test','primary')}${button('Reset the line','reset')}
      ${button('Hint','hint')}${button('Back to trail','close')}</div>`,
    action=>{
      if(action==='close')return close();
      if(action==='inner'||action==='outer'){
        path=action;cleat=false;load=0;slider.value='0';fx('rope-handle',450);
        feedback(path==='inner'?'The rope passes cleanly through the inner guide.':'The rope lies against the damaged outer edge.');
      }
      if(action==='cleat'){
        if(!path)return feedback('Feed the rope through a guide before securing the far end.');
        cleat=true;fx('rope-handle',450,.47);feedback('The rope is connected to the far cleat.');
      }
      if(action==='reset'){path='';cleat=false;load=0;slider.value='0';feedback('The load is released.');}
      if(action==='hint')return kit.hint(state.survey,'rig',[
        'The far cleat holds the rope. The inner guide keeps it away from the splinters.',
        'Move the load marker into the shaded band before locking the rope.',
      ]);
      if(action==='test'){
        const result=checkRig(path,cleat,load);
        kit.rigTrial(path,cleat,load,result);
        if(result==='secure'){
          body.closest('dialog').addEventListener('close',()=>finish(state.survey.hints.includes('rig')),{once:true});
          close();
          return;
        }
        fx(result==='strain'?'bridge-creak':'rope-handle',450,.5);
        feedback(rigLabels[result]);
      }
      render();
    },'rig');
  const slider=body.querySelector('#rig-load');
  const line=body.querySelector('.rig-line');
  slider.addEventListener('input',()=>{
    load=Number(slider.value);
    render();
  });
  function render(){
    const middle=path==='inner'?[161,80]:[171,137];
    const far=cleat?[345,49]:[244,middle[1]+21];
    const sag=cleat?(100-load)*.45:30;
    line.setAttribute('d',path?`M57 108 Q98 ${117+sag} ${middle.join(' ')} Q255 ${middle[1]+sag} ${far.join(' ')}`:'M57 108 q30 29 68 17');
    line.dataset.load=load>RIG_LOAD.max?'strain':load<RIG_LOAD.min?'slack':'band';
    body.querySelector('.rig-scene').dataset.fitted=String(cleat);
    body.querySelector('#rig-status').textContent=path?`${load} · ${!cleat?'far end loose':load<RIG_LOAD.min?'slack':load>RIG_LOAD.max?'strained':'in the safe band'}`:'Choose how to feed the rope.';
    body.querySelector('[data-action="cleat"]').setAttribute('aria-pressed',String(cleat));
    for(const id of ['inner','outer'])body.querySelector(`[data-action="${id}"]`).setAttribute('aria-pressed',String(id===path));
  }
  render();
}
