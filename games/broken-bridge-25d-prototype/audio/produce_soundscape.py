"""Render original Alder River ambience and foley to local, loopable mono WAVs."""
import hashlib
import json
from pathlib import Path
import wave

import numpy as np

RATE = 22050
OUT = Path(__file__).resolve().parent / 'world'
rng = np.random.default_rng(3065)


def time(seconds):
    return np.arange(round(seconds * RATE)) / RATE


def band(seconds, low, high):
    count = round(seconds * RATE)
    source = np.fft.rfft(rng.standard_normal(count))
    f = np.fft.rfftfreq(count, 1 / RATE)
    highpass = (f / low)**2 / (1 + (f / low)**2)
    lowpass = 1 / (1 + (f / high)**3)
    signal = np.fft.irfft(source * highpass * lowpass, n=count)
    return signal / max(signal.std(), .001)


def pulse(seconds, low, high, tail):
    t = time(seconds)
    return band(seconds, low, high) * (1 - np.exp(-t * 310)) * np.exp(-t / tail)


def resonant(seconds, partials, tail, slide=0):
    t = time(seconds)
    phase = t + slide * t**2
    return sum(weight * np.sin(2 * np.pi * key * phase) for key, weight in partials) * (
        1 - np.exp(-t * 190)) * np.exp(-t / tail)


def add(track, source, at, gain=1):
    indexes = (np.arange(len(source)) + round(at * RATE)) % len(track)
    track[indexes] += source * gain


def river():
    duration = 18
    t = time(duration)
    rush = band(duration, 150, 2450) * (.62 + .12 * np.sin(2 * np.pi * 4 * t / duration))
    flow = band(duration, 66, 620) * .76 + rush
    for at in rng.uniform(0, duration, 220):
        add(flow, pulse(.065, 550, 4200, .017), at, rng.uniform(.035, .17))
    return flow


def breeze():
    duration = 16
    t = time(duration)
    gusts = .5 + .24 * np.sin(2 * np.pi * t / duration) + .15 * np.sin(6 * np.pi * t / duration)
    return gusts * (.8 * band(duration, 55, 310) + .32 * band(duration, 560, 3850))


def wildlife():
    track = time(22) * 0
    for at, pitch in [(2.7,2300),(2.96,2260),(3.22,2520),(8.9,2850),(14.1,2110),(14.5,2380),(19,2710)]:
        t = time(.22)
        sweep = 2 * np.pi * (pitch * t + 790 * t**2 + 180 * t**3)
        call = (np.sin(sweep) + .21 * np.sin(2.01 * sweep)) * np.sin(np.pi * t / .22)**3
        add(track, call, at, .7)
        add(track, call, at + .067, .17)
    return track + band(22, 2200, 4300) * .032


def cabin():
    duration = 14
    track = band(duration, 48, 380) * .24 + band(duration, 140, 1100) * .115
    for at in (1.2, 4.8, 8.1, 11.6):
        add(track,resonant(.52,[(96,.4),(156,.6),(228,.25)],.19,-.105),at,.6)
        add(track,pulse(.29,240,1750,.09),at+.05,.32)
    return track


def foot(surface, variation):
    spec = {
        'gravel': (440, 4100, [(83,.48),(136,.30)], .11),
        'wood': (155, 1390, [(114,.81),(197,.52),(307,.22)], .12),
        'stone': (600, 3600, [(239,.48),(389,.24)], .075),
    }
    low, high, partials, tail = spec[surface]
    stomp = .64 * pulse(.28,low,high,tail*.52) + resonant(.28,partials,tail)
    for at in (.013,.055,.083,.117):
        add(stomp,pulse(.045,low*1.2,high*1.4,.013),at+variation*.007,rng.uniform(.12,.49))
    return stomp


def foley():
    board_up = .38 * pulse(.49,310,2550,.16) + resonant(.49,[(112,.72),(225,.32)],.105,.08)
    board_set = .42 * pulse(.46,245,3150,.067) + resonant(.46,[(84,1),(151,.6),(482,.14)],.18)
    add(board_set,pulse(.16,160,1200,.049),.075,.6)
    rope = .77 * pulse(.64,370,3600,.17)
    add(rope,resonant(.26,[(266,.33),(520,.45),(830,.31)],.055),.24)
    tension = band(.92,170,870) * np.sin(np.pi*time(.92)/.92)**3 * .40
    add(tension,resonant(.41,[(127,.66),(236,.31),(389,.21)],.125,-.12),.38,.6)
    add(tension,pulse(.12,800,2900,.027),.76,.75)
    creak = resonant(1.05,[(76,.68),(149,.3),(355,.06)],.42,-.12)
    creak += band(1.05,160,1260) * np.sin(np.pi*time(1.05)/1.05)**2 * .31
    splash = pulse(.65,420,5400,.12)
    add(splash,pulse(.32,260,2200,.09),.035,.85)
    cloth = pulse(.62,325,2850,.16)
    add(cloth,resonant(.25,[(107,.68),(189,.15)],.08),.27,.72)
    strike = pulse(.43,445,3000,.091) + resonant(.43,[(256,.60),(606,.33),(879,.09)],.135)
    notice = .54*pulse(.6,280,2850,.15) + resonant(.6,[(147,.78),(347,.23),(686,.1)],.147,-.056)
    return {'board-pickup':board_up,'board-place':board_set,'rope-handle':rope,
            'rope-tension':tension,'bridge-creak':creak,'splash':splash,
            'gear-handoff':cloth,'probe-contact':strike,'notice-turn':notice}


def main():
    OUT.mkdir(exist_ok=True)
    loops = {'river':river(),'breeze':breeze(),'wildlife':wildlife(),'cabin':cabin()}
    cues = {f'step-{surface}-{index+1}':foot(surface,index)
            for surface in ('gravel','wood','stone') for index in range(3)}
    cues.update(foley())
    clips = {}
    for name,signal in {**loops,**cues}.items():
        if name not in loops:
            signal *= np.minimum(1,np.minimum(np.arange(len(signal)),np.arange(len(signal))[::-1]) / (.012*RATE))
        ceiling = .72 if name in loops else .90
        pcm = np.round(np.tanh(signal*.82) / max(np.max(np.abs(np.tanh(signal*.82))), .001)*ceiling*32767)
        output = OUT / f'{name}.wav'
        with wave.open(str(output), 'wb') as w:
            w.setparams((1,2,RATE,0,'NONE','not compressed'))
            w.writeframes(pcm.astype('<i2').tobytes())
        clips[name] = {'file':output.name,'loop':name in loops,'seconds':round(len(signal)/RATE,3),
                       'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    manifest = {'origin':'Original offline DSP synthesis and authored foley layers for The Broken Bridge',
                'source':'../produce_soundscape.py','format':'Mono PCM WAV, 22050 Hz, 16-bit',
                'license':'Original project audio, distributable with this game', 'clips':clips}
    (OUT / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__ == '__main__':
    main()
