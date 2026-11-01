"""Produce a self-contained, black-and-white café print preview from the game data."""
from pathlib import Path
import base64, html, json, argparse
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);args=parser.parse_args()
items=[v for v in json.loads((ROOT/'data/vocabulary.json').read_text()) if v.get('milestone')]
def uri(path):
    p=ROOT/path;mime='image/svg+xml' if p.suffix=='.svg' else ('font/otf' if p.suffix=='.otf' else ('font/ttf' if p.suffix=='.ttf' else 'image/png'))
    return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
def esc(value):return html.escape(value)
pages=[]
for mode,title in [('picture','PICTURE CARDS'),('en','ENGLISH WORD CARDS'),('zh','CHINESE WORD CARDS')]:
    for start in range(0,len(items),9):
        cards=[]
        for v in items[start:start+9]:
            content='<img alt="'+esc(v['en'])+'" src="'+uri(v['illustration'])+'">' if mode=='picture' else esc(v[mode])
            cards.append('<div class="card">'+content+'</div>')
        pages.append('<section><h1>Alan’s café · '+title+'</h1><p>Print at 100%. Cut on the dashed lines. Keep the decks separate.</p><div class="cards">'+''.join(cards)+'</div></section>')
strips=[('My name is Alan.','我叫艾伦。'),("What’s your favorite food?",'你最喜欢什么食物？'),('My favorite food is rice.','我最喜欢的食物是米饭。'),('My favorite food is pizza.','我最喜欢的食物是比萨饼。'),('I like apples.','我喜欢苹果。'),('I love ice cream.','我爱冰淇淋。'),("That’s my favorite, too!",'那也是我最喜欢的！')]
pages.append('<section><h1>Alan’s café · SENTENCE STRIPS</h1><p>Use the two word decks and pictures for matching. Personal choices have no wrong answer.</p>'+''.join('<div class="strip"><strong>'+esc(en)+'</strong><br>'+zh+'</div>' for en,zh in strips)+'</section>')
prompts=[('Draw an apple.','画一个苹果。'),('Draw a banana and an orange.','画一根香蕉和一个橙子。'),('Draw rice and eggs.','画米饭和鸡蛋。'),('Draw noodles and dumplings.','画面条和饺子。'),('Draw your favorite food.','画你最喜欢的食物。')]
pages.append('<section><h1>I SAY, YOU DRAW</h1><p>Read a prompt. Let Alan draw or arrange the picture cards, then compare together.</p>'+''.join('<div class="drawing"><strong>'+esc(en)+'</strong><br>'+zh+'<div></div></div>' for en,zh in prompts)+'</section>')
css='''@page{size:A4;margin:10mm}*{box-sizing:border-box}body{margin:0;color:#000;font-family:Body,Chinese,sans-serif}section{break-after:page;min-height:277mm}section:last-child{break-after:auto}h1{font-size:15pt;margin:0 0 3mm}p{font-size:9pt;margin:0 0 5mm}.cards{display:grid;grid-template-columns:repeat(3,1fr)}.card{height:80mm;border:1px dashed #000;display:flex;align-items:center;justify-content:center;padding:7mm;text-align:center;font-size:25pt;overflow-wrap:anywhere}.card img{max-width:100%;max-height:100%;filter:grayscale(1) contrast(1.15)}.strip{border:1px dashed #000;padding:4mm 5mm;margin-bottom:3mm;font-size:14pt;line-height:1.5}.drawing{height:48mm;border:1px dashed #000;padding:3mm;font-size:12pt}.drawing div{height:28mm}@media screen{body{max-width:190mm;margin:20px auto}section{background:white;margin-bottom:24px}}'''
fonts="@font-face{font-family:Body;src:url('"+uri('assets/fonts/Body.ttf')+"')}@font-face{font-family:Chinese;src:url('"+uri('assets/fonts/Chinese.otf')+"')}"
result='<!doctype html><html lang="en"><meta charset="utf-8"><title>Alan — Café Classroom Cards</title><style>'+fonts+css+'</style><body>'+''.join(pages)+'</body></html>'
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(result)
print('Created',len(pages),'print pages,',len(items),'matching picture/English/Chinese sets.')
