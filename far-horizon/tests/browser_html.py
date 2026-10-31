"""Verify the delivered single HTML, using browser input and actual persisted state."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests'
URL=os.environ.get('FH_HTML_URL','http://127.0.0.1:8071/')
STANDARD=os.environ.get('FH_STANDARD_BUILD')=='1'
async def run():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1280,'height':720})
  errors=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('request',lambda r:requests.append(r.url))
  async def ready():
   await page.wait_for_selector('#status',state='detached',timeout=90000)
   await page.wait_for_function("localStorage.getItem('far-horizon-session1-v1')",timeout=15000)
  async def state():return await page.evaluate("JSON.parse(localStorage.getItem('far-horizon-session1-v1'))")
  async def click(x,y):await page.mouse.click(x*1280/1366,y*720/768);await page.wait_for_timeout(350)
  async def wait(js):await page.wait_for_function("(()=>{const s=JSON.parse(localStorage.getItem('far-horizon-session1-v1'));return s&&("+js+");})()",timeout=20000)
  async def write(text):
   await page.keyboard.press('Control+a')
   await page.evaluate('''text=>{const target=document.activeElement===document.body?document.querySelector('#canvas'):document.activeElement;for(const key of text){const code=/[a-z]/i.test(key)?'Key'+key.toUpperCase():key===' '?'Space':key==='.'?'Period':'';const o={key,code,shiftKey:/[A-Z]/.test(key),bubbles:true,cancelable:true};target.dispatchEvent(new KeyboardEvent('keydown',o));target.dispatchEvent(new KeyboardEvent('keyup',o));}}''',text)
   await page.wait_for_timeout(400)
  await page.goto(URL)
  await ready()
  assert await page.evaluate('typeof window.farHorizonTestState')=='undefined','Debug observations leaked into release.'
  await click(245,348)
  await click(911,59)
  await page.keyboard.down('d');await wait('s.position>670');await page.keyboard.up('d')
  await page.wait_for_timeout(400)
  await page.keyboard.press('l')
  values=['I leave because I want to build a second home.','I want to prove I can lead.','I need to learn to listen.','I fear losing our stories.','I brought a stone from the sea.']
  for i,text in enumerate(values):await click(690,243+i*73);await write(text)
  await click(600,635);await wait('!!s.records["Orion Kade"]')
  assert (await state())['records']['Orion Kade']['need']==values[2]
  await page.screenshot(path=str(OUT/'17-html-1280-log.png'))
  await page.keyboard.press('Escape')
  await page.reload();await ready()
  assert (await state())['records']['Orion Kade']['object']==values[4]
  await page.screenshot(path=str(OUT/'18-html-1280-world.png'))
  # Restore a real save exported by the full classroom-route test, then test
  # new-class controls. This is a persistence fixture, not a game action API.
  completed=json.loads((OUT/'session-export.json').read_text())
  await page.evaluate("s=>localStorage.setItem('far-horizon-session1-v1',JSON.stringify(s))",completed)
  await page.reload();await ready()
  await click(990,649)
  await page.screenshot(path=str(OUT/'19-new-class-confirmation.png'))
  await click(920,454)
  await wait('s.scene==="terminal" && !s.finished && Object.keys(s.records).length===0')
  await page.screenshot(path=str(OUT/'20-new-class.png'))
  allowed={URL.rstrip('/'),URL.rstrip('/')+'/'}
  if STANDARD:
   manifest=json.loads((ROOT/'review-candidate/manifest.json').read_text())
   allowed.update(URL.rstrip('/')+'/'+entry['path'] for entry in manifest['files'])
  external=[u for u in requests if u.startswith(('http:','https:')) and u not in allowed]
  assert not external,external
  assert not errors,errors
  result={'passed':True,'format':'standard Godot web export' if STANDARD else 'single embedded HTML','viewport':'1280x720','checks':['release startup','audio worklets','real movement','crew writing','reload persistence','release without debug globals','new-class confirmation and reset'],'unexpected_network_requests':external,'browser_errors':errors,'file_protocol':'Standard Godot web delivery requires an HTTP/HTTPS host.' if STANDARD else 'Not tested: managed Chromium blocks file://.'}
  (OUT/('standard-result.json' if STANDARD else 'html-result.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
  await browser.close()
asyncio.run(run())
