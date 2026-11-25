"""Cut out original Alder River props and derive registered mist and water textures."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / 'assets'
SHEET = HERE / 'originals' / 'exec-4860558b-8d71-457a-8c87-a7a3872f294f.png'
PLATE = HERE / 'originals' / 'exec-352d35e3-5b2d-4e73-ab53-8ed54f01d44e.png'


def keyed(image):
    rgb = np.asarray(image.convert('RGB'), dtype=np.float32)
    red, green, blue = np.moveaxis(rgb, 2, 0)
    spill = np.minimum(red,blue)-green
    alpha = np.clip((51-spill)*6,0,255)
    rgb[:,:,0] -= np.clip(spill,0,110)*.57
    rgb[:,:,2] -= np.clip(spill,0,140)*.85
    result = Image.fromarray(np.dstack([rgb,alpha]).clip(0,255).astype('uint8'))
    return result.crop(result.getbbox())


def save(image,name):
    image.save(ASSETS / f'{name}.webp',quality=91,method=6)


sheet = Image.open(SHEET)
cells = {
    'wind-fern': (0,0,514,493), 'wind-reed': (550,0,1010,487),
    'wind-fir': (1012,0,1536,494), 'wind-cedar': (0,505,511,1024),
    'survey-winch': (542,510,992,1024), 'bridge-rig': (1012,521,1536,1024),
}
for name,box in cells.items():
    image = keyed(sheet.crop(box))
    image.thumbnail((480,490),Image.Resampling.LANCZOS)
    save(image,name)

plate=Image.open(PLATE).convert('RGB').resize((1060,540),Image.Resampling.LANCZOS)
save(plate.crop((206,299,332,351)).resize((630,260),Image.Resampling.LANCZOS),'survey-water')
save(plate.crop((0,244,1060,476)).resize((900,197),Image.Resampling.LANCZOS),'trail-overview')

# The soft mask keeps the painted river details below each independently advected strip.
for name,box in {
    'stream-amber':(208,317,322,347),
    'stream-jade':(690,324,805,348),
    'stream-wake':(654,350,759,374),
}.items():
    surface=plate.crop(box).convert('RGBA')
    w,h=surface.size
    # Mirror across the center so the moving strip contains no hard edges.
    tile=Image.new('RGBA',(w*2,h))
    tile.paste(surface,(0,0))
    tile.paste(ImageOps.mirror(surface),(w,0))
    xx,yy=np.meshgrid(np.linspace(-1,1,w*2),np.linspace(-1,1,h))
    alpha = (np.clip(1-np.abs(xx)**3,0,1)**2*np.clip(1-np.abs(yy)**2,0,1)**2*215).astype('uint8')
    tile.putalpha(Image.fromarray(alpha))
    save(tile,name)

# Lift the low-contrast fog from the original ridgeline and shape a soft transparent matte.
mist=plate.crop((538,76,1010,199))
rgb=np.asarray(mist,dtype=np.int16)
lum=rgb.mean(axis=2)
xx,yy=np.meshgrid(np.linspace(-1,1,mist.width),np.linspace(-1,1,mist.height))
edge=np.clip(1-xx**2-yy**2,0,1)**1.7
density=(np.clip((lum-86)/110,0,1)*edge*160).astype('uint8')
fog=Image.new('RGBA',mist.size,(195,213,202,0))
fog.putalpha(Image.fromarray(density).filter(ImageFilter.GaussianBlur(4.5)))
save(fog,'ridge-mist')
