"""Package the checked standard Web export and a device-appropriate offline guide."""
from pathlib import Path
import hashlib, json, shutil, zipfile, argparse
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
parser=argparse.ArgumentParser()
parser.add_argument('--classroom-html',type=Path,required=True)
parser.add_argument('--classroom-pdf',type=Path,required=True)
args=parser.parse_args()
candidate=REPO/'alan-review/candidate'
candidate.mkdir(parents=True,exist_ok=True)
shutil.copytree(REPO/'builds/alan-island',candidate/'web',dirs_exist_ok=True)
materials=candidate/'materials';materials.mkdir(exist_ok=True)
shutil.copy2(args.classroom_html,materials/'Cafe-Classroom-Cards.html')
shutil.copy2(args.classroom_pdf,materials/'Cafe-Classroom-Cards.pdf')
guide='''ALAN'S FAVORITES ISLAND — CAFE MILESTONE

iPAD / iPHONE: INSTALL THE OFFLINE WEB APP
1. Open https://loganrossbryant-ai.github.io/hello-earth-demo/alan-island/ in Safari.
2. Tap Save for offline. Keep the page open until Offline ready appears.
3. Safari Share > Add to Home Screen.
4. Open the island icon, enable Airplane Mode, then try Play with Pip.
All pictures, fonts, music and Jesse speech are saved on that device.
The initial download needs access to the play site. Play after installation
needs no network, VPN, account, API key or voice service.
This ZIP is a complete backup, not an iOS app. Opening game.html directly in
iOS Files is not supported. Keep the app icon and website data. Confirm real
iOS Safari/Home Screen behavior on Alan's device; physical iOS was not available
for the automated tests.

DESKTOP OFFLINE RECOVERY
Unzip the whole folder. With Python 3 installed, run:
    python3 Start-local.py
Then open http://127.0.0.1:8079/ in a modern browser.
This local server uses only Python's standard library and binds to this computer.
It does not fetch anything from the internet. Keep the play folder intact.

PLAY
Tap the terrace to walk. Tap Mina, a food stall or the festival table to approach
and interact. Alternatively use arrows/WASD and E/Enter. Chinese reveals short
help. Menu provides voice/music controls, mute, teacher summary, export and reset.
Personal favorites have no wrong answer. We said it is manual participation,
not automatic pronunciation scoring.

CLASSROOM PREVIEW
materials/Cafe-Classroom-Cards.pdf is eight A4 pages of black-and-white picture
cards, separate English/Chinese cards, sentence strips and drawing prompts.
The HTML version is self-contained and can be printed from a browser.

VOICE SCOPE
Eight foods have approved Jesse word and sentence recordings reused unchanged
from the supplied HTML. Noodles, dumplings, bread and eggs have visual matching;
their new voice samples could not start because ElevenLabs was busy. No new
dialogue batch or substitute voice was produced. New speech awaits sample review.

This delivery is the cafe scene for review. Further island locations are pending.
'''
(candidate/'OFFLINE-READ-ME.txt').write_text(guide)
server='''from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
root=Path(__file__).resolve().parent/'play'
print('Alan and Pip: open http://127.0.0.1:8079/ ; Ctrl+C to stop.')
ThreadingHTTPServer(('127.0.0.1',8079),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
'''
archive=candidate/'Alan-Favorites-Island-Offline.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted((candidate/'web').rglob('*')):
        if p.is_file():z.write(p,'Alan-Favorites-Island/play/'+p.relative_to(candidate/'web').as_posix())
    for p in sorted(materials.iterdir()):z.write(p,'Alan-Favorites-Island/materials/'+p.name)
    z.writestr('Alan-Favorites-Island/OFFLINE-READ-ME.txt',guide)
    z.writestr('Alan-Favorites-Island/Start-local.py',server)
files=[{'path':p.relative_to(candidate).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(candidate.rglob('*')) if p.is_file()]
(candidate.parent/'manifest.json').write_text(json.dumps({'files':files},indent=2))
(candidate.parent/'.gitattributes').write_text('* -text\n')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('Packaged',len(files),'files; backup ZIP',round(archive.stat().st_size/1048576,1),'MiB; hashes recorded.')
