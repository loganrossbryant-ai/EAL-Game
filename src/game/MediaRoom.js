import Phaser from 'phaser';

const W = 1280, H = 780;
const TARGETS = [
  { id: 'noticeboard', label: 'Read the community notice', x: 260, y: 220, approach: { x: 230, y: 460 } },
  { id: 'laptop', label: 'Open the campaign website', x: 440, y: 300, approach: { x: 430, y: 465 } },
  { id: 'editor', label: 'Talk to Maya', x: 850, y: 385, approach: { x: 855, y: 535 } },
  { id: 'inbox', label: 'Read the volunteer email', x: 970, y: 340, approach: { x: 1020, y: 515 } },
  { id: 'door', label: 'Step into the courtyard', x: 1210, y: 300, approach: { x: 1166, y: 518 } },
];
const COURTYARD_TARGETS = [{id:'return',label:'Return to the newsroom',x:184,y:332,approach:{x:193,y:514}}];
const OBSTACLES = [
  { x: 0, y: 0, w: 140, h: 470 },
  { x: 300, y: 0, w: 420, h: 435 },
  { x: 745, y: 0, w: 315, h: 455 },
];
const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
let seed = 491;
const random = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

function roomTexture() {
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d');
  function rect(x,y,w,h,color) { g.fillStyle=color;g.fillRect(x,y,w,h); }
  function line(x,y,x2,y2,color,width=1) { g.strokeStyle=color;g.lineWidth=width;g.beginPath();g.moveTo(x,y);g.lineTo(x2,y2);g.stroke(); }
  function poly(points,color) { g.fillStyle=color;g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.fill(); }
  function ellipse(x,y,rx,ry,color) {g.fillStyle=color;g.beginPath();g.ellipse(x,y,rx,ry,0,0,Math.PI*2);g.fill();}
  function text(s,x,y,size,color,font='sans-serif',align='left') {g.font=`${size}px ${font}`;g.fillStyle=color;g.textAlign=align;g.fillText(s,x,y);g.textAlign='left';}
  function rounded(x,y,w,h,r,color) {g.fillStyle=color;g.beginPath();g.roundRect(x,y,w,h,r);g.fill();}
  function shadow(x,y,rx,ry,alpha=.25) {const grad=g.createRadialGradient(x,y,0,x,y,rx);grad.addColorStop(0,`rgba(7,15,16,${alpha})`);grad.addColorStop(1,'rgba(7,15,16,0)');g.save();g.translate(x,y);g.scale(1,ry/rx);g.fillStyle=grad;g.fillRect(-rx,-rx,rx*2,rx*2);g.restore();}

  const wall=g.createLinearGradient(0,0,W,420);wall.addColorStop(0,'#50605a');wall.addColorStop(.5,'#76786a');wall.addColorStop(1,'#394b49');rect(0,0,W,H,wall);
  // A quiet, old school newsroom. The architecture is hand drawn and fully local.
  rect(0,0,W,18,'#273e3b');rect(0,18,W,7,'#a49a77');rect(0,25,W,6,'#3b4c45');
  for(let y=38;y<388;y+=23) for(let x=-60+(Math.floor(y/23)%2)*54;x<W;x+=108) {
    rect(x+1,y+1,105,20,`rgba(212,196,157,${.014+random()*.025})`);
    line(x,y,x+106,y,'rgba(18,36,33,.045)');
  }
  // Left return and right return walls create an architectural frame.
  poly([[0,25],[83,62],[83,389],[0,443]],'#344c46');
  poly([[1232,29],[1280,10],[1280,448],[1232,390]],'#293f3d');
  rect(82,51,1150,8,'#374a43');rect(82,60,1150,4,'#a59f80');
  rect(81,355,1152,35,'#4c5146');rect(80,355,1155,7,'#aaa082');rect(80,388,1157,13,'#273a33');
  for(let x=87;x<1230;x+=90) {rect(x,365,83,23,'#474b40');rect(x+3,368,76,17,'#555647');}
  // Two enormous windows, distant town and hazy afternoon sun.
  function windowArt(x,y,w,h) {
    shadow(x+w/2+8,y+h/2+10,w*.7,h*.7,.3);
    rect(x-12,y-12,w+24,h+25,'#273f39');rect(x-7,y-8,w+14,h+14,'#b4ab8b');
    const sky=g.createLinearGradient(x,y,x+w,y+h);sky.addColorStop(0,'#d4dfd0');sky.addColorStop(.5,'#c0cfc0');sky.addColorStop(1,'#e0c28b');rect(x,y,w,h,sky);
    for(let i=0;i<13;i++) {const bx=x+i*w/11-12,bh=35+random()*70;rect(bx,y+h-15-bh,25+random()*20,bh,'#899b8d');for(let yy=y+h-bh;yy<y+h-20;yy+=12)rect(bx+5,yy,3,6,'#b8c6ad');}
    for(let i=0;i<14;i++) {const bx=x+random()*w,by=y+h-30+random()*20;ellipse(bx,by,20+random()*20,30+random()*18,'rgba(68,96,72,.45)');}
    rect(x,y+h-15,w,15,'#87917d');
    const glare=g.createLinearGradient(x,y,x+w,y+h);glare.addColorStop(0,'rgba(255,245,199,.24)');glare.addColorStop(.5,'rgba(255,249,213,.02)');glare.addColorStop(1,'rgba(255,246,186,.23)');rect(x,y,w,h,glare);
    for(let xx=1;xx<3;xx++){rect(x+w*xx/3-4,y,8,h,'#485e50');rect(x+w*xx/3-3,y,2,h,'#bab797');}
    rect(x,y+h*.52-4,w,8,'#4a6154');rect(x,y+h*.52-3,w,2,'#c7bfa0');
    rect(x-14,y+h+6,w+28,10,'#a29a7b');rect(x-15,y+h+16,w+31,6,'#35473c');
    // Unrolled blinds and its cord.
    rect(x-8,y-8,w+16,14,'#c7b998');for(let yy=y-7;yy<y+7;yy+=3)line(x-6,yy,x+w+7,yy,'#948e73');
    line(x+w+7,y+2,x+w+7,y+h*.6,'#d4c49a',1);ellipse(x+w+7,y+h*.6,2,5,'#e0cd9e');
  }
  windowArt(353,86,271,237); windowArt(664,86,271,237);
  // Ceiling fixtures and overhead utility conduits.
  line(103,46,1210,46,'#253a35',4);line(1008,47,1008,87,'#243a35',3);
  ellipse(1008,88,48,11,'#263c38');poly([[960,87],[976,61],[1041,61],[1056,87]],'#2a423c');ellipse(1008,88,37,5,'#d6bb81');
  // Perspective oak boards.
  const floor=g.createLinearGradient(0,385,0,H);floor.addColorStop(0,'#726f52');floor.addColorStop(.34,'#8d8060');floor.addColorStop(1,'#655b47');
  poly([[0,440],[82,395],[1232,395],[1280,442],[1280,H],[0,H]],floor);
  for(let i=-10;i<25;i++) {
    let topx=640+(i*74-640)*.65,botx=640+(i*74-640)*1.55;
    poly([[topx,398],[topx+45,398],[botx+111,H],[botx,H]],i%2?'rgba(221,192,137,.055)':'rgba(28,29,22,.025)');
    line(topx,399,botx,H,'rgba(28,35,26,.25)',1);
    for(let j=0;j<4;j++) line(topx+8+j*8,403,botx+15+j*20,H,'rgba(226,201,147,.035)',1);
  }
  const rows=[405,427,455,490,533,586,651,729];
  rows.forEach((yy,i)=>{line(0,yy,W,yy,'rgba(27,36,27,.22)');for(let x=(i%2)*120;x<W;x+=244)line(x,yy,x+3,rows[i+1]||H,'rgba(18,28,20,.17)');});
  // Afternoon window projections, long and softly warmed.
  g.save();g.globalCompositeOperation='screen';
  poly([[366,399],[619,399],[993,780],[618,780]],'rgba(229,195,115,.18)');
  poly([[677,399],[922,399],[1280,750],[1085,780]],'rgba(232,195,112,.15)');
  for(let i=1;i<3;i++){poly([[366+i*83,399],[373+i*83,399],[637+i*119,780],[625+i*119,780]],'rgba(16,31,24,.18)');}
  g.restore();
  // Threadbare newsroom rug.
  poly([[566,485],[892,485],[1039,698],[499,698]],'#384e49');
  poly([[577,495],[882,495],[1020,687],[515,687]],'#627064');
  poly([[588,506],[876,506],[998,674],[531,674]],'#455953');
  for(let yy=513;yy<675;yy+=7)line(540+(675-yy)*.31,yy,992-(675-yy)*.7,yy,'rgba(193,180,137,.07)');
  for(let i=0;i<24;i++){let xx=518+i*21;line(xx,694,xx-3,703,'#8b8b70');}
  // Corkboard with layered campaign papers.
  shadow(238,275,130,120,.25);rect(128,155,208,205,'#342e23');rect(135,162,194,190,'#a0895e');rect(140,167,184,180,'#9e865b');
  for(let i=0;i<2200;i++)rect(141+random()*181,167+random()*180,1,1,random()>.5?'#af9568':'#8e7854');
  g.save();g.translate(147,182);g.rotate(-.06);rect(2,3,69,89,'rgba(32,31,23,.2)');rect(0,0,69,89,'#e1d7bb');rect(6,9,57,24,'#738c78');text('VOLUNTEER',6,47,7,'#34483c');for(let i=0;i<4;i++)rect(6,54+i*6,52-i*4,1,'#989784');g.restore();
  g.save();g.translate(215,196);g.rotate(.035);rect(3,4,92,128,'rgba(32,31,23,.3)');rect(0,0,92,128,'#ede4c9');rect(0,0,92,21,'#a94d38');text('HELP STARTS',46,14,9,'#fff1cc','sans-serif','center');text('HERE.',46,41,19,'#374f40','serif','center');rect(9,49,74,38,'#b2b89a');ellipse(44,67,11,9,'#e2cb9d');text('ONE CLICK.',46,99,8,'#4b5345','sans-serif','center');text('REAL CHANGE?',46,113,8,'#4b5345','sans-serif','center');g.restore();
  ellipse(151,183,3,3,'#a54430');ellipse(260,199,3,3,'#ad4930');rect(158,294,41,34,'#d4c07c');text('Verify',162,307,8,'#615a3e');text('the source!',161,318,7,'#615a3e');
  // Clock and wall lettering.
  ellipse(1059,119,30,31,'#243c36');ellipse(1059,119,26,27,'#d7d4bb');ellipse(1059,119,23,24,'#e0dcc1');
  for(let i=0;i<12;i++){const a=i*Math.PI/6;line(1059+Math.sin(a)*20,119-Math.cos(a)*20,1059+Math.sin(a)*23,119-Math.cos(a)*23,'#54604e',1.5);}
  line(1059,119,1074,119,'#354b3e',2);line(1059,119,1054,104,'#354b3e',3);ellipse(1059,119,2,2,'#a65c3f');
  text('THE RIVERSIDE',1004,214,10,'#b1b497','sans-serif');text('CHRONICLE',1002,239,22,'#d1ceb0','serif');line(1003,248,1161,248,'#a39f7f');text('ASK. VERIFY. TELL THE STORY.',1005,263,7.5,'#b0b198');
  // Bookshelf with dozens of individual journals and books.
  rect(1131,284,91,139,'#263d37');rect(1138,291,76,122,'#394b3e');
  for(let row=0;row<3;row++) {const yy=295+row*38;rect(1137,yy+32,78,6,'#8c8260');let bx=1141;for(let k=0;k<9;k++){const bw=5+random()*5,bh=21+random()*9;const colors=['#bcb38a','#6c8071','#98694e','#d0c49b','#455f57'];rect(bx,yy+32-bh,bw,bh,colors[k%5]);rect(bx+1,yy+32-bh+3,bw-2,1,'rgba(245,225,172,.4)');bx+=bw+1;if(bx>1205)break;}}
  rect(1129,281,96,8,'#8c8061');
  // The onward doorway stays visible in the room and opens after publication.
  rect(1123,145,102,258,'#253c36');rect(1131,153,86,245,'#a19470');rect(1138,161,71,235,'#566355');
  rect(1145,169,57,100,'#849381');rect(1149,173,49,92,'#a6b49a');
  for(let i=0;i<8;i++){const yy=182+i*10;rect(1149,yy,49,2,'rgba(56,87,60,.15)');}
  rect(1150,286,47,73,'#485b4b');rect(1155,292,37,61,'#506451');
  ellipse(1197,300,4,4,'#d8ba78');rect(1140,120,70,17,'#d1c59a');text('COURTYARD',1175,132,8,'#384f3e','sans-serif','center');
  rect(1126,399,96,6,'#b5a47a');
  // Plants, with individually shaded fronds.
  function plant(x,y,s=1) {
    shadow(x,y+6,40*s,12*s,.3);poly([[x-17*s,y-37*s],[x+18*s,y-37*s],[x+13*s,y+3*s],[x-12*s,y+3*s]],'#ac7650');
    ellipse(x,y-37*s,18*s,5*s,'#c7976c');ellipse(x,y-37*s,14*s,3*s,'#4b4431');
    for(let k=0;k<11;k++){const endx=x+(random()-.5)*81*s,endy=y-(62+random()*67)*s;g.strokeStyle='#3d6043';g.lineWidth=2*s;g.beginPath();g.moveTo(x,y-35*s);g.quadraticCurveTo(x+(endx-x)*.2,endy,endx,endy);g.stroke();g.save();g.translate(endx,endy);g.rotate((endx-x)*.025);ellipse(0,0,8*s,20*s,k%2?'#5c7951':'#385c40');line(0,12*s,0,-14*s,'rgba(194,199,127,.3)');g.restore();}
  }
  plant(90,447,.95);plant(1183,448,1.12);plant(679,369,.52);
  // Radiators beneath the windows.
  for(let xx=372;xx<608;xx+=13){rounded(xx,350,10,40,3,'#878b72');rect(xx+1,352,2,35,'#a5a88b');}rect(364,347,250,5,'#9a9d82');
  // Work desk, aged oak surface, drawers, keyboard and readable display.
  function desk(x,y,w) {
    shadow(x+w/2+12,y+78,w*.63,32,.45);
    poly([[x+3,y+23],[x+w-2,y+23],[x+w+10,y+92],[x+w-2,y+94],[x+w-13,y+38],[x+17,y+38],[x+5,y+94],[x-5,y+93]],'#3d4132');
    poly([[x+8,y+26],[x+70,y+26],[x+62,y+85],[x+8,y+85]],'#666044');
    for(let yy=y+34;yy<y+83;yy+=17){rect(x+12,yy,45,14,'#746b4c');rect(x+31,yy+5,12,2,'#343f31');}
    poly([[x,y],[x+w-8,y],[x+w+17,y+37],[x-17,y+37]],'#a39169');
    poly([[x-17,y+37],[x+w+17,y+37],[x+w+17,y+45],[x-17,y+45]],'#6b6044');
    for(let i=0;i<22;i++){let yy=y+1+i*1.6;line(x+3-(i*.6),yy,x+w-7+(i*.8),yy,'rgba(230,199,139,.09)');}
  }
  desk(330,411,215);
  // Laptop and its light reflected in the table.
  poly([[389,374],[474,374],[480,420],[394,420]],'#243735');poly([[394,379],[468,379],[473,413],[398,413]],'#849c8c');
  rect(399,383,68,7,'#e4e5ce');text('GIVEFORWARD',403,389,4,'#2e6050');poly([[401,395],[468,395],[470,409],[403,409]],'#b9c4a3');text('Make a difference.',408,402,5,'#2c5644');
  poly([[394,420],[480,420],[496,434],[380,434]],'#a0a49a');poly([[399,422],[477,422],[487,430],[391,430]],'#364946');
  for(let yy=423;yy<430;yy+=2)line(399,yy,481,yy,'#728078');
  rect(382,434,113,2,'#344840');
  // Coffee cup, newspaper, pencils, headset.
  ellipse(517,427,10,4,'#c2b68d');rect(508,414,16,13,'#dad2b0');ellipse(516,414,8,3,'#ece0b8');ellipse(516,415,6,2,'#524b32');g.strokeStyle='#d9cba2';g.lineWidth=3;g.beginPath();g.arc(525,420,5,-Math.PI/2,Math.PI/2);g.stroke();
  poly([[337,419],[365,417],[381,433],[350,435]],'#d4cdb1');for(let i=0;i<4;i++)line(345+i*2,423+i*2,369+i*2,422+i*2,'#959782');
  desk(958,398,158);
  // Desktop inbox, document stack and reading lamp.
  poly([[987,412],[1044,412],[1059,431],[977,431]],'#394b42');poly([[991,404],[1041,404],[1051,424],[983,424]],'#dbd6bb');for(let i=0;i<5;i++)line(994+i,410+i*2,1039+i,410+i*2,'#9a9e88');
  poly([[1000,402],[1042,402],[1045,416],[997,416]],'#e9e0c3');line(1000,402,1022,411,'#a6a891');line(1042,402,1022,411,'#a6a891');
  ellipse(1090,419,16,5,'#34463c');line(1090,416,1098,370,'#344a3e',5);line(1098,371,1075,354,'#344a3e',4);poly([[1055,362],[1071,343],[1089,359]],'#344d40');ellipse(1074,361,18,5,'#f5d998');
  const lampglow=g.createRadialGradient(1069,409,0,1069,409,65);lampglow.addColorStop(0,'rgba(255,222,148,.2)');lampglow.addColorStop(1,'rgba(255,222,148,0)');ellipse(1069,409,65,36,lampglow);
  // Stools pushed beneath worktops.
  ellipse(355,494,24,9,'rgba(17,27,21,.18)');line(347,467,339,501,'#313f36',4);line(371,467,376,501,'#313f36',4);ellipse(359,466,23,9,'#535f48');ellipse(359,463,23,8,'#7a8062');
  // Foreground editorial table, cropped purposefully like an adventure-game set.
  shadow(102,753,255,75,.4);poly([[0,679],[164,693],[263,780],[0,780]],'#4c4e3b');poly([[0,660],[177,679],[293,780],[0,780]],'#9f8c63');
  for(let i=0;i<8;i++)line(0,667+i*10,216+i*9,780,'rgba(238,209,151,.1)');
  g.save();g.translate(43,696);g.rotate(.21);rect(0,0,81,64,'#d9d1b0');text('THE CHRONICLE',5,11,7,'#485343','serif');rect(5,16,31,23,'#8b9a82');for(let i=0;i<6;i++)rect(41,17+i*5,31,1,'#919580');for(let i=0;i<3;i++)rect(5,47+i*5,66,1,'#919580');g.restore();
  // Dust motes and atmospheric, cinematic edge falloff.
  for(let i=0;i<100;i++){const x=350+random()*700,y=80+random()*540;ellipse(x,y,.5+random(),.5+random(),'rgba(248,225,166,.18)');}
  const vignette=g.createRadialGradient(650,360,210,650,360,760);vignette.addColorStop(0,'rgba(10,24,21,0)');vignette.addColorStop(.68,'rgba(10,24,21,.06)');vignette.addColorStop(1,'rgba(7,18,17,.55)');rect(0,0,W,H,vignette);
  return c;
}

function courtyardTexture(){
  const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');
  const rect=(x,y,w,h,color)=>{g.fillStyle=color;g.fillRect(x,y,w,h);};
  const poly=(pts,color)=>{g.fillStyle=color;g.beginPath();pts.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.fill();};
  const ellipse=(x,y,rx,ry,color)=>{g.fillStyle=color;g.beginPath();g.ellipse(x,y,rx,ry,0,0,Math.PI*2);g.fill();};
  const sky=g.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#abbfb6');sky.addColorStop(.6,'#e5d5a6');sky.addColorStop(1,'#b7ac81');rect(0,0,W,H,sky);
  rect(0,65,474,348,'#8b8e72');rect(0,55,484,12,'#c0b38d');
  for(let y=78;y<408;y+=22)for(let x=-40+(Math.floor(y/22)%2)*52;x<474;x+=104){rect(x+1,y+1,101,19,'rgba(213,194,151,.12)');}
  // School doorway and an actual return interaction.
  rect(111,142,146,276,'#52675a');rect(122,152,124,265,'#3a5146');rect(132,163,103,252,'#78846a');rect(142,175,83,118,'#b7b99a');
  rect(181,175,5,118,'#5b715d');rect(142,229,83,5,'#5b715d');rect(144,315,78,84,'#65775e');ellipse(221,309,4,4,'#e1c586');
  rect(116,114,135,18,'#cbbd95');g.fillStyle='#394e3c';g.font='11px sans-serif';g.textAlign='center';g.fillText('THE CHRONICLE',183,127);g.textAlign='left';
  // Distant school wing frames a planted green courtyard.
  rect(530,213,750,194,'#a29d7b');rect(520,205,760,12,'#c9b98c');
  for(let x=548;x<1280;x+=92){rect(x,241,58,109,'#697967');rect(x+5,247,48,100,'#99ac96');rect(x+27,247,4,100,'#d0c49a');rect(x+5,292,48,4,'#d0c49a');}
  rect(0,414,W,H-414,'#a8a282');
  for(let y=414;y<H;y+=30+(y-414)*.07){rect(0,y,W,1,'rgba(72,83,61,.3)');}
  for(let x=-900;x<1900;x+=128)poly([[640+(x-640)*.35,414],[641+(x-640)*.35,414],[x+3,H],[x,H]],'rgba(76,86,65,.22)');
  poly([[474,407],[1230,407],[1280,532],[493,532]],'#657e53');poly([[487,411],[1218,411],[1246,492],[500,492]],'#849664');
  rect(483,493,776,18,'#b5ab83');
  function tree(x,y,s){poly([[x-8*s,y],[x+9*s,y],[x+5*s,y-148*s],[x-4*s,y-152*s]],'#64704b');for(let i=0;i<40;i++){const a=random()*Math.PI*2,r=random()*80*s;ellipse(x+Math.cos(a)*r,y-170*s+Math.sin(a)*r*.7,24*s+random()*20*s,19*s+random()*24*s,['#526f49','#688652','#7c925a','#8e9c63'][i%4]);}}
  tree(745,443,1.25);tree(1082,444,.9);
  // A simple waiting bench, encouraging the conclusion to feel like arrival.
  rect(802,469,200,19,'#7a714f');rect(812,492,7,31,'#4f6147');rect(984,492,7,31,'#4f6147');rect(811,435,9,48,'#53634a');rect(981,435,9,48,'#53634a');
  for(let y=437;y<465;y+=9)rect(804,y,195,6,'#a18b5c');
  const light=g.createRadialGradient(938,90,20,938,90,550);light.addColorStop(0,'rgba(255,238,180,.3)');light.addColorStop(1,'rgba(255,238,180,0)');rect(0,0,W,H,light);
  const vignette=g.createRadialGradient(640,400,230,640,400,790);vignette.addColorStop(0,'rgba(10,25,18,0)');vignette.addColorStop(1,'rgba(8,27,20,.44)');rect(0,0,W,H,vignette);
  return c;
}

function characterTexture(scene, key, npc = false) {
  const c=document.createElement('canvas');c.width=112;c.height=176;const g=c.getContext('2d');
  const ellipse=(x,y,rx,ry,color)=>{g.fillStyle=color;g.beginPath();g.ellipse(x,y,rx,ry,0,0,Math.PI*2);g.fill();};
  const shape=(points,color)=>{g.fillStyle=color;g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.fill();};
  // Soft directional shadow, feet sit at y164; anchor used by the world.
  ellipse(56,164,25,6,'rgba(8,20,17,.30)');
  const skin=npc?'#aa7454':'#b78a67', light=npc?'#c8936b':'#cda27d';
  shape([[39,102],[56,104],[54,151],[44,155],[40,139]],'#263e40');shape([[58,103],[75,102],[72,155],[61,156],[57,138]],'#30484a');
  shape([[43,150],[55,150],[55,160],[37,161],[36,157]],'#e0d7bb');shape([[62,151],[73,152],[80,158],[79,162],[61,161]],'#d6ceb4');
  shape([[36,59],[72,57],[82,105],[68,112],[39,109],[30,84]],npc?'#bd8560':'#596e5b');
  shape([[36,61],[44,61],[43,106],[34,104]],npc?'#a16e4c':'#455e51');shape([[62,60],[72,60],[78,104],[67,107]],npc?'#c7926c':'#73856b');
  shape([[38,61],[48,55],[58,60],[63,56],[70,60],[63,91],[43,91]],npc?'#e5d9be':'#d9ceb0');
  shape([[36,61],[32,66],[23,93],[28,117],[34,117],[33,94],[43,74]],npc?'#b78059':'#5d735c');ellipse(31,117,4,7,skin);
  shape([[72,61],[79,67],[87,91],[82,111],[76,109],[78,90],[66,75]],npc?'#c18b64':'#607861');ellipse(79,112,4,7,light);
  g.fillStyle=skin;g.fillRect(50,48,12,15);
  g.save();g.translate(56,48);g.scale(.66,.66);g.translate(-56,-48);ellipse(56,35,19,25,skin);ellipse(59,34,15,22,light);
  shape([[37,36],[36,18],[42,10],[56,7],[71,14],[76,31],[69,35],[66,23],[50,26],[43,21],[43,40]],npc?'#302b24':'#3b3429');
  if(npc){ellipse(39,40,7,18,'#302b24');ellipse(74,42,6,20,'#302b24');}
  ellipse(48,37,1.8,2,'#30352c');ellipse(64,37,1.8,2,'#30352c');g.strokeStyle='#946a4e';g.lineWidth=1.3;g.beginPath();g.moveTo(57,39);g.lineTo(55,45);g.lineTo(59,45);g.stroke();g.strokeStyle='#79543e';g.beginPath();g.moveTo(51,51);g.quadraticCurveTo(57,54,63,50);g.stroke();g.restore();
  if(!npc){shape([[39,66],[31,72],[36,106],[43,106]],'#273e36');g.strokeStyle='#ab9b72';g.lineWidth=3;g.beginPath();g.moveTo(39,63);g.quadraticCurveTo(54,78,68,103);g.stroke();shape([[61,90],[77,91],[80,110],[62,111]],'#a99060');}
  else {g.fillStyle='#d8c9a6';g.fillRect(42,79,25,3);}
  scene.textures.addCanvas(key,c);
}

export function createMediaRoom(parent, callbacks = {}, initialPosition) {
  let sceneRef;
  class MediaRoom extends Phaser.Scene {
    constructor(){super('MediaRoom');this.room='newsroom';this.pausedByUI=false;this.path=[];this.pendingTarget=null;this.lastSave=0;this.lastNear=null;this.walkClock=0;}
    preload(){this.load.image('media-room-photo',`${import.meta.env.BASE_URL}assets/media-room.webp`);this.load.image('courtyard-photo',`${import.meta.env.BASE_URL}assets/courtyard.webp`);}
    create(){
      sceneRef=this;seed=491;
      this.textures.addCanvas('newsroom',roomTexture());this.textures.addCanvas('courtyard',courtyardTexture());this.courtyardKey=this.textures.exists('courtyard-photo')?'courtyard-photo':'courtyard';this.hasPhoto=this.textures.exists('media-room-photo');this.newsroomKey=this.hasPhoto?'media-room-photo':'newsroom';this.background=this.add.image(0,0,this.newsroomKey).setOrigin(0).setDisplaySize(W,H);
      characterTexture(this,'student');characterTexture(this,'maya',true);
      this.npc=this.add.image(850,495,'maya').setOrigin(.5,.94).setScale(.77).setDepth(495);
      const pos=initialPosition && this.canStand(initialPosition.x,initialPosition.y)?initialPosition:{x:682,y:626};
      this.player=this.add.image(pos.x,pos.y,'student').setOrigin(.5,.94).setScale(.82).setDepth(pos.y);
      this.playerShadow=this.add.ellipse(pos.x,pos.y,32,9,0x0a1a16,.14).setDepth(pos.y-1);
      this.destination=this.add.graphics().setDepth(4);
      this.markers=[...TARGETS,...COURTYARD_TARGETS].map(t=>{
        const ring=this.add.circle(t.x,t.y,14,0x162d28,.85).setStrokeStyle(1,0xe3c889,.9).setDepth(1500);
        const icon=this.add.text(t.x,t.y,t.id==='editor'?'…':'+',{fontFamily:'Georgia, serif',fontSize:t.id==='editor'?'24px':'22px',color:'#f6dfaa'}).setOrigin(.5,.56).setDepth(1501);
        const zone=this.add.zone(t.x,t.y,88,85).setInteractive({useHandCursor:true}).setDepth(1510);
        zone.on('pointerover',()=>{ring.setFillStyle(0x947b47,.95);this.hoverTarget=t.id;});zone.on('pointerout',()=>{ring.setFillStyle(0x162d28,.85);this.hoverTarget=null;});
        zone.on('pointerdown',()=>{if(this.pausedByUI)return;this.walkTo(t.approach.x,t.approach.y,t);});
        const visible=t.id!=='return';ring.setVisible(visible);icon.setVisible(visible);zone.setVisible(visible);zone.input.enabled=visible;
        return {ring,icon,zone,target:t};
      });
      this.input.on('pointerdown',(pointer,objects)=>{
        if(this.pausedByUI||this.hoverTarget||objects?.length)return;
        if(pointer.y<395)return;
        this.walkTo(pointer.worldX,pointer.worldY);
      });
      this.keys=this.input.keyboard.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,E,SPACE');
      this.input.keyboard.removeCapture(['W','A','S','D','UP','DOWN','LEFT','RIGHT','E','SPACE']);
      this.input.keyboard.on('keydown-E',()=>this.interactNearest());this.input.keyboard.on('keydown-SPACE',e=>{if(!this.pausedByUI){e.preventDefault();this.interactNearest();}});
      this.input.keyboard.on('keydown',e=>{if(!this.pausedByUI&&['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))e.preventDefault();});
      window.__gameScene=this;
      callbacks.onReady?.(this);
    }
    setRoom(room){callbacks.onNear?.(null);this.room=room==='courtyard'?'courtyard':'newsroom';this.background.setTexture(this.room==='courtyard'?this.courtyardKey:this.newsroomKey).setDisplaySize(W,H);this.npc.setVisible(this.room==='newsroom');this.path=[];this.pendingTarget=null;this.destination.clear();this.lastNear=null;this.hoverTarget=null;this.player.setPosition(this.room==='courtyard'?310:1145,560);this.markers.forEach(m=>{const visible=this.room==='courtyard'?m.target.id==='return':m.target.id!=='return';m.ring.setVisible(visible);m.icon.setVisible(visible);m.zone.setVisible(visible);m.zone.input.enabled=visible;});callbacks.onMove?.({x:this.player.x,y:this.player.y});}
    canStand(x,y){if(this.room==='courtyard')return x>=115&&x<=1180&&y>=540&&y<=726;return x>=150&&x<=1220&&y>=440&&y<=726&&!OBSTACLES.some(r=>x>r.x-14&&x<r.x+r.w+14&&y>r.y-7&&y<r.y+r.h+10);}
    nearest(){let best=null,dist=Infinity;for(const t of this.room==='courtyard'?COURTYARD_TARGETS:TARGETS){const d=Phaser.Math.Distance.Between(this.player.x,this.player.y,t.approach.x,t.approach.y);if(d<dist){dist=d;best=t;}}return dist<112?best:null;}
    interactNearest(){if(this.pausedByUI)return;const t=this.nearest();if(t){this.path=[];this.pendingTarget=null;callbacks.onInteract?.(t.id);}}
    // Grid A* keeps click-to-walk out of desks and reaches targets around corners.
    findPath(x,y){
      const step=20,cols=64,rows=39;
      const cell=(px,py)=>({x:clamp(Math.round(px/step),0,cols-1),y:clamp(Math.round(py/step),0,rows-1)});
      const valid=(cx,cy)=>this.canStand(cx*step,cy*step);
      let goal=cell(x,y);
      if(!valid(goal.x,goal.y)){let min=Infinity;for(let cy=21;cy<37;cy++)for(let cx=6;cx<60;cx++){if(!valid(cx,cy))continue;const d=Math.hypot(cx*step-x,cy*step-y);if(d<min){min=d;goal={x:cx,y:cy};}}}
      const start=cell(this.player.x,this.player.y),key=p=>`${p.x},${p.y}`;
      const open=[{...start,g:0,f:0}],parents=new Map(),costs=new Map([[key(start),0]]);let found=null,iterations=0;
      while(open.length&&iterations++<3000){open.sort((a,b)=>a.f-b.f);const cur=open.shift();if(cur.x===goal.x&&cur.y===goal.y){found=cur;break;}
        for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
          const nx=cur.x+dx,ny=cur.y+dy;if(!valid(nx,ny)||(dx&&dy&&(!valid(cur.x+dx,cur.y)||!valid(cur.x,cur.y+dy))))continue;
          const n={x:nx,y:ny},nk=key(n),ng=cur.g+(dx&&dy?1.414:1);if(costs.has(nk)&&costs.get(nk)<=ng)continue;
          costs.set(nk,ng);parents.set(nk,cur);open.push({...n,g:ng,f:ng+Math.hypot(goal.x-nx,goal.y-ny)});
        }
      }
      if(!found)return [];
      const path=[];let cur=found;while(key(cur)!==key(start)){path.unshift({x:cur.x*step,y:cur.y*step});cur=parents.get(key(cur));if(!cur)break;}
      if(this.canStand(x,y))path.push({x,y});return path;
    }
    walkTo(x,y,target=null){this.path=this.findPath(x,y);this.pendingTarget=target;const end=this.path.at(-1);this.destination.clear();if(end){this.destination.lineStyle(1,0xdcca92,.7);this.destination.strokeEllipse(end.x,end.y,21,8);this.destination.fillStyle(0xf3df9e,.7);this.destination.fillCircle(end.x,end.y,2);}if(!this.path.length&&target&&this.nearest()?.id===target.id)callbacks.onInteract?.(target.id);}
    update(time,delta){
      if(!this.player||this.pausedByUI)return;
      const dt=Math.min(delta,40)/1000;let vx=0,vy=0;
      if(this.keys.A.isDown||this.keys.LEFT.isDown)vx--;if(this.keys.D.isDown||this.keys.RIGHT.isDown)vx++;
      if(this.keys.W.isDown||this.keys.UP.isDown)vy--;if(this.keys.S.isDown||this.keys.DOWN.isDown)vy++;
      if(vx||vy){this.path=[];this.pendingTarget=null;this.destination.clear();}
      else if(this.path.length){const p=this.path[0],dx=p.x-this.player.x,dy=p.y-this.player.y,d=Math.hypot(dx,dy);if(d<6){this.path.shift();if(!this.path.length){this.destination.clear();if(this.pendingTarget){const target=this.pendingTarget;this.pendingTarget=null;callbacks.onInteract?.(target.id);return;}}}else {vx=dx/d;vy=dy/d;}}
      const moving=!!(vx||vy);
      if(moving){const norm=Math.hypot(vx,vy),speed=167;vx=vx/norm*speed*dt;vy=vy/norm*speed*dt;
        if(this.canStand(this.player.x+vx,this.player.y))this.player.x+=vx;
        if(this.canStand(this.player.x,this.player.y+vy))this.player.y+=vy;
        this.walkClock+=delta*.012;this.player.setAngle(Math.sin(this.walkClock)*1.3);if(vx<-0.1)this.player.setFlipX(true);else if(vx>.1)this.player.setFlipX(false);
      } else this.player.setAngle(0);
      const baseScale=.70+(this.player.y-422)/304*.18;this.player.setScale(baseScale,baseScale+(moving?Math.sin(this.walkClock*2)*.007:0));this.player.setDepth(this.player.y);
      this.playerShadow.setPosition(this.player.x,this.player.y+2).setDepth(this.player.y-1);
      const near=this.nearest();if(near?.id!==this.lastNear){this.lastNear=near?.id;callbacks.onNear?.(near?{id:near.id,label:near.label}:null);}
      this.markers.forEach((m,i)=>{m.ring.setScale(1+Math.sin(time*.002+i)*.04);});
      if(moving&&time-this.lastSave>700){this.lastSave=time;callbacks.onMove?.({x:Math.round(this.player.x),y:Math.round(this.player.y)});}
    }
  }
  const game=new Phaser.Game({type:Phaser.CANVAS,parent,width:W,height:H,backgroundColor:'#253e37',transparent:false,render:{antialias:true,roundPixels:false},scale:{mode:Phaser.Scale.FIT,autoCenter:Phaser.Scale.CENTER_BOTH},scene:[MediaRoom],audio:{noAudio:true},input:{keyboard:true},banner:false});
  return {game,setRoom(room){sceneRef?.setRoom(room);},setPaused(paused){if(sceneRef){sceneRef.pausedByUI=paused;if(paused){sceneRef.path=[];sceneRef.pendingTarget=null;sceneRef.destination.clear();sceneRef.input.keyboard.resetKeys();}}},focus(){game.canvas?.focus();},destroy(){if(window.__gameScene===sceneRef)delete window.__gameScene;game.destroy(true);}};
}
