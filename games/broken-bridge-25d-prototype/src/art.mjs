// All primary scenery, characters and inspectable objects are authored raster assets.
export function loadArt(scene) {
  Object.entries(ART).forEach(([name, url]) => scene.load.image(name, url));
}

export function illustratedWorld(scene) {
  const add = (key,x,y,width,height,depth,originX=0,originY=0) =>
    scene.add.image(x,y,key).setOrigin(originX,originY).setDisplaySize(width,height).setDepth(depth);
  add('forest',0,0,1060,540,0);
  const current=add('current',209,272,596,137,1).setAlpha(.23);
  const frontLeft=add('front-left',0,445,266,95,550).setScrollFactor(1.035,1);
  const frontRight=add('front-right',830,450,230,90,550).setScrollFactor(1.035,1);
  const lamp=scene.add.ellipse(70,287,67,50,0xffb250,.014).setDepth(2);
  const bridge=add('broken',450,413,111,119,4,.5,1);
  const fill=[0,1].map(i=>add('bridge-fill-'+i,450,413,111,119,5,.5,1).setVisible(false));
  const rack=add('rack-loaded',113,438,55,48,438,.5,1);
  const parcel=add('supplies',204,431,30,21,431,.5,1);
  add('depth',778,414,39,51,414,.5,1);
  add('sign',934,449,58,32,449,.5,1);
  const flags=[
    add('flag-0',954,415,21,40,415,.5,1).setFlipX(true),
    add('flag-1',857,310,18,34,310,.5,1),
  ];
  const actor = (role, height) => ({
    image: add(role+'-0',0,0,height*160/192,height,20,.5,188/192),
    shadow: scene.add.ellipse(0,0,22,6,0x171b15,.35),
    role,height,
  });
  return {current,frontLeft,frontRight,lamp,bridge,fill,rack,flags,parcel,
    ranger:actor('ranger',73), scout:actor('scout',66)};
}

export function paintWorld(art,time,state) {
  art.current.x=209+Math.sin(time*.78)*7;
  art.current.alpha=.18+.06*Math.sin(time*1.2);
  art.frontLeft.x=Math.sin(time*.82)*1.5;
  art.frontRight.x=830+Math.sin(time*.66)*1.8;
  art.lamp.fillAlpha=.014+.008*Math.sin(time*1.9);
  const repaired=state.delivered&&state.route==='bridge';
  art.bridge.setTexture(repaired?'repaired':'broken').setDisplaySize(111,119);
  art.fill.forEach((image,i)=>image.setVisible(!repaired&&state.pieces.includes(['boardA','boardB'][i])));
  art.rack.setTexture(state.pieces.includes('boardA')&&state.pieces.includes('boardB')?'rack':'rack-loaded').setDisplaySize(55,48);
  art.flags.forEach((flag,i)=>flag.setVisible(state.pieces.includes(['postA','postB'][i])));
}

export function figure(actor,x,y,{step=0,face=1,gesture=false}={}) {
  const frame=gesture?3:step?[0,1,0,2][Math.floor(step/2)%4]:0;
  const scale=.83+(y-300)*.00118;
  actor.image.setTexture(actor.role+'-'+frame).setPosition(x,y)
    .setDisplaySize(actor.height*160/192*scale,actor.height*scale).setDepth(y+.3).setFlipX(face<0);
  actor.shadow.setPosition(x+4,y).setDisplaySize(24*scale,6*scale).setDepth(y);
}
