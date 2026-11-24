"""Exercise the exact extracted single-file package with network denied."""
import json
import os
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
RESULTS = ROOT / 'test-results' / 'v030'
ARTIFACT = 'Broken-Bridge-v0.3.0.html'
URL = f'http://127.0.0.1:8127/{ARTIFACT}'
RESULTS.mkdir(parents=True, exist_ok=True)

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
    context.add_init_script("""
        window.voicePlays = [];
        const originalPlay = HTMLMediaElement.prototype.play;
        HTMLMediaElement.prototype.play = function () {
            const result = originalPlay.call(this);
            const entry = { audio: this, resolved: false, source: this.src };
            window.voicePlays.push(entry);
            if (result) result.then(() => { entry.resolved = true; }, () => {});
            return result;
        };
    """)
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

    def saved():
        return page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1'))")

    def position():
        return saved()['x']

    def walk_to_marker(marker, direction):
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
        raise AssertionError(f'Could not reach {marker}')

    def walk(target, direction):
        labels = {113:'Tool rack',246:'Ranger Lin',447:'Broken bridge',778:'Depth marker',934:'Fallen sign'}
        marker = page.locator('#pins').get_by_role('button', name=labels[target], exact=True)
        walk_to_marker(marker, direction)

    def walk_right(target):
        walk(target,1)

    def walk_left(target):
        walk(target,-1)

    press('Elementary · supported English' if mode == 'elementary' else 'Middle school · field investigation')
    expect(page.locator('#objective')).to_have_text('Meet Ranger Lin')
    expect(page.locator('canvas')).to_be_visible()
    expect(page.locator('#pins').get_by_role('button', name='Ranger Lin', exact=True)).to_be_visible()
    page.screenshot(path=RESULTS / f'{name}-opening.png')
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
    walk_left(246)
    pin('Ranger Lin')
    page.screenshot(path=RESULTS / f'{name}-ranger.png')
    if AUDIO_PACKAGED:
        previous_plays = page.evaluate('window.voicePlays.length')
        press('Replay Ranger Lin')
        page.wait_for_function("""
            start => window.voicePlays.slice(start).some(entry => entry.resolved
                && entry.source.startsWith('data:audio/mpeg;base64,')
                && entry.audio.currentTime > .05 && entry.audio.duration > .1)
        """, arg=previous_plays)
    press('I practised speaking')
    expect(page.locator('#feedback')).to_contain_text('your own report')
    press('Can you help me?' if mode == 'elementary' else 'Where is the safe crossing?')
    press('Explore the riverbank')
    pin('Ranger Lin')
    press('Discuss a crossing plan')
    page.locator('#recommend').select_option('unsafe')
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('thirty-eight centimetres')
    page.locator('#recommend').select_option(route)
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('both observations')
    press('Hint')
    expect(page.locator('#feedback')).to_contain_text('clue')
    press('Close dialog')

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
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('Lin needs')
    expect(page.locator('#panel-title')).to_have_text('Recommend a crossing')
    if mode == 'elementary':
        click(page.get_by_text('Open word bank', exact=True))
        press('I saw')
        expect(page.locator('#draft')).to_have_value('I saw')
    message = 'The spare boards are 90 cm long and fit the gap.' if route == 'bridge' else 'The ford is 16 cm deep, below the 20 cm limit.'
    page.locator('#draft').fill(message)
    press('Tell Ranger Lin')
    expect(page.locator('#panel-title')).to_have_text('Crossing authorized')
    press('Back to trail')
    coordinates = {
        'bridge': {'pick': (83,119,155), 'place': (443,455,481)},
        'ford': {'pick': (903,939,204), 'place': (958,851,977)},
    }[route]
    pieces = ['boardA','boardB','rope'] if route=='bridge' else ['postA','postB','pack']
    names = ['first board','second board','rope'] if route=='bridge' else ['near marker','far marker','supply pack']
    notice = page.locator('#notice')
    layer = page.locator('.field-layer')

    def field_button(action):
        return layer.locator(f'button[data-action="{action}"]')

    def show_field_action(action):
        marker = field_button(action)
        anchor = coordinates['pick' if action.startswith('pick') else 'place'][int(action[-1])]
        walk_to_marker(marker, 1 if anchor > position() else -1)
        return marker

    def choose(action):
        click(show_field_action(action))
        if action.startswith('pick'):
            expect(page.locator('#field-holding')).to_contain_text(names[int(action[-1])], ignore_case=True)

    def wait_for_piece(index):
        page.wait_for_function("""
            id => JSON.parse(localStorage.getItem('broken-bridge-v1')).pieces.includes(id)
        """, arg=pieces[index])

    expect(page.locator('#panel')).not_to_be_visible()
    choose('pick2')
    choose('place2')
    expect(notice).to_contain_text('before')
    assert not saved()['pieces']
    press('Return material')
    expect(page.locator('#field-holding')).to_contain_text('Crossing materials')
    choose('pick0')
    choose('place1')
    expect(notice).to_contain_text('matching')
    assert not saved()['pieces']
    if route=='ford':
        choose('place0')
        expect(notice).to_contain_text('northwest')
        for _ in range(3):
            press('Turn marker clockwise')
    expect(page.locator('#panel')).not_to_be_visible()
    page.screenshot(path=RESULTS / f'{name}-physical-carry.png')
    if touch or route=='ford':
        choose('place0')
    else:
        page.locator('.field-carried').drag_to(show_field_action('place0'))
    wait_for_piece(0)
    expect(field_button('pick0')).to_be_hidden()
    expect(page.locator('#panel')).not_to_be_visible()
    page.screenshot(path=RESULTS / f'{name}-physical-placement.png')
    page.reload()
    assert saved()['pieces'] == [pieces[0]]
    expect(layer).to_be_visible()
    expect(field_button('pick0')).to_be_hidden()
    choose('pick1')
    if route=='ford':
        press('Turn marker clockwise')
    choose('place1')
    wait_for_piece(1)
    if name=='desktop-bridge':
        press('Settings')
        press('Environmental motion: reduced')
        press('Back to trail')
    click(page.locator('#field-guide'))
    expect(page.locator('#field-holding')).to_contain_text(names[2], ignore_case=True, timeout=14000)
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
    if name=='desktop-ford':
        page.wait_for_function("JSON.parse(localStorage.getItem('broken-bridge-v1')).y < 315")
        page.reload()
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
    recommendations = record['observedAnswers']['recommendations']
    assert [attempt['accepted'] for attempt in recommendations][:2] == [False, False]
    assert all(not attempt['accepted'] for attempt in recommendations[:-1])
    assert recommendations[-1]['accepted'] is True
    assert recommendations[-1]['message'] == message
    assert recommendations[-1]['submissionSource'] == ('supported-elementary' if mode=='elementary' else 'student-written')
    assert recommendations[-1]['languageReview'] == 'teacher-review'
    assert record['selfReportedSpeakingPractice']==['Ranger conversation']
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
    voice_status = 'local voice replay' if AUDIO_PACKAGED else 'voice assets absent'
    print(f'PASS {name}: {mode}/{route}, offline journey, retries, resume, export, settings, reset, {voice_status}',flush=True)

def migrate(browser):
    previous_name = 'Broken-Bridge-v0.2.0.html'
    previous_url = URL.replace(ARTIFACT, previous_name)
    previous_html = (ROOT / 'downloads' / previous_name).read_bytes()
    context = browser.new_context(viewport={'width':1366,'height':768},
                                  offline=True, reduced_motion='reduce', accept_downloads=True)
    unexpected = []

    def serve(request):
        if request.request.url in (URL, previous_url):
            artifact = HTML if request.request.url==URL else previous_html
            request.fulfill(status=200, body=artifact, content_type='text/html; charset=utf-8')
        elif request.request.url == 'http://127.0.0.1:8127/favicon.ico':
            request.fulfill(status=204)
        else:
            unexpected.append(request.request.url)
            request.abort()

    context.route('**/*', serve)
    page = context.new_page()
    page.set_default_timeout(6500)

    def press(label):
        page.get_by_role('button', name=label, exact=True).click()

    def pin(label):
        page.locator('#pins').get_by_role('button', name=label, exact=True).click()
        expect(page.locator('#panel')).to_be_visible()

    page.goto(previous_url)
    press('Elementary · supported English')
    pin('Ranger Lin')
    press('Can you help me?')
    press('Explore the riverbank')
    pin('Tool rack')
    press('Back to trail')
    pin('Broken bridge')
    press('Back to trail')
    pin('Ranger Lin')
    press('Discuss a crossing plan')
    page.locator('#recommend').select_option('bridge')
    page.locator('input[value=bridge]').check()
    page.locator('input[value=rack]').check()
    press('Tell Ranger Lin')
    expect(page.locator('#panel-title')).to_have_text('Crossing authorized')
    press('Back to trail')
    pin('Broken bridge')
    page.locator('[data-action=pick0]').click()
    page.locator('[data-action=place0]').click()
    expect(page.locator('#feedback')).to_contain_text('seated')

    page.goto(URL)
    expect(page.locator('.field-layer')).to_be_visible()
    state = page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1'))")
    assert state['route']=='bridge' and state['pieces']==['boardA']
    expect(page.locator('.field-layer [data-action=pick0]')).to_be_hidden()
    press('Field log')
    with page.expect_download() as pending:
        press('Export progress')
    record = json.loads(Path(pending.value.path()).read_text())
    legacy = record['observedAnswers']['recommendations'][-1]
    assert legacy['accepted'] is True
    assert legacy['submissionSource'] == 'legacy-route-selection'
    assert legacy['languageReview'] == 'not-applicable'
    assert record['outcome']['piecesPlaced'] == ['boardA']
    assert not unexpected, unexpected
    context.close()
    print('PASS migration: live v0.2.0 partial bridge save into cold v0.3.0; legacy route selection distinguished',flush=True)

with ZipFile(BUILD / f'{Path(ARTIFACT).stem}-Offline.zip') as package:
    assert package.testzip() is None
    HTML = package.read(ARTIFACT)
assert HTML == (BUILD / ARTIFACT).read_bytes()
AUDIO_PACKAGED = b'data:audio/mpeg;base64,' in HTML
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'))
    cases = [
        ('desktop-bridge',{'width':1366,'height':768},False,'elementary','bridge'),
        ('desktop-ford',{'width':1366,'height':768},False,'middle','ford'),
        ('iphone-portrait-ford',{'width':390,'height':844},True,'elementary','ford'),
        ('iphone-landscape-bridge',{'width':844,'height':390},True,'middle','bridge'),
    ]
    selection = os.getenv('BRIDGE_TEST_CASE')
    selected = [args for args in cases if not selection or selection==args[0]]
    assert selected or selection=='migration', f'Unknown BRIDGE_TEST_CASE {selection!r}'
    for args in selected:
        play(browser,*args)
    if not selection or selection=='migration':
        migrate(browser)
    browser.close()
