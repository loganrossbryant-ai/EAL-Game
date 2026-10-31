"""Deterministic original ambient/SFX assets. No supplied M01/M02 recordings."""
import math, random, struct, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'far-horizon/assets/audio'
RATE=22050
def make(name, seconds, sample):
    rng=random.Random(2247)
    samples=[]
    low=0
    for i in range(int(seconds*RATE)):
        t=i/RATE
        low=low*.985+rng.uniform(-1,1)*.015
        samples.append(max(-.8,min(.8,sample(t,rng,low))))
    with wave.open(str(ROOT/name),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE)
        f.writeframes(struct.pack('<'+'h'*len(samples),*[int(x*32767) for x in samples]))
def ambience(t,rng,low):
    # Integer-period harmonics and slowly modulated ventilator noise.
    envelope=.88+.12*math.cos(2*math.pi*t/8)
    return envelope*(.036*math.sin(2*math.pi*62*t)+.014*math.sin(2*math.pi*124*t)+.06*low)
make('ambience.wav',8,ambience)
make('step.wav',.19,lambda t,r,l:math.exp(-t*31)*(.13*math.sin(2*math.pi*110*t)+.1*r.uniform(-1,1)))
make('ignition.wav',5,lambda t,r,l:min(1,t/.7)*min(1,(5-t)/.8)*(.13*math.sin(2*math.pi*(45*t+3*t*t))+.2*l+.035*r.uniform(-1,1)))
make('cutoff.wav',.9,lambda t,r,l:math.exp(-t*8)*(.1*math.sin(2*math.pi*84*t)+.04*r.uniform(-1,1)))
print('Created four original Pioneer ambient/SFX WAV files.')
