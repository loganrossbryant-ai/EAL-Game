"""Capture real Chromium frames and an independent tap on the game mixer output."""
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from playwright.sync_api import expect, sync_playwright

from browser import HTML, RESULTS, URL, encode_screencast, observe_actor_draws

PORT = 'http://127.0.0.1:8127/'
AUDIO_TAP = """
(() => {
  const wire = AudioNode.prototype.connect;
  AudioNode.prototype.connect = function (destination, ...args) {
    const result = wire.call(this, destination, ...args);
    if (destination === this.context.destination && !window.gameAudioOutput) {
      const stream = this.context.createMediaStreamDestination();
      const analysis = this.context.createAnalyser();
      analysis.fftSize = 2048;
      wire.call(this, stream);
      wire.call(this, analysis);
      window.gameAudioOutput = {stream, analysis};
    }
    return result;
  };
  window.measureGameSound = async (milliseconds) => {
    if (!window.gameAudioOutput) return 0;
    const node = window.gameAudioOutput.analysis;
    const buffer = new Float32Array(node.fftSize);
    const end = performance.now() + milliseconds;
    let peakRms = 0;
    do {
      node.getFloatTimeDomainData(buffer);
      peakRms = Math.max(peakRms, Math.sqrt(buffer.reduce((s,v) => s+v*v, 0)/buffer.length));
      await new Promise(r => setTimeout(r, 25));
    } while (performance.now() < end);
    return Number(peakRms.toFixed(6));
  };
  window.startGameAudioRecording = () => {
    const recorder = new MediaRecorder(window.gameAudioOutput.stream.stream, {mimeType:'audio/webm;codecs=opus'});
    const data = [];
    recorder.ondataavailable = event => { if (event.data.size) data.push(event.data); };
    recorder.start(180);
    window.finishGameAudioRecording = () => new Promise(resolve => {
      recorder.onstop = () => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(new Blob(data,{type:recorder.mimeType}));
      };
      recorder.stop();
    });
  };
})();
"""

def start_game(browser, save=None, reduced=False, audio=False):
    external = []
    context = browser.new_context(viewport={'width':1366,'height':768}, offline=True,
                                  reduced_motion='reduce' if reduced else 'no-preference')
    def serve(route):
        if route.request.url == URL:
            route.fulfill(status=200, body=HTML, content_type='text/html')
        elif route.request.url == PORT+'favicon.ico':
            route.fulfill(status=204)
        else:
            external.append(route.request.url)
            route.abort()
    context.route('**/*',serve)
    if save:
        context.add_init_script(f"localStorage.setItem('broken-bridge-v1', {json.dumps(json.dumps(save))})")
    if audio:
        context.add_init_script(AUDIO_TAP)
    observe_actor_draws(context)
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(URL)
    page.set_default_timeout(6500)
    expect(page.locator('canvas')).to_be_visible()
    return context,page,external,errors

def press(page,label):
    page.get_by_role('button',name=label,exact=True).click()

def pin(page,label):
    page.locator('#pins').get_by_role('button',name=label,exact=True).click()
    expect(page.locator('#panel')).to_be_visible()

def keys(page,key,hold):
    page.locator('#stage').focus()
    page.keyboard.down(key)
    page.wait_for_timeout(hold)
    page.keyboard.up(key)

def checkpoint(name,x=278,story=False):
    save = {'version':1,'fieldEdition':6,'mode':'middle','id':name,'x':x,'y':449}
    if story:
        save.update(question='Where is the safe crossing?',clues=['bridge','rack','depth','sign'],
                    survey={'readings':{'bridge':38,'ford':16},'compared':True})
    return save

def begin_capture(context,page):
    session=context.new_cdp_session(page)
    frames=[]
    started=time.monotonic()
    def frame(event):
        frames.append((time.monotonic()-started,base64.b64decode(event['data'])))
        session.send('Page.screencastFrameAck',{'sessionId':event['sessionId']})
    session.on('Page.screencastFrame',frame)
    session.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1366,'maxHeight':768})
    return session,frames,started

def finish_capture(session,frames,started,target,seconds):
    duration=time.monotonic()-started
    session.send('Page.stopScreencast')
    assert seconds[0]<=duration<=seconds[1], (target,duration)
    encode_screencast(frames,target,duration)
    return {'duration_s':round(duration,3),'real_frames':len(frames)}

def rest_until(page,started,seconds):
    page.wait_for_timeout(max(0,(seconds-(time.monotonic()-started))*1000))

def readonly_ambience(browser):
    metrics={}
    for reduced in (False,True):
        label='stationary-reduced' if reduced else 'stationary-living'
        context,page,external,errors=start_game(browser,checkpoint(label),reduced=reduced)
        expect(page.locator('#location')).to_have_text('Ranger clearing')
        page.mouse.move(2,2)
        page.screenshot(path=RESULTS/f'{label}.png')
        if reduced:
            frames=[]
            started=time.monotonic()
            for i in range(18):
                rest_until(page,started,i)
                frames.append((time.monotonic()-started,page.screenshot(type='jpeg',quality=88)))
            rest_until(page,started,17.8)
            duration=time.monotonic()-started
            encode_screencast(frames,RESULTS/f'{label}.mp4',duration)
            metrics[label]={'duration_s':round(duration,3),'real_frames':len(frames),'unique_frames':len(set(image for _,image in frames))}
            assert metrics[label]['unique_frames']==1,metrics
        else:
            s,frames,started=begin_capture(context,page)
            rest_until(page,started,17.3)
            metrics[label]=finish_capture(s,frames,started,RESULTS/f'{label}.mp4',(16,20))
            assert len(frames)>60
        result=page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1'))")
        assert (result['x'],result['y'])==(278,449)
        assert not external and not errors,(external,errors)
        context.close()
    (RESULTS/'stationary-evidence.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print('PASS fixed-camera capture and stationary reduced-motion comparison',metrics,flush=True)

def notice_consequence(browser):
    context,page,external,errors=start_game(browser,checkpoint('notice',story=True))
    expect(page.locator('#location')).to_have_text('Ranger clearing')
    capture=begin_capture(context,page)
    pin(page,'Ranger Lin')
    press(page,'Ask about the old ford notice')
    rest_until(page,capture[2],2.2)
    press(page,'When did you check the ford?')
    page.locator('input[name=notice-source][value=log]').check()
    page.locator('input[name=notice-source][value=sounding]').check()
    page.locator('#notice-correction').fill('Today the ford is 16 cm, which is less than 20 cm.')
    rest_until(page,capture[2],7.5)
    press(page,'Show the two records')
    expect(page.locator('#panel-kicker')).to_have_text('NOTICE REVISED')
    page.screenshot(path=RESULTS/'notice-card.png')
    rest_until(page,capture[2],10)
    page.evaluate('window.actorDraws.length=0')
    press(page,'Watch Lin turn the notice')
    page.wait_for_function("window.actorDraws.some(entry => entry.asset === 'ranger-v4-inspect')")
    page.wait_for_function("window.actorDraws.some(entry => entry.asset === 'ranger-v4-handoff')")
    page.screenshot(path=RESULTS/'notice-turn.png')
    rest_until(page,capture[2],16.4)
    metrics=finish_capture(*capture,RESULTS/'notice-consequence.mp4',(15,20))
    assert not external and not errors,(external,errors)
    print('PASS actual notice interview, two ranger poses and result',metrics,flush=True)
    context.close()

def audio_preferences(browser):
    context,page,external,errors=start_game(browser,audio=True,reduced=True)
    press(page,'Middle school · field investigation')
    assert not page.evaluate('Boolean(window.gameAudioOutput)')
    pin(page,'Ranger Lin')
    press(page,'Replay Ranger Lin')
    expect(page.locator('#audio-tip')).to_contain_text('Sound is off')
    assert not page.evaluate('Boolean(window.gameAudioOutput)')
    page.locator('#audio-tip').get_by_role('button',name='Enable sound',exact=True).click()
    page.wait_for_function('Boolean(window.gameAudioOutput)')
    press(page,'Back to trail')
    page.wait_for_timeout(650)
    levels={'ambience_on':page.evaluate('measureGameSound(320)')}
    press(page,'Settings')
    press(page,'Ambience: on')
    press(page,'Voice: on')
    press(page,'Sound effects: on')
    press(page,'Back to trail')
    page.wait_for_timeout(650)
    levels['all_buses_off']=page.evaluate('measureGameSound(320)')
    pin(page,'Ranger Lin')
    press(page,'Replay Ranger Lin')
    expect(page.locator('#audio-tip')).to_contain_text('Voice is off')
    levels['voice_disabled_replay']=page.evaluate('measureGameSound(280)')
    press(page,'Back to trail')
    press(page,'Settings')
    press(page,'Voice: off')
    press(page,'Back to trail')
    pin(page,'Ranger Lin')
    press(page,'Replay Ranger Lin')
    levels['voice_only']=page.evaluate('measureGameSound(1050)')
    press(page,'Back to trail')
    press(page,'Settings')
    press(page,'Sound effects: off')
    press(page,'Back to trail')
    page.locator('#stage').focus()
    old_x=page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1')).x")
    page.keyboard.down('ArrowRight')
    levels['effects_only']=page.evaluate('measureGameSound(970)')
    page.keyboard.up('ArrowRight')
    assert page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1')).x")>old_x+35
    press(page,'Mute sound')
    page.wait_for_timeout(330)
    levels['master_off']=page.evaluate('measureGameSound(300)')
    assert all(levels[id]>.002 for id in ('ambience_on','voice_only','effects_only')),levels
    assert all(levels[id]<.0005 for id in ('all_buses_off','voice_disabled_replay','master_off')),levels
    assert not external and not errors,(external,errors)
    (RESULTS/'audio-mixer.json').write_text(json.dumps(levels,indent=2)+'\n')
    print('PASS opt-in and independent mixer signals',levels,flush=True)
    context.close()

def audible_run(browser):
    save=checkpoint('audible',story=True)
    save.update(route='bridge',pieces=['boardA','boardB'])
    save['survey'].update(asked=True,interview=[
        {'sources':['log','sounding'],'note':'Today it is 16 cm, below 20 cm.'},
    ])
    context,page,external,errors=start_game(browser,save,audio=True)
    page.wait_for_timeout(350)
    capture=begin_capture(context,page)
    press(page,'Enable sound')
    page.wait_for_function('Boolean(window.gameAudioOutput)')
    offset=time.monotonic()-capture[2]
    page.evaluate('startGameAudioRecording()')
    pin(page,'Ranger Lin')
    press(page,'Replay Ranger Lin')
    rest_until(page,capture[2],8.6)
    press(page,'Back to trail')
    keys(page,'ArrowLeft',720)
    page.locator('#field-guide').click()
    expect(page.locator('#field-holding')).to_contain_text('Carrying rope')
    page.locator('#field-guide').click()
    expect(page.locator('#field-holding')).to_contain_text('Rope hooked')
    page.locator('#field-guide').click()
    expect(page.locator('#panel-title')).to_have_text('Bridge rigging')
    press(page,'Inner guide')
    press(page,'Far cleat')
    slider=page.locator('#rig-load')
    box=slider.bounding_box()
    page.mouse.click(box['x']+box['width']*.67,box['y']+box['height']*.5)
    expect(page.locator('#rig-status')).to_contain_text('in the safe band')
    press(page,'Lock and test')
    expect(page.locator('#panel-title')).to_have_text('The bridge is open')
    press(page,'Replay Ranger Lin')
    page.wait_for_timeout(4700)
    press(page,'Watch the crossing')
    rest_until(page,capture[2],24)
    press(page,'Mute sound')
    page.wait_for_timeout(520)
    silence=page.evaluate('measureGameSound(450)')
    assert silence<.0005,silence
    rest_until(page,capture[2],27)
    press(page,'Enable sound')
    page.wait_for_timeout(520)
    output=page.evaluate('measureGameSound(450)')
    assert output>.002,output
    rest_until(page,capture[2],32.0)
    audio=base64.b64decode(page.evaluate('finishGameAudioRecording()'))
    assert len(audio)>30000
    target=RESULTS/'gameplay-with-audio.mp4'
    with tempfile.TemporaryDirectory(prefix='bridge-av-') as tmp:
        work=Path(tmp)
        video=work/'browser.mp4'
        metrics=finish_capture(*capture,video,(29,35))
        track=work/'game-mixer.webm'
        track.write_bytes(audio)
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(video),'-itsoffset',str(round(offset,4)),
            '-i',str(track),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','128k',
            '-af','apad','-shortest','-movflags','+faststart',str(target)],check=True)
    report=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]))
    assert {stream['codec_type'] for stream in report['streams']}=={'video','audio'},report
    assert not external and not errors,(external,errors)
    metrics.update(muted_rms=silence,restored_rms=output,audio_capture_offset_s=round(offset,3))
    (RESULTS/'audio-video-evidence.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print('PASS live screen + mixer output',metrics,flush=True)
    context.close()

if __name__=='__main__':
    runs={'stationary':readonly_ambience,'notice':notice_consequence,'mixer':audio_preferences,'audible':audible_run}
    only=os.environ.get('BRIDGE_EVIDENCE_CASE')
    if only and only not in runs: raise SystemExit(f'Unknown evidence case: {only}')
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'))
        for key,run in runs.items():
            if not only or only==key:run(browser)
        browser.close()
