const ambientSources = {
  river: {x:560, y:364, near:.51, falloff:410, base:.12},
  breeze: {x:680, y:300, near:.24, falloff:380, base:.10},
  wildlife: {x:884, y:280, near:.24, falloff:370, base:.048},
  cabin: {x:78, y:409, near:.40, falloff:150, base:0},
};

export function createSoundscape({bank, voices, onUnavailable}) {
  let context, master, voice, sceneX=278, sceneY=449, lastMix=-1, stepIndex=0, loaded=false;
  let preferences={enabled:false, voice:true, ambience:true, effects:true};
  const buses={}, buffers=new Map(), loops=new Map();

  function routeGain(destination, level) {
    const gain=context.createGain();
    gain.gain.value=level;
    gain.connect(destination);
    return gain;
  }

  function unlocked() {
    return context?.state==='running';
  }

  function prepare() {
    if(context)return;
    const AudioEngine=window.AudioContext||window.webkitAudioContext;
    if(!AudioEngine)throw new Error('No Web Audio support');
    context=new AudioEngine();
    const limiter=context.createDynamicsCompressor();
    limiter.threshold.value=-9;
    limiter.ratio.value=5;
    limiter.connect(context.destination);
    master=routeGain(limiter,0);
    buses.voice=routeGain(master,.86);
    buses.ambience=routeGain(master,1);
    buses.effects=routeGain(master,.80);
  }

  function decode(id) {
    if(!buffers.has(id)){
      const bytes=Uint8Array.from(atob(bank[id].split(',')[1]),char=>char.charCodeAt(0));
      buffers.set(id,context.decodeAudioData(bytes.buffer));
    }
    return buffers.get(id);
  }

  function balance(x) {
    return Math.max(-.76,Math.min(.76,(x-sceneX)/360));
  }

  function positionNode(destination) {
    const node=context.createStereoPanner?.()??context.createGain();
    node.connect(destination);
    return node;
  }

  function automate(parameter,value,ramp=.09) {
    parameter?.setTargetAtTime(value,context.currentTime,ramp);
  }

  function spatialMix() {
    if(!context)return;
    for(const [id,{gain,pan}] of loops) {
      const {x,y,near,falloff,base}=ambientSources[id];
      const distance=Math.hypot(sceneX-x,(sceneY-y)*2.8);
      const focus=Math.exp(-((distance/falloff)**2));
      automate(gain.gain,base+near*focus,.28);
      automate(pan.pan,balance(x),.25);
    }
    automate(voice?.pan.pan,voice?balance(voice.x)*.50:0,.15);
  }

  function update(next) {
    preferences={...next};
    if(!context)return;
    if(!preferences.enabled||!preferences.voice)stopVoice();
    automate(master.gain,preferences.enabled&&!document.hidden?1:0,.025);
    automate(buses.voice.gain,preferences.voice ? .86 : 0,.035);
    automate(buses.ambience.gain,preferences.ambience?(voice ? .55 : 1):0,.12);
    automate(buses.effects.gain,preferences.effects ? .80 : 0,.04);
  }

  async function unlock({quiet=false}={}) {
    if(!preferences.enabled)return false;
    try {
      prepare();
      if(!unlocked())await context.resume();
      if(!unlocked())return false;
      update(preferences);
      if(loaded)return true;
      loaded=true;
      for(const id of Object.keys(bank)){
        const buffer=decode(id);
        if(!Object.hasOwn(ambientSources,id)){buffer.catch(()=>onUnavailable());continue;}
        if(loops.has(id))continue;
        const pan=positionNode(buses.ambience);
        const gain=routeGain(pan,0);
        loops.set(id,{gain,pan});
        buffer.then(value=>{
          const source=context.createBufferSource();
          source.buffer=value;
          source.loop=true;
          source.connect(gain);
          source.start();
          spatialMix();
        }).catch(()=>onUnavailable());
      }
      return true;
    } catch {
      if(!quiet)onUnavailable();
      return false;
    }
  }

  function stopVoice() {
    if(!voice)return;
    const current=voice;
    voice=null;
    current.audio.pause();
    current.source.disconnect();
    current.pan.disconnect();
    automate(buses.ambience.gain,preferences.ambience?1:0,.12);
  }

  function playVoice(id,x) {
    if(!preferences.enabled||!preferences.voice||!Object.hasOwn(voices,id))return null;
    try {
      prepare();
      void unlock();
      stopVoice();
      const audio=new Audio(voices[id]);
      const source=context.createMediaElementSource(audio);
      const pan=positionNode(buses.voice);
      source.connect(pan);
      voice={audio,source,pan,x:x??sceneX};
      spatialMix();
      update(preferences);
      audio.addEventListener('ended',()=>{if(voice?.audio===audio)stopVoice();},{once:true});
      audio.play().catch(()=>{
        if(voice?.audio!==audio)return;
        stopVoice();
        onUnavailable();
      });
      return audio;
    } catch {
      onUnavailable();
      return null;
    }
  }

  function at(x,y,t) {
    if(t-lastMix<.08)return;
    sceneX=x;sceneY=y;lastMix=t;
    spatialMix();
  }

  function cue(id,x=sceneX,level=.60) {
    if(!unlocked()||!preferences.enabled||!preferences.effects||!Object.hasOwn(bank,id))return;
    decode(id).then(buffer=>{
      if(!preferences.enabled||!preferences.effects)return;
      const source=context.createBufferSource();
      const pan=positionNode(buses.effects);
      if(pan.pan)pan.pan.value=balance(x);
      const gain=routeGain(pan,level);
      source.buffer=buffer;
      source.connect(gain);
      source.start();
      source.onended=()=>{source.disconnect();gain.disconnect();pan.disconnect();};
    }).catch(()=>onUnavailable());
  }

  function foot(surface,x,level=.53) {
    stepIndex=(stepIndex+1)%9;
    cue('step-'+surface+'-'+(stepIndex%3+1),x,level);
    if(surface==='stone'&&stepIndex%3===1)cue('splash',x,.30*level);
    if(surface==='wood'&&stepIndex%5===1)cue('bridge-creak',x,.55*level);
  }

  document.addEventListener('visibilitychange',()=>update(preferences));
  return {update, unlock, stopVoice, playVoice, at, cue, foot,
    voicePlaying:()=>Boolean(voice&&!voice.audio.paused&&!voice.audio.ended)};
}
