// Original hand-coded illustration. All coordinates use the world camera's units.
const W = 1060, H = 540;
function random(seed) {
  return () => ((seed = (Math.imul(1664525, seed) + 1013904223) >>> 0) / 4294967296);
}
function poly(c, color, points) {
  c.fillStyle = color;
  c.beginPath();
  points.forEach(([x,y],i) => i ? c.lineTo(x,y) : c.moveTo(x,y));
  c.closePath();
  c.fill();
}
function stroke(c,color,width,points) {
  c.strokeStyle=color; c.lineWidth=width; c.lineCap='round'; c.lineJoin='round';
  c.beginPath();
  points.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));
  c.stroke();
}
function oval(c,color,x,y,rx,ry) {
  c.fillStyle=color; c.beginPath(); c.ellipse(x,y,rx,ry,0,0,Math.PI*2); c.fill();
}
function gradient(c, y1, y2, colors) {
  const g=c.createLinearGradient(0,y1,0,y2);
  colors.forEach((color,i)=>g.addColorStop(i/(colors.length-1),color));
  return g;
}
function fir(c,x,y,s,colors,seed) {
  const r=random(seed);
  c.save(); c.translate(x,y); c.scale(s,s);
  poly(c,colors[0],[[-4,3],[3,3],[1,-147],[-1,-147]]);
  for(let i=0;i<10;i++){
    const height=-132+i*12, spread=8+i*3.2;
    const bough=[[-1,height-21],[-spread*.35,height-3],[-spread*.7,height+6],[-spread,height+12],
      [-spread*.34,height+11],[-spread*.62,height+18],[0,height+13],[spread*.70,height+17],
      [spread*.43,height+10],[spread,height+12],[spread*.45,height+3]];
    poly(c,colors[i%2],bough);
    stroke(c,colors[2],.75,[[-spread*.8,height+11],[-spread*.25,height+5],[0,height-1],[spread*.6,height+9]]);
    if (r()>.32) stroke(c,colors[2],.7,[[0,height+5],[spread*.38,height+14]]);
  }
  c.restore();
}
function layer(scene,name,paint) {
  const texture=scene.textures.createCanvas(name,W,H);
  paint(texture.context);
  texture.refresh();
  return scene.add.image(0,0,name).setOrigin(0);
}
export function illustratedWorld(scene) {
  const far=layer(scene,'far',(c)=>{
    c.fillStyle=gradient(c,0,333,['#15293c','#49616a','#e6b589']);
    c.fillRect(0,0,W,H);
    const glow=c.createRadialGradient(335,92,12,335,92,235);
    glow.addColorStop(0,'#fceaceb9'); glow.addColorStop(1,'#ffe0a100');
    c.fillStyle=glow; c.fillRect(0,0,W,360);
    oval(c,'#f5d8ad',335,89,24,24);
    const r=random(29);
    for(let i=0;i<22;i++) {
      const x=r()*W,y=70+r()*130;
      const mist=c.createRadialGradient(x,y,2,x,y,90+r()*90);
      mist.addColorStop(0,'#c7b49716');mist.addColorStop(1,'#e1b49700');
      c.fillStyle=mist;c.fillRect(x-180,y-120,360,240);
    }
    for(let row=0;row<4;row++){
      const y=156+row*43;
      const palette=[['#657c82','#647c82','#879696'],['#4b6a70','#56767a','#759294'],
        ['#355960','#3b6066','#53787c'],['#1d3a43','#244750','#395c62']][row];
      for(let x=-80;x<W+120;x+=13+row*9) fir(c,x+r()*24,y+r()*26,.25+row*.12+r()*.43,palette,x+200);
    }
  });
  const ground=layer(scene,'ground',(c)=>{
    const r=random(813);
    const shore=[[0,245],[75,239],[130,251],[225,253],[340,244],[437,229],[540,243],[641,251],
      [743,268],[863,294],[946,312],[1060,302]];
    const bank=[[0,339],[84,344],[155,364],[231,358],[306,362],[380,355],[458,346],[520,353],
      [597,364],[689,380],[777,404],[858,421],[940,413],[1060,382]];
    poly(c,gradient(c,195,352,['#29464a','#162f32','#263d36']),[[0,198],[W,188],...[...shore].reverse()]);
    poly(c,gradient(c,240,460,['#316d74','#245663','#213b48']),[...shore,...[...bank].reverse()]);
    stroke(c,'#92c2ad80',5,shore);
    stroke(c,'#7aa78f70',8,bank);
    poly(c,gradient(c,334,540,['#496553','#354b3d','#182f2d']),[...bank,[W,H],[0,H]]);
    const path=[[0,447],[85,418],[161,408],[224,412],[303,414],[376,398],[456,380],[524,389],
      [598,415],[681,434],[768,454],[850,470],[946,449],[1060,431]];
    stroke(c,'#242e2990',61,path);
    stroke(c,'#978367',47,path);
    stroke(c,'#ad967255',26,path.map(([x,y])=>[x,y-5]));
    for(let i=0;i<3100;i++){
      const x=r()*W,y=194+r()*346;
      const sample=line=>{
        const j=Math.min(line.length-1,line.findIndex(([at])=>at>=x));
        const [a,b]=[line[Math.max(0,j-1)],line[Math.max(0,j)]];
        return a[1]+(b[1]-a[1])*(x-a[0])/Math.max(1,b[0]-a[0]);
      };
      const near=sample(bank),far=sample(shore);
      if(y>near+4 || y<far-3) {
        const onPath=Math.abs(y-sample(path))<23;
        oval(c,onPath?'#ded1a431':['#142b2d72','#bcb48655','#667b50a0','#2e513a'][i%4],x,y,1+r()*5,.3+r()*2);
      } else if(y>far+6 && y<near-3 && i%3===0) {
        const size=Math.min(8+r()*35,W-x);
        stroke(c,['#a9d6c545','#1f425988','#d7dbad44','#58879488'][i%4],.6+r()*1.2,[[x,y],[x+size,y-.4]]);
      }
    }
    for(let i=0;i<30;i++) {
      const x=r()*W,y=207+r()*24;
      fir(c,x,y,.2+r()*.28,['#1b3738','#2e4d44','#5d7860'],i+12);
    }
    for(let i=0;i<92;i++){
      const x=r()*W,y=338+Math.max(0,x-450)*.13+r()*18;
      oval(c,'#172e2e68',x,y,4+r()*8,1+r()*2.5);
    }
    // White stones mark the diagonal ford on both banks.
    for(let i=0;i<9;i++){
      const x=946-i*4,y=411-i*12;
      oval(c,'#182d34',x+1,y+3,7+i%2,3);
      oval(c,'#aeb3a0',x,y,6+i%2,2.6);
      stroke(c,'#ece4c6',.9,[[x-3,y],[x+1,y-1],[x+4,y]]);
    }
    // Ranger shelter: lit timber walls, sloped roof, porch and stair treads.
    poly(c,'#222c2c',[[-8,385],[51,391],[173,378],[195,385],[165,401],[12,403]]);
    poly(c,'#594931',[[23,306],[140,303],[140,378],[23,386]]);
    poly(c,'#796142',[[140,303],[179,322],[179,367],[140,378]]);
    for(let y=312;y<382;y+=7) stroke(c,'#c4a36a60',1,[[24,y],[140,y-5],[178,y-14]]);
    poly(c,'#303b38',[[9,313],[45,261],[143,257],[189,321],[145,313]]);
    poly(c,'#627060',[[9,311],[45,261],[143,257],[122,298]]);
    for(let i=0;i<16;i++) stroke(c,i%2?'#384b46':'#89907b',1,[[46+i*5,264],[14+i*6,310-i*.8]]);
    poly(c,'#27302a',[[101,380],[101,329],[126,328],[126,379]]);
    c.fillStyle='#ecc38a'; c.fillRect(45,326,34,26);
    c.fillStyle='#b77e50'; c.fillRect(49,329,26,20);
    stroke(c,'#483d2c',2,[[62,327],[62,352]]);
    stroke(c,'#483d2c',2,[[46,339],[78,339]]);
    for(let i=0;i<3;i++) stroke(c,'#b19666',3,[[96-i*3,383+i*4],[134+i*3,381+i*4]]);
    // Lantern and hand painted insignia.
    oval(c,'#efb96531',135,333,14,18);
    c.fillStyle='#ffd595'; c.fillRect(133,330,5,8);
    poly(c,'#303b31',[[133,328],[136,324],[139,328]]);
  });
  const foreground=layer(scene,'foreground',(c)=>{
    const r=random(987);
    for(let i=0;i<210;i++){
      const x=r()*W,y=486+r()*72,l=4+r()*22;
      stroke(c,['#162e2b','#264237','#50704b','#6e7956'][i%4],.7+r()*1.6,[[x,y],[x+(r()-.5)*8,y-l*.66],[x+(r()-.5)*14,y-l]]);
    }
    fir(c,18,561,1.12,['#111f25','#172d31','#304640'],400);
    fir(c,1045,554,1.09,['#122026','#1b3132','#304a42'],834);
  });
  far.setScrollFactor(.90,1); ground.setDepth(0); foreground.setDepth(500).setScrollFactor(1.04,1);
  return scene.add.graphics().setDepth(5);
}

export function paintWorld(g, time, state) {
  g.clear();
  // Current follows the actual river, between the two uneven banks.
  for(let i=0;i<58;i++){
    const x=(i*71+time*(6+i%4))%1060;
    const axis=281+Math.max(x-440,0)*.14;
    const y=axis+(i*63%66)-21;
    const length=10+i%28;
    g.lineStyle(1,0xc1e7cd,.10+(i%4)*.033);
    g.lineBetween(x,y,x+length,y-.7);
  }
  // Low reeds sway separately from the trunks and trail.
  for(let i=0;i<78;i++){
    const x=17+(i*119)%1026,y=495+(i*29)%34,h=5+i%13;
    g.lineStyle(1+((i%3)===0),[0x83a174,0x60774d,0xa3ad72][i%3],.65);
    g.lineBetween(x,y,x+Math.sin(time*2+i)*2.8+(i%7)-3,y-h);
  }
  // Shelter lantern and fireflies at dusk, with a stable still state.
  g.fillStyle(0xeaba72,.06+.035*Math.sin(time*1.6));
  g.fillCircle(136,334,22);
  g.fillStyle(0xffd995,.19);
  g.fillCircle(136,334,7);
  for(let i=0;i<19;i++){
    const x=30+i*55+Math.sin(time*.55+i*5)*11;
    const y=416+(i*79)%90+Math.cos(i+time*.63)*9;
    g.fillStyle(0xf3dca2,.17+.16*(1+Math.sin(i*5+time*1.3)));
    g.fillCircle(x,y,i%4===0?1.5:1);
  }
  // Bridge geometry and repair sockets remain fixed throughout.
  const deck=[[407,349],[466,349],[472,226],[433,222]];
  g.fillStyle(0x142a31,.65); g.fillTriangle(407,361,481,355,476,228);
  for(let i=0;i<21;i++){
    const y=226+i*5.8;
    if ((i===16&&!state.pieces.includes('boardA'))||(i===17&&!state.pieces.includes('boardB'))) continue;
    const t=i/20,left=433-t*26,right=472-t*6;
    g.fillStyle(i===16||i===17?0xc9a367:[0x9b7751,0xa08459,0x826446][i%3]);
    g.fillRect(left,y,right-left,4.7);
    g.lineStyle(.5,0xe7c590,.7); g.lineBetween(left+1,y+1,right-2,y+1);
  }
  g.lineStyle(3,0x503c31); g.lineBetween(...deck[0],...deck[3]); g.lineBetween(...deck[1],...deck[2]);
  for(const [x,y] of [[406,347],[467,347],[416,305],[468,306],[427,260],[470,260],[433,226],[472,229]]){
    g.fillStyle(0x674e38); g.fillRect(x-2,y-12,4,13);
    g.fillStyle(0xc1a475); g.fillRect(x-2,y-13,4,2);
  }
  g.lineStyle(2,state.pieces.includes('rope')?0xe4c990:0x867658);
  g.lineBetween(406,335,433,213); g.lineBetween(467,334,472,216);
  // Rack, gauge and painted trail sign are interactive physical landmarks.
  g.fillStyle(0x5f4834); g.fillRect(89,403,45,17); g.fillRect(89,416,4,13); g.fillRect(130,415,4,14);
  g.fillStyle(0xcca977);
  if(!state.pieces.includes('boardA'))g.fillRect(85,403,48,4);
  if(!state.pieces.includes('boardB'))g.fillRect(88,410,49,4);
  if(!state.pieces.includes('rope')) { g.lineStyle(2,0xd9b07b); g.strokeEllipse(126,414,11,7); }
  g.fillStyle(0xddd4b0); g.fillRect(778,379,8,38);
  for(let i=0;i<7;i++){g.fillStyle(i%2?0x496368:0x86574c);g.fillRect(779,383+i*4,5,1);}
  g.fillStyle(0xa78559); g.fillTriangle(919,453,945,440,949,446); g.fillRect(938,447,14,5);
  for(const [key,x,y] of [['postA',947,413],['postB',914,309]]) {
    if(!state.pieces.includes(key)) continue;
    g.fillStyle(0x3d4030);g.fillRect(x,y-21,4,22);
    g.fillStyle(0x9ee9c6);
    const direction=key==='postA'?-1:1;
    g.fillTriangle(x+2,y-21,x+2+direction*16,y-17,x+2,y-13);
  }
  if(state.delivered){
    const phase=.55+.2*Math.sin(time*2);
    const x=state.route==='bridge'?451:931,y=state.route==='bridge'?242:315;
    g.fillStyle(0xbde8b6,phase*.19);g.fillCircle(x,y,16);
    g.fillStyle(0x423e2c);g.fillRoundedRect(x-9,y-3,18,9,3);
    g.fillStyle(0xeac686);g.fillRect(x-2,y-3,4,9);
    g.fillStyle(0xcaf0bf);g.fillCircle(x,y-7,3);
  }
}

export function figure(g,x,y,{ranger=false,step=0,face=1,pack=false}={}) {
  const d=Math.sin(step)*3;
  g.fillStyle(0x0e242b,.44);g.fillEllipse(x,y+1,24,7);
  g.lineStyle(4,0x283938);g.lineBetween(x-4,y-9,x-5+d,y-1);g.lineBetween(x+3,y-9,x+4-d,y);
  g.fillStyle(ranger?0xd29755:0x71a9a0);
  g.fillRoundedRect(x-8,y-26,16,18,5);
  g.fillStyle(ranger?0x66583e:0x98654a);g.fillRoundedRect(x-9*face-4,y-25,8,11,2);
  g.fillStyle(0xc99372);g.fillCircle(x+face,y-31,6);
  g.fillStyle(ranger?0xd3ae6f:0x382b37);
  if(ranger){g.fillEllipse(x,y-35,21,5);g.fillRoundedRect(x-6,y-40,12,7,2);}
  else g.fillRoundedRect(x-6,y-37,12,6,3);
  g.fillStyle(0xedd28e);g.fillRect(x+4*face,y-23,3,4);
  if(pack){g.fillStyle(0xae7b4d);g.fillRoundedRect(x+6,y-16,10,10,2);g.fillStyle(0xf9d58c);g.fillRect(x+10,y-16,2,10);}
}
