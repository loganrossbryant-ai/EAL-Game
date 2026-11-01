"""Copy transparent, inspectable GM desk files beside a standard Godot Web export."""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('destination', type=Path)
    args = p.parse_args()
    target = args.destination.resolve()
    if not (target / 'index.html').is_file():
        raise SystemExit('Export Godot Web to this folder first.')
    for name in ('gm.html', 'gm.js', 'gm.css', 'academic.otf'):
        shutil.copyfile(ROOT / 'far-horizon/web' / name, target / name)
    shutil.copyfile(ROOT / 'far-horizon/data/campaign.json', target / 'campaign.json')
    print('Copied the same-browser GM desk, campaign and local vocabulary font.')

if __name__ == '__main__':
    main()
