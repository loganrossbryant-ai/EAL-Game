import {makeRiver} from './river.mjs';

// All primary scenery, characters and inspectable objects are authored raster assets.
export function loadArt(scene) {
  Object.entries(ART).forEach(([name, url]) => scene.load.image(name, url));
}

export function illustratedWorld(scene) {
  const add = (key,x,y,width,height,depth,originX=0,originY=0) =>
    scene.add.image(x,y,key).setOrigin(originX,originY).setDisplaySize(width,height).setDepth(depth);
  add('scenery-distance',-45,0,1150,540,-2).setScrollFactor(.91,1);
  add('scenery-bank',0,0,1060,540,0);
  add('storm-canopy',-39,-38,425,165,582).setScrollFactor(1.08,1);
  add('storm-boulder',332,474,71,43,474,.5,1);
  const debris=add('storm-debris',397,430,81,31,428,.5,1);
  add('front-left',0,445,266,95,550).setScrollFactor(1.035,1);
  add('front-right',830,450,230,90,550).setScrollFactor(1.035,1);
  // The pivot is at each plant's attachment point. Roots and trunks remain grounded.
  const plant=(id,x,y,w,h,depth,ox,oy,phase,strength,hz,scroll=1)=>({
    image:add('wind-'+id,x,y,w,h,depth,ox,oy).setScrollFactor(scroll,1),phase,strength,hz,
  });
  const wind=[
    plant('fern',74,532,139,117,562,.49,.96,0,.10,.23,1.035),
    plant('fern',992,544,172,145,565,.51,.95,2.4,.10,.17,1.043),
    plant('reed',520,401,42,63,400,.50,.99,1.6,.15,.33),
    plant('reed',737,405,42,66,405,.49,.98,3.1,.17,.26),
    plant('reed',823,478,43,68,492,.50,.98,5.1,.12,.19),
    plant('fir',1078,22,260,169,580,.97,.05,4.5,.085,.13,1.04),
    plant('cedar',278,25,156,139,64,.02,.035,3.6,.070,.21,.97),
  ];
  const mist=[
    {image:add('ridge-mist',432,145,305,71,-.5).setScrollFactor(.97,1),x:432,y:145,phase:1,speed:.64},
    {image:add('ridge-mist',670,191,320,64,-.4).setScrollFactor(.99,1),x:670,y:191,phase:3,speed:.47},
    {image:add('ridge-mist',561,257,232,37,1).setScrollFactor(1,1),x:561,y:257,phase:4.4,speed:.53},
  ];
  const paintRiver=makeRiver(scene);
  const lamp=scene.add.ellipse(70,287,67,50,0xffb250,.014).setDepth(2);
  const bridge=add('bridge-damaged-v3',450,416,139,125,4,.5,1);
  const fill=[0,1].map(i=>add('bridge-patch-v3-'+i,450,416,139,125,5,.5,1).setVisible(false));
  const rack=add('rack-loaded',113,438,55,48,438,.5,1);
  const parcel=add('supplies',204,431,30,21,431,.5,1);
  add('depth',778,414,39,51,414,.5,1);
  add('sign',934,449,58,32,449,.5,1);
  const notice=add('sign',316,423,42,24,423,.43,.88);
  const caution=add('flag-0',317,422,15,26,424,.48,1);
  const flags=[
    add('flag-0',954,415,21,40,415,.5,1).setFlipX(true),
    add('flag-1',857,310,18,34,310,.5,1),
  ];
  const actor = (role, height) => ({
    image: add(role+'-v3-0',0,0,height*160/192,height,20,.5,188/192),
    shadow: scene.add.ellipse(0,0,22,6,0x171b15,.50),
    penumbra: scene.add.ellipse(0,0,35,9,0x252317,.23),
    role,height, gait:0, direction:'right',
  });
  const carry=add('board',0,0,1,1,20,.5,.5).setVisible(false);
  return {wind,mist,paintRiver,notice,caution,debris,lamp,bridge,fill,rack,flags,parcel,carry,
    ranger:actor('ranger',88), scout:actor('scout',81)};
}

export function paintWorld(art,time,state,splashes,noticeMode) {
  // Separate wind, mist and current clocks keep the view alive while the camera holds.
  for(const {image,phase,strength,hz} of art.wind){
    const beat=time*hz*Math.PI*2;
    image.rotation=strength*(Math.sin(beat+phase)+.24*Math.sin(beat*2.3+phase));
  }
  for(const {image,x,y,phase,speed} of art.mist){
    image.x=x+Math.sin(time*speed+phase)*29;
    image.y=y+Math.sin(time*speed*.61+phase)*7;
    image.alpha=.51+.21*Math.sin(time*speed*.77+phase);
  }
  art.paintRiver(time,splashes);
  art.lamp.fillAlpha=.034+.016*Math.sin(time*3.1)+.007*Math.sin(time*5.5);
  const noticeClosed=state.fieldEdition===6&&!state.survey.corrected||noticeMode==='pending';
  art.notice.setVisible(state.fieldEdition===6).setAngle(noticeClosed?-14:10).setFlipX(noticeClosed);
  art.caution.setVisible(noticeClosed);
  const visualKey=state.id+'|'+state.route+'|'+state.pieces.join('|');
  if(art.visualKey===visualKey)return;
  art.visualKey=visualKey;
  const repaired=state.delivered&&state.route==='bridge';
  art.debris.setVisible(!repaired);
  art.bridge.setTexture(repaired?'bridge-restored-v3':'bridge-damaged-v3').setDisplaySize(139,125);
  art.fill.forEach((image,i)=>image.setVisible(!repaired&&state.pieces.includes(['boardA','boardB'][i])));
  art.rack.setTexture(state.route==='bridge'?'rack':'rack-loaded').setDisplaySize(55,48);
  art.flags.forEach((flag,i)=>flag.setVisible(state.pieces.includes(['postA','postB'][i])));
}

export function figure(actor,x,y,{face=1,gesture=false,pose='',carrying=false}={}) {
  const dx=x-(actor.x??x),dy=y-(actor.y??y);
  const distance=Math.hypot(dx,dy);
  const moving=distance>.065&&distance<35;
  const scale=.83+(y-300)*.00118;
  if(moving) {
    const direction=Math.abs(dy)>Math.abs(dx)*.68?(dy<0?'up':'down'):(dx<0?'left':'right');
    if(direction!==actor.direction) {actor.gait=0;actor.direction=direction;}
    actor.gait=(actor.gait+distance/(63*scale))%1;
  } else actor.gait=0;
  actor.x=x;actor.y=y;
  const frame=Math.floor(actor.gait*6);
  const cycle=actor.role+'-v4-'+actor.direction+'-'+frame;
  const posed=actor.role+'-v4-'+(pose||(carrying?'hold':''));
  const resolvedPose=(pose||(!moving&&carrying))&&actor.image.scene.textures.exists(posed);
  const walking=moving&&actor.image.scene.textures.exists(cycle);
  const key=resolvedPose?posed:walking?cycle:actor.role+'-v3-'+(gesture?3:0);
  actor.key=key;
  actor.action=carrying?'carry':moving?'walk':pose|| (gesture?'gesture':'idle');
  actor.image.setTexture(key).setPosition(x,y)
    .setDisplaySize(actor.height*160/192*scale,actor.height*scale).setDepth(y+.3)
    .setFlipX(!walking&&face<0);
  const footShift=walking?Math.cos(frame*Math.PI/3)*2:0;
  actor.penumbra.setPosition(x+4,y+1).setDisplaySize(37*scale,10*scale).setDepth(y-.05);
  actor.shadow.setPosition(x+footShift,y).setDisplaySize(27*scale,6*scale).setDepth(y)
    .setAlpha(walking?(frame%3===0?.93:.76):1);
}
