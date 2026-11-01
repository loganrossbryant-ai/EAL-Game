"""Record actual input-driven walking and item use for visual animation review."""
import asyncio,json,os,time
from pathlib import Path
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/.cache/fh-playwright'
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/interaction-video'
URL=os.environ.get('FH_URL','http://127.0.0.1:8090')
async def run():
 OUT.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  context=await browser.new_context(viewport={'width':1366,'height':768},record_video_dir=str(OUT),record_video_size={'width':1366,'height':768})
  page=await context.new_page();start=time.monotonic();await page.goto(URL)
  async def wait(expr):await page.wait_for_function('window.farHorizonTestState&&('+expr+')',timeout=90000)
  await wait('window.farHorizonTestState.scene==="s1_terminal"')
  await page.keyboard.down('d');await wait('window.farHorizonTestState.party[0].x>786');await page.keyboard.up('d')
  await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  await page.keyboard.press('e');await wait('window.farHorizonTestState.upper_route&&!window.farHorizonTestState.branch_pending')
  await page.keyboard.down('d');await wait('window.farHorizonTestState.party[0].x>1530');await page.keyboard.up('d')
  await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  use_time=time.monotonic()-start
  await page.keyboard.press('e');await wait('window.farHorizonTestState.physical_inspection&&window.farHorizonTestState.inspection_time>2.2')
  await page.wait_for_timeout(700);await page.keyboard.press('Escape');await wait('window.farHorizonTestState.stage_camera_size>5.9')
  await page.wait_for_timeout(500)
  video=page.video
  await context.close();path=await video.path()
  (OUT/'timing.json').write_text(json.dumps({'video':Path(path).name,'item_use_wall_seconds':use_time},indent=2))
  print(json.dumps({'video':str(path),'item_use_wall_seconds':use_time}),flush=True);await browser.close()
if __name__=='__main__':asyncio.run(run())
