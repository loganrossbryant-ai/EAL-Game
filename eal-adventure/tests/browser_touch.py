from pathlib import Path
import json,math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/alan-tests'
results=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl'])
    for name,width,height in [('ipad-landscape',1024,768),('iphone-landscape',844,390),('ipad-portrait',768,1024)]:
        context=b.new_context(viewport={'width':width,'height':height},has_touch=True,device_scale_factor=1,is_mobile=True)
        page=context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('http://127.0.0.1:8072/')
        page.wait_for_function('window.__alanTest',timeout=60000)
        scale=min(width/1440,height/960)
        ox=(width-1440*scale)/2;oy=(height-960*scale)/2
        def tap(text):
            buttons=page.evaluate('window.__alanTest.buttons')
            r=[v['rect'] for v in buttons if v['text']==text][-1]
            page.touchscreen.tap(ox+(r[0]+r[2]/2)*scale,oy+(r[1]+r[3]/2)*scale)
            page.wait_for_timeout(400)
        tap("Let's go!");tap('We said it')
        assert page.evaluate('window.__alanTest.modal')==''
        page.screenshot(path=str(OUT/(name+'.png')))
        page.touchscreen.tap(ox+660*scale,oy+660*scale);page.wait_for_timeout(1700)
        assert math.dist(page.evaluate('window.__alanTest.position'),[660,660])<15
        tap('Mina');page.wait_for_function("window.__alanTest.modal==='resident'",timeout=10000)
        tap('中文')
        assert page.evaluate("JSON.parse(localStorage.getItem('alan-favorites-island-v1')).settings.chinese")
        page.screenshot(path=str(OUT/(name+'-dialogue.png')))
        assert not errors,errors
        results.append({'device':name,'touch_move':True,'touch_interact':True,'chinese_reveal':True,'errors':errors})
        print('PASS',name,flush=True)
        context.close()
    b.close()
(OUT/'touch-report.json').write_text(json.dumps({'emulation':'Chromium viewport and touch emulation, not physical iOS Safari','results':results},indent=2))
