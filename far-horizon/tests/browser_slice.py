"""Black-box Godot browser test: real keyboard/mouse input, read-only snapshots."""
import asyncio,json,os,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests'
async def run():
 OUT.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1366,'height':768})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' and not '404' in m.text else None)
  await page.goto(os.environ.get('FH_URL','http://127.0.0.1:8070'))
  await page.wait_for_function('window.farHorizonTestState',timeout=90000)
  async def snap():return await page.evaluate('window.farHorizonTestState')
  async def wait(js):
   try:await page.wait_for_function('window.farHorizonTestState && ('+js+')',timeout=30000)
   except Exception:
    await page.screenshot(path=str(OUT/'failure.png'))
    print(json.dumps({'failed_wait':js,'snapshot':await snap(),'errors':errors}),flush=True)
    raise
  async def key(value):await page.keyboard.press(value);await page.wait_for_timeout(330)
  async def click(x,y):await page.mouse.click(x,y);await page.wait_for_timeout(350)
  async def walk(x):
   s=await snap();i=int(s['leader']);start=s['party'][i]['x'];direction='d' if x>start else 'a'
   await page.keyboard.down(direction)
   await wait(f'window.farHorizonTestState.party[{i}].x {">" if x>start else "<"} {x}')
   await page.keyboard.up(direction)
   await page.wait_for_timeout(400)
  await click(245,348)
  await page.screenshot(path=str(OUT/'03-terminal-play.png'))
  await walk(690)
  s=await snap();assert s['party'][3]['x']>270 and abs(s['party'][0]['y']-686)<2
  await key('e');await wait('window.farHorizonTestState.modal')
  await page.screenshot(path=str(OUT/'04-briefing-fixed.png'))
  await key('Escape')
  await key('l')
  await click(600,635) # Reject empty record.
  await wait('Object.keys(window.farHorizonTestState.records).length===0')
  records={'reason':'I leave because I want to help build a second home.','want':'I want to prove I can lead.','need':'I need to learn to listen to my crew.','fear':'I fear losing my family stories.','object':'I brought a blue stone because it reminds me of the sea.'}
  async def write(text):
   await page.keyboard.press('Control+a')
   await page.evaluate('''text=>{const target=document.activeElement===document.body?document.querySelector('#canvas'):document.activeElement;for(const key of text){const code=/[a-z]/i.test(key)?'Key'+key.toUpperCase():key===' '?'Space':key==='.'?'Period':'';const opts={key,code,shiftKey:/[A-Z]/.test(key),bubbles:true,cancelable:true};target.dispatchEvent(new KeyboardEvent('keydown',opts));target.dispatchEvent(new KeyboardEvent('keyup',opts));}}''',text)
  for i,(field,text) in enumerate(records.items()):
   await click(690,243+i*73)
   await write(text)
   await page.wait_for_function('([field,text])=>window.farHorizonTestState.editors[field]===text',arg=[field,text],timeout=15000)
  await click(600,635)
  await wait('!!window.farHorizonTestState.records["Orion Kade"]')
  await page.screenshot(path=str(OUT/'05-crew-record.png'))
  await key('Escape')
  await key('3');await wait('window.farHorizonTestState.leader===2')
  await key('1')
  await walk(1080);await key('e');await wait('window.farHorizonTestState.conversation==="juno"')
  start=(await snap())['party'][0]['x']
  await page.keyboard.down('d');await page.wait_for_timeout(600);await page.keyboard.up('d')
  assert abs((await snap())['party'][0]['x']-start)<1
  await click(495,638) # Juno: company wants different things.
  await wait('window.farHorizonTestState.line.includes("Who crosses first")')
  await page.screenshot(path=str(OUT/'06-dialogue.png'))
  await key('Escape')
  await walk(1730);await key('e');await wait('window.farHorizonTestState.conversation==="venn"')
  await click(500,590)
  await wait('window.farHorizonTestState.line.includes("Earth is not dying")')
  await key('Escape')
  await key('g')
  for i in range(4):
   await click(205+i*307,364)
   await click(205+i*307,419)
  await wait('window.farHorizonTestState.boarding_ready')
  await key('Escape')
  await page.reload();await wait('window.farHorizonTestState.boarding_ready')
  assert (await snap())['records']['Orion Kade']['object']==records['object']
  await walk(2160);await key('e');await wait('window.farHorizonTestState.modal')
  await page.screenshot(path=str(OUT/'07-boarding.png'))
  await click(500,523)
  await wait('window.farHorizonTestState.scene==="launch"')
  await page.screenshot(path=str(OUT/'08-crossed.png'))
  if '--full' in sys.argv:
   await wait('window.farHorizonTestState.modal')
   await click(911,59) # Enable original audio using a browser user gesture.
   # The modal intentionally intercepts header controls; enable after holding.
   await click(400,354)
   await click(911,59)
   await wait('window.farHorizonTestState.sound')
   await key('g')
   await click(400,358)
   for target in range(1,5):
    await click(1030,354)
    await wait(f'window.farHorizonTestState.cue==={target}')
    if target==2:
     await page.reload();await wait('window.farHorizonTestState.scene==="launch" && window.farHorizonTestState.cue===2')
    if target==3:
     await page.wait_for_timeout(2600)
     await page.screenshot(path=str(OUT/'09-launch-orbit.png'))
   await click(1030,354)
   await wait('window.farHorizonTestState.scene==="habitation"')
   await page.wait_for_timeout(1100)
   await page.screenshot(path=str(OUT/'10-habitation.png'))
   await key('g');await click(400,358)
   for i in range(4):
    await click(215+i*299,258)
    await click(250+(i%3)*399,392+(i//3)*134)
    if i==0:
     await click(620,462);await write('The bridge matters because our choices affect every department.')
    await click(450,542)
    await wait(f'Object.keys(window.farHorizonTestState.deck_choices).length==={i+1}')
   await page.screenshot(path=str(OUT/'11-deck-directory.png'))
   await click(950,640)
   await wait('window.farHorizonTestState.scene==="bridge"')
   await page.wait_for_timeout(1100)
   await walk(1870)
   await page.screenshot(path=str(OUT/'12-bridge.png'))
   await key('e');await click(450,432)
   await wait('window.farHorizonTestState.flags.anomaly')
   await page.wait_for_timeout(2400)
   await click(450,432)
   await wait('window.farHorizonTestState.line==="insufficient image duration for classification."')
   await page.screenshot(path=str(OUT/'13-iris.png'))
   await key('Escape');await key('e');await click(950,432)
   script={'action':'The tower falls away. A pen lifts from the console.','dialogue':'NIA: We are still together.','reaction':'Nia closes her hand around the stone and watches Earth.'}
   for i,(field,text) in enumerate(script.items()):
    await click(650,362+i*75);await write(text)
    await page.wait_for_function('([field,text])=>window.farHorizonTestState.editors[field]===text',arg=[field,text],timeout=15000)
   await click(280,630)
   await wait('Object.keys(window.farHorizonTestState.script).length===1')
   await page.screenshot(path=str(OUT/'14-screenplay.png'))
   await click(700,630)
   for i in range(4):await click(245+i*280,410)
   await wait('window.farHorizonTestState.script_paper.every(Boolean)')
   await click(650,550)
   await wait('window.farHorizonTestState.scene==="ending" && window.farHorizonTestState.line==="Route correction accepted."')
   await page.wait_for_timeout(1000)
   await click(450,649);await key('e')
   await wait('window.farHorizonTestState.cue===0 && window.farHorizonTestState.modal')
   await click(930,649);await wait('window.farHorizonTestState.line==="Who entered that correction?"')
   await click(930,649);await wait('window.farHorizonTestState.line==="No correction was entered."')
   await page.screenshot(path=str(OUT/'15-cliffhanger.png'))
   await click(930,649);await wait('window.farHorizonTestState.finished')
   await page.screenshot(path=str(OUT/'16-complete.png'))
   async with page.expect_download() as download:
    await click(400,649)
   d=await download.value
   await d.save_as(str(OUT/'session-export.json'))
   exported=json.loads((OUT/'session-export.json').read_text())
   assert exported['finished'] and exported['records']['Orion Kade']['object']==records['object']
   assert exported['script']['Nia Rowan']==script
   assert exported['deck_choices']['Flight']['mode']=='written'
   assert exported['deck_choices']['Science']['mode']=='spoken'
   await page.reload();await wait('window.farHorizonTestState.finished')
  assert not errors,errors
  result={'passed':True,'full_session':'--full' in sys.argv,'checks':['movement and collision floor','party following','leader switching','document readability','reject empty writing','five-field language product','NPC branch and paused movement','GM paper acknowledgement','four performances','synchronous reload persistence','boarding gate and room transition'],'browser_errors':errors}
  (OUT/('full-result.json' if '--full' in sys.argv else 'slice-result.json')).write_text(json.dumps(result,indent=2))
  print(json.dumps(result),flush=True)
  await browser.close()
asyncio.run(run())
