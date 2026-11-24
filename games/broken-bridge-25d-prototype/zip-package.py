"""Create a reproducible offline archive from the exact tested browser payload."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

BUILD = Path(__file__).resolve().parent / 'build'
FILES = ['Broken-Bridge-v0.4.0.html', 'OFFLINE-README.txt', 'PHASER-LICENSE.txt']

with ZipFile(BUILD / 'Broken-Bridge-v0.4.0-Offline.zip', 'w') as archive:
    for file in FILES:
        entry = ZipInfo(file, (2026, 1, 1, 0, 0, 0))
        entry.external_attr = 0o644 << 16
        archive.writestr(entry, (BUILD / file).read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
