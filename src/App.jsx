import React, {useEffect,useRef,useState} from 'react';
import {ArrowRight, ArrowUpRight, BookOpen, Bookmark, Check, ChevronDown, CircleHelp, Compass, FileText, Headphones, Leaf, MapPin, Maximize2, Moon, RotateCcw, Settings2, ShieldCheck, Volume2, VolumeX, X} from 'lucide-react';
import {createMediaRoom} from './game/MediaRoom';
import {initialState,loadProgress,saveProgress,evaluateResponse} from './state';
import {support} from './content';
import {Campaign,Notice,Inbox,Dialogue,Assessment,Notebook,Glossary} from './components/Interfaces';

const titles={laptop:'Newsroom laptop',noticeboard:'Community noticeboard',inbox:'Maya’s email',editor:'A conversation with Maya',assessment:'Your editorial note',notebook:'Your investigation notebook',glossary:'Language companion',help:'Make yourself at home',door:'The courtyard door',ending:'A story becomes a helping hand'};
function App(){
 const [state,setState]=useState(()=>loadProgress());
 const [modal,setModal]=useState(null);
 const [near,setNear]=useState(null);
 const [ready,setReady]=useState(false);
 const [toast,setToast]=useState('');
 const [sound,setSound]=useState(false);
 const [storageOK,setStorageOK]=useState(true);
 const [time,setTime]=useState(new Date());
 const gameRef=useRef(null), hostRef=useRef(null), stateRef=useRef(state), openRef=useRef(null), closeRef=useRef(null), previousFocus=useRef(null), modalRef=useRef(null), soundRef=useRef(null);
 const patch=(change)=>setState(prev=>({...prev,...change}));
 stateRef.current=state;
 const notify=(message)=>setToast(message);
 const open=(id)=>{
   if(id==='return'){patch({room:'newsroom',position:null});gameRef.current?.setRoom('newsroom');return;}
   if(id==='door'&&stateRef.current.completed){patch({room:'courtyard',position:null});gameRef.current?.setRoom('courtyard');setModal('ending');return;}
   previousFocus.current=document.activeElement;setModal(id);
 };
 openRef.current=open;
 const close=()=>{setModal(null);window.speechSynthesis?.cancel();setTimeout(()=>{previousFocus.current?.focus?.();gameRef.current?.focus?.();},0);};
 closeRef.current=close;
 useEffect(()=>{
   const api=createMediaRoom(hostRef.current,{onInteract:(id)=>openRef.current(id),onNear:setNear,onMove:pos=>setState(prev=>({...prev,position:pos})),onReady:(scene)=>{if(stateRef.current.room==='courtyard')scene.setRoom('courtyard');setReady(true);}},stateRef.current.position);
   gameRef.current=api;
   return()=>{api.destroy();};
 },[]);
 useEffect(()=>{setStorageOK(saveProgress(state));},[state]);
 useEffect(()=>{gameRef.current?.setPaused(Boolean(modal)); if(modal){setTimeout(()=>modalRef.current?.querySelector('button')?.focus(),20);} },[modal]);
 useEffect(()=>{if(!toast)return;const timer=setTimeout(()=>setToast(''),3800);return()=>clearTimeout(timer);},[toast]);
 useEffect(()=>{const timer=setInterval(()=>setTime(new Date()),60000);return()=>clearInterval(timer);},[]);
 useEffect(()=>{
   const onKey=(e)=>{if(e.key==='Escape'){closeRef.current();return;} if(!modal)return; if(e.key==='Tab'){const nodes=[...modalRef.current.querySelectorAll('button,[href],input,select,textarea,[tabindex="0"]')].filter(n=>!n.disabled);const first=nodes[0],last=nodes.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}};
   window.addEventListener('keydown',onKey);return()=>window.removeEventListener('keydown',onKey);
 },[modal]);
 const collect=(id)=>{if(state.evidence.includes(id))return;patch({evidence:[...state.evidence,id]});notify('Evidence added to your notebook');};
 const submit=(sources)=>{const feedback=evaluateResponse({...state,sources});patch({sources,feedback,completed:feedback.passed||state.completed,responses:[...state.responses,{response:state.response,decision:state.decision,evidence:[...state.evidence],sources,feedback,timestamp:new Date().toISOString()}]});if(feedback.passed)notify('Recommendation delivered · the courtyard is open');};
 const exportRecord=()=>{const record={game:'Signal — Good Intentions',...state,exportedAt:new Date().toISOString()};const url=URL.createObjectURL(new Blob([JSON.stringify(record,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='signal-learning-record.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),500);};
 const toggleSound=()=>{
   if(sound){soundRef.current?.close();soundRef.current=null;setSound(false);return;}
   try {const ctx=new(window.AudioContext||window.webkitAudioContext)(); const buffer=ctx.createBuffer(1,ctx.sampleRate*3,ctx.sampleRate);const d=buffer.getChannelData(0);let previous=0;for(let i=0;i<d.length;i++){previous=(previous+Math.random()*.04-.02)/1.02;d[i]=previous;}const node=ctx.createBufferSource();node.buffer=buffer;node.loop=true;const filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=230;const gain=ctx.createGain();gain.gain.value=.28;node.connect(filter).connect(gain).connect(ctx.destination);node.start();soundRef.current=ctx;setSound(true);}catch{notify('Ambient audio is unavailable. You can still play with captions.');}
 };
 const tasks=[{label:'Meet Maya, the student editor',done:state.talked},{label:'Compare three sources',done:state.evidence.length===3},{label:'Send an informed recommendation',done:state.completed}];
 return <div className="app-shell">
  <header className="topbar"><a href="#" className="wordmark" aria-label="Signal home" onClick={e=>e.preventDefault()}><span className="signal-mark"><i/><i/><i/></span>signal<span className="wordmark-dot">.</span></a><span className="header-divider"/><span className="header-caption">THE STORY BEHIND THE STORY</span><div className="topbar-actions"><span className={`save-status ${!storageOK?'save-error':''}`}><i/>{storageOK?'Progress saved locally':'Local saving unavailable'}</span><button className="icon-button ambient-button" aria-label={sound?'Mute room ambience':'Enable room ambience'} onClick={toggleSound}>{sound?<Volume2 size={19}/>:<VolumeX size={19}/>}</button><button className="support-button" onClick={()=>open('glossary')}><BookOpen size={17}/><span>Language companion</span></button></div></header>
  <main>
   <div className="chapter-heading"><div><div className="chapter-eyebrow"><span>CHAPTER 01</span><span className="chapter-line"/> MEDIA & COMMUNITY</div><h1>Good intentions<span>,</span> <em>better questions.</em></h1></div><button className="chapter-help" onClick={()=>open('help')}><CircleHelp size={18}/> How to play</button></div>
   <section className="adventure-layout">
    <aside className="case-sidebar"><div className="case-label"><Compass size={17}/><span>YOUR ASSIGNMENT</span></div><h2>A story worth<br/>checking.</h2><p className="case-intro">{support[state.level].intro}</p><div className="case-separator"/><span className="eyebrow">FOLLOW THE LEAD</span><ol className="objectives">{tasks.map((t,i)=><li key={t.label} className={t.done?'done':''}><span>{t.done?<Check size={12}/>:String(i+1).padStart(2,'0')}</span><p>{t.label}</p></li>)}</ol><button className="notebook-button" onClick={()=>open('notebook')}><span className="notebook-icon"><BookOpen size={21}/></span><span><strong>Field notebook</strong><small>{state.evidence.length} / 3 sources collected</small></span><ArrowUpRight size={17}/></button><div className="support-setting"><label htmlFor="level"><Settings2 size={15}/> Language support</label><div className="select-wrap"><select id="level" aria-label="Language support level" value={state.level} onChange={e=>patch({level:Number(e.target.value)})}><option value="2">Level 2 · More support</option><option value="3">Level 3 · Guided support</option><option value="4">Level 4 · Light support</option></select><ChevronDown size={13}/></div><small>Same mystery. A little more help.</small></div><div className="sidebar-bottom"><Leaf size={14}/><span>Good stories can do good.</span></div></aside>
    <div className="world-column"><div className="scene-frame"><div ref={hostRef} className="phaser-host" aria-label="Explorable school newsroom. Use WASD or arrow keys to move, click to walk, E to interact." tabIndex="0"/>{!ready&&<div className="scene-loading">Opening the newsroom…</div>}<div className="location-plaque"><span className="location-icon"><MapPin size={16}/></span><div><span>RIVERSIDE HIGH</span><strong>{state.room==='courtyard'?'The courtyard':'The newsroom'}</strong></div></div><div className="scene-time"><span className="sun-symbol">☀</span> LATE AFTERNOON <i/> 16:42</div><div className="scene-chapter">01 <span>/ THE GOOD INTENTIONS</span></div><button className="scene-fullscreen icon-button" aria-label="Expand game view" onClick={()=>{const el=document.querySelector('.scene-frame');if(document.fullscreenElement)document.exitFullscreen?.();else if(el.requestFullscreen)el.requestFullscreen();else notify('Use your browser’s fullscreen mode for a larger view.');}}><Maximize2 size={17}/></button>{near&&!modal&&<button className="interaction-prompt" onClick={()=>open(near.id)}><kbd>E</kbd><span>{near.label}</span><ArrowRight size={16}/></button>}<div className="world-caption"><i/><span>{state.room==='courtyard'?'A small next step. A real difference.':'The next edition is waiting. So is the truth.'}</span></div></div>
    <div className="controls-strip"><div><span className="key-group"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd></span><span>or arrow keys to move</span><span className="control-dot">·</span><span className="mouse-icon"/> <span>Click to walk</span><span className="control-dot">·</span><kbd>E</kbd><span>to interact</span></div><span className="live-indicator"><i/> {state.completed?'STORY COMPLETE':'EXPLORE AT YOUR PACE'}</span></div>
    <div className="story-note"><span className="note-line"/><span><strong>{state.completed?'Your words made a difference.':'Not every headline tells the whole story.'}</strong> {state.completed?'Step through the courtyard door to see what happens next.':'Talk to Maya. Look closely. Find out who your help is really helping.'}</span><Bookmark size={17}/></div></div>
   </section>
   <footer className="page-footer"><span>AN ENGLISH LANGUAGE ADVENTURE</span><span>Read the world. <em>Change the story.</em></span><span>01 — THE NEWSROOM</span></footer>
  </main>
  {toast&&<div className="toast" role="status"><Check size={17}/>{toast}</div>}
  {modal&&<div className="modal-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)close();}}><section ref={modalRef} className={`modal-window modal-${modal}`} role="dialog" aria-modal="true" aria-labelledby="modal-title"><header className="modal-titlebar"><div><span className="inworld-indicator"/><h2 id="modal-title">{titles[modal]}</h2></div><button className="icon-button" onClick={close} aria-label="Close interaction"><X size={20}/></button></header><div className="modal-scroll">
   {modal==='laptop'&&<Campaign state={state} collect={collect}/>}
   {modal==='noticeboard'&&<Notice state={state} collect={collect}/>}
   {modal==='inbox'&&<Inbox state={state} collect={collect}/>}
   {modal==='editor'&&<Dialogue state={state} onChoice={choice=>patch({talked:true,dialogueChoice:choice})} onCheckpoint={()=>setModal('assessment')}/>}
   {modal==='assessment'&&<Assessment state={state} onChange={patch} onSubmit={submit}/>}
   {modal==='notebook'&&<Notebook state={state} onOpen={setModal} onExport={exportRecord}/>}
   {modal==='glossary'&&<Glossary/>}
   {modal==='door'&&<div className="simple-view"><MapPin size={35}/><span className="eyebrow">ONE MORE THING BEFORE YOU GO</span><h2>The story comes first.</h2><p>Maya is waiting for your recommendation. Investigate the three sources and send her an editorial note before meeting the community in the courtyard.</p><button className="button primary" onClick={()=>setModal(state.talked?'assessment':'editor')}>{state.talked?'Write your recommendation':'Talk with Maya'}<ArrowRight size={16}/></button></div>}
   {modal==='help'&&<div className="simple-view help-view"><Compass size={35}/><span className="eyebrow">WELCOME TO RIVERSIDE</span><h2>You’re part of the newsroom.</h2><p>A viral donation appeal could help your community. Maya needs you to check its claims before the school shares it.</p><div className="help-steps"><div><kbd>W A S D</kbd><p>Move with WASD or arrow keys. Click the floor to walk there.</p></div><div><kbd>E</kbd><p>Walk near a glowing marker and press E, or click an object to approach it.</p></div><div><BookOpen/><p>Save three sources to your notebook. Talk with Maya, then write a recommendation using evidence.</p></div></div><p className="muted">Your position, evidence, drafts, and submitted responses save in this browser. No name or account is needed. Audio is optional; every spoken line has text.</p><button className="button primary" onClick={close}>Step into the story <ArrowRight size={17}/></button></div>}
   {modal==='ending'&&<div className="simple-view ending-view"><span className="ending-icon"><Leaf size={31}/></span><span className="eyebrow">CHAPTER 01 · COMPLETE</span><h2>Better questions.<br/><em>Better help.</em></h2><p>{state.decision==='pause'?'The school pauses the appeal and organizes a collection of blankets and school supplies with Ms Chen.':state.decision==='verify'?'Maya asks the organizer to verify the kit numbers and costs. Meanwhile, Ms Chen helps the school plan a needs-led collection.':'Maya publishes your qualified report, clearly separating the campaign’s claims from confirmed community needs.'}</p><blockquote>“You helped us tell a more responsible story — and listen to the people at its heart.”<br/><small>— Maya Patel</small></blockquote><div className="ending-result"><Check size={17}/> Three sources compared · Recommendation delivered · Progress saved</div><button className="button primary" onClick={close}>Explore the courtyard <ArrowRight size={17}/></button><button className="text-button" onClick={exportRecord}>Export your learning record</button></div>}
  </div><footer className="modal-footer"><span><ShieldCheck size={13}/> Part of your investigation</span><span><kbd>ESC</kbd> to return to the room</span></footer></section></div>}
 </div>;
}
export default App;
