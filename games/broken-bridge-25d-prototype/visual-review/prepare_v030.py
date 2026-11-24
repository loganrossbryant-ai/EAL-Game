"""Separate the approved-to-revise plate and key the new v0.3 authored sprites."""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import numpy as np

project = Path(__file__).resolve().parents[1]
assets = project / 'assets'
originals = Path(__file__).resolve().parent / 'originals'

def keyed(path):
    pixels = np.array(Image.open(originals / path).convert('RGBA'))
    red, green, blue, _ = np.moveaxis(pixels.astype(int), 2, 0)
    saturation = np.minimum(red, blue) - green
    # Chroma spill also affects partially covered pixels around needles,
    # cap brims and rope fibres. Limit decontamination to key-coloured edges.
    magenta = (red > 67) & (blue > 53) & (saturation > 14) & (blue > red*.58)
    pixels[magenta, 3] = np.clip((65-saturation[magenta])*5.0, 0, 255).astype(np.uint8)
    edge = magenta & (pixels[:, :, 3] > 0)
    pixels[edge, 0] = np.minimum(red[edge], green[edge]+31).astype(np.uint8)
    pixels[edge, 2] = np.minimum(blue[edge], green[edge]+8).astype(np.uint8)
    return Image.fromarray(pixels)

def cells(image, count):
    for i in range(count):
        piece = image.crop((image.width*i//count,0,image.width*(i+1)//count,image.height))
        yield piece.crop(piece.getbbox())

def save(image, name):
    image.save(assets / f'{name}.webp', quality=91, method=6)

forest = Image.open(assets / 'forest.webp').convert('RGBA')
forest.thumbnail((1470,735), Image.Resampling.LANCZOS)
width, height = forest.size
save(forest.convert('RGB'), 'scenery-distance')
overlay=forest.copy()
bank_mask=Image.new('L',forest.size)
shoreline=[(0,0),(.15,0),(.24,.10),(.34,.21),(.47,.27),(.62,.30),(.76,.32),(1,.27),(1,1),(0,1)]
ImageDraw.Draw(bank_mask).polygon([(round(x*width),round(y*height)) for x,y in shoreline], fill=255)
overlay.putalpha(bank_mask.filter(ImageFilter.GaussianBlur(18)))
save(overlay,'scenery-bank')
for name, image in zip(('storm-canopy','storm-boulder','storm-debris'),cells(keyed('exec-20e45035-9127-4a37-96ef-308fee0152aa.png'),3),strict=True):
    image.thumbnail((580,335),Image.Resampling.LANCZOS)
    save(image,name)
bridge = list(cells(keyed('exec-1e0c790a-34ad-4f14-a8d5-243683c7bfba.png'),2))
for name,image in zip(('bridge-damaged-v3','bridge-restored-v3'),bridge,strict=True):
    save(image.resize((470,530),Image.Resampling.LANCZOS),name)
fixed=Image.open(assets/'bridge-restored-v3.webp').convert('RGBA')
for i, box in enumerate(((.27,.47,.72,.67),(.31,.29,.69,.47))):
    mask=Image.new('L',fixed.size)
    ImageDraw.Draw(mask).rectangle(tuple(round(n*d) for n,d in zip(box, fixed.size*2)),fill=255)
    patch=fixed.copy()
    patch.putalpha(ImageChops.multiply(mask,fixed.getchannel('A')))
    save(patch,f'bridge-patch-v3-{i}')

actors = keyed('exec-0750e7af-4a26-4a5c-975d-4ecdc08dc23b.png')
for row, role in enumerate(('ranger','scout')):
    strip=actors.crop((0,actors.height*row//3,actors.width,actors.height*(row+1)//3))
    for i, art in enumerate(cells(strip,4)):
        if row==0 and i==3:
            save(art.crop((0,0,art.width,round(art.height*.56))), 'ranger-v3-portrait')
        art.thumbnail((153,181),Image.Resampling.LANCZOS)
        frame=Image.new('RGBA',(160,192))
        frame.paste(art,((160-art.width)//2,188-art.height))
        save(frame,f'{role}-v3-{i}')
