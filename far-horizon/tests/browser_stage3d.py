"""Inspect the integrated GM game's rendered 3D paths, poses and devices.
Actions use real keys and the GM desk; snapshots only observe the running game.
"""
import asyncio,json,math,os,io
import numpy as np
from PIL import Image
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/stage3d'
URL=os.environ.get('FH_URL','http://127.0.0.1:8090')

async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  ctx=await browser.new_context(viewport={'width':1366,'height':768})
  page=await ctx.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  await page.goto(URL)
  await page.wait_for_function('window.farHorizonTestState',timeout=90000)
  async def snap():return await page.evaluate('window.farHorizonTestState')
  async def wait(condition):await page.wait_for_function('window.farHorizonTestState&&('+condition+')',timeout=90000)
  async def capture(name):await page.screenshot(path=str(OUT/(name+'.png')))
  async def walk(x):
   s=await snap();old=s['party'][s['leader']]['x'];key='d' if x>old else 'a'
   await page.keyboard.down(key)
   await wait('window.farHorizonTestState.party[window.farHorizonTestState.leader].x'+('>' if x>old else '<')+str(x))
   await page.keyboard.up(key)
   await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  await capture('01-start')
  await page.keyboard.down('d');await wait('window.farHorizonTestState.party[0].vx>120')
  samples=[]
  for _ in range(12):
   samples.append(await snap());await page.wait_for_timeout(70)
  await page.keyboard.up('d')
  hips=[s['avatars'][0]['hip_height'] for s in samples]
  hip_range=max(hips)-min(hips);assert min(hips)>0 and hip_range<.012,hips
  await walk(786);await page.keyboard.press('e')
  await wait('window.farHorizonTestState.upper_route&&!window.farHorizonTestState.branch_pending')
  await page.keyboard.down('d');await wait('window.farHorizonTestState.party[0].x>1080')
  ramp=await snap();assert .5<ramp['avatars'][0]['y']<.8 and ramp['avatars'][0]['z']<-.8,ramp['avatars']
  phases=[round(a['time'],2) for a in ramp['avatars']];assert len(set(phases))>2,phases
  await capture('02-raised-route')
  await wait('window.farHorizonTestState.party[0].x>1530');await page.keyboard.up('d')
  await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  await page.keyboard.press('e');await wait('window.farHorizonTestState.physical_inspection')
  await wait('window.farHorizonTestState.inspection_time>.36')
  turn=await snap();await capture('03-turn-and-reach')
  await wait('window.farHorizonTestState.stage_camera_size<1.7&&window.farHorizonTestState.inspection_time>2')
  zoom=await snap();assert abs(math.atan2(math.sin(zoom['avatars'][0]['yaw']-math.pi),math.cos(zoom['avatars'][0]['yaw']-math.pi)))<.07
  assert zoom['avatars'][0]['animation']=='Use'
  await capture('04-item-closeup')
  x=zoom['party'][0]['x'];await page.keyboard.down('d');await page.wait_for_timeout(600);await page.keyboard.up('d');assert abs((await snap())['party'][0]['x']-x)<.1
  await page.keyboard.press('Escape');await wait('window.farHorizonTestState.stage_camera_size>5.85')
  await capture('05-return-camera')
  # Reverse with followers still on the raised walkway: none may drop vertically.
  await page.keyboard.down('a');await wait('window.farHorizonTestState.party[0].x<800');await page.keyboard.up('a')
  await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
  before=await snap();await page.keyboard.press('e');await wait('!window.farHorizonTestState.upper_route&&!window.farHorizonTestState.branch_pending')
  after=await snap()
  for old,new in zip(before['avatars'][1:],after['avatars'][1:]):
   assert abs(old['y']-new['y'])<.2,(old,new)
  await walk(690);await wait('window.farHorizonTestState.avatars.every(m=>Math.abs(m.y)<.001)')
  await capture('06-lower-return')
  async with page.expect_popup() as pop:await page.keyboard.press('g')
  gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
  await gm.locator('[data-scene="s1_boarding"]').click();await wait('window.farHorizonTestState.scene==="s1_boarding"')
  await walk(2200);await page.keyboard.press('e');await wait('window.farHorizonTestState.scene==="s1_launch"')
  await capture('07-second-setting')
  await gm.locator('[data-cue="3"]').click();await wait('window.farHorizonTestState.effect==="float"')
  await capture('08-engine-cutoff')
  await gm.locator('[data-scene="s2_malfunction"]').click();await wait('window.farHorizonTestState.scene==="s2_malfunction"')
  await capture('09-articulated-m77')
  await gm.locator('[data-action="freeze"]').click();await wait('window.farHorizonTestState.paused')
  held=await snap();await page.wait_for_timeout(700);assert (await snap())['stage_clock']==held['stage_clock']
  await gm.locator('[data-action="freeze"]').click()
  motion={}
  for scene in ['s1_terminal','s1_launch','s1_habitation','s1_observation','s2_recreation','s2_malfunction','s2_restricted','s3_observation']:
   await gm.locator('[data-scene="'+scene+'"]').click();await wait('window.farHorizonTestState.scene==='+json.dumps(scene))
   await gm.locator('[data-cue="0"]').click();await wait('window.farHorizonTestState.cue===0')
   await gm.locator('[data-action="close"]').click()
   a=await snap();before=await page.screenshot(path=str(OUT/(scene+'-motion-a.png')))
   await wait('window.farHorizonTestState.stage_clock>'+str(a['stage_clock']+.8))
   b=await snap();after=await page.screenshot(path=str(OUT/(scene+'-motion-b.png')))
   assert any(abs(x['x']-y['x'])>.001 or abs(x['y']-y['y'])>.001 or abs(x['rotation']-y['rotation'])>.002 for x,y in zip(a['subjects'],b['subjects'])),scene
   aa=np.asarray(Image.open(io.BytesIO(before)).convert('RGB')).astype(float);bb=np.asarray(Image.open(io.BytesIO(after)).convert('RGB')).astype(float)
   fraction=float((np.abs(aa[330:650,750:1325]-bb[330:650,750:1325]).max(axis=2)>8).mean())
   assert fraction>.0006,(scene,fraction)
   motion[scene]=round(fraction,5)
  assert not errors,errors
  result={'default_gm_game':True,'two_connected_settings':True,'depth_route':ramp['avatars'][0],'independent_walk_phases':phases,'skeletal_hip_peak_to_peak_m':round(hip_range,6),'turn_animation':turn['avatars'][0],'terminal_closeup':zoom['stage_camera_size'],'back_facing_yaw':zoom['avatars'][0]['yaw'],'movement_lock_return_camera_followers':'passed','hold_picture':'passed','eight_room_motion':motion,'browser_errors':errors,'software_renderer_fps':zoom['render_fps']}
  (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
  await browser.close()

if __name__=='__main__':asyncio.run(run())
