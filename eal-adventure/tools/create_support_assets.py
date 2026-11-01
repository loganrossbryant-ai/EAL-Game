"""Bundle local fonts and original non-speech music. No runtime generation."""
from pathlib import Path
import math, struct, wave, shutil
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1]
source=ROOT.parent/'far-horizon/assets/fonts'
for name in ['Body.ttf','LICENSE-OpenSans.txt']:
    shutil.copy2(source/name,ROOT/'assets/fonts'/name)
texts=''.join(p.read_text() for folder in ['scripts','data','web','tools'] for p in (ROOT/folder).rglob('*') if p.suffix in ['.gd','.json','.html','.js','.py'])
font=TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',fontNumber=2)
options=subset.Options()
options.layout_features=['*']
subsetter=subset.Subsetter(options=options)
subsetter.populate(text=texts+'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ✓▶←→↑↓–—×%/.,!?“”‘’：。…_')
subsetter.subset(font)
font.save(ROOT/'assets/fonts/Chinese.otf')
rate=22050
def write(name,samples):
    with wave.open(str(ROOT/'assets'/name),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
        f.writeframes(b''.join(struct.pack('<h',max(-32767,min(32767,int(s*32767)))) for s in samples))
def note(freq,t):
    return math.exp(-t*4.2)*(math.sin(2*math.pi*freq*t)+.20*math.sin(2*math.pi*freq*2*t))*(1-math.exp(-t*100))
beat=.625
chords=[[48,55,60,64],[45,52,57,60],[41,48,53,57],[43,50,55,59]]
duration=beat*64
samples=[0.] * int(duration*rate)
for step in range(128):
    chord=chords[(step//8)%4]
    midi=chord[[0,2,1,3,2,3,1,2][step%8]]+12
    freq=440*2**((midi-69)/12)
    start=int(step*beat*.5*rate)
    for j in range(int(rate*1.8)):
        index=start+j
        if index<len(samples): samples[index]+=note(freq,j/rate)*.095
fade=int(rate*.1)
for i in range(fade):samples[i]*=i/fade;samples[-1-i]*=i/fade
write('music.wav',samples)
write('chime.wav',[sum(note(freq,max(0,i/rate-delay))*.12 if i/rate>=delay else 0 for freq,delay in [(523.25,0),(659.25,.10),(783.99,.20)]) for i in range(int(rate*1.2))])
print('Bundled English and Simplified Chinese fonts, 40 seconds of original instrumental music and a chime.')
