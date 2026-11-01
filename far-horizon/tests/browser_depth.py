"""Browser-rendered 3D slice: real routes, articulated people and item inspection."""
import asyncio,json,os,math
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/depth'
URL=os.environ.get('FH_URL','http://127.0.0.1:8090')+'/?preview=depth'

async def run():
 OUT.mkdir(parents=True,exist_ok=True)
 errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  context=await browser.new_context(viewport={'width':1366,'height':768})
  page=await context.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  await page.goto(URL)
  await page.wait_for_function('window.farHorizonDepthTest',timeout=90000)
  async def snap():return await page.evaluate('window.farHorizonDepthTest')
  async def wait(test):await page.wait_for_function('window.farHorizonDepthTest&&('+test+')',timeout=60000)
  async def screenshot(name):await page.screenshot(path=str(OUT/(name+'.png')))
  async def walk(x):
   old=(await snap())['x'];key='d'if x>old else'a'
   await page.keyboard.down(key)
   await wait('window.farHorizonDepthTest.x'+('>'if x>old else'<')+str(x))
   await page.keyboard.up(key);await page.wait_for_timeout(300)
  assert (await snap())['rigged']
  await screenshot('10-refined-start')
  await walk(8.2)
  await page.keyboard.press('e');await wait('window.farHorizonDepthTest.talking==="juno"')
  await page.mouse.click(330,605);await wait('window.farHorizonDepthTest.line.includes("give your character")')
  await screenshot('11-juno-dialogue');await page.keyboard.press('Escape')
  await walk(6.18)
  await page.keyboard.press('e');await wait('window.farHorizonDepthTest.upper&&!window.farHorizonDepthTest.branch_pending')
  await page.keyboard.down('d');await wait('window.farHorizonDepthTest.x>8.35')
  ramp=await snap();assert .35<ramp['party'][0]['y']<.9 and ramp['party'][0]['z']<-.8
  phases=[round(a['animation_time'],2) for a in ramp['party']]
  assert len(set(phases))>2,phases
  await screenshot('12-stairs-and-depth')
  await wait('window.farHorizonDepthTest.x>12.0');await page.keyboard.up('d');await page.wait_for_timeout(280)
  top=await snap();assert top['party'][0]['y']>1 and top['party'][0]['z']< -1.7
  await screenshot('13-upper-gallery')
  await page.keyboard.press('e');await wait('window.farHorizonDepthTest.inspecting')
  await page.wait_for_timeout(250);turn=await snap()
  await screenshot('14-turn-and-reach')
  await wait('window.farHorizonDepthTest.camera_size<1.70&&window.farHorizonDepthTest.inspection_time>1.8')
  zoom=await snap();assert abs(math.atan2(math.sin(zoom['yaw']-math.pi),math.cos(zoom['yaw']-math.pi)))<.08,zoom
  await screenshot('15-device-closeup')
  x=zoom['x'];await page.keyboard.down('d');await page.wait_for_timeout(500);await page.keyboard.up('d');assert abs((await snap())['x']-x)<.01
  await page.keyboard.press('Escape');await wait('window.farHorizonDepthTest.camera_size>5.85')
  await screenshot('16-return-to-world')
  await walk(14.4);await page.keyboard.press('e');await wait('window.farHorizonDepthTest.talking==="venn"')
  await page.mouse.click(330,605);await wait('window.farHorizonDepthTest.line.includes("humanity should never")')
  await screenshot('17-venn-dialogue');await page.keyboard.press('Escape')
  await walk(16.7);await page.keyboard.press('e');await wait('window.farHorizonDepthTest.room==="launch"')
  await page.wait_for_timeout(1000);await screenshot('18-second-area')
  await walk(12.0);await page.keyboard.press('e');await wait('window.farHorizonDepthTest.inspecting&&window.farHorizonDepthTest.camera_size<1.7')
  await screenshot('19-second-device');await page.keyboard.press('Escape');await wait('window.farHorizonDepthTest.camera_size>5.85')
  await page.keyboard.press('Space');held=await snap();await page.wait_for_timeout(700);assert (await snap())['clock']==held['clock']
  await page.keyboard.press('Space')
  assert errors==[],errors
  result={'two_playable_areas':True,'true_skeletal_3d':True,'vertical_and_depth_route':ramp['party'][0],'independent_gait_phases':phases,'turn_yaw_radians':zoom['yaw'],'closeup_camera_size':zoom['camera_size'],'dialogue_selection':'passed','movement_lock_and_escape':'passed','browser_errors':errors,'software_renderer_fps':zoom['fps']}
  (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
  await context.close();await browser.close()

if __name__=='__main__':asyncio.run(run())
