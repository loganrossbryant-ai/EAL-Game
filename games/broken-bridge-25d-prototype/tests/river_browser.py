"""Inspect the surface in the actual offline build with the camera parked."""
import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from browser import HTML, RESULTS, URL
from evidence import begin_capture, finish_capture, rest_until

TRACE = """
(() => {
  const textures = new WeakSet();
  const stats = {updates:0, draws:0, strokes:0};
  window.riverTrace = stats;
  const originalUpload = CanvasRenderingContext2D.prototype.putImageData;
  CanvasRenderingContext2D.prototype.putImageData = function(image, ...args) {
    if (image.width > 800 && image.height > 100 && image.height < 225) {
      textures.add(this.canvas);
      stats.updates++;
    }
    return originalUpload.call(this, image, ...args);
  };
  const originalDraw = CanvasRenderingContext2D.prototype.drawImage;
  CanvasRenderingContext2D.prototype.drawImage = function(image, ...args) {
    if (textures.has(image) && this.canvas.closest('#world')) stats.draws++;
    return originalDraw.call(this, image, ...args);
  };
  const originalStroke = CanvasRenderingContext2D.prototype.stroke;
  CanvasRenderingContext2D.prototype.stroke = function(...args) {
    if (this.canvas.closest('#world')) stats.strokes++;
    return originalStroke.apply(this,args);
  };
})();
"""

# These sample boxes are within two reaches of the original painting and
# within the exposed face of the large rock. The desktop camera fits 1060
# world units across the canvas and its bottom edge is at world y=540.
SAMPLES = {
    'reflection': [232,318,19,9],
    'current': [679,353,34,13],
    'rock': [595,337,24,11],
    'far_bank': [712,296,35,8],
}
VIEWPORTS = (
    ('desktop',1366,768,False,278),
    ('phone-portrait',390,844,True,701),
    ('phone-landscape',844,390,True,950),
)

def launch(browser, html, name, width, height, touch, x, reduced=False):
    context = browser.new_context(viewport={'width':width,'height':height}, offline=True,
        is_mobile=touch, has_touch=touch, reduced_motion='reduce' if reduced else 'no-preference')
    external = []
    def serve(route):
        if route.request.url==URL:
            route.fulfill(body=html,content_type='text/html')
        elif route.request.url.endswith('/favicon.ico') and route.request.url.startswith('http://127.0.0.1:8127/'):
            route.fulfill(status=204)
        else:
            external.append(route.request.url)
            route.abort()
    context.route('**/*',serve)
    context.add_init_script(TRACE)
    checkpoint = {'version':1,'fieldEdition':6,'id':'river-'+name,'mode':'middle','x':x,'y':449}
    context.add_init_script(f"localStorage.setItem('broken-bridge-v1',{json.dumps(json.dumps(checkpoint))})")
    page = context.new_page()
    errors = []
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(URL)
    expect(page.locator('#world canvas')).to_be_visible()
    page.mouse.move(6,6)
    page.wait_for_timeout(500)
    return context,page,external,errors

def scene_samples(page):
    return page.evaluate("""samples => {
      const canvas = document.querySelector('#world canvas');
      const ctx = canvas.getContext('2d');
      const zoom = canvas.width / 1060;
      return Object.fromEntries(Object.entries(samples).map(([name,[x,y,w,h]]) => {
        const pixels = ctx.getImageData(Math.round(x*zoom),canvas.height-Math.round((540-y)*zoom),
          Math.round(w*zoom),Math.round(h*zoom));
        return [name, Array.from(pixels.data)];
      }));
    }""",SAMPLES)

def changed_pixels(first,second):
    differences = {}
    for label,values in first.items():
        after = second[label]
        differences[label] = sum(
            max(abs(values[pos+channel]-after[pos+channel]) for channel in range(3))>=4
            for pos in range(0,len(values),4)
        )
    return differences

def observe(browser, html, view, name, *, reduced=False, record=False):
    context,page,external,errors = launch(browser,html,*view,reduced=reduced)
    start = page.evaluate('({...window.riverTrace})')
    if view[0]=='desktop':
        first = scene_samples(page)
    cadence = page.evaluate("""() => new Promise(resolve => {
        const intervals = [];
        const start = performance.now();
        let last;
        const frame = timestamp => {
          if (last!==undefined) intervals.push(timestamp-last);
          last=timestamp;
          if (timestamp-start < 1480) requestAnimationFrame(frame);
          else resolve(intervals.sort((a,b) => a-b));
        };
        requestAnimationFrame(frame);
    })""")
    end = page.evaluate('({...window.riverTrace})')
    result = {key:end[key]-start[key] for key in start}
    result['raf_p95_ms'] = round(cadence[int((len(cadence)-1)*.95)],2)
    if view[0]=='desktop':
        result['changed_pixels'] = changed_pixels(first,scene_samples(page))
    page.screenshot(path=RESULTS/f'river-{name}.png')
    if record:
        clip = begin_capture(context,page)
        rest_until(page,clip[2],15.3)
        result['video'] = finish_capture(*clip,RESULTS/f'river-{name}.mp4',(15,20))
    assert not external and not errors,(external,errors)
    context.close()
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-html',type=Path)
    parser.add_argument('--record',action='store_true')
    args = parser.parse_args()
    measures = {}
    with sync_playwright() as tools:
        browser = tools.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'))
        if args.baseline_html:
            measures['prior-desktop'] = observe(browser,args.baseline_html.read_bytes(),VIEWPORTS[0],'prior-desktop',
                record=args.record)
        for view in VIEWPORTS:
            name=view[0]
            data = observe(browser,HTML,view,name,record=args.record and name=='desktop')
            measures[name]=data
            assert data['strokes']==0 and data['updates']>=10 and data['draws']>=10,(name,data)
        surface = measures['desktop']['changed_pixels']
        assert surface['reflection']>=30 and surface['current']>=30,surface
        assert surface['rock']==0 and surface['far_bank']==0,surface
        reduced = observe(browser,HTML,VIEWPORTS[0],'reduced-desktop',reduced=True)
        measures['reduced-desktop'] = reduced
        assert reduced['updates']==0 and reduced['draws']==0 and not any(reduced['changed_pixels'].values()),reduced
        browser.close()
    (RESULTS/'river-checks.json').write_text(json.dumps(measures,indent=2)+'\n')
    print('PASS offline desktop and both phone sizes, textured surface, fixed rock and bank samples, reduced motion')
    print(json.dumps(measures,indent=2))

if __name__=='__main__':
    main()
