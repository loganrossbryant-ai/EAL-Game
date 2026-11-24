"""Produce the crisp registered bank and parallax plate from the authored edit."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

review = Path(__file__).resolve().parent
assets = review.parent / 'assets'
source = review / 'originals' / 'exec-352d35e3-5b2d-4e73-ab53-8ed54f01d44e.png'
forest = Image.open(source).convert('RGB')
forest = forest.filter(ImageFilter.UnsharpMask(radius=1.1, percent=34, threshold=4))
forest.save(assets / 'scenery-distance.webp', quality=95, method=6)
width, height = forest.size
mask = Image.new('L', forest.size)
shoreline = [(0,0),(.15,0),(.24,.10),(.34,.21),(.47,.27),(.62,.30),(.76,.32),(1,.27),(1,1),(0,1)]
ImageDraw.Draw(mask).polygon([(round(x*width),round(y*height)) for x,y in shoreline], fill=255)
bank = forest.convert('RGBA')
bank.putalpha(mask.filter(ImageFilter.GaussianBlur(20)))
bank.save(assets / 'scenery-bank.webp', quality=95, method=6)
