"""Render the original Alder River music loop without external recordings."""
import hashlib
import json
from pathlib import Path
import wave

import numpy as np

RATE = 22050
BEAT = 60 / 57.6
OUT = Path(__file__).parent / 'music'
RNG = np.random.default_rng(1602)


def pitch(note):
    return 440 * 2 ** ((note - 69) / 12)


def times(seconds):
    return np.arange(round(seconds * RATE)) / RATE


def filtered_breath(t, low, high):
    frequencies = np.fft.rfftfreq(t.size, d=1 / RATE)
    slope = frequencies / low
    window = slope**2 / (1 + slope**2) / (1 + (frequencies / high)**4)
    return np.fft.irfft(np.fft.rfft(RNG.normal(0, 1, t.size)) * window, n=t.size)


def plucked(note):
    t = times(4.3)
    frequency = pitch(note)
    phase = 2 * np.pi * frequency * t
    string = np.zeros(t.size)
    # Warmer harmonics and a brief, filtered fingertip sound.
    for harmonic in range(1, 9):
        strike = np.sin(harmonic * .31) / (harmonic**1.26)
        string += strike * np.sin(harmonic * phase) * np.exp(-t * (1.05 + .46 * harmonic))
    contact = filtered_breath(t, 530, 2350) * np.exp(-t * 54)
    body = np.sin(phase * .997) * np.exp(-t * 1.84)
    return (string + .13 * body + .031 * contact) * (1 - np.exp(-t * 100))


def flute(note, beats):
    length = beats * BEAT
    t = times(length)
    breath = np.minimum(1, t / .34) * np.minimum(1, (length - t) / .54)
    envelope = np.sin(.5 * np.pi * breath)**2
    drift = .20 * (1 - np.exp(-t * 1.7)) * np.sin(2 * np.pi * 4.2 * t)
    angle = 2 * np.pi * pitch(note) * t + drift
    tone = np.sin(angle) + .12 * np.sin(2 * angle + .3) + .040 * np.sin(3 * angle)
    air = filtered_breath(t, 870, 3900)
    ripple = .92 + .08 * np.sin(2 * np.pi * 2.7 * t)
    return envelope * (tone * ripple + .043 * air)


def held(note):
    t = times(BEAT * 9.3)
    frequency = pitch(note)
    envelope = np.sin(np.pi * t / (BEAT * 9.3))**2
    a = np.sin(2 * np.pi * frequency * t)
    b = np.sin(2 * np.pi * (frequency + .70) * t + .8)
    c = np.sin(2 * np.pi * 2 * frequency * t + .2)
    return envelope * (.48 * a + .31 * b + .14 * c)


def add(track, samples, beat, gain):
    indexes = (round(beat * BEAT * RATE) + np.arange(samples.size)) % track.size
    track[indexes] += gain * samples


def main():
    OUT.mkdir(exist_ok=True)
    score = np.zeros(round(48 * BEAT * RATE))
    # Open fifths and suspended chords, with space between the melodic phrases.
    for beat, bass, fifth in [(0, 38, 45), (8, 41, 48), (16, 36, 43),
                               (24, 43, 50), (32, 41, 48), (40, 38, 45)]:
        add(score, held(bass), beat - .35, .108)
        add(score, held(fifth), beat + .40, .078)
    plucks = [(0.3,50), (1.78,57), (3.0,64), (5.55,57), (7.12,60),
              (8.28,53), (10.23,60), (13.0,57), (15.3,65), (16.7,48),
              (18.0,55), (21.5,62), (24.28,55), (26.10,62), (29.35,57),
              (31.40,62), (33.24,53), (34.84,60), (37.7,64), (40.02,50),
              (42.4,57), (44.39,64), (46.4,62)]
    for beat, note in plucks:
        add(score, plucked(note), beat, RNG.uniform(.30, .45))
    for beat, note, duration in [(3.65, 69, 2.3), (6.1, 67, 1.75),
                                  (12.1, 65, 2.4), (20.3, 67, 2.4),
                                  (23.0, 64, 1.6), (29.0, 69, 2.6),
                                  (36.8, 65, 2.2), (43.1, 62, 2.55)]:
        add(score, flute(note, duration), beat, .11)
    # Circular reflections carry the tails smoothly across the loop boundary.
    dry = score.copy()
    for delay, wet in [(.071, .13), (.137, .095), (.211, .07), (.349, .048), (.473, .03)]:
        score += np.roll(dry, round(delay * RATE)) * wet
    scale = min(.112 / np.sqrt(np.mean(score**2)), .62 / np.max(np.abs(score)))
    pcm = np.rint(score * scale * 32767).astype('<i2')
    asset = OUT / 'clearing-music.wav'
    with wave.open(str(asset), 'wb') as output:
        output.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        output.writeframes(pcm.tobytes())
    info = {
        'origin': 'Alder River Clearing, original score synthesized for The Broken Bridge',
        'source': '../compose_music.py',
        'format': 'Mono PCM WAV, 22050 Hz, 16-bit',
        'license': 'Original project audio, distributable with this game',
        'clips': {
            'clearing-music': {
                'file': asset.name,
                'loop': True,
                'seconds': round(score.size / RATE, 3),
                'sha256': hashlib.sha256(asset.read_bytes()).hexdigest(),
            },
        },
    }
    (OUT / 'manifest.json').write_text(json.dumps(info, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
