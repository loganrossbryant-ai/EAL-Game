"""Real browser checks for the GM-only first three sessions and separate desk.

Only real keyboard, mouse and GM controls change the game. Debug snapshots are
read-only observations. No student input or artificial game-state setter exists.
"""
import asyncio
import io
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'artifacts/far-horizon-tests/gm'
URL = os.environ.get('FH_URL', 'http://127.0.0.1:8090')
CAMPAIGN = json.loads((ROOT / 'far-horizon/data/campaign.json').read_text())


async def run():
    OUT.mkdir(parents=True, exist_ok=True)
    errors, requests, findings = [], set(), {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=[
            '--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-dev-shm-usage'])
        ctx = await browser.new_context(viewport={'width':1366,'height':768})
        page = await ctx.new_page()
        def observe(tab):
            tab.on('pageerror', lambda e: errors.append(str(e)))
            tab.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            tab.on('request', lambda r: requests.add(r.url))
        observe(page)
        await page.goto(URL)
        await page.wait_for_function('window.farHorizonTestState', timeout=90000)
        async def snap(): return await page.evaluate('window.farHorizonTestState')
        async def wait(expr):
            await page.wait_for_function('window.farHorizonTestState && (' + expr + ')', timeout=20000)
        async def capture(name):
            await page.wait_for_timeout(180)
            await page.screenshot(path=str(OUT/(name+'.png')))
        await capture('01-terminal')
        initial = await snap()
        assert initial['scene'] == 's1_terminal' and len(initial['index']) == 18
        assert initial['recordings'] == 0 or initial['recordings'] == len(json.loads((ROOT/'far-horizon/assets/voices/dialogue.json').read_text())['lines'])
        assert not await page.locator('input,textarea').count()
        await page.keyboard.down('d')
        await page.wait_for_timeout(1100)
        samples = []
        for _ in range(36):
            samples.append(await snap())
            await page.wait_for_timeout(65)
        await capture('02-walking')
        await page.keyboard.up('d')
        await page.wait_for_timeout(1600)
        settled = await snap()
        assert all(abs(m['vx']) < 1 for m in settled['party']), settled['party']
        stable = [s for s in samples if s['party'][0]['vx'] > 120]
        assert len(stable) >= 25
        assert max(s['party'][0]['hip_y'] for s in stable)-min(s['party'][0]['hip_y'] for s in stable) < 1.05
        assert max(s['party'][0]['y'] for s in stable)-min(s['party'][0]['y'] for s in stable) < .05
        plants = []
        for a,b in zip(stable,stable[1:]):
            if a['clock'] == b['clock']: continue
            for old,new in zip(a['party'],b['party']):
                for f,g in zip(old['feet'],new['feet']):
                    if f['stance'] and g['stance'] and f['contact']==g['contact']:
                        drift=abs(f['world_x']-g['world_x']);assert drift < .005;assert g['height']==0;plants.append(drift)
        assert len(plants) > 40
        for s in stable[8:]:
            for a,b in zip(s['party'],s['party'][1:]):
                assert 78 < a['x']-b['x'] < 95 and b['vx'] > 115
        await page.keyboard.down('a');await page.wait_for_timeout(1600)
        left=await snap();assert all(m['vx'] < -115 and m['facing']==-1 for m in left['party']),left['party']
        await capture('03-turn-left');await page.keyboard.up('a')
        await page.wait_for_timeout(1200)
        async with page.expect_popup(timeout=15000) as popup:
            await page.keyboard.press('g')
        gm=await popup.value;observe(gm)
        await gm.locator('#connection').filter(has_text='Connected to the stage').wait_for()
        assert await gm.locator('[data-scene]').count()==18
        assert await gm.locator('[data-clue]').count()==13
        await gm.screenshot(path=str(OUT/'04-gm-desk.png'))
        async def jump(id):
            await gm.locator('[data-scene="'+id+'"]').click()
            await wait('window.farHorizonTestState.scene==='+json.dumps(id))
        async def cue(index):
            await gm.locator('[data-cue="'+str(index)+'"]').click()
            await wait('window.farHorizonTestState.cue==='+str(index))
            await page.wait_for_timeout(180)
        async def command(action):
            await gm.locator('[data-action="'+action+'"]').first.click()
            await page.wait_for_timeout(250)
        await gm.locator('[data-clue="ticket"]').click()
        assert 'TOMORROW 14:32' in await gm.locator('#clue-preview').inner_text()
        assert 'Collision with unrecorded passenger resolved.' in await gm.locator('#clue-preview').inner_text()
        assert (await snap())['clue']=='' and not (await snap())['revealed'].get('ticket')
        await gm.get_by_role('button',name='Reveal on stage',exact=True).click()
        await wait('window.farHorizonTestState.clue==="ticket"')
        await capture('05-ticket')
        await gm.get_by_role('button',name='Hide from evidence board',exact=True).click()
        await wait('window.farHorizonTestState.clue==="" && !window.farHorizonTestState.revealed.ticket')

        visited, clue_cards = [], set()
        for scene in CAMPAIGN['scenes']:
            await jump(scene['id'])
            await capture(scene['id']+'-scene')
            for index, beat in enumerate(scene['cues']):
                await cue(index)
                current=await snap()
                assert current['cue_title']==beat['title']
                assert current.get('layout_issues',[])==[],(scene['id'],index,current.get('layout_issues'))
                if beat.get('clue'):
                    key=beat['clue'];assert current['clue']==key and current['revealed'][key]
                    if key not in clue_cards: await capture('clue-'+key)
                    clue_cards.add(key)
                if beat.get('effect')=='round2':
                    await page.wait_for_timeout(1300)
                    assert (await snap())['camera']>1000
                    await capture('encounter-life-support')
            visited.append(scene['id'])
        assert len(visited)==18 and clue_cards==set(CAMPAIGN['clues'])
        last=await snap();await command('next');assert (await snap())['scene']==last['scene']
        await jump('s2_record');await cue(1)
        await command('close');await page.keyboard.press('c');await wait('window.farHorizonTestState.conversation==="board"')
        await capture('06-all-evidence');await command('close')
        await page.reload();await wait('window.farHorizonTestState.scene==="s2_record" && window.farHorizonTestState.cue===1')
        assert (await snap())['revealed']['ticket']
        await command('close')

        await jump('s1_terminal')
        await gm.get_by_role('button',name='Talk: Captain Mara Venn',exact=True).click()
        await wait('window.farHorizonTestState.conversation==="venn"')
        await page.mouse.click(500,606)
        await wait('window.farHorizonTestState.line.includes("humanity should never")')
        await capture('07-selectable-dialogue')
        location=(await snap())['party'][0]['x']
        await page.keyboard.down('d');await page.wait_for_timeout(500);await page.keyboard.up('d')
        assert abs((await snap())['party'][0]['x']-location)<1
        await command('close')

        for language in ('zh','ko','ja'):
            await gm.locator('#language').select_option(language)
            await gm.locator('[data-action="glossary"]').click()
            await wait('window.farHorizonTestState.conversation==="glossary" && window.farHorizonTestState.language==='+json.dumps(language))
            assert await gm.locator('#word-list .word').count()==21
            await capture('words-'+language)
            await command('close')
        await gm.locator('[data-action="clean"]').click();await wait('window.farHorizonTestState.clean')
        await page.keyboard.press('p');await wait('!window.farHorizonTestState.clean')

        motion={}
        for id in ('s1_terminal','s1_launch','s1_habitation','s1_observation','s2_recreation','s2_malfunction','s2_restricted','s3_observation'):
            await jump(id);await cue(0);await command('close')
            await page.wait_for_timeout(600)
            a=await snap();before=await page.screenshot(path=str(OUT/('motion-'+id+'-a.png')))
            await page.wait_for_timeout(1200)
            b=await snap();after=await page.screenshot(path=str(OUT/('motion-'+id+'-b.png')))
            assert any(abs(x['x']-y['x'])>1 or abs(x['y']-y['y'])>1 or abs(x['rotation']-y['rotation'])>.05 for x,y in zip(a['subjects'],b['subjects']))
            aa=np.asarray(Image.open(io.BytesIO(before)).convert('RGB')).astype(float)
            bb=np.asarray(Image.open(io.BytesIO(after)).convert('RGB')).astype(float)
            # Every initial view must contain a visibly animated subject to the right of its cue card.
            fraction=float((np.abs(aa[330:460,750:1325]-bb[330:460,750:1325]).max(axis=2)>8).mean())
            assert fraction>.0006,(id,fraction)
            motion[id]=round(fraction,5)
        await command('freeze');await wait('window.farHorizonTestState.paused')
        held=await snap();await page.wait_for_timeout(600);assert (await snap())['clock']==held['clock']
        await command('freeze')
        await page.set_viewport_size({'width':1280,'height':720})
        await jump('s3_evidence');await cue(2);await capture('08-1280-clocks')
        await command('close');await capture('09-1280-stage')
        assert all(url.startswith(URL) or url.startswith('data:') or url.startswith('blob:') for url in requests),requests
        assert errors==[],errors
        findings={'scenes':visited,'clues':sorted(clue_cards),'hip_peak_to_peak_px':round(max(s['party'][0]['hip_y'] for s in stable)-min(s['party'][0]['hip_y'] for s in stable),4),'planted_contact_observations':len(plants),'scene_motion_changed_pixel_fraction':motion,'browser_errors':errors,'requests':sorted(requests),'voices':initial['recordings']}
        (OUT/'results.json').write_text(json.dumps(findings,indent=2)+'\n')
        (OUT/'walk-samples.json').write_text(json.dumps(samples))
        print(json.dumps(findings,indent=2),flush=True)
        await browser.close()

if __name__=='__main__':
    asyncio.run(run())
