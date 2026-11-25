"""Exercise the exact extracted single-file package with network denied."""
import base64
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
RESULTS = ROOT / 'test-results' / 'v061'
ARTIFACT = 'Broken-Bridge-v0.6.1.html'
URL = f'http://127.0.0.1:8127/{ARTIFACT}'
RESULTS.mkdir(parents=True, exist_ok=True)

def observe_actor_draws(context):
    # Observe real Phaser Canvas rendering, so a moving water layer or a
    # debug label alone cannot satisfy the animation assertions.
    context.add_init_script(script="""
        (() => {
            const identities = new Map(Object.entries(DRAW_KEYS));
            const draws = [];
            window.actorDraws = draws;
            const original = CanvasRenderingContext2D.prototype.drawImage;
            CanvasRenderingContext2D.prototype.drawImage = function (image, ...args) {
                const result = original.call(this, image, ...args);
                const src = image.currentSrc || image.src;
                if (this.canvas.closest('#world') && src) {
                    const asset = identities.get(src.length + '|' + src.slice(-64));
                    if (asset) draws.push({
                        asset,
                        scoutAction: this.canvas.dataset.scoutAction,
                        rangerAction: this.canvas.dataset.rangerAction,
                    });
                }
                return result;
            };
        })();
    """.replace('DRAW_KEYS', json.dumps(DRAW_KEYS)))

def drawn_frames(page, actor, direction=None, action=None):
    entries = page.evaluate('window.actorDraws')
    stem = f'{actor}-v4-' if direction is None else f'{actor}-v4-{direction}-'
    return {entry['asset'] for entry in entries if entry['asset'].startswith(stem)
            and (action is None or entry.get(f'{actor}Action')==action)}

def clear_draws(page):
    page.evaluate('window.actorDraws.length = 0')

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
    observe_actor_draws(context)
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

    def voice_replay(locator):
        previous_plays = page.evaluate('window.voicePlays.length')
        click(locator)
        page.wait_for_function("""
            start => window.voicePlays.slice(start).some(entry => entry.resolved
                && entry.source.startsWith('data:audio/mpeg;base64,')
                && entry.audio.currentTime > .05 && entry.audio.duration > .1)
        """, arg=previous_plays)

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
    press('Enable sound')
    expect(button('Mute sound')).to_be_visible()
    start_x = position()
    # Exercise real keyboard movement and touch walking before using landmarks.
    if touch:
        box = page.locator('canvas').bounding_box()
        page.touchscreen.tap(box['x']+box['width']*.68, box['y']+box['height']*.83)
        page.wait_for_timeout(550)
    else:
        page.keyboard.down('ArrowRight')
        try:
            page.wait_for_function("x => JSON.parse(localStorage.getItem('broken-bridge-v1')).x > x+12", arg=start_x)
        finally:
            page.keyboard.up('ArrowRight')
        page.wait_for_timeout(100)
    assert position() > start_x + 12, (name, position(), errors)
    page.screenshot(path=RESULTS / f'{name}-clearing.png')
    walk_left(246)
    pin('Ranger Lin')
    page.screenshot(path=RESULTS / f'{name}-ranger.png')
    if AUDIO_PACKAGED:
        voice_replay(button('Replay Ranger Lin'))
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
    expect(page.locator('#panel-kicker')).to_have_text('RIVER SURVEY')
    press('Log reading')
    expect(page.locator('#feedback')).to_contain_text('touches the riverbed')
    press('Hint')
    expect(page.locator('#feedback')).to_contain_text('weight touches')
    probe = page.locator('#probe-length')

    def drive_range(control, fraction):
        if touch:
            control.evaluate("element => element.scrollIntoView({block:'center'})")
            box = control.bounding_box()
            assert 0<=box['y']<=viewport['height']-box['height'],box
            page.touchscreen.tap(box['x']+box['width']*fraction, box['y']+box['height']*.5)
        else:
            control.press('End' if fraction>.95 else 'Home')
            if fraction<=.95:
                for _ in range(round(float(control.get_attribute('max'))*fraction)):
                    page.keyboard.press('ArrowRight')

    drive_range(probe,.98)
    expect(page.locator('#probe-status')).to_have_text('Bed contact · 38 cm')
    press('White stones')
    expect(page.locator('#feedback')).to_contain_text('Raise the probe')
    press('Log reading')
    assert saved()['survey']['readings']=={'bridge':38}
    if name=='desktop-bridge':
        press('Back to trail')
        page.reload()
        pin('Depth marker')
        expect(page.locator('#sounding-record')).to_contain_text('38 cm')
    press('Raise probe')
    press('White stones')
    drive_range(probe,.98)
    expect(page.locator('#probe-status')).to_have_text('Bed contact · 16 cm')
    page.screenshot(path=RESULTS / f'{name}-sounding-in-use.png')
    press('Log reading')
    page.locator('#ford-station').select_option('bridge')
    page.locator('#ford-relation').select_option('below')
    press('Log comparison')
    expect(page.locator('#feedback')).to_contain_text('shallower')
    assert 'depth' not in saved()['clues']
    page.locator('#ford-station').select_option('ford')
    press('Log comparison')
    expect(page.locator('#feedback')).to_contain_text('16 cm, below')
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
    press('Ask about the old ford notice')
    press('When did you check the ford?')
    expect(page.locator('#panel-body')).to_contain_text('26 cm')
    click(page.locator('label:has(input[name=notice-source][value=log])'))
    click(page.locator('label:has(input[name=notice-source][value=rack])'))
    page.locator('#notice-correction').fill('Today the ford is 16 cm, below 20 cm.')
    press('Show the two records')
    expect(page.locator('#feedback')).to_contain_text('dated log and today')
    click(page.locator('label:has(input[name=notice-source][value=rack])'))
    click(page.locator('label:has(input[name=notice-source][value=sounding])'))
    page.locator('#notice-correction').fill('Today the water is 26 cm, below 20 cm.')
    press('Show the two records')
    expect(page.locator('#feedback')).to_contain_text('Name today’s reading')
    if mode=='elementary':
        press('Hint')
    correction = ('Today it is 16 cm. That is below 20 cm.' if mode=='elementary' else
        'Yesterday the ford was 26 cm. Today it is 16 cm, which is below the limit of 20 cm.')
    page.locator('#notice-correction').fill(correction)
    press('Show the two records')
    expect(page.locator('#panel-kicker')).to_have_text('NOTICE REVISED')
    if AUDIO_PACKAGED:
        voice_replay(button('Replay Ranger Lin'))
    page.screenshot(path=RESULTS / f'{name}-notice-revised.png')
    press('Watch Lin turn the notice')
    pin('Ranger Lin')
    press('Discuss a crossing plan')
    page.locator('#recommend').select_option(route)
    for clue in (['bridge','rack'] if route=='bridge' else ['depth','sign']):
        click(page.locator(f'label:has(input[value="{clue}"])'))
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('Choose an observation')
    expect(page.locator('#panel-title')).to_have_text('Recommend a crossing')
    fact, inference = ('matching-boards', 'fill-sockets') if route == 'bridge' else ('ford-depth','use-shallows')
    page.locator('#claim-fact').select_option(fact)
    page.locator('#claim-link').select_option(inference)
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('Connect your words to the observation you selected')
    nonsense = 'Cat dog tree' if mode == 'elementary' else 'Cat dog tree fish bird'
    page.locator('#draft').fill(nonsense)
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('Connect your words to the observation you selected')
    assert saved()['route'] is None
    page.locator('#claim-fact').select_option('short-boards' if route=='bridge' else 'deep-ford')
    press('Tell Ranger Lin')
    expect(page.locator('#feedback')).to_contain_text('does not match the field notes')
    page.locator('#claim-fact').select_option(fact)
    page.locator('#draft').fill('')
    if mode == 'elementary':
        click(page.get_by_text('Open word bank', exact=True))
        press('I saw')
        expect(page.locator('#draft')).to_have_value('I saw')
    message = 'Two matching ninety-centimetre planks fill the gap.' if route == 'bridge' else 'I measured 16 cm at the ford.'
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
    if AUDIO_PACKAGED:
        voice_replay(page.locator('#field-listen'))
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
    else:
        press('Turn board clockwise')
        choose('place0')
        expect(notice).to_contain_text('Turn the board across')
        assert not saved()['pieces']
        for _ in range(3):
            press('Turn board clockwise')
    expect(page.locator('#panel')).not_to_be_visible()
    page.screenshot(path=RESULTS / f'{name}-physical-carry.png')
    if name=='desktop-bridge':
        # Returning to a save mid-carry leaves the loose board recoverable.
        page.reload()
        expect(layer).to_be_visible()
        expect(page.locator('#field-holding')).to_contain_text('Crossing materials')
        assert not saved()['pieces']
        choose('pick0')
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
    if route=='bridge':
        expect(notice).to_contain_text('Rope hooked')
        if name=='desktop-bridge':
            assert page.evaluate("window.actorDraws.some(entry => entry.asset === 'scout-v4-fit')")
        assert saved()['pieces'] == pieces[:2]
        click(layer.locator('[data-action=tension]'))
        expect(page.locator('#panel-title')).to_have_text('Bridge rigging')
        press('Far cleat')
        expect(page.locator('#feedback')).to_contain_text('Feed the rope')
        press('Outer edge')
        press('Far cleat')
        press('Lock and test')
        expect(page.locator('#feedback')).to_contain_text('rubs the broken edge')
        press('Inner guide')
        press('Lock and test')
        expect(page.locator('#feedback')).to_contain_text('far end is loose')
        press('Far cleat')
        press('Lock and test')
        expect(page.locator('#feedback')).to_contain_text('still moves')
        load = page.locator('#rig-load')
        drive_range(load,.98)
        press('Lock and test')
        expect(page.locator('#feedback')).to_contain_text('strained')
        assert saved()['pieces'] == pieces[:2]
        if touch:
            press('Hint')
        drive_range(load,.67)
        expect(page.locator('#rig-status')).to_contain_text('in the safe band')
        page.screenshot(path=RESULTS / f'{name}-rig.png')
        press('Lock and test')
    if name=='desktop-bridge':
        # Take time to read the modal. The ranger must wait before starting the crossing.
        page.wait_for_timeout(4500)
    clear_draws(page)
    press('Watch the crossing')
    if name=='desktop-bridge':
        page.wait_for_function("""
            new Set(window.actorDraws.filter(entry => /^ranger-v4-(right|left|up|down)-[0-9]+$/
                .test(entry.asset)).map(entry => entry.asset)).size >= 3
        """)
        pin('Ranger Lin')
        expect(page.locator('#panel-title')).to_have_text('Ranger Lin is on the trail')
        press('Back to trail')
        page.wait_for_timeout(4600)
        ranger = drawn_frames(page,'ranger')
        assert {'ranger-v4-inspect','ranger-v4-handoff'}.issubset(ranger), sorted(ranger)
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
    consequence = 'The repaired deck is open.' if route=='bridge' else 'Visitors stay here because only the ford is marked.'
    page.locator('#consequence').fill(consequence)
    with page.expect_download() as pending:
        press('Export progress')
    record = json.loads(Path(pending.value.path()).read_text())
    assert record['languageMode']==mode
    assert record['fieldInstruments']['soundingsCm']=={'bridge':38,'ford':16}
    assert record['safetyInterview']['noticeRevised']
    checks=record['safetyInterview']['attempts']
    assert [attempt['accepted'] for attempt in checks]==[False,False,True]
    assert checks[-1]['note']==correction and checks[-1]['assisted']==(mode=='elementary')
    assert record['observedAnswers']['consequence']['text']==consequence
    trials=record['bridgeLoadTrials']
    if route=='bridge':
        assert [trial['result'] for trial in trials]==['edge','cleat','slack','strain','secure']
        assert trials[-1]['assisted']==touch
    else:
        assert not trials
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
    assert recommendations[-1]['structuredEvidence'] == {'fact':fact, 'inference':inference}
    assert record['selfReportedSpeakingPractice']==['Ranger conversation']
    activities = record['physicalActions']
    assert any(event['action']=='contact-rejected' for event in activities)
    assert any(event['action']=='collected' and event['method']=='guide' and event['assisted'] for event in activities)
    assert [event['piece'] for event in activities if event['action']=='placed']==pieces
    if route=='bridge':
        assert [event['action'] for event in activities if event['action'].startswith('rope-')]==['rope-hooked','rope-tensioned']
    press('Back to trail')
    page.reload()
    expect(page.locator('#objective')).to_have_text('Supplies delivered')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    if touch:
        press('Field log')
        expect(page.locator('.trail-map')).to_be_visible()
        expect(page.locator('.trail-map figcaption')).to_contain_text('You are at')
        page.screenshot(path=RESULTS / f'{name}-trail-map.png')
        press('Close dialog')
    press('Settings')
    press('Sound effects: on')
    press('Sound effects: off')
    press('Voice: on')
    press('Voice: off')
    press('Ambience: on')
    press('Ambience: off')
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
        assert saved()['survey']['corrected'] and saved()['rigTrials'][-1]['result']=='secure'
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

def migrate(browser, version):
    previous_name = f'Broken-Bridge-v{version}.html'
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
    if version=='0.3.0':
        page.locator('#draft').fill('The 90 cm boards fill the gap.')
    if version=='0.5.0':
        page.locator('#claim-fact').select_option('matching-boards')
        page.locator('#claim-link').select_option('fill-sockets')
        page.locator('#draft').fill('The 90 cm boards fill the gap.')
    press('Tell Ranger Lin')
    expect(page.locator('#panel-title')).to_have_text('Crossing authorized')
    press('Back to trail')
    if version=='0.2.0':
        pin('Broken bridge')
        page.locator('[data-action=pick0]').click()
        page.locator('[data-action=place0]').click()
        expect(page.locator('#feedback')).to_contain_text('seated')
    else:
        page.locator('#field-guide').click()
        expect(page.locator('#field-holding')).to_have_text('Carrying first board')
        page.locator('#field-guide').click()
        expect(page.locator('#notice')).to_contain_text('Board seated')

    page.goto(URL,timeout=20000)
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
    expected_source, expected_review = ('legacy-route-selection','not-applicable') if version=='0.2.0' else ('supported-elementary','teacher-review')
    assert legacy['submissionSource'] == expected_source
    assert legacy['languageReview'] == expected_review
    assert record['outcome']['piecesPlaced'] == ['boardA']
    assert not unexpected, unexpected
    context.close()
    print(f'PASS migration: live v{version} partial bridge save into cold v0.6.1; original production classified',flush=True)

def encode_screencast(frames, path, duration):
    # CDP returns real composed screen frames only when the screen changes.
    # Use capture times when encoding so idle pauses and movement keep time.
    assert len(frames) >= 18, f'Insufficient Chrome screencast frames: {len(frames)}'
    with tempfile.TemporaryDirectory(prefix='bridge-clip-') as temp:
        folder = Path(temp)
        manifest = []
        for i, (at, image) in enumerate(frames):
            following = frames[i+1][0] if i+1 < len(frames) else duration
            filename = f'frame-{i:04}.jpg'
            (folder / filename).write_bytes(image)
            manifest.extend((f"file '{filename}'", f'duration {max(.001, following-at):.5f}'))
        manifest.append(f"file '{filename}'")
        timeline = folder / 'timeline.txt'
        timeline.write_text('\n'.join(manifest)+'\n')
        subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',str(timeline),
                        '-t',f'{duration:.4f}','-vf','fps=24','-c:v','libx264','-threads','2','-preset','veryfast',
                        '-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],check=True)

def record_motion(browser,name,viewport,touch):
    context = browser.new_context(viewport=viewport, is_mobile=touch, has_touch=touch,
                                  offline=True, reduced_motion='no-preference')
    external = []

    def serve(request):
        if request.request.url == URL:
            request.fulfill(status=200, body=HTML, content_type='text/html; charset=utf-8')
        elif request.request.url == 'http://127.0.0.1:8127/favicon.ico':
            request.fulfill(status=204)
        else:
            external.append(request.request.url)
            request.abort()

    context.route('**/*', serve)
    observe_actor_draws(context)
    # A legitimate observer fixture starts after bridge authorization. The
    # footage uses actual game input and live Canvas rendering thereafter.
    context.add_init_script(script=f"""
        localStorage.setItem('broken-bridge-v1', {json.dumps(json.dumps({
            'version':1, 'id':f'recording-{name}', 'mode':'elementary',
            'clues':['bridge','rack'], 'question':'Can you help me?', 'route':'bridge',
            'pieces':[], 'x':236, 'y':455 if touch else 481,
        }))});
    """)
    page = context.new_page()
    page.goto(URL,timeout=20000)
    expect(page.locator('.field-layer')).to_be_visible()
    canvas = page.locator('#world canvas')
    expect(canvas).to_be_visible()
    page.locator('#stage').focus()
    session = context.new_cdp_session(page)
    frames = []
    observed = {}
    started = time.monotonic()

    def frame(event):
        frames.append((time.monotonic()-started, base64.b64decode(event['data'])))
        session.send('Page.screencastFrameAck', {'sessionId':event['sessionId']})

    session.on('Page.screencastFrame', frame)
    session.send('Page.startScreencast', {'format':'jpeg','quality':84,'everyNthFrame':2,
                                          'maxWidth':viewport['width'],'maxHeight':viewport['height']})

    def move(direction, milliseconds, action='walk'):
        clear_draws(page)
        if touch:
            box = canvas.bounding_box()
            fractions = (.86,.79,.72) if direction=='right' else (.14,.21,.28)
            points = [[box['x']+box['width']*fraction, box['y']+box['height']*offset]
                      for fraction in fractions for offset in (.81,.77,.74,.70,.68,.64,.60,.56,.52)]
            point = page.evaluate("""points => points.find(([x,y]) =>
                document.elementFromPoint(x,y)?.tagName === 'CANVAS')""", points)
            assert point, 'No unobstructed trail target for touch recording'
            x,y = point
            page.touchscreen.tap(x,y)
            page.wait_for_timeout(milliseconds)
        else:
            key = 'Arrow'+direction.capitalize()
            page.keyboard.down(key)
            page.wait_for_timeout(milliseconds)
            page.keyboard.up(key)
            page.wait_for_timeout(125)
        found = drawn_frames(page,'scout',direction,action)
        minimum = 3 if direction in ('up','down') or touch else 4
        assert len(found) >= minimum, (name,direction,action,sorted(found),sorted(drawn_frames(page,'scout')))
        observed[f'{action}-{direction}'] = sorted(found)

    move('right',1250)
    move('left',1200)
    if not touch:
        move('up',650)
        move('down',650)
    guide = page.locator('#field-guide')
    (guide.tap if touch else guide.click)()
    expect(page.locator('#field-holding')).to_contain_text('first board', ignore_case=True, timeout=8000)
    page.locator('#stage').focus()
    move('right',1400,'carry')
    assert page.evaluate("window.actorDraws.some(entry => entry.asset === 'board' && entry.scoutAction === 'carry')")
    page.screenshot(path=RESULTS / f'{name}-carry.png')
    move('left',900,'carry')
    # Keep the generated file in the requested 10–15 second window, without
    # padding movement with made-up frames.
    page.wait_for_timeout(max(0, 12100-(time.monotonic()-started)*1000))
    duration = time.monotonic()-started
    session.send('Page.stopScreencast')
    assert 10 <= duration <= 15, f'Recorded duration {duration:.2f}s outside target'
    assert not external, external
    encode_screencast(frames,RESULTS / f'{name}.mp4',duration)
    (RESULTS / f'{name}-frames.json').write_text(json.dumps(observed,indent=2)+'\n')
    context.close()
    print(f'PASS {name}: {duration:.2f}s live Chromium screencast; actual sprite draws { {key:len(value) for key,value in observed.items()} }',flush=True)

with ZipFile(BUILD / f'{Path(ARTIFACT).stem}-Offline.zip') as package:
    assert package.testzip() is None
    HTML = package.read(ARTIFACT)
assert HTML == (BUILD / ARTIFACT).read_bytes()
AUDIO_PACKAGED = b'data:audio/mpeg;base64,' in HTML
DRAW_KEYS = {}
for asset, source in re.findall(rb'"([^"]+)":"(data:image/webp;base64,[A-Za-z0-9+/=]+)"', HTML):
    name = asset.decode()
    if name.startswith(('scout-v4-', 'ranger-v4-')) or name=='board':
        signature = f'{len(source)}|{source[-64:].decode()}'
        assert signature not in DRAW_KEYS, f'Duplicate frame texture {name!r}: {DRAW_KEYS.get(signature)}'
        DRAW_KEYS[signature] = name
def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'))
        cases = [
            ('desktop-bridge',{'width':1366,'height':768},False,'elementary','bridge'),
            ('desktop-ford',{'width':1920,'height':1080},False,'middle','ford'),
            ('iphone-portrait-ford',{'width':390,'height':844},True,'elementary','ford'),
            ('iphone-landscape-bridge',{'width':844,'height':390},True,'middle','bridge'),
        ]
        selection = os.getenv('BRIDGE_TEST_CASE')
        selected = [args for args in cases if not selection or selection==args[0]]
        motion_cases = [
            ('motion-desktop',{'width':1366,'height':768},False),
            ('motion-portrait',{'width':390,'height':844},True),
            ('motion-landscape',{'width':844,'height':390},True),
        ]
        motion_selected = [args for args in motion_cases if selection==args[0] or selection=='motion']
        assert selected or motion_selected or selection=='migration', f'Unknown BRIDGE_TEST_CASE {selection!r}'
        for args in selected:
            play(browser,*args)
        if not selection or selection=='migration':
            for version in ('0.2.0','0.3.0','0.5.0'):
                migrate(browser, version)
        for args in motion_selected:
            record_motion(browser,*args)
        browser.close()


if __name__ == '__main__':
    main()
