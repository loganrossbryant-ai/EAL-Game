"""Exercise every vocabulary card through real UI; enforce the Chinese boundary."""
from pathlib import Path
import json, os, math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/expanded-tests';OUT.mkdir(parents=True,exist_ok=True)
VOCAB=json.loads((ROOT/'eal-adventure/data/vocabulary.json').read_text())
BY_ID={v['id']:v for v in VOCAB}
report={'checks':[],'errors':[],'reachable':{},'scene_limits':'Chromium, not physical iOS Safari'}
def check(name,value):
    if not value:page.screenshot(path=str(OUT/'failure.png'))
    assert value,(name,report.get('diagnostic'))
    report['checks'].append(name);print('PASS',name,flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl'])
    page=b.new_page(viewport={'width':960,'height':640})
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
    requests=[];page.on('request',lambda req:requests.append(req.url))
    page.goto(os.environ.get('ALAN_URL','http://127.0.0.1:8092/'))
    page.wait_for_function('window.__alanTest',timeout=60000)
    def snap():return page.evaluate('window.__alanTest')
    def wait(expr):page.wait_for_function('(x)=>{const s=window.__alanTest;return '+expr+'}',timeout=30000)
    def click(text=None,semantic=None):
        matches=[v for v in snap()['buttons'] if not v['disabled'] and (v['semantic']==semantic if semantic is not None else v['text']==text)]
        assert matches,(text,semantic,snap())
        fingerprint="(s)=>JSON.stringify([s.mode,s.modal,s.labels,s.buttons,s.selected,s.quest,s.stage,s.topic,s.room])"
        before=page.evaluate('('+fingerprint+')(window.__alanTest)')
        before_save=page.evaluate("localStorage.getItem('alan-favorites-island-v1')")
        x,y,w,h=matches[-1]['rect'];page.mouse.click((x+w/2)*2/3,(y+h/2)*2/3)
        if text!='Export summary':
            # A mission pool can equal catalogue page one. Its persisted seen
            # counters still prove the press was processed; then await a fresh
            # rendered snapshot, so no test depends on machine frame rate.
            page.wait_for_function('(old)=>('+fingerprint+")(window.__alanTest)!==old.view || localStorage.getItem('alan-favorites-island-v1')!==old.save",arg={'view':before,'save':before_save},timeout=30000)
            current=snap()
            page.wait_for_function("(old)=>{const s=window.__alanTest;return (s.mode||'cafe')!==old.mode || s.tick>old.tick}",arg={'mode':current.get('mode','cafe'),'tick':current['tick']},timeout=30000)
    def modal(name):page.wait_for_function('(x)=>window.__alanTest.modal===x',arg=name,timeout=30000)
    def saved():return page.evaluate("JSON.parse(localStorage.getItem('alan-favorites-island-v1'))")
    def no_chinese(name):
        text='\n'.join(snap().get('labels',[]))
        leaked=[v['en'] for v in VOCAB if v['zh'] in text]
        check(name+' has no target Chinese',not leaked)
        check(name+' has no sentence translation','我最喜欢' not in text and '我叫艾伦' not in text)
    click("Let's go!");click('We said it');modal('')
    click('操作');check('Chinese navigation help can be enabled',saved()['settings']['chinese'])
    food_seen=set()
    for label in ['Meals','Fruit','Kitchen']:
        click(label);modal('menu')
        for _ in range(2):
            food_seen.update(x['semantic'][5:] for x in snap()['buttons'] if x['semantic'].startswith('food:'))
            no_chinese(label+' counter');click('More food')
        click('Close');modal('')
    report['diagnostic']={'food_seen':sorted(food_seen)}
    check('All eighteen foods are reachable in the café',food_seen=={v['en'] for v in VOCAB if v['topic']=='food'})
    report['reachable']['food']=sorted(food_seen)
    click('Album');modal('album');album_seen=set()
    for _ in range(5):
        album_seen.update(x['semantic'][9:] for x in snap()['buttons'] if x['semantic'].startswith('favorite:'))
        no_chinese('Personal album');click('More foods')
    check('Personal album includes every food, not the eight old recordings',album_seen==food_seen)
    for _ in range(5):
        if any(x['semantic']=='favorite:watermelon' for x in snap()['buttons']):break
        click('More foods')
    click(semantic='favorite:watermelon');modal('favorite');no_chinese('New personal sentence')
    check('Unrecorded new word is not falsely marked as heard',saved()['words']['watermelon']['heard']==0)
    check('No silent replay button for an unrecorded sentence',not any('Replay' in x['text'] or 'Hear “' in x['text'] for x in snap()['buttons']))
    click('Close');modal('')
    click('Mina');modal('resident');no_chinese('NPC order');click("I'll find it!")
    click('Meals');modal('menu');click(semantic='food:pizza')
    click('Mina');modal('resident');click('Give pizza');modal('sentence');check('Navigation Chinese does not count as a vocabulary answer hint',not saved()['tasks'][-1]['hinted']);no_chinese('Café sentence building')
    for text in ['My favorite','food','is','pizza.']:click(text)
    click('Check sentence');modal('speak');click('We said it');modal('album')
    chosen=next(x['semantic'] for x in snap()['buttons'] if x['semantic'].startswith('favorite:'))
    click(semantic=chosen);modal('favorite');click('Close');modal('')
    click('Festival');modal('festival');check('Café still contributes its festival stamp','food' in saved()['festival_stamps'])
    click('See our table');modal('');click('Island trail');wait("s.mode==='trail' && s.room===''")
    page.screenshot(path=str(OUT/'01-island.png'))
    routes=[('Animal sanctuary','sanctuary',['animals'],'Ari'),('Sports park','park',['sports','activities'],'Max'),('Story square','story',['entertainment','people'],'Luna'),('Art garden','garden',['colors','places'],'Zoe')]
    for place,room,topics,npc in routes:
        click(place);page.wait_for_function('(v)=>window.__alanTest.room===v',arg=room,timeout=30000)
        page.screenshot(path=str(OUT/(room+'-world.png')))
        for topic in topics:
            if snap()['topic']!=topic:click(topic.capitalize());modal('request')
            else:click(npc);modal('request')
            target=snap()['quest']['target'];entry=BY_ID[target]
            no_chinese(topic+' resident request')
            check(topic+' starts with vocabulary beyond the old café',entry['topic']==topic and entry['en'] in ['dolphin','badminton','drawing','puppet show','firefighter','silver','aquarium'])
            click("I'll help!");modal('');click('Picture shelf');modal('shelf')
            first=[v['semantic'][8:] for v in snap()['buttons'] if v['semantic'].startswith('collect:')]
            check(topic+' mission presents a small round containing its answer',len(first)==4 and target in first)
            seen=set(first)
            for _ in range(6):
                no_chinese(topic+' shelf')
                seen.update(v['semantic'][8:] for v in snap()['buttons'] if v['semantic'].startswith('collect:'))
                click('More pictures')
            expected={v['id'] for v in VOCAB if v['topic']==topic}
            check(topic+' has eighteen actually reachable illustrated cards',seen==expected)
            report['reachable'][topic]=sorted(seen)
            click('Picture + word');modal('word');no_chinese(topic+' English matching')
            click(semantic='answer:'+target);click('Back to the shelf');modal('shelf')
            click('Translation game');modal('translation')
            check(topic+' Chinese appears inside the explicit translation game',entry['zh'] in '\n'.join(snap()['labels']))
            click(semantic='answer:'+target);click('Back to the shelf');modal('shelf');no_chinese(topic+' after leaving translation')
            if topic=='animals':
                wrong=next(v['semantic'] for v in snap()['buttons'] if v['semantic'].startswith('collect:') and v['semantic']!='collect:'+target)
                click(semantic=wrong);modal('');click(npc);modal('request');click('Give the picture')
                check('Wrong new-topic delivery gives a gentle retry',snap()['quest']['stage']==1)
                no_chinese('New-topic retry feedback');click('Close');modal('');click('Picture shelf');modal('shelf')
            click(semantic='collect:'+target);modal('')
            click(npc);modal('request');click('Give the picture');modal('build');check(topic+' translation support is recorded honestly',saved()['tasks'][-1]['hinted']);no_chinese(topic+' sentence building')
            if topic=='animals':
                for chunk in reversed(entry['chunks']):click(chunk)
                click('Check sentence')
                check('New-topic sentence order is actually checked',snap()['quest']['stage']==2)
                click('Start again')
            for chunk in entry['chunks']:click(chunk)
            click('Check sentence');modal('personal');no_chinese(topic+' personal choices')
            count=len(saved()['tasks'])
            favorite=next(v['semantic'] for v in snap()['buttons'] if v['semantic'].startswith('favorite:'))
            click(semantic=favorite);modal('speaking');no_chinese(topic+' spoken sentence')
            check(topic+' personal preference is never scored',len(saved()['tasks'])==count)
            click('We said it');modal('finished')
            check(topic+' mission adds a visible saved festival contribution',topic in saved()['festival_stamps'] and target in saved()['topic_quests'][topic]['completed'])
            click('See the display');modal('');page.screenshot(path=str(OUT/(topic+'-complete.png')))
            click(npc);modal('finished');click('Another request');modal('request')
            check(topic+' replay advances the full eighteen-word cycle',snap()['quest']['target']!=target and snap()['quest']['round']==1)
            click('Close');modal('')
        click('Island path');wait("s.room===''")
    click('Stamps');modal('passport')
    check('All eight topic missions reach the festival ending',len(saved()['festival_stamps'])==8 and 'All eight festival teams are ready!' in snap()['labels'])
    page.screenshot(path=str(OUT/'festival-passport.png'))
    check('All 144 agreed words were reached through real controls',sum(len(x) for x in report['reachable'].values())==144)
    page.reload();page.wait_for_function('window.__alanTest',timeout=60000)
    click("Let's go!");modal('');click('Island trail');wait("s.mode==='trail' && s.room===''")
    check('Eight contributions and Chinese policy survive a reload',len(saved()['festival_stamps'])==8 and saved()['settings']['chinese'])
    click('Café');wait("s.mode!=='trail'");click('Menu');modal('settings');click('Teacher');modal('teacher')
    with page.expect_download() as d:click('Export summary')
    d.value.save_as(str(OUT/'progress.json'))
    check('No browser or Godot errors',not report['errors'])
    check('No external runtime dependencies',all(x.startswith('http://127.0.0.1:8092') or x.startswith('blob:') for x in requests))
    (OUT/'expanded-report.json').write_text(json.dumps(report,indent=2))
    b.close()
print('COMPLETED',len(report['checks']),'checks; 144 reachable words',flush=True)
