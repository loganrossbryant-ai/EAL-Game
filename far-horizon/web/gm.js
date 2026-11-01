(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const id = new URLSearchParams(location.search).get('channel');
  let channel, campaign, latest, renderedScene = '', renderedCue = -1, previewId = '', wordsLanguage = '', lastMessage = 0;
  const el = (tag, text, cls) => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (cls) node.className = cls; return node; };
  const send = (action, values = {}) => { if (channel) channel.postMessage({app:'far-horizon-gm',kind:'command',command:{action,...values}}); };
  const button = (text, action, values, cls) => { const node = el('button',text,cls); node.type='button';node.addEventListener('click',() => send(action,values));return node; };
  if (id && /^fh-gm-[a-zA-Z0-9.-]{1,100}$/.test(id)) {
    channel = new BroadcastChannel(id);
    channel.onmessage = event => {
      const data = event.data;
      if (!data || data.app !== 'far-horizon-gm' || data.kind !== 'state' || !data.state) return;
      latest = data.state; lastMessage = Date.now(); if(campaign) render();
    };
  } else $('connection').textContent = 'Open the GM Desk from the game window to connect.';
  fetch('campaign.json').then(r => {if(!r.ok) throw Error('campaign');return r.json();}).then(data => {campaign=data;buildDirectory();if(latest)render();renderWords('zh');}).catch(() => {$('connection').textContent='The campaign data could not load. Serve this folder through a web host.';});
  function buildDirectory(){
    for(const session of campaign.sessions){const group=el('div');group.append(el('h3',String(session.id).padStart(2,'0')+' / '+session.title));for(const scene of campaign.scenes.filter(s=>s.session===session.id)){const b=button('', 'jump',{id:scene.id},'scene');b.dataset.scene=scene.id;b.append(el('span',scene.focus,'number'),el('span',scene.title));group.append(b);}$('scene-list').append(group);}
    for(const [key,clue] of Object.entries(campaign.clues)){const b=el('button',clue.title,'clue');b.dataset.clue=key;b.addEventListener('click',()=>preview(key));$('clue-list').append(b);}
  }
  function render(){
    const s=latest,scene=campaign.scenes.find(x=>x.id===s.scene);if(!scene)return;
    $('connection').textContent='● Connected to the stage';$('session').textContent='SESSION '+String(s.session).padStart(2,'0')+' / BEAT '+(s.cue+1)+' OF '+s.cue_count;$('scene-title').textContent=scene.title;$('focus').textContent=scene.focus;
    $('freeze').textContent=s.paused?'Resume picture':'Hold picture';$('clean').textContent=s.clean?'Show stage controls':'Hide stage controls';$('sound').textContent=s.sound?'SFX on':'SFX off';$('voice').textContent=s.recordings?(s.voice?'Voices on':'Voices off'):'NPC text dialogue';$('voice').disabled=!s.recordings;$('language').value=s.language;
    $('audio-status').textContent=s.recordings ? s.recordings+' NPC recordings installed'+(s.voice_playing?' · voice playing':'') : 'NPC dialogue uses readable captions and selectable responses. This draft has no voice pack.';
    if(renderedScene!==s.scene){
      renderedScene=s.scene;$('gm-notes').textContent=scene.gm;$('cue-list').replaceChildren();$('npc-list').replaceChildren();
      scene.cues.forEach((c,i)=>{const b=button(String(i+1).padStart(2,'0')+' / '+c.title,'cue',{index:i},'cue');b.dataset.cue=i;$('cue-list').append(b);});
      for(const key of scene.npcs){$('npc-list').append(button('Talk: '+campaign.characters[key].name,'talk',{id:key}));}
      document.querySelectorAll('[data-scene]').forEach(n=>n.classList.toggle('active',n.dataset.scene===s.scene));
    }
    renderedCue=s.cue;document.querySelectorAll('[data-cue]').forEach(n=>{n.classList.toggle('active',Number(n.dataset.cue)===s.cue);n.setAttribute('aria-current',Number(n.dataset.cue)===s.cue?'step':'false');});
    document.querySelectorAll('[data-clue]').forEach(n=>n.classList.toggle('revealed',Boolean(s.revealed[n.dataset.clue])));
    $('encounter').hidden=s.session!==2;
    if(JSON.stringify(s.threats)!==$('threat-list').dataset.value){$('threat-list').dataset.value=JSON.stringify(s.threats);$('threat-list').replaceChildren();['M-77','Minor drone 1','Minor drone 2'].forEach((name,i)=>{const d=el('div',undefined,'threat');d.append(el('span',name+'  '+ '■'.repeat(s.threats[i])+'□'.repeat((i===0?2:1)-s.threats[i])),button('−','threat',{index:i,value:s.threats[i]-1}),button('+','threat',{index:i,value:s.threats[i]+1}));$('threat-list').append(d);});}
    if(wordsLanguage!==s.language)renderWords(s.language);
  }
  function preview(key){
    previewId=key;const c=campaign.clues[key],p=$('clue-preview');p.hidden=false;p.replaceChildren(el('p',c.tag,'eyebrow'),el('h3',c.title));const dl=el('dl');for(const [k,v]of c.fields)dl.append(el('dt',k),el('dd',v));p.append(dl,el('p',c.note,'subtle'));const row=el('div',undefined,'row');row.append(button('Reveal on stage','clue',{id:key},'primary'),button('Hide from evidence board','hide_clue',{id:key}));p.append(row);
  }
  function renderWords(language){if(!campaign)return;wordsLanguage=language;$('word-list').replaceChildren();for(const word of campaign.glossary){const d=el('div',undefined,'word'),gloss=el('span',word[language]);gloss.lang=language;d.append(el('strong',word.term),gloss,el('small',word.definition));$('word-list').append(d);}}
  document.querySelectorAll('[data-action]').forEach(n=>n.addEventListener('click',()=>send(n.dataset.action)));
  $('language').addEventListener('change',e=>{renderWords(e.target.value);send('language',{value:e.target.value});});
  $('reset').addEventListener('click',()=>{if(latest && confirm('Reset Session '+latest.session+' to its first beats and hide its revealed clues? Other sessions are preserved.'))send('reset_session');});
  $('print-words').addEventListener('click',()=>window.print());
  setInterval(()=>{if(lastMessage&&Date.now()-lastMessage>3500)$('connection').textContent='Stage connection paused. Keep the game window open.';},1500);
})();
