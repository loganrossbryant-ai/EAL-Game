"""Visually inspect the terminal and flat lounge through real game controls."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/detail-slice'
URL=os.environ.get('FH_DETAIL_URL','http://127.0.0.1:8093')

async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling','--disable-backgrounding-occluded-windows'])
  ctx=await browser.new_context(viewport={'width':1366,'height':768},has_touch=True)
  page=await ctx.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  await page.goto(URL)
  await page.wait_for_function('window.farHorizonTestState',timeout=120000)
  async def state():return await page.evaluate('window.farHorizonTestState')
  async def wait(test):
   print('WAIT',test,flush=True)
   await page.wait_for_function('window.farHorizonTestState&&('+test+')',timeout=120000,polling=100)
   print('STATE',json.dumps({k:v for k,v in (await state()).items() if k in ['scene','nearest','branch_pending','upper_route','modal','layout_kind','render_fps','draw_calls']}),flush=True)
  async def capture(name):
   await page.screenshot(path=str(OUT/(name+'.png')));print(name,flush=True)
  async def walk(x):
   await page.bring_to_front();await page.locator('#canvas').focus()
   print('WALK',x,flush=True)
   s=await state();old=s['party'][s['leader']]['x'];key='d' if x>old else 'a'
   await page.keyboard.down(key)
   await wait('window.farHorizonTestState.party[window.farHorizonTestState.leader].x'+('>' if x>old else '<')+str(x))
   await page.keyboard.up(key)
   await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  await capture('01-terminal-start')
  async with page.expect_popup() as pop:await page.keyboard.press('g')
  gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
  print('CLOSE MODAL',flush=True)
  await gm.locator('[data-action="close"]').click()
  await page.bring_to_front();await page.locator('#canvas').focus()
  await walk(835);await page.keyboard.press('e')
  await wait('window.farHorizonTestState.upper_route&&!window.farHorizonTestState.branch_pending')
  await walk(390);await capture('02-left-observation-balcony')
  await page.keyboard.press('e');await wait('window.farHorizonTestState.conversation==="venn"')
  await page.wait_for_timeout(1100);await capture('03-venn-ppt-portrait')
  await gm.locator('[data-scene="s2_recreation"]').click();await wait('window.farHorizonTestState.scene==="s2_recreation"')
  print('CLOSE MODAL',flush=True)
  await gm.locator('[data-action="close"]').click()
  await page.bring_to_front();await page.locator('#canvas').focus()
  await walk(1115);await capture('05-flat-recreation')
  await gm.get_by_role('button',name='Talk: Juno Reyes',exact=True).click()
  await wait('window.farHorizonTestState.conversation==="juno"')
  await page.wait_for_timeout(1300);await capture('06-juno-ppt-portrait')
  assert (await state())['layout_kind']=='flat'
  result={'two_scenes':True,'render_profile':'coarse-pointer world with full-size UI','terminal_route':'left observation balcony','lounge':'flat, no second level','original_ppt_portraits':['venn','juno'],'browser_errors':errors,'final_state':await state()}
  (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
  print(json.dumps({'two_scenes':True,'browser_errors':errors}),flush=True)
  assert not errors,errors
  await browser.close()

if __name__=='__main__':asyncio.run(run())
