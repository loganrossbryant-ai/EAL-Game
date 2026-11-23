"""Exercise the exact extracted single-file package with network denied."""
import json
import os
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
RESULTS = ROOT / 'test-results'
URL = 'http://127.0.0.1:8127/Broken-Bridge-v0.2.0.html'
RESULTS.mkdir(exist_ok=True)

def play(browser, name, viewport, touch, mode, route):
    context = browser.new_context(viewport=viewport, has_touch=touch, is_mobile=touch,
                                  offline=True, reduced_motion='reduce', accept_downloads=True)
    external = []
    def serve(request):
        if request.request.url == URL:
            request.fulfill(status=200, body=HTML, content_type='text/html; charset=utf-8')
        elif request.request.url.endswith('/favicon.ico') and request.request.url.startswith('http://127.0.0.1:8127/'):
            request.fulfill(status=204)
        else:
            external.append(request.request.url)
            request.abort()
    context.route('**/*', serve)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.set_default_timeout(6500)

    def click(locator):
        if touch:
            locator.tap()
        else:
            locator.click()

    def button(label):
        return page.get_by_role('button', name=label, exact=True)

    def press(label):
        click(button(label))

    def pin(label):
        click(page.locator('#pins').get_by_role('button', name=label, exact=True))
        expect(page.locator('#panel')).to_be_visible(timeout=7000)

    def position():
        return page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1')).x")

    press('Elementary · supported English' if mode == 'elementary' else 'Middle school · field investigation')
    expect(page.locator('#objective')).to_have_text('Meet Ranger Lin')
    expect(page.locator('canvas')).to_be_visible()
    start_x = position()
    # Exercise real keyboard movement and touch walking before using landmarks.
    if touch:
        box = page.locator('canvas').bounding_box()
        page.touchscreen.tap(box['x']+box['width']*.68, box['y']+box['height']*.83)
        page.wait_for_timeout(550)
    else:
        page.keyboard.down('ArrowRight')
        page.wait_for_timeout(330)
        page.keyboard.up('ArrowRight')
        page.wait_for_timeout(100)
    assert position() > start_x + 12, (name, position(), errors)
    page.screenshot(path=RESULTS / f'{name}-clearing.png')
    pin('Ranger Lin')
    page.screenshot(path=RESULTS / f'{name}-ranger.png')
    press('I practised speaking')
    expect(page.locator('#feedback')).to_contain_text('your own report')
    press('Can you help me?' if mode == 'elementary' else 'Where is the safe crossing?')
    press('Explore the riverbank')
    pin('Ranger Lin')
    press('Discuss a crossing plan')
    page.locator('#recommend').select_option('unsafe')
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('38 cm')
    page.locator('#recommend').select_option(route)
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('both observations')
    press('Hint')
    expect(page.locator('#feedback')).to_contain_text('clue')
    press('Close dialog')

    def walk(target, direction):
        labels = {113:'Tool rack',246:'Ranger Lin',447:'Broken bridge',778:'Depth marker',934:'Fallen sign'}
        marker = page.locator('#pins').get_by_role('button', name=labels[target], exact=True)
        for _ in range(12):
            if marker.is_visible():
                return
            before = position()
            box = page.locator('canvas').bounding_box()
            x=box['x']+box['width']*(.89 if direction>0 else .11)
            for fraction in [.78,.72,.65,.60,.56,.88]:
                y=box['y']+box['height']*fraction
                if page.evaluate("([x,y]) => document.elementFromPoint(x,y)?.tagName === 'CANVAS'", [x,y]):
                    break
            else:
                raise AssertionError('No unblocked trail tap location')
            (page.touchscreen.tap if touch else page.mouse.click)(x,y)
            page.wait_for_timeout(850)
            assert (position()-before)*direction>12, (before, position(), errors)
        raise AssertionError('Could not reach '+labels[target])

    def walk_right(target):
        walk(target,1)

    def walk_left(target):
        walk(target,-1)

    walk_left(113)
    pin('Tool rack')
    if mode=='elementary':
        expect(page.locator('[lang=zh-Hans]').first).to_be_visible()
    press('Back to trail')
    walk_right(447)
    pin('Broken bridge')
    expect(page.locator('#panel-body')).to_contain_text('90 cm')
    press('Back to trail')
    if not touch: page.mouse.move(0,0)
    page.screenshot(path=RESULTS / f'{name}-broken.png')
    walk_right(778)
    pin('Depth marker')
    expect(page.locator('#panel-body')).to_contain_text('16 cm')
    page.screenshot(path=RESULTS / f'{name}-evidence.png')
    press('Back to trail')
    walk_right(934)
    pin('Fallen sign')
    press('Back to trail')
    expect(page.locator('#count')).to_have_text('4 / 4')
    walk_left(246)
    pin('Ranger Lin')
    press('Report the damaged bridge')
    expect(page.locator('#feedback')).to_contain_text('The bridge is broken. I found a board.')
    press('Discuss a crossing plan')
    page.locator('#recommend').select_option(route)
    for clue in (['bridge','rack'] if route=='bridge' else ['depth','sign']):
        click(page.locator(f'label:has(input[value="{clue}"])'))
    page.locator('#draft').fill('I checked the field clues and compared both crossings.')
    press('Tell Ranger Lin')
    expect(page.locator('#panel-title')).to_have_text('Crossing authorized')
    press('Back to trail')
    work_site='Broken bridge' if route=='bridge' else 'Fallen sign'
    walk_right(447 if route=='bridge' else 934)
    pin(work_site)

    def choose(action):
        click(page.locator(f'[data-action="{action}"]'))
    choose('pick2')
    choose('place2')
    expect(page.locator('#feedback')).to_contain_text('before')
    choose('pick0')
    choose('place1')
    expect(page.locator('#feedback')).to_contain_text('matching')
    if route=='ford':
        choose('place0')
        expect(page.locator('#feedback')).to_contain_text('northwest')
        for _ in range(3):
            press('Turn marker clockwise')
    if touch or route=='ford':
        choose('place0')
    else:
        page.locator('[data-action=pick0]').drag_to(page.locator('[data-action=place0]'))
    expect(page.locator('[data-action=place0]')).to_be_disabled()
    page.screenshot(path=RESULTS / f'{name}-workbench.png')
    page.reload()
    pin(work_site)
    expect(page.locator('[data-action=place0]')).to_be_disabled()
    choose('pick1')
    if route=='ford':
        press('Turn marker clockwise')
    choose('place1')
    if name=='desktop-bridge':
        press('Close dialog')
        press('Settings')
        press('Environmental motion: reduced')
        press('Back to trail')
        pin(work_site)
    choose('pick2')
    choose('place2')
    if name=='desktop-bridge':
        # Take time to read the modal. The ranger must wait before starting the crossing.
        page.wait_for_timeout(4500)
    press('Watch the crossing')
    if name=='desktop-bridge':
        first = page.locator('canvas').screenshot()
        page.wait_for_timeout(330)
        assert first != page.locator('canvas').screenshot(), 'Expected river and ranger animation'
        pin('Ranger Lin')
        expect(page.locator('#panel-title')).to_have_text('Ranger Lin is on the trail')
        press('Back to trail')
        page.wait_for_timeout(4600)
    expect(page.locator('#objective')).to_have_text('Report to the ranger')
    press('Walk the crossing')
    expect(page.locator('#location')).to_have_text('Lookout bank', timeout=9000)
    press('Return across the river')
    expect(button('Walk the crossing')).to_be_enabled(timeout=9000)
    if not touch: page.mouse.move(0,0)
    page.screenshot(path=RESULTS / f'{name}-outcome.png')
    walk_left(246)
    pin('Ranger Lin')
    expect(page.locator('#panel-title')).to_have_text('Report from the lookout')
    with page.expect_download() as pending:
        press('Export progress')
    record = json.loads(Path(pending.value.path()).read_text())
    assert record['languageMode']==mode
    assert record['outcome']=={'route':route,'piecesPlaced':(['boardA','boardB','rope'] if route=='bridge' else ['postA','postB','pack']),
                               'suppliesDelivered':True,'fieldReportComplete':True}
    assert len(record['evidence'])==4
    assert [attempt['accepted'] for attempt in record['observedAnswers']['recommendations']]==[False,False,True]
    assert record['selfReportedSpeakingPractice']==['Ranger conversation']
    assert record['ungradedReasoning'].startswith('I checked')
    press('Back to trail')
    page.reload()
    expect(page.locator('#objective')).to_have_text('Supplies delivered')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    press('Settings')
    press('Sound effects: off')
    press('Sound effects: on')
    if name=='desktop-bridge':
        press('Environmental motion: on')
        press('Environmental motion: reduced')
    else:
        press('Environmental motion: reduced')
        press('Environmental motion: on')
    if name=='desktop-bridge':
        with page.expect_download() as saved_backup:
            press('Back up save')
        backup_bytes=Path(saved_backup.value.path()).read_bytes()
        press('Restore a saved mission')
        page.locator('#save-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'bad'})
        press('Restore this mission')
        expect(page.locator('#feedback')).to_contain_text('Current progress is intact')
        page.locator('#save-file').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':backup_bytes})
        press('Restore this mission')
        expect(page.locator('#notice')).to_have_text('Mission restored.')
        expect(page.locator('#objective')).to_have_text('Supplies delivered')
        press('Settings')
    if touch:
        press('Focus view: off')
        press('Close dialog')
        page.screenshot(path=RESULTS / f'{name}-compact.png')
        press('Settings')
    press('Reset progress / change guide')
    press('Reset this mission')
    expect(page.locator('#panel-title')).to_have_text('Choose your field guide')
    assert not errors, errors
    assert not external, external
    context.close()
    print(f'PASS {name}: {mode}/{route}, offline journey, retries, resume, export, settings, reset',flush=True)

with ZipFile(BUILD / 'Broken-Bridge-v0.2.0-Offline.zip') as package:
    assert package.testzip() is None
    HTML = package.read('Broken-Bridge-v0.2.0.html')
assert HTML == (BUILD / 'Broken-Bridge-v0.2.0.html').read_bytes()
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'))
    for args in [
        ('desktop-bridge',{'width':1366,'height':768},False,'elementary','bridge'),
        ('desktop-ford',{'width':1366,'height':768},False,'middle','ford'),
        ('iphone-portrait-ford',{'width':390,'height':844},True,'elementary','ford'),
        ('iphone-landscape-bridge',{'width':844,'height':390},True,'middle','bridge'),
    ]:
        if not os.getenv('BRIDGE_TEST_CASE') or os.getenv('BRIDGE_TEST_CASE')==args[0]:
            play(browser,*args)
    browser.close()
