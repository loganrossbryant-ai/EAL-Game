"""Real PC controls check a full-display TV view and half-screen portraits."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/far-horizon-tests/tv-slice';URL=os.environ.get('FH_TV_URL','http://127.0.0.1:8097')
async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling','--disable-backgrounding-occluded-windows'])
  ctx=await browser.new_context(viewport={'width':1920,'height':1080})
  await ctx.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__observedPreview=e.data.state;});")
  page=await ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  try:
   await page.goto(URL+'/play.html')
   await page.evaluate("localStorage.setItem('far-horizon-gm-v2',JSON.stringify({version:2,sentinel:'saved classroom progress'}))")
   await page.locator('#begin').click()
   async def state(check=lambda s:True):
    for _ in range(1200):
     s=await page.evaluate('window.__observedPreview')
     if s and check(s):return s
     await page.wait_for_timeout(100)
    raise AssertionError('Expected state unavailable: '+json.dumps(s))
   first=await state();assert first['scene']=='s1_terminal'
   await page.locator('#quality').select_option('smooth');await state(lambda s:s['picture_quality']=='smooth')
   await page.locator('#present').click();await state(lambda s:s['presentation'])
   box=await page.locator('#stage').bounding_box();viewport=page.viewport_size
   assert box['width']>=viewport['width']*.97 and box['height']>=viewport['height']*.97,(box,viewport)
   await page.screenshot(path=str(OUT/'01-tv-full-frame.png'))
   frame=page.frame_locator('#stage');await frame.locator('#canvas').focus()
   async with page.expect_popup() as pop:await page.keyboard.press('g')
   gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
   await gm.get_by_role('button',name='Talk: Captain Mara Venn',exact=True).click();s=await state(lambda s:s['conversation']=='venn')
   assert s['world_covered'];assert len(s['projected_line'])<len(s['line'])
   assert 'Asteria' in await gm.locator('#full-script').inner_text()
   await page.bring_to_front();await page.screenshot(path=str(OUT/'02-venn-half-screen.png'))
   await page.locator('#read').click();await page.locator('dialog.dialogue-card').wait_for()
   image_box=await page.locator('.dialogue-image').bounding_box();dialog_box=await page.locator('#sheet').bounding_box();assert abs(image_box['width']/dialog_box['width']-.5)<.03
   await page.screenshot(path=str(OUT/'03-html-half-screen-portrait.png'))
   await page.locator('#dismiss').click();await state(lambda s:not s['modal'])
   await gm.locator('[data-scene="s1_observation"]').click();await state(lambda s:s['scene']=='s1_observation')
   await gm.locator('[data-action="close"]').click();await state(lambda s:not s['modal'])
   await page.bring_to_front();await frame.locator('#canvas').focus()
   await page.keyboard.down('d');await state(lambda s:s['party'][0]['x']>1650);await page.keyboard.up('d');await state(lambda s:all(abs(m['vx'])<1 for m in s['party']))
   await page.screenshot(path=str(OUT/'04-iris-clear-sightline.png'))
   await gm.locator('[data-scene="s2_malfunction"]').click();await state(lambda s:s['scene']=='s2_malfunction')
   await gm.get_by_role('button',name='Talk: Maintenance unit M-77',exact=True).click();await state(lambda s:s['conversation']=='m77')
   await page.bring_to_front();await page.screenshot(path=str(OUT/'05-enemy-half-screen.png'))
   assert await page.evaluate("JSON.parse(localStorage.getItem('far-horizon-gm-v2')).sentinel")=='saved classroom progress'
   assert await page.evaluate("localStorage.getItem('far-horizon-gm-performance-v3')!==null")
   assert not errors,errors
   result={'viewport':viewport,'tv_frame':box,'half_screen_html_portrait_fraction':image_box['width']/dialog_box['width'],'tv_mode':True,'full_original_script_on_gm_desk':True,'full_dialogue_covers_world':True,'saved_classroom_progress_untouched':True,'two_scenes_and_enemy_portrait':True,'browser_errors':errors}
   (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await page.evaluate('window.__observedPreview'),indent=2))
   except Exception:pass
   raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(run())
