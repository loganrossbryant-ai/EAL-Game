import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
URL=os.environ.get('FH_QUALITY_URL','http://127.0.0.1:8094')
OUT=Path(__file__).resolve().parents[2]/'artifacts/far-horizon-tests/quality';OUT.mkdir(exist_ok=True,parents=True)
async def run():
 errors=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling'])
  c=await b.new_context(viewport={'width':1366,'height':768});await c.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__observedPreview=e.data.state;});")
  page=await c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  async def state(check=lambda s:True):
   for _ in range(1800):
    s=await page.evaluate('window.__observedPreview')
    if s and check(s):return s
    await page.wait_for_timeout(100)
   raise AssertionError(s)
  await page.goto(URL+'/play.html');await page.locator('#begin').click();start=await state();initial=start['world_resolution'];auto=await state(lambda s:s['world_resolution'][0]<initial[0]);assert auto['picture_quality']=='auto'
  for choice,width in [('sharp',1920),('balanced',1366),('smooth',960)]:
   await page.locator('#quality').select_option(choice);await state(lambda s:s['picture_quality']==choice and s['world_resolution'][0]==width)
  await page.locator('#present').click();await state(lambda s:s['presentation']);await page.screenshot(path=str(OUT/'tv-fixed-smooth.png'));box=await page.locator('#stage').bounding_box();assert abs(box['width']-1366)<2 and abs(box['height']-768)<2,box
  await page.mouse.move(1300,22);await page.locator('#present').click();await state(lambda s:not s['presentation']);assert not await page.evaluate('Boolean(document.fullscreenElement)')
  assert not errors,errors
  result={'auto_initial_world':initial,'auto_reduced_world':auto['world_resolution'],'fixed_quality_widths':[1920,1366,960],'ui_display':[1366,768],'fullscreen_exit':True,'browser_errors':errors,'software_rendering_only':True};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));await b.close()
asyncio.run(run())
