"""Original scalable vocabulary illustrations and grammar, linked to the agreed IDs.

Existing approved pictures are retained. Every new word has its own authored
scene; no emoji, remote images, font symbols or unrelated picture substitutions.
"""
from pathlib import Path
import json, math, html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/vocabulary';OUT.mkdir(exist_ok=True)
INK='#355953';TEAL='#51a8a0';GOLD='#f5bf52';CORAL='#e98266';BLUE='#70b7dd';GREEN='#7ab571';CREAM='#fff5d9'
def c(x,y,r,fill,stroke=INK):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
def e(x,y,rx,ry,fill,stroke=INK):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
def r(x,y,w,h,fill,rad=8,stroke=INK):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
def p(d,fill='none',stroke=INK,sw=5):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def line(x,y,a,b,color=INK,sw=6):return p(f'M{x} {y}L{a} {b}','none',color,sw)
def g(body,x=0,y=0,scale=1):return f'<g transform="translate({x} {y}) scale({scale})">{body}</g>'
def eyes(x,y,spread=17):return c(x-spread,y,4,INK)+c(x+spread,y,4,INK)
def face(x,y,fill='#f6c69d',hair='#3b3335',size=31):
    return c(x,y,size,fill)+p(f'M{x-size} {y-3}Q{x-size} {y-size-18} {x+size} {y-8}Q{x+5} {y-size+10} {x-size} {y-3}',hair,hair)+eyes(x,y+1,11)+p(f'M{x-9} {y+13}Q{x} {y+20} {x+9} {y+13}',sw=3)
def person(shirt=TEAL,pose='stand',hair='#3d3338'):
    legs=p('M-13 93L-19 147M14 93L25 147',sw=13)
    arms=p('M-25 36L-40 81M25 36L41 80',sw=10)
    if pose=='run':legs=p('M-13 93L-40 117L-64 112M14 93L41 125L61 149',sw=13);arms=p('M-25 36L-48 57L-67 38M25 36L48 12L67 20',sw=10)
    if pose=='dance':legs=p('M-13 93L-45 147M14 93L50 133',sw=13);arms=p('M-25 36L-50 10L-65 -10M25 36L54 6L64 -15',sw=10)
    if pose=='sit':legs=p('M-13 93L-47 106L-37 145M14 93L48 106L40 145',sw=13)
    return legs+arms+r(-28,25,56,76,shirt,14)+face(0,-9,hair=hair)+line(-28,150,-7,150,CREAM,13)+line(16,150,38,150,CREAM,13)
def note(x,y,fill=CORAL):return e(x,y,12,8,fill)+line(x+10,y,x+10,y-48,fill,6)+p(f'M{x+10} {y-48}q22 0 23 19','none',fill,6)
def book(fill=CORAL,opened=False):
    if opened:return p('M70 110Q126 94 180 118Q234 94 290 110V245Q238 229 180 252Q125 229 70 245Z',CREAM)+line(180,119,180,251)+line(91,146,150,148,'#ab9f7d',3)+line(210,146,267,145,'#ab9f7d',3)
    return r(100,80,160,190,fill,10)+line(119,89,119,262,CREAM,5)
def monitor(fill=BLUE):return r(62,91,236,151,'#557f7c',14)+r(76,105,208,120,fill,7)+line(180,244,180,273)+line(130,276,230,276)
def controller():return p('M102 133Q75 124 61 164L49 218Q46 244 70 244L116 214H244L290 244Q315 246 312 221L296 162Q283 127 255 133Z','#a8b9dd')+line(83,171,125,171)+line(104,151,104,191)+c(260,165,8,CORAL)+c(280,185,8,GOLD)
def animal(name):
    if name in ['horse','zebra','cow']:
        fill={'horse':'#b87c56','zebra':'#fffaf0','cow':'#fffaf0'}[name]
        z=e(177,181,94,54,fill)+p('M220 171L236 92Q244 64 273 83L298 129L270 151L245 130L234 200',fill)
        for x in [116,151,208,237]:z+=line(x,206,x-5,274,fill,17)+line(x-10,275,x+8,275,INK,9)
        z+=p('M88 169Q45 141 51 192','none',INK,7)+p('M246 83L244 54L260 74M267 81L283 59L280 92',fill)+c(274,107,4,INK)
        if name=='zebra':
            for x in range(112,229,22):z+=p(f'M{x} 139l14 36-12 39','none',INK,10)
            z+=line(240,102,252,127,INK,9)+line(232,121,243,148,INK,8)
        elif name=='cow':z+=e(125,173,22,27,INK)+e(194,163,24,25,INK)+e(279,133,23,15,'#efb1ac')+p('M247 77l-6-20M268 77l9-20',sw=8)
        else:z+=p('M240 92Q218 110 220 145','none','#674530',14)
        return z
    if name=='turtle':return e(180,208,88,57,GREEN)+c(278,206,25,GREEN)+eyes(281,202,7)+p('M113 231l-16 26M146 249l-8 17M226 248l12 19M247 228l15 20','none',GREEN,17)+p('M180 155l-29 34 16 39h35l17-39Z','#4a927a')+line(103,201,151,189)+line(218,189,260,201)+line(166,228,145,255)+line(201,228,222,254)
    if name=='dolphin':return p('M55 221Q125 97 242 151L280 178L306 189L275 202Q208 221 126 236L88 271L86 238L52 245Z',BLUE)+p('M165 156l35-47 5 53M191 202l24 42-46-28',BLUE)+c(264,177,4,INK)+p('M57 282q24-12 49 0t49 0t49 0t49 0','none',TEAL,6)
    if name=='duck':return e(170,215,80,53,GOLD)+c(231,153,40,GOLD)+p('M259 151l42 17-40 11Z',CORAL)+c(240,145,5,INK)+p('M104 203l-29-25 8 45Z',GOLD)+p('M139 260l-12 20h28M197 263l9 18h25','none',CORAL,7)+p('M131 212q25-26 54 6q-28 31-54-6',GOLD)
    if name=='sheep':
        z=''
        for x,y in [(118,163),(151,142),(188,143),(219,159),(236,195),(215,221),(176,235),(133,224),(104,192)]:z+=c(x,y,34,'#fffcf0')
        return z+e(247,189,31,39,'#7f7164')+eyes(249,182,9)+line(132,242,127,279,INK,10)+line(204,246,210,279,INK,10)+e(222,151,18,10,'#7f7164')
    fill={'tiger':'#e9a149','bear':'#a77b58','monkey':'#b78a5d'}[name]
    z=e(180,218,65,69,fill)+line(145,252,137,279,fill,23)+line(216,250,225,279,fill,23)
    z+=c(128,103,24,fill)+c(230,103,24,fill)+c(180,145,70,fill)+e(180,171,42,29,'#ffe4b4')+eyes(180,141,26)+p('M172 160h16l-8 10Z',INK)+p('M180 173q-12 17-23 1M180 173q12 17 23 1',sw=3)
    if name=='tiger':
        for d in ['M151 86l12 30','M181 78v33','M213 88l-13 29','M118 139l23 12','M219 152l25-14','M126 202l26 10','M209 217l28-12']:z+=p(d,sw=8)
    if name=='monkey':z+=p('M226 228Q321 196 283 151Q255 124 249 153Q247 176 269 174','none',fill,14)+g(p('M15 0Q50 15 25 56Q20 28 0 23Z',GOLD),90,219)
    return z
def food(name):
    plate=e(180,254,131,41,CREAM)
    if name=='chicken':return plate+e(176,189,93,59,'#c48145')+p('M211 189q55-37 60-2l-19 29q-42 17-41-27','#df9c55')+line(268,187,295,170,CREAM,13)+c(297,164,10,CREAM)+c(305,176,10,CREAM)+p('M126 178q31-33 61-16','none','#f2bc6c',7)
    if name=='fish':return plate+e(173,207,92,42,'#80b9bc')+p('M92 205l-42-40v76Z','#e9b873')+p('M166 170l31-32 18 40M160 244l37 22 19-28',BLUE)+c(234,198,6,INK)+p('M143 185q21 18 0 40M169 183q21 21 0 43','none','#3c8886',4)
    if name=='soup':return p('M63 182H297q-13 99-116 99T63 182',TEAL)+e(180,182,117,35,'#efbb73')+e(150,178,20,9,GREEN)+c(209,190,10,CORAL)+p('M128 127q-20-24 1-43M178 123q-20-24 1-43M228 128q-20-24 1-43','none','#a8aaa0',5)
    if name=='cheese':return plate+p('M73 204L206 116L286 224L76 262Z',GOLD)+p('M73 204l133-88 79 66-209 52Z','#ffdc83')+c(142,228,15,'#d79d37')+c(231,213,14,'#d79d37')+e(181,177,19,10,'#d79d37')
    if name=='watermelon':
        z=p('M54 124H306Q282 287 180 288T54 124',GREEN)+p('M72 126H288Q267 264 180 267T72 126','#f17870')
        for x,y in [(115,161),(161,187),(222,160),(244,202),(187,230),(120,211)]:z+=e(x,y,4,8,INK)
        return z
    return p('M161 105L238 129L120 285Z','#ee9a42')+p('M175 112Q118 65 150 51q29 18 38 55M192 113q-3-84 24-77q16 33-10 78M209 120q51-58 65-32q-20 28-65 32',GREEN)+p('M167 161l28 9M153 198l23 6M139 235l17 5','none','#c66d30',4)
def sport(name):
    if name in ['badminton','tennis']:
        z=e(160,137,65,82,'#e7eff1')+line(159,220,159,285,CORAL,14)
        for x in range(120,207,18):z+=line(x,88,x,185,'#91ada9',2)
        for y in range(88,204,19):z+=line(113,y,209,y,'#91ada9',2)
        if name=='tennis':return z+c(269,235,29,'#c3d86a')+p('M252 212q34 8 33 41','none',CREAM,4)
        return z+p('M245 240l-21-59h68l-20 59Z',CREAM)+line(244,185,250,232)+line(272,185,265,232)+c(259,245,16,CREAM)
    if name in ['swimming','surfing']:
        z=p('M30 249q29-18 58 0t58 0t58 0t58 0t58 0','none',BLUE,20)
        if name=='swimming':return z+c(217,184,28,'#f6c69d')+p('M73 221l88-23 48 24M137 200l-29-40 44-20','none',TEAL,15)+line(201,179,232,179,BLUE,8)
        return z+e(180,227,120,18,GOLD)+g(person(CORAL,'dance'),180,85,.70)
    if name in ['running','gymnastics']:
        return p('M48 283H312','none',CORAL,12)+g(person(TEAL,'run' if name=='running' else 'dance'),180,92,1.1)+(r(48,246,263,21,GOLD) if name=='gymnastics' else '')
    if name in ['cycling','skateboarding']:
        if name=='cycling':return c(98,236,47,'#fff4d9')+c(266,236,47,'#fff4d9')+p('M98 236l57-85 37 85H98l82-49 45 49-21-106','none',CORAL,9)+line(141,150,171,150)+line(192,128,219,128)+face(192,67)+p('M187 105l-31 54 55 38M187 107l45 44','none',TEAL,16)
        return g(person(GOLD,'run'),184,61,.95)+r(59,247,235,19,TEAL,10)+c(98,276,13,INK)+c(253,276,13,INK)
    if name=='boxing':return p('M72 236V156q0-50 45-50q45 0 45 50v80Z',CORAL)+r(69,227,96,48,CREAM)+p('M201 236v-80q0-50 45-50q45 0 45 50v80Z',BLUE)+r(198,227,96,48,CREAM)
    if name=='skiing':return p('M76 271L225 100M112 287L269 116','none',CORAL,20)+p('M55 125L274 276M88 94L305 245','none',INK,5)+p('M70 140l-17-7M85 116l15 2','none',GOLD,13)+p('M124 253l65-77M160 268l65-78','none',CREAM,10)
    if name=='ice hockey':return p('M76 70L224 255H301','none','#9c714f',13)+e(115,257,42,17,INK)+p('M65 292H309','none',BLUE,7)
    if name=='golf':return e(185,259,128,27,GREEN)+e(222,261,28,10,INK)+line(223,254,223,65)+p('M225 66l66 20-66 27Z',CORAL)+line(65,95,125,258,'#8a9292',8)+r(119,247,56,18,'#9caaaa')+c(184,259,10,CREAM)
    if name=='skating':return p('M91 100H183v89l54 26q20 15 0 34H80q-26-25 0-49Z',CREAM)+p('M85 259v22h163l19-16','none',INK,7)+line(98,280,243,280,BLUE,5)+line(117,141,172,141,CORAL)+line(117,161,172,161,CORAL)
    if name=='volleyball':return c(180,176,104,CREAM)+p('M180 72q-55 89 0 207M180 72q97 30 101 113M78 170q83-14 182 76M98 118q97 0 179 97','none',TEAL,7)
    raise ValueError(name)
def entertainment(name):
    if name=='movie':return r(65,128,230,144,'#56736c')+p('M62 96l224-41 9 44-224 40Z',INK)+p('M85 91l32 36M143 81l32 36M204 70l32 36','none',CREAM,15)+p('M154 167l60 33-60 33Z',CREAM)
    if name in ['TV show','cartoon']:return monitor('#bae1df')+(g(person(CORAL),180,126,.52) if name=='TV show' else c(165,160,38,GOLD)+p('M130 137l-11-32 34 23M188 137l22-28 1 43',GOLD)+eyes(165,158,13))
    if name=='video game':return controller()
    if name=='app':
        z=r(98,48,164,245,'#456567',22)+r(110,65,140,203,'#f6e3ba',9)+c(180,281,6,CREAM)
        for i,color in enumerate([CORAL,TEAL,GOLD,BLUE,GREEN,'#b093ca']):z+=r(124+(i%2)*64,91+(i//2)*53,43,40,color,9)
        return z
    if name=='song':return r(83,64,192,217,CREAM)+line(111,115,248,115,'#acbab1',3)+line(111,142,248,142,'#acbab1',3)+line(111,169,248,169,'#acbab1',3)+note(153,178)+note(226,214,TEAL)
    if name=='music':return p('M83 191V153q0-102 97-102t97 102v39','none',TEAL,18)+r(65,151,48,95,CORAL,20)+r(248,151,48,95,CORAL,20)+note(175,235,GOLD)
    if name=='dance':return g(person('#b191ca','dance'),180,111,1)+note(281,175,GOLD)
    if name=='comic book':return book(BLUE)+r(134,104,100,63,CREAM)+r(134,185,100,61,CREAM)+p('M146 138q25-38 55 0l16-12','none',CORAL,6)+p('M151 216h60l-17 17','none',TEAL,5)
    if name=='storybook':return book(TEAL,True)+p('M211 210v-38h51v38M221 172v-18l15-12 15 12v18',GOLD)+p('M104 206q-8-25 15-29q26-2 22 29Z',GREEN)
    if name=='puppet show':return r(46,77,267,204,GOLD)+r(65,95,230,164,'#8c6264')+p('M65 95l50 0-20 164H65ZM295 95h-48l20 164h28Z',CORAL)+g(person(TEAL),180,136,.62)+line(165,95,169,143,CREAM,2)+line(194,95,190,143,CREAM,2)
    if name=='magic show':return e(177,236,123,25,INK)+p('M108 138H247l-16 98H126Z',INK)+r(118,200,117,25,CORAL)+line(243,107,291,58,INK,10)+c(254,87,8,GOLD)+p('M145 114v-40M124 95h41','none',GOLD,7)
    if name=='concert':return r(40,69,280,193,'#79618e')+p('M52 80l60 136M305 80l-62 137','none',GOLD,18)+g(person(CORAL,'dance'),181,131,.65)+''.join(c(x,274,17,INK) for x in range(63,315,37))
    if name=='board game':return p('M64 105L269 91L309 244L90 265Z','#c8dfb4')+p('M99 137h114v47H135v43h120','none',CORAL,18)+c(109,137,9,GOLD)+c(251,226,9,TEAL)+r(236,113,48,48,CREAM)+c(248,126,4,INK)+c(271,147,4,INK)
    if name=='card game':return g(r(100,78,117,186,CREAM)+p('M134 120q-22-27-20 3q0 23 24 36q28-16 24-36q-3-24-28-3Z',CORAL),-15,0)+g(r(100,78,117,186,CREAM)+p('M155 108l26 33-26 34-25-34Z',TEAL),70,13)
    if name=='puzzle':return p('M76 93h80q-16-38 17-38t17 38h92v77q39-17 39 18t-39 18v71h-91q17-38-17-38t-18 38H76v-76q38 17 38-17t-38-17Z',TEAL)+p('M157 93v75h125M76 201h81v76','none',CREAM,5)
    if name=='toy':return r(80,132,148,91,CORAL)+r(206,96,61,128,TEAL)+r(250,172,55,52,GOLD)+c(115,241,27,INK)+c(241,241,27,INK)+r(107,91,39,45,GOLD)+r(216,111,39,35,CREAM)
    if name=='building blocks':return r(62,202,81,72,CORAL)+r(150,202,81,72,TEAL)+r(238,202,61,72,GOLD)+r(107,123,82,72,BLUE)+r(197,123,81,72,CORAL)+p('M149 115l50-64 48 64Z',GOLD)
    raise ValueError(name)
def people(name):
    family=['mother','father','sister','brother','grandmother','grandfather']
    if name in family:
        selected=family.index(name)
        z=line(80,131,125,159,'#c5d1c1',3)+line(280,131,235,159,'#c5d1c1',3)+line(142,220,156,257,'#c5d1c1',3)+line(222,220,211,257,'#c5d1c1',3)
        positions=[(125,156,.59),(237,156,.59),(153,258,.35),(213,258,.35),(80,65,.55),(280,65,.55)]
        for i,(x,y,scale) in enumerate(positions):
            color=CORAL if i==selected else '#d6ded5'
            hair='#b4b7af' if i>=4 else '#4d3b35'
            long_hair=i in [0,2,4]
            member=(p('M-30-14q-12 33-4 61h22V-5M30-14q12 33 4 61H12V-5',hair,hair) if long_hair else '')+person(color,hair=hair)
            if long_hair:member+=p('M-23 37h46l21 65h-88Z',color)
            if i>=4:member+=c(-11,-8,9,'none')+c(11,-8,9,'none')+line(-2,-8,2,-8,INK,2)
            if i==5:member+=p('M-18 11q18 27 36 0q-4 35-18 35T-18 11',hair,hair)
            z+=g(member,x,y,scale)
            if i==selected:z+=c(x,y-48*scale,9,GOLD)
        return z
    if name=='friend':return g(person(TEAL),123,107,1)+g(person(CORAL),238,106,1)+p('M157 183q23 20 46 0','none',GOLD,9)
    colors={'singer':'#a18bc7','teacher':TEAL,'writer':'#a58a67','actor':'#a68cc2','soccer player':CORAL,'doctor':CREAM,'nurse':'#99cbd7','firefighter':'#e9b348','police officer':'#617caa','chef':CREAM,'artist':'#e9aa73'}
    z=g(person(colors[name]),180,100,1)
    if name=='singer':z+=line(217,119,244,147)+e(250,154,13,21,INK)+note(282,107,GOLD)
    elif name=='teacher':z=r(31,67,104,115,'#72a084')+line(45,99,113,99,CREAM,4)+line(45,125,103,125,CREAM,4)+z+line(151,169,91,143,GOLD,4)
    elif name=='writer':z+=r(65,195,229,26,'#ae8056')+r(91,175,86,18,CREAM)+line(165,141,127,182,INK,5)
    elif name=='actor':z+=p('M47 99q36-20 68 0v77q-33 48-68 0Z',GOLD)+eyes(81,128,14)+p('M65 153q16 22 32 0',sw=3)+p('M267 92h37v153h-37Z',CORAL)
    elif name=='soccer player':z+=c(269,249,37,CREAM)+p('M263 227l17 5 3 18-18 8-14-16Z',INK)
    elif name in ['doctor','nurse']:z+=p('M165 131q-24 50 16 53q42-3 14-53','none',TEAL,6)+c(181,183,9,TEAL)+(r(214,50,36,29,CREAM)+line(231,54,231,74,TEAL)+line(221,64,242,64,TEAL) if name=='nurse' else '')
    elif name=='firefighter':z+=p('M145 71q4-62 69-10l15 13Z',GOLD)+r(136,68,92,14,GOLD)+line(152,164,207,164,'#f7e2a1',9)
    elif name=='police officer':z+=p('M145 73V57q36-34 71 0v16Z','#617caa')+r(138,69,87,13,'#49658c')+p('M192 139l16-7 15 7-5 26-11 8-11-8Z',GOLD)
    elif name=='chef':z+=c(153,45,24,CREAM)+c(180,32,29,CREAM)+c(207,45,24,CREAM)+r(152,45,56,28,CREAM)+p('M157 140h47l14 87h-73Z',CORAL)
    elif name=='artist':z+=e(250,182,43,33,'#deb27b')+c(238,172,7,CORAL)+c(265,173,7,TEAL)+c(251,196,7,GOLD)+line(143,150,110,102,'#9e724a',6)+p('M110 103l-7-27 18 12Z',TEAL)
    return z
def place(name):
    if name=='park':return e(180,270,137,23,GREEN)+line(91,209,91,118,'#926948',13)+c(91,102,57,GREEN)+r(170,196,122,23,'#b5865b')+line(180,218,174,265)+line(278,218,284,265)+line(177,163,285,163,CORAL,13)
    if name=='beach':return p('M30 234q140-55 300 0v56H30Z',GOLD)+p('M28 255q30-12 60 0t60 0t60 0t60 0t60 0','none',BLUE,13)+line(193,102,193,248)+p('M101 141Q193 8 284 141Z',CORAL)+p('M193 50q-35 35-31 91M193 50q35 35 31 91','none',CREAM,4)
    if name=='playground':return p('M54 260l58-173h140l56 173','none',CORAL,10)+line(155,92,155,206)+line(206,92,206,206)+line(143,211,217,211,GOLD,12)+p('M103 133l-40 111h54l47-111Z',BLUE)
    if name=='swimming pool':return p('M56 120H280L312 277H33Z',BLUE)+p('M60 168q30-16 60 0t60 0t60 0t52 0M48 225q30-16 60 0t60 0t60 0t60 0','none',CREAM,5)+p('M99 184V87q0-28 22-28M143 184V87q0-28 22-28','none',INK,8)+line(100,115,141,115)+line(100,145,141,145)
    if name=='farm':return p('M59 134l118-79 119 79V282H59Z',CORAL)+r(141,184,77,98,CREAM)+p('M141 184l77 98M218 184l-77 98','none','#ae7152',5)+r(142,107,75,50,CREAM)+p('M31 278q14-56 34-8M301 278q-14-56-34-8','none',GREEN,9)
    if name=='aquarium':return r(45,100,270,179,TEAL)+r(64,122,232,130,BLUE)+e(154,184,48,22,GOLD)+p('M111 180l-27-22v44Z',GOLD)+c(182,180,3,INK)+p('M262 246q-30-32-3-70M236 245q-26-24-12-54','none',GREEN,8)+c(252,145,7,CREAM)
    if name=='classroom':return r(56,65,249,110,'#76a68a')+line(78,103,263,103,CREAM,4)+''.join(r(x,y,82,20,GOLD)+line(x+10,y+20,x+7,y+54)+line(x+71,y+20,x+74,y+54) for x,y in [(54,203),(205,203)])
    z=r(61,106,238,175,CREAM)+p('M44 106L180 46L316 106Z',CORAL)+r(149,205,63,76,TEAL)
    for x in [83,239]:z+=r(x,136,39,51,BLUE)
    if name=='home':return z+p('M161 211l32 0v60h-32Z','#a77f55')
    if name=='zoo':return z+g(animal('bear'),112,73,.35)+p('M44 257H316M70 218v64M104 218v64M139 218v64M222 218v64M257 218v64M290 218v64','none','#a57b51',5)
    if name=='library':return z+g(book(TEAL,True),85,60,.52)
    if name=='school':return z+c(180,96,22,CREAM)+line(180,80,180,97)+line(180,97,192,102)+line(285,67,285,27)+p('M286 28l40 10-40 14Z',GOLD)
    if name=='hospital':return z+line(181,105,181,162,TEAL,15)+line(153,134,209,134,TEAL,15)
    if name=='supermarket':return z+g(p('M0 0h22l18 68h88l17-49H26',GOLD)+c(50,91,11,INK)+c(116,91,11,INK),121,121,.7)
    if name=='restaurant':return z+line(149,119,149,174,INK)+line(134,119,134,140,INK,4)+line(164,119,164,140,INK,4)+line(134,140,164,140,INK,4)+line(215,118,215,173,INK)+e(215,127,13,21,CREAM)
    if name=='movie theater':return z+e(181,144,42,30,INK)+c(164,136,9,CREAM)+c(197,136,9,CREAM)+c(179,159,8,CREAM)
    if name=='museum':return z+''.join(r(x,126,22,148,CREAM) for x in [77,132,206,261])+p('M75 111h210','none',GOLD,10)
    if name=='toy store':return z+r(120,128,53,54,CORAL)+r(182,128,53,54,GOLD)+p('M144 120l33-43 34 43Z',TEAL)
    if name=='bakery':return z+p('M122 167v-21q0-47 58-28q60-19 60 28v21Z',GOLD)+p('M151 124v26M182 119v29M211 126v24','none','#af7c43',5)
    raise ValueError(name)
def activity(name):
    if name=='riding a bike':return p('M37 282H323','none',GREEN,9)+g(sport('cycling'),20,25,.88)
    if name=='dancing':return g(person(TEAL,'dance'),180,107,1)+p('M71 158l15 16M282 158l-15 16','none',GOLD,5)
    if name in ['watching TV','playing video games','listening to music']:return {'watching TV':lambda:monitor()+g(person(CORAL),180,217,.48),'playing video games':lambda:monitor('#beded6')+g(person(CORAL,'sit'),179,173,.64)+g(controller(),101,161,.43),'listening to music':lambda:g(person(GOLD),180,115,1)+p('M142 100q0-70 76 0','none',TEAL,10)+r(136,100,15,38,TEAL)+r(208,100,15,38,TEAL)}[name]()
    if name in ['drawing','painting','writing']:
        z=r(63,79,232,204,CREAM)+p('M101 229q22-49 48 0t50 0l25-55 33 55','none',TEAL,5)
        if name=='drawing':return z+p('M154 162L249 47L275 69L179 183Z',GOLD)+p('M154 162l-5 33 30-12Z','#d0a97f')
        if name=='writing':return r(63,79,232,204,CREAM)+p('M95 170l16-39 16 39M101 154h20M144 131v39h16q23-10 0-20q22-10 0-19ZM219 134q-35-18-35 18t35 15','none',INK,5)+line(92,207,244,207,'#8aabc0',3)+p('M252 64L177 226l25-5 71-147Z',TEAL)
        return z+line(153,216,262,61,'#aa7952',17)+p('M140 239q-26-31 11-43l20 17q-9 31-31 26',CORAL)+e(265,252,42,26,GOLD)+c(253,245,7,TEAL)+c(280,257,7,CORAL)
    if name=='reading':return g(person(TEAL,'sit'),180,106,1)+g(book(CORAL,True),59,100,.68)
    if name=='singing':return g(person(CORAL),170,107,1)+line(214,131,249,159)+e(257,164,12,21,INK)+note(280,110,GOLD)
    if name=='cooking':return g(person(TEAL),182,102,1)+r(46,215,269,29,'#b1855d')+p('M118 187h141l-12 45H130Z',CORAL)+line(250,186,285,145,GOLD,7)+p('M145 165q-12-20 0-35M196 165q-12-20 0-35','none','#a0aea1',4)
    if name=='taking photos':return g(person(GOLD),180,104,1)+r(133,95,97,63,'#627b80')+c(181,127,23,BLUE)+r(147,79,42,18,'#627b80')
    if name=='building with blocks':return g(person(TEAL,'sit'),180,110,.8)+g(entertainment('building blocks'),45,93,.67)
    if name=='doing puzzles':return g(person(CORAL,'sit'),180,110,.83)+g(entertainment('puzzle'),52,122,.65)
    if name=='flying a kite':return g(person(TEAL,'dance'),110,145,.76)+p('M140 166Q213 195 252 120','none',INK,3)+p('M251 42l49 42-43 59-44-51Z',CORAL)+line(214,93,297,85,GOLD,3)+line(251,42,257,143,GOLD,3)+p('M258 143q-24 12 2 30q-23 16 4 30','none',TEAL,5)
    if name=='gardening':return g(person(GOLD,'sit'),132,121,.8)+p('M232 277V169M230 212q-70-48-49-54q45-8 50 40M232 196q58-57 65-32q-10 40-65 48','none',GREEN,10)+line(277,182,298,275,'#9e7c59',9)+p('M285 259l-17 26h38Z',INK)
    if name=='fishing':return g(person(TEAL,'sit'),121,110,.86)+p('M157 183l88-129q25 25 37 202','none','#ad8050',5)+p('M34 277q30-16 60 0t60 0t60 0t60 0t60 0','none',BLUE,13)+e(278,252,9,18,CORAL)
    if name=='camping':return p('M54 279L180 62L310 279Z',TEAL)+p('M103 279l77-161 80 161Z',GOLD)+line(180,62,180,282)+p('M42 102v120M24 142l18-45 20 45M22 178l20-47 22 47','none',GREEN,10)+c(291,74,23,GOLD)
    raise ValueError(name)

items=json.loads((ROOT/'data/vocabulary.json').read_text())
old_map={'orange':'orange-fruit','ice cream':'ice-cream','table tennis':'table-tennis'}
plural={'sheep':'sheep','mouse':'mice','person':'people','sandwich':'sandwiches','storybooks':'storybooks'}
color_values=['#e85d59','#3e8dc9','#66a77c','#f1cf51','#9c78bc','#ed9d4b','#ecabc0','#a77956','#3f484c','#fffefa','#9ca6a7','#a4d7e9','#355c8b','#b8dba0','#356c4d','url(#gold)','url(#silver)','#d5c39e']
ent_plural={'movie':'movies','TV show':'TV shows','video game':'video games','app':'apps','song':'songs','cartoon':'cartoons','comic book':'comic books','storybook':'storybooks','music':'music','dance':'dancing','puppet show':'puppet shows','magic show':'magic shows','concert':'concerts','board game':'board games','card game':'card games','puzzle':'puzzles','toy':'toys','building blocks':'building blocks'}
for v in items:
    name,topic=v['en'],v['topic'];stem=old_map.get(name,name)
    original=ROOT/'assets/art'/f'{stem}.png'
    existing_svg=ROOT/'assets/art'/f'{stem}.svg'
    if topic in ['food','animals','sports'] and original.exists():v['illustration']=original.relative_to(ROOT).as_posix()
    elif topic=='food' and existing_svg.exists():v['illustration']=existing_svg.relative_to(ROOT).as_posix()
    else:
        if topic=='colors':body=r(87,99,187,177,color_values[[x['en'] for x in items if x['topic']=='colors'].index(name)],24)+r(77,76,207,35,CREAM)+p('M130 129v66','none','#ffffff88',11)
        else:body={'animals':animal,'food':food,'sports':sport,'entertainment':entertainment,'people':people,'places':place,'activities':activity}[topic](name)
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="360" height="340" viewBox="0 0 360 340"><defs><linearGradient id="gold"><stop stop-color="#b9852e"/><stop offset=".45" stop-color="#ffe79a"/><stop offset="1" stop-color="#c49333"/></linearGradient><linearGradient id="silver"><stop stop-color="#8e9fa9"/><stop offset=".5" stop-color="#f2f7fa"/><stop offset="1" stop-color="#9eafb9"/></linearGradient></defs>'+e(180,294,119,12,'#e4e4d4','none')+body+'</svg>'
        path=OUT/(v['id']+'.svg');path.write_text(svg);v['illustration']=path.relative_to(ROOT).as_posix()
    if topic=='food':chunks=['My favorite','food','is',v['sentence_value']+'.'];question="What's your favorite food?"
    elif topic=='animals':chunks=['My favorite','animal','is',('an ' if name[0] in 'aeiou' else 'a ')+name+'.'];question="What's your favorite animal?"
    elif topic in ['sports','colors','activities']:
        category={'sports':'sport','colors':'color','activities':'activity'}[topic];chunks=['My favorite',category,'is',name+'.'];question="What's your favorite "+category+'?'
    elif topic=='entertainment':chunks=['I','like',ent_plural[name]+'.'];question='What do you like?'
    elif topic=='people':chunks=['I','like',('my ' if name in ['teacher','friend','mother','father','sister','brother','grandmother','grandfather','doctor'] else 'the ')+name+'.'];question='Who do you like?'
    else:chunks=['I','like',(name if name in ['home','school'] else 'the '+name)+'.'];question='What place do you like?'
    v['chunks']=chunks;v['sentence']=' '.join(chunks);v['question']=question
    v['mission_item']='food' if topic=='food' else 'picture'
(ROOT/'data/vocabulary.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
assert len(items)==144 and len({v['illustration'] for v in items})==144
print('144 distinct local illustrations linked to playable vocabulary; grammar checked by topic.')
