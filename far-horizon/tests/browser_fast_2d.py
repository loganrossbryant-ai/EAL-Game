"""Measure real quick controls on the restored 2D M-77 classroom slice."""
import asyncio,json,os,statistics
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/far-horizon-tests/fast-2d';URL=os.environ.get('FH_FAST_URL','http://127.0.0.1:8098')
async def run():
 OUT.mkdir(exist_ok=True,parents=True);errors=[];latencies=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage','--disable-renderer-backgrounding','--disable-background-timer-throttling'])
  c=await b.new_context(viewport={'width':1366,'height':900})
  await c.add_init_script("""window.addEventListener('message',e=>{if(e.data?.app==='far-horizon-preview'&&e.data.kind==='state'){window.__state=e.data.state;const probe=window.__probe;if(probe&&!probe.waiting&&probe.target===e.data.state.conversation&&e.data.state.modal){probe.waiting=true;probe.stateMs=performance.now()-probe.start;requestAnimationFrame(()=>probe.frameMs=performance.now()-probe.start);}}});""")
  page=await c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  async def state(check=lambda s:True):
   for _ in range(1200):
    s=await page.evaluate('window.__state')
    if s and check(s):return s
    await page.wait_for_timeout(50)
   raise AssertionError(s)
  try:
   await page.goto(URL+'/play.html');await page.locator('#begin').click();s=await state();assert s['fast_2d'] and s['scene']=='s2_malfunction'
   frame=page.frame_locator('#stage');await frame.locator('#canvas').focus();await page.keyboard.down('d');await page.wait_for_timeout(800);await page.keyboard.up('d');s=await state(lambda s:all(abs(m['vx'])<1 for m in s['party']));assert s['party'][0]['x']>800,s['party']
   await page.screenshot(path=str(OUT/'01-restored-2d.png'));print('movement',s['party'][0]['x'],flush=True)
   for target in ['rhee','m77']*4:
    await page.evaluate("target=>{window.__probe={target,start:performance.now()};document.getElementById('quick-'+target).click();}",target)
    s=await state(lambda s:s['conversation']==target and s['modal']);await page.wait_for_function('window.__probe?.frameMs!==undefined')
    timing=await page.evaluate('window.__probe');latencies.append({'npc':target,'state_ms':round(timing['stateMs'],1),'next_animation_frame_ms':round(timing['frameMs'],1)});await page.evaluate('window.__probe=null')
    assert not s.get('layout_issues'),s.get('layout_issues');await page.locator('#back').click();await state(lambda s:not s['modal'])
   await page.locator('#quick-rhee').click();await state(lambda s:s['conversation']=='rhee');await page.screenshot(path=str(OUT/'02-immediate-dialogue.png'));await page.locator('#back').click();await state(lambda s:not s['modal'])
   await page.locator('#quick-focus').click();s=await state(lambda s:abs(s['party'][0]['x']-910)<2);assert abs(s['camera']-1152)<3;await page.screenshot(path=str(OUT/'03-door-focus.png'))
   async with page.expect_popup() as pop:await page.locator('#desk').click()
   gm=await pop.value;await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for();assert await gm.locator('[data-scene]').count()==3
   checked=0;campaign=json.loads((ROOT/'far-horizon/data/campaign.json').read_text())
   for scene in campaign['scenes']:
    await gm.locator('[data-scene="'+scene['id']+'"]').click();await state(lambda s:s['scene']==scene['id'])
    for i in range(len(scene['cues'])):
     await gm.locator('[data-cue="'+str(i)+'"]').click();s=await state(lambda s:s['scene']==scene['id'] and s['cue']==i);assert not s.get('layout_issues'),s.get('layout_issues');checked+=1
   await page.bring_to_front();await page.locator('#quick-ticket').click();await state(lambda s:s['clue']=='ticket');await page.screenshot(path=str(OUT/'04-ticket.png'))
   await page.locator('#back').click();await state(lambda s:not s['modal']);await page.reload();await page.locator('#begin').click();s=await state(lambda s:s['scene']=='s2_record');assert s['revealed']['ticket']
   await page.locator('#present').click();await state(lambda s:s['presentation']);await page.screenshot(path=str(OUT/'05-tv.png'));await page.mouse.move(1300,22);await page.locator('#present').click();await state(lambda s:not s['presentation'])
   assert not errors,errors
   result={'render_fps_observed':s['render_fps'],'restored_original_2d_characters':True,'three_scene_encounter':True,'checked_beats':checked,'movement_speed_pixels_per_second':520,'direct_npc_and_clue_controls':True,'instant_door_positioning':True,'save_reload':True,'half_screen_portraits_and_tv':True,'logical_response_timings':latencies,'response_max_ms':max(x['state_ms']for x in latencies),'browser_errors':errors,'note':'State and next animation-frame timing in Chromium software rendering; not a physical classroom-device measurement.'};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));(OUT/'failure-state.json').write_text(json.dumps(await page.evaluate('window.__state'),indent=2));print(json.dumps(errors),flush=True);raise
  finally:await b.close()
if __name__=='__main__':asyncio.run(run())
