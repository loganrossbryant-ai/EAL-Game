"""Exercise distinct routes, articulated scene motion and PPT dialogue headers.

Real stage keys and the public GM desk drive the game. The debug snapshot is
read only. A coarse pointer uses the shipping mobile world rendering profile.
"""
import asyncio,io,json,math,os
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/far-horizon-tests/detail-rooms'
URL=os.environ.get('FH_DETAIL_URL','http://127.0.0.1:8093')
ARGS=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling','--disable-backgrounding-occluded-windows']

async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[];captures=[];motion={};routes={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=ARGS)
  ctx=await browser.new_context(viewport={'width':1366,'height':768},has_touch=True)
  page=await ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  try:
   await page.goto(URL);await page.wait_for_function('window.farHorizonTestState',timeout=120000,polling=100)
   async def state():return await page.evaluate('window.farHorizonTestState')
   async def wait(test):await page.wait_for_function('window.farHorizonTestState&&('+test+')',timeout=180000,polling=100)
   async def capture(name):
    await page.screenshot(path=str(OUT/(name+'.png')));captures.append(name);print(name,flush=True)
   async with page.expect_popup() as pop:await page.keyboard.press('g')
   gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
   async def close():
    await gm.locator('[data-action="close"]').click();await wait('!window.farHorizonTestState.modal')
    await page.bring_to_front();await page.locator('#canvas').focus()
   async def jump(id):
    await gm.locator('[data-scene="'+id+'"]').click();await wait('window.farHorizonTestState.scene==='+json.dumps(id));await close()
   async def walk(x):
    await page.bring_to_front();await page.locator('#canvas').focus()
    s=await state();old=s['party'][s['leader']]['x'];key='d' if x>old else 'a'
    await page.keyboard.down(key)
    try:await wait('window.farHorizonTestState.party[window.farHorizonTestState.leader].x'+('>' if x>old else '<')+str(x))
    finally:await page.keyboard.up(key)
    await wait('window.farHorizonTestState.party.every(m=>Math.abs(m.vx)<1)')
   async def use_route(upper):
    await page.keyboard.press('e');await wait('window.farHorizonTestState.upper_route==='+str(upper).lower()+'&&!window.farHorizonTestState.branch_pending&&!window.farHorizonTestState.route_transition')
   # Entirely flat rooms cannot accidentally inherit a gallery from another room.
   for id in ['s1_boarding','s1_launch','s2_recreation']:
    await jump(id);s=await state();assert s['layout_kind']=='flat' and not s['upper_route'];routes[id]='flat'
    await capture(id+'-flat')
   # Central mezzanine has a second descending exit at the other end.
   await jump('s1_habitation');await walk(610);await use_route(True);await walk(990)
   s=await state();assert abs(s['avatars'][0]['y']-.68)<.02 and s['avatars'][0]['z']<-1.4,s['avatars']
   await capture('habitation-central-mezzanine');await walk(1760)
   await wait('Math.abs(window.farHorizonTestState.avatars[0].y)<.01');routes['habitation']='central mezzanine with descending far exit'
   # Curved bridge route travels into depth without climbing.
   await jump('s1_observation');await walk(550);await use_route(True);await walk(1300)
   s=await state();assert abs(s['avatars'][0]['y'])<.01 and s['avatars'][0]['z']<-1.5,s['avatars']
   await capture('bridge-curved-level-aisle');routes['bridge']='zero-rise curved depth aisle'
   # The security lift boards all four representatives, then returns them safely.
   await jump('s2_restricted');await walk(1110);await use_route(True)
   s=await state();assert all(abs(a['y']-1.25)<.01 for a in s['avatars']),s['avatars']
   assert all(6.4<a['x']<9.25 for a in s['avatars']),s['avatars']
   await capture('restricted-lift-upper');await walk(450);await page.keyboard.press('e')
   await wait('window.farHorizonTestState.physical_inspection&&window.farHorizonTestState.inspection_time>2')
   await capture('restricted-access-screen');await close()
   # Save and reload must restore the cabin at its corresponding stop.
   await page.wait_for_timeout(2200);await page.reload();await wait('window.farHorizonTestState.scene==="s2_restricted"&&window.farHorizonTestState.upper_route')
   await wait('window.farHorizonTestState.avatars.every(a=>Math.abs(a.y-1.25)<.01)')
   await close();await walk(1115);await use_route(False)
   await wait('window.farHorizonTestState.avatars.every(a=>Math.abs(a.y)<.01)');await capture('restricted-lift-lower')
   routes['restricted']='four-person boarding, lift, screen, upper save restore and descent'
   # K-17 has a short raised instrument plinth with lower paths at both ends.
   await jump('s3_observation');await walk(1350);await use_route(True);await walk(1840)
   s=await state();assert abs(s['avatars'][0]['y']-.45)<.02 and s['avatars'][0]['z']<-1.45,s['avatars']
   await capture('k17-short-instrument-plinth');routes['k17']='short right plinth'
   # Scene motion must change both the relevant assembly and rendered world pixels.
   for id in ['s1_terminal','s1_boarding','s1_launch','s1_habitation','s1_observation','s2_recreation','s2_malfunction','s2_restricted','s3_observation']:
    await jump(id);await gm.locator('[data-cue="0"]').click();await wait('window.farHorizonTestState.cue===0');await close()
    a=await state();before=await page.screenshot(path=str(OUT/(id+'-motion-a.png')))
    await wait('window.farHorizonTestState.stage_clock>'+str(a['stage_clock']+1.1))
    b=await state();after=await page.screenshot(path=str(OUT/(id+'-motion-b.png')))
    changed=any(abs(x['x']-y['x'])>.001 or abs(x['y']-y['y'])>.001 or abs(x['rotation']-y['rotation'])>.002 or abs(x.get('assembly_motion',0)-y.get('assembly_motion',0))>.002 for x,y in zip(a['subjects'],b['subjects']))
    assert changed,(id,a['subjects'],b['subjects'])
    aa=np.asarray(Image.open(io.BytesIO(before)).convert('RGB')).astype(float);bb=np.asarray(Image.open(io.BytesIO(after)).convert('RGB')).astype(float)
    fraction=float((np.abs(aa[330:690]-bb[330:690]).max(axis=2)>8).mean());assert fraction>.0003,(id,fraction)
    motion[id]={'changed_world_pixels':round(fraction,6),'subjects':[v['kind'] for v in b['subjects']]};print('motion',id,flush=True)
   # Every NPC uses an accessible original PPT photo and has unclipped dialogue.
   people={'venn':'s1_terminal','juno':'s2_recreation','iris':'s3_iris','rhee':'s2_malfunction','m77':'s2_malfunction','vale':'s3_council','okafor':'s3_council'}
   campaign=json.loads((ROOT/'far-horizon/data/campaign.json').read_text())
   for who,id in people.items():
    await jump(id);name=campaign['characters'][who]['name'];await gm.get_by_role('button',name='Talk: '+name,exact=True).click()
    await wait('window.farHorizonTestState.conversation==='+json.dumps(who));s=await state();assert not s['layout_issues'],s['layout_issues']
    await capture('dialogue-'+who)
   assert not errors,errors
   result={'render_profile':'shipping coarse-pointer world; full 1366x768 UI','routes':routes,'animated_rooms':motion,'ppt_dialogue_headers':list(people),'browser_errors':errors,'screenshots':captures}
   (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await page.evaluate('window.farHorizonTestState'),indent=2))
   except Exception:pass
   raise
  finally:await browser.close()

if __name__=='__main__':asyncio.run(run())
