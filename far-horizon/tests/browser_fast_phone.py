import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/far-horizon-tests/fast-phone';URL=os.environ.get('FH_FAST_URL','http://127.0.0.1:8099')
async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage']);device=dict(p.devices['iPhone 13']);device.pop('default_browser_type',None);c=await b.new_context(**device);await c.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__state=e.data.state;});")
  page=await c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  async def state(check=lambda s:True):
   for _ in range(1200):
    s=await page.evaluate('window.__state')
    if s and check(s):return s
    await page.wait_for_timeout(50)
   raise AssertionError(s)
  await page.goto(URL+'/play.html');await page.set_viewport_size({'width':844,'height':390});await page.locator('#begin').tap();s=await state();assert s['phone_view'] and s['fast_2d']
  await page.locator('#quick-rhee').tap();await state(lambda s:s['conversation']=='rhee');await page.locator('dialog.dialogue-card').wait_for();im=await page.locator('.dialogue-image').bounding_box();card=await page.locator('#sheet').bounding_box();assert abs(im['width']/card['width']-.5)<.03;await page.screenshot(path=str(OUT/'01-half-screen.png'),scale='css');await page.locator('#dismiss').tap();await state(lambda s:not s['modal'])
  cdp=await c.new_cdp_session(page);box=await page.locator('#right').bounding_box();x0=(await state())['party'][0]['x'];await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box['x']+box['width']/2,'y':box['y']+box['height']/2,'id':1}]});await page.wait_for_timeout(700);await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});s=await state(lambda s:all(abs(m['vx'])<1 for m in s['party']));assert s['party'][0]['x']>x0+200
  await page.locator('#quick-ticket').tap();await state(lambda s:s['clue']=='ticket');await page.locator('#sheet').wait_for();assert 'TOMORROW 14:32'in await page.locator('#sheet-content').inner_text();await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(OUT/'02-ticket-portrait.png'),scale='css');assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');await page.locator('#dismiss').tap();await state(lambda s:not s['modal']);assert not errors,errors
  result={'phone_size_touch_emulation':True,'original_half_screen_portrait':True,'fast_touch_movement':True,'ticket_portrait_orientation':True,'browser_errors':errors,'physical_safari_test':False};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));await b.close()
asyncio.run(run())
