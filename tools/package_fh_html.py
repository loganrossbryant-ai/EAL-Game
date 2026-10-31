"""Embed a tested Godot export and both audio worklets in one distributable HTML.

Uses the pinned Godot 4.6.3 loader. Test the output over HTTP; this managed browser
blocks file://. The file contains no external game-asset URLs.
"""
import argparse, base64, gzip, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = r'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Far Horizon — Session 01</title>
<link rel="icon" href="data:image/svg+xml;base64,__ICON__">
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#06141d;color:#eaf0ed}
#canvas{display:block;width:100%;height:100%;outline:none;touch-action:none}
#status{position:fixed;inset:0;display:grid;place-content:center;background:radial-gradient(ellipse at 70% 30%,#183744,#06141d 75%);font:18px/1.6 Arial,sans-serif;padding:30px;z-index:2}
#status section{max-width:650px;border-left:2px solid #84d5df;padding:10px 36px}
#status small{color:#edbd7e;letter-spacing:.2em}h1{font-size:clamp(32px,5vw,58px);line-height:1.15;margin:20px 0}p{color:#bdd1d7}progress{width:100%;height:4px;accent-color:#84d5df}
</style></head><body>
<canvas id="canvas" tabindex="0" aria-label="Far Horizon game. A or D to move, E to interact, 1 to 4 to switch departments, L for crew log, G for GM cues, Escape to close panels.">Open this game in a current Chrome or Edge browser.</canvas>
<div id="status" role="status"><section><small>CSV-01 / COHORT 01 / 2247</small><h1>THE FAR HORIZON</h1><p>Session 01 — Welcome to Pioneer</p><p id="message">Preparing your ship…</p><progress id="progress" max="5" value="0"></progress></section></div>
<template id="license-notices"><pre>__LICENSES__</pre></template>
<script type="application/json" id="game-data">__ASSETS__</script>
<script>
(async()=>{
 const message=document.querySelector('#message'),progress=document.querySelector('#progress');
 try {
  if(!window.DecompressionStream)throw Error('Use a current Chrome or Edge browser.');
  const encoded=JSON.parse(document.querySelector('#game-data').textContent),buffers={},urls={};
  for(const [name,data] of Object.entries(encoded)){
   const binary=atob(data),bytes=new Uint8Array(binary.length);
   for(let i=0;i<binary.length;i++)bytes[i]=binary.charCodeAt(i);
   buffers[name]=await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
   urls[name]=URL.createObjectURL(new Blob([buffers[name]],{type:name.endsWith('.wasm')?'application/wasm':'text/javascript'}));
   progress.value++;
  }
  document.querySelector('#game-data').remove();
  const fetchOriginal=window.fetch.bind(window);
  window.fetch=(input,init)=>{
   const address=typeof input==='string'?input:input.url;
   if(address&&address.split('/').pop().split('?')[0]==='far-horizon.wasm')return Promise.resolve(new Response(buffers['index.wasm'],{headers:{'Content-Type':'application/wasm','Content-Length':String(buffers['index.wasm'].byteLength)}}));
   return fetchOriginal(input,init);
  };
  await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=urls['index.js'];s.onload=resolve;s.onerror=()=>reject(Error('The game engine could not load.'));document.head.append(s);});
  const missing=Engine.getMissingFeatures({threads:false});if(missing.length)throw Error('Browser features needed: '+missing.join(', '));
  const engine=new Engine({executable:'far-horizon',canvas:document.querySelector('#canvas'),canvasResizePolicy:2,focusCanvas:true,experimentalVK:true,persistentPaths:[],args:['--main-pack','far-horizon.pck']});
  // Godot 4.6.3 resolves audio helpers through this instance configuration.
  // Supply embedded Blob modules rather than making file/network requests.
  const originalConfig=engine.config.getModuleConfig.bind(engine.config);
  engine.config.getModuleConfig=(path,response)=>{
   const config=originalConfig(path,response),locate=config.locateFile;
   config.locateFile=name=>name.endsWith('.audio.position.worklet.js')?urls['index.audio.position.worklet.js']:name.endsWith('.audio.worklet.js')?urls['index.audio.worklet.js']:locate(name);
   return config;
  };
  message.textContent='The last room on Earth is waiting.';
  await engine.init('far-horizon');
  engine.copyToFS('/userfs/.keep',new Uint8Array(0));
  await engine.preloadFile(buffers['index.pck'],'far-horizon.pck');
  await engine.start();document.querySelector('#status').remove();
 }catch(error){console.error(error);message.textContent='The game could not start. '+(error.message||String(error));progress.remove();}
})();
</script></body></html>'''

def package(build, output):
    names=['index.js','index.wasm','index.pck','index.audio.worklet.js','index.audio.position.worklet.js']
    assets={name:base64.b64encode(gzip.compress((build/name).read_bytes(),compresslevel=9,mtime=0)).decode('ascii') for name in names}
    notices=[]
    for p in sorted((ROOT/'far-horizon').glob('GODOT-*.txt'))+sorted((ROOT/'far-horizon/assets/fonts').glob('LICENSE-*.txt')):
        notices.append(p.name+'\n\n'+p.read_text())
    notices.append('Far Horizon original game art generated from the user-supplied Session 1 visual references. Original ambient/SFX synthesis: tools/synthesize_fh_audio.py. No Silver Pines assets, source media M01/M02, raw GM bible, or later-session material are distributed.')
    page=SHELL.replace('__ASSETS__',json.dumps(assets,separators=(',',':'))).replace('__LICENSES__',html.escape('\n\n'.join(notices))).replace('__ICON__',base64.b64encode((ROOT/'far-horizon/assets/icon.svg').read_bytes()).decode('ascii'))
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(page,encoding='utf-8')
    print(f'{output}: {output.stat().st_size/1024/1024:.1f} MiB; engine, artwork, fonts, audio and license notices embedded.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--build',type=Path,default=ROOT/'builds/far-horizon-release')
    parser.add_argument('--output',type=Path,default=ROOT/'builds/far-horizon-delivery/index.html')
    args=parser.parse_args();package(args.build,args.output)
