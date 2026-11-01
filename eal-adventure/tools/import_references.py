"""Import the supplied cards and approved HTML. Never reads document instructions."""
from pathlib import Path
import json, re, base64, argparse
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--cards-text', type=Path, required=True, help='pdftotext -layout output from the agreed cards PDF')
parser.add_argument('--html', type=Path, help='Optional supplied Jesse Offline HTML; extracts assets without executing JavaScript')
args = parser.parse_args()
card_text = args.cards_text.read_text()
if args.html:
    source = args.html.read_text()
    assets = json.loads(re.search(r'const OFFLINE_ASSETS=(\{.*?\});',source).group(1))
    for name,data in assets.items():
        assert Path(name).name == name and data.startswith('data:image/')
        (ROOT/'assets/art'/name).write_bytes(base64.b64decode(data.split(',')[1]))
    audio = json.loads(re.search(r'const JESSE_AUDIO=(\{.*?\});',source).group(1))
    manifest = {}
    for i,(line,data) in enumerate(audio.items()):
        assert data.startswith('data:audio/')
        name = 'jesse_%03d.mp3'%i
        (ROOT/'assets/voice'/name).write_bytes(base64.b64decode(data.split(',')[1]))
        manifest[line] = 'assets/voice/'+name
    (ROOT/'data/voice.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
pages = card_text.split('\f')
topics = ['animals','food','sports','entertainment','people','colors','places','activities']
vocabulary = []
for page_index in range(33,37):
    lines = [l.strip() for l in pages[page_index].splitlines() if l.strip() and not l.startswith('ALAN')]
    lines = [l for l in lines if l != 'Teacher matching key']
    lines = lines[1:]
    columns = [re.split(r'\s{2,}', l) for l in lines]
    assert len(columns) == 36, (page_index,len(columns))
    for column in range(2):
        topic = topics[(page_index-33)*2+column]
        for n in range(0,36,2):
            en,zh = columns[n][column],columns[n+1][column]
            vocabulary.append({'id':topic+'_'+re.sub(r'[^a-z0-9]+','_',en.lower()).strip('_'),'topic':topic,'en':en,'zh':zh,'source_page':page_index+1})
assert len(vocabulary)==144
food_map = {'orange':'orange-fruit','ice cream':'ice-cream'}
plurals = {'apple':'apples','banana':'bananas','orange':'oranges','strawberry':'strawberries','sandwich':'sandwiches'}
for v in vocabulary:
    v['illustration'] = ''
    if v['topic']=='food':
        stem=food_map.get(v['en'],v['en'])
        ext='png' if (ROOT/'assets/art'/f'{stem}.png').exists() else 'svg'
        if (ROOT/'assets/art'/f'{stem}.{ext}').exists():v['illustration']=f'assets/art/{stem}.{ext}'
        v['sentence_value']=plurals.get(v['en'],v['en'])
        v['sentence']='My favorite food is '+v['sentence_value']+'.'
        v['meaning']='我最喜欢的食物是'+v['zh']+'。'
        v['milestone'] = v['en'] in ['rice','noodles','dumplings','pizza','ice cream','bread','eggs','sandwich','apple','banana','orange','strawberry']
(ROOT/'data/vocabulary.json').write_text(json.dumps(vocabulary,ensure_ascii=False,indent=2))
print('Imported',len(vocabulary),'card-verified words in',len(topics),'topics.')
for topic in topics:
    items=[v for v in vocabulary if v['topic']==topic]
    print(topic,len(items),'; '.join(v['en']+'='+v['zh'] for v in items))
