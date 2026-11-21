#!/usr/bin/env python3
"""Verify immutable Allen L4 benchmark ZIP and its language map; NOT browser QA."""
from pathlib import Path
import hashlib, zipfile, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'references'/'allen-lesson-4'
EXPECTED_FILES={'index.html','manifest.webmanifest','service-worker.js','LANGUAGE_MAP.json','JESSE_NEW_RECORDING_QUEUE.txt','QA_REPORT.md','icon-192.png','icon-512.png','START_HERE.txt'}
MODULES_8=('SOUND','SYLLABLE','SCAN','SORT','PHRASES','HABITATS','TRAINS','GAP','BECAUSE','CONTRAST','DRONE','READER','INTERVIEW')

def check():
    manifest=json.loads((REF/'REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
    zpath=REF/manifest['reference_pwa_filename']
    errors=[]
    if not zpath.is_file(): return [f'Missing benchmark: {zpath}']
    sha=hashlib.sha256(zpath.read_bytes()).hexdigest()
    if sha!=manifest['reference_pwa_sha256']: errors.append('Benchmark PWA checksum changed')
    with zipfile.ZipFile(zpath) as z:
        corrupt=z.testzip()
        if corrupt: errors.append(f'PWA corrupt entry: {corrupt}')
        missing=EXPECTED_FILES-set(z.namelist())
        if missing: errors.append(f'Missing PWA contents: {sorted(missing)}')
        html=z.read('index.html')
        if hashlib.sha256(html).hexdigest()!=manifest['embedded_html_sha256']: errors.append('Benchmark embedded HTML changed')
        for media,count in manifest['embedded_media_data_url_occurrences'].items():
            actual=html.count(('data:'+media+';base64,').encode())
            if actual!=count: errors.append(f'{media}: {actual} != reference {count}')
        m=json.loads(z.read('LANGUAGE_MAP.json'))
        on_disk=json.loads((REF/'LANGUAGE_MAP.json').read_text(encoding='utf-8'))
        if m!=on_disk: errors.append('Extracted language map does not match archived game')
        for name in MODULES_8:
            if not isinstance(m.get(name),list) or len(m[name])!=8:
                errors.append(f'{name}: expected 8 benchmark entries; found {len(m.get(name,[]))}')
        finale=m.get('FINALE',[])
        if len(finale)!=5: errors.append('Finale count is not 5')
        for idx,entry in enumerate(finale,1):
            if not isinstance(entry,dict) or entry.get('correct') not in entry.get('options',[]):
                errors.append(f'Finale {idx}: correct answer missing from options')
        if 'ORAL' not in m: errors.append('ORAL content missing')
        if not z.read('JESSE_NEW_RECORDING_QUEUE.txt').startswith(b'ALLEN'): errors.append('Recording queue malformed')
    return errors

if __name__=='__main__':
    problems=check()
    if problems:
        print('FAIL: immutable reference failed validation')
        for p in problems:print(' -',p)
        sys.exit(1)
    print('PASS: PWA integrity, SHA-256, archived language map, focus module counts, media data URLs, and finale answer membership')
    print('NOTE: Not a browser gameplay test, semantic grammar review, audio playback test, or iPhone/WeChat certification')
