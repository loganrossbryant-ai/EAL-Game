"""Copy transparent, inspectable GM desk files beside a standard Godot Web export."""
from pathlib import Path
import argparse
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('destination', type=Path)
    args = p.parse_args()
    target = args.destination.resolve()
    if not (target / 'index.html').is_file():
        raise SystemExit('Export Godot Web to this folder first.')
    for name in ('gm.html', 'gm.js', 'gm.css', 'academic.otf', 'play.html', 'play.js', 'play.css'):
        shutil.copyfile(ROOT / 'far-horizon/web' / name, target / name)
    shutil.copyfile(ROOT / 'far-horizon/data/campaign.json', target / 'campaign.json')
    shutil.copyfile(ROOT / 'far-horizon/data/portraits.json', target / 'portraits.json')
    (target/'portraits').mkdir(exist_ok=True)
    for entry in json.loads((ROOT/'far-horizon/data/portraits.json').read_text()).values():
        shutil.copyfile(ROOT/'far-horizon/assets/portraits'/entry['file'],target/'portraits'/entry['file'])
    shutil.copyfile(ROOT / 'far-horizon/assets/art/corridor.png', target / 'poster.png')
    print('Copied the same-browser GM desk, campaign and local vocabulary font.')

if __name__ == '__main__':
    main()
