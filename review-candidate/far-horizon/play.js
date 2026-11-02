(function(){
 'use strict';
 const $=id=>document.getElementById(id),frame=$('stage'),sheet=$('sheet');
 const coarse=matchMedia('(pointer:coarse)').matches;
 let campaign=null,portraits=null,state=null,mode='',rendered='',walkTimer=null,walking=0,ready=false;
 const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
 const send=(action,values={})=>{try{return Boolean(frame.contentWindow.fhGMBridge?.submit({action,...values}));}catch(_){return false;}};
 const button=(text,action)=>{const b=el('button',text);b.type='button';b.addEventListener('click',action);return b;};
 function focusStage(){if(!coarse&&ready){frame.focus();try{frame.contentDocument.getElementById('canvas').focus();}catch(_){}}}
 function stop(){clearInterval(walkTimer);walkTimer=null;if(walking)send('move',{direction:0});walking=0;}
 function walk(direction){stop();if(!ready||state?.modal||state?.paused)return;walking=direction;send('move',{direction});walkTimer=setInterval(()=>send('move',{direction}),180);}
 function fit(){const slot=$('stage-slot'),w=slot.clientWidth,h=slot.clientHeight,width=Math.min(w,h*16/9);frame.style.width=width+'px';frame.style.height=(width*9/16)+'px';}
 new ResizeObserver(fit).observe($('stage-slot'));window.addEventListener('resize',fit);window.visualViewport?.addEventListener('resize',fit);
 for(const [id,direction] of [['left',-1],['right',1]]){
  const b=$(id);b.addEventListener('pointerdown',e=>{e.preventDefault();b.setPointerCapture(e.pointerId);walk(direction);});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,stop);
  b.addEventListener('contextmenu',e=>e.preventDefault());
 }
 window.addEventListener('blur',stop);window.addEventListener('pagehide',stop);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 function closeSheet(closeGame=true){stop();const old=mode;mode='';rendered='';if(sheet.open)sheet.close();if(closeGame&&old==='read'&&state?.modal)send('close');focusStage();}
 function openSheet(kind){stop();mode=kind;rendered='';render();if(!sheet.open)sheet.showModal();}
 $('dismiss').addEventListener('click',()=>closeSheet());sheet.addEventListener('cancel',e=>{e.preventDefault();closeSheet();});
 $('use').addEventListener('click',()=>{stop();send('interact');focusStage();});
 $('read').addEventListener('click',()=>openSheet('read'));
 $('scenes').addEventListener('click',()=>openSheet('scenes'));
 $('back').addEventListener('click',()=>{closeSheet();send('close');focusStage();});
 $('previous').addEventListener('click',()=>{stop();send('previous');focusStage();});
 $('next').addEventListener('click',()=>{stop();send('next');focusStage();});
 $('desk').addEventListener('click',()=>{stop();frame.contentWindow.fhGMBridge?.openDesk();});
 $('begin').addEventListener('click',async()=>{
  $('begin').disabled=true;$('load-note').textContent='Preparing the ship…';
  try{
   const test=document.createElement('canvas'),gl=test.getContext('webgl2');
   if(!gl)throw Error('This draft needs WebGL 2. Try current Safari on iPhone, or Chrome / Edge on PC.');
   gl.getExtension('WEBGL_lose_context')?.loseContext();
   const response=await fetch('campaign.json');if(!response.ok)throw Error('The story could not load. Please refresh and try again.');campaign=await response.json();
   const photos=await fetch('portraits.json');if(!photos.ok)throw Error('The crew portraits could not load. Please refresh and try again.');portraits=await photos.json();
   $('welcome').hidden=true;$('player').hidden=false;fit();frame.src='index.html';frame.addEventListener('load',focusStage,{once:true});
  }catch(error){$('load-note').textContent=error.message;$('begin').disabled=false;}
 });
 window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.source!==frame.contentWindow||event.data?.app!=='far-horizon-preview'||event.data.kind!=='state')return;
  const previous=state;state=event.data.state;if(!state)return;
  if(!ready){ready=true;document.querySelectorAll('#player button').forEach(b=>b.disabled=false);focusStage();}
  $('status').textContent='S'+state.session+' · '+state.title+' · '+(state.cue+1)+'/'+state.cue_count;
  const lock=state.modal||state.paused||sheet.open;
  $('left').disabled=Boolean(lock);$('right').disabled=Boolean(lock);
  $('use').disabled=Boolean(lock||!state.nearest);
  $('back').disabled=!state.modal;
  if(lock&&walking)stop();
  if(coarse&&state.modal&&!state.physical_inspection&&(!previous||state.clue!==previous.clue||state.conversation!==previous.conversation))openSheet('read');
  if(sheet.open)render();
 });
 function render(){
  if(!campaign||!state)return;
  const key=[mode,state.scene,state.cue,state.clue,state.conversation,state.line,state.language,JSON.stringify(state.revealed)].join('|');if(rendered===key)return;rendered=key;
  const content=$('sheet-content');content.replaceChildren();
  if(mode==='scenes'){
   $('sheet-title').textContent='Choose a scene';
   for(const session of campaign.sessions){content.append(el('h3',String(session.id).padStart(2,'0')+' / '+session.title));
    for(const scene of campaign.scenes.filter(s=>s.session===session.id)){
     const b=button(scene.title,()=>{send('jump',{id:scene.id});closeSheet(false);});b.dataset.scene=scene.id;if(scene.id===state.scene)b.className='current';content.append(b);
    }
   }
   return;
  }
  if(state.clue&&campaign.clues[state.clue]){
   const clue=campaign.clues[state.clue];$('sheet-title').textContent=clue.title;content.append(el('p',clue.tag,'eyebrow'));
   const dl=el('dl');for(const [k,v] of clue.fields)dl.append(el('dt',k),el('dd',v));content.append(dl,el('p',clue.note,'note'));return;
  }
  if(state.conversation==='glossary'){
   $('sheet-title').textContent='Academic words';
   for(const [value,label] of [['zh','简体中文'],['ko','한국어'],['ja','日本語']])content.append(button(label,()=>send('language',{value})));
   for(const word of campaign.glossary){const row=el('div',undefined,'gloss'),translated=el('span',word[state.language]);translated.lang=state.language;row.append(el('strong',word.term),translated,el('small',word.definition));content.append(row);}return;
  }
  if(state.conversation==='board'){
   $('sheet-title').textContent='Revealed evidence';for(const [id,clue] of Object.entries(campaign.clues))if(state.revealed[id])content.append(button(clue.title,()=>send('clue',{id})));return;
  }
  const person=campaign.characters[state.conversation];
  if(person){
   $('sheet-title').textContent=person.name;
   const photo=portraits?.[state.conversation];
   if(photo){
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox',photo.region.join(' '));svg.setAttribute('role','img');svg.setAttribute('aria-label',person.name+' — original PPT portrait');svg.classList.add('npc-photo');
    const img=document.createElementNS('http://www.w3.org/2000/svg','image');img.setAttribute('href','portraits/'+photo.file);img.setAttribute('width',photo.size[0]);img.setAttribute('height',photo.size[1]);svg.append(img);content.append(svg);
   }
   content.append(el('p',person.role,'eyebrow'),el('p',state.line));
   const options=person.replies.filter(o=>(o.min_session||1)<=state.session&&(o.max_session||3)>=state.session&&(!o.requires||state.revealed[o.requires]));
   options.forEach((option,index)=>{const b=button(option.question,()=>send('reply',{index}));b.dataset.reply=index;content.append(b);});return;
  }
  const scene=campaign.scenes.find(s=>s.id===state.scene),cue=scene.cues[state.cue];
  $('sheet-title').textContent=cue.title;content.append(el('p','SESSION '+state.session+' · '+scene.title,'eyebrow'));
  if(cue.speaker&&campaign.characters[cue.speaker])content.append(el('h3',campaign.characters[cue.speaker].name));content.append(el('p',cue.text));
  if(scene.npcs.length){content.append(el('h3','Speak with the crew'));for(const id of scene.npcs){const b=button(campaign.characters[id].name,()=>send('talk',{id}));b.dataset.talk=id;content.append(b);}}
  content.append(button('Academic vocabulary',()=>send('glossary')));
 }
})();
