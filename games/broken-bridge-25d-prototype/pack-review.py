"""Pack the verified game, editable Git source, pinned npm archives and QA evidence."""
import argparse
import base64
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import tarfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

PROJECT = Path(__file__).resolve().parent
BUILD = PROJECT / 'build'
GAME_PATH = 'games/' + PROJECT.name
VERSION = json.loads((PROJECT / 'package.json').read_text())['version']
STEM = f'Broken-Bridge-v{VERSION}'
SOURCE_ROOT = 'source/EAL-Game'
LEGACY_MEDIA = ('visual-review/screenshots/', 'visual-review/v030-screenshots/',
                'visual-review/v040-evidence/', 'visual-review/v0.1.0-opening-')


def source_entries(commit):
    data = subprocess.check_output(['git','archive','--format=tar',commit,GAME_PATH],cwd=PROJECT)
    with tarfile.open(fileobj=BytesIO(data)) as archive:
        for item in archive:
            if not item.isfile():
                continue
            if item.name.removeprefix(GAME_PATH+'/').startswith(LEGACY_MEDIA):
                continue
            yield f'{SOURCE_ROOT}/{item.name}', archive.extractfile(item).read()


def dependencies(folder, lock):
    for name, spec in sorted(lock['packages'].items()):
        if not name:
            continue
        tarball = folder / f'{name.removeprefix("node_modules/")}-{spec["version"]}.tgz'
        data = tarball.read_bytes()
        method, encoded = spec['integrity'].split('-',1)
        if hashlib.new(method,data).digest()!=base64.b64decode(encoded):
            raise SystemExit(f'Dependency integrity mismatch: {tarball}')
        yield 'dependencies/'+tarball.name,data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_commit')
    parser.add_argument('npm_archives',type=Path)
    parser.add_argument('review_material',type=Path,help='Folder with START-HERE.md plus qa/ and evidence/')
    args=parser.parse_args()
    commit=subprocess.check_output(['git','rev-parse',args.source_commit],cwd=PROJECT,text=True).strip()
    source=dict(source_entries(commit))
    lock_path=f'{SOURCE_ROOT}/{GAME_PATH}/package-lock.json'
    lock=json.loads(source[lock_path])
    if lock['version']!=VERSION:
        raise SystemExit('Source version and play build version disagree.')
    if not all((args.review_material/name).exists() for name in ('START-HERE.md','qa','evidence')):
        raise SystemExit('Collect instructions, QA and visual/audio evidence before packaging.')
    entries={
        'SOURCE-SHA.txt': (commit+'\n').encode(),
        **source,
        **dict(dependencies(args.npm_archives,lock)),
    }
    with ZipFile(BUILD/f'{STEM}-Offline.zip') as play:
        if play.testzip() is not None:
            raise SystemExit('The play archive is corrupt.')
        for name in play.namelist():
            entries['play/'+name]=play.read(name)
    for path in args.review_material.rglob('*'):
        if path.is_file():
            entries[path.relative_to(args.review_material).as_posix()]=path.read_bytes()
    checks=''.join(f'{hashlib.sha256(value).hexdigest()}  {key}\n' for key,value in sorted(entries.items()))
    entries['SHA256SUMS.txt']=checks.encode()
    target=BUILD/f'{STEM}-Review.zip'
    with ZipFile(target,'w') as review:
        for key,value in sorted(entries.items()):
            entry=ZipInfo(key,(2026,1,1,0,0,0))
            entry.external_attr=0o644<<16
            review.writestr(entry,value,compress_type=ZIP_DEFLATED,compresslevel=9)
    with ZipFile(target) as review:
        if review.testzip() is not None:
            raise SystemExit('Review archive integrity check failed.')
    print(f'{target.name}: {len(entries)} files, {target.stat().st_size:,} bytes, source {commit}')


if __name__=='__main__':
    main()
