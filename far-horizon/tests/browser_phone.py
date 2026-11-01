"""Real touch input on the shared preview page, using iPhone-size emulation.
This checks mobile layout and interaction; it is not a physical iPhone test.
"""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/phone'
URL=os.environ.get('FH_PREVIEW_URL','http://127.0.0.1:8092')

async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[];requests=set()
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  device=dict(p.devices['iPhone 13']);device.pop('default_browser_type',None)
  context=await browser.new_context(**device)
  await context.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__observedPreview=e.data.state;});")
  page=await context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);page.on('request',lambda r:requests.add(r.url))
  await page.goto(URL+'/play.html');await page.screenshot(path=str(OUT/'01-portrait-welcome.png'),scale='css')
  await page.set_viewport_size({'width':844,'height':390});await page.locator('#begin').tap()
  async def state(check=lambda s:True):
   for _ in range(600):
    s=await page.evaluate('window.__observedPreview')
    if s and check(s):return s
    await page.wait_for_timeout(100)
   raise AssertionError('No expected preview state: '+json.dumps(s))
  s=await state();assert s['phone_view'] and s['volumetric'];assert s['scene']=='s1_terminal'
  await page.screenshot(path=str(OUT/'02-landscape-game.png'),scale='css')
  cdp=await context.new_cdp_session(page)
  async def hold(id,predicate):
   box=await page.locator('#'+id).bounding_box();assert box
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box['x']+box['width']/2,'y':box['y']+box['height']/2,'id':1}]})
   reached=await state(predicate)
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   await state(lambda s:all(abs(m['vx'])<1 for m in s['party']))
   return reached
  await hold('right',lambda s:s['nearest']=='route:change')
  await page.locator('#use').tap();await state(lambda s:s['upper_route'] and not s['branch_pending'])
  await hold('right',lambda s:s['party'][0]['x']>1530)
  await page.screenshot(path=str(OUT/'03-touch-depth-route.png'),scale='css')
  await page.locator('#use').tap();await state(lambda s:s['physical_inspection'] and s['stage_camera_size']<1.7)
  await page.screenshot(path=str(OUT/'04-touch-item-zoom.png'),scale='css')
  await page.locator('#read').tap();await page.locator('#sheet-title').filter(has_text='Mission briefing').wait_for()
  assert 'Asteria-4' in await page.locator('#sheet-content').inner_text()
  await page.screenshot(path=str(OUT/'05-readable-clue.png'),scale='css')
  await page.locator('#dismiss').tap();await state(lambda s:not s['modal'])
  await page.locator('#read').tap();await page.locator('[data-talk="juno"]').tap();await state(lambda s:s['conversation']=='juno')
  await page.locator('[data-reply="0"]').tap();await state(lambda s:'give your character' in s['line'])
  await page.screenshot(path=str(OUT/'06-touch-dialogue.png'),scale='css')
  await page.locator('#dismiss').tap();await state(lambda s:not s['modal'])
  await page.locator('#scenes').tap();assert await page.locator('[data-scene]').count()==18
  await page.locator('[data-scene="s2_record"]').tap();await state(lambda s:s['scene']=='s2_record')
  await page.locator('#next').tap();await state(lambda s:s['clue']=='ticket')
  assert 'TOMORROW 14:32' in await page.locator('#sheet-content').inner_text()
  await page.screenshot(path=str(OUT/'07-tomorrow-ticket.png'),scale='css')
  await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(OUT/'08-portrait-reading.png'),scale='css')
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.locator('#dismiss').tap();await state(lambda s:not s['modal'])
  stopped=(await state())['party'][0]['x'];await page.wait_for_timeout(800);assert abs((await state())['party'][0]['x']-stopped)<1
  assert not errors,errors
  assert all(u.startswith(URL) or u.startswith('data:') or u.startswith('blob:') for u in requests),requests
  result={'device':'iPhone 13 size/touch emulation in Chromium; not physical Safari','portrait':[390,844],'landscape':[844,390],'game_loaded':True,'touch_walk_depth_use_zoom':True,'dialogue_reply':True,'scene_picker_count':18,'readable_clue_and_orientation':True,'stuck_movement':False,'browser_errors':errors,'external_requests':False}
  (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True);await browser.close()

if __name__=='__main__':asyncio.run(run())
