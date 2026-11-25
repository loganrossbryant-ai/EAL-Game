"""Verify live audio routing, slider behaviour and optional music in the offline build."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from playwright.sync_api import expect, sync_playwright

from browser import RESULTS
from evidence import begin_capture, checkpoint, finish_capture, pin, press, rest_until, start_game

# The tap is installed by the test browser. It follows the real graph back from
# the final compressor so measurements include the per-channel gain and ducking.
BUS_TRACE = """
(() => {
  const wires = new Map();
  const analyserByBus = new Map();
  const connect = AudioNode.prototype.connect;
  AudioNode.prototype.connect = function(destination, ...args) {
    if (destination instanceof AudioNode) wires.set(this, destination);
    return connect.call(this, destination, ...args);
  };
  const origin = (channel) => Array.from(wires.keys()).reverse().find(node => {
    if (channel==='voice') return node instanceof MediaElementAudioSourceNode;
    if (!(node instanceof AudioBufferSourceNode) || !node.buffer) return false;
    if (channel==='effects') return !node.loop;
    return node.loop && (channel==='music' ? node.buffer.duration > 30 : node.buffer.duration < 30);
  });
  window.hasSoundBus = channel => Boolean(origin(channel));
  function sampleNode(channel) {
    let node=origin(channel), previous;
    for(let index=0; node&&index<12; index++){
      const next=wires.get(node);
      if (next instanceof DynamicsCompressorNode) {
        if (!analyserByBus.has(previous)) {
          const analyser=node.context.createAnalyser();
          analyser.fftSize=2048;
          connect.call(previous,analyser);
          analyserByBus.set(previous,analyser);
        }
        return analyserByBus.get(previous);
      }
      previous=node;
      node=next;
    }
    return null;
  }
  window.soundRms = async ({channels, milliseconds}) => {
    const buses=channels.map(channel => sampleNode(channel));
    const samples=channels.map(() => new Float32Array(2048));
    const totals=channels.map(() => 0);
    let count=0;
    const end=performance.now()+milliseconds;
    do {
      for(let i=0;i<buses.length;i++){
        if(!buses[i])continue;
        buses[i].getFloatTimeDomainData(samples[i]);
        totals[i]+=samples[i].reduce((sum,value)=>sum+value*value,0)/samples[i].length;
      }
      count++;
      await new Promise(resolve=>setTimeout(resolve,30));
    } while(performance.now()<end);
    return Object.fromEntries(channels.map((channel,i)=>[channel,Number(Math.sqrt(totals[i]/count).toFixed(6))]));
  };
})();
"""
LEVELS = {
    'master':'Master volume','voice':'Voice volume','ambience':'Ambience volume',
    'effects':'Sound effects volume','music':'Music volume',
}


def rms(page, channels, milliseconds=620):
    return page.evaluate('soundRms', {'channels':channels,'milliseconds':milliseconds})


def save_data(page):
    return page.evaluate("JSON.parse(localStorage.getItem('broken-bridge-v1'))")


def known_level(page, channel, value):
    page.get_by_role('slider',name=LEVELS[channel],exact=True).evaluate("""(control, value) => {
        control.value=value;
        control.dispatchEvent(new Event('input',{bubbles:true}));
        control.dispatchEvent(new Event('change',{bubbles:true}));
    }""",value)


def rangers_mixer(browser, baseline=None):
    options={'html':baseline} if baseline is not None else {}
    context,page,external,errors=start_game(browser,checkpoint('mix-assessment'),audio=True,
        reduced=True,audio_trace=BUS_TRACE,**options)
    press(page,'Enable sound')
    page.wait_for_function("hasSoundBus('ambience')")
    assert not page.evaluate("hasSoundBus('music')")
    pin(page,'Ranger Lin')
    page.wait_for_timeout(720)
    idle = rms(page,['ambience'])
    press(page,'Replay Ranger Lin')
    page.wait_for_function("hasSoundBus('voice')")
    page.wait_for_timeout(550)
    during = rms(page,['ambience','voice'],1200)
    page.wait_for_timeout(3800)
    restored = rms(page,['ambience'])
    assert not external and not errors,(external,errors)
    context.close()
    return {'idle':idle,'dialogue':during,'after_dialogue':restored}


def adjust_mixer(browser):
    # Start without a seeded save so a genuine reload exercises persistence.
    context,page,external,errors=start_game(browser,audio=True,reduced=True,audio_trace=BUS_TRACE)
    press(page,'Elementary · supported English')
    assert not page.evaluate('Boolean(window.gameAudioOutput)')
    press(page,'Enable sound')
    page.wait_for_function("hasSoundBus('ambience')")
    press(page,'Settings')
    expect(page.get_by_role('button',name='Music: off',exact=True)).to_be_visible()
    for channel,label in LEVELS.items():
        expect(page.get_by_role('slider',name=label,exact=True)).to_have_value(str(save_data(page)['sound']['volumes'][channel]))
    assert not page.evaluate("hasSoundBus('music')")

    press(page,'Music: off')
    page.wait_for_function("hasSoundBus('music')")
    page.wait_for_timeout(430)
    music_enabled = rms(page,['music'])['music']
    assert music_enabled>.004,music_enabled

    # Zero and restore the faders while listening. Use Home/End on native
    # ranges and also test specific saved percentages with input/change events.
    music=page.get_by_role('slider',name='Music volume',exact=True)
    music.press('Home')
    expect(music).to_have_attribute('aria-valuetext','0%')
    page.wait_for_timeout(350)
    assert rms(page,['music'])['music']<.0005
    known_level(page,'music',40)
    known_level(page,'ambience',0)
    page.wait_for_timeout(340)
    assert rms(page,['ambience'])['ambience']<.0005
    known_level(page,'ambience',30)
    known_level(page,'effects',38)

    master=page.get_by_role('slider',name='Master volume',exact=True)
    master.press('Home')
    page.wait_for_timeout(330)
    assert page.evaluate('measureGameSound(350)')<.0005
    known_level(page,'master',65)
    assert page.evaluate('measureGameSound(460)')>.002

    known_level(page,'voice',0)
    press(page,'Preview Ranger Lin')
    expect(page.locator('#audio-tip')).to_contain_text('volume is at 0%')
    known_level(page,'voice',75)
    page.wait_for_timeout(420)
    no_voice=rms(page,['music','ambience'])
    press(page,'Preview Ranger Lin')
    page.wait_for_function("hasSoundBus('voice')")
    page.wait_for_timeout(550)
    with_voice=rms(page,['music','ambience','voice'],1000)
    assert with_voice['voice']>5*max(with_voice['ambience'],with_voice['music']),with_voice
    assert with_voice['music']<.45*no_voice['music'],(no_voice,with_voice)
    assert with_voice['ambience']<.45*no_voice['ambience'],(no_voice,with_voice)
    page.locator('#panel').get_by_role('button',name='Mute sound',exact=True).click()
    page.wait_for_timeout(330)
    assert page.evaluate('measureGameSound(300)')<.0005
    expected = save_data(page)['sound']
    assert expected['music'] is True and expected['enabled'] is False
    assert expected['volumes']=={'master':65,'voice':75,'ambience':30,'effects':38,'music':40},expected
    page.reload()
    press(page,'Settings')
    for channel,label in LEVELS.items():
        expect(page.get_by_role('slider',name=label,exact=True)).to_have_value(str(expected['volumes'][channel]))
    expect(page.get_by_role('button',name='Music: on',exact=True)).to_be_visible()
    assert not page.evaluate('Boolean(window.gameAudioOutput)')
    page.screenshot(path=RESULTS/'audio-mixer-desktop.png')
    assert not external and not errors,(external,errors)
    context.close()
    return {'music_enabled':music_enabled,'music_and_ambience':no_voice,
            'dialogue_with_music_enabled':with_voice,'reloaded_sound_settings':expected}


def touch_mixer(browser):
    for name,width,height in [('portrait',390,844),('landscape',844,390)]:
        context,page,external,errors=start_game(browser,checkpoint('audio-'+name),reduced=True,
            viewport={'width':width,'height':height},touch=True)
        page.get_by_role('button',name='Settings',exact=True).tap()
        master=page.get_by_role('slider',name='Master volume',exact=True)
        master.tap(position={'x':55,'y':22})
        expect(master).not_to_have_value('100')
        expect(master).to_have_attribute('aria-valuetext',master.input_value()+'%')
        music=page.get_by_role('button',name='Music: off',exact=True)
        music.tap()
        expect(page.get_by_role('button',name='Music: on',exact=True)).to_be_visible()
        assert save_data(page)['sound']['music'] is True
        assert page.evaluate("document.querySelector('#panel').scrollWidth <= document.querySelector('#panel').clientWidth")
        assert master.bounding_box()['height']>=44
        assert page.get_by_role('button',name='Music: on',exact=True).bounding_box()['height']>=44
        page.screenshot(path=RESULTS/f'audio-mixer-{name}.png')
        assert not external and not errors,(external,errors)
        context.close()


def record_audio(browser):
    context,page,external,errors=start_game(browser,checkpoint('audio-review'),audio=True,reduced=False)
    press(page,'Enable sound')
    page.wait_for_function('Boolean(window.gameAudioOutput)')
    capture=begin_capture(context,page)
    offset=time.monotonic()-capture[2]
    page.evaluate('startGameAudioRecording()')
    rest_until(page,capture[2],1.7)
    press(page,'Settings')
    press(page,'Music: off')
    rest_until(page,capture[2],4.5)
    press(page,'Preview Ranger Lin')
    rest_until(page,capture[2],9.5)
    press(page,'Back to trail')
    pin(page,'Ranger Lin')
    press(page,'Replay Ranger Lin')
    rest_until(page,capture[2],17.2)
    press(page,'Back to trail')
    rest_until(page,capture[2],19)
    audio=base64.b64decode(page.evaluate('finishGameAudioRecording()'))
    with tempfile.TemporaryDirectory(prefix='alder-river-mix-') as tmp:
        folder=Path(tmp)
        video,track=folder/'capture.mp4',folder/'browser-mix.webm'
        info=finish_capture(*capture,video,(18,23))
        track.write_bytes(audio)
        output=RESULTS/'audio-mixer-preview.mp4'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(video),'-itsoffset',str(round(offset,4)),
            '-i',str(track),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','128k',
            '-af','apad','-shortest','-movflags','+faststart',str(output)],check=True)
    report=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(output)]))
    assert {stream['codec_type'] for stream in report['streams']}=={'video','audio'}
    assert not external and not errors,(external,errors)
    context.close()
    return info


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-html',type=Path)
    parser.add_argument('--record',action='store_true')
    args=parser.parse_args()
    evidence={}
    with sync_playwright() as tools:
        browser=tools.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'))
        revised=rangers_mixer(browser)
        evidence['revised']=revised
        assert revised['dialogue']['ambience']<.38*revised['idle']['ambience'],revised
        assert revised['after_dialogue']['ambience']>.55*revised['idle']['ambience'],revised
        assert revised['dialogue']['voice']>5*revised['dialogue']['ambience'],revised
        if args.baseline_html:
            prior=rangers_mixer(browser,args.baseline_html.read_bytes())
            evidence['prior']=prior
            assert revised['idle']['ambience']<.42*prior['idle']['ambience'],(prior,revised)
        evidence['controls']=adjust_mixer(browser)
        touch_mixer(browser)
        if args.record:evidence['capture']=record_audio(browser)
        browser.close()
    (RESULTS/'audio-mixer-review.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('PASS voice priority, master and channel volumes, opt-in music, audio persistence and both touch layouts')
    print(json.dumps(evidence,indent=2))


if __name__=='__main__':
    main()
