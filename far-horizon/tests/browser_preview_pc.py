"""PC launcher/frame/keyboard/GM-window smoke check of the shared preview URL."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/far-horizon-tests/preview-pc';URL=os.environ.get('FH_PREVIEW_URL','http://127.0.0.1:8092')
async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  ctx=await browser.new_context(viewport={'width':1366,'height':800})
  await ctx.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__observedPreview=e.data.state;});")
  page=await ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  await page.goto(URL+'/play.html');await page.locator('#begin').click()
  async def state(check=lambda s:True):
   for _ in range(600):
    s=await page.evaluate('window.__observedPreview')
    if s and check(s):return s
    await page.wait_for_timeout(100)
   raise AssertionError('No expected state')
  first=await state();assert not first['phone_view']
  await page.screenshot(path=str(OUT/'01-pc-preview.png'))
  await page.keyboard.down('d');await state(lambda s:s['party'][0]['x']>first['party'][0]['x']+60);await page.keyboard.up('d')
  async with page.expect_popup() as pop:await page.locator('#desk').click()
  gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
  assert await gm.locator('[data-scene]').count()==18
  await gm.locator('[data-scene="s3_observation"]').click();await state(lambda s:s['scene']=='s3_observation')
  await page.locator('#read').click();assert await page.locator('#sheet').is_visible()
  await page.screenshot(path=str(OUT/'02-pc-reading.png'))
  await page.locator('#dismiss').click()
  assert not errors,errors
  result={'desktop_preview':True,'keyboard_movement':True,'gm_popup_and_scene_jump':True,'read_panel':True,'browser_errors':errors}
  (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);await browser.close()
if __name__=='__main__':asyncio.run(run())
