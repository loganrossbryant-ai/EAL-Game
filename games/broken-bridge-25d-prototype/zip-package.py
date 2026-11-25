"""Create a reproducible offline archive from the exact tested browser payload."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

PROJECT = Path(__file__).resolve().parent
BUILD = PROJECT / 'build'
VERSION = json.loads((PROJECT / 'package.json').read_text())['version']
STEM = f'Broken-Bridge-v{VERSION}'
FILES = [f'{STEM}.html', 'OFFLINE-README.txt', 'PHASER-LICENSE.txt']

with ZipFile(BUILD / f'{STEM}-Offline.zip', 'w') as archive:
    for file in FILES:
        entry = ZipInfo(file, (2026, 1, 1, 0, 0, 0))
        entry.external_attr = 0o644 << 16
        archive.writestr(entry, (BUILD / file).read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
