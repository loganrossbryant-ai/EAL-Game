"""Add an offline installer around an ordinary, unmodified Godot Web export."""
from pathlib import Path
import argparse, hashlib, json, shutil
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('directory',type=Path)
args=parser.parse_args()
out=args.directory.resolve()
source=out/'index.html'
html=source.read_text()
if 'GODOT_CONFIG' not in html: raise SystemExit('Start with a fresh standard Godot export.')
html=html.replace('<html lang="en">','<html lang="en">')
html=html.replace('</head>','<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="app-icon.png"><style>body{background:#1f625c!important}#canvas{outline:none}#status{background:#1f625c;font-family:Arial,sans-serif}</style></head>')
(out/'game.html').write_text(html)
shutil.copy2(ROOT/'assets/art/cafe.png',out/'cover.png')
shutil.copy2(ROOT/'assets/art/pip.png',out/'pip.png')
shutil.copy2(ROOT/'assets/fonts/Body.ttf',out/'Body.ttf')
shutil.copy2(ROOT/'assets/fonts/Chinese.otf',out/'Chinese.otf')
shutil.copy2(ROOT/'assets/icon512.png',out/'app-icon.png')
licenses=out/'licenses';licenses.mkdir(exist_ok=True)
for name in ['GODOT-LICENSE.txt','GODOT-THIRD-PARTY-NOTICES.txt']:
    shutil.copy2(ROOT.parent/'far-horizon'/name,licenses/name)
shutil.copy2(ROOT/'assets/fonts/LICENSE-OpenSans.txt',licenses/'LICENSE-OpenSans.txt')
shutil.copy2(ROOT/'assets/fonts/LICENSE-Noto.txt',licenses/'LICENSE-Noto.txt')
manifest={'name':"Alan's Favorites Island",'short_name':'Alan + Pip','id':'./','start_url':'./','scope':'./','display':'standalone','orientation':'landscape','background_color':'#1f625c','theme_color':'#217e76','icons':[{'src':'app-icon.png','sizes':'512x512','type':'image/png','purpose':'any'}]}
(out/'manifest.webmanifest').write_text(json.dumps(manifest,indent=2))
# Include the installer and worker templates too, so an offline update is atomic.
# Ignore generated files left by a prior export; they must not affect revision IDs.
digest=hashlib.sha256()
for p in sorted(out.rglob('*')):
    if p.is_file() and p.name not in ['index.html','update.html','sw.js','asset-manifest.json']:
        digest.update(p.relative_to(out).as_posix().encode());digest.update(p.read_bytes())
for name in ['install.html','sw.js']:digest.update((ROOT/'web'/name).read_bytes())
revision=digest.hexdigest()[:16]
landing=(ROOT/'web/install.html').read_text().replace('__VERSION__',revision)
(out/'index.html').write_text(landing)
(out/'update.html').write_text(landing)
assets=['./']+[p.relative_to(out).as_posix() for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['sw.js','asset-manifest.json']]
worker=(ROOT/'web/sw.js').read_text().replace('__VERSION__',revision).replace('__ASSETS__',json.dumps(assets))
(out/'sw.js').write_text(worker)
files=[{'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='asset-manifest.json']
(out/'asset-manifest.json').write_text(json.dumps({'version':revision,'engine':'Godot 4.6.3 non-threaded Web','files':files},indent=2))
print('Prepared',len(files),'local files;',round(sum(p['bytes'] for p in files)/1048576,1),'MiB; offline cache',revision)
