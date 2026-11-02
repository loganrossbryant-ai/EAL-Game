"""Exercise the projected aid through its real stage and private GM controls.

Captures both ends of every room, all 18 scenes, 13 large clue cards and every
available NPC reply. State is observed only; no game-state setters are used.
"""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/projection-review'
FOCUSED=os.environ.get('FH_PROJECTION_FOCUSED')=='1'
URL=os.environ.get('FH_PROJECTION_URL','http://127.0.0.1:8097')
ARGS=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling','--disable-backgrounding-occluded-windows']
async def run():
 OUT.mkdir(parents=True,exist_ok=True);errors=[];rooms=set();scene_checks=[];clue_checks=[];dialogue_checks=[]
 campaign=json.loads((ROOT/'far-horizon/data/campaign.json').read_text())
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=ARGS)
  ctx=await browser.new_context(viewport={'width':1366,'height':768})
  await ctx.add_init_script("window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state')window.__observedPreview=e.data.state;});")
  page=await ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  async def state(check=lambda s:True):
   for _ in range(1600):
    s=await page.evaluate('window.__observedPreview')
    if s and check(s):return s
    await page.wait_for_timeout(100)
   raise AssertionError('Expected state unavailable: '+json.dumps(s))
  async def capture(name):
   await page.bring_to_front();await page.wait_for_timeout(450);await page.screenshot(path=str(OUT/(name+'.png')))
  try:
   await page.goto(URL+'/play.html');await page.locator('#begin').click();await state()
   await page.locator('#quality').select_option('balanced');await state(lambda s:s['world_resolution'][0]==1366)
   await page.locator('#present').click();await state(lambda s:s['presentation'])
   frame=page.frame_locator('#stage');await frame.locator('#canvas').focus()
   async with page.expect_popup() as pop:await page.keyboard.press('g')
   gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
   async def close():
    await gm.locator('[data-action="close"]').click();await state(lambda s:not s['modal'])
   async def jump(id):
    await gm.locator('[data-scene="'+id+'"]').click();await state(lambda s:s['scene']==id)
    await gm.locator('[data-cue="0"]').click();await state(lambda s:s['cue']==0);await close()
   for scene in campaign['scenes']:
    id=scene['id']
    if FOCUSED and id not in ['s1_launch','s1_habitation','s1_observation','s3_observation']:continue
    await jump(id);await capture(id+'-west')
    s=await state();assert not s['layout_issues'],(id,s['layout_issues'])
    scene_checks.append({'id':id,'layout':s['layout'],'draw_calls':s.get('draw_calls'),'fps':s['render_fps']})
    if s['layout'] not in rooms:
     rooms.add(s['layout']);await page.bring_to_front();await frame.locator('#canvas').focus()
     await page.keyboard.down('d')
     try:await state(lambda s:s['party'][s['leader']]['x']>1690)
     finally:await page.keyboard.up('d')
     await state(lambda s:all(abs(m['vx'])<1 for m in s['party']));await capture(id+'-east')
    print('scene',id,flush=True)
   for id in campaign['clues']:
    await gm.locator('[data-clue="'+id+'"]').click();await gm.get_by_role('button',name='Reveal on stage',exact=True).click()
    await state(lambda s:s['clue']==id);await page.wait_for_timeout(350);s=await state();assert not s['layout_issues'],(id,s['layout_issues'])
    await capture('clue-'+id);clue_checks.append(id);await close();print('clue',id,flush=True)
   for session,scene_id in [(1,'s1_habitation'),(2,'s2_recreation'),(3,'s3_council')]:
    await jump(scene_id)
    for who,person in campaign['characters'].items():
     npc_scene=next((scene['id'] for scene in campaign['scenes'] if scene['session']==session and who in scene['npcs']),None)
     if not npc_scene:continue
     await jump(npc_scene)
     await gm.get_by_role('button',name='Talk: '+person['name'],exact=True).click()
     await state(lambda s:s['conversation']==who);await page.wait_for_timeout(300);s=await state();assert not s['layout_issues'],(session,who,s['layout_issues'])
     await capture('dialogue-'+who+'-s'+str(session))
     options=[r for r in person['replies'] if r.get('min_session',1)<=session<=r.get('max_session',3)]
     for index,option in enumerate(options[:4]):
      await page.bring_to_front();await frame.locator('#canvas').focus();await page.mouse.click(1015,482+index*55)
      await state(lambda s:s['line']==option['text']);await page.wait_for_timeout(220);s=await state();assert not s['layout_issues'],(session,who,index,s['layout_issues'])
      dialogue_checks.append({'session':session,'npc':who,'reply':index,'caption_chars':len(s['projected_line'])})
     await close()
   await page.bring_to_front();await page.mouse.move(1300,22);await page.locator('#present').click();await state(lambda s:not s['presentation'])
   assert not await page.evaluate('Boolean(document.fullscreenElement)')
   assert not errors,errors
   result={'focused_followup':FOCUSED,'scenes':scene_checks,'room_profiles':sorted(rooms),'large_clues':clue_checks,'dialogue_replies':dialogue_checks,'fullscreen_exit':True,'browser_errors':errors,'render_note':'Software WebGL diagnostic only; not the teacher PC frame rate.'}
   (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'scenes':len(scene_checks),'rooms':len(rooms),'clues':len(clue_checks),'replies':len(dialogue_checks),'browser_errors':errors}),flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   (OUT/'failure-state.json').write_text(json.dumps(await page.evaluate('window.__observedPreview'),indent=2));raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(run())
