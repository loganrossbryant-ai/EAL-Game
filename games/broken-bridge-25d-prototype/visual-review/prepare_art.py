"""Prepare the original generated production plates and chroma-keyed asset sheets."""
from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

parser = ArgumentParser(description=__doc__)
parser.add_argument('forest', type=Path)
parser.add_argument('characters', type=Path)
parser.add_argument('bridge', type=Path)
parser.add_argument('--kit', type=Path)
args = parser.parse_args()
assets = Path(__file__).resolve().parents[1] / 'assets'

def save(image, name, quality=88):
    image.save(assets / f'{name}.webp', quality=quality, method=6)

def key(image):
    pixels = np.asarray(image.convert('RGBA')).copy()
    r, g, b, _ = np.moveaxis(pixels.astype(float), 2, 0)
    saturation = np.minimum(r, b) - g
    magenta = (b > 104) & (r > 110) & (saturation > 60)
    pixels[magenta, 3] = np.clip((128-saturation[magenta])*4, 0, 255).astype(np.uint8)
    changed = magenta & (pixels[:, :, 3] > 0)
    pixels[changed, 2] = np.minimum(b[changed], g[changed] + 32).astype(np.uint8)
    return Image.fromarray(pixels)

def cell(image, columns, rows, x, y):
    return image.crop((image.width*x//columns, image.height*y//rows,
                       image.width*(x+1)//columns, image.height*(y+1)//rows))

def subject(image):
    return image.crop(image.getbbox())

forest = Image.open(args.forest).convert('RGB')
forest.thumbnail((1600, 815), Image.Resampling.LANCZOS)
save(forest, 'forest', 90)
plate = forest.resize((1060, 540), Image.Resampling.LANCZOS).convert('RGBA')

def local_layer(name, points, feather):
    mask = Image.new('L', plate.size)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    layer = plate.copy()
    layer.putalpha(mask)
    save(layer.crop(mask.getbbox()), name, 84)

local_layer('current', [(245,307),(429,314),(615,339),(760,338),(777,365),(610,379),(428,369),(242,356)], 13)
local_layer('front-left', [(0,450),(26,457),(43,479),(82,486),(94,496),(133,490),
                           (190,509),(250,528),(261,540),(0,540)], 2)
local_layer('front-right', [(833,540),(890,513),(926,510),(955,488),(997,494),
                            (1030,477),(1060,454),(1060,540)], 2)

sheet = key(Image.open(args.characters))
gesture = subject(cell(sheet, 4, 3, 3, 0))
save(gesture.crop((0,0,gesture.width,round(gesture.height*.56))), 'ranger-portrait', 93)
for row, role in enumerate(('ranger', 'scout')):
    for column in range(4):
        figure = subject(cell(sheet, 4, 3, column, row))
        figure.thumbnail((153, 181), Image.Resampling.LANCZOS)
        frame = Image.new('RGBA', (160, 192))
        frame.paste(figure, ((160-figure.width)//2, 188-figure.height))
        save(frame, f'{role}-{column}', 90)
for column, name in enumerate(('rack', 'depth', 'sign', 'flags')):
    prop = subject(cell(sheet, 4, 3, column, 2))
    prop.thumbnail((296, 270), Image.Resampling.LANCZOS)
    save(prop, name, 88)

spans = key(Image.open(args.bridge))
for column, name in enumerate(('broken', 'repaired')):
    bridge = subject(cell(spans, 2, 1, column, 0))
    bridge.thumbnail((520, 450), Image.Resampling.LANCZOS)
    save(bridge, name, 91)
    if name == 'repaired':
        for index, box in enumerate(((.31,.28,.70,.45),(.28,.45,.72,.65))):
            mask = Image.new('L', bridge.size)
            ImageDraw.Draw(mask).rectangle(tuple(round(n*d) for n,d in zip(box, bridge.size*2)), fill=255)
            part = bridge.copy()
            part.putalpha(ImageChops.multiply(mask,part.getchannel('A')))
            save(part, f'bridge-fill-{index}', 90)

flag_sheet = Image.open(assets / 'flags.webp').convert('RGBA')
for i in range(2):
    flag = subject(cell(flag_sheet, 2, 1, i, 0))
    save(flag, f'flag-{i}')


if args.kit:
    kit = key(Image.open(args.kit))
    for i, name in enumerate(('board', 'rope', 'supplies', 'rack-loaded')):
        item = subject(cell(kit, 2, 2, i%2, i//2))
        item.thumbnail((325, 270), Image.Resampling.LANCZOS)
        save(item, name, 89)
