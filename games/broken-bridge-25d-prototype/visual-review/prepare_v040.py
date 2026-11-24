"""Register the generated gait and performance art to a shared foot origin."""
from pathlib import Path
from statistics import median
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'visual-review/v040-originals'
ATLAS = {'scout': 'exec-7cfe68bd-8f94-4138-af10-1507d998ae92.png',
         'ranger': 'exec-a47bc4a0-4bdc-4d2d-a972-6aadbaf181d5.png',
         'actions': 'exec-afcfab3c-b415-4674-93b9-d0b4e790306f.png'}
DIRECTIONS = ('right', 'left', 'down', 'up')

def cut_cells(name, columns, rows):
    with Image.open(SOURCES / ATLAS[name]) as image:
        assert image.width % columns == 0 and image.height % rows == 0, image.size
        cw, ch = image.width // columns, image.height // rows
        for row in range(rows):
            for col in range(columns):
                frame = np.array(image.crop((col*cw,row*ch,(col+1)*cw,(row+1)*ch)).convert('RGBA'))
                red, green, blue, _ = np.moveaxis(frame.astype(int), 2, 0)
                saturation=np.minimum(red,blue)-green
                key = (red>65)&(blue>52)&(saturation>13)&(blue>red*.56)
                frame[key,3]=np.clip((62-saturation[key])*5.5,0,255).astype(np.uint8)
                frame[key,0]=np.minimum(red[key],green[key]+34)
                frame[key,2]=np.minimum(blue[key],green[key]+10)
                frame[frame[:,:,3]<32,3]=0
                sprite=Image.fromarray(frame)
                bounds=sprite.getbbox()
                assert bounds and bounds[1]>1 and bounds[3]<=ch-1, (name,row,col,bounds)
                yield sprite.crop(bounds)

def register(name, sprite, scale):
    alpha=np.asarray(sprite.getchannel('A'))
    h,w=alpha.shape
    torso=alpha[int(h*.25):int(h*.55)]>160
    axis=float(np.nonzero(torso)[1].mean())
    target=(round(w*scale),round(h*scale))
    fit=sprite.resize(target,Image.Resampling.LANCZOS)
    start=(round(80-axis*scale),188-fit.height)
    assert start[0]>=0 and start[1]>=0 and start[0]+fit.width<=160, (name,start,target)
    frame=Image.new('RGBA',(160,192))
    frame.paste(fit,start)
    frame.save(ROOT/'assets'/f'{name}.webp',quality=91,method=5)

for role in ('scout','ranger'):
    frames=list(cut_cells(role,6,4))
    scale=180/median(frame.height for frame in frames)
    for i,sprite in enumerate(frames):
        register(f'{role}-v4-{DIRECTIONS[i//6]}-{i%6}',sprite,scale)

actions=list(cut_cells('actions',3,2))
for names, frames, reference in [
    (('scout-v4-hold','scout-v4-carry-step','scout-v4-fit'),actions[:3],0),
    (('ranger-v4-inspect','ranger-v4-listen','ranger-v4-handoff'),actions[3:],1),
]:
    for name,sprite in zip(names,frames,strict=True):
        register(name,sprite,180/frames[reference].height)
