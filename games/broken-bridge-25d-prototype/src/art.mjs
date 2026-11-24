// All primary scenery, characters and inspectable objects are authored raster assets.
export function loadArt(scene) {
  Object.entries(ART).forEach(([name, url]) => scene.load.image(name, url));
}

export function illustratedWorld(scene) {
  const add = (key,x,y,width,height,depth,originX=0,originY=0) =>
    scene.add.image(x,y,key).setOrigin(originX,originY).setDisplaySize(width,height).setDepth(depth);
  add('scenery-distance',-45,0,1150,540,-2).setScrollFactor(.91,1);
  add('scenery-bank',0,0,1060,540,0);
  const canopy=add('storm-canopy',-39,-38,425,165,582).setScrollFactor(1.08,1);
  add('storm-boulder',332,474,71,43,474,.5,1);
  const debris=add('storm-debris',397,430,81,31,428,.5,1);
  const current=add('current',209,272,596,137,1).setAlpha(.23);
  const frontLeft=add('front-left',0,445,266,95,550).setScrollFactor(1.035,1);
  const frontRight=add('front-right',830,450,230,90,550).setScrollFactor(1.035,1);
  const lamp=scene.add.ellipse(70,287,67,50,0xffb250,.014).setDepth(2);
  const bridge=add('bridge-damaged-v3',450,416,139,125,4,.5,1);
  const fill=[0,1].map(i=>add('bridge-patch-v3-'+i,450,416,139,125,5,.5,1).setVisible(false));
  const rack=add('rack-loaded',113,438,55,48,438,.5,1);
  const parcel=add('supplies',204,431,30,21,431,.5,1);
  add('depth',778,414,39,51,414,.5,1);
  add('sign',934,449,58,32,449,.5,1);
  const flags=[
    add('flag-0',954,415,21,40,415,.5,1).setFlipX(true),
    add('flag-1',857,310,18,34,310,.5,1),
  ];
  const actor = (role, height) => ({
    image: add(role+'-v3-0',0,0,height*160/192,height,20,.5,188/192),
    shadow: scene.add.ellipse(0,0,22,6,0x171b15,.35),
    role,height, gait:0, direction:'right',
  });
  const carry=add('board',0,0,1,1,20,.5,.5).setVisible(false);
  return {current,frontLeft,frontRight,canopy,debris,lamp,bridge,fill,rack,flags,parcel,carry,
    ranger:actor('ranger',73), scout:actor('scout',66)};
}

export function paintWorld(art,time,state) {
  art.current.x=209+Math.sin(time*.78)*7;
  art.current.alpha=.18+.06*Math.sin(time*1.2);
  art.frontLeft.x=Math.sin(time*.82)*1.5;
  art.frontRight.x=830+Math.sin(time*.66)*1.8;
  art.lamp.fillAlpha=.014+.008*Math.sin(time*1.9);
  art.canopy.setRotation(Math.sin(time*.64)*.004);
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
  actor.shadow.setPosition(x+footShift,y).setDisplaySize(24*scale,6*scale).setDepth(y)
    .setAlpha(walking?(frame%3===0?.93:.76):1);
}
