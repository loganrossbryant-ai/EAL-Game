"""Upgrade a genuinely installed v1 pack; retain the learner's saved choices."""
from pathlib import Path
import io,tarfile,subprocess,shutil,tempfile,json,hashlib,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/expanded-tests';OUT.mkdir(parents=True,exist_ok=True)
fixture=Path(tempfile.mkdtemp(prefix='alan-update-site-',dir=ROOT.parent))
profile=Path(tempfile.mkdtemp(prefix='alan-update-browser-',dir=ROOT.parent))
old_commit='afa83513b3b2cd7618eea2f35032beaa7b4c5bde'
raw=subprocess.check_output(['git','archive',old_commit,'alan-review/candidate/web'],cwd=ROOT)
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
    for member in archive.getmembers():
        if not member.isfile():continue
        relative=Path(member.name).relative_to('alan-review/candidate/web')
        target=fixture/relative;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(archive.extractfile(member).read())
del raw
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8094),partial(Quiet,directory=str(fixture)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:8094/'
checks=[]
def check(name,value):
    assert value,name
    checks.append(name);print('PASS',name,flush=True)
with sync_playwright() as p:
    def launch():return p.chromium.launch_persistent_context(str(profile),executable_path='/usr/bin/chromium',headless=True,viewport={'width':960,'height':640},args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl'])
    context=launch();page=context.pages[0]
    page.goto(url);page.get_by_role('button',name='Save for offline').click()
    page.wait_for_function("document.getElementById('status').textContent.startsWith('Offline ready')",timeout=120000)
    page.get_by_role('link',name='Play with Pip').click()
    page.wait_for_function("!document.getElementById('status')",timeout=60000);page.wait_for_timeout(700)
    def tap(x,y):page.mouse.click(x*2/3,y*2/3);page.wait_for_timeout(500)
    tap(1125,749);tap(300,749);tap(1044,77);tap(1193,77);tap(559,462)
    old_save=page.evaluate("JSON.parse(localStorage.getItem('alan-favorites-island-v1'))")
    check('Installed old game has a real saved personal choice',old_save['favorite']=='rice' and old_save['settings']['chinese'])
    page.evaluate("async()=>{const c=await caches.open('unrelated-classroom-cache');await c.put('/keep-this',new Response('keep'));localStorage.setItem('unrelated-classroom-save','keep')}")
    context.close()
    # Simulate publication with current file dates. Preserving older source mtimes
    # would make this test server incorrectly return 304 for changed worker bytes.
    shutil.copytree(ROOT/'builds/alan-island',fixture,dirs_exist_ok=True,copy_function=shutil.copyfile)
    manifest=json.loads((fixture/'asset-manifest.json').read_text())
    expected_hash=hashlib.sha256((fixture/'index.pck').read_bytes()).hexdigest()
    context=launch();page=context.pages[0];page.goto(url+'update.html')
    try:
        page.wait_for_function("document.getElementById('status').textContent.startsWith('Offline ready')",timeout=120000)
    except Exception:
        page.screenshot(path=str(OUT/'update-failure.png'))
        state=page.evaluate("async()=>({status:document.getElementById('status').textContent,caches:await caches.keys(),workers:(await navigator.serviceWorker.getRegistrations()).map(x=>({active:x.active?.state,waiting:x.waiting?.state,installing:x.installing?.state})),controlled:!!navigator.serviceWorker.controller})")
        (OUT/'update-failure.json').write_text(json.dumps(state,indent=2))
        raise
    cache='alan-island-'+manifest['version']
    live_hash=page.evaluate("""async({cache,url})=>{const c=await caches.open(cache);const r=await c.match(url+'index.pck');const h=await crypto.subtle.digest('SHA-256',await r.arrayBuffer());return Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}""",{'cache':cache,'url':url})
    check('Previously installed app receives the new game bytes',live_hash==expected_hash)
    keys=page.evaluate('caches.keys()')
    check('Old vocabulary pack is replaced',keys==[cache,'unrelated-classroom-cache'] or set(keys)=={cache,'unrelated-classroom-cache'})
    check('Unrelated classroom data is preserved',page.evaluate("localStorage.getItem('unrelated-classroom-save')")=='keep')
    page.get_by_role('link',name='Play with Pip').click()
    page.wait_for_function("!document.getElementById('status')",timeout=60000);page.wait_for_timeout(500)
    updated=page.evaluate("JSON.parse(localStorage.getItem('alan-favorites-island-v1'))")
    check('Saved favorite and speaking history survive the update',updated['favorite']=='rice' and updated['patterns']==old_save['patterns'])
    check('Existing Chinese-help setting is retained under the new policy',updated['settings']['chinese'])
    page.screenshot(path=str(OUT/'upgrade-preserved.png'))
    context.close()
server.shutdown()
(OUT/'update-report.json').write_text(json.dumps({'checks':checks,'new_cache':cache,'pck_sha256':expected_hash},indent=2))
