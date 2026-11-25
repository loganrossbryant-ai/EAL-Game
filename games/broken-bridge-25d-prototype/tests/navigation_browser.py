"""Compare the exact packages and exercise real input against the lookout boundary."""
import json
from pathlib import Path
from zipfile import ZipFile

from playwright.sync_api import expect, sync_playwright

root = Path(__file__).resolve().parents[1]
results = root / 'test-results' / 'v060'
results.mkdir(parents=True, exist_ok=True)
old = (root / 'downloads' / 'Broken-Bridge-v0.4.0.html').read_bytes()
previous = (root / 'downloads' / 'Broken-Bridge-v0.5.0.html').read_bytes()
with ZipFile(root / 'build' / 'Broken-Bridge-v0.6.0-Offline.zip') as archive:
    new = archive.read('Broken-Bridge-v0.6.0.html')
save_key = 'broken-bridge-v1'
url = 'http://127.0.0.1:8127/clearing.html'

def state_at(route, x, y):
    return {'version': 1, 'id': 'boundary-review', 'mode': 'middle', 'route': route,
            'clues': ['bridge','rack'] if route == 'bridge' else ['depth','sign'],
            'question': 'How can we reach the lookout?',
            'pieces': ['boardA','boardB','rope'] if route == 'bridge' else ['postA','postB','pack'],
            'x': x, 'y': y}

def open_game(browser, html, state, size=(1366,768), touch=False, motion='reduce'):
    context = browser.new_context(viewport=dict(zip(('width','height'),size)), offline=True,
                                  reduced_motion=motion, has_touch=touch, is_mobile=touch)
    def serve(request):
        if request.request.url == url:
            request.fulfill(body=html, content_type='text/html')
        else:
            request.abort()
    context.route('**/*', serve)
    context.add_init_script(f'localStorage.setItem({json.dumps(save_key)}, {json.dumps(json.dumps(state))})')
    page = context.new_page()
    page.goto(url)
    expect(page.locator('#world canvas')).to_be_visible()
    return page

def position(page):
    saved = page.evaluate(f'JSON.parse(localStorage.getItem({json.dumps(save_key)}))')
    return tuple(round(saved[key],2) for key in ('x','y'))

def push_up(page,legacy=False):
    page.locator('#stage').focus()
    page.keyboard.down('ArrowUp')
    try:
        if legacy:
            page.wait_for_function("JSON.parse(localStorage.getItem('broken-bridge-v1')).y === 202")
        else:
            page.wait_for_timeout(1150)
    finally:
        page.keyboard.up('ArrowUp')
    page.wait_for_timeout(140)
    return position(page)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium')
    for version,html in [('v050',previous),('v060',new)]:
        page = open_game(browser,html,{'version':1,'id':'compare','mode':'middle','x':278,'y':449})
        expect(page.locator('#location')).to_have_text('Ranger clearing')
        page.screenshot(path=results / f'comparison-{version}.png')
        page.context.close()
    evidence = {}
    for version,html,route,x,y,limit in [
        ('v040',old,'bridge',450,288,202),('v060',new,'bridge',450,288,265),
        ('v060',new,'ford',829,299,280),
    ]:
        page = open_game(browser,html,state_at(route,x,y))
        expect(page.locator('#location')).to_have_text('Lookout bank')
        end = push_up(page,legacy=version=='v040')
        assert end[1] == limit if version=='v040' else limit <= end[1] < y, end
        page.screenshot(path=results / f'collision-{version}-{route}.png')
        evidence[f'{version}-{route}-keyboard'] = {'start':[x,y],'end':end}
        page.context.close()
    for route,x,y in [('bridge',450,288),('ford',829,299)]:
        page = open_game(browser,new,state_at(route,x,y),size=(390,844),touch=True)
        expect(page.locator('#location')).to_have_text('Lookout bank')
        start = position(page)
        for row in (175,205,235):
            assert page.evaluate(f"document.elementFromPoint(195,{row}).tagName")=='CANVAS'
            page.touchscreen.tap(195,row)
        page.wait_for_timeout(900)
        end = position(page)
        assert start==end, (route,start,end)
        evidence[f'v060-{route}-touch-background'] = {'start':start,'end':end}
        page.context.close()
    for version,html in [('v050',previous),('v060',new)]:
        page = open_game(browser,html,{'version':1,'id':'ambient','mode':'middle','motion':True,'x':278,'y':449},
                         motion='no-preference')
        expect(page.locator('#location')).to_have_text('Ranger clearing')
        for frame in range(2):
            page.screenshot(path=results / f'ambient-{version}-{frame}.png')
            page.wait_for_timeout(840)
        page.context.close()
    (results / 'navigation-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))
    browser.close()
