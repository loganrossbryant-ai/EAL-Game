"""Check the exact standard release through real stage/desk controls.

Observe the public desk's BroadcastChannel; no debug game globals or state
setters are needed. Serve review-candidate/far-horizon over local HTTP first.
"""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/far-horizon-tests/gm-release'
URL = os.environ.get('FH_RELEASE_URL','http://127.0.0.1:8091')

async def run():
    OUT.mkdir(parents=True,exist_ok=True)
    errors, requests = [], set()
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=[
            '--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage'])
        ctx=await browser.new_context(viewport={'width':1280,'height':720})
        page=await ctx.new_page()
        def observe(tab):
            tab.on('pageerror',lambda e:errors.append(str(e)))
            tab.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            tab.on('request',lambda r:requests.add(r.url))
        observe(page)
        await page.goto(URL)
        await page.locator('#status').wait_for(state='hidden',timeout=90000)
        await page.wait_for_timeout(1800)
        assert await page.evaluate('typeof window.farHorizonTestState')=='undefined'
        assert not await page.locator('input,textarea').count()
        async with page.expect_popup(timeout=15000) as popup: await page.keyboard.press('g')
        gm=await popup.value;observe(gm)
        await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
        await gm.evaluate('''() => {
            const c=new BroadcastChannel(new URLSearchParams(location.search).get('channel'));
            window.__releaseObserver=c;
            c.onmessage=e=>{if(e.data.kind==='state')window.__observedState=e.data.state;};
        }''')
        async def state(check=lambda s:True):
            for _ in range(160):
                value=await gm.evaluate('window.__observedState')
                if value and check(value):return value
                await page.wait_for_timeout(100)
            raise AssertionError('No matching state received from the running release')
        s=await state();assert s['scene']=='s1_terminal'
        await page.screenshot(path=str(OUT/'01-release-terminal.png'))
        await page.keyboard.down('d');await page.wait_for_timeout(1300);await page.keyboard.up('d')
        moved=await state(lambda x:x['party'][0]['x']>s['party'][0]['x']+75)
        assert moved['storage_ok'] and all(x['rig'] for x in moved['party'])
        campaign=json.loads((ROOT/'far-horizon/data/campaign.json').read_text())
        checked_beats=0
        for scene in campaign['scenes']:
            await gm.locator('[data-scene="'+scene['id']+'"]').click()
            await state(lambda x:x['scene']==scene['id'])
            assert await gm.locator('[data-cue]').count()==len(scene['cues'])
            for i,beat in enumerate(scene['cues']):
                await gm.locator('[data-cue="'+str(i)+'"]').click()
                current=await state(lambda x:x['scene']==scene['id'] and x['cue']==i)
                assert current['cue_title']==beat['title']
                if beat.get('clue'):assert current['clue']==beat['clue']
                checked_beats+=1
        await gm.locator('[data-scene="s3_council"]').click()
        await state(lambda x:x['scene']=='s3_council')
        await gm.get_by_role('button',name='Talk: Dr Nia Okafor',exact=True).click()
        await state(lambda x:x['conversation']=='okafor' and x['line'].startswith('Your cells'))
        await gm.locator('[data-action="close"]').click()
        for id,clue,beat in [('s2_record','ticket',1),('s3_evidence','clocks',2),('s3_packet','packet',1)]:
            await gm.locator('[data-scene="'+id+'"]').click()
            await state(lambda x:x['scene']==id)
            await gm.locator('[data-cue="'+str(beat)+'"]').click()
            await state(lambda x:x['cue']==beat and x['clue']==clue)
            await page.screenshot(path=str(OUT/(clue+'-1280.png')))
        await page.reload()
        restored=await state(lambda x:x['scene']=='s3_packet' and x['clue']=='packet')
        assert restored['revealed']['ticket'] and restored['revealed']['clocks']
        for lang in ('zh','ko','ja'):
            await gm.locator('#language').select_option(lang)
            await gm.locator('[data-action="glossary"]').click()
            await state(lambda x:x['language']==lang and x['conversation']=='glossary')
            await page.screenshot(path=str(OUT/('words-'+lang+'-1280.png')))
            await gm.locator('[data-action="close"]').click()
        assert await page.evaluate('typeof window.farHorizonTestState')=='undefined'
        assert errors==[],errors
        assert all(url.startswith(URL) or url.startswith('data:') or url.startswith('blob:') for url in requests),requests
        result={'viewport':'1280x720','standard_release':True,'debug_global':False,'checked_beats':checked_beats,'scene_jump_save_clues_dialogue_support':'passed','voice_recordings':restored['recordings'],'browser_errors':errors,'requests':sorted(requests)}
        (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2),flush=True)
        await browser.close()

if __name__=='__main__':asyncio.run(run())
