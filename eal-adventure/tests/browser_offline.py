"""Test final release bytes, cold browser restart, disabled networking and PCM output."""
from pathlib import Path
import json, tempfile, time, io, os
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/alan-tests'
URL=os.environ.get('ALAN_RELEASE_URL','http://127.0.0.1:8093/')
PROFILE=Path(tempfile.mkdtemp(prefix='alan-offline-',dir=ROOT.parent))
report={'checks':[],'errors':[],'runtime':'Chromium; actual iOS Safari still requires device verification'}
report['build_version']=json.loads((ROOT/'builds/alan-island/asset-manifest.json').read_text())['version']
METER=r"""
window.__audioMeter={peak:0,rms:0,contexts:[]};
if(window.AudioNode){
 const original=AudioNode.prototype.connect;
 AudioNode.prototype.connect=function(destination,...args){
   const result=original.call(this,destination,...args);
   if(destination instanceof AudioDestinationNode){
     const analyser=this.context.createAnalyser();analyser.fftSize=2048;
     original.call(this,analyser);
     const samples=new Float32Array(analyser.fftSize);
     window.__audioMeter.contexts.push(this.context);
     setInterval(()=>{analyser.getFloatTimeDomainData(samples);let sum=0;for(const x of samples)sum+=x*x;const rms=Math.sqrt(sum/samples.length);window.__audioMeter.rms=rms;window.__audioMeter.peak=Math.max(window.__audioMeter.peak,rms)},40);
   }
   return result;
 };
}
"""
def wait_panel(opened=True):
    end=time.monotonic()+30
    while time.monotonic()<end:
        # Left panel padding stays clear of the differently colored action buttons.
        rgb=Image.open(io.BytesIO(page.screenshot(clip={'x':90,'y':780,'width':1,'height':1}))).convert('RGB').getpixel((0,0))
        visible=sum(abs(a-b) for a,b in zip(rgb,(255,249,232)))<12
        if visible==opened:return
        page.wait_for_timeout(220)
    page.screenshot(path=str(OUT/'offline-panel-timeout.png'))
    (OUT/'offline-panel-state.json').write_text(page.evaluate("localStorage.getItem('alan-favorites-island-v1')"))
    raise AssertionError('Expected visible dialogue panel: '+str(opened))

def check(name,condition):
    if not condition:
        page.screenshot(path=str(OUT/'offline-failure.png'))
        (OUT/'offline-failure.json').write_text(json.dumps(report,indent=2))
    assert condition,name
    report['checks'].append(name);print('PASS',name,flush=True)
with sync_playwright() as p:
    def launch():
        c=p.chromium.launch_persistent_context(str(PROFILE),executable_path='/usr/bin/chromium',headless=True,viewport={'width':1440,'height':960},args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl'])
        c.add_init_script(METER)
        return c
    context=launch();page=context.pages[0]
    page.goto(URL)
    page.get_by_role('button',name='Save for offline').click()
    page.wait_for_function("document.getElementById('status').textContent.startsWith('Offline ready')",timeout=120000)
    page.wait_for_function('navigator.serviceWorker.controller',timeout=30000)
    entries=page.evaluate("async()=>{let all=[];for(const name of await caches.keys())if(name.startsWith('alan-island-')){const c=await caches.open(name);all=(await c.keys()).map(x=>x.url)}return all}")
    check('Offline installer caches every Godot dependency',any(x.endswith('index.wasm') for x in entries) and any(x.endswith('index.pck') for x in entries) and any(x.endswith('_offline_complete') for x in entries))
    page.screenshot(path=str(OUT/'08-offline-ready.png'))
    page.get_by_role('link',name='Play with Pip').click()
    page.wait_for_function("!document.getElementById('status')",timeout=60000);page.wait_for_timeout(600)
    check('Production export has no test bridge',page.evaluate('typeof window.__alanTest')=='undefined')
    page.mouse.click(220,745);page.wait_for_timeout(1000)
    check('Jesse MP3 produces actual decoded audio samples',page.evaluate('window.__audioMeter.peak')>.0005)
    report['jesse_pcm_peak']=page.evaluate('window.__audioMeter.peak')
    page.mouse.click(1125,745);page.wait_for_timeout(500)
    page.mouse.click(300,745);page.wait_for_timeout(500)
    page.mouse.click(1168,250);wait_panel()
    page.mouse.click(1125,745);page.wait_for_timeout(500)
    def saved():return page.evaluate("JSON.parse(localStorage.getItem('alan-favorites-island-v1'))")
    check('Release mission begins through real input',saved()['stage']==1)
    context.close()
    # New browser process and disk-backed profile: neither open tabs nor game
    # memory can supply assets. Playwright disables every network connection.
    context=launch();context.set_offline(True);page=context.pages[0]
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
    page.goto(URL,wait_until='domcontentloaded')
    page.wait_for_function("document.getElementById('status').textContent.startsWith('Offline ready')",timeout=10000)
    check('Home Screen entry loads after a cold offline restart',True)
    page.get_by_role('link',name='Play with Pip').click()
    page.wait_for_function("!document.getElementById('status')",timeout=60000);page.wait_for_timeout(600)
    check('Bundled game starts with networking disabled',saved()['stage']==1)
    page.mouse.click(1125,745);page.wait_for_timeout(500)
    page.mouse.click(577,368);wait_panel()
    page.mouse.click(248,462);wait_panel(False)
    check('Offline food pickup works',saved()['carrying']=='pizza')
    page.mouse.click(1168,250);wait_panel()
    page.mouse.click(1050,745);page.wait_for_timeout(500)
    check('Offline delivery works',saved()['stage']==2)
    for x,y in [(715,524),(299,524),(715,618),(1131,524),(1070,745)]:
        page.mouse.click(x,y);page.wait_for_timeout(180)
    page.wait_for_timeout(500)
    check('Offline sentence logic works',saved()['stage']==3)
    page.mouse.click(1125,745);page.wait_for_timeout(400)
    page.mouse.click(248,462);page.wait_for_timeout(500)
    check('Offline personal choice works',saved()['favorite']=='rice' and saved()['stage']==5)
    page.mouse.click(1261,224);page.wait_for_timeout(400)
    page.mouse.click(363,298);wait_panel()
    check('Offline mission reaches its visible ending',saved()['stage']==6 and saved()['festival'])
    page.mouse.click(300,745);page.wait_for_timeout(500)
    page.screenshot(path=str(OUT/'09-offline-festival.png'))
    # Reach a newly added topic using only cached assets and real input.
    page.mouse.click(145,200);page.wait_for_timeout(1000)
    page.mouse.click(408,310)
    page.wait_for_function("JSON.parse(localStorage.getItem('alan-favorites-island-v1')).topic_quests.animals",timeout=30000)
    page.mouse.click(1117,219);wait_panel()
    page.mouse.click(1125,749);wait_panel(False)
    page.mouse.click(612,323);wait_panel()
    page.mouse.click(248,480);wait_panel(False)
    check('New dolphin picture is available offline',saved()['topic_quests']['animals']['carrying']=='animals_dolphin')
    page.mouse.click(1117,219);wait_panel()
    page.mouse.click(1075,749);page.wait_for_timeout(600)
    check('New NPC delivery works offline',saved()['topic_quests']['animals']['stage']==2)
    page.screenshot(path=str(OUT/'expanded-offline.png'))
    page.mouse.click(1261,227);wait_panel(False)
    page.mouse.click(1352,77);page.wait_for_timeout(1000)
    # Isolate the voice channel: music volume zero, then listen, then master mute.
    page.mouse.click(1346,77);page.wait_for_timeout(400)
    page.mouse.click(513,491);page.wait_for_timeout(500)
    check('Separate music control saves a zero level',saved()['settings']['music']<=.05)
    page.evaluate('window.__audioMeter.peak=0')
    page.mouse.click(690,623);page.wait_for_timeout(1200)
    check('Jesse audio replays while offline',page.evaluate('window.__audioMeter.peak')>.0005)
    page.mouse.click(280,623);page.wait_for_timeout(700)
    page.evaluate('window.__audioMeter.peak=0')
    page.mouse.click(690,623);page.wait_for_timeout(700)
    check('Master mute suppresses actual audio output',page.evaluate('window.__audioMeter.peak')<.0001)
    check('Final release has no browser or Godot errors',not report['errors'])
    report['offline_cache_entries']=entries
    report['saved_progress']=saved()
    context.close()
(OUT/'offline-report.json').write_text(json.dumps(report,indent=2))
print('COMPLETED',len(report['checks']),'release/offline checks',flush=True)
